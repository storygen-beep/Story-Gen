"""Written lines must not vanish into "No content" (first_term's café shift, LO 2026-11-05)."""
from apps.game_generation.management.commands.package_from_toml import passages_with_stand_in
from apps.projects.services.template_import import _normalize_block_list


def _group(*blocks):
    return {"type": "group", "conditions": {"version": "1.0", "logic": "AND", "items": []}, "blocks": list(blocks)}


def _pool(*blocks):
    return {"type": "block_pool", "blocks": list(blocks)}


def _texts(blocks):
    found = []
    for block in blocks:
        props = block.get("props") or {}
        if block.get("type") == "paragraph":
            content = block.get("content")
            found.append(content if isinstance(content, str) else str(content))
        found += _texts(props.get("blocks") or [])
        found += _texts(block.get("children") or [])
    return found


LINE = {"type": "paragraph", "content": "The man in the suit over-tips."}


def test_a_line_pool_inside_a_stand_alone_group_keeps_its_lines():
    # the shift's shape: G (a one-item pool holding a group) round a pool of groups
    shape = _pool(_group(_pool(_group(LINE), _group(LINE))))
    assert any("over-tips" in t for t in _texts(_normalize_block_list([shape])))


def test_runaway_nesting_is_still_cut():
    shape = LINE
    for _ in range(12):
        shape = _group(shape)
    assert not any("over-tips" in t for t in _texts(_normalize_block_list([shape])))


def _page(name, body):
    return f'<tw-passagedata pid="1" name="{name}" tags="">{body}</tw-passagedata>'


def test_the_build_check_names_a_screen_with_the_stand_in():
    built = _page("Canvas_a", "&lt;p&gt;&lt;em&gt;No content&lt;/em&gt;&lt;/p&gt;") + _page("Canvas_b", "&lt;p&gt;Fine.&lt;/p&gt;")
    assert passages_with_stand_in(built) == ["Canvas_a"]


def test_a_clean_build_passes_even_if_a_line_says_the_words():
    assert passages_with_stand_in(_page("Canvas_a", "&lt;p&gt;No content here, he says.&lt;/p&gt;")) == []
