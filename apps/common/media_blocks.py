"""Shared reader for the media a single image/video content block declares.

A media block declares its media in one of three shapes, and this module is the
one place that knows the precedence between them:

    pool_dir = "sex/brothel_oral_t5"   # a FOLDER — everything inside is the pool
    pool     = 4                       # ...and how many we were aiming for

    files = ["sex/a.webm", "sex/b.webm"]   # an explicit pool (legacy)
    file  = "sex/a.webm"                   # a single file

**`pool_dir` > `files` > `file`.** The generator cycles a pool on successive
visits (`v2.py::_render_media_pool`), so all three end up in the same renderer;
they differ only in where the list of paths comes from.

`pool_dir` is the shape to prefer. Its contents are discovered from disk, so the
count is never hardcoded in the TOML and the human curates by adding/removing
files (via the review UI) instead of editing a list. `pool` is a **target**, not
a manifest: the folder is the truth, `pool` only says what we were aiming for so
a half-filled pool can be reported as "3 of 4" instead of passing as finished.

This lives here because there are two INDEPENDENT media enumerators outside the
generator — the game-review missing-media API (`api/v1/game_review.py`) and
`manage.py check_media` — and both used to read `props["file"]` only. Every pool
entry was therefore invisible to them: a game could declare forty empty pool
slots and the audit would report "0 missing", which is exactly how ~30 image
pools in `the_long_summer_test` went dark. One shared helper is what stops the
walks drifting apart again the next time the block schema grows.
"""
import re
from typing import Any, Dict, List, Optional

# What a pool aims for when the block names a folder but no target. Four is what
# find-media's frame strip typically leaves from a single search (measured 3-of-5
# and 4-of-6 survival, two independent rounds).
DEFAULT_POOL_TARGET = 4

# The importer's positional fallback id: "b3", "b0.b2", "b1.beat0.b2". These shift
# when a block is inserted above them, so they must never key a shelf — see
# `block_slot_key`. Matched conservatively: an authored id that happens to look like
# this is indistinguishable from the generated one, so it is refused either way.
_POSITIONAL_ID_RE = re.compile(r"^b\d+(?:\.(?:beat\d+|b\d+))*$")


def block_slot_key(block: Dict[str, Any]) -> str:
    """The stable identity of one media slot — what its shelf and verdict file under.

        authored `id`  ->  else `pool_dir`  ->  else `file`

    **Why this exists.** A slot's shelf (stocked options) and its review verdict are
    both filed under a string. Using the declared *path* means every edit that moves
    the path orphans both ledgers: converting to a pool drops the extension
    (`a_t5.webm` -> `a_t5`), and a tier retag rewrites it outright (`_t4` -> `_t5`).
    Measured live: 148 stocked options stranded on the first pool conversion. An
    authored `id` doesn't move, so the ledgers survive.

    **Opt-in by design.** There are ~560 media blocks in this repo; mandating an id
    on all of them is neither realistic nor desirable. A block without one keeps
    using its path, exactly as before — which is also why no migration is needed for
    existing games. Tag a block when you expect its path to move.

    ⚠️ **Explicit `id` only — NEVER a positional fallback id.** The IMPORTER assigns
    every block a positional id when the TOML has none (`template_import.py`,
    ``str(b.get("id") or _bid)`` where `_bid` is `b3` / `b0.b2`). That id shifts when
    you insert a block above it, so keying a shelf on it would re-key on an unrelated
    edit — strictly worse than keying on the path. This function is fed RAW TOML
    blocks, where an un-authored id is simply absent; the guard below exists because
    the normalized dict does carry one and a caller will eventually pass it in.
    """
    if not isinstance(block, dict):
        return ""

    raw_id = block.get("id")
    if isinstance(raw_id, str) and raw_id.strip():
        candidate = raw_id.strip()
        if not _POSITIONAL_ID_RE.match(candidate):
            return candidate

    props = block.get("props")
    if not isinstance(props, dict):
        props = {}

    pool = block_media_pool(props)
    if pool is not None:
        return pool["dir"]

    paths = block_media_paths(props)
    return paths[0] if paths else ""


def block_media_pool(props: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """The folder pool a block declares, or None if it doesn't declare one.

    Returns ``{"dir": "sex/brothel_oral_t5", "target": 4}``.

    Deliberately a SEPARATE function from `block_media_paths` rather than an
    extra return shape on it: three call sites depend on that one's flat
    ``List[str]`` contract, and a folder cannot be expressed in it — the
    contents live on disk, not in the TOML.

    Callers check this FIRST. A block with a `pool_dir` has no statically
    declared paths at all, so `block_media_paths` returns [] for it.
    """
    if not isinstance(props, dict):
        return None

    pool_dir = props.get("pool_dir")
    if not isinstance(pool_dir, str) or not pool_dir.strip():
        return None

    # Normalise to forward slashes and strip any trailing separator, so
    # "sex/foo", "sex/foo/" and "sex\\foo" all key the same pool. That key is
    # load-bearing: the options store, the review ledger and the options-page
    # URL are all keyed by this string, so two spellings would fork the shelf.
    normalized = pool_dir.replace("\\", "/").strip().rstrip("/")
    if not normalized:
        return None

    target = props.get("pool")
    # bool is an int subclass — `pool = true` is a typo, not a count of 1.
    if not isinstance(target, int) or isinstance(target, bool) or target < 1:
        target = DEFAULT_POOL_TARGET

    return {"dir": normalized, "target": target}


def block_media_paths(props: Dict[str, Any]) -> List[str]:
    """Every media path a single block declares STATICALLY, in declared order.

    `files` wins over `file` when both are present, matching the generator.
    Non-string and empty entries are dropped.

    Returns [] when the block declares no path at all — including the `pool_dir`
    case, whose paths are discovered from disk rather than declared. Callers that
    care about folder pools must consult `block_media_pool` first; a caller that
    only uses this one will simply see a pool block as declaring nothing, which
    is true, rather than seeing a wrong path.
    """
    if not isinstance(props, dict):
        return []

    # A folder pool declares no static paths. Checked first so `pool_dir` wins
    # over a stale `files`/`file` left on the same block during a migration.
    if block_media_pool(props) is not None:
        return []

    files = props.get("files")
    if isinstance(files, list):
        paths = [f for f in files if isinstance(f, str) and f.strip()]
        if paths:
            return paths

    single = props.get("file")
    if isinstance(single, str) and single.strip():
        return [single]
    return []


def iter_media_blocks(blocks: List[Any]):
    """Yield every image/video block reachable in `blocks`, descending into the
    nested-block containers the game generator actually renders.

    A flat walk over `node["blocks"]` only sees media that are DIRECT children of a
    node. But the hottest content is always nested one level deeper:
      - sex-loop FINISHERS + ambient sex  -> `group` blocks   (`block["blocks"]`)
      - OPENING / first-time sex          -> `cascade` beats  (`props["beats"][*]["blocks"]`)
      - random-still pools                -> `block_pool`     (`props["blocks"]`)
    The flat walk missed all of it, so those files never reached the missing-media
    list and shipped without art while the audit reported "0 missing". This mirrors
    v2.py `_convert_blocks_to_game_html`'s descent so the list matches the real build.

    **It lives here, not in one enumerator, because the drift already happened
    twice.** `block_media_paths` above was extracted after three hand-copied walks
    all read `props["file"]` and went blind to pools. This descent was then written
    in `api/v1/game_review.py` and never propagated to `manage.py check_media`,
    whose own docstring says it "must match api/v1/game_review.py's treatment or
    the two enumerators drift apart again" — and it did: measured on vesper,
    28 of 177 media blocks (16%) were invisible to the audit, including both
    pools inside Marsh's `finish_soft` group chain. Import it; do not re-write it.
    """
    for block in blocks:
        if not isinstance(block, dict):
            continue
        if (block.get("type") or "").strip() in ("image", "video"):
            yield block
        props = block.get("props") or {}
        # group (and any block carrying a direct child list)
        yield from iter_media_blocks(block.get("blocks") or [])
        # block_pool — children under props.blocks
        yield from iter_media_blocks(props.get("blocks") or [])
        # cascade — children under props.beats[*].blocks
        for beat in (props.get("beats") or []):
            if isinstance(beat, dict):
                yield from iter_media_blocks(beat.get("blocks") or [])
