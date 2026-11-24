"""The scene sheet: the facts of each screen, worked out from the merged TOML, so prose is read against them.

    venv/bin/python .claude/skills/author-game-lean/scripts/sheet.py games/<slug> <id>
        prints the computed sheet for the canvases on the card's Builds: line, in the card's Sheet: format

One row per screen, every path into it merged:

    <canvas>.<node> | <clock in>–<clock out> | <place> | <who is there> | <what she wears> | <flags set>

How each column is worked out (LO, relayed 2026-11-24: "Commit and continue", the plan's Part C):
  clock    the starting canvas starts at [time] starting_day / starting_hour, minute 0 (v2.py:1592-1593); a
           repeatable starts in its trigger's time_of_day window ("07:00–09:00"), or "any" with none. Each choice adds
           its time_progression_minutes, 3 when it has none (v2.py:17755, 17758). In and out are the screen's first
           minute and the minute its choice leaves it; a repeatable's are written "+<n>" from the scene's start.
           A repeatable bound to a person with no window reads "while <id> is there": who else is there is
           worked out over the minutes that person's rows put them at the place.
  place    the canvas trigger's location. A screen of a canvas with no location (the opening) has no place the
           engine knows: the place is the card's, marked "(card)", and who is there is worked out at it.
  who      people whose schedule rows (who_is_where.where) put them at the place at every five-minute slot the
           screen can show at (its first minute, on every day and time the scene can start; not the time its choice
           then spends); "<id> (part)" when only at some; the scene's bound person (trigger npc / requires_npc) is
           always there. "nobody" when no one is.
  wearing  on the starting canvas: the `initial` garments, equipped in file order (v2.py:1213-1235), then each
           wardrobeEffects equip / unequip / remove on the path, with the dress rule of setup.equipItem
           (v2.py:1760-1766). On a repeatable: the garments its trigger checks as equipped, else "any".
  flags    flags set by choices on the path before the screen, plus flags the trigger checks is_true. Flags set on
           only some paths come after "by path:".

A screen it can't model (a canvas with no place the engine knows and no card place, or one no path reaches) is
"?" in that column, and check.py's `sheet` is INCOMPLETE for it, never green.
"""
import re
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import who_is_where  # noqa: E402
from scenes import guaranteed  # noqa: E402

DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
DEFAULT_MINUTES = 3  # v2.py:17755
SLOTS_OF = ("bra", "underwear", "top", "bottom", "dress", "legwear", "shoes")
COLUMNS = ("screen", "clock", "place", "who", "wearing", "flags")


def hhmm(m):
    m %= 1440
    return f"{m // 60:02d}:{m % 60:02d}"


def items(conditions):
    out = []

    def visit(d):
        if isinstance(d, dict):
            if d.get("type"):
                out.append(d)
            for v in d.values():
                visit(v)
        elif isinstance(d, list):
            for v in d:
                visit(v)
    visit(conditions)
    return out


# ── paths ─────────────────────────────────────────────────────────────────────────────────────────────────

def walks(c):
    """[(node id, minutes in, the choice that leaves it or None)] for every path from the first screen."""
    nodes = {n.get("id"): n for n in c.get("nodes") or [] if n.get("id")}
    first = (c.get("nodes") or [{}])[0].get("id")
    if first is None:
        return []
    out, stack = [], [([], first, 0)]
    while stack:
        done, nid, t = stack.pop()
        if any(d[0] == nid for d in done):
            out.append(done)
            continue
        choices = (nodes[nid].get("exit_block") or {}).get("choices") or []
        inner = []
        for ch in choices:
            to = str(ch.get("nodeId") or "")
            to = to.split(".", 1)[1] if to.startswith(c["id"] + ".") else to
            if ch.get("targetType", "trigger") == "node" and to in nodes:
                inner.append((ch, to))
        if not inner:
            out.append(done + [(nid, t, choices[0] if choices else None)])
            continue
        for ch, to in inner:
            m = ch.get("time_progression_minutes", DEFAULT_MINUTES)
            stack.append((done + [(nid, t, ch)], to, t + int(m or 0)))
        if len(out) > 500:
            break
    return out


def leave_minutes(ch):
    return int(ch.get("time_progression_minutes", DEFAULT_MINUTES) or 0) if ch else 0


# ── state along a path ────────────────────────────────────────────────────────────────────────────────────

def start_outfit(game):
    """{slot: item id} at the start, per v2.py:1213-1235."""
    eq = dict.fromkeys(SLOTS_OF)
    for it in game.get("clothing") or []:
        if isinstance(it, dict) and it.get("initial"):
            wear(eq, it, game)
    return eq


def wear(eq, it, game):
    slot = it.get("slot")
    if slot == "dress":
        eq["top"] = eq["bottom"] = None
    if slot in ("top", "bottom"):
        eq["dress"] = None
    eq[slot] = it.get("id")


def apply_wardrobe(eq, ch, game):
    byid = {i.get("id"): i for i in game.get("clothing") or [] if isinstance(i, dict)}
    for ef in (ch or {}).get("wardrobeEffects") or []:
        act, iid = ef.get("action"), ef.get("item_id")
        if act == "equip" and iid in byid:
            wear(eq, byid[iid], game)
        elif act in ("unequip", "remove"):
            for s, v in eq.items():
                if v == iid:
                    eq[s] = None


def set_flags(flags, ch):
    for ef in (ch or {}).get("flagEffects") or []:
        if isinstance(ef, dict) and ef.get("flag"):
            if ef.get("op", "set") == "set":
                flags.add(ef["flag"])
            elif ef.get("op") == "unset":
                flags.discard(ef["flag"])


# ── who is there ──────────────────────────────────────────────────────────────────────────────────────────

def slots_between(day, start, end):
    """Five-minute slots from start (inclusive) to end (exclusive; the start slot when they're equal)."""
    end = max(end, start + who_is_where.STEP)
    return [((day + m // 1440) % 7, (m % 1440) // who_is_where.STEP * who_is_where.STEP)
            for m in range(start, end, who_is_where.STEP)]


def present(where, place, slots, bound=()):
    """Sorted labels: '<id>' there at every slot, '<id> (part)' at some."""
    out = []
    for pid, table in sorted(where.items()):
        places = [{p for p, _ in table.get(s, ())} for s in slots]
        hits = [place in ps for ps in places]
        if pid in bound or (slots and all(ps == {place} for ps in places)):
            out.append(pid)
        elif any(hits):
            out.append(f"{pid} (part)")
    for pid in sorted(set(bound) - set(where)):
        out.append(pid)
    return sorted(set(out)) or ["nobody"]


# ── the sheet ─────────────────────────────────────────────────────────────────────────────────────────────

def window(trig):
    for i in items(trig.get("conditions")):
        if i.get("type") == "time_of_day":
            return who_is_where.minutes(i.get("start_time")), who_is_where.minutes(i.get("end_time"))
    return None


def days_text(trig):
    days = [i.get("weekdays") for i in items(trig.get("conditions")) if i.get("type") == "weekday"]
    if not days:
        return ""
    names = who_is_where.DAYS
    return " · " + " / ".join(" ".join(names[d] for d in sorted(set(ds or [])) if 0 <= d < 7) or "no day" for ds in days)


def clock_text(trig, win, bound, place, minute):
    if win and win[0] is not None:
        s, e = win
        e = s + 60 if e is None else (e if e > s else e + 1440)
        head = f"{hhmm(s)}–{hhmm(e)} +{minute}"
    elif bound and place:
        head = f"while {sorted(bound)[0]} is there +{minute}"
    else:
        head = f"any +{minute}"
    return head + days_text(trig)


def shifted(starts, minute, until):
    """The slots a screen is on, from the slots its scene can start at: from start + minute to start + until."""
    out = set()
    for d, m in starts:
        out.update(slots_between(d, m + minute, m + until))
    return out


def shift_slot(slot, minutes):
    d, m = slot
    k = m + minutes
    return ((d + k // 1440) % 7, (k % 1440) // who_is_where.STEP * who_is_where.STEP)


def choice_narrow(starts, minute, ch):
    """The scene-start slots left after a choice whose own conditions read the clock (a weekday, a time_of_day),
    checked at the minute the choice is taken. A choice with no clock condition leaves them as they were."""
    allowed = who_is_where.when_slots(ch.get("conditions"))
    if len(allowed) == len(who_is_where.SLOTS):
        return starts
    return {s for s in starts if shift_slot(s, minute) in allowed}


def node_starts(c, base):
    """{node id: the scene-start slots it can show at}: the union over every path into it of `base` narrowed by each
    choice's clock conditions on the way (choice_narrow). Shared with scenes.check_presence."""
    out = {}
    for path in walks(c):
        starts = set(base)
        for nid, minute, ch in path:
            out.setdefault(nid, set()).update(starts)
            if ch:
                starts = choice_narrow(starts, minute, ch)
    return out


def fmt_slots(slots):
    """A clock cell for a narrowed screen, from the slots it shows at: "08:05–12:00 · Sun", or one part per day,
    joined " / ", when the days differ."""
    if not slots:
        return "never"
    step = who_is_where.STEP
    runs = {}
    for d in range(7):
        mins = sorted(m for dd, m in slots if dd == d)
        parts, s = [], None
        for i, m in enumerate(mins):
            if s is None:
                s = m
            if i + 1 == len(mins) or mins[i + 1] != m + step:
                parts.append((s, m + step))
                s = None
        if parts:
            runs[d] = tuple(parts)
    names = who_is_where.DAYS
    by_shape = {}
    for d in sorted(runs):
        by_shape.setdefault(runs[d], []).append(d)  # days with the same hours print together
    parts = []
    for shape, days in sorted(by_shape.items(), key=lambda x: x[1][0]):
        parts += [f"{hhmm(a)}–{hhmm(b)} · {' '.join(names[d] for d in days)}" for a, b in shape]
    return " / ".join(parts)


def fmt_flags(per_path):
    if not per_path:
        return "?"
    common = set.intersection(*per_path)
    some = set.union(*per_path) - common
    text = ", ".join(sorted(common)) or "none"
    return text + (f"; by path: {', '.join(sorted(some))}" if some else "")


def fmt_join(values):
    return " / ".join(sorted(set(values))) if values else "?"


def compute(game, canvas_ids, card_places=None):
    """{screen: {column: text}} for every screen of the named canvases."""
    card_places = card_places or {}
    where = who_is_where.where(game)
    start_id = (game.get("project") or {}).get("starting_canvas")
    t = game.get("time") or {}
    start_day = DAYS.index(t.get("starting_day", "Monday")) if t.get("starting_day", "Monday") in DAYS else 0
    start_min = int(t.get("starting_hour", 0) or 0) * 60
    out = {}
    for c in game.get("canvases") or []:
        cid = c.get("id")
        if cid not in canvas_ids:
            continue
        trig = c.get("trigger") or {}
        is_start = cid == start_id
        bound = {trig.get("npc"), trig.get("requires_npc")} - {None}
        win = None if is_start else window(trig)
        acc = {}
        base = None
        if not is_start:
            base = who_is_where.when_slots(trig.get("conditions"))
            if bound and trig.get("location"):
                # A scene bound to a person shows only while they're there (requires_npc).
                table = where.get(sorted(bound)[0], {})
                base = {s for s in base if trig.get("location") in {p for p, _ in table.get(s, ())}}
        grouped = not is_start and any(i.get("type") == "group" for i in (trig.get("conditions") or {}).get("items") or []
                                         if isinstance(i, dict)) and base is not None and len(base) < len(who_is_where.SLOTS)
        for path in walks(c):
            eq = start_outfit(game) if is_start else None
            # a choice's own clock conditions narrow the screens after it (P34); a trigger whose clock is a group
            # ("weekdays 7-21 OR weekends 10-21") is written from its slots, part by part, from the first screen
            starts, narrowed = base, grouped
            flags = guaranteed(trig.get("conditions"), "flag", "flag_key", "is_true")
            for nid, minute, ch in path:
                key = f"{cid}.{nid}"
                row = acc.setdefault(key, {"clock": [], "who": [], "wearing": [], "flags": [], "place": None})
                out_m = minute + leave_minutes(ch)
                place = trig.get("location")
                place_txt = place
                if not place and key in card_places:
                    place, place_txt = card_places[key], f"{card_places[key]} (card)"
                row["place"] = place_txt or "?"
                if is_start:
                    row["clock"].append(f"{hhmm(start_min + minute)}–{hhmm(start_min + out_m)}")
                    # Who is there is read at the minute the screen shows, not across the time its choice spends
                    # (a "Work a shift (4 hours)" button would otherwise mark everyone who leaves mid-shift "(part)").
                    slots = slots_between(start_day, start_min + minute, start_min + minute)
                else:
                    slots = shifted(starts, minute, minute + who_is_where.STEP)
                    row["clock"].append(fmt_slots(slots) if narrowed else clock_text(trig, win, bound, place, minute))
                row["who"].append(", ".join(present(where, place, slots, bound)) if place else "?")
                if eq is not None:
                    worn = sorted(v for v in eq.values() if v)
                    row["wearing"].append(", ".join(worn) or "none")
                else:
                    checked = sorted(guaranteed(trig.get("conditions"), "clothing_item", "item_id", "equipped"))
                    row["wearing"].append(", ".join(checked) or "any")
                row["flags"].append(set(flags))
                if eq is not None:
                    apply_wardrobe(eq, ch, game)
                set_flags(flags, ch)
                if starts is not None and ch:
                    after = choice_narrow(starts, minute, ch)
                    narrowed, starts = narrowed or after != starts, after
        for node in c.get("nodes") or []:
            key = f"{cid}.{node.get('id')}"
            r = acc.get(key)
            if r is None:
                out[key] = dict.fromkeys(COLUMNS[1:], "?")
                continue
            out[key] = {"clock": fmt_join(r["clock"]), "place": r["place"], "who": fmt_join(r["who"]),
                        "wearing": fmt_join(r["wearing"]), "flags": fmt_flags(r["flags"])}
    return out


def line(screen, row):
    return " | ".join([screen] + [row[c] for c in COLUMNS[1:]])


# ── the card's sheet ──────────────────────────────────────────────────────────────────────────────────────

def card_sheet(text):
    """{screen: {column: text}} from the card's `Sheet:` block, or None when the card has none."""
    m = re.search(r"^Sheet:[ \t]*\n((?:[ \t]+\S.*\n?)*)", text, re.M)
    if not m:
        return None
    out = {}
    for raw in m.group(1).splitlines():
        cells = [x.strip() for x in raw.split("|")]
        if len(cells) == len(COLUMNS) and not cells[0].startswith("<"):
            out[cells[0]] = dict(zip(COLUMNS[1:], cells[1:]))
    return out


def card_info(game_dir, card_id):
    text = (Path(game_dir) / "cards" / f"{card_id}.md").read_text(encoding="utf-8")
    b = re.search(r"^Builds:[ \t]*(.*)$", text, re.M)
    ids = {x.strip(" `") for x in (b.group(1).split(",") if b else [])}
    return text, ids


def places_from(sheet):
    out = {s: r["place"].replace("(card)", "").strip() for s, r in (sheet or {}).items()}
    return {s: v for s, v in out.items() if v and v != "?" and not v.startswith("<")}


def for_card(game, game_dir, card_id):
    """(the card's sheet or None, the computed sheet for its canvases)."""
    text, ids = card_info(game_dir, card_id)
    mine = card_sheet(text)
    canvases = {c.get("id") for c in game.get("canvases") or []} & ids
    return mine, compute(game, canvases, places_from(mine))


DAY_NAMES = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
DAY_WORDS = {"weekdays": range(0, 5), "weekends": range(5, 7), "weekend": range(5, 7), "daily": range(7),
             "every day": range(7)}
TIMES = re.compile(r"(\d{1,2}):(\d{2})\s*[–-]\s*(\d{1,2}):(\d{2})")


def parse_days(text):
    """The days a clock cell names, 0 = Monday, or None when it names none (every day)."""
    low = text.lower()
    days = set()
    for word, rng in DAY_WORDS.items():
        if re.search(rf"\b{word}\b", low):
            days |= set(rng)
    for a, b in re.findall(r"\b(mon|tue|wed|thu|fri|sat|sun)\w*\s*[–-]\s*(mon|tue|wed|thu|fri|sat|sun)\w*", low):
        i, j = DAY_NAMES.index(a), DAY_NAMES.index(b)
        days |= set(range(i, j + 1)) if i <= j else set(range(i, 7)) | set(range(0, j + 1))
    low = re.sub(r"\b(mon|tue|wed|thu|fri|sat|sun)\w*\s*[–-]\s*(mon|tue|wed|thu|fri|sat|sun)\w*", "", low)
    days |= {DAY_NAMES.index(d) for d in re.findall(r"\b(mon|tue|wed|thu|fri|sat|sun)\w*", low)}
    return days or None


def clock_meaning(text, exact):
    """What a clock cell means, so a card written by hand compares with the build by meaning, not by text.
    exact (the starting canvas): the in and out minutes. Otherwise: the (day, minute) slots the screen shows at,
    the window shifted by "+N" (none means the window is already the screen's), on the days named (none: every day).
    "while <id> is there" and "any" keep their words. A cell it can't read compares as text."""
    low = text.lower().replace("any minute", "")
    if " / " in low and not exact:
        # several parts (paths, or days with different hours): the union of their slots
        parts = [clock_meaning(x, exact) for x in low.split(" / ")]
        if all(p[0] == "slots" for p in parts):
            return ("slots", frozenset().union(*(p[1] for p in parts)))
    m = TIMES.search(low)
    off = re.search(r"\+\s*(\d+)", low)
    n = int(off.group(1)) if off else 0
    if "while" in low:
        return ("while", re.sub(r"\s+", " ", low.split("+")[0].strip()), n, frozenset(parse_days(low) or range(7)))
    if exact:
        return ("exact", tuple(int(x) for x in m.groups())) if m else ("text", low.strip())
    if m:
        s = int(m.group(1)) * 60 + int(m.group(2))
        e = int(m.group(3)) * 60 + int(m.group(4))
        e = e if e > s else e + 1440
    elif re.search(r"\bany\b", low):
        s, e = 0, 1440
    else:
        return ("text", low.strip())
    days = parse_days(low) or set(range(7))
    step = who_is_where.STEP
    return ("slots", frozenset(((d + (k // 1440)) % 7, k % 1440) for d in days for k in range(s + n, e + n, step)))


def norm(col, text, exact=False):
    if col == "clock":
        return clock_meaning(text, exact)
    """A cell as the sheet means it: the clock by its slots (clock_meaning); who, wearing and flags as sets, so their
    order on the card doesn't matter."""
    if col not in ("who", "wearing", "flags"):
        return text.strip()
    head, _, by_path = text.partition("; by path:")
    def sets(s):
        alts = {tuple(sorted(x.strip() for x in alt.split(",") if x.strip())) for alt in s.split(" / ")}
        return tuple(sorted(alts))
    return sets(head), sets(by_path)


def compare(mine, computed):
    """(red rows, incomplete rows)."""
    red, inc = [], []
    for s in sorted(set(computed) - set(mine)):
        red.append(f"{s} is built but not on the card's Sheet:")
    for s in sorted(set(mine) - set(computed)):
        red.append(f"{s} is on the card's Sheet: but not built")
    for s in sorted(set(mine) & set(computed)):
        got, want = computed[s], mine[s]
        exact = "+" not in got["clock"] and "while" not in got["clock"] and "any" not in got["clock"]
        for col in COLUMNS[1:]:
            if got[col] == "?":
                inc.append(f"{s} · {col}: the sheet can't work it out")
            elif col == "place" and got[col].endswith("(card)"):
                continue  # the card's own place: who is there is checked at it
            elif norm(col, got[col], exact) != norm(col, want[col], exact):
                red.append(f"{s} · {col}: the card says \"{want[col]}\", the build says \"{got[col]}\"")
    return red, inc


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 2:
        print(__doc__)
        return 2
    game_dir, card_id = Path(args[0]), args[1]
    game = tomllib.loads((game_dir / "toml_phases" / "7_final_game.toml").read_text(encoding="utf-8"))
    mine, computed = for_card(game, game_dir, card_id)
    print("Sheet:")
    for s, row in computed.items():
        print("  " + line(s, row))
    return 0


if __name__ == "__main__":
    sys.exit(main())
