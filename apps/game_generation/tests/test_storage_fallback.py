"""A downloaded build must not die because the browser blocks site data.

2026-08-28, a player report on Vesper v0.2.0 (F95zone thread 312420, post #18): the
game was opened from disk in Chrome and showed a stack trace instead of a title screen.

    Apologies! A fatal error has occurred. Aborting.
    Error: no valid storage adapters found.

Reproduced exactly in real Chrome with "block all cookies / site data" on. SugarCube
takes the first storage adapter that works — Web Storage, then cookies — and aborts if
neither does. On a file:// page Chrome silently drops cookies in EVERY profile, so the
second adapter is not really there: one way to save, no net under it.

So the compiler now injects a probe into <head> that installs an in-memory Storage when
the browser denies the real one, plus a notice telling the player their saves are
temporary and what to do about it.

These tests pin the four properties that make the injection safe to run on every build:

  1. it lands in <head>, BEFORE the story format's scripts
  2. it carries both halves — the shim AND the notice with its guide
  3. it cannot be applied twice
  4. it never breaks a build: no <head> means unchanged output, not an exception

Run with an explicit path — pyproject sets testpaths = ["tests"], so app suites are not
collected by a bare `pytest`:

    pytest apps/game_generation/tests/test_storage_fallback.py -q
"""
from unittest.mock import Mock, patch

from apps.game_generation.services.game_service import (
    STORAGE_FALLBACK_MARKER,
    GameService,
    _inject_storage_fallback,
)

TWEE = ":: StoryTitle\nProbe\n\n:: Start\nhello\n"
BANNER = "tweego, version 2.1.1+81d1d71 (2020-02-25T07:09:26Z) [darwin/amd64]"

# The shape Tweego actually emits: <head>, then the format's scripts, then the story.
BUILD = (
    '<!DOCTYPE html>\n<html data-init="no-js">\n<head>\n'
    '<meta charset="UTF-8" />\n<title>Probe</title>\n'
    '<script id="script-libraries" type="text/javascript">/* SugarCube */</script>\n'
    "</head>\n<body>\n"
    '<tw-storydata name="Probe" format="SugarCube">'
    '<tw-passagedata pid="1" name="Start">hello</tw-passagedata>'
    "</tw-storydata>\n</body>\n</html>"
)


# --- 1. placement --------------------------------------------------------------


def test_injected_into_head():
    out = _inject_storage_fallback(BUILD)
    assert STORAGE_FALLBACK_MARKER in out
    assert out.index(STORAGE_FALLBACK_MARKER) > out.index("<head>")
    assert out.index(STORAGE_FALLBACK_MARKER) < out.index("</head>")


def test_runs_before_the_story_format():
    """The whole point. SugarCube picks its adapter at load; arriving after is useless."""
    out = _inject_storage_fallback(BUILD)
    assert out.index(STORAGE_FALLBACK_MARKER) < out.index("script-libraries")


def test_story_data_survives_intact():
    out = _inject_storage_fallback(BUILD)
    assert "tw-storydata" in out and "tw-passagedata" in out
    assert out.endswith("</html>")


# --- 2. both halves are present ------------------------------------------------


def test_carries_the_shim():
    out = _inject_storage_fallback(BUILD)
    assert "localStorage" in out and "sessionStorage" in out
    assert "Object.defineProperty" in out
    assert "SecurityError" in out  # the comment naming what is being caught


def test_carries_the_notice_and_its_guide():
    """A silent shim is the worse bug: progress vanishes with no explanation."""
    out = _inject_storage_fallback(BUILD)
    assert "storage-fallback-notice" in out
    assert "Saving is switched off in this browser." in out
    assert "progress is lost when you close this tab" in out
    # three routes out, all of them things the player can actually do
    assert "Cookies and site data" in out  # 1 · fix the setting
    assert "Save to Disk" in out  # 2 · keep this session
    assert "a different browser" in out  # 3 · sidestep it
    assert "Dismiss" in out


def test_notice_only_shows_when_the_shim_was_needed():
    """`patched` gates the banner, so an ordinary load stays clean."""
    out = _inject_storage_fallback(BUILD)
    body = out[out.index(STORAGE_FALLBACK_MARKER) :]
    assert "if (!patched) { return; }" in body
    assert body.index("if (!patched) { return; }") < body.index("showNotice")


# --- 3. idempotent -------------------------------------------------------------


def test_second_pass_is_a_no_op():
    once = _inject_storage_fallback(BUILD)
    assert _inject_storage_fallback(once) == once


# --- 4. never breaks a build ---------------------------------------------------


def test_no_head_returns_input_unchanged():
    fragment = "<tw-storydata name='x'></tw-storydata>"
    assert _inject_storage_fallback(fragment) == fragment


def test_no_head_does_not_warn():
    """It is a log line, not a defect — and warning here would drown the real warnings."""
    with patch("apps.game_generation.services.game_service.logger") as log:
        _inject_storage_fallback("<tw-storydata/>")
    assert not log.warning.called
    assert log.info.called


# --- and it is actually wired into the compile path ----------------------------


def test_compile_output_carries_the_fallback():
    """The end that matters: what compile_twee_to_html hands back is already patched."""
    mod = "apps.game_generation.services.game_service"
    with patch(
        f"{mod}.subprocess.run",
        return_value=Mock(returncode=0, stdout=BANNER, stderr=""),
    ):
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = BUILD
            with patch(f"{mod}.os.path.exists", return_value=True), patch(
                f"{mod}.os.unlink"
            ):
                out = GameService().compile_twee_to_html(TWEE, "Probe")

    assert STORAGE_FALLBACK_MARKER in out
    assert out.index(STORAGE_FALLBACK_MARKER) < out.index("script-libraries")
