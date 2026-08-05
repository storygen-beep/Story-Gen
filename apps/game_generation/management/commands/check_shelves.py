"""Find shelves and review verdicts filed under a slot path that no longer exists.

A media slot's **shelf** (its stocked candidate options) and its **verdict**
(approve/disapprove) are both filed under the slot's declared file path — the
literal string from the TOML:

    data["options"].setdefault(file_, [])      # api/v1/media_finder.py
    reviews.get(item.get("file"), {})          # api/v1/media_review.py

A path says *where the bytes live*. A shelf answers *"what clip goes in this
beat?"* Those are different questions, and the first changes far more often. So
every edit that moves a path silently orphans both ledgers:

  * converting a slot to a pool   — "a/b_t5.webm" becomes "a/b_t5" (a folder has
    no extension). Measured live: 148 stocked options stranded on the very first
    conversion.
  * retagging a tier             — apply_retags.py rewrites _t4 -> _t5 IN THE
    TOML, and nothing re-keys the ledgers.
  * renaming or moving a slot, or any hand edit of the path.

Nothing anywhere re-keys either ledger, so the options are still on disk — just
filed under a label nobody looks up. You open the picker, see an empty shelf,
and re-run a search you did not need.

This command is the alarm. It DEFAULTS to read-only — diagnosing loudly is the
whole job — and `--repair` is the separate, deliberate step that acts on it.

A shelf is now two roots of one file: `options` (the candidates) and `queries`
(which search found each of them). They are keyed on the same slot string and a
repair moves BOTH or neither — a shelf that outlived its labels would show every
option under "older searches" with no way to tell that anything was lost.

    python manage.py check_shelves --game vesper
    python manage.py check_shelves --all

Exits 1 when any orphan is found, so it can gate a release check.
"""
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

try:
    import tomllib
except ImportError:  # py<3.11
    import tomli as tomllib

GAMES_ROOT = Path(settings.BASE_DIR) / "games"

# Media extensions, only used to compare a ledger key against a declared slot
# ignoring the extension — the resolver is extension-agnostic, so "a/b.webm" and
# "a/b.gif" name the same slot.
_MEDIA_EXTS = {
    ".mp4", ".webm", ".mov", ".m4v", ".avi", ".mkv",
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp",
}
# Tier suffix, e.g. "sex/oral_t5" -> "sex/oral". Stripped only when SUGGESTING a
# match, never when deciding whether something is an orphan.
_TIER_SUFFIXES = tuple(f"_t{n}" for n in range(9)) + ("_base",)


def _strip_ext(key: str) -> str:
    p = Path(key)
    return str(p.with_suffix("")) if p.suffix.lower() in _MEDIA_EXTS else key


def _strip_tier(key: str) -> str:
    for suf in _TIER_SUFFIXES:
        if key.endswith(suf):
            return key[: -len(suf)]
    return key


class Command(BaseCommand):
    help = "Report shelf/verdict entries whose slot path no longer exists in the TOML"

    def add_arguments(self, parser):
        parser.add_argument("--game", type=str, help="Game slug (folder under games/)")
        parser.add_argument("--all", action="store_true", help="Every game that has a ledger")
        parser.add_argument(
            "--quiet-ok", action="store_true",
            help="Print nothing for games with no orphans",
        )
        parser.add_argument(
            "--repair", action="store_true",
            help="Move each confidently-matched orphan onto its slot (backs up first)",
        )

    def handle(self, *args, **options):
        game = options.get("game")
        do_all = options.get("all")
        if not game and not do_all:
            raise CommandError("Pass --game <slug> or --all")

        if do_all:
            games = sorted(
                p.parts[-3] for p in GAMES_ROOT.glob("*/.find-media/media_options.json")
            )
            # A game can have verdicts but no shelf yet.
            games += sorted(
                p.parts[-3] for p in GAMES_ROOT.glob("*/.find-media/media_reviews.json")
                if p.parts[-3] not in games
            )
        else:
            games = [game]

        total_orphans = 0
        for slug in games:
            total_orphans += self._audit(
                slug, quiet_ok=options.get("quiet_ok"), repair=options.get("repair")
            )

        self.stdout.write("")
        if total_orphans:
            hint = "" if options.get("repair") else "  Re-run with --repair to move them."
            self.stdout.write(self.style.ERROR(
                f"{total_orphans} orphaned ledger key(s) remain. Their options/verdicts are still "
                f"on disk but unreachable — the picker opens on an empty shelf.{hint}"
            ))
            raise SystemExit(1)
        self.stdout.write(self.style.SUCCESS("No orphaned shelves or verdicts."))

    # ------------------------------------------------------------------ audit

    def _audit(self, slug: str, quiet_ok: bool = False, repair: bool = False) -> int:
        game_dir = GAMES_ROOT / slug
        if not game_dir.is_dir():
            raise CommandError(f"Game '{slug}' not found under {GAMES_ROOT}")

        declared = self._declared_slots(game_dir, slug)
        if declared is None:
            self.stdout.write(self.style.WARNING(f"{slug}: no merged TOML — skipped"))
            return 0

        # A label can span several roots of ONE file. `options` and `queries` are two
        # halves of a shelf; the first root is the primary — it is what "N options
        # stranded" counts — and the rest ride along so a repair can never separate
        # a shelf from its query labels.
        ledgers = {
            "shelf": (game_dir / ".find-media" / "media_options.json", ("options", "queries")),
            "verdict": (game_dir / ".find-media" / "media_reviews.json", ("reviews",)),
        }

        rows = []
        n_keys = 0
        for label, (path_, root_keys) in ledgers.items():
            per_root = {rk: self._read_ledger(path_, rk) for rk in root_keys}
            # UNION of keys, depth from the primary root only. Walking the roots
            # separately would report every slot once per root, doubling both the
            # orphan count and the exit-code signal. The union is also what catches a
            # queries-only orphan — a search that yielded nothing on a slot whose path
            # later moved — which reports honestly as "0 options stranded".
            entries = {
                k: per_root[root_keys[0]].get(k, [])
                for k in sorted(set().union(*(d.keys() for d in per_root.values())))
            }
            n_keys += len(entries)
            for key, value in sorted(entries.items()):
                # An orphan is an EXACT-match failure. A key whose stem matches a
                # declared slot is still an orphan — "a/b_t5.webm" and the pool
                # "a/b_t5" are different strings, so the shelf really is
                # unreachable. The stem is only used to SUGGEST the repair.
                if key in declared:
                    continue
                depth = len(value) if isinstance(value, list) else 1
                rows.append((label, key, depth, self._suggest(key, declared)))

        if not rows:
            if not quiet_ok:
                self.stdout.write(f"{slug}: {n_keys} ledger key(s), 0 orphaned")
            return 0

        self.stdout.write(self.style.WARNING(
            f"\n{slug}: {n_keys} ledger key(s), {len(rows)} ORPHANED"
        ))
        unresolved = 0
        for label, key, depth, suggestion in rows:
            unit = "options" if label == "shelf" else "verdict"
            self.stdout.write(f"  [{label:7s}] {key}")
            self.stdout.write(f"            {depth} {unit} stranded")
            if not suggestion:
                # Never invent a destination. vesper's `sex/renner_anal_t5.webm` is a
                # slot the author DELETED (the TOML says so in a comment) — moving its
                # verdict somewhere would fabricate a decision about a different beat.
                self.stdout.write("            no obvious match — slot may have been deleted")
                unresolved += 1
                continue

            self.stdout.write(self.style.SUCCESS(f"            probably meant: {suggestion}"))
            if not repair:
                unresolved += 1
                continue

            path_, root_keys = ledgers[label]
            moved, why = self._move_key(path_, root_keys, key, suggestion)
            if moved:
                self.stdout.write(self.style.SUCCESS(f"            MOVED -> {suggestion}"))
            else:
                self.stdout.write(self.style.ERROR(f"            NOT moved: {why}"))
                unresolved += 1
        return unresolved

    @staticmethod
    def _move_key(path_: Path, root_keys: tuple, old: str, new: str):
        """Re-file one SLOT across every root of a ledger. Returns (moved, reason).

        A slot, not a root key: `media_options.json` holds a shelf's candidates and
        the searches that produced them under two roots keyed on the same string, and
        moving one without the other is worse than moving neither.

        Backs the ledger up beside itself first — these files are the only record of a
        shelf, and a bad merge is unrecoverable otherwise. Locked and atomic, because
        the dev server may be writing this same file: the old truncate-then-write could
        strand a torn 2.9 MB ledger, which `_read_options` then reads back as EMPTY.
        """
        import json

        from apps.common.json_ledger import ledger_lock, write_json_atomic

        with ledger_lock(path_):
            try:
                raw = path_.read_text()
                data = json.loads(raw)
            except Exception as exc:  # noqa: BLE001
                return False, f"unreadable ({type(exc).__name__})"

            present = [rk for rk in root_keys
                       if isinstance(data.get(rk), dict) and old in data[rk]]
            if not present:
                return False, "key vanished between audit and repair"
            # Refuse across ALL roots, not just the ones holding `old`. A slot can
            # legitimately have `queries[new]` (a zero-yield search recorded against
            # the new key) while `options[new]` is absent; checking only the root
            # being moved would silently clobber it.
            for rk in root_keys:
                if isinstance(data.get(rk), dict) and new in data[rk]:
                    # Merging two shelves would mix two beats' candidates, and merging
                    # two verdicts would pick one arbitrarily. Refuse; a human decides.
                    return False, f"'{new}' already exists in {rk} — refusing to merge"

            # Back up from the bytes we actually read, so the .bak provably matches the
            # state being mutated rather than whatever a concurrent writer left behind.
            path_.with_suffix(path_.suffix + ".bak").write_text(raw)
            for rk in present:
                data[rk][new] = data[rk].pop(old)
            # Never invent a root: a legacy ledger with no `queries` key must not gain
            # one from an operation that was only asked to re-key a slot.
            write_json_atomic(path_, data)
            return True, ""

    # ------------------------------------------------------------- collectors

    def _declared_slots(self, game_dir: Path, slug: str):
        """Every slot key the real enumerator would produce, or None if no TOML.

        Deliberately calls `_extract_missing_media` — the SAME function the
        game-review API and the review UI use — rather than re-walking the TOML
        here. A second walk is exactly how the enumerators drifted apart before
        (see apps/common/media_blocks.py), and an audit that disagrees with the
        thing it audits is worse than no audit.
        """
        tomls = sorted(game_dir.glob("toml_phases/*_final_game.toml"))
        if not tomls:
            return None

        from api.v1 import game_review

        with open(tomls[-1], "rb") as fh:
            data = tomllib.load(fh)

        original_root = game_review.GAMES_ROOT
        try:
            game_review.GAMES_ROOT = GAMES_ROOT
            media = game_review._extract_missing_media(data, slug)
        finally:
            game_review.GAMES_ROOT = original_root

        return {e["file"] for e in media["found"] + media["missing"] if e.get("file")}

    @staticmethod
    def _read_ledger(path_: Path, root_key: str) -> dict:
        if not path_.is_file():
            return {}
        try:
            import json
            data = json.loads(path_.read_text())
        except Exception:
            return {}
        got = data.get(root_key)
        return got if isinstance(got, dict) else {}

    @staticmethod
    def _suggest(orphan: str, declared) -> str:
        """The declared slot this orphan most likely belongs to.

        Two rules, matching the two ways a path actually moves:
          * extension-stripped  -> catches pool conversion ("a/b_t5.webm" vs "a/b_t5")
          * tier-stripped too   -> catches a retag ("a/b_t4" vs "a/b_t5")
        """
        want_ext = _strip_ext(orphan)
        for slot in sorted(declared):
            if _strip_ext(slot) == want_ext:
                return slot
        want_tier = _strip_tier(want_ext)
        for slot in sorted(declared):
            if _strip_tier(_strip_ext(slot)) == want_tier:
                return slot
        return ""
