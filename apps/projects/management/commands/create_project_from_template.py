"""Create a new Project from a TOML template.

Usage:
  python manage.py create_project_from_template \
      --file /path/to/game.toml \
      --owner-id <UUID> \
      [--name "Override Title"] \
      [--dry-run]
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand, CommandError

from apps.projects.services.template_import import (
    parse_toml,
    normalize,
    validate,
    create_project_from_template,
)


class Command(BaseCommand):
    help = "Create a new project (and related entities) from a single TOML template"

    def add_arguments(self, parser):
        parser.add_argument("--file", required=True, help="Path to game.toml template")
        parser.add_argument("--owner-id", required=True, help="Owner user UUID")
        parser.add_argument("--name", required=False, help="Override project title")
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse + validate only; no database writes",
        )

    def handle(self, *args, **options):
        file_path = options["file"]
        owner_id = options["owner_id"]
        name_override = options.get("name")
        dry_run = bool(options.get("dry_run"))

        path = Path(file_path)
        if not path.exists():
            raise CommandError(f"Template file not found: {file_path}")

        try:
            raw = parse_toml(str(path))
        except Exception as e:
            raise CommandError(f"Failed to read TOML: {e}")

        template = normalize(raw)
        errors = validate(template)

        # Strict rule: any trait referenced in trigger conditions or choice effects
        # must be declared in the corresponding character's core_traits
        errors.extend(self._validate_trait_declarations(template))
        if errors:
            payload: dict[str, Any] = {
                "valid": False,
                "errors": errors,
            }
            self.stdout.write(json.dumps(payload, indent=2))
            raise CommandError("Template validation failed")

        if dry_run:
            stats = {
                "npcs": len(template.npcs),
                "locations": len(template.locations),
                "canvases": len(getattr(template, "canvases", [])),
                "nodes": sum(len(c.nodes) for c in getattr(template, "canvases", [])),
            }
            payload = {
                "valid": True,
                "schema_version": template.schema_version,
                "project_title": template.project.title,
                "starting_canvas_slug": getattr(template, "starting_canvas", None),
                "stats": stats,
            }
            self.stdout.write(json.dumps(payload, indent=2))
            return

        try:
            result = create_project_from_template(
                template=template, owner_id=owner_id, name_override=name_override
            )
        except Exception as e:
            raise CommandError(f"Creation failed: {e}")

        self.stdout.write(json.dumps(result, indent=2))

    def _validate_trait_declarations(self, template) -> list[str]:
        """Ensure all traits used in conditions/effects are declared on Player/NPC core_traits.

        This mirrors the UI behavior where trait pickers are sourced from declared keys.
        """
        errors: list[str] = []

        # Collect declared traits
        player_traits = set((getattr(template.player, "core_traits", {}) or {}).keys())
        npc_traits_map = {n.id: set((n.core_traits or {}).keys()) for n in (template.npcs or [])}

        def check_trait(subject: str, trait_key: str | None, npc_id: str | None, context: str):
            if not trait_key:
                errors.append(f"{context}: trait_key is required but missing")
                return
            if subject == "player":
                if trait_key not in player_traits:
                    errors.append(f"{context}: trait '{trait_key}' not declared in player.core_traits")
            elif subject == "npc":
                if not npc_id:
                    errors.append(f"{context}: character_id required for NPC trait condition/effect")
                    return
                if npc_id not in npc_traits_map:
                    errors.append(f"{context}: npc id '{npc_id}' not found among declared NPCs")
                    return
                if trait_key not in npc_traits_map[npc_id]:
                    errors.append(f"{context}: trait '{trait_key}' not declared in NPC '{npc_id}'.core_traits")

        # Scan canvases
        for ci, c in enumerate(getattr(template, "canvases", []) or []):
            # Trigger conditions
            trig = getattr(c, "trigger", None)
            if trig and isinstance(trig.conditions, dict):
                items = (trig.conditions or {}).get("items", []) or []
                for ii, it in enumerate(items):
                    if not isinstance(it, dict):
                        continue
                    if it.get("type") == "trait":
                        subject = it.get("subject")
                        trait_key = it.get("trait_key")
                        npc_id = it.get("character_id") if subject == "npc" else None
                        check_trait(subject, trait_key, npc_id, f"canvases[{ci}].trigger.conditions.items[{ii}]")

            # Node choice effects
            for ni, n in enumerate(getattr(c, "nodes", []) or []):
                eb = getattr(n, "exit_block", None)
                if not eb or getattr(eb, "type", "location") != "choices":
                    continue
                for chi, ch in enumerate(getattr(eb, "choices", []) or []):
                    for ei, eff in enumerate(getattr(ch, "effects", []) or []):
                        # eff is TemplateChoiceEffect
                        subject = getattr(eff, "targetType", "player")
                        trait_key = getattr(eff, "trait", None)
                        npc_id = getattr(eff, "npcId", None) if subject == "npc" else None
                        check_trait(subject, trait_key, npc_id, f"canvases[{ci}].nodes[{ni}].choices[{chi}].effects[{ei}]")

        return errors
