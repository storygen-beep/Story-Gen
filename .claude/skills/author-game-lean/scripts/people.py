"""CoT's people system (`[engine.people] system = "cot"`) as the lean scripts see it: check.py's `people` check.

    [engine.people] system = "cot"    every person: friendship, lust, control (-1000..1000), gender, attracted,
                                      traits from CoT's table; her skills: [[traits.labels]] skill = true
    (author-game-v2/references/engine.md §54; the importer half is apps/projects/services/people_system.py)

The importer already refuses a missing gender or attracted, an unknown trait, a feeling out of range and a gate on an
unknown skill, but only at package time. This check reads the merged TOML, so the card's build is red before the
package step, and it adds what the importer can't know, because it is the skill's rule and not the engine's
(LO, typed in main-lean 2026-11-25: "Yes lets move to cot style type system", "Go ahead with your picks", "Go ahead"):

  1. every person has a type (`people_type`, read only here: the engine ignores the key) or hand-set values (a
     feeling in core_traits, or a `want`), and 1 to 4 traits (craft/people.md rules 8 and 13);
  2. every trait has a job: it is in a set that changes a number (NUMBER_SETS; or it is Chaste or Asexual), some
     `npc_has_trait` condition reads it, or it is a shown personality-kind trait, a manner or hobby the People view
     teaches (its truth is the reader's, C2183); and not every trait of a person is hidden (craft/people.md rule 13);
  3. no person keeps a 0-100 meter from before the switch: a core_traits key, a trait_decay key, or an effect on
     a person's trait that is not friendship, lust, control or a professor's intimacy (craft/people.md rule 8);
  4. every skill gate and skill_level condition names one of her skills, at a level 1 to 10, and no skill also
     has an [engine.daily_caps] band table, which would cut it twice (craft/meters.md rules 1 and 6).
"""
import functools
import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]  # scripts -> author-game-lean -> skills -> .claude -> repo
ENGINE = REPO / "apps" / "projects" / "services" / "people_system.py"
FEELINGS = ("friendship", "lust", "control")
PROFESSOR_ONLY = ("intimacy",)
WANT_READS = ("Chaste", "Asexual")  # read by name in the want (engine.md §54), in no set
# The sets that change a number: the want, the lust tipping point or when the control meter shows (engine.md §54's
# set table). `shy` is read by conditions only, so Shy and Insecure need a scene that reads them.
NUMBER_SETS = ("slut", "casualsex", "active", "dominant", "submissive", "forceful", "nodating")
MAX_TRAITS = 4  # CoT's special people carry 2-3 inclinations; 2-4 is the rule (craft/people.md rule 8)


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


def trait_readers(game):
    """{(npc id, trait name or set name)} that some npc_has_trait condition reads."""
    out = set()

    def visit(node, _):
        if node.get("type") == "npc_has_trait":
            for key in ("trait", "set"):
                if node.get(key):
                    out.add((str(node.get("npc_id")), str(node[key])))
    _walk(game.get("canvases") or [], visit)
    return out


def shown_manner(row):
    """A personality-kind trait the People view shows: a manner or hobby trait (Shy, Bully, Gamer, Cook...). Its job
    is to be learned there, later a chat topic; whether a written scene shows it is the reader's (C2183)."""
    return row.get("kind") == "personality" and not row.get("hidden")


def has_job(npc_id, name, table, readers):
    row = table.get(name) or {}
    if set(row.get("sets") or ()) & set(NUMBER_SETS) or name in WANT_READS or shown_manner(row):
        return True
    return (npc_id, name) in readers or any((npc_id, s) in readers for s in row.get("sets") or [])


def problems(game, mod=None):
    """Rows that make the people check red. Empty for a game without the switch."""
    if not on(game):
        return []
    mod = mod or engine()
    table, skills = mod.trait_table(game), mod.skill_keys(game)
    readers = trait_readers(game)
    rows = []
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
        if not traits:
            rows.append(f"person `{nid}` has no trait: give them 2-4 from CoT's table (craft/people.md rule 8)")
        elif len(traits) > MAX_TRAITS:
            rows.append(f"person `{nid}` has {len(traits)} traits; 2-4, each with a job (craft/people.md rule 8)")
        if traits and all((table.get(t) or {}).get("hidden") for t in traits if t in table):
            rows.append(f"person `{nid}` has only hidden traits, so their personality on the People view stays empty: "
                        f"add a manner or hobby trait a written scene shows (craft/people.md rule 13; C2183)")
        for t in traits:
            if t in table and not has_job(nid, t, table, readers):
                rows.append(f"person `{nid}`'s trait `{t}` has no job: a sex-kind or hidden trait that changes no number, "
                            f"and no npc_has_trait reads it; write the line that reads it, or drop it (craft/people.md rule 13)")
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
    return rows


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
