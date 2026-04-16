"""Backfill StoryNode BlockNote metadata and sanitize blocks.

Usage:
  python manage.py backfill_storynode_blocknote [--project-id <UUID>] [--dry-run]

What it does:
  - Finds StoryNode rows where node_data has `blocks` but version is missing or not "2.0".
  - Sets `version` to "2.0" and adds a preview `content` if missing.
  - Sanitizes blocks (ensures ids present) and defaults heading level to 1 when missing.
"""

from __future__ import annotations

import json
from typing import Any

from django.core.management.base import BaseCommand

from apps.stories.models import StoryNode
from apps.stories.services.block_conversion import BlockConversionService


class Command(BaseCommand):
    help = "Backfill StoryNode BlockNote version and sanitize blocks"

    def add_arguments(self, parser):
        parser.add_argument(
            "--project-id",
            dest="project_id",
            help="Optional Project UUID to limit scope",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would change without saving",
        )

    def handle(self, *args, **options):
        project_id = options.get("project_id")
        dry_run = bool(options.get("dry_run"))

        qs = StoryNode.objects.all()
        if project_id:
            qs = qs.filter(canvas__project_id=project_id)

        # Only nodes that have blocks but are not flagged as v2.0
        # (MariaDB/Postgres JSON contains key filter may differ; keep Python-side filter for portability)
        nodes = [n for n in qs if isinstance(n.node_data, dict) and "blocks" in (n.node_data or {})]

        updated = 0
        examined = 0
        changes_preview: list[dict[str, Any]] = []

        for node in nodes:
            examined += 1
            data = node.node_data or {}
            blocks = data.get("blocks", [])

            needs_version = data.get("version") != BlockConversionService.DEFAULT_VERSION
            # Sanitize blocks and ensure heading level default
            sanitized = BlockConversionService._sanitize_blocks(blocks)  # type: ignore[attr-defined]
            fixed = []
            changed_local = False
            for b in sanitized:
                if b.get("type") == "heading":
                    props = b.get("props") or {}
                    if not props.get("level"):
                        props["level"] = 1
                        b["props"] = props
                        changed_local = True
                fixed.append(b)

            needs_blocks_fix = fixed != blocks
            needs_content = "content" not in data

            if not (needs_version or needs_blocks_fix or needs_content):
                continue

            preview = BlockConversionService.get_preview_text(fixed) if needs_content else data.get("content", "")

            changes_preview.append(
                {
                    "node_id": str(node.id),
                    "name": node.name,
                    "needs_version": needs_version,
                    "needs_blocks_fix": needs_blocks_fix,
                    "needs_content": needs_content,
                }
            )

            if not dry_run:
                data["version"] = BlockConversionService.DEFAULT_VERSION
                data["blocks"] = fixed
                if needs_content:
                    data["content"] = preview
                node.node_data = data
                node.save(update_fields=["node_data"])
            updated += 1

        payload = {
            "examined": examined,
            "updated": updated,
            "dry_run": dry_run,
            "project_id": str(project_id) if project_id else None,
            "changes": changes_preview[:50],  # cap preview
        }
        self.stdout.write(json.dumps(payload, indent=2))

