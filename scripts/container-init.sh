# It is for claude cloud container to run this script to install the dependencies for the project.
# Not for local agents


# !/usr/bin/env bash
#
# container-init.sh — make a fresh container able to BUILD games.
#   
# Installs the two external binaries this repo cannot work without:
#
#   ffmpeg/ffprobe  find-media's only hard dependency. Without it video_frames.py exits 3
#                   and no animated media slot can legally be filled, because a pick may
#                   not be installed unless its loop has been frame-stripped.
#   tweego          the game compiler. Without it package_from_toml now HARD FAILS.
#
# WHY THIS EXISTS. On 2026-07-28 two cloud sessions built media_lab_c and media_lab_d in a
# container with no Tweego. The packager silently fell back to a "Basic Preview Mode" page
# that prints the raw Twee source as text, announced "Package ready!", and 324,722 bytes of
# source dump were merged to the public portal. The fallback is now deleted (a build raises
# instead), so a container without Tweego fails loudly — this script is how it stops being
# without Tweego.
#
# SCOPE: build toolchain only. No database, no pip install, no Django dev server. Flows that
# need the API (media-finder/grab, game-review/load) are out of scope here by design.
#
# Safe to re-run: everything present and correct is detected and skipped.
#
#   Usage:  bash scripts/container-init.sh
#   Exit:   0 = ready to build,  1 = something required is missing
#
set -uo pipefail   # deliberately NOT -e: each step reports its own status into the summary

# Must match EXPECTED_TWEEGO_VERSION / EXPECTED_SUGARCUBE_VERSION in
# apps/game_generation/services/game_service.py. Tweego bundles its own story format, so the
# compiler version decides which SugarCube every game ships against.
TWEEGO_VERSION="2.1.1"
SUGARCUBE_VERSION="2.30.0"

# ~/bin is already in TWEEGO_SEARCH_PATHS in game_service.py, and mirrors the dev machine.
INSTALL_DIR="${HOME}/bin"

FFMPEG_OK=0; TWEEGO_OK=0; FORMAT_OK=0; SMOKE_OK=0
FFMPEG_NOTE="";  TWEEGO_NOTE="";  FORMAT_NOTE="";  SMOKE_NOTE=""

say()  { printf '  %s\n' "$*"; }
step() { printf '\n[%s] %s\n' "$1" "$2"; }

# Tweego prints --version and --list-formats to STDERR and exits 1 on success. Any check
# that reads stdout or trusts the exit code reports failure on a healthy install.
tweego_out() { "$1" "${@:2}" 2>&1 || true; }

# ---------------------------------------------------------------- 1. ffmpeg

step 1/3 "ffmpeg + ffprobe"
if command -v ffmpeg >/dev/null 2>&1 && command -v ffprobe >/dev/null 2>&1; then
    FFMPEG_OK=1
    FFMPEG_NOTE="$(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}')"
    say "already present (${FFMPEG_NOTE})"
else
    say "missing — installing"
    if command -v apt-get >/dev/null 2>&1; then
        (apt-get update -qq && apt-get install -y -qq ffmpeg) >/dev/null 2>&1 \
            || (sudo apt-get update -qq && sudo apt-get install -y -qq ffmpeg) >/dev/null 2>&1
    elif command -v dnf >/dev/null 2>&1; then
        dnf install -y -q ffmpeg >/dev/null 2>&1 || sudo dnf install -y -q ffmpeg >/dev/null 2>&1
    elif command -v apk >/dev/null 2>&1; then
        apk add --no-cache ffmpeg >/dev/null 2>&1 || sudo apk add --no-cache ffmpeg >/dev/null 2>&1
    elif command -v brew >/dev/null 2>&1; then
        brew install ffmpeg >/dev/null 2>&1
    else
        FFMPEG_NOTE="no supported package manager (apt/dnf/apk/brew)"
    fi

    if command -v ffmpeg >/dev/null 2>&1 && command -v ffprobe >/dev/null 2>&1; then
        FFMPEG_OK=1
        FFMPEG_NOTE="$(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}')"
        say "installed (${FFMPEG_NOTE})"
    else
        [ -n "$FFMPEG_NOTE" ] || FFMPEG_NOTE="install failed"
        say "FAILED — ${FFMPEG_NOTE}"
    fi
fi

# ---------------------------------------------------------------- 2. tweego

step 2/3 "tweego ${TWEEGO_VERSION} + storyformats"

find_tweego() {
    for c in tweego "${INSTALL_DIR}/tweego" /usr/local/bin/tweego /usr/bin/tweego \
             /opt/homebrew/bin/tweego; do
        command -v "$c" >/dev/null 2>&1 && { command -v "$c"; return 0; }
        [ -x "$c" ] && { printf '%s\n' "$c"; return 0; }
    done
    return 1
}

TWEEGO_BIN="$(find_tweego || true)"

if [ -n "$TWEEGO_BIN" ] && tweego_out "$TWEEGO_BIN" --version | grep -q "$TWEEGO_VERSION"; then
    TWEEGO_OK=1
    TWEEGO_NOTE="already present at ${TWEEGO_BIN}"
    say "$TWEEGO_NOTE"
else
    if [ -n "$TWEEGO_BIN" ]; then
        say "found ${TWEEGO_BIN} but it is not ${TWEEGO_VERSION} — installing the pinned build"
    else
        say "missing — installing ${TWEEGO_VERSION}"
    fi

    # Map uname to the published asset names. NOTE: upstream ships no linux-arm64 build —
    # fail clearly rather than guess, or we recreate the original bug one layer up.
    OS="$(uname -s)"; ARCH="$(uname -m)"
    case "$OS" in
        Linux)  ASSET_OS="linux"  ;;
        Darwin) ASSET_OS="macos"  ;;
        *)      ASSET_OS=""       ;;
    esac
    case "$ARCH" in
        x86_64|amd64) ASSET_ARCH="x64" ;;
        i386|i686)    ASSET_ARCH="x86" ;;
        arm64|aarch64)
            # macOS runs the x64 build under Rosetta 2; Linux has no equivalent.
            if [ "$ASSET_OS" = "macos" ]; then ASSET_ARCH="x64"; else ASSET_ARCH=""; fi ;;
        *)            ASSET_ARCH="" ;;
    esac

    if [ -z "$ASSET_OS" ] || [ -z "$ASSET_ARCH" ]; then
        TWEEGO_NOTE="no published Tweego build for ${OS}/${ARCH}"
        say "FAILED — ${TWEEGO_NOTE}"
        say "upstream ships linux-x64/x86, macos-x64/x86, windows-x64/x86 only."
        say "on linux-arm64 you must build Tweego from source (Go) — see"
        say "https://github.com/tmedwards/tweego"
    else
        ASSET="tweego-${TWEEGO_VERSION}-${ASSET_OS}-${ASSET_ARCH}.zip"
        URL="https://github.com/tmedwards/tweego/releases/download/v${TWEEGO_VERSION}/${ASSET}"
        TMP="$(mktemp -d)"
        say "downloading ${ASSET}"
        if curl -fsSL "$URL" -o "${TMP}/tweego.zip"; then
            # The archive carries the binary AND storyformats/. Both are required: the
            # binary alone runs but compiles nothing, because the story format is data.
            if command -v unzip >/dev/null 2>&1; then
                unzip -q -o "${TMP}/tweego.zip" -d "$TMP"
            else
                python3 -c "import zipfile,sys; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" \
                    "${TMP}/tweego.zip" "$TMP"
            fi
            mkdir -p "$INSTALL_DIR"
            SRC_BIN="$(find "$TMP" -type f -name tweego -perm -u+x | head -1)"
            [ -n "$SRC_BIN" ] || SRC_BIN="$(find "$TMP" -type f -name 'tweego*' ! -name '*.zip' | head -1)"
            SRC_FMT="$(find "$TMP" -type d -name storyformats | head -1)"
            if [ -n "$SRC_BIN" ] && [ -n "$SRC_FMT" ]; then
                cp "$SRC_BIN" "${INSTALL_DIR}/tweego"
                chmod +x "${INSTALL_DIR}/tweego"
                # storyformats must sit NEXT TO the binary — lookup is binary-relative and
                # cwd-independent (verified: found from /, /tmp and ~ alike).
                rm -rf "${INSTALL_DIR}/storyformats"
                cp -R "$SRC_FMT" "${INSTALL_DIR}/storyformats"
                TWEEGO_BIN="${INSTALL_DIR}/tweego"
                TWEEGO_OK=1
                TWEEGO_NOTE="installed -> ${TWEEGO_BIN}"
                say "$TWEEGO_NOTE"
            else
                TWEEGO_NOTE="archive missing binary or storyformats/"
                say "FAILED — ${TWEEGO_NOTE}"
            fi
        else
            TWEEGO_NOTE="download failed: ${URL}"
            say "FAILED — ${TWEEGO_NOTE}"
        fi
        rm -rf "$TMP"
    fi
fi

# storyformats reachable? This is a separate failure from "binary runs".
if [ "$TWEEGO_OK" = "1" ]; then
    FORMATS="$(tweego_out "$TWEEGO_BIN" --list-formats)"
    if printf '%s' "$FORMATS" | grep -q "sugarcube-2"; then
        FORMAT_OK=1
        FORMAT_NOTE="$(printf '%s' "$FORMATS" | grep 'sugarcube-2' | tr -s ' ' | sed 's/^ //')"
        say "storyformats: ${FORMAT_NOTE}"
        printf '%s' "$FORMATS" | grep -q "$SUGARCUBE_VERSION" || \
            say "WARNING: expected SugarCube ${SUGARCUBE_VERSION} — every portal game was built against it"
    else
        FORMAT_NOTE="sugarcube-2 not found next to the binary"
        say "FAILED — ${FORMAT_NOTE}"
    fi
fi

if [ -n "${TWEEGO_BIN:-}" ] && [ "$(dirname "$TWEEGO_BIN")" = "$INSTALL_DIR" ]; then
    case ":${PATH}:" in
        *":${INSTALL_DIR}:"*) ;;
        *) say "NOTE: ${INSTALL_DIR} is not on PATH — add it, or rely on the search paths"
           say "      already baked into game_service.py (it looks in ~/bin)." ;;
    esac
fi

# ---------------------------------------------------------------- 3. smoke compile

step 3/3 "smoke compile"
if [ "$FORMAT_OK" = "1" ]; then
    # The only check that proves the toolchain actually works. Mirrors the assertion in
    # game_service._compile_with_tweego: a real build has story data AND passages.
    TMP="$(mktemp -d)"
    # StoryData with a fixed IFID is REQUIRED — without it Tweego refuses to compile
    # ("Story IFID not found") and writes no output at all. The UUID is arbitrary; this
    # file is a throwaway probe, never a game.
    {
        printf ':: StoryTitle\nSmoke\n\n'
        printf ':: StoryData\n{"ifid":"E57CCAC2-CD31-4742-B430-D7F22779B7CE",'
        printf '"format":"SugarCube","format-version":"%s"}\n\n' "$SUGARCUBE_VERSION"
        printf ':: Start\nhello [[Next]]\n\n:: Next\ndone\n'
    } > "${TMP}/s.twee"
    "$TWEEGO_BIN" -f sugarcube-2 "${TMP}/s.twee" -o "${TMP}/s.html" >/dev/null 2>&1
    if [ -f "${TMP}/s.html" ] \
       && grep -q "tw-storydata"  "${TMP}/s.html" \
       && grep -q "tw-passagedata" "${TMP}/s.html"; then
        SMOKE_OK=1
        SMOKE_NOTE="real SugarCube, $(grep -o 'tw-passagedata' "${TMP}/s.html" | wc -l | tr -d ' ') passages"
        say "ok (${SMOKE_NOTE})"
    else
        SMOKE_NOTE="compiled nothing usable"
        say "FAILED — ${SMOKE_NOTE}"
    fi
    rm -rf "$TMP"
else
    SMOKE_NOTE="skipped (no usable tweego)"
    say "$SMOKE_NOTE"
fi

# ---------------------------------------------------------------- summary

mark() { [ "$1" = "1" ] && printf 'ok     ' || printf 'MISSING'; }

printf '\n%s\n' "----------------------------------------------------------------"
printf '  ffmpeg + ffprobe ....... %s  %s\n' "$(mark $FFMPEG_OK)" "$FFMPEG_NOTE"
printf '  tweego %-15s %s  %s\n' "$TWEEGO_VERSION" "$(mark $TWEEGO_OK)" "$TWEEGO_NOTE"
printf '  storyformats ........... %s  %s\n' "$(mark $FORMAT_OK)" "$FORMAT_NOTE"
printf '  smoke compile .......... %s  %s\n' "$(mark $SMOKE_OK)" "$SMOKE_NOTE"
printf '\n  Django API ............. not set up (build toolchain only, by design)\n'
printf '%s\n' "----------------------------------------------------------------"

if [ "$FFMPEG_OK" = "1" ] && [ "$SMOKE_OK" = "1" ]; then
    printf '\n  READY. Builds will compile; there is no preview fallback to hide a failure.\n\n'
    exit 0
fi

printf '\n  NOT READY — fix the MISSING rows above before building or running find-media.\n'
printf '  A build without Tweego now exits non-zero and writes nothing (by design).\n\n'
exit 1



