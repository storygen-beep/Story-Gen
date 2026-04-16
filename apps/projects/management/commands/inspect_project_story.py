"""Inspect a project's story setup: starting canvas, canvases, nodes.

Usage:
  python manage.py inspect_project_story --project-id <UUID>
"""

from __future__ import annotations

import json
from typing import Any

from django.core.management.base import BaseCommand, CommandError

from apps.projects.models import Project
from apps.stories.models import StoryCanvas, StoryNode


class Command(BaseCommand):
    help = "Print story details for a project: starting canvas, canvases, and nodes"

    def add_arguments(self, parser):
        parser.add_argument("--project-id", required=True, help="Project UUID")

    def handle(self, *args, **options):
        pid = options["project_id"]
        try:
            project = Project.objects.get(id=pid)
        except Project.DoesNotExist:
            raise CommandError(f"Project not found: {pid}")

        data: dict[str, Any] = {
            "project_id": str(project.id),
            "project_name": project.name,
            "starting_canvas": None,
            "canvases": [],
        }

        sc = project.starting_canvas
        if sc:
            nodes_qs = StoryNode.objects.filter(canvas=sc).order_by("created_at")
            data["starting_canvas"] = {
                "id": str(sc.id),
                "name": sc.name,
                "metadata_slug": (sc.metadata or {}).get("slug"),
                "node_count": nodes_qs.count(),
                "node_names": [n.name for n in nodes_qs],
            }

        # list all canvases for the project
        canvases = StoryCanvas.objects.filter(project=project).order_by("created_at")
        for c in canvases:
            data["canvases"].append(
                {
                    "id": str(c.id),
                    "name": c.name,
                    "metadata_slug": (c.metadata or {}).get("slug"),
                    "nodes": [n.name for n in StoryNode.objects.filter(canvas=c).order_by("created_at")],
                }
            )

        self.stdout.write(json.dumps(data, indent=2))

