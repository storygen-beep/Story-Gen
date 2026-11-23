"""The scene sheet: the facts of each screen, worked out from the merged TOML, so prose is read against them.

    venv/bin/python .claude/skills/author-game-lean/scripts/sheet.py games/<slug> <id>
        prints the computed sheet for the canvases on the card's Builds: line, in the card's Sheet: format

One row per screen, every path into it merged:

    <canvas>.<node> | <clock in>–<clock out> | <place> | <who is there> | <what she wears> | <flags set>

How each column is worked out (LO, relayed 2026-11-24: "Commit and continue", the plan's Part C):
  clock    the starting canvas starts at [time] starting_day / starting_hour, minute 0 (v2.py:1592-1593); a
           repeatable starts in its trigger's time_of_day window ("07:00–09:00"), or "any" with none. Each choice adds
           its time_progression_minutes, 3 when it has none (v2.py:17744, 17758). In and out are the screen's first
           minute and the minute its choice leaves it; a repeatable's are written "+<n>" from the scene's start.
           A repeatable bound to a person with no window reads "while <id> is there": who else is there is
           worked out over the minutes that person's rows put them at the place.
  place    the canvas trigger's location. A screen of a canvas with no location (the opening) has no place the
           engine knows: the place is the card's, marked "(card)", and who is there is worked out at it.
  who      people whose schedule rows (who_is_where.where) put them at the place at every five-minute slot of
           the screen; "<id> (part)" when only at some; the scene's bound person (trigger npc / requires_npc) is
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

DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
DEFAULT_MINUTES = 3  # v2.py:17744
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
        for path in walks(c):
            eq = start_outfit(game) if is_start else None
            flags = {i.get("flag_key") for i in items(trig.get("conditions"))
                     if i.get("type") == "flag" and i.get("operator") == "is_true"} - {None}
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
                    slots = slots_between(start_day, start_min + minute, start_min + out_m)
                elif win and win[0] is not None:
                    s, e = win
                    e = s + 60 if e is None else (e if e > s else e + 1440)
                    row["clock"].append(f"{hhmm(s)}–{hhmm(e)} +{minute}")
                    last = e - who_is_where.STEP  # the last minute the scene can start
                    slots = [sl for d in range(7) for sl in slots_between(d, s + minute, last + max(out_m, minute + 5))]
                elif bound and place:
                    # A scene bound to a person shows only while they're there (requires_npc).
                    pid = sorted(bound)[0]
                    row["clock"].append(f"while {pid} is there +{minute}")
                    table = where.get(pid, {})
                    slots = [s for s in who_is_where.SLOTS if place in {p for p, _ in table.get(s, ())}]
                else:
                    row["clock"].append(f"any +{minute}")
                    slots = list(who_is_where.SLOTS)
                row["who"].append(", ".join(present(where, place, slots, bound)) if place else "?")
                if eq is not None:
                    worn = sorted(v for v in eq.values() if v)
                    row["wearing"].append(", ".join(worn) or "none")
                else:
                    checked = sorted({i.get("item_id") for i in items(trig.get("conditions"))
                                      if i.get("type") == "clothing_item" and i.get("operator") == "equipped"} - {None})
                    row["wearing"].append(", ".join(checked) or "any")
                row["flags"].append(set(flags))
                if eq is not None:
                    apply_wardrobe(eq, ch, game)
                set_flags(flags, ch)
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


def compare(mine, computed):
    """(red rows, incomplete rows)."""
    red, inc = [], []
    for s in sorted(set(computed) - set(mine)):
        red.append(f"{s} is built but not on the card's Sheet:")
    for s in sorted(set(mine) - set(computed)):
        red.append(f"{s} is on the card's Sheet: but not built")
    for s in sorted(set(mine) & set(computed)):
        got, want = computed[s], mine[s]
        for col in COLUMNS[1:]:
            if got[col] == "?":
                inc.append(f"{s} · {col}: the sheet can't work it out")
            elif col == "place" and got[col].endswith("(card)"):
                continue  # the card's own place: who is there is checked at it
            elif got[col] != want[col]:
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
