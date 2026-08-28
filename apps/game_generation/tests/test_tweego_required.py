"""Tweego is REQUIRED — a build compiles or it fails, it never degrades.

The regression guard for 2026-07-28. Two cloud-session builds ran without Tweego on
PATH; `_try_tweego_compilation` returned None, the packager fell through to a "Basic
Preview Mode" wrapper, and 324,722 bytes of raw Twee source shipped to the portal
announced as "Package ready!". Verification missed it because every media reference
still resolved — those references were inside the source being printed.

So these tests assert the three properties that make that impossible now:

  1. no Tweego  -> RuntimeError, with a message that is actionable in a container
  2. the fallback generator does not exist and cannot come back
  3. exit 0 is NOT enough — output that is not a SugarCube build is refused

(3) is the one that generalises. (1) only covers the failure we already had; (3)
covers any future way the compile could quietly produce something unplayable.

Lives here rather than in apps/game_generation/tests.py because that file is SHADOWED
by this package and is never imported — see that file's note.

Run with an explicit path — pyproject sets testpaths = ["tests"], so app suites are
not collected by a bare `pytest`:

    pytest apps/game_generation/tests/test_tweego_required.py -q
"""
import re
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from apps.game_generation.services.game_service import (
    EXPECTED_SUGARCUBE_VERSION,
    EXPECTED_TWEEGO_VERSION,
    TWEEGO_SEARCH_PATHS,
    GameService,
)

TWEE = ":: StoryTitle\nProbe\n\n:: Start\nhello\n"
BANNER = "tweego, version 2.1.1+81d1d71 (2020-02-25T07:09:26Z) [darwin/amd64]"


@pytest.fixture
def service():
    return GameService()


# --- 1. missing binary is fatal ------------------------------------------------


def test_missing_tweego_raises(service):
    """No Tweego anywhere => RuntimeError, not a degraded build."""
    with patch(
        "apps.game_generation.services.game_service.subprocess.run",
        side_effect=FileNotFoundError(),
    ):
        with pytest.raises(RuntimeError) as exc:
            service.compile_twee_to_html(TWEE, "Probe")

    msg = str(exc.value)
    assert "Tweego not found" in msg
    # The message must be self-explanatory in a fresh container, where it fires first:
    # every path tried, the version wanted, and why there is no fallback.
    for path in TWEEGO_SEARCH_PATHS:
        assert path in msg
    assert EXPECTED_TWEEGO_VERSION in msg
    assert "no preview fallback" in msg.lower()


def test_compile_never_returns_a_source_dump(service):
    """The old failure returned a page containing the raw Twee. Never again."""
    with patch(
        "apps.game_generation.services.game_service.subprocess.run",
        side_effect=FileNotFoundError(),
    ):
        with pytest.raises(RuntimeError):
            service.compile_twee_to_html(TWEE, "Probe")


# --- 2. the fallback is gone ---------------------------------------------------


def test_fallback_generator_does_not_exist(service):
    assert not hasattr(service, "_generate_html_fallback")


def test_old_optional_compile_entrypoint_is_gone(service):
    """`_try_tweego_compilation` returned None on failure — that contract is deleted."""
    assert not hasattr(service, "_try_tweego_compilation")


# --- 3. exit 0 is not sufficient -----------------------------------------------


def _run_compile_with_output(service, html):
    """Drive a 'successful' Tweego run that emitted `html`."""
    mod = "apps.game_generation.services.game_service"
    with patch(
        f"{mod}.subprocess.run",
        return_value=Mock(returncode=0, stdout=BANNER, stderr=""),
    ):
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = html
            with patch(f"{mod}.os.path.exists", return_value=True), patch(
                f"{mod}.os.unlink"
            ):
                return service.compile_twee_to_html(TWEE, "Probe")


def test_output_without_storydata_is_refused(service):
    with pytest.raises(RuntimeError) as exc:
        _run_compile_with_output(service, "<html><body>not a game</body></html>")
    assert "no SugarCube story data" in str(exc.value)


def test_output_with_zero_passages_is_refused(service):
    """The exact shape of the broken builds: story data present, no passages."""
    with pytest.raises(RuntimeError) as exc:
        _run_compile_with_output(
            service, '<html><tw-storydata name="Probe"></tw-storydata></html>'
        )
    assert "ZERO passages" in str(exc.value)


def test_real_sugarcube_output_is_accepted(service):
    html = (
        '<html><tw-storydata name="Probe" format="SugarCube">'
        '<tw-passagedata pid="1" name="Start">hello</tw-passagedata>'
        "</tw-storydata></html>"
    )
    assert _run_compile_with_output(service, html) == html


# --- version pinning is recorded, and a mismatch warns but does not block -------


def test_version_mismatch_warns_but_still_builds(service):
    """An upgrade must stay possible — but never silently.

    Tweego bundles its own story format, so a different compiler changes the SugarCube
    every future game ships against. That has to reach a human.

    Asserts on the logger call rather than caplog: the `apps` logger is configured with
    propagate=False, so records never reach the root handler caplog installs.
    """
    html = (
        '<html><tw-storydata name="Probe">'
        '<tw-passagedata pid="1" name="Start">hi</tw-passagedata></tw-storydata></html>'
    )
    mod = "apps.game_generation.services.game_service"
    with patch(f"{mod}.logger") as mock_logger:
        with patch(
            f"{mod}._installed_sugarcube_version",
            return_value=EXPECTED_SUGARCUBE_VERSION,
        ), patch(
            f"{mod}.subprocess.run",
            return_value=Mock(returncode=0, stdout="tweego, version 9.9.9", stderr=""),
        ):
            with patch("builtins.open", create=True) as mock_open:
                mock_open.return_value.__enter__.return_value.read.return_value = html
                with patch(f"{mod}.os.path.exists", return_value=True), patch(
                    f"{mod}.os.unlink"
                ):
                    assert service.compile_twee_to_html(TWEE, "Probe") == html

    assert mock_logger.warning.called, "a version mismatch must not pass unnoticed"
    emitted = " ".join(str(a) for a in mock_logger.warning.call_args.args)
    assert "version mismatch" in emitted
    assert EXPECTED_TWEEGO_VERSION in emitted
    assert EXPECTED_SUGARCUBE_VERSION in emitted


def test_matching_version_does_not_warn(service):
    """The happy path stays quiet, or the warning becomes noise and gets ignored."""
    html = (
        '<html><tw-storydata name="Probe">'
        '<tw-passagedata pid="1" name="Start">hi</tw-passagedata></tw-storydata></html>'
    )
    mod = "apps.game_generation.services.game_service"
    with patch(f"{mod}.logger") as mock_logger:
        with patch(
            f"{mod}._installed_sugarcube_version",
            return_value=EXPECTED_SUGARCUBE_VERSION,
        ), patch(
            f"{mod}.subprocess.run",
            return_value=Mock(returncode=0, stdout=BANNER, stderr=""),
        ):
            with patch("builtins.open", create=True) as mock_open:
                mock_open.return_value.__enter__.return_value.read.return_value = html
                with patch(f"{mod}.os.path.exists", return_value=True), patch(
                    f"{mod}.os.unlink"
                ):
                    service.compile_twee_to_html(TWEE, "Probe")

    assert not mock_logger.warning.called


# --- the story format is installed separately from the compiler ----------------
#
# `tweego --version` cannot see SugarCube: Tweego loads the format from a
# storyformats/ directory beside the binary. Swap that directory and every future
# build ships a different runtime with the compiler reporting the same version it
# reported yesterday. Until 2026-08-29 EXPECTED_SUGARCUBE_VERSION was compared to
# nothing — it appeared only inside the text of the Tweego warning.


def test_the_installed_sugarcube_is_read_from_disk():
    """Not mocked. This is the version the player actually runs, and if this machine
    cannot answer, the test says so rather than asserting against a guess."""
    from apps.game_generation.services.game_service import _installed_sugarcube_version

    found = _installed_sugarcube_version("tweego")
    if found is None:
        pytest.skip("no storyformats/sugarcube-2/format.js reachable from tweego")
    assert found == EXPECTED_SUGARCUBE_VERSION, (
        f"the installed story format is {found}; every game on the portal was built "
        f"against {EXPECTED_SUGARCUBE_VERSION}"
    )


def test_an_unlocatable_format_is_not_a_pass():
    """None means the question could not be asked. A resolver that returned the
    expected version on failure would make the check permanently green."""
    from apps.game_generation.services.game_service import _installed_sugarcube_version

    assert _installed_sugarcube_version("/nonexistent/path/to/tweego") is None


def test_a_different_sugarcube_warns_and_still_builds(service):
    """Same contract as the Tweego mismatch: loud, never fatal — an upgrade has to
    stay possible, and a fatal check here would block the machine that does it."""
    html = (
        '<html><tw-storydata name="Probe">'
        '<tw-passagedata pid="1" name="Start">hi</tw-passagedata></tw-storydata></html>'
    )
    mod = "apps.game_generation.services.game_service"
    with patch(f"{mod}.logger") as mock_logger:
        with patch(f"{mod}._installed_sugarcube_version", return_value="2.36.1"), patch(
            f"{mod}.subprocess.run",
            return_value=Mock(returncode=0, stdout=BANNER, stderr=""),
        ):
            with patch("builtins.open", create=True) as mock_open:
                mock_open.return_value.__enter__.return_value.read.return_value = html
                with patch(f"{mod}.os.path.exists", return_value=True), patch(
                    f"{mod}.os.unlink"
                ):
                    assert service.compile_twee_to_html(TWEE, "Probe") == html

    assert mock_logger.warning.called, "a swapped story format must not pass unnoticed"
    emitted = " ".join(str(a) for a in mock_logger.warning.call_args.args)
    assert "SugarCube version mismatch" in emitted
    assert "2.36.1" in emitted


def test_the_generator_declares_the_sugarcube_that_is_installed():
    """⚠️ Tweego HARD-ERRORS on a format-version it does not have — "Story format
    named \"SugarCube\" at version ... is not available" — and our packager only
    escapes that because it passes `-f sugarcube-2`, which overrides StoryData
    outright. So a wrong declaration is inert for us and fatal for anyone compiling
    the same Twee any other way. It read 2.36.1 against an installed 2.30.0 from the
    day the generator was written until 2026-08-29."""
    src = Path("apps/game_generation/twee_comprehensive/generators/v2.py").read_text(
        encoding="utf-8"
    )
    declared = set(re.findall(r'"format-version":\s*"([^"]+)"', src))
    assert declared == {EXPECTED_SUGARCUBE_VERSION}, declared
