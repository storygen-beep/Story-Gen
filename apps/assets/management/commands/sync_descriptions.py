"""Sync description symlinks for a game's video collections.

Creates a descriptions/ folder at each collection level with symlinks
pointing to the descriptions.json files inside individual clip folders.

Usage:
    python manage.py sync_descriptions jacks_world
    python manage.py sync_descriptions jacks_world --collection angela_white
    python manage.py sync_descriptions jacks_world --dry-run
    python manage.py sync_descriptions jacks_world --clean
"""

from __future__ import annotations

import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

GAMES_ROOT = Path(settings.BASE_DIR) / "games"


class Command(BaseCommand):
    help = "Create symlinks in videos/<collection>/descriptions/ for each clip folder's descriptions.json"

    def add_arguments(self, parser):
        parser.add_argument(
            "game",
            type=str,
            help="Game directory name (e.g. jacks_world)",
        )
        parser.add_argument(
            "--collection",
            type=str,
            help="Limit to a single collection (e.g. angela_white)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would happen without creating anything",
        )
        parser.add_argument(
            "--clean",
            action="store_true",
            help="Also remove broken symlinks in descriptions/ folders",
        )

    def handle(self, *args, **options):
        game: str = options["game"]
        collection_filter: str | None = options.get("collection")
        dry_run: bool = options["dry_run"]
        clean: bool = options["clean"]

        videos_dir = GAMES_ROOT / game / "videos"
        if not videos_dir.is_dir():
            raise CommandError(f"Videos directory not found: {videos_dir}")

        # Gather collection dirs
        if collection_filter:
            collection_dirs = [videos_dir / collection_filter]
            if not collection_dirs[0].is_dir():
                raise CommandError(f"Collection not found: {collection_dirs[0]}")
        else:
            collection_dirs = sorted(
                p for p in videos_dir.iterdir() if p.is_dir()
            )

        created = 0
        skipped = 0
        replaced = 0
        cleaned = 0

        for coll_dir in collection_dirs:
            clips_dir = coll_dir / "clips"
            if not clips_dir.is_dir():
                continue

            desc_dir = coll_dir / "descriptions"

            # Find all clip folders with descriptions.json
            desc_files = sorted(clips_dir.glob("*/descriptions.json"))
            if not desc_files and not clean:
                continue

            if not dry_run and desc_files:
                desc_dir.mkdir(exist_ok=True)

            for desc_file in desc_files:
                video_stem = desc_file.parent.name
                link_path = desc_dir / f"{video_stem}.json"
                target = Path("..") / "clips" / video_stem / "descriptions.json"

                if link_path.is_symlink():
                    existing_target = os.readlink(link_path)
                    if existing_target == str(target):
                        skipped += 1
                        continue
                    # Stale symlink — replace
                    if not dry_run:
                        link_path.unlink()
                    replaced += 1
                elif link_path.exists():
                    # Regular file in the way — skip with warning
                    self.stderr.write(
                        self.style.WARNING(f"  Skipping (not a symlink): {link_path}")
                    )
                    continue

                if not dry_run:
                    link_path.symlink_to(target)
                created += 1
                self.stdout.write(f"  {link_path.name}  ->  {target}")

            # Clean broken symlinks
            if clean and desc_dir.is_dir():
                for link in desc_dir.iterdir():
                    if link.is_symlink() and not link.resolve().exists():
                        self.stdout.write(
                            self.style.WARNING(f"  Removing broken: {link.name}")
                        )
                        if not dry_run:
                            link.unlink()
                        cleaned += 1

        # Summary
        prefix = "[DRY RUN] " if dry_run else ""
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"{prefix}Done: {created} created, {replaced} replaced, "
                f"{skipped} up-to-date, {cleaned} cleaned"
            )
        )
