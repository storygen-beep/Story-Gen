"""CoT's people system (`[engine.people] system = "cot"`) as the lean scripts see it: check.py's `people` check.

    [engine.people] system = "cot"    every person: friendship, lust, control (-1000..1000), gender, attracted,
    show_traits = false               2-4 trait words of the game's own, never shown;
                                      her skills: [[traits.labels]] skill = true
    (author-game-v2/references/engine.md §54; the importer half is apps/projects/services/people_system.py)

The importer already refuses a missing gender or attracted, an unknown trait, a feeling out of range and a gate on an
unknown skill, but only at package time. This check reads the merged TOML, so the card's build is red before the
package step, and it adds what the importer can't know, because it is the skill's rule and not the engine's
(LO, typed in main-lean 2026-11-25: "Yes lets move to cot style type system", "Go ahead with your picks", "Go ahead"):

  1. every person has a type (`people_type`, read only here: the engine ignores the key) or hand-set values (a
     feeling in core_traits, or a `want`) (craft/people.md rules 8 and 13);
  2. traits are the author's brief, never shown (LO, typed in main-lean 2026-11-26: "Hide them dont show them, they
     are for us, to design the npc scenes and all, dont have to show to a player."): `[engine.people] show_traits =
     false`, every person carries 2 to 4 trait words, and every word has a row in the game's own table
     `[engine.people.traits.<Word>]`, never another game's table by default (craft/people.md rule 13; C2193, C2184).
     Whether a scene keeps the words is the reader's (C2194);
  3. no person keeps a 0-100 meter from before the switch: a core_traits key, a trait_decay key, or an effect on
     a person's trait that is not friendship, lust, control or a professor's intimacy (craft/people.md rule 8);
  4. every skill gate and skill_level condition names one of her skills, at a level 1 to 10, and no skill also
     has an [engine.daily_caps] band table, which would cut it twice (craft/meters.md rules 1 and 6).

Rule 5 runs on every lean game, with or without the switch (LO, typed in main-lean 2026-11-26: "Option B."):
  5. everyone she has met has a menu (C2197): a person with schedule rows, met by a `met_<x>` flag some canvas sets
     or by a flag their `[[quest_cards]]` `when` waits on (a friend met through someone else), has a repeatable, manual canvas with `npc` set to them (their face), or carries `no_menu = "<why>"`. Each
     menu's Talk sets a `_today` flag that `[engine.daily_tick]` clears, and all of one person's menus share it,
     so Talk is once a day across places (C2198). The steps and the hooks are the reader's.
"""
import functools
import re
import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]  # scripts -> author-game-lean -> skills -> .claude -> repo
ENGINE = REPO / "apps" / "projects" / "services" / "people_system.py"
FEELINGS = ("friendship", "lust", "control")
PROFESSOR_ONLY = ("intimacy",)
MIN_TRAITS, MAX_TRAITS = 2, 4  # a few words used often beat many used rarely (craft/people.md rule 13)


@functools.lru_cache(maxsize=1)
def engine():
    """The importer's own module, loaded from its file so the trait table can never drift from the build's."""
    spec = importlib.util.spec_from_file_location("lean_people_system", ENGINE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def on(game):
    people = (game.get("engine") or {}).get("people") if isinstance(game.get("engine"), dict) else None
    return isinstance(people, dict) and people.get("system") == "cot"


def _walk(obj, visit, ctx=""):
    if isinstance(obj, dict):
        visit(obj, ctx)
        for k, v in obj.items():
            _walk(v, visit, f"{ctx}.{k}" if ctx else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            _walk(v, visit, f"{ctx}[{i}]")


def own_words(game):
    """The game's own trait words: the keys of `[engine.people.traits]`."""
    raw = ((game.get("engine") or {}).get("people") or {}) if isinstance(game.get("engine"), dict) else {}
    own = raw.get("traits") if isinstance(raw, dict) else None
    return set(own) if isinstance(own, dict) else set()


def shows_traits(game):
    """False only when `[engine.people] show_traits = false` (engine.md §54; written to the config only then)."""
    raw = ((game.get("engine") or {}).get("people") or {}) if isinstance(game.get("engine"), dict) else {}
    return raw.get("show_traits") is not False


def _short(npc_id):
    return re.sub(r"^npc_", "", str(npc_id))


def met_by(game, npc_id):
    """The flags that mean she has met this person: `met_<x>`, and every flag their `[[quest_cards]]` `when` waits on
    being true (a person met through someone else, like a friend Brooke names: their card opens on `met_brooke`)."""
    out = {f"met_{_short(npc_id)}"}
    for q in game.get("quest_cards") or []:
        if isinstance(q, dict) and str(q.get("npc_id")) == str(npc_id):
            for w in q.get("when") or []:
                if isinstance(w, dict) and w.get("flag") and str(w.get("op", "is_true")) == "is_true":
                    out.add(str(w["flag"]))
    return out


def met_flags_set(game):
    """Flags some canvas sets, in a flagEffects entry anywhere in it."""
    found = set()

    def visit(node, ctx):
        for e in node.get("flagEffects") or []:
            if isinstance(e, dict) and str(e.get("op", "set")).lower() == "set" and e.get("flag"):
                found.add(str(e["flag"]))
    _walk(game.get("canvases") or [], visit)
    return found


def _retired(c):
    return any(str(v).lower() == "false" for v in (c.get("is_active"), (c.get("trigger") or {}).get("is_active"))
               if v is not None)


def menus(game):
    """{npc id: [menu canvas]}: repeatable, manual, not substitution_only, not retired, with `npc` on the trigger."""
    out = {}
    for c in game.get("canvases") or []:
        t = c.get("trigger") if isinstance(c, dict) and isinstance(c.get("trigger"), dict) else {}
        if not t.get("npc") or not t.get("is_repeatable") or (t.get("trigger_mode") or "manual") != "manual":
            continue
        if t.get("substitution_only") or c.get("substitution_only") or _retired(c):
            continue
        out.setdefault(str(t["npc"]), []).append(c)
    return out


def _daily_unset(game):
    tick = ((game.get("engine") or {}).get("daily_tick") or {}) if isinstance(game.get("engine"), dict) else {}
    return {str(e.get("flag")) for e in tick.get("flagEffects") or []
            if isinstance(e, dict) and str(e.get("op", "")).lower() in ("unset", "clear")}


def talk_flags(menu, cleared):
    """For each Talk choice in a menu: the `_today` flags it sets that the daily tick clears (empty when none)."""
    out = []
    for node in menu.get("nodes") or []:
        for ch in ((node.get("exit_block") or {}).get("choices") or []) if isinstance(node, dict) else []:
            if isinstance(ch, dict) and str(ch.get("text", "")).strip().lower() == "talk":
                out.append({str(e.get("flag")) for e in ch.get("flagEffects") or [] if isinstance(e, dict)
                            and str(e.get("op", "set")).lower() == "set" and str(e.get("flag", "")).endswith("_today")}
                           & cleared)
    return out


def menu_problems(game):
    """Rule 5: everyone she has met has a menu, and Talk is once a day across their places (C2197, C2198)."""
    rows = []
    met = met_flags_set(game)
    by_npc = menus(game)
    cleared = _daily_unset(game)
    for n in game.get("npcs") or []:
        if not isinstance(n, dict):
            continue
        nid = str(n.get("id"))
        if not (met_by(game, nid) & met) or not (n.get("schedules") or []):
            continue
        if not by_npc.get(nid):
            if not str(n.get("no_menu") or "").strip():
                why = sorted(met_by(game, nid) & met)[0]
                rows.append(f"person `{nid}` is met (`{why}`) but has no menu: their face only says what "
                            f"their row has them doing. Give them a menu with Talk where talking fits, or "
                            f"`no_menu = \"<why>\"` (craft/people.md rule 16; C2197)")
            continue
        flags = []
        for m in by_npc[nid]:
            for got in talk_flags(m, cleared):
                if not got:
                    rows.append(f"{m.get('id')}: Talk sets no `_today` flag that [engine.daily_tick] clears, so it "
                                f"isn't once a day (craft/people.md rule 16; C2198)")
                flags.append(got)
        shared = set.intersection(*flags) if flags else set()
        if len([f for f in flags if f]) > 1 and not shared:
            rows.append(f"person `{nid}`'s menus set different `_today` flags on Talk ({sorted(set().union(*flags))}): "
                        f"one flag for the person makes Talk once a day across places (C2198)")
    return rows


def problems(game, mod=None):
    """Rows that make the people check red. Rule 5 runs on every game; rules 1 to 4 only under the switch."""
    menu_rows = menu_problems(game)
    if not on(game):
        return menu_rows
    mod = mod or engine()
    skills = mod.skill_keys(game)
    words = own_words(game)
    rows = []
    if shows_traits(game):
        rows.append("[engine.people] show_traits is not false: trait words are the author's brief and the People "
                    "view shows none of them; set `show_traits = false` (craft/people.md rule 13; C2193)")
    for n in game.get("npcs") or []:
        if not isinstance(n, dict) or n.get("hidden_from_ui") is True:
            continue
        nid = str(n.get("id"))
        core = n.get("core_traits") if isinstance(n.get("core_traits"), dict) else {}
        for key in ("gender", "attracted"):
            if key not in n:
                rows.append(f"person `{nid}` has no `{key}` (craft/people.md rule 8)")
        hand_set = any(core.get(f) for f in FEELINGS) or n.get("want")
        if not str(n.get("people_type") or "").strip() and not hand_set:
            rows.append(f"person `{nid}` has no `people_type` and no hand-set feeling or want: pick a type from the "
                        f"plan's type table, then tune (craft/people.md rule 13)")
        traits = n.get("traits") if isinstance(n.get("traits"), list) else []
        if not MIN_TRAITS <= len(traits) <= MAX_TRAITS:
            rows.append(f"person `{nid}` has {len(traits)} trait word(s); 2-4, each with the line that shows it on "
                        f"the plan (craft/people.md rule 13; C2193)")
        for t in traits:
            if t not in words:
                rows.append(f"person `{nid}`'s trait `{t}` has no row in [engine.people.traits.{t}]: the words are "
                            f"the game's own, defined there, never another game's table by default "
                            f"(craft/people.md rule 13; C2193, C2184)")
        allowed = FEELINGS + (PROFESSOR_ONLY if mod.is_professor(n) else ())
        for key in sorted(set(core) - set(allowed)):
            rows.append(f"person `{nid}` keeps `{key}` in core_traits, a meter from before the people system: their "
                        f"feelings are friendship, lust and control (craft/people.md rule 8)")
        for key in sorted(set(n.get("trait_decay") or {}) - set(FEELINGS)):
            rows.append(f"person `{nid}` decays `{key}`, a meter from before the people system (craft/people.md rule 8)")
    npc_ids = {str(n.get("id")) for n in game.get("npcs") or [] if isinstance(n, dict)}

    def visit(node, ctx):
        if node.get("targetType") == "npc" and node.get("trait") and str(node.get("npcId")) in npc_ids:
            npc = next(x for x in game["npcs"] if str(x.get("id")) == str(node.get("npcId")))
            ok = FEELINGS + (PROFESSOR_ONLY if mod.is_professor(npc) else ())
            if node["trait"] not in ok:
                rows.append(f"{ctx}: an effect moves `{node['npcId']}`'s `{node['trait']}`, a meter from before the "
                            f"people system (craft/people.md rule 8)")
        gate = node.get("skill_gate")
        if gate is not None:
            rows.extend(f"{ctx}.skill_gate: {r}" for r in _skill_problems(gate, skills))
        if node.get("type") == "skill_level":
            rows.extend(f"{ctx}: {r}" for r in _skill_problems(node, skills))
    _walk(game.get("canvases") or [], visit, "canvases")
    caps = ((game.get("engine") or {}).get("daily_caps") or {}) if isinstance(game.get("engine"), dict) else {}
    for key in sorted(set(caps) & set(skills)):
        rows.append(f"skill `{key}` also has [engine.daily_caps.{key}]: CoT's cap table already cuts a skill, so the "
                    f"band table would cut it twice; drop it (craft/meters.md rule 6)")
    return menu_rows + rows


def _skill_problems(gate, skills):
    if not isinstance(gate, dict) or not gate.get("skill"):
        return ["names no skill (craft/meters.md rule 1)"]
    out = []
    if gate["skill"] not in skills:
        out.append(f"names `{gate['skill']}`, which is not one of her skills ([[traits.labels]] skill = true)")
    level = gate.get("level")
    if not isinstance(level, int) or isinstance(level, bool) or not 1 <= level <= 10:
        out.append(f"level {level!r} is not 1 to 10 (craft/meters.md rule 1)")
    return out
