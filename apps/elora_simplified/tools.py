"""
Elora Agent Tools for story canvas and world interaction.

These tools provide read/write operations for the agent to interact with
the story system. Focus on open world novel creation, not game generation.
"""

import logging
import uuid
from typing import Any, Optional

from django.db import transaction

from apps.projects.models import Project
from apps.stories.models import CanvasTrigger, StoryCanvas, StoryNode
from apps.world.models import Location

logger = logging.getLogger(__name__)


class StoryTools:
    """Tools for reading and writing story canvas data."""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.project = None
        self._load_project()

    def _load_project(self):
        """Load and cache project instance."""
        try:
            self.project = Project.objects.get(id=self.project_id, deleted_at__isnull=True)
        except Project.DoesNotExist:
            raise ValueError(f"Project {self.project_id} not found")

    def read_canvas_summary(self) -> dict[str, Any]:
        """
        Get high-level summary of all story canvases in project.

        Returns:
            Dict with canvas list, counts, and basic structure info
        """
        canvases = StoryCanvas.objects.filter(
            project=self.project,
            deleted_at__isnull=True
        ).prefetch_related('nodes')

        canvas_list = []
        for canvas in canvases:
            node_count = canvas.nodes.count()
            # Check for trigger without prefetching to avoid serialization issues
            trigger_location = None
            has_trigger = False

            try:
                from apps.stories.models import CanvasTrigger
                trigger = CanvasTrigger.objects.select_related('location').filter(canvas=canvas).first()
                if trigger:
                    has_trigger = True
                    trigger_location = trigger.location.name if trigger.location else None
            except Exception:
                pass

            canvas_list.append({
                "id": str(canvas.id),
                "name": canvas.name,
                "description": canvas.description,
                "canvas_type": canvas.canvas_type,
                "status": canvas.status,
                "node_count": node_count,
                "has_trigger": has_trigger,
                "trigger_location": trigger_location,
                "created_at": canvas.created_at.isoformat(),
            })

        return {
            "project_name": self.project.name,
            "project_id": str(self.project.id),
            "canvas_count": len(canvas_list),
            "canvases": canvas_list,
            "starting_canvas": str(self.project.starting_canvas.id) if self.project.starting_canvas else None,
        }

    def read_canvas_detail(self, canvas_id: str) -> dict[str, Any]:
        """
        Get detailed information about a specific canvas.

        Args:
            canvas_id: UUID of the canvas

        Returns:
            Detailed canvas information including nodes
        """
        try:
            canvas = StoryCanvas.objects.get(
                id=canvas_id,
                project=self.project,
                deleted_at__isnull=True
            )
        except StoryCanvas.DoesNotExist:
            raise ValueError(f"Canvas {canvas_id} not found in project")

        # Get nodes (ordered by creation time due to single-node limitation)
        nodes = canvas.nodes.all().order_by('created_at')
        node_list = []

        for node in nodes:
            # Extract content from BlockNote format
            content_text = ""
            if node.node_data and isinstance(node.node_data, dict):
                blocks = node.node_data.get('blocks', [])
                content_parts = []
                for block in blocks:
                    content = block.get('content', '').strip()
                    if content:
                        content_parts.append(content)
                content_text = ' '.join(content_parts)

            node_list.append({
                "id": str(node.id),
                "name": node.name,
                "content": content_text,
                "exit_block": node.exit_block,
                "tags": node.tags,
                "created_at": node.created_at.isoformat(),
            })

        # Get trigger info if exists
        trigger_info = None
        if hasattr(canvas, 'trigger') and canvas.trigger:
            trigger_location = None
            if canvas.trigger.location_id:
                try:
                    location = Location.objects.get(id=canvas.trigger.location_id)
                    trigger_location = {
                        "id": str(location.id),
                        "name": location.name,
                        "description": location.description,
                    }
                except Location.DoesNotExist:
                    pass

            trigger_info = {
                "location": trigger_location,
                "is_active": canvas.trigger.is_active,
                "is_activity": canvas.trigger.is_activity,
                "is_repeatable": canvas.trigger.is_repeatable,
                "conditions": canvas.trigger.conditions,
            }

        return {
            "id": str(canvas.id),
            "name": canvas.name,
            "description": canvas.description,
            "canvas_type": canvas.canvas_type,
            "status": canvas.status,
            "metadata": canvas.metadata,
            "tags": canvas.tags,
            "nodes": node_list,
            "trigger": trigger_info,
            "created_at": canvas.created_at.isoformat(),
            "updated_at": canvas.updated_at.isoformat(),
        }

    def create_canvas(self, name: str, description: str = "", canvas_type: str = "story",
                     location_id: str = None) -> dict[str, Any]:
        """
        Create a new story canvas.

        Args:
            name: Canvas name
            description: Canvas description
            canvas_type: Type of canvas (story, intro, dialogue, tutorial)
            location_id: Optional location ID for trigger

        Returns:
            Created canvas information
        """
        with transaction.atomic():
            # Create canvas
            canvas = StoryCanvas.objects.create(
                project=self.project,
                name=name,
                description=description,
                canvas_type=canvas_type,
                created_by_id=None,  # TODO: Get from session context
                updated_by_id=None,
            )

            # Create trigger if location_id provided
            if location_id:
                try:
                    # Verify location exists in project
                    location = Location.objects.get(id=location_id, project=self.project)
                    CanvasTrigger.objects.create(
                        canvas=canvas,
                        location_id=location_id,
                        is_active=True,
                        created_by_id=None,  # TODO: Get from session context
                        updated_by_id=None,
                    )
                except Location.DoesNotExist:
                    logger.warning(f"Location {location_id} not found, creating canvas without trigger")

        return {
            "id": str(canvas.id),
            "name": canvas.name,
            "description": canvas.description,
            "canvas_type": canvas.canvas_type,
            "status": canvas.status,
            "created_at": canvas.created_at.isoformat(),
            "trigger_location_id": location_id if location_id else None,
        }

    def update_canvas_content(self, canvas_id: str, updates: dict[str, Any]) -> dict[str, Any]:
        """
        Update canvas basic information (name, description, etc.).

        Args:
            canvas_id: Canvas UUID
            updates: Dictionary of fields to update

        Returns:
            Updated canvas information
        """
        try:
            canvas = StoryCanvas.objects.get(
                id=canvas_id,
                project=self.project,
                deleted_at__isnull=True
            )
        except StoryCanvas.DoesNotExist:
            raise ValueError(f"Canvas {canvas_id} not found")

        # Update allowed fields
        allowed_fields = ['name', 'description', 'canvas_type', 'status', 'tags']
        updated_fields = []

        for field, value in updates.items():
            if field in allowed_fields and hasattr(canvas, field):
                setattr(canvas, field, value)
                updated_fields.append(field)

        canvas.save()

        return {
            "id": str(canvas.id),
            "name": canvas.name,
            "description": canvas.description,
            "updated_fields": updated_fields,
            "updated_at": canvas.updated_at.isoformat(),
        }

    def create_node_content(self, canvas_id: str, name: str, content_blocks: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Create a new node with content (single node per canvas for now).

        Args:
            canvas_id: Canvas UUID
            name: Node name
            content_blocks: BlockNote format blocks

        Returns:
            Created node information
        """
        try:
            canvas = StoryCanvas.objects.get(
                id=canvas_id,
                project=self.project,
                deleted_at__isnull=True
            )
        except StoryCanvas.DoesNotExist:
            raise ValueError(f"Canvas {canvas_id} not found")

        # Check single-node limitation
        if canvas.nodes.exists():
            raise ValueError("Canvas already has a node (single-node limitation)")

        # Create node with BlockNote content (ensure proper format)
        preview_text = "\n".join(
            [
                str(b.get("content", "")).strip()
                for b in (content_blocks or [])
                if str(b.get("content", "")).strip()
            ]
        )
        node_data = {
            "blocks": content_blocks or [],
            "version": "2.0",
            "content": preview_text,
        }

        node = StoryNode.objects.create(
            canvas=canvas,
            name=name,
            node_data=node_data,
        )

        return {
            "id": str(node.id),
            "canvas_id": str(canvas.id),
            "name": node.name,
            "content_blocks": content_blocks,
            "created_at": node.created_at.isoformat(),
        }

    def update_node_content(self, node_id: str, updates: dict[str, Any]) -> dict[str, Any]:
        """
        Update node content and properties.

        Args:
            node_id: Node UUID
            updates: Dictionary with 'name', 'content_blocks', 'exit_block'

        Returns:
            Updated node information
        """
        try:
            node = StoryNode.objects.get(id=node_id, canvas__project=self.project)
        except StoryNode.DoesNotExist:
            raise ValueError(f"Node {node_id} not found in project")

        updated_fields = []

        # Update name
        if 'name' in updates:
            node.name = updates['name']
            updated_fields.append('name')

        # Update content blocks
        if 'content_blocks' in updates:
            content_blocks = updates['content_blocks'] or []
            preview_text = "\n".join(
                [
                    str(b.get("content", "")).strip()
                    for b in content_blocks
                    if str(b.get("content", "")).strip()
                ]
            )
            node.node_data = {
                "blocks": content_blocks,
                "version": "2.0",
                "content": preview_text,
            }
            updated_fields.append('content_blocks')

        # Update exit block
        if 'exit_block' in updates:
            node.exit_block = updates['exit_block']
            updated_fields.append('exit_block')

        node.save()

        return {
            "id": str(node.id),
            "name": node.name,
            "updated_fields": updated_fields,
            "updated_at": node.updated_at.isoformat(),
        }

    def find_canvas(self, query: str) -> dict[str, Any]:
        """
        Find canvas using entity-aware search with disambiguation.

        This method uses the entity search system to find canvases,
        enabling fuzzy matching and conversational disambiguation.

        Args:
            query: Canvas name or description to search for

        Returns:
            Search result with disambiguation if needed
        """
        from .services.entity_service import EntityService

        entity_service = EntityService(self.project_id)
        result = entity_service.search(query, entity_types=["canvas"], fuzzy_match=True)

        if result["type"] == "single_match":
            # Found exact match - return detailed canvas info
            entity = result["entity"]
            canvas_id = entity["entity_id"]
            try:
                return self.read_canvas_detail(canvas_id)
            except ValueError:
                return {"error": f"Canvas entity {canvas_id} exists but canvas not found in database"}

        elif result["type"] == "disambiguation":
            # Multiple matches - return disambiguation choices
            return {
                "type": "disambiguation",
                "query": query,
                "message": f"Multiple canvases match '{query}'. Please choose:",
                "choices": result["matches"]
            }

        else:
            # No matches - return suggestions
            return {
                "type": "no_match",
                "query": query,
                "message": f"No canvases found matching '{query}'",
                "suggestions": result.get("suggestions", [])
            }


class WorldTools:
    """Tools for reading world/location data."""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.project = None
        self._load_project()

    def _load_project(self):
        """Load and cache project instance."""
        try:
            self.project = Project.objects.get(id=self.project_id, deleted_at__isnull=True)
        except Project.DoesNotExist:
            raise ValueError(f"Project {self.project_id} not found")

    def read_locations_summary(self) -> dict[str, Any]:
        """
        Get summary of all locations in project.

        Returns:
            Dict with location list and basic info
        """
        locations = Location.objects.filter(project=self.project).order_by('created_at')

        location_list = []
        for location in locations:
            location_list.append({
                "id": str(location.id),
                "name": location.name,
                "description": location.description,
                "location_type": location.location_type,
                "is_starting_location": location.is_starting_location,
                "is_accessible": location.is_accessible,
                "created_at": location.created_at.isoformat(),
            })

        return {
            "project_name": self.project.name,
            "location_count": len(location_list),
            "locations": location_list,
        }

    def read_location_detail(self, location_id: str) -> dict[str, Any]:
        """
        Get detailed information about a specific location.

        Args:
            location_id: UUID of location

        Returns:
            Detailed location information
        """
        try:
            location = Location.objects.get(id=location_id, project=self.project)
        except Location.DoesNotExist:
            raise ValueError(f"Location {location_id} not found in project")

        # Get story canvases triggered at this location
        triggered_canvases = []
        canvas_triggers = CanvasTrigger.objects.filter(
            location_id=location_id,
            canvas__project=self.project,
            canvas__deleted_at__isnull=True
        ).select_related('canvas')

        for trigger in canvas_triggers:
            triggered_canvases.append({
                "canvas_id": str(trigger.canvas.id),
                "canvas_name": trigger.canvas.name,
                "is_active": trigger.is_active,
                "is_activity": trigger.is_activity,
            })

        return {
            "id": str(location.id),
            "name": location.name,
            "description": location.description,
            "location_type": location.location_type,
            "properties": location.properties,
            "is_starting_location": location.is_starting_location,
            "is_accessible": location.is_accessible,
            "triggered_canvases": triggered_canvases,
            "created_at": location.created_at.isoformat(),
        }


# Entity/Edge Tools (Simple, Atomic Interface)


class EntityTools:
    """
    Simple, atomic tools for entity operations.

    Following GPT-5's "lego bricks" pattern - keeps tools simple and dumb,
    with all intelligence in the EntityService layer.
    """

    def __init__(self, project_id: str):
        self.project_id = project_id
        from .services.entity_service import EntityService
        self.entity_service = EntityService(project_id)

    def search(self, query: str, entity_types: list[str] = None,
               fuzzy_match: bool = True, limit: int = 10) -> dict[str, Any]:
        """
        Search entities with simple parameters.

        Args:
            query: Search text
            entity_types: Optional entity types to filter by
            fuzzy_match: Enable fuzzy matching
            limit: Maximum results

        Returns:
            Service result with type indication for disambiguation
        """
        return self.entity_service.search(
            query=query,
            entity_types=entity_types,
            fuzzy_match=fuzzy_match,
            limit=limit
        )

    def get_by_id(self, entity_id: str) -> Optional[dict[str, Any]]:
        """Get entity details by ID."""
        return self.entity_service.get_by_id(entity_id)

    def get_by_slug(self, slug: str, entity_type: str = None) -> Optional[dict[str, Any]]:
        """Get entity by URL-friendly slug."""
        return self.entity_service.get_by_slug(slug, entity_type)

    def get_counts(self, entity_types: list[str] = None) -> dict[str, int]:
        """Get entity counts by type."""
        return self.entity_service.get_counts(entity_types)

    def list_by_type(self, entity_type: str, limit: int = 20) -> list[dict[str, Any]]:
        """List entities of specific type."""
        return self.entity_service.list_by_type(entity_type, limit)


class EdgeTools:
    """
    Simple, atomic tools for relationship operations.

    Enables cross-entity queries like "canvases that use Kitchen location"
    through simple relationship traversal methods.
    """

    def __init__(self, project_id: str):
        self.project_id = project_id
        from .services.edge_service import EdgeService
        self.edge_service = EdgeService(project_id)

    def out(self, subject_ids: list[str], predicate: str,
            object_types: list[str] = None, limit: int = 50) -> list[dict[str, Any]]:
        """
        Get outgoing relationships: subject -> predicate -> object

        Example: canvas_ids -> "USES_LOCATION" -> location entities
        """
        return self.edge_service.out(subject_ids, predicate, object_types, limit)

    def in_(self, object_ids: list[str], predicate: str,
            subject_types: list[str] = None, limit: int = 50) -> list[dict[str, Any]]:
        """
        Get incoming relationships: subject <- predicate <- object

        Example: location_ids <- "USES_LOCATION" <- canvas entities
        """
        return self.edge_service.in_(object_ids, predicate, subject_types, limit)

    def get_relationships(self, entity_id: str) -> dict[str, int]:
        """Get relationship counts for an entity."""
        return self.edge_service.get_relationship_counts(entity_id)

    def traverse(self, start_ids: list[str], path: list[tuple],
                limit: int = 20) -> list[dict[str, Any]]:
        """
        Multi-hop relationship traversal.

        Args:
            start_ids: Starting entity IDs
            path: List of (predicate, target_types) tuples
            limit: Maximum results
        """
        return self.edge_service.traverse(start_ids, path, limit)

    def find_paths(self, source_id: str, target_id: str,
                  max_hops: int = 3) -> list[list[dict[str, Any]]]:
        """Find relationship paths between entities."""
        return self.edge_service.find_paths(source_id, target_id, max_hops)

    def get_predicate_stats(self) -> dict[str, int]:
        """Get statistics on relationship types used."""
        return self.edge_service.get_predicate_stats()


# Adapter Tools (Canvas-Specific Operations)


class CanvasAdapterTools:
    """
    Tools for Canvas adapter operations and entity synchronization.

    Provides simple interface for keeping StoryCanvas objects synchronized
    with Entity/Edge records.
    """

    def __init__(self, project_id: str):
        self.project_id = project_id
        from .adapters.canvas_adapter import CanvasAdapter
        self.canvas_adapter = CanvasAdapter(project_id)

    def sync_canvas(self, canvas_id: str, force_update: bool = False) -> dict[str, Any]:
        """
        Sync single canvas to Entity record.

        Args:
            canvas_id: UUID of canvas to sync
            force_update: Force update even if unchanged

        Returns:
            Sync result with entity and relationship data
        """
        from apps.stories.models import StoryCanvas

        try:
            canvas = StoryCanvas.objects.get(
                id=canvas_id,
                project_id=self.project_id,
                deleted_at__isnull=True
            )
            return self.canvas_adapter.full_sync(canvas)
        except StoryCanvas.DoesNotExist:
            return {"error": f"Canvas {canvas_id} not found"}

    def sync_all_canvases(self, force_update: bool = False) -> dict[str, Any]:
        """
        Sync all canvases in project to Entity records.

        Args:
            force_update: Force update all canvases

        Returns:
            Sync statistics
        """
        return self.canvas_adapter.sync_all_canvases(force_update)

    def get_canvas_entity(self, canvas_name: str) -> Optional[dict[str, Any]]:
        """
        Get Entity record for canvas by name.

        Args:
            canvas_name: Name of canvas to find

        Returns:
            Entity dictionary or None if not found
        """
        from .services.entity_service import EntityService
        entity_service = EntityService(self.project_id)

        result = entity_service.search(canvas_name, entity_types=["canvas"], fuzzy_match=False)

        if result["type"] == "single_match":
            return result["entity"]
        return None
