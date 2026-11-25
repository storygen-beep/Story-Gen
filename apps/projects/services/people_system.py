"""Course of Temptation's people system for the v2 engine (2026-11-25): the importer half.

One switch, `[engine.people] system = "cot"`. A game without it is untouched: nothing here
adds a key to its metadata, so it builds byte for byte as before. With it:

  * every person has three feelings toward her, friendship / lust / control, held in
    `core_traits` on CoT's -1000..1000 scale and starting at 0 (CoT alter_attitude);
  * `attracted` (yes/no) decides whether lust can rise at all (CoT attracted_to_pc);
  * `traits` are fixed labels from the trait table below (CoT's personality_traits, shown on
    the People view once she knows the person well enough, CoT filter_known_traits);
  * what the person wants from her is worked out at run time (CoT desired_relationship) and
    read by the `npc_wants` condition; `npc_has_trait` reads the traits;
  * a `[[traits.labels]]` row marked `skill = true` is one of her skills, stored 0..1000 and
    shown as a level 0..10 (CoT skill_level); a choice's `skill_gate` opens at a level and
    raises the skill when taken (CoT skillgate, raise_skill).

Everything is checked on the raw TOML (validate_raw) and resolved into one metadata key,
`people_system` (build_config), which the generator dumps into the game. The run-time half
is generators/people_system.py. CoT's source:
/Users/a0000/Documents/Process_Review_20260925/round1_evidence/scripts/_cot_js.txt.
"""
from __future__ import annotations

from typing import Any

FEELINGS = ("friendship", "lust", "control")
FEELING_MIN, FEELING_MAX = -1000, 1000
SKILL_MAX = 1000
# CoT desired_relationship's results. "date" is reachable without romance (a friendly,
# lusting person who is neither casual nor forward wants to date her).
WANTS = ("date", "friend", "fuckbuddy", "hatefuck", "rival", "indifferent")
GENDERS = ("male", "female")
TRAIT_KINDS = ("personality", "sex")
# CoT's inclination_sets that desired_relationship or the People view reads, plus `shy`.
TRAIT_SETS = (
    "slut",
    "casualsex",
    "active",
    "dominant",
    "submissive",
    "forceful",
    "nodating",
    "shy",
)
ENGINE_KEYS = frozenset({"system", "fade", "traits", "show_traits"})
TRAIT_ROW_KEYS = frozenset(
    {"kind", "threshold", "emoji", "description", "hidden", "sets"}
)
NPC_KEYS = ("attracted", "gender", "traits", "want", "professor", "age")
PEOPLE_CONDITION_TYPES = ("npc_wants", "npc_has_trait", "skill_level")

# CoT's shown traits (setup.people.personality_traits, _cot_js.txt:116953-117371): name,
# kind, reveal threshold, emoji, description, and the sets the name stands in. CoT keeps a
# hidden "inclination" under each shown trait; here the shown name is the trait, so the
# sets are CoT's inclination_sets (_cot_js.txt:20908) rewritten in shown names:
# "Strictly Casual" is CoT's Casual Hookup, "Forceful" stands for the forceful set.
_COT_TRAITS: tuple[tuple[str, str, int, str, str, tuple[str, ...]], ...] = (
    ("Sporty", "personality", 200, "🏃", "Likes sports and working out.", ()),
    ("Nerd", "personality", 200, "🤓", "Likes science, geek culture, and the like.", ()),
    ("Artistic", "personality", 200, "🎨", "They're into art.", ()),
    ("Photographer", "personality", 200, "📷", "They enjoy photography.", ()),
    ("Wordsmith", "personality", 200, "✍️", "They're into writing.", ()),
    ("Gamer", "personality", 200, "🎮", "They really like video games.", ()),
    ("Dancer", "personality", 200, "💃", "They're really into dancing.", ()),
    ("Green Thumb", "personality", 200, "🌱", "They're happiest in a garden.", ()),
    ("Cook", "personality", 200, "🍳", "They know their way around a kitchen.", ()),
    (
        "Natural Odor",
        "personality",
        10,
        "💨",
        "Let's just say they don't exactly always smell of strawberries and cream.",
        (),
    ),
    ("Loner", "personality", 200, "🐺", "Happy being on their own.", ()),
    (
        "Particular",
        "personality",
        100,
        "📋",
        "Not satisfied unless things are getting done their way.",
        (),
    ),
    (
        "Pescetarian",
        "personality",
        100,
        "🐟",
        "They don't eat meat. Except for fish: nature's vegetables.",
        (),
    ),
    ("Vegetarian", "personality", 100, "🥦", "They don't eat meat.", ()),
    ("Vegan", "personality", 100, "🌿", "They don't eat any animal products.", ()),
    (
        "Aromantic",
        "personality",
        100,
        "💚",
        "They don't really have any desire for romance or committed relationships.",
        ("nodating",),
    ),
    (
        "Asexual",
        "personality",
        100,
        "💜",
        "Sex isn't really something they need or think about much, though they can still enjoy it.",
        (),
    ),
    (
        "Polyamorous",
        "personality",
        100,
        "💞",
        "They feel that they can devote themselves fully to more than one romantic partner.",
        (),
    ),
    (
        "Open Relationships",
        "personality",
        100,
        "🔓",
        "They prefer not to tie sexual needs to a single person.",
        (),
    ),
    (
        "Strictly Casual",
        "personality",
        100,
        "😏",
        "They are very casual about sex and not interested in dating.",
        ("slut", "casualsex", "nodating"),
    ),
    (
        "Dominant",
        "sex",
        200,
        "😈",
        "They prefer to be dominant in bed.",
        ("casualsex", "active", "dominant"),
    ),
    (
        "Submissive",
        "sex",
        200,
        "🥺",
        "They prefer to be submissive in bed.",
        ("submissive",),
    ),
    (
        "Switch",
        "sex",
        200,
        "🔁",
        "They can enjoy being on the top or the bottom, depending on their mood.",
        ("dominant", "submissive"),
    ),
    ("Prefers Top", "sex", 200, "⬆️", "They prefer to take the top role in bed.", ()),
    (
        "Prefers Bottom",
        "sex",
        200,
        "⬇️",
        "They prefer to take the bottom role in bed.",
        (),
    ),
    (
        "Masochist",
        "sex",
        200,
        "🎭",
        "Pain and pleasure are often two sides of the same coin.",
        ("submissive",),
    ),
    (
        "Sadist",
        "sex",
        200,
        "🗡️",
        "Inflicting pain is very arousing to them.",
        ("dominant", "forceful"),
    ),
    ("Anal Fetish", "sex", 200, "🍑", "They really like butt stuff.", ()),
    ("Oral Fixation", "sex", 200, "👅", "They like oral sex above all.", ()),
    (
        "Likes Standing Position",
        "sex",
        400,
        "🧍",
        "They like having sex in a standing position, such as up against a wall.",
        (),
    ),
    (
        "Likes Missionary",
        "sex",
        400,
        "🤝",
        "They like having sex in the missionary position.",
        (),
    ),
    ("Likes Doggy Style", "sex", 400, "🐕", "They like having doggy style sex.", ()),
    (
        "Likes Spooning",
        "sex",
        400,
        "🥄",
        "They like having sex in a spooning position.",
        (),
    ),
    (
        "Likes Cowgirl",
        "sex",
        400,
        "🤠",
        "They like having sex in positions where one partner is riding on top.",
        (),
    ),
    (
        "Attentive Lover",
        "sex",
        100,
        "💗",
        "Their lover's satisfaction is their satisfaction.",
        (),
    ),
    ("Risktaker", "sex", 600, "🎲", "They like risky, bareback sex.", ()),
    (
        "Sensitive Nipples",
        "sex",
        600,
        "⚡",
        "They can achieve orgasm just from nipple play.",
        (),
    ),
    (
        "Shy",
        "personality",
        100,
        "🙈",
        "They tend to be passive or unsure during interactions.",
        ("shy",),
    ),
    (
        "Forward",
        "personality",
        100,
        "👉",
        "They like taking the lead.",
        ("casualsex", "active"),
    ),
    (
        "Passive",
        "personality",
        100,
        "🪶",
        "Often uncertain or passive during sex, waiting for their partner to take the lead.",
        (),
    ),
    (
        "Stoner",
        "personality",
        100,
        "🍃",
        "They're into drugs and it's part of their lifestyle.",
        (),
    ),
    (
        "Bragger",
        "personality",
        200,
        "📢",
        "If they learn about your secret, it is no longer a secret.",
        (),
    ),
    (
        "Chaste",
        "personality",
        100,
        "🙏",
        "Maybe a religious upbringing, maybe something else... they tend to be very reluctant to have sex.",
        (),
    ),
    (
        "Bully",
        "personality",
        100,
        "🤬",
        "Being mean to people brings them pleasure.",
        (),
    ),
    (
        "Insecure",
        "personality",
        200,
        "😟",
        "They are not very sure of themselves and need frequent reassurance.",
        ("shy",),
    ),
    (
        "Assertive",
        "sex",
        200,
        "🗯️",
        "They get what they want. Or at least believe they should.",
        (),
    ),
    ("Compliant", "sex", 200, "🤲", "They say yes to almost anything.", ()),
    (
        "Slut",
        "sex",
        50,
        "🥵",
        "They love to fuck and probably aren't ashamed of it.",
        ("slut", "casualsex"),
    ),
    ("Voyeur", "sex", 100, "👀", "They like watching other people.", ()),
    ("Exhibitionist", "sex", 100, "🧖", "They love showing off their body.", ()),
    (
        "Groper",
        "sex",
        200,
        "🖐️",
        "Their hands tend to wander to places they shouldn't.",
        (),
    ),
)
# CoT inclinations with no shown trait that desired_relationship reads. Never drawn as a
# bubble. Loyal and Cheater only matter once people can be in relationships with each other.
_COT_HIDDEN: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Confident", ("active",)),
    ("Loyal", ()),
    ("Cheater", ()),
)


def default_traits() -> dict[str, dict[str, Any]]:
    """The trait table a game gets without defining anything."""
    table: dict[str, dict[str, Any]] = {}
    for name, kind, threshold, emoji, description, sets in _COT_TRAITS:
        table[name] = {
            "kind": kind,
            "threshold": threshold,
            "emoji": emoji,
            "description": description,
            "sets": list(sets),
        }
    for name, sets in _COT_HIDDEN:
        table[name] = {
            "kind": "personality",
            "threshold": 0,
            "emoji": "",
            "description": "",
            "hidden": True,
            "sets": list(sets),
        }
    return table


def _engine_people(data: dict[str, Any]) -> Any:
    engine = data.get("engine")
    return engine.get("people") if isinstance(engine, dict) else None


def is_on(data: dict[str, Any]) -> bool:
    raw = _engine_people(data)
    return isinstance(raw, dict) and raw.get("system") == "cot"


def _is_number(value: Any) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool)


def trait_table(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """CoT's table with the game's own rows laid over it (a row replaces a default whole)."""
    table = default_traits()
    raw = _engine_people(data) or {}
    own = raw.get("traits") if isinstance(raw, dict) else None
    if isinstance(own, dict):
        for name, row in own.items():
            if not isinstance(row, dict):
                continue
            entry = {
                "kind": row.get("kind", "personality"),
                "threshold": row.get("threshold", 100),
                "emoji": row.get("emoji", ""),
                "description": row.get("description", ""),
                "sets": list(row.get("sets") or []),
            }
            if row.get("hidden") is True:
                entry["hidden"] = True
            table[str(name)] = entry
    return table


def skill_keys(data: dict[str, Any]) -> dict[str, str]:
    """Her skills: key -> label, from `[[traits.labels]]` rows with `skill = true`."""
    labels = (data.get("traits") or {}).get("labels") or []
    out: dict[str, str] = {}
    for row in labels if isinstance(labels, list) else []:
        if isinstance(row, dict) and row.get("skill") is True and row.get("key"):
            out[str(row["key"])] = str(row.get("label") or row["key"])
    return out


def is_professor(npc: dict[str, Any]) -> bool:
    """CoT: faculty who teach. Here: `professor = true`, or filed under the Faculty tab
    unless `professor = false` says otherwise."""
    if isinstance(npc.get("professor"), bool):
        return npc["professor"]
    return npc.get("people_tab") == "faculty"


def npc_defaults(core_traits: dict[str, Any], professor: bool) -> dict[str, Any]:
    """An NPC's core_traits under the switch: each feeling present (0 unless set), and
    `intimacy` for a professor (CoT profintimacy, 0/1/2)."""
    out = dict(core_traits or {})
    for key in FEELINGS:
        out.setdefault(key, 0)
    if professor:
        out.setdefault("intimacy", 0)
    return out


def gate_label(skill_label: str, level: int) -> str:
    return f"(Needs {skill_label} {level})"


def desugar_skill_gate(choice: dict[str, Any], skills: dict[str, str]) -> None:
    """Turn a choice's `skill_gate = { skill, level }` into parts the engine already has:
    a `skill_level` condition (so the choice hides, or greys under show_when_locked with
    "(Needs <Skill> <level>)" beside its text), and a player effect whose value is CoT's
    gain for that gate (resolved when the choice is taken). Rewrites `choice` in place; a
    malformed gate is left alone for validate_raw to name."""
    gate = choice.get("skill_gate")
    if not isinstance(gate, dict):
        return
    skill, level = gate.get("skill"), gate.get("level")
    if skill not in skills or isinstance(level, bool) or not isinstance(level, int):
        return
    if not 1 <= level <= 10:
        return
    item = {"type": "skill_level", "skill": skill, "level": level}
    old = choice.get("conditions")
    if isinstance(old, dict) and old.get("items"):
        if old.get("logic", "AND") == "AND":
            items = list(old["items"]) + [item]
        else:
            group = {"type": "group", "logic": old["logic"], "items": old["items"]}
            items = [group, item]
    else:
        items = [item]
    choice["conditions"] = {"version": "1.0", "logic": "AND", "items": items}
    base = choice.get("locked_text") or choice.get("text") or "Continue"
    choice["locked_text"] = f"{base} {gate_label(skills[skill], level)}"
    choice["effects"] = list(choice.get("effects") or []) + [
        {
            "targetType": "player",
            "trait": skill,
            "op": "add",
            "value": {"type": "skill_gain", "skill": skill, "level": level},
            "clamp": False,
        }
    ]


def build_config(data: dict[str, Any]) -> dict[str, Any] | None:
    """What the generator needs, or None when the switch is off."""
    if not is_on(data):
        return None
    raw = _engine_people(data)
    npcs: dict[str, dict[str, Any]] = {}
    for npc in data.get("npcs") or []:
        if not isinstance(npc, dict) or not npc.get("id"):
            continue
        row: dict[str, Any] = {
            "attracted": npc.get("attracted") is True,
            "gender": npc.get("gender") or "",
            "traits": [str(t) for t in (npc.get("traits") or [])],
        }
        if npc.get("want"):
            row["want"] = npc["want"]
        if is_professor(npc):
            row["professor"] = True
        if npc.get("people_tab") == "faculty":
            row["faculty"] = True
        if _is_number(npc.get("age")):
            row["age"] = npc["age"]
        npcs[str(npc["id"])] = row
    config = {
        "system": "cot",
        "fade": raw.get("fade", True) is not False,
        "traits": trait_table(data),
        "npcs": npcs,
        "skills": skill_keys(data),
    }
    # show_traits = false: traits are the author's brief for a person's scenes and the People
    # view prints none of them (LO 2026-11-26). Written only when false, so a game that leaves
    # it alone builds as before.
    if raw.get("show_traits") is False:
        config["show_traits"] = False
    return config


# ── checks ───────────────────────────────────────────────────────────────────


def _walk(node: Any, ctx: str, visit) -> None:
    """Every table in the raw TOML, with a readable path."""
    if isinstance(node, dict):
        visit(node, ctx)
        for key, value in node.items():
            _walk(value, f"{ctx}.{key}" if ctx else str(key), visit)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            label = value.get("id") if isinstance(value, dict) else None
            _walk(
                value,
                f"{ctx}['{label}']"
                if isinstance(label, str) and label
                else f"{ctx}[{i}]",
                visit,
            )


def _validate_table(raw: dict[str, Any], errors: list[str]) -> None:
    for key in sorted(set(raw) - ENGINE_KEYS):
        errors.append(
            f"[engine.people]: unknown key `{key}` (allowed: {', '.join(sorted(ENGINE_KEYS))})"
        )
    if "fade" in raw and not isinstance(raw["fade"], bool):
        errors.append(
            f"[engine.people] fade must be true or false, got {raw['fade']!r}"
        )
    if "show_traits" in raw and not isinstance(raw["show_traits"], bool):
        errors.append(
            f"[engine.people] show_traits must be true or false, got {raw['show_traits']!r}"
        )
    own = raw.get("traits", {})
    if not isinstance(own, dict):
        errors.append(
            "[engine.people.traits] must be a table of traits, one sub-table per trait name"
        )
        return
    for name, row in own.items():
        ctx = f"[engine.people.traits.{name}]"
        if not isinstance(row, dict):
            errors.append(
                f"{ctx} must be a table {{kind, threshold, emoji, description}}"
            )
            continue
        for key in sorted(set(row) - TRAIT_ROW_KEYS):
            errors.append(
                f"{ctx}: unknown key `{key}` (allowed: {', '.join(sorted(TRAIT_ROW_KEYS))})"
            )
        if row.get("kind") not in TRAIT_KINDS:
            errors.append(
                f"{ctx} kind must be \"personality\" or \"sex\", got {row.get('kind')!r}"
            )
        threshold = row.get("threshold", 100)
        if not _is_number(threshold) or not 0 <= threshold <= FEELING_MAX:
            errors.append(
                f"{ctx} threshold must be a number from 0 to {FEELING_MAX}, got {threshold!r}"
            )
        for key in ("emoji", "description"):
            if key in row and not isinstance(row[key], str):
                errors.append(f"{ctx} {key} must be text, got {row[key]!r}")
        if "hidden" in row and not isinstance(row["hidden"], bool):
            errors.append(f"{ctx} hidden must be true or false, got {row['hidden']!r}")
        sets = row.get("sets", [])
        if not isinstance(sets, list):
            errors.append(f"{ctx} sets must be a list, got {sets!r}")
            continue
        for name_ in sets:
            if name_ not in TRAIT_SETS:
                errors.append(
                    f"{ctx} sets: unknown set {name_!r} (known: {', '.join(TRAIT_SETS)})"
                )


def _validate_npcs(
    data: dict[str, Any], table: dict[str, dict[str, Any]], errors: list[str]
) -> None:
    for npc in data.get("npcs") or []:
        if not isinstance(npc, dict):
            continue
        ctx = f"npcs['{npc.get('id')}']"
        hidden = npc.get("hidden_from_ui") is True
        if not isinstance(npc.get("attracted"), bool) and not (
            hidden and "attracted" not in npc
        ):
            errors.append(
                f"{ctx}.attracted must be true or false under [engine.people]: lust rises "
                f"only for a person who is attracted to her, got {npc.get('attracted')!r}"
            )
        if npc.get("gender") not in GENDERS and not (hidden and "gender" not in npc):
            errors.append(
                f'{ctx}.gender must be "male" or "female" under [engine.people] (what '
                f"the person wants is worked out differently for each), got {npc.get('gender')!r}"
            )
        traits = npc.get("traits", [])
        if not isinstance(traits, list):
            errors.append(f"{ctx}.traits must be a list of trait names, got {traits!r}")
            traits = []
        for name in traits:
            if name not in table:
                errors.append(
                    f"{ctx}.traits: unknown trait {name!r} (not in CoT's table nor in "
                    f"[engine.people.traits])"
                )
        if len(set(map(str, traits))) != len(traits):
            errors.append(f"{ctx}.traits names a trait twice")
        if "want" in npc and npc["want"] not in WANTS:
            errors.append(
                f"{ctx}.want: unknown want {npc['want']!r} (one of: {', '.join(WANTS)})"
            )
        if "professor" in npc and not isinstance(npc["professor"], bool):
            errors.append(
                f"{ctx}.professor must be true or false, got {npc['professor']!r}"
            )
        if "age" in npc and (not _is_number(npc["age"]) or npc["age"] < 18):
            errors.append(f"{ctx}.age must be a number, 18 or more, got {npc['age']!r}")
        core = (
            npc.get("core_traits") if isinstance(npc.get("core_traits"), dict) else {}
        )
        for key in FEELINGS:
            value = core.get(key, 0)
            if not _is_number(value) or not FEELING_MIN <= value <= FEELING_MAX:
                errors.append(
                    f"{ctx}.core_traits.{key} must be a number from {FEELING_MIN} to "
                    f"{FEELING_MAX}, got {value!r}"
                )
        if "intimacy" in core:
            if not is_professor(npc):
                errors.append(
                    f"{ctx}.core_traits.intimacy is read only for a professor "
                    f'(professor = true, or people_tab = "faculty")'
                )
            elif core["intimacy"] not in (0, 1, 2) or isinstance(
                core["intimacy"], bool
            ):
                errors.append(
                    f"{ctx}.core_traits.intimacy must be 0, 1 or 2, got {core['intimacy']!r}"
                )


def _validate_skills(
    data: dict[str, Any], skills: dict[str, str], errors: list[str]
) -> None:
    labels = (data.get("traits") or {}).get("labels") or []
    for row in labels if isinstance(labels, list) else []:
        if (
            isinstance(row, dict)
            and "skill" in row
            and not isinstance(row["skill"], bool)
        ):
            errors.append(
                f"traits.labels[{row.get('key')}] skill must be true or false, got {row['skill']!r}"
            )
    core = (data.get("player") or {}).get("core_traits") or {}
    for key in skills:
        if key not in core:
            errors.append(
                f"traits.labels[{key}] skill = true: '{key}' is not in [player] core_traits"
            )
        elif not _is_number(core[key]) or not 0 <= core[key] <= SKILL_MAX:
            errors.append(
                f"[player] core_traits.{key} is a skill: it must be a number from 0 to "
                f"{SKILL_MAX} (level = value / 100), got {core[key]!r}"
            )


def _validate_uses(
    data: dict[str, Any],
    table: dict[str, dict[str, Any]],
    skills: dict[str, str],
    errors: list[str],
) -> None:
    npc_ids = {str(n.get("id")) for n in data.get("npcs") or [] if isinstance(n, dict)}

    def visit(node: dict[str, Any], ctx: str) -> None:
        if "skill_gate" in node:
            gate, gctx = node["skill_gate"], f"{ctx}.skill_gate"
            if not ctx.rsplit("[", 1)[0].endswith(".choices"):
                errors.append(f"{gctx}: a skill gate is read only on a node's choice")
            if not isinstance(gate, dict) or set(gate) != {"skill", "level"}:
                errors.append(
                    f'{gctx} must be {{ skill = "<key>", level = N }}, got {gate!r}'
                )
            else:
                if gate["skill"] not in skills:
                    errors.append(
                        f"{gctx}: unknown skill {gate['skill']!r} (a skill is a "
                        f"[[traits.labels]] row with skill = true; known: "
                        f"{', '.join(sorted(skills)) or 'none'})"
                    )
                level = gate["level"]
                if (
                    isinstance(level, bool)
                    or not isinstance(level, int)
                    or not 1 <= level <= 10
                ):
                    errors.append(
                        f"{gctx}.level must be a whole number from 1 to 10, got {level!r}"
                    )
        ctype = node.get("type")
        if ctype not in PEOPLE_CONDITION_TYPES or "items" in node:
            return
        if "operator" in node and node["operator"] not in ("is_true", "is_false"):
            return  # the conditions schema names the bad operator
        if ctype == "skill_level":
            if node.get("skill") not in skills:
                errors.append(
                    f"{ctx}: unknown skill {node.get('skill')!r} on a `skill_level` condition"
                )
            level = node.get("level")
            if (
                isinstance(level, bool)
                or not isinstance(level, int)
                or not 1 <= level <= 10
            ):
                errors.append(
                    f"{ctx}: a `skill_level` condition needs level = 1..10, got {level!r}"
                )
            return
        if node.get("npc_id") not in npc_ids:
            errors.append(
                f"{ctx}: a `{ctype}` condition needs npc_id, a person in [[npcs]]; got {node.get('npc_id')!r}"
            )
        if ctype == "npc_wants":
            wants = node.get("any_of") if "any_of" in node else [node.get("value")]
            if (
                ("value" in node) == ("any_of" in node)
                or not isinstance(wants, list)
                or not wants
            ):
                errors.append(
                    f'{ctx}: an `npc_wants` condition needs value = "<want>" or any_of = [ ... ], one of them'
                )
                return
            for want in wants:
                if want not in WANTS:
                    errors.append(
                        f"{ctx}: unknown want {want!r} (one of: {', '.join(WANTS)})"
                    )
        else:
            if ("trait" in node) == ("set" in node):
                errors.append(
                    f'{ctx}: an `npc_has_trait` condition needs trait = "<name>" or set = "<set>", one of them'
                )
            elif "trait" in node and node["trait"] not in table:
                errors.append(
                    f"{ctx}: unknown trait {node['trait']!r} on an `npc_has_trait` condition"
                )
            elif "set" in node and node["set"] not in TRAIT_SETS:
                errors.append(
                    f"{ctx}: unknown set {node['set']!r} (known: {', '.join(TRAIT_SETS)})"
                )

    _walk(data, "", visit)


def _validate_off(data: dict[str, Any], errors: list[str]) -> None:
    """The switch is off: every key only it reads is dead, and says so."""
    need = 'is read only under [engine.people] system = "cot"'
    for npc in data.get("npcs") or []:
        if not isinstance(npc, dict):
            continue
        for key in NPC_KEYS:
            if key in npc:
                errors.append(f"npcs['{npc.get('id')}'].{key} {need}")
    labels = (data.get("traits") or {}).get("labels") or []
    for row in labels if isinstance(labels, list) else []:
        if isinstance(row, dict) and "skill" in row:
            errors.append(f"traits.labels[{row.get('key')}] skill {need}")

    def visit(node: dict[str, Any], ctx: str) -> None:
        if "skill_gate" in node:
            errors.append(f"{ctx}.skill_gate {need}")
        if node.get("type") in PEOPLE_CONDITION_TYPES and "items" not in node:
            errors.append(f"{ctx}: a `{node['type']}` condition {need}")

    _walk(data, "", visit)


def validate_raw(data: dict[str, Any]) -> list[str]:
    """Every check of the people system, on the raw TOML. All errors."""
    errors: list[str] = []
    raw = _engine_people(data)
    if raw is None:
        _validate_off(data, errors)
        return errors
    if not isinstance(raw, dict):
        return [f"[engine.people] must be a table, got {type(raw).__name__}"]
    if raw.get("system") != "cot":
        return [f'[engine.people] system must be "cot", got {raw.get("system")!r}']
    _validate_table(raw, errors)
    table = trait_table(data)
    skills = skill_keys(data)
    _validate_npcs(data, table, errors)
    _validate_skills(data, skills, errors)
    _validate_uses(data, table, skills, errors)
    return errors
