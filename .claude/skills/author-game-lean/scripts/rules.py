"""A piece's rule list, from the card's `Does:` block and the labelled craft tables (the plan's Part B).

    check.py --rules games/<slug> <id>      the piece's rule list, grouped by judge, each with its home file
    check.py --rules games/<slug> plan      the rows whose `when` is "the plan" (plan.md and each release's list)

The card's `Does:` block names, per screen, what the screen does, from SKILL.md's "Rule labels":

    Does:
      <canvas>.<node> | <trigger>, <trigger>, …

"always" is never written: it applies to every screen. "the plan" and "a rule is changed" are not screens and
can't be written here. A screen's rules are every `always` row plus every row whose `when` names one of its
triggers. Pointer rows ("see craft/x.md") are skipped: the id's home holds its labels.

The guard: after the build, what a script can see on a screen must be named in its `Does:` (see GUARD below).
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
NOT_A_SCREEN = ("always", "the plan", "a rule is changed")


def triggers(skill=SKILL):
    """The `when` words, from SKILL.md's Rule labels table."""
    text = (Path(skill) / "SKILL.md").read_text(encoding="utf-8")
    part = text.split("## Rule labels", 1)[-1].split("\n## ", 1)[0]
    return set(re.findall(r"^\| ([a-z][^|]*?) \| ", part, re.M)) - {"when"}


def table(skill=SKILL):
    """{id: {"home", "asks", "failure", "when": [..], "judge", "checks": [..]}} for every home row."""
    out = {}
    for path in sorted((Path(skill) / "craft").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        part = text.split("## Must read", 1)[-1].split("\n## ", 1)[0] if "## Must read" in text else ""
        for m in re.finditer(r"^\| ([CL]\d+) \|.*$", part, re.M):
            cells = [c.strip() for c in m.group(0).strip().strip("|").split("|")]
            if len(cells) != 5 or cells[1].startswith("see "):
                continue
            kind, _, named = cells[4].partition("+")
            out[cells[0]] = {"home": f"craft/{path.name}", "asks": cells[1], "failure": cells[2],
                             "when": [w.strip() for w in cells[3].split(",") if w.strip()],
                             "judge": kind.strip(), "checks": [x.strip() for x in named.split(",") if x.strip()]}
    return out


def card_does(text):
    """{screen: [triggers]} from the card's `Does:` block, or None when the card has none."""
    m = re.search(r"^Does:[ \t]*\n((?:[ \t]+\S.*\n?)*)", text, re.M)
    if not m:
        return None
    out = {}
    for raw in m.group(1).splitlines():
        screen, _, rest = raw.strip().partition("|")
        screen = screen.strip()
        if screen and not screen.startswith("<"):
            out[screen] = [t.strip() for t in rest.split(",") if t.strip()]
    return out


def does_problems(does, skill=SKILL):
    """Rows that make a card's Does: block red: an unknown trigger, a non-screen trigger, a screen with none."""
    known = triggers(skill)
    rows = []
    for screen, trig in does.items():
        if not trig:
            rows.append(f"Does: {screen} names no trigger")
        for t in trig:
            if t in NOT_A_SCREEN:
                rows.append(f"Does: {screen} names `{t}`, which is not written per screen")
            elif t not in known:
                rows.append(f"Does: {screen} names `{t}`, which is not in SKILL.md's Rule labels")
    return rows


def applies(row, screen_triggers):
    return "always" in row["when"] or bool(set(row["when"]) & set(screen_triggers))


def rule_list(does, skill=SKILL, rows=None):
    """{id: sorted screens it applies on} for a card's Does: block."""
    rows = rows or table(skill)
    out = {}
    for rid, row in rows.items():
        on = sorted(s for s, trig in does.items() if applies(row, trig))
        if on:
            out[rid] = on
    return out


def plan_rows(skill=SKILL):
    return {rid: r for rid, r in table(skill).items() if "the plan" in r["when"]}


def print_list(ids, rows, screens_of=None):
    lines = []
    for kind in ("script", "reader", "note"):
        mine = sorted(i for i in ids if rows[i]["judge"] == kind)
        if not mine:
            continue
        lines.append(f"{kind} ({len(mine)})")
        for i in mine:
            r = rows[i]
            extra = f" · checks: {', '.join(r['checks'])}" if r["checks"] else ""
            where = f" · on {len(screens_of[i])} screen(s)" if screens_of else ""
            lines.append(f"  {i} · {r['asks']} · {r['home']}{extra}{where}")
    return lines


# ── the guard ─────────────────────────────────────────────────────────────────────────────────────────────

# What a script can see on a built screen. Triggers not here are the writer's and the reader's to name:
# a moment alone with her body, something sexual shows, an explicit beat (the card's own [explicit] marks),
# a walk-in, a release after the first, the start choice, a person's arc step, a no is possible, and a price written
# in words. The hand-over is seen only on the opening's last screens; a screen before them may name it too.
TIME = re.compile(r"\(\s*\d+\s*(?:min|mins|minutes|hour|hours|h)\b|\b\d{1,2}(?::\d{2})?\s*(?:am|pm)\b", re.I)
MONEY = re.compile(r"\$\s?\d")
GOAL_MARKS = ("✅", "➜")
NOT_METERS = {"energy", "money"}


def _text(node):
    import scenes
    return " ".join(str(b.get("content") or "") for b, _ in scenes.walk(node.get("blocks")))


def seen(game):
    """{screen: set of triggers a script can see}, for every canvas."""
    import scenes
    who = scenes.people(game)
    start = (game.get("project") or {}).get("starting_canvas")
    garments = [str(i.get("name") or "").lower() for i in game.get("clothing") or [] if isinstance(i, dict)]
    garments = [g for g in garments if len(g) >= 4]
    out = {}
    for c in game.get("canvases") or []:
        cid, trig = c.get("id"), c.get("trigger") or {}
        nodes, nxt, _ = scenes.graph(c)
        # The starting canvas plays once, at the start; any other canvas is repeatable unless it says
        # is_repeatable = false (v2.py:15065).
        rep = cid != start and str(trig.get("is_repeatable", "true")).lower() != "false"
        for node in c.get("nodes") or []:
            nid = node.get("id")
            key, seen_here = f"{cid}.{nid}", set()
            text = _text(node)
            choices = (node.get("exit_block") or {}).get("choices") or []
            labels = " ".join(str(ch.get("text") or "") for ch in choices)
            if scenes.has_company(c, node, who):
                seen_here.add("a person is on screen")
            seen_here.add("a repeatable" if rep else "a one-time step")
            if cid == start:
                seen_here.add("the opening")
                if nid == (c.get("nodes") or [{}])[0].get("id"):
                    seen_here.add("the first screen")
                if not nxt.get(nid):
                    seen_here.add("the hand-over")
            if not nxt.get(nid):
                seen_here.add("a scene's last screen")
            if any(ch.get("wardrobeEffects") for ch in choices):
                seen_here.add("she dresses or undresses")
            low = text.lower()
            if any(re.search(rf"\b{re.escape(g)}\b", low) for g in garments):
                seen_here.add("a garment is named")
            if MONEY.search(text) or MONEY.search(labels):
                seen_here.add("a price or pay is shown")
            if TIME.search(labels) or TIME.search(text):
                seen_here.add("the clock moves")
            if any(b.get("type") in ("image", "video") for b, _ in scenes.walk(node.get("blocks"))):
                seen_here.add("a media spot")
            if any(ef.get("trait") not in NOT_METERS for ch in choices for ef in ch.get("effects") or []
                   if isinstance(ef, dict) and ef.get("trait")):
                seen_here.add("a meter is shown or paid")
            if any(m in text for m in GOAL_MARKS):
                seen_here.add("a goal card is shown")
            if any(ch.get("targetType") == "location" for ch in choices):
                seen_here.add("a place is entered")
            out[key] = seen_here
    return out


def meetings(game):
    """[(screen the met flag is set leaving, screen it leads to or None, flag)]: a first meeting shows on one of them."""
    out = []
    for c in game.get("canvases") or []:
        ids = {n.get("id") for n in c.get("nodes") or []}
        for node in c.get("nodes") or []:
            for ch in (node.get("exit_block") or {}).get("choices") or []:
                for ef in ch.get("flagEffects") or []:
                    flag = str(ef.get("flag", "")) if isinstance(ef, dict) else ""
                    if flag.startswith("met_") or flag.endswith("_met"):
                        to = ch.get("nodeId") if ch.get("nodeId") in ids else None
                        out.append((f"{c['id']}.{node.get('id')}", f"{c['id']}.{to}" if to else None, flag))
    return out


def guard(does, game):
    """Rows where the built screen does something its Does: line doesn't name."""
    s = seen(game)
    rows = []
    for screen, trig in sorted(does.items()):
        got = s.get(screen)
        if got is None:
            rows.append(f"Does: {screen} is not built")
            continue
        rows += [f"{screen} does `{t}` in the build, and its Does: line doesn't name it" for t in sorted(got)
                 if t not in trig]
    # A step she can say no to, on a one-time canvas at a place, fires by itself on entry and doesn't check the
    # person is there (v2.py:5895-5915, 6083-6086): it must gate on presence or hours in its own conditions.
    by_id = {c.get("id"): c for c in game.get("canvases") or []}
    start = (game.get("project") or {}).get("starting_canvas")
    for screen, trig in sorted(does.items()):
        c = by_id.get(screen.split(".")[0]) or {}
        t = c.get("trigger") or {}
        if (c.get("id") == start or not t.get("location") or str(t.get("is_repeatable", "true")).lower() != "false"
                or not {"a person's arc step", "a no is possible"} <= set(trig)):
            continue
        import scenes
        gated = any(i.get("type") == "time_of_day" or (i.get("type") == "npc_at_location"
                                                         and i.get("operator", "is_present") == "is_present")
                    for i in scenes.items(t.get("conditions")))
        if not gated:
            rows.append(f"{screen}: a one-time step she can say no to fires by itself on arrival, without checking "
                        f"the person is there; gate it on npc_at_location or their hours, or make it a repeatable "
                        f"row in their menu (craft/arc.md, How a step reaches her)")
    for src, dst, flag in meetings(game):
        if src in does and not any("a first meeting" in does.get(x, ()) for x in (src, dst) if x):
            rows.append(f"{src} sets {flag}: name `a first meeting` on it or on {dst or 'the screen she meets them'}")
    return rows
