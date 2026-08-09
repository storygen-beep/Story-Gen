"""Recover where already-installed clips came from — by arithmetic, not by search.

Installing a clip CONSUMES its option row (`_drop_option`, api/v1/media_finder.py),
and that row held the only copy of the clip's Google `docid`. The `picks` root fixes
that going forward; every file installed before 2026-08-09 is still provenance-less,
which in the picker means a selected clip that can never seed a related fetch.

Most of them can be recovered without asking anybody anything, because a pool member
is NAMED after its source url:

    _pool_member_stem(url) -> "c" + md5(url).hexdigest()[:10]

md5 is one-way, so this is not a search — it is a JOIN. Hash every url still sitting
on any shelf in the game, and look for a pool file with that stem. A match is a
proven preimage: a false positive needs a 40-bit collision, ~7e-6 expected across
vesper's 45k urls x 182 files. The matched option row still carries the docid, the
thumb and the search that found it, so all three come back.

Two things it recovers, and one it cannot:

  * pool members            c<md5>.<ext>                -> a `picks` entry
  * demoted picks           c<md5>-<stamp>.<ext> in     -> `source_url`/`docid` written
    (pool_unselect moves    .find-media/previous/          back onto the option row
     the file, keeping the stem)
  * SINGLE-slot installs                                -> nothing. Ever. grab names
    those after the SLOT (`parse_scene_path`), so no join key was written at the time
    and none can be derived now. Reported honestly rather than papered over.

A clip whose url is no longer on ANY shelf in the game is left exactly as it is.
Finding it again would mean driving Chrome at Google, which this command does not do:
it opens no socket of any kind.

Read-only by default — the count IS the useful output. `--write` backs the ledger up
to media_options.json.bak first, and never overwrites a pick that was recorded
first-hand: a recovered entry is marked `"recovered": true` because its `found_by` is
the shelf's labels TODAY and may name searches that ran after the install.

    python manage.py backfill_picks --game vesper
    python manage.py backfill_picks --all --write
"""

import re
from datetime import datetime, timezone
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from api.v1.media_finder import (
    _options_lock,
    _options_path,
    _pool_member_stem,
    _pool_members,
    _read_options,
    _write_options,
)
from api.v1.media_review import _enumerate

GAMES_ROOT = Path(settings.BASE_DIR) / "games"

# What `_pool_member_stem` produces: "c" + md5(url)[:10].
_POOL_STEM_RE = re.compile(r"^c[0-9a-f]{10}$")
# The same stem after `pool_unselect` moved the file into .find-media/previous/,
# which appends a UTC stamp but keeps the hash intact — which is exactly why a
# demoted pool clip is recoverable and a demoted single-slot one is not.
_DEMOTED_STEM_RE = re.compile(r"^(c[0-9a-f]{10})-\d{8}-\d{6}$")


def _remote_of(row: dict) -> str:
    """The fetchable url a row knows about — its own, or the one a demoted pick was
    installed from. A `/games/…` path is a serve path no index has ever seen."""
    for key in ("url", "source_url"):
        value = str(row.get(key) or "")
        if value.lower().startswith(("http://", "https://")):
            return value
    return ""


def _url_index(data: dict) -> dict:
    """stem -> the best option row for the url that hashes to it, across EVERY slot.

    Cross-slot on purpose. Measured on vesper: of the 101 installed pool clips whose
    url still exists somewhere, only 15 are on their own slot's shelf — the other 86
    survive only because a different slot searched for the same thing. Restricting
    the join to the clip's own shelf would recover 15% of what is actually provable.
    """
    index: dict = {}
    for rows in data.get("options", {}).values():
        for row in rows:
            url = _remote_of(row)
            if not url:
                continue
            stem = _pool_member_stem(url)
            best = index.get(stem)
            # Prefer a row that carries an id. The whole point of the join is the
            # docid, and the same url can sit on several shelves with only one of
            # them enriched by a harvest that captured ids.
            if best is None or (row.get("docid") and not best.get("docid")):
                index[stem] = row
    return index


def _pick_from(row: dict, filename: str, at: str) -> dict:
    entry = {"filename": filename, "at": at, "recovered": True}
    url = _remote_of(row)
    if url:
        entry["url"] = url
    for key in ("docid", "thumb", "found_by"):
        if row.get(key):
            entry[key] = row[key]
    return entry


class Command(BaseCommand):
    help = "Recover provenance for clips installed before the picks table existed"

    def add_arguments(self, parser):
        parser.add_argument("--game", type=str, help="Game slug (folder under games/)")
        parser.add_argument(
            "--all", action="store_true", help="Every game that has a shelf"
        )
        parser.add_argument(
            "--write",
            action="store_true",
            help="Commit the recovered rows (backs the ledger up first)",
        )

    def handle(self, *args, **options):
        game = options.get("game")
        if not game and not options.get("all"):
            raise CommandError("Pass --game <slug> or --all")

        if options.get("all"):
            games = sorted(
                p.parts[-3] for p in GAMES_ROOT.glob("*/.find-media/media_options.json")
            )
        else:
            games = [game]

        totals = {"picks": 0, "demoted": 0, "unmatched": 0, "single": 0}
        for slug in games:
            for key, value in self._run(slug, bool(options.get("write"))).items():
                totals[key] += value

        self.stdout.write("")
        summary = (
            f"{totals['picks']} pick(s) recovered, "
            f"{totals['demoted']} demoted option(s) repaired, "
            f"{totals['unmatched']} pool clip(s) unmatched, "
            f"{totals['single']} single-slot install(s) unrecoverable"
        )
        if options.get("write"):
            self.stdout.write(self.style.SUCCESS(summary))
        else:
            self.stdout.write(
                self.style.WARNING(summary + "  —  dry run, nothing written")
            )
            self.stdout.write("Re-run with --write to commit.")

    # ------------------------------------------------------------------ per game

    def _run(self, slug: str, write: bool) -> dict:
        counts = {"picks": 0, "demoted": 0, "unmatched": 0, "single": 0}
        game_dir = GAMES_ROOT / slug
        if not game_dir.is_dir():
            raise CommandError(f"Game '{slug}' not found under {GAMES_ROOT}")

        enumerated = _enumerate(slug, game_dir)
        if enumerated is None:
            self.stdout.write(self.style.WARNING(f"{slug}: no merged TOML — skipped"))
            return counts

        # The lock is held across read AND write so a picker POST landing mid-run
        # cannot have its change read, discarded and overwritten.
        with _options_lock(game_dir):
            data = _read_options(game_dir)
            index = _url_index(data)
            now = datetime.now(timezone.utc).isoformat()
            lines: list = []

            for item in enumerated["items"]:
                slot_key = item.get("slot_key") or item.get("file") or ""
                if not slot_key:
                    continue
                pool_dir = item.get("pool_dir")
                if pool_dir:
                    counts_delta = self._recover_pool(
                        data, index, game_dir, slot_key, pool_dir, now, lines
                    )
                elif item.get("found") and item.get("serve_path"):
                    # Named after the slot, so there is no hash to join on. Counted,
                    # never guessed: the wrong url here would put a stranger's docid
                    # behind this clip's ⇢.
                    filename = Path(item["serve_path"]).name
                    already = any(
                        p.get("filename") == filename
                        for p in data["picks"].get(slot_key, [])
                    )
                    counts_delta = {"single": 0 if already else 1}
                else:
                    continue
                for key, value in counts_delta.items():
                    counts[key] += value

            counts["demoted"] += self._repair_demoted(data, index, lines)

            changed = counts["picks"] + counts["demoted"]
            if changed and write:
                path_ = _options_path(game_dir)
                path_.with_suffix(path_.suffix + ".bak").write_bytes(path_.read_bytes())
                data["game"] = slug
                data["updated_at"] = now
                _write_options(game_dir, data)

        head = (
            f"{slug}: {counts['picks']} pick(s), {counts['demoted']} demoted option(s), "
            f"{counts['unmatched']} unmatched, {counts['single']} single-slot"
        )
        self.stdout.write(self.style.SUCCESS(head) if changed else head)
        for line in lines[:20]:
            self.stdout.write("    " + line)
        if len(lines) > 20:
            self.stdout.write(f"    … and {len(lines) - 20} more")
        return counts

    def _recover_pool(
        self,
        data: dict,
        index: dict,
        game_dir: Path,
        slot_key: str,
        pool_dir: str,
        now: str,
        lines: list,
    ) -> dict:
        counts = {"picks": 0, "unmatched": 0}
        existing = data["picks"].get(slot_key, [])
        have = {p.get("filename") for p in existing}
        for member in _pool_members(game_dir / "videos" / pool_dir):
            if member.name in have:
                continue  # a first-hand record always beats a recovered one
            if not _POOL_STEM_RE.match(member.stem):
                # Not named by `_pool_member_stem` — a hand-dropped file. There is
                # no hash in the name, so there is nothing to prove anything with.
                counts["unmatched"] += 1
                continue
            row = index.get(member.stem)
            if row is None:
                counts["unmatched"] += 1
                continue
            existing.append(_pick_from(row, member.name, now))
            data["picks"][slot_key] = existing
            counts["picks"] += 1
            lines.append(f"{slot_key}  {member.name}  <-  {_remote_of(row)}")
        return counts

    def _repair_demoted(self, data: dict, index: dict, lines: list) -> int:
        """Write the remote url back onto UNSELECTED pool clips sitting on a shelf.

        `pool_unselect` re-shelves the file as an `origin: "previous"` option with a
        local path and nothing else — measured 276 such rows on vesper, none with a
        docid. Its filename keeps the md5 stem, so the same join applies.
        """
        repaired = 0
        for slot_key, rows in data.get("options", {}).items():
            for row in rows:
                if row.get("origin") != "previous" or row.get("source_url"):
                    continue
                match = _DEMOTED_STEM_RE.match(Path(row.get("local_path") or "").stem)
                if not match:
                    continue  # a demoted SINGLE slot: named after the slot, no hash
                source = index.get(match.group(1))
                if source is None or not _remote_of(source):
                    continue
                row["source_url"] = _remote_of(source)
                for key in ("docid", "thumb"):
                    if source.get(key) and not row.get(key):
                        row[key] = source[key]
                repaired += 1
                lines.append(f"{slot_key}  demoted  <-  {row['source_url']}")
        return repaired
