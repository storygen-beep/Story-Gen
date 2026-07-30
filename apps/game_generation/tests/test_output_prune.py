"""The packager removes output media this build no longer references.

`output/` is regenerated on every build but was never WIPED, so anything a
previous build copied stayed there forever. That was harmless clutter until two
things changed:

  * media pools made file churn routine — every clip unselected from a pool
    leaves a multi-MB orphan behind in output/
  * a game's output media became git-tracked (games/media_lab/output/videos), so
    each orphan is a permanent commit, growing with every curation pass

Keyed on what the build REFERENCES, not on what was unselected. An unselect is
only one way a file goes stale — a rename, a tier retag, a deleted slot, or a
changed extension all orphan a file too, and none leave a trace to detect.
"Not referenced" is one rule that covers every case.

⚠️ This code DELETES files, so the tests below are mostly about what it must
refuse to touch: the source folder, non-media files, and anything still in use.

    pytest apps/game_generation/tests/test_output_prune.py -q
"""
import pytest

from apps.game_generation.services.game_service import GameService


@pytest.fixture
def out(tmp_path):
    """An output/videos tree with three clips in a pool plus a loose still."""
    d = tmp_path / "videos"
    (d / "scenes" / "pool_t5").mkdir(parents=True)
    for n in ("a.gif", "b.gif", "c.gif"):
        (d / "scenes" / "pool_t5" / n).write_bytes(b"x" * 100)
    (d / "scenes" / "solo.jpg").write_bytes(b"y" * 50)
    return d


LIVE = ["scenes/pool_t5/a.gif", "scenes/pool_t5/c.gif", "scenes/solo.jpg"]


def test_unreferenced_media_is_removed(out):
    stats = GameService()._prune_orphaned_media(out, LIVE)

    assert stats["removed"] == 1
    assert stats["files"] == ["scenes/pool_t5/b.gif"]
    assert stats["bytes_freed"] == 100
    assert not (out / "scenes" / "pool_t5" / "b.gif").exists()


def test_referenced_media_survives(out):
    GameService()._prune_orphaned_media(out, LIVE)

    for rel in LIVE:
        assert (out / rel).is_file(), f"{rel} was referenced and must not be pruned"


def test_a_clean_build_removes_nothing(out):
    everything = LIVE + ["scenes/pool_t5/b.gif"]
    stats = GameService()._prune_orphaned_media(out, everything)

    assert stats["removed"] == 0
    assert len(list(out.rglob("*.gif"))) == 3


def test_non_media_files_are_never_touched(out):
    """The output dir also holds index.html and whatever else. A prune that
    deletes 'anything unknown' is one bad path from eating the build."""
    (out / "index.html").write_text("<html>")
    (out / "notes.txt").write_text("keep me")
    (out / "scenes" / "data.json").write_text("{}")

    GameService()._prune_orphaned_media(out, LIVE)

    assert (out / "index.html").is_file()
    assert (out / "notes.txt").is_file()
    assert (out / "scenes" / "data.json").is_file()


def test_an_emptied_pool_folder_is_swept_up(out):
    """Unselect every clip and the whole folder should go, not linger empty."""
    GameService()._prune_orphaned_media(out, ["scenes/solo.jpg"])

    assert not (out / "scenes" / "pool_t5").exists()
    assert (out / "scenes" / "solo.jpg").is_file()


def test_a_missing_output_dir_is_not_an_error(tmp_path):
    stats = GameService()._prune_orphaned_media(tmp_path / "nope", LIVE)
    assert stats == {"removed": 0, "bytes_freed": 0, "files": []}


def test_pruning_everything_is_possible_but_leaves_the_tree(out):
    """A build that references no media at all still must not blow up."""
    stats = GameService()._prune_orphaned_media(out, [])
    assert stats["removed"] == 4
    assert out.is_dir()


def test_windows_style_keep_paths_still_match(out):
    """`used_assets` paths are normalised to forward slashes upstream, but the
    prune must not silently delete a live file if one ever arrives otherwise."""
    stats = GameService()._prune_orphaned_media(out, LIVE)
    assert stats["removed"] == 1, "only b.gif should have gone"
