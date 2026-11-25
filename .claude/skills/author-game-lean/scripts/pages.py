"""The Quests page as CoT's Hints page and the People page as CoT's People dialog, as the lean scripts see them.

    [ui] quests_layout = "hints"   [[story_hints]] and [[walkthroughs]] (engine.md, the hints layout)
    [ui] people_page = "cot"       every [[npcs]] with stranger_name and people_tab (engine.md, the People dialog)

Two jobs:
  1. The page as screens. Each [[story_hints]] entry is the screen `story_hints.<slug of its title>` and each
     [[walkthroughs]] the screen `walkthroughs.<id>`, so rules.py and reading.py reach the goal-card rules on them.
     Why: rules.py set "a goal card is shown" only on a story screen with a ✅ or ➜ mark, and the Quests page is
     never a story screen; P46's ladders were read only because the game session put them into the reader brief by
     hand (LO, typed in main-lean 2026-11-25: "Go ahead").
  2. The pointers (check.py's `pages` check). Every first meeting a scene sets, every flag a hidden place waits
     on, is a `when` in some hint step or walkthrough step, unless the opening sets it; every flag a hint step reads
     is set by some canvas; under people_page = "cot", every person has stranger_name and people_tab. Why: before
     P46 only Tom was pointed at, and the Faculty Offices stayed hidden for good once Walsh's class was missed.
"""
import re
import unicodedata

PAGE_KINDS = ("story_hints", "walkthroughs")  # goal cards: a card that builds one names it on its Does:
PEOPLE_FIELDS = ("stranger_name", "people_tab", "tip")  # what the People dialog prints of a person
PEOPLE_KEYS = ("stranger_name", "people_tab")
# What the people system shows of a person on the People view: their traits, and the feelings they start at
# (`[engine.people] system = "cot"`, people.py). A screen each, so a changed trait or start value re-opens its rows
# (P48, 2026-11-25: nothing hashed either, so a later change asked the reader nothing). LO: "Go ahead".
SYSTEM_FIELDS = ("traits", "feelings")


def slug(title):
    plain = unicodedata.normalize("NFKD", str(title or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", plain.lower()).strip("_") or "untitled"


def hints_on(game):
    return str((game.get("ui") or {}).get("quests_layout") or "") == "hints"


def is_page(screen):
    return str(screen).split(".", 1)[0] in PAGE_KINDS + ("npcs", "sidebar")


def people_entries(game):
    """{`npcs.<id>.<field>`: its text} for what the People view shows of each person: under people_page = "cot" the
    dialog fields (stranger_name, people_tab, tip), and under `[engine.people] system = "cot"` their traits and the
    feelings they start at (`npcs.<id>.traits`, `npcs.<id>.feelings`). The reader judges each as a screen, so a
    changed field re-opens its rows (P46, 2026-11-25: 23 names rewritten, the 18 that had passed carried unjudged;
    P48: traits and start values were no screen at all)."""
    import people
    dialog = str((game.get("ui") or {}).get("people_page") or "") == "cot"
    system = people.on(game)
    if not (dialog or system):
        return {}
    tips = {q.get("npc_id"): q.get("tip") for q in game.get("quest_cards") or [] if isinstance(q, dict) and q.get("tip")}
    out = {}
    for n in game.get("npcs") or []:
        if not isinstance(n, dict):
            continue
        values = {}
        if dialog:
            values.update(stranger_name=n.get("stranger_name"), people_tab=n.get("people_tab"), tip=tips.get(n.get("id")))
        if system and n.get("hidden_from_ui") is not True:
            values.update(traits=", ".join(str(t) for t in n.get("traits") or []), feelings=start_feelings(n))
        out.update({f"npcs.{n.get('id')}.{k}": str(v) for k, v in values.items() if v})
    return out


def start_feelings(npc):
    """The values a person starts at, as the importer fills them (people_system.npc_defaults): friendship, lust and
    control (0 unless set), a professor's intimacy, and a hand-set `want`, with their type, gender and attracted."""
    import people
    core = npc.get("core_traits") if isinstance(npc.get("core_traits"), dict) else {}
    mod = people.engine()
    values = mod.npc_defaults({k: v for k, v in core.items() if k in people.FEELINGS + people.PROFESSOR_ONLY},
                              mod.is_professor(npc))
    parts = [f"{k} {values[k]}" for k in people.FEELINGS + people.PROFESSOR_ONLY if k in values]
    parts += [f"{k} {npc[k]}" for k in ("want", "people_type", "gender", "attracted") if k in npc]
    return ", ".join(parts)


def sidebar_entries(game):
    """{`sidebar.<trait>`: the item as the TOML has it} for every sidebar item: its label, bar or bands are what the
    player reads, so a changed band re-opens its rows (P48, 2026-11-25: the four skills by level)."""
    out = {}
    for item in game.get("sidebar_items") or []:
        if isinstance(item, dict):
            out[f"sidebar.{item.get('trait') or slug(item.get('label'))}"] = item
    return out


def entries(game):
    """{screen: (kind, the TOML entry)} for every hint entry and walkthrough."""
    out = {}
    for h in game.get("story_hints") or []:
        if isinstance(h, dict):
            out[f"story_hints.{slug(h.get('title'))}"] = ("story_hints", h)
    for w in game.get("walkthroughs") or []:
        if isinstance(w, dict):
            out[f"walkthroughs.{w.get('id') or slug(w.get('title'))}"] = ("walkthroughs", w)
    return out


def text(entry):
    """Everything the player can read on the entry: title, description, overview, guard, every step's text."""
    parts = [entry.get(k) for k in ("title", "category", "description", "overview")]
    parts.append((entry.get("guard") or {}).get("text"))
    for step in (entry.get("hints") or []) + (entry.get("steps") or []):
        if isinstance(step, dict):
            parts += [step.get(k) for k in ("text", "done_text", "todo_text")]
    return " ".join(str(p) for p in parts if p)


def built(builds):
    """The page screens a card's Builds: line covers: `story_hints` (every entry), `story_hints:<slug>`,
    `walkthroughs` (every walkthrough), `walkthrough:<id>` or `walkthroughs:<id>`."""
    def covers(screen):
        kind, _, name = screen.partition(".")
        singular = kind[:-1]
        return any(b == kind or b in (f"{kind}:{name}", f"{singular}:{name}", screen) for b in builds)
    return covers


def screens_for(game, builds, people=True):
    """{screen: entry} for the page screens a card's Builds: line covers. `sidebar:<trait>` covers that sidebar
    item. `ui:people_page` covers every person's People view fields, `engine:people` every person's traits and start
    feelings, and `npcs:<id>` one person's fields. `people=False` leaves out the people fields and sidebar items: a
    card's Does: need not list them (P09 and P36 built theirs before they were screens), and the reader reaches them
    through reading.PAGE_WHEN."""
    builds = set(builds)
    covers = built(builds)
    out = {s: e for s, (_, e) in entries(game).items() if covers(s)}
    if people:
        out.update({s: e for s, e in sidebar_entries(game).items() if f"sidebar:{s.split('.', 1)[1]}" in builds})
        for s, v in people_entries(game).items():
            _, nid, field = s.split(".", 2)
            whole = "ui:people_page" in builds or ("engine:people" in builds and field in SYSTEM_FIELDS)
            if whole or f"npcs:{nid}" in builds:
                out[s] = v
    return out


# ── the pointers ──────────────────────────────────────────────────────────────────────────────────────────────

def _flags_in(conds):
    return {str(c.get("flag")) for c in conds or [] if isinstance(c, dict) and c.get("flag")}


def ladder_flags(game):
    """Every flag a hint step, a hint's own `when`, a walkthrough step or a walkthrough guard reads."""
    out = set()
    for _, (kind, e) in entries(game).items():
        out |= _flags_in(e.get("when"))
        out |= _flags_in((e.get("guard") or {}).get("when"))
        for step in (e.get("hints") or []) + (e.get("steps") or []):
            if isinstance(step, dict):
                out |= _flags_in(step.get("when"))
    return out


def _set_by(obj, found):
    """Walk a canvas: every flagEffects list, each set (not cleared) flag, with the flags set beside it."""
    if isinstance(obj, dict):
        effects = obj.get("flagEffects")
        if isinstance(effects, list):
            together = {str(ef.get("flag")) for ef in effects if isinstance(ef, dict) and ef.get("flag")
                        and str(ef.get("op", "set")).lower() not in ("clear", "unset", "remove", "false")}
            for f in together:
                found.setdefault(f, set()).update(together)
        for v in obj.values():
            _set_by(v, found)
    elif isinstance(obj, list):
        for v in obj:
            _set_by(v, found)


def flags_set(game, skip=()):
    """{flag: the flags set on the same choice as it}, over every canvas except those in skip."""
    found = {}
    for c in game.get("canvases") or []:
        if c.get("id") not in skip:
            _set_by(c, found)
    return found


def start_id(game):
    return (game.get("project") or {}).get("starting_canvas") or game.get("starting_canvas")


def meeting_flags(game):
    return {f for f in flags_set(game) if f.startswith("met_") or f.endswith("_met")}


def problems(game):
    """Rows that make the pages check red. Empty for a game without either CoT page."""
    rows = []
    if hints_on(game):
        ladders = ladder_flags(game)
        everywhere = flags_set(game)
        opening = set(flags_set(game, skip={c.get("id") for c in game.get("canvases") or []} - {start_id(game)}))
        pointed = lambda f: bool(everywhere.get(f, {f}) & ladders)  # it, or a flag set beside it, is on a ladder
        for f in sorted(meeting_flags(game) - opening):
            if f not in ladders:
                rows.append(f"first meeting `{f}` is set by a scene and no hint step points at it: add a step whose "
                            f"`when` is {f}, after a step that says where and when (craft/people.md rule 11)")
        for loc in game.get("locations") or []:
            hid = loc.get("hidden_until") if isinstance(loc, dict) else None
            f = str(hid.get("flag")) if isinstance(hid, dict) and hid.get("flag") else None
            if f and f not in opening and not pointed(f):
                rows.append(f"place `{loc.get('id')}` is hidden until `{f}`, and no hint step points at the step "
                            f"that sets it (craft/places.md rule 10)")
        for f in sorted(ladders):
            if f not in everywhere:
                rows.append(f"a hint reads flag `{f}`, which no canvas sets: the step can never pass")
    if str((game.get("ui") or {}).get("people_page") or "") == "cot":
        for n in game.get("npcs") or []:
            missing = [k for k in PEOPLE_KEYS if not str(n.get(k) or "").strip()]
            if missing:
                rows.append(f"person `{n.get('id')}` has no {' or '.join(missing)}, and people_page = \"cot\" lists "
                            f"them by it (craft/people.md rule 3)")
    return rows
