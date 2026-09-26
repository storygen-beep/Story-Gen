#!/usr/bin/env python3
"""Package a built game and publish it to the download mirrors, then print the
post text that Patreon, Discord and F95 all need.

    python3 scripts/release_upload.py vesper

Why this exists
---------------
The 0.1.9 release shipped with `games/vesper/output.zip` four days older than the
build it was supposed to contain, and nobody noticed. That is the bug this kills:
the archive is produced FROM the build every time, and the version comes out of
the game's own TOML rather than being typed in by hand.

The uploads are the smaller half. The real deliverable is step 9 — a verified
block of links you can paste into all five destinations without re-checking
anything.

Mirrors
-------
Mega, then Pixeldrain, then Gofile, then MixDrop — the order comes from
measuring the top 20 HTML games on F95: Mega 90%, Pixeldrain 85%, Gofile 70%,
MixDrop 35%.

Mega needs MEGAcmd installed and logged in once (see --help-mega). Gofile needs
nothing at all. MixDrop needs a free account's API credentials
(see --help-mixdrop). Pixeldrain sits behind --with-pixeldrain: it is blocked or
flaky on some Indian ISPs and no longer accepts anonymous uploads.

The F95 uploader team adds VikingFile, DataNodes and Buzzheavier on top of
whatever we post — measured at 60-80% of top threads each — so the job here is
to supply a couple of good links, not to match a finished thread.

Credentials never live in this repo — it is public. They are read from the
environment, optionally sourced from ~/.config/storygen/release.env.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

import tomli

REPO_ROOT = Path(__file__).resolve().parent.parent

# Substrings that must never appear in a release build. `devJumps` is the dev
# jump menu; the MISSING markers are what the generator writes in place of a
# media file it could not resolve. Both are invisible in a --dev build and
# glaring in a shipped one, which is exactly why they need a machine check.
DEV_BUILD_MARKERS = ("devJumps", "IMAGE MISSING", "VIDEO MISSING", "DEV MODE")

# A git checkout stamps the whole tree with one mtime, so the TOML can land a
# few ms "after" the build it produced. Anything under this is that, not an edit.
CHECKOUT_MTIME_TOLERANCE_SECONDS = 120

# Media the built HTML points at, e.g. videos/sex/foo_t5/abc123.mp4
MEDIA_REF = re.compile(r"videos/[A-Za-z0-9_/.\-]+\.(?:mp4|webm|jpg|jpeg|png|webp|gif)")

MIXDROP_UPLOAD = "https://ul.mixdrop.ag/api"
MIXDROP_INFO = "https://api.mixdrop.ag/fileinfo2"

# Pixeldrain is the third-most-used host on F95 and the one we cannot rely on
# here. Reliance Jio poisons its DNS to 49.44.79.236, and of its four real IPs
# only 103.107.199.58 completed a TLS handshake at all — intermittently.
# It also stopped accepting anonymous uploads: the API now answers
# "authentication_required" and wants a key. Measured 2026-08-26. MixDrop was
# taken as the reachable substitute; this stays behind --with-pixeldrain.
PIXELDRAIN_UPLOAD = "https://pixeldrain.com/api/file/"
PIXELDRAIN_INFO = "https://pixeldrain.com/api/file/{file_id}/info"
PIXELDRAIN_PUBLIC = "https://pixeldrain.com/u/{file_id}"


class ReleaseError(RuntimeError):
    """A check failed hard enough that publishing would ship something wrong."""


# ── environment ───────────────────────────────────────────────────────────────


def load_env_file() -> None:
    """Read ~/.config/storygen/release.env into os.environ if it exists.

    Kept outside the repo on purpose: this repo is public, and a committed
    credential stays in the history after it is deleted.
    """
    env_path = Path.home() / ".config" / "storygen" / "release.env"
    if not env_path.is_file():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


# ── the game's own facts ──────────────────────────────────────────────────────


def read_project_block(toml_path: Path) -> dict:
    with toml_path.open("rb") as handle:
        return tomli.load(handle).get("project", {})


def resolve_version(game_dir: Path) -> tuple[str, str]:
    """Return (title, version), refusing to guess when the sources disagree.

    `0_systems_spec.toml` is what the author edits; `7_final_game.toml` is the
    merged file the build actually consumed. If they have drifted, the merge was
    never re-run and the build on disk is not the version we are about to claim.
    """
    spec = game_dir / "toml_phases" / "0_systems_spec.toml"
    merged = game_dir / "toml_phases" / "7_final_game.toml"
    if not spec.is_file():
        raise ReleaseError(f"no {spec.relative_to(REPO_ROOT)}")

    spec_project = read_project_block(spec)
    version = str(spec_project.get("version", "")).strip()
    title = str(spec_project.get("title", game_dir.name)).strip()
    if not version:
        raise ReleaseError(f"[project] version is not set in {spec.name}")

    if merged.is_file():
        merged_version = str(read_project_block(merged).get("version", "")).strip()
        if merged_version and merged_version != version:
            raise ReleaseError(
                f"version drift: {spec.name} says {version} but {merged.name} says "
                f"{merged_version}. Re-run scripts/merge_toml_phases.py and rebuild."
            )
    return title, version


# ── pre-flight checks on the build ────────────────────────────────────────────


def check_build_is_fresh(game_dir: Path, output_html: Path) -> None:
    """Fail if any phase TOML is meaningfully newer than the build.

    This is the 0.1.9 staleness bug as a check. The tolerance is not cosmetic:
    a git checkout rewrites every mtime in the tree within the same instant, so
    an exact comparison flags a clean checkout as stale — measured here at 27 ms.
    A real "edited it and forgot to rebuild" gap is minutes at minimum.
    """
    phase_files = sorted((game_dir / "toml_phases").glob("*.toml"))
    if not phase_files:
        return
    newest = max(phase_files, key=lambda p: p.stat().st_mtime)
    drift_seconds = newest.stat().st_mtime - output_html.stat().st_mtime
    if drift_seconds > CHECKOUT_MTIME_TOLERANCE_SECONDS:
        raise ReleaseError(
            f"{newest.name} is {drift_seconds / 60:.0f} min newer than "
            f"output/index.html — the build is stale. Rebuild, or pass "
            f"--allow-stale if you know why."
        )


def check_version_is_baked_in(output_html: Path, version: str) -> None:
    """The version we are about to publish must appear inside the build itself.

    Stronger than the mtime check and immune to checkout noise: the engine bakes
    the version into the sidebar footer and the cheat-code salt, so bumping
    [project] version without rebuilding leaves the new number nowhere in the
    HTML. That is the exact shape of the 0.1.9 mistake.
    """
    html = output_html.read_text(encoding="utf-8", errors="replace")
    if f"v{version}" not in html and f'"{version}"' not in html:
        raise ReleaseError(
            f"the TOML says version {version} but that string is nowhere in "
            f"output/index.html — the build predates the version bump. Rebuild."
        )


def check_is_release_build(output_html: Path) -> None:
    html = output_html.read_text(encoding="utf-8", errors="replace")
    # "DEV MODE" is matched case-sensitively: the lowercase spellings are a code
    # comment and a CSS class name that ship in every build.
    found = [marker for marker in DEV_BUILD_MARKERS if marker in html]
    if found:
        raise ReleaseError(
            f"output/index.html carries dev-build markers {found} — "
            f"rebuild without --dev/--debug"
        )


GATES_PY = REPO_ROOT / ".claude" / "skills" / "author-game-v2" / "scripts" / "gates.py"


def check_ship(slug: str) -> None:
    """Refuse to package a v2 game that `gates.py --ship` does not pass.

    Added 2026-09-26 (PRD WS6). The ship check blocks only what makes a build broken,
    unfinishable or untrue, and prints everything else for the author to judge; its
    output is shown here unfiltered. A game without games/<slug>/v2_state.json is not a
    v2 game (vesper) and is not checked.
    """
    if not (REPO_ROOT / "games" / slug / "v2_state.json").is_file():
        print(f"note: {slug} has no v2_state.json — not a v2 game, ship check skipped")
        return
    rc = subprocess.run([sys.executable, str(GATES_PY), "--ship", slug], cwd=REPO_ROOT).returncode
    if rc != 0:
        raise ReleaseError(f"gates.py --ship {slug} failed — see the BLOCK list above")


def check_media_present(output_dir: Path, output_html: Path) -> int:
    """Every media path the HTML references must exist on disk.

    A missing clip is silent in the browser (the element just renders empty), so
    it survives right up until a player finds the hole.
    """
    html = output_html.read_text(encoding="utf-8", errors="replace")
    refs = sorted(set(MEDIA_REF.findall(html)))
    missing = [ref for ref in refs if not (output_dir / ref).is_file()]
    if missing:
        preview = "\n  ".join(missing[:10])
        raise ReleaseError(
            f"{len(missing)} referenced media file(s) missing from output/:\n  {preview}"
            + ("\n  ..." if len(missing) > 10 else "")
        )
    return len(refs)


# ── packaging ─────────────────────────────────────────────────────────────────


def safe_stem(title: str, version: str) -> str:
    """Build an archive name that survives every OS the player might unzip on.

    A title like "Vesper: The Leash" would otherwise produce a filename with a
    colon in it — illegal on Windows, and displayed as "/" by Finder. Strip the
    characters Windows forbids rather than trusting the title to be tame.
    """
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", title).strip()
    return re.sub(r"-{2,}", "-", cleaned.replace(" ", "-")) + f"-v{version}"


def count_payload_files(output_dir: Path) -> int:
    return sum(
        1
        for path in output_dir.rglob("*")
        if path.is_file() and path.name != ".DS_Store"
    )


def build_archive(output_dir: Path, dist_dir: Path, stem: str) -> Path:
    """Zip output/ as a single sensibly-named folder, with no macOS cruft.

    The existing output.zip was made by Finder, which pairs every entry with a
    `__MACOSX/._name` resource fork — 1,120 junk entries for 481 real files.
    `zip -X` drops the extra attributes; staging under `stem` means the player
    extracts "Vesper-v0.1.9/" rather than a generic "output/".
    """
    dist_dir.mkdir(parents=True, exist_ok=True)
    # dist/ holds build artefacts and link records; keep the whole thing out of
    # git rather than relying on the global *.zip rule.
    (dist_dir / ".gitignore").write_text("*\n", encoding="utf-8")

    archive_path = dist_dir / f"{stem}.zip"
    if archive_path.exists():
        archive_path.unlink()

    with tempfile.TemporaryDirectory(prefix="release-stage-") as tmp:
        staged = Path(tmp) / stem
        # -c clones on APFS: instant, and costs no extra disk for 245 MB.
        if subprocess.run(["cp", "-Rc", str(output_dir), str(staged)]).returncode != 0:
            subprocess.run(["cp", "-R", str(output_dir), str(staged)], check=True)

        subprocess.run(
            ["zip", "-r", "-X", "-q", str(archive_path), stem, "-x", "*.DS_Store"],
            cwd=tmp,
            check=True,
        )
    return archive_path


def verify_archive(archive_path: Path, expected_files: int, stem: str) -> None:
    listing = subprocess.run(
        ["unzip", "-Z1", str(archive_path)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()

    entries = [line for line in listing if line and not line.endswith("/")]
    if any("__MACOSX" in line for line in listing):
        raise ReleaseError("archive contains __MACOSX entries — the -X flag did not take")
    if not any(line == f"{stem}/index.html" for line in listing):
        raise ReleaseError(f"archive has no {stem}/index.html at its root")
    if len(entries) != expected_files:
        raise ReleaseError(
            f"archive holds {len(entries)} files but output/ has {expected_files}"
        )


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


# ── mirrors ───────────────────────────────────────────────────────────────────


GOFILE_SERVERS = "https://api.gofile.io/servers"
GOFILE_UPLOAD = "https://{server}.gofile.io/contents/uploadfile"


def upload_gofile(archive_path: Path) -> str:
    """Upload to Gofile and return the public download page.

    No account and no token: that requirement belongs to rclone's Gofile
    backend, not to the API itself. The upload response reports the stored size
    back, so the mirror tells us what it received instead of us trusting the
    transfer — which matters more here than elsewhere, because a Gofile link
    cannot be re-checked afterwards (see check_link).
    """
    try:
        with urllib.request.urlopen(GOFILE_SERVERS, timeout=30) as response:
            servers = json.load(response)["data"]["servers"]
    except (urllib.error.URLError, ValueError, KeyError) as exc:
        raise ReleaseError(f"could not pick a gofile server: {exc}") from exc
    if not servers:
        raise ReleaseError("gofile returned no available servers")

    endpoint = GOFILE_UPLOAD.format(server=servers[0]["name"])
    result = subprocess.run(
        ["curl", "--fail", "--silent", "--show-error", "-F", f"file=@{archive_path}", endpoint],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise ReleaseError(f"gofile upload failed: {result.stderr.strip()}")
    try:
        data = json.loads(result.stdout)["data"]
        url = data["downloadPage"]
    except (ValueError, KeyError) as exc:
        raise ReleaseError(f"unreadable gofile response: {result.stdout[:200]}") from exc

    stored = int(data.get("size", -1))
    if stored != archive_path.stat().st_size:
        raise ReleaseError(
            f"gofile stored {stored} bytes, archive is {archive_path.stat().st_size}"
        )
    return url


def upload_mixdrop(archive_path: Path) -> str | None:
    """Upload to MixDrop and return the public file page.

    Chosen as the third mirror after Pixeldrain proved unusable here: MixDrop
    carries 35% of the top HTML games on F95, has a 10 GB ceiling, and is
    reachable on this connection where Pixeldrain, Workupload and Krakenfiles
    are all blocked.

    Returns None rather than raising when the credentials are absent, so a
    release still goes out on the other mirrors while this is being set up.
    """
    email = os.environ.get("MIXDROP_EMAIL")
    key = os.environ.get("MIXDROP_KEY")
    if not (email and key):
        return None

    result = subprocess.run(
        [
            "curl", "--fail", "--silent", "--show-error", "-X", "POST",
            "-F", f"email={email}", "-F", f"key={key}",
            "-F", f"file=@{archive_path}",
            MIXDROP_UPLOAD,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise ReleaseError(f"mixdrop upload failed: {result.stderr.strip()}")
    try:
        payload = json.loads(result.stdout)
    except ValueError as exc:
        raise ReleaseError(f"unreadable mixdrop response: {result.stdout[:200]}") from exc
    if not payload.get("success"):
        raise ReleaseError(f"mixdrop refused the upload: {payload.get('result')}")
    return payload["result"]["url"]


def check_mixdrop_link(url: str) -> tuple[str, str]:
    """Ask MixDrop's own API whether the file is still there.

    Their file page is a single-page app and answers 200 for a dead reference,
    so an HTTP fetch would lie. The API needs the same credentials as the
    upload; without them we say "unknown" rather than guess.
    """
    email = os.environ.get("MIXDROP_EMAIL")
    key = os.environ.get("MIXDROP_KEY")
    if not (email and key):
        return "unknown", "set MIXDROP_EMAIL/MIXDROP_KEY to let this be checked"
    ref = url.rstrip("/").rsplit("/", 1)[-1]
    query = urllib.parse.urlencode({"email": email, "key": key, "ref[]": ref})
    # MixDrop 403s Python's default User-Agent while serving the identical
    # request to curl. Measured 2026-08-26 — the header is not optional.
    request = urllib.request.Request(
        f"{MIXDROP_INFO}?{query}", headers={"User-Agent": "Mozilla/5.0"}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except (urllib.error.URLError, ValueError) as exc:
        return "unknown", f"could not reach the MixDrop API ({exc})"
    if not payload.get("success"):
        return "unknown", str(payload.get("result"))
    info = (payload.get("result") or {}).get(ref) or {}
    if str(info.get("status", "")).lower() == "notfound":
        return "dead", "MixDrop reports no such file"
    if info.get("size"):
        return "live", f"{int(info['size']) / (1024 * 1024):.1f} MB on the server"
    return "unknown", f"unrecognised MixDrop reply: {info}"


def upload_pixeldrain(archive_path: Path) -> str:
    """PUT the archive and return its public URL.

    curl rather than urllib: it streams a 245 MB body without holding it in
    memory and prints a progress bar, which matters when you are watching it.
    An API key is optional — uploading works anonymously — but with one the file
    belongs to the account and can be managed later.
    """
    command = ["curl", "--fail", "--silent", "--show-error", "-T", str(archive_path)]
    api_key = os.environ.get("PIXELDRAIN_API_KEY")
    if api_key:
        command += ["-u", f":{api_key}"]
    command.append(PIXELDRAIN_UPLOAD)

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise ReleaseError(f"pixeldrain upload failed: {result.stderr.strip()}")
    try:
        file_id = json.loads(result.stdout)["id"]
    except (ValueError, KeyError) as exc:
        raise ReleaseError(f"unreadable pixeldrain response: {result.stdout[:200]}") from exc
    return PIXELDRAIN_PUBLIC.format(file_id=file_id)


def verify_pixeldrain(url: str, expected_size: int) -> None:
    """Confirm the link resolves and the stored size matches what we sent.

    Publishing an unverified link is the one failure the reader sees before we
    do — a supporter clicking a dead link reads as sloppiness, not bad luck.
    """
    file_id = url.rsplit("/", 1)[-1]
    try:
        with urllib.request.urlopen(PIXELDRAIN_INFO.format(file_id=file_id), timeout=30) as response:
            info = json.load(response)
    except (urllib.error.URLError, ValueError) as exc:
        raise ReleaseError(f"could not verify {url}: {exc}") from exc

    if int(info.get("size", -1)) != expected_size:
        raise ReleaseError(
            f"pixeldrain reports {info.get('size')} bytes, archive is {expected_size}"
        )


def upload_mega(archive_path: Path) -> str | None:
    """Upload via MEGAcmd and export a public link, if MEGAcmd is installed.

    Deliberately not wired to the personal account: point MEGAcmd at a throwaway
    login before enabling this. The archive carries sourced footage, and on Mega
    the account password is also the key to everything else in the drive.
    """
    if shutil.which("mega-put") is None:
        return None
    remote = f"/{archive_path.name}"
    if subprocess.run(["mega-put", str(archive_path), remote]).returncode != 0:
        raise ReleaseError("mega-put failed — check `mega-whoami`")
    exported = subprocess.run(
        ["mega-export", "-a", remote], capture_output=True, text=True
    )
    if exported.returncode != 0:
        raise ReleaseError(f"mega-export failed: {exported.stderr.strip()}")
    match = re.search(r"https://mega\.nz/\S+", exported.stdout)
    if not match:
        raise ReleaseError(f"no link in mega-export output: {exported.stdout[:200]}")
    return match.group(0)


# ── output ────────────────────────────────────────────────────────────────────


def render_post_blocks(title: str, version: str, links: dict[str, str], size_mb: float) -> str:
    """Both paste formats. Order is deliberate — see the host study.

    Mega leads because 90% of the top HTML games on F95 carry it and players
    look for it first. Its per-IP transfer quota is real, but that is an argument
    for carrying several mirrors rather than for demoting the one everybody uses
    — which is exactly what the top threads do, at ~6 mirrors apiece.
    """
    order = ["Mega", "Pixeldrain", "Gofile", "Mixdrop"]
    live = [(name, links[name]) for name in order if links.get(name)]

    f95_line = " - ".join(f"[URL={url}]{name.upper()}[/URL]" for name, url in live)
    patreon_line = " | ".join(f"{name}: {url}" for name, url in live)

    return "\n".join(
        [
            "=" * 72,
            f"  {title} v{version}   ({size_mb:.1f} MB, {date.today().isoformat()})",
            "=" * 72,
            "",
            "--- F95zone, inside the DOWNLOAD block -------------------------------",
            f"[B]All[/B]: {f95_line}",
            "",
            "--- Patreon / Discord, replaces `Download: [LINK]` -------------------",
            f"Download: {patreon_line}",
            "",
            "--- raw --------------------------------------------------------------",
            *[f"{name:<11} {url}" for name, url in live],
            "",
        ]
    )


MEGA_API = "https://g.api.mega.co.nz/cs"


def check_mega_link(url: str) -> tuple[str, str]:
    """Ask Mega's own API whether the file is still there, and how big it is.

    Measured 2026-08-24: `[{"a":"g","p":"<id>"}]` returns `{"s": <bytes>, ...}`
    for a live file and `[-9]` for one that is gone. This is the only one of the
    three mirrors where a link can be checked properly rather than guessed at.
    """
    match = re.search(r"mega\.nz/file/([A-Za-z0-9_-]+)", url)
    if not match:
        return "unknown", "could not read a file id out of the link"
    payload = json.dumps([{"a": "g", "p": match.group(1)}]).encode()
    request = urllib.request.Request(
        MEGA_API, data=payload, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = json.load(response)
    except (urllib.error.URLError, ValueError) as exc:
        return "unknown", f"could not reach the Mega API ({exc})"

    if isinstance(body, list) and body and isinstance(body[0], dict) and "s" in body[0]:
        return "live", f"{int(body[0]['s']) / (1024 * 1024):.1f} MB on the server"
    return "dead", "Mega reports the file no longer exists"


def check_http_link(url: str) -> tuple[str, str]:
    """Plain fetch, for hosts that answer honestly with a status code."""
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return ("live" if response.status < 400 else "dead"), f"HTTP {response.status}"
    except urllib.error.HTTPError as exc:
        return "dead", f"HTTP {exc.code}"
    except urllib.error.URLError as exc:
        return "unknown", str(exc.reason)


def check_link(name: str, url: str) -> tuple[str, str]:
    """Verify one published link, and say plainly when we cannot.

    Mega gets a real check against its own API. Everything else falls back to an
    HTTP fetch, which is only as honest as the host.

    Gofile is never reported as live, because it cannot be: measured 2026-08-24,
    its download page, its anonymous API and its token-authenticated API were
    byte-identical for a real code and an invented one. Returning "OK" there
    would be a guess dressed as a check, and Gofile is also the mirror that rots
    fastest — roughly ten idle days — so a false OK is the likeliest false OK we
    could print. Mega is the durable link; Gofile is the fallback for someone
    whose Mega quota is spent.
    """
    if name == "Mega":
        return check_mega_link(url)
    if name == "Mixdrop":
        return check_mixdrop_link(url)
    if name == "Gofile":
        return "unknown", "Gofile links cannot be verified — open it yourself"
    return check_http_link(url)


def check_existing_links(dist_dir: Path) -> int:
    """Re-test the most recent release's links.

    Published links rot — hosts prune idle files and takedowns happen. Better we
    find a dead mirror than a supporter does.
    """
    records = sorted(dist_dir.glob("*.links.json"))
    if not records:
        raise ReleaseError(f"no release records in {dist_dir}")
    record = json.loads(records[-1].read_text(encoding="utf-8"))

    print(f"{record['title']} v{record['version']} — published {record['date']}")
    dead = 0
    for name, url in record.get("links", {}).items():
        state, detail = check_link(name, url)
        label = {"live": "LIVE", "dead": "DEAD", "unknown": "  ? "}[state]
        print(f"  {label}  {name:<11} {url}\n        {detail}")
        dead += 1 if state == "dead" else 0
    if dead:
        print(f"\n{dead} link(s) need re-uploading.")
    return dead


MIXDROP_HELP = """\
Enabling the MixDrop mirror
---------------------------
MixDrop is the third mirror because it carries 35% of the top HTML games on F95
and, unlike Pixeldrain, it is reachable without a VPN.

1. Sign up free at https://mixdrop.ag (use the release account, not a personal
   one — the archive carries sourced footage).
2. Open the API page and copy the API E-Mail and the API Key.
3. Put both in ~/.config/storygen/release.env  (NOT in the repo, it is public):

     MIXDROP_EMAIL=the-api-email-they-show-you
     MIXDROP_KEY=the-api-key

   chmod 600 that file.
4. Re-run this script. MixDrop is used automatically once both are set, and
   --check can then verify its links through their API.
"""


MEGA_HELP = """\
Enabling the Mega mirror
------------------------
1. Make a THROWAWAY Mega account — not the personal one. The archive carries
   sourced footage, and on Mega the password is the encryption key for the whole
   drive, so a takedown there should not be able to reach anything else.

2. brew install --cask megacmd-app

   NOTE THE PACKAGE NAME. `brew install megacmd` (no --cask) installs an
   unrelated third-party client by t3rm1n4l that shares the name. It can upload
   but has no export command, so it cannot produce the public link this script
   needs. MEGA's own tool is the cask `megacmd-app`, and it is the one that
   provides mega-put / mega-export / mega-whoami.

3. mega-login <throwaway-email>          (once; the session is remembered)

4. mega-whoami                           (should print the account, not an error)

5. Re-run this script. Mega is picked up automatically when `mega-put` exists.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", nargs="?", help="game folder under games/, e.g. vesper")
    parser.add_argument("--no-upload", action="store_true", help="package and verify only")
    parser.add_argument(
        "--check",
        action="store_true",
        help="re-test the links from the last release instead of publishing a new one",
    )
    parser.add_argument(
        "--with-pixeldrain",
        action="store_true",
        help="also mirror to Pixeldrain (blocked by some Indian ISPs — see the notes)",
    )
    parser.add_argument("--allow-stale", action="store_true", help="skip the build-freshness check")
    parser.add_argument("--help-mega", action="store_true", help="how to enable the Mega mirror")
    parser.add_argument(
        "--help-mixdrop", action="store_true", help="how to enable the MixDrop mirror"
    )
    args = parser.parse_args()

    if args.help_mega:
        print(MEGA_HELP)
        return 0
    if args.help_mixdrop:
        print(MIXDROP_HELP)
        return 0
    if not args.slug:
        parser.error("slug is required")

    load_env_file()

    game_dir = REPO_ROOT / "games" / args.slug
    output_dir = game_dir / "output"
    output_html = output_dir / "index.html"
    if not output_html.is_file():
        print(f"error: no build at {output_html.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    if args.check:
        try:
            return 1 if check_existing_links(game_dir / "dist") else 0
        except ReleaseError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    try:
        title, version = resolve_version(game_dir)
        if not args.allow_stale:
            check_build_is_fresh(game_dir, output_html)
            check_version_is_baked_in(output_html, version)
        check_is_release_build(output_html)
        media_refs = check_media_present(output_dir, output_html)
        check_ship(args.slug)

        stem = safe_stem(title, version)
        payload_files = count_payload_files(output_dir)

        print(f"{title} v{version}")
        print(f"  build      {payload_files} files, {media_refs} media references, all present")

        dist_dir = game_dir / "dist"
        archive_path = build_archive(output_dir, dist_dir, stem)
        verify_archive(archive_path, payload_files, stem)

        size_bytes = archive_path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        checksum = sha256_of(archive_path)
        print(f"  archive    {archive_path.name}  {size_mb:.1f} MB")
        print(f"  sha256     {checksum}")

        if args.no_upload:
            print("\n--no-upload: stopping before the mirrors.")
            return 0

        links: dict[str, str] = {}

        # One mirror failing must not lose a release that another mirror already
        # carried. Each is attempted independently and its error reported; the
        # guard below is what turns "all of them failed" into a non-zero exit.
        try:
            mega_url = upload_mega(archive_path)
            if mega_url:
                links["Mega"] = mega_url
                print(f"  mega       {mega_url}")
            else:
                print("  mega       skipped — MEGAcmd not installed (--help-mega)")
        except ReleaseError as exc:
            print(f"  mega       FAILED — {exc}")

        if args.with_pixeldrain:
            print("  pixeldrain uploading...")
            try:
                pixeldrain_url = upload_pixeldrain(archive_path)
                verify_pixeldrain(pixeldrain_url, size_bytes)
                links["Pixeldrain"] = pixeldrain_url
                print(f"  pixeldrain {pixeldrain_url}  (verified)")
            except ReleaseError as exc:
                print(f"  pixeldrain FAILED — {exc}")

        print("  gofile     uploading...")
        try:
            gofile_url = upload_gofile(archive_path)
            links["Gofile"] = gofile_url
            print(f"  gofile     {gofile_url}  (size confirmed by server)")
        except ReleaseError as exc:
            print(f"  gofile     FAILED — {exc}")

        try:
            mixdrop_url = upload_mixdrop(archive_path)
            if mixdrop_url:
                links["Mixdrop"] = mixdrop_url
                print(f"  mixdrop    {mixdrop_url}")
            else:
                print("  mixdrop    skipped — credentials not set (--help-mixdrop)")
        except ReleaseError as exc:
            print(f"  mixdrop    FAILED — {exc}")

        # An empty post block that still exits 0 is the worst outcome available:
        # it looks like the run worked and hands you nothing to paste.
        if not links:
            raise ReleaseError(
                "no mirror produced a link — the archive is built at "
                f"{archive_path.relative_to(REPO_ROOT)} but nothing was published. "
                "Set up Mega (--help-mega) or MixDrop (--help-mixdrop), or read the errors above."
            )

        record = {
            "game": args.slug,
            "title": title,
            "version": version,
            "date": date.today().isoformat(),
            "archive": archive_path.name,
            "size_bytes": size_bytes,
            "sha256": checksum,
            "links": links,
        }
        (dist_dir / f"{stem}.links.json").write_text(
            json.dumps(record, indent=2) + "\n", encoding="utf-8"
        )

        blocks = render_post_blocks(title, version, links, size_mb)
        (dist_dir / f"{stem}.post.txt").write_text(blocks, encoding="utf-8")
        print()
        print(blocks)
        print(f"saved: {(dist_dir / f'{stem}.post.txt').relative_to(REPO_ROOT)}")
        return 0

    except ReleaseError as exc:
        print(f"\nerror: {exc}", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as exc:
        print(f"\nerror: {exc.cmd[0]} exited {exc.returncode}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
