"""L1 (PRD v2 phase 4 · I27, 2026-09-30): the adjacent-groups lint.

Adjacent `group` blocks are ONE if/elseif chain (`_render_group_chain`): an unconditioned
group is the <<else>> (only the last survives) and first match wins. The lint lists every
group in a run that can never render.

Fixtures are written here; nothing in games/ is read or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def trait(key, op, value):
    return {"type": "trait", "subject": "player", "trait_key": key, "operator": op, "value": value}


def flag(key, op="is_true"):
    return {"type": "flag", "subject": "player", "flag_key": key, "operator": op}


def group(*items, logic="AND", text="x"):
    g = {"type": "group", "blocks": [{"type": "paragraph", "content": text}]}
    if items:
        g["conditions"] = {"version": "1.0", "logic": logic, "items": list(items)}
    return g


def lint(*blocks):
    game = {"canvases": [{"id": "c", "nodes": [{"id": "n", "blocks": list(blocks)}]}]}
    return gates.lint_adjacent_groups(game)[1]


# ── pass ──────────────────────────────────────────────────────────────────────

def test_a_high_first_ladder_with_an_else_is_clean():
    assert lint(group(trait("favour", "gte", 15)), group(trait("favour", "gte", 5)), group()) == []


def test_three_bands_on_a_stage_counter_are_clean():
    assert lint(group(trait("stage", "gte", 3)), group(trait("stage", "eq", 2)),
                group(trait("stage", "lt", 2))) == []


def test_a_separator_starts_a_new_chain():
    # The invisible separator: an empty paragraph between two ladders.
    assert lint(group(trait("a", "lt", 50)), group(trait("a", "gte", 50)),
                {"type": "paragraph", "content": ""},
                group(flag("b")), group()) == []


def test_pool_variants_and_or_groups_are_not_judged():
    pool = {"type": "block_pool", "blocks": [group(), group()]}
    assert lint(pool) == []
    assert lint(group(flag("a"), flag("b"), logic="OR"), group(flag("a"))) == []


def test_a_narrower_group_after_a_different_axis_is_not_dead():
    assert lint(group(trait("service", "gte", 30)), group(trait("cover", "gte", 15)), group()) == []


# ── fail ──────────────────────────────────────────────────────────────────────

def test_two_unconditioned_groups_drop_the_first():
    hits = lint(group(flag("a")), group(text="one"), group(text="two"))
    assert len(hits) == 1 and "group 2 of a run of 3" in hits[0] and "dropped" in hits[0]


def test_a_low_first_ladder_is_dead_above_its_first_rung():
    hits = lint(group(trait("favour", "gte", 5)), group(trait("favour", "gte", 15)))
    assert len(hits) == 1 and "group 2" in hits[0] and "#1" in hits[0]


def test_a_second_ladder_after_an_exhaustive_one_is_dead():
    # The I27 shape: a body ladder that always matches, then a status ladder beside it.
    hits = lint(group(trait("body", "lt", 50)), group(trait("body", "gte", 50)),
                group(flag("status_a")), group(flag("status_b")))
    assert [h.split(" of a run")[0] for h in hits] == ["c.n: group 3", "c.n: group 4"]


def test_the_else_is_dead_when_a_flag_is_split_both_ways():
    hits = lint(group(flag("met")), group(flag("met", "is_false")), group(text="never"))
    assert len(hits) == 1 and "group 3" in hits[0] and "<<else>>" in hits[0]


def test_a_repeated_group_and_a_nested_run_are_found():
    inner = group(trait("x", "gte", 1))
    inner["blocks"] = [group(), group()]
    hits = lint(inner, group(trait("x", "gte", 1), flag("y")))
    assert any("group 2 of a run of 2 never renders — it is true only when #1" in h for h in hits)
    assert any("dropped" in h for h in hits)


# ── follow-ups ───────────────────────────────────────────────────────────────

def test_a_group_without_version_fails_open_and_kills_the_rest():
    bad = group(flag("a"))
    bad["conditions"].pop("version")
    hits = lint(bad, group(flag("b")), group())
    assert [h.split(" of a run")[0] for h in hits] == ["c.n: group 2", "c.n: group 3"]
    assert all("fails open" in h for h in hits)


def test_the_else_after_an_npc_ladder_names_the_old_save_case():
    def his(op, v):
        return {"type": "trait", "subject": "npc", "npc_id": "npc_vic", "trait_key": "trust",
                "operator": op, "value": v}
    hits = lint(group(his("gte", 50)), group(his("lt", 50)), group())
    assert len(hits) == 1 and "dead unless the trait is undefined (old save)" in hits[0]
