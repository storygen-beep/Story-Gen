"""Walk-ins that fire on arrival (craft/walk-ins.md): check.py's `walkins` check. Two kinds, both behind a chance:
  (a) she comes across something: Does: names "she comes across something" on its screen; no shared brake, once a
      day by its own `max_triggers_per_day = 1` (LO, typed in main-lean 2026-11-26: "2nd one", then "Go", reversing
      his "2 i would say button is good here");
  (b) someone comes to her: every other random canvas at a place, written for one named person, on the shared brake.

    [canvases.trigger] location = "<place>", trigger_mode = "random", chance = <0..1>, requires_npc = "<npc id>"

A canvas with `trigger_mode = "random"` is never a button: every button path skips it (v2.py:4616, 4736, 6603,
6726, 5946-6009), and on arrival `setup.getStoryCanvasRedirect` (v2.py:6555) runs `setup.checkRandomEncounters`
(v2.py:6823-6943), which rolls each one's chance and sends her into the first hit. A story moment (a non-repeatable
canvas that is not random) wins over it (v2.py:5938-5959, 6560-6566). The engine's own brakes are per place (the
place rests `random_cooldown` arrivals, 3 by default, v2.py:6936-6938) and per canvas name
(`max_triggers_per_day`, v2.py:6870-6879); the game-wide one-a-day brake is authored: one flag that every such
canvas waits on and sets, cleared in `[engine.daily_tick]` (v2.py:7209-7227; author-game-v2 engine.md §7, §28).

Red on (LO, typed in main-lean 2026-11-26: "Yes", "One is fine for now"):
  1. a "comes to her" canvas that names no person where their rows are (C2186). Either form passes:
     - `requires_npc` and a schedule row for them at the scene's place; or
     - (P49, LO, typed in main-lean 2026-11-26: "Go with your picks") the person coming to her from next door: an
       `npc_at_location` `is_present` condition on an adjoining place (one sharing the scene's `parent`, or the
       scene's parent itself, the hub) with a schedule row for them there, and no `requires_npc`, which would
       ask for them at her place (v2.py:6905-6918). The condition is read by v2.py:5419-5435.
  2. one without the brake: no `is_false` condition on a flag that `[engine.daily_tick]` unsets, a choice on its
     first screen that doesn't set that flag, or two such canvases on different flags (C2187);
  3. one whose first screen has fewer than two choices: there is always a written way out (C2188);
  4. a card whose Does: puts "a person's arc step" on one: a story moment never waits behind a chance (C2190);
  5. kind (a) as a button: a canvas whose Does: says "she comes across something", or an old "a walk-in" that is
     no substitution, left `trigger_mode = "manual"` (C2195);
  6. kind (a) on the shared brake (it waits on or sets the flag kind (b) shares), or without
     `max_triggers_per_day = 1` (C2195). Kind (a) keeps rule 3 (a way out) and rule 4; rules 1 and 2 are kind (b)'s.
  7. (LO, typed in main-lean 2026-11-26: "she is working out in this scene. Why??", then "Go ahead.") a kind (b)
     scene that fires on arrival whose first screen says she is in the middle of an act ("your stance", "the chair
     beside you", ACT_WORDS): she has only just walked in, so it rides on the act instead (C2196). A short list;
     the reader's C2196 is the real check.
  8. kind (b) inside an act: a substitution target that waits on the shared brake. It keeps rules 1 to 3: the
     person (`requires_npc`, or `npc_at_location` in the rule's or its own conditions), every first-screen choice
     setting the brake, two choices; and it is `substitution_only` with the act's `trigger.location`, or the
     engine can't find it (v2.py:4151-4165) or offers it as a button (C2196).
"""

import scenes

RANDOM = "random"
FINDS = "she comes across something"  # the Rule label that marks kind (a) on a card's Does: (SKILL.md)
# Words that put her in the middle of an act. On a scene that fires as she walks in, each is a line about something
# she isn't doing yet (C2196; first_term_lean's marco_hips, "Your stance is all wrong", P49).
ACT_WORDS = ("your stance", "your form", "your set", "your squat", "your reps", "your lift", "mid-set",
             "your plate", "your fork", "your books", "your notes", "the chair beside you", "the seat beside you")


def comes_to_her(game):
    """[canvas] for every canvas that fires by itself on arrival, behind a chance."""
    out = []
    for c in game.get("canvases") or []:
        t = c.get("trigger") if isinstance(c.get("trigger"), dict) else {}
        if t.get("trigger_mode") == RANDOM and t.get("location") and not scenes.retired(c):
            out.append(c)
    return out


def daily_unset(game):
    """Flags `[engine.daily_tick]` clears each morning."""
    tick = ((game.get("engine") or {}).get("daily_tick") or {}) if isinstance(game.get("engine"), dict) else {}
    return {str(e.get("flag")) for e in tick.get("flagEffects") or []
            if isinstance(e, dict) and str(e.get("op", "")).lower() in ("unset", "clear")}


def waits_on(conditions):
    """Flags a condition block requires to be false (`type = "flag"`, `operator = "is_false"`), at the top level."""
    items = (conditions or {}).get("items") if isinstance(conditions, dict) else None
    return {str(i.get("flag_key")) for i in items or []
            if isinstance(i, dict) and i.get("type") == "flag" and i.get("operator") == "is_false"}


def first_choices(canvas):
    nodes = canvas.get("nodes") or []
    if not nodes:
        return []
    return ((nodes[0].get("exit_block") or {}).get("choices") or []) if isinstance(nodes[0], dict) else []


def sets(choice):
    return {str(e.get("flag")) for e in choice.get("flagEffects") or []
            if isinstance(e, dict) and str(e.get("op", "set")).lower() == "set"}


def rows_at(game, npc_id, place):
    for n in game.get("npcs") or []:
        if isinstance(n, dict) and str(n.get("id")) == str(npc_id):
            return any(isinstance(r, dict) and r.get("location") == place for r in n.get("schedules") or [])
    return False


def parent_of(game, place):
    for loc in game.get("locations") or []:
        if isinstance(loc, dict) and loc.get("id") == place:
            return loc.get("parent")
    return None


def adjoins(game, a, b):
    """Same area: two places sharing a parent, or one the other's parent (the hub)."""
    pa, pb = parent_of(game, a), parent_of(game, b)
    return a != b and ((pa is not None and pa == pb) or pa == b or pb == a)


def next_door(conditions):
    """[(npc id, place)] for each top-level `npc_at_location` `is_present` condition naming a person."""
    items = (conditions or {}).get("items") if isinstance(conditions, dict) else None
    return [(str(i.get("npc_id")), str(i.get("location_id") or i.get("location")))
            for i in items or [] if isinstance(i, dict) and i.get("type") == "npc_at_location"
            and i.get("npc_id") and str(i.get("operator") or "is_present") == "is_present"]


def first_text(canvas):
    """The first screen's words, every block and group, lower case."""
    nodes = canvas.get("nodes") or []
    out = []

    def walk(blocks):
        for b in blocks or []:
            if isinstance(b, dict):
                if isinstance(b.get("content"), str):
                    out.append(b["content"])
                walk(b.get("blocks"))
    if nodes and isinstance(nodes[0], dict):
        walk(nodes[0].get("blocks"))
    return " ".join(out).lower()


def in_acts(game):
    """[(act canvas, rule, target canvas)] for every substitution rule whose target exists."""
    by_id = {c.get("id"): c for c in game.get("canvases") or [] if isinstance(c, dict)}
    out = []
    for c in by_id.values():
        t = c.get("trigger") if isinstance(c.get("trigger"), dict) else {}
        for r in t.get("substitutions") or []:
            if isinstance(r, dict) and r.get("target_canvas_id") in by_id:
                out.append((c, r, by_id[r["target_canvas_id"]]))
    return out


def labelled(does_by_card, label):
    """Canvas ids with a Does: screen that names the label."""
    return {screen.split(".", 1)[0] for does in (does_by_card or {}).values() for screen, trig in (does or {}).items()
            if label in trig}


def substitution_canvases(game):
    """Someone walking in on her: substitution_only canvases, substitution targets, and the acts that carry the rules."""
    out = set()
    for c in game.get("canvases") or []:
        t = c.get("trigger") if isinstance(c.get("trigger"), dict) else {}
        if t.get("substitution_only") or c.get("substitution_only"):
            out.add(c.get("id"))
        for r in t.get("substitutions") or []:
            if isinstance(r, dict) and r.get("target_canvas_id"):
                out.update({r["target_canvas_id"], c.get("id")})  # the act it rides on is no walk-in button either
    return out


def problems(game, does_by_card=None):
    """Rows that make the walkins check red. does_by_card: {card id: its Does: dict}, for rules 4 to 6."""
    rows = []
    finds = labelled(does_by_card, FINDS)
    walk_ins = labelled(does_by_card, "a walk-in")
    subs = substitution_canvases(game)
    for c in game.get("canvases") or []:
        t = c.get("trigger") if isinstance(c.get("trigger"), dict) else {}
        cid = c.get("id")
        if scenes.retired(c) or t.get("trigger_mode") == RANDOM or cid in subs:
            continue
        if cid in finds or (cid in walk_ins and t.get("location")):
            rows.append(f"{cid}: a walk-in she comes across is a button; it fires by itself on arrival: "
                        f"trigger_mode = \"random\", chance (0.35 by default), max_triggers_per_day = 1 "
                        f"(craft/walk-ins.md, C2195)")
    every = comes_to_her(game)
    found = [c for c in every if c.get("id") in finds]
    scenes_b = [c for c in every if c.get("id") not in finds]
    cleared = daily_unset(game)
    brakes = {}
    for c in scenes_b:
        cid, t = c.get("id"), c["trigger"]
        who, place = t.get("requires_npc"), t.get("location")
        near = next_door(t.get("conditions"))
        if who and not rows_at(game, who, place):
            rows.append(f"{cid}: `{who}` has no schedule row at `{place}`, so it never fires where their rows put "
                        f"them; if they come to her from next door, drop `requires_npc` and gate on their place "
                        f"(npc_at_location, is_present) (C2186, L97)")
        elif not who and not near:
            rows.append(f"{cid}: comes to her with no person: `requires_npc` at `{place}`, or an npc_at_location "
                        f"is_present on the adjoining place they come from (craft/walk-ins.md, C2186)")
        elif not who:
            for npc, there in near:
                if not adjoins(game, place, there):
                    rows.append(f"{cid}: `{npc}` comes from `{there}`, which doesn't adjoin `{place}` (same parent, "
                                f"or the hub) (C2186)")
                elif not rows_at(game, npc, there):
                    rows.append(f"{cid}: `{npc}` has no schedule row at `{there}`, so it never fires (C2186, L97)")
        brake = waits_on(t.get("conditions")) & cleared
        if not brake:
            rows.append(f"{cid}: no one-a-day brake: wait on a flag (`is_false`) that [engine.daily_tick] unsets "
                        f"(craft/walk-ins.md, C2187)")
        else:
            brakes[cid] = brake
        said = [w for w in ACT_WORDS if w in first_text(c)]
        if said:
            rows.append(f"{cid}: fires as she walks in, but its first screen has her mid-act (\"{said[0]}\"); put it "
                        f"on that act as a substitution rule, after its costs (craft/walk-ins.md, C2196)")
        choices = first_choices(c)
        if len(choices) < 2:
            rows.append(f"{cid}: its first screen has {len(choices)} choice(s); she always has a written way out "
                        f"(C2188)")
        for i, ch in enumerate(choices):
            if brake and not (sets(ch) & brake):
                rows.append(f"{cid}: choice {i + 1} (`{ch.get('text')}`) doesn't set the brake "
                            f"`{sorted(brake)[0]}`, so a second scene can come to her today (C2187)")
    shared_flags = {f for b in brakes.values() for f in b}
    for c in found:
        cid, t = c.get("id"), c["trigger"]
        on = (waits_on(t.get("conditions")) | {f for ch in first_choices(c) for f in sets(ch)}) & shared_flags
        if on:
            rows.append(f"{cid}: a walk-in she comes across is on the shared brake `{sorted(on)[0]}`; that flag is "
                        f"only for the scenes that come to her (C2195, C2187)")
        if t.get("max_triggers_per_day") != 1:
            rows.append(f"{cid}: a walk-in she comes across is once a day: max_triggers_per_day = 1 (C2195)")
        choices = first_choices(c)
        if len(choices) < 2:
            rows.append(f"{cid}: its first screen has {len(choices)} choice(s); she always has a written way out "
                        f"(C2188)")
    for act, rule, target in in_acts(game):
        tt = target.get("trigger") if isinstance(target.get("trigger"), dict) else {}
        brake = waits_on(tt.get("conditions")) & shared_flags
        if not brake or scenes.retired(target):
            continue  # someone walking in on her, off the brake: not a scene that comes to her
        tid = target.get("id")
        at = (act.get("trigger") or {}).get("location")
        who = tt.get("requires_npc")
        near = next_door(rule.get("conditions")) + next_door(tt.get("conditions"))
        if who and not rows_at(game, who, at):
            rows.append(f"{tid}: `{who}` has no schedule row at `{at}`, where `{act.get('id')}` is, so it never "
                        f"fires (C2186, L97)")
        elif not who and not near:
            rows.append(f"{tid}: comes to her inside `{act.get('id')}` with no person: `requires_npc`, or an "
                        f"npc_at_location is_present on the rule (C2186)")
        if not (tt.get("substitution_only") or target.get("substitution_only")):
            rows.append(f"{tid}: rides on `{act.get('id')}` but isn't substitution_only, so it is a button too "
                        f"(C2196)")
        if tt.get("location") != at:
            rows.append(f"{tid}: its trigger.location is `{tt.get('location')}`, not `{at}` where "
                        f"`{act.get('id')}` is; the engine finds a target only under a place (v2.py:4151-4165, C2196)")
        choices = first_choices(target)
        if len(choices) < 2:
            rows.append(f"{tid}: its first screen has {len(choices)} choice(s); she always has a written way out "
                        f"(C2188)")
        for i, ch in enumerate(choices):
            if not (sets(ch) & brake):
                rows.append(f"{tid}: choice {i + 1} (`{ch.get('text')}`) doesn't set the brake "
                            f"`{sorted(brake)[0]}`, so a second scene can come to her today (C2187)")
    shared = set.intersection(*brakes.values()) if brakes else set()
    if len(brakes) > 1 and not shared:
        rows.append(f"the scenes that come to her wait on different flags ({sorted({f for b in brakes.values() for f in b})}); "
                    f"one flag for the whole game makes it one a day (C2187)")
    ids = {c.get("id") for c in every}
    for card, does in sorted((does_by_card or {}).items()):
        for screen, trig in sorted((does or {}).items()):
            if screen.split(".", 1)[0] in ids and "a person's arc step" in trig:
                rows.append(f"{card}: {screen} is a person's arc step on a scene that waits behind a chance; a story "
                            f"moment fires for sure when due (C2190)")
    return rows
