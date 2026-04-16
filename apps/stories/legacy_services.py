"""
Story Canvas service layer.

Provides business logic for story canvas operations including CRUD, validation,
canvas management, node/connection operations, and template generation.

Note: This service layer handles canvas_settings and generation_settings fields
by storing them in the metadata field, following the pattern established by
the StoryCanvasCreateSerializer to maintain compatibility with frontend requests.
"""

from typing import Any, Optional

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone

from apps.projects.models import Project

from .models import (
    CanvasStatus,
    CanvasTrigger,
    CanvasType,
    NodeConnection,
    StoryCanvas,
    StoryNode,
)

User = get_user_model()


class StoryCanvasService:
    """Service layer for story canvas management operations."""

    @staticmethod
    def get_canvas_overview(
        project: Project,
        status_filter: Optional[str] = None,
        canvas_type_filter: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        """
        Get comprehensive canvas overview for a project.

        Args:
            project: Project instance
            status_filter: Optional status filter
            canvas_type_filter: Optional canvas type filter
            limit: Maximum number of canvases to return
            offset: Number of canvases to skip

        Returns:
            Dictionary containing canvases and pagination info
        """
        # Build query
        queryset = StoryCanvas.objects.filter(
            project=project, deleted_at__isnull=True
        ).select_related("project")

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if canvas_type_filter:
            queryset = queryset.filter(canvas_type=canvas_type_filter)

        # Get total count for pagination
        total_count = queryset.count()

        # Apply pagination and ordering
        canvases = queryset.order_by("display_order", "-updated_at")[
            offset : offset + limit
        ]

        # Convert to dictionary format
        canvas_list = []
        for canvas in canvases:
            canvas_dict = canvas.to_dict()
            canvas_list.append(canvas_dict)

        return {
            "canvases": canvas_list,
            "pagination": {
                "total": total_count,
                "offset": offset,
                "limit": limit,
                "has_more": offset + len(canvas_list) < total_count,
            },
            "starting_canvas_info": {
                "has_starting_canvas": project.starting_canvas is not None,
                "starting_canvas_id": (
                    str(project.starting_canvas.id) if project.starting_canvas else None
                ),
                "starting_canvas_name": (
                    project.starting_canvas.name if project.starting_canvas else None
                ),
            },
            "available_statuses": [choice[0] for choice in CanvasStatus.choices],
            "canvas_limits": {
                "max_canvases_per_project": 20,
                "max_nodes_per_canvas": 200,
            },
        }

    @staticmethod
    def get_intro_canvas(
        project: Project, include_trigger: bool = True, include_validation: bool = True
    ) -> dict[str, Any]:
        """
        Get the project's intro canvas with optional trigger and validation info.

        Args:
            project: Project instance
            include_trigger: Include trigger/starting location info
            include_validation: Include validation status

        Returns:
            Dictionary containing intro canvas information
        """
        # Get intro canvas (assuming project has intro_canvas_id field or we find by type)
        intro_canvas = StoryCanvas.objects.filter(
            project=project, canvas_type=CanvasType.INTRO, deleted_at__isnull=True
        ).first()

        if not intro_canvas:
            return {
                "intro_canvas": None,
                "message": "Project does not have an intro canvas",
            }

        # Build response with canvas details
        response_data = intro_canvas.to_dict()

        # Add trigger info if requested
        if include_trigger:
            try:
                trigger = CanvasTrigger.objects.get(canvas=intro_canvas)
                response_data["trigger"] = trigger.to_dict()
                response_data["starting_location_id"] = (
                    str(trigger.location_id) if trigger.location_id else None
                )
            except CanvasTrigger.DoesNotExist:
                response_data["trigger"] = None
                response_data["starting_location_id"] = None

        # Add validation info if requested
        if include_validation:
            validation_result = StoryCanvasService.validate_canvas(intro_canvas)
            response_data["validation"] = validation_result

        return {
            "intro_canvas": response_data,
            "message": "Intro canvas retrieved successfully",
        }

    @staticmethod
    def create_canvas_with_validation(
        project: Project, canvas_data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Create a new story canvas with business validation.

        Args:
            project: Project instance
            canvas_data: Dictionary containing canvas data

        Returns:
            Dictionary containing created canvas and validation results
        """
        # Check canvas limits
        current_canvas_count = StoryCanvas.objects.filter(
            project=project, deleted_at__isnull=True
        ).count()

        max_canvases = 20  # Project limit
        if current_canvas_count >= max_canvases:
            raise ValidationError(
                f"Project has reached maximum canvas limit of {max_canvases}"
            )

        # Validate required fields (canvas_type has model default)
        required_fields = ["name"]
        for field in required_fields:
            if not canvas_data.get(field):
                raise ValidationError(f"Field '{field}' is required")

        # Set display order if not provided
        if "display_order" not in canvas_data:
            max_order = (
                StoryCanvas.objects.filter(
                    project=project, deleted_at__isnull=True
                ).aggregate(max_order=models.Max("display_order"))["max_order"]
                or 0
            )
            canvas_data["display_order"] = max_order + 1

        try:
            with transaction.atomic():
                # Extract canvas_settings and generation_settings like the serializer does
                canvas_settings = canvas_data.pop("canvas_settings", {})
                generation_settings = canvas_data.pop("generation_settings", {})

                # Store settings in metadata field (following serializer pattern)
                metadata = canvas_data.get("metadata", {})
                if canvas_settings:
                    metadata["canvas_settings"] = canvas_settings
                if generation_settings:
                    metadata["generation_settings"] = generation_settings
                canvas_data["metadata"] = metadata

                # Create canvas
                canvas = StoryCanvas.objects.create(
                    project=project,
                    **canvas_data,
                )

                # Validate the new canvas
                validation_result = StoryCanvasService.validate_canvas(canvas)

                return {
                    "canvas": canvas.to_dict(),
                    "validation": validation_result,
                    "message": "Canvas created successfully",
                }

        except Exception as e:
            raise ValidationError(f"Failed to create canvas: {str(e)}")

    @staticmethod
    def update_canvas(
        canvas: StoryCanvas, update_data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Update an existing canvas with validation.

        Args:
            canvas: StoryCanvas instance to update
            update_data: Dictionary containing update data

        Returns:
            Dictionary containing updated canvas
        """
        try:
            with transaction.atomic():
                # Handle canvas_settings and generation_settings if present
                canvas_settings = update_data.pop("canvas_settings", None)
                generation_settings = update_data.pop("generation_settings", None)

                if canvas_settings is not None or generation_settings is not None:
                    # Update metadata with settings (following serializer pattern)
                    metadata = canvas.metadata or {}
                    if canvas_settings is not None:
                        metadata["canvas_settings"] = canvas_settings
                    if generation_settings is not None:
                        metadata["generation_settings"] = generation_settings
                    update_data["metadata"] = metadata

                # Update fields
                for field, value in update_data.items():
                    if hasattr(canvas, field):
                        setattr(canvas, field, value)

                # Canvas updated automatically with auto_now=True
                canvas.save()

                # Re-validate if structure changed
                validation_result = StoryCanvasService.validate_canvas(canvas)

                return {
                    "canvas": canvas.to_dict(),
                    "validation": validation_result,
                    "message": "Canvas updated successfully",
                }

        except Exception as e:
            raise ValidationError(f"Failed to update canvas: {str(e)}")

    @staticmethod
    def duplicate_canvas(canvas: StoryCanvas, new_name: str) -> dict[str, Any]:
        """
        Duplicate an existing canvas with all its nodes and connections.

        Args:
            canvas: StoryCanvas instance to duplicate
            new_name: Name for the new canvas

        Returns:
            Dictionary containing duplicated canvas
        """
        try:
            with transaction.atomic():
                # Create new canvas
                new_canvas = StoryCanvas.objects.create(
                    project=canvas.project,
                    name=new_name,
                    description=f"Copy of {canvas.description}",
                    canvas_type=canvas.canvas_type,
                    status=CanvasStatus.DRAFT,
                    metadata=canvas.metadata.copy() if canvas.metadata else {},
                    tags=canvas.tags.copy() if canvas.tags else [],
                    estimated_play_time=canvas.estimated_play_time,
                    # created_at and updated_at set automatically
                )

                # Duplicate nodes
                node_mapping = {}  # Old node ID -> New node
                for old_node in canvas.nodes.all():
                    new_node = StoryNode.objects.create(
                        canvas=new_canvas,
                        name=f"{old_node.name} (Copy)",
                        position_x=old_node.position_x,
                        position_y=old_node.position_y,
                        width=old_node.width,
                        height=old_node.height,
                        node_data=(
                            old_node.node_data.copy() if old_node.node_data else {}
                        ),
                        tags=old_node.tags.copy() if old_node.tags else [],
                    )
                    node_mapping[old_node.id] = new_node

                # Duplicate connections
                for old_connection in canvas.connections.all():
                    if (
                        old_connection.source_node_id in node_mapping
                        and old_connection.target_node_id in node_mapping
                    ):
                        NodeConnection.objects.create(
                            canvas=new_canvas,
                            source_node=node_mapping[old_connection.source_node_id],
                            target_node=node_mapping[old_connection.target_node_id],
                            connection_type=old_connection.connection_type,
                            label=old_connection.label,
                            conditions=(
                                old_connection.conditions.copy()
                                if old_connection.conditions
                                else {}
                            ),
                            effects=(
                                old_connection.effects.copy()
                                if old_connection.effects
                                else {}
                            ),
                            metadata=(
                                old_connection.metadata.copy()
                                if old_connection.metadata
                                else {}
                            ),
                            weight=old_connection.weight,
                            is_bidirectional=old_connection.is_bidirectional,
                        )

                # Duplicate flags removed (StoryFlag no longer supported)

                # Update counts
                new_canvas.node_count = len(node_mapping)
                new_canvas.connection_count = NodeConnection.objects.filter(
                    canvas=new_canvas
                ).count()
                new_canvas.save()

                return {
                    "canvas": new_canvas.to_dict(),
                    "message": "Canvas duplicated successfully",
                }

        except Exception as e:
            raise ValidationError(f"Failed to duplicate canvas: {str(e)}")

    @staticmethod
    def validate_canvas(canvas: StoryCanvas) -> dict[str, Any]:
        """
        Validate a story canvas and its components.

        Args:
            canvas: StoryCanvas instance to validate

        Returns:
            Dictionary containing validation results
        """
        errors = []
        warnings = []

        # Get nodes and connections
        nodes = list(canvas.nodes.all())
        connections = list(canvas.connections.all())

        # Note: Start node validation removed - all nodes are equal now

        # Check for orphaned nodes
        connected_node_ids = set()
        for connection in connections:
            connected_node_ids.add(connection.source_node_id)
            connected_node_ids.add(connection.target_node_id)

        orphaned_nodes = [node for node in nodes if node.id not in connected_node_ids]
        if orphaned_nodes:
            warnings.append(
                {
                    "type": "orphaned_nodes",
                    "message": f"Found {len(orphaned_nodes)} orphaned nodes with no connections",
                    "severity": "warning",
                    "node_ids": [str(node.id) for node in orphaned_nodes],
                }
            )

        # Check for circular references
        # Simple check - can be made more sophisticated
        for connection in connections:
            if connection.source_node_id == connection.target_node_id:
                warnings.append(
                    {
                        "type": "self_reference",
                        "message": f"Node {connection.source_node.name} connects to itself",
                        "severity": "warning",
                    }
                )

        # Update canvas validation status
        is_valid = len(errors) == 0
        canvas.is_valid = is_valid
        canvas.validation_errors = errors + warnings
        canvas.last_validated_at = timezone.now()
        canvas.save()

        return {
            "is_valid": is_valid,
            "error_count": len(errors),
            "warning_count": len(warnings),
            "errors": errors,
            "warnings": warnings,
            "validation_timestamp": canvas.last_validated_at.isoformat(),
        }

    @staticmethod
    def get_canvas_templates() -> list[dict[str, Any]]:
        """
        Get available canvas templates for creation.

        Returns:
            List of template dictionaries
        """
        templates = [
            {
                "id": "basic_story",
                "name": "Basic Story Canvas",
                "description": "Simple linear story with start, middle, and end nodes",
                "canvas_type": CanvasType.STORY,
                "node_count": 3,
                "estimated_setup_time": 5,
                "difficulty_level": "Beginner",
                "tags": ["linear", "simple", "beginner"],
                "preview_image": "/templates/basic_story.png",
            },
            {
                "id": "branching_narrative",
                "name": "Branching Narrative",
                "description": "Story with multiple choice paths and outcomes",
                "canvas_type": CanvasType.STORY,
                "node_count": 8,
                "estimated_setup_time": 15,
                "difficulty_level": "Intermediate",
                "tags": ["branching", "choices", "intermediate"],
                "preview_image": "/templates/branching_narrative.png",
            },
            {
                "id": "intro_sequence",
                "name": "Introduction Sequence",
                "description": "Template for game introduction with character setup",
                "canvas_type": CanvasType.INTRO,
                "node_count": 5,
                "estimated_setup_time": 10,
                "difficulty_level": "Beginner",
                "tags": ["intro", "character", "setup"],
                "preview_image": "/templates/intro_sequence.png",
            },
            {
                "id": "dialogue_tree",
                "name": "Dialogue Tree",
                "description": "Conversation system with NPC interaction",
                "canvas_type": CanvasType.DIALOGUE,
                "node_count": 12,
                "estimated_setup_time": 20,
                "difficulty_level": "Advanced",
                "tags": ["dialogue", "npc", "conversation"],
                "preview_image": "/templates/dialogue_tree.png",
            },
            {
                "id": "tutorial_flow",
                "name": "Tutorial Flow",
                "description": "Step-by-step tutorial with validation checkpoints",
                "canvas_type": CanvasType.TUTORIAL,
                "node_count": 6,
                "estimated_setup_time": 12,
                "difficulty_level": "Intermediate",
                "tags": ["tutorial", "learning", "checkpoints"],
                "preview_image": "/templates/tutorial_flow.png",
            },
        ]

        return templates

    @staticmethod
    def soft_delete_canvas(canvas: StoryCanvas, deleted_by: User) -> dict[str, Any]:
        """
        Soft delete a canvas and all its components.

        Args:
            canvas: StoryCanvas instance to delete
            deleted_by: User performing the deletion

        Returns:
            Dictionary with deletion confirmation
        """
        try:
            with transaction.atomic():
                # Soft delete the canvas
                canvas.soft_delete()
                # Canvas updated automatically
                canvas.save()

                return {
                    "message": "Canvas deleted successfully",
                    "canvas_id": str(canvas.id),
                }

        except Exception as e:
            raise ValidationError(f"Failed to delete canvas: {str(e)}")

    @staticmethod
    def create_default_starting_canvas(project: Project) -> dict[str, Any]:
        """
        Create a default starting canvas for a new project.

        Args:
            project: Project instance to create starting canvas for

        Returns:
            Dictionary containing created canvas
        """
        try:
            with transaction.atomic():
                # Create the starting canvas
                canvas = StoryCanvas.objects.create(
                    project=project,
                    name="Introduction",
                    description="Welcome to your story! This is your starting canvas.",
                    canvas_type=CanvasType.INTRO,
                    status=CanvasStatus.DRAFT,
                    # created_at and updated_at set automatically
                    display_order=0,  # First canvas
                    metadata={
                        "is_default_starting": True,
                        "created_automatically": True,
                    },
                )

                # Create a default welcome node
                welcome_node = StoryNode.objects.create(
                    canvas=canvas,
                    name="Welcome",
                    position_x=300,  # Center position
                    position_y=200,
                    width=200,
                    height=100,
                    node_data={
                        "content": "Welcome to your story! Edit this canvas to create your opening scene. This is where your adventure begins!",
                        "version": "1.0",
                    },
                    tags=["default"],
                )

                # Update canvas counts
                canvas.node_count = 1
                canvas.connection_count = 0
                canvas.save()

                # Set this canvas as the project's starting canvas
                project.starting_canvas = canvas
                project.save(update_fields=["starting_canvas"])

                return {
                    "canvas": canvas.to_dict(),
                    "message": "Default starting canvas created successfully",
                }

        except Exception as e:
            raise ValidationError(f"Failed to create default starting canvas: {str(e)}")

    @staticmethod
    def get_project_canvases_for_settings(project: Project) -> list[dict[str, Any]]:
        """
        Get simplified canvas list for project settings dropdown.

        Args:
            project: Project instance

        Returns:
            List of canvas dictionaries with id, name, canvas_type
        """
        canvases = (
            StoryCanvas.objects.filter(project=project, deleted_at__isnull=True)
            .only("id", "name", "canvas_type")
            .order_by("display_order", "name")
        )

        canvas_list = []
        for canvas in canvases:
            canvas_list.append(
                {
                    "id": str(canvas.id),
                    "name": canvas.name,
                    "canvas_type": canvas.canvas_type,
                }
            )

        return canvas_list

    # Define allowed fields for updating (excludes read-only system fields)
    ALLOWED_NODE_FIELDS = {
        "name",
        "position_x",
        "position_y",
        "width",
        "height",
        "node_data",
        "tags",
        "exit_block",
    }

    ALLOWED_CONNECTION_FIELDS = {
        # Connection endpoints (support both ForeignKey and ID versions)
        "source_node",
        "source_node_id",
        "target_node",
        "target_node_id",
        # Basic properties
        "connection_type",
        "label",
        # Connection logic
        "conditions",
        "effects",
        "metadata",
        # Visual properties
        "path_data",
        "style",
        # Connection behavior
        "priority",
        "weight",
        "is_bidirectional",
    }

    # StoryFlag removed: flag field set no longer used

    @staticmethod
    def save_story_content(
        canvas: StoryCanvas, story_data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Save complete story content (nodes, connections, flags) atomically.

        Args:
            canvas: StoryCanvas instance to update
            story_data: Dictionary containing nodes, connections, and flags

        Returns:
            Dictionary containing save results and statistics
        """
        try:
            with transaction.atomic():
                saved_counts = {"nodes": 0, "connections": 0}

                # Save nodes
                if "nodes" in story_data and story_data["nodes"]:
                    from .serializers import StoryNodeCreateSerializer
                    for node_data in story_data["nodes"]:
                        # Check if node exists (update) or is new (create)
                        node_id = node_data.get("id")
                        # Safety: validate and normalize exit_block (including per-choice conditions)
                        try:
                            if "exit_block" in node_data and node_data["exit_block"] is not None:
                                validator = StoryNodeCreateSerializer(context={"project": canvas.project})
                                node_data["exit_block"] = validator.validate_exit_block(node_data["exit_block"])  # type: ignore[assignment]
                        except Exception as e:
                            raise ValidationError(f"Invalid exit_block for node: {str(e)}")
                        if (
                            node_id
                            and StoryNode.objects.filter(
                                id=node_id, canvas=canvas
                            ).exists()
                        ):
                            # Update existing node - only update allowed fields
                            node = StoryNode.objects.get(id=node_id, canvas=canvas)
                            for field, value in node_data.items():
                                if (
                                    field in StoryCanvasService.ALLOWED_NODE_FIELDS
                                    and hasattr(node, field)
                                ):
                                    setattr(node, field, value)
                            node.save()
                        else:
                            # Create new node - filter to allowed fields only
                            filtered_data = {
                                field: value
                                for field, value in node_data.items()
                                if field in StoryCanvasService.ALLOWED_NODE_FIELDS
                            }
                            StoryNode.objects.create(canvas=canvas, **filtered_data)
                        saved_counts["nodes"] += 1

                # Save connections
                if "connections" in story_data and story_data["connections"]:
                    for conn_data in story_data["connections"]:
                        conn_id = conn_data.get("id")
                        if (
                            conn_id
                            and NodeConnection.objects.filter(
                                id=conn_id, canvas=canvas
                            ).exists()
                        ):
                            # Update existing connection - only update allowed fields
                            connection = NodeConnection.objects.get(
                                id=conn_id, canvas=canvas
                            )
                            for field, value in conn_data.items():
                                if (
                                    field
                                    in StoryCanvasService.ALLOWED_CONNECTION_FIELDS
                                    and hasattr(connection, field)
                                ):
                                    setattr(connection, field, value)
                            connection.save()
                        else:
                            # Create new connection - filter to allowed fields only
                            filtered_data = {
                                field: value
                                for field, value in conn_data.items()
                                if field in StoryCanvasService.ALLOWED_CONNECTION_FIELDS
                            }
                            NodeConnection.objects.create(
                                canvas=canvas, **filtered_data
                            )
                        saved_counts["connections"] += 1

                # Save flags removed (StoryFlag no longer supported)

                # Update canvas counts and metadata
                canvas.node_count = canvas.nodes.count()
                canvas.connection_count = canvas.connections.count()
                # Canvas updated automatically with auto_now=True
                canvas.save()

                # Return success response
                total_saved = sum(saved_counts.values())
                message = f"Story saved successfully: {total_saved} items updated"

                return {
                    "success": True,
                    "message": message,
                    "saved_counts": saved_counts,
                    "save_timestamp": timezone.now(),
                }

        except Exception as e:
            raise ValidationError(f"Failed to save story content: {str(e)}")


class StoryNodeService:
    """Service layer for story node operations."""

    @staticmethod
    def create_node(canvas: StoryCanvas, node_data: dict[str, Any]) -> dict[str, Any]:
        """Create a new node in the canvas."""
        try:
            with transaction.atomic():
                node = StoryNode.objects.create(canvas=canvas, **node_data)

                # Update canvas node count
                canvas.node_count = canvas.nodes.count()
                canvas.save()

                return {"node": node.to_dict(), "message": "Node created successfully"}

        except Exception as e:
            raise ValidationError(f"Failed to create node: {str(e)}")

    @staticmethod
    def update_node(node: StoryNode, update_data: dict[str, Any]) -> dict[str, Any]:
        """Update an existing node."""
        try:
            for field, value in update_data.items():
                if hasattr(node, field):
                    setattr(node, field, value)

            node.save()

            return {"node": node.to_dict(), "message": "Node updated successfully"}

        except Exception as e:
            raise ValidationError(f"Failed to update node: {str(e)}")

    @staticmethod
    def delete_node(node: StoryNode) -> dict[str, Any]:
        """Delete a node and its connections."""
        try:
            with transaction.atomic():
                canvas = node.canvas

                # Delete all connections involving this node
                NodeConnection.objects.filter(
                    models.Q(source_node=node) | models.Q(target_node=node)
                ).delete()

                # Delete the node
                node.delete()

                # Update canvas counts
                canvas.node_count = canvas.nodes.count()
                canvas.connection_count = canvas.connections.count()
                canvas.save()

                return {"message": "Node deleted successfully", "node_id": str(node.id)}

        except Exception as e:
            raise ValidationError(f"Failed to delete node: {str(e)}")

    @staticmethod
    def update_node_with_blocks(
        node: StoryNode, blocks_data: dict[str, Any], user: User = None
    ) -> dict[str, Any]:
        """Update a node with BlockNote blocks content."""
        from .services.block_conversion import BlockConversionService
        from .services.validation import BlockValidationService

        try:
            with transaction.atomic():
                # Validate the blocks data
                validation_result = BlockValidationService.validate_story_node(
                    {
                        "name": node.name,
                        "node_data": blocks_data,
                        "tags": node.tags or [],
                    }
                )

                if not validation_result.is_valid:
                    error_messages = BlockValidationService.format_validation_errors(
                        validation_result
                    )
                    raise ValidationError(
                        f"Block validation failed: {', '.join(error_messages)}"
                    )

                # Update the node data
                node.node_data = blocks_data
                # Node updated automatically
                node.save()

                # Generate content statistics
                content_stats = BlockConversionService.get_content_stats(
                    blocks_data.get("blocks", [])
                )

                return {
                    "node": node.to_dict(),
                    "content_stats": content_stats,
                    "message": "Node updated with blocks successfully",
                    "warnings": (
                        BlockValidationService.format_validation_warnings(
                            validation_result
                        )
                        if validation_result.warnings
                        else None
                    ),
                }

        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(f"Failed to update node with blocks: {str(e)}")

    @staticmethod
    def convert_legacy_content_to_blocks(node: StoryNode) -> dict[str, Any]:
        """Convert legacy content in a node to BlockNote blocks format."""
        from .services.block_conversion import BlockConversionService

        try:
            current_data = node.node_data or {}

            # Check if already converted
            if BlockConversionService._is_block_format(current_data):
                return {
                    "node": node.to_dict(),
                    "message": "Content is already in block format",
                    "converted": False,
                }

            # Migrate the data
            migrated_data = BlockConversionService.migrate_node_data(current_data)

            # Update the node
            node.node_data = migrated_data
            node.save()

            # Generate content statistics
            content_stats = BlockConversionService.get_content_stats(
                migrated_data.get("blocks", [])
            )

            return {
                "node": node.to_dict(),
                "content_stats": content_stats,
                "message": "Content converted to block format successfully",
                "converted": True,
            }

        except Exception as e:
            raise ValidationError(f"Failed to convert content to blocks: {str(e)}")

    @staticmethod
    def validate_node_blocks(node: StoryNode) -> dict[str, Any]:
        """Validate a node's BlockNote content."""
        from .services.validation import BlockValidationService

        try:
            # Prepare validation data
            validation_data = {
                "name": node.name,
                "node_data": node.node_data or {},
                "tags": node.tags or [],
            }

            # Perform validation
            validation_result = BlockValidationService.validate_story_node(
                validation_data
            )

            return {
                "node_id": str(node.id),
                "node_name": node.name,
                "is_valid": validation_result.is_valid,
                "errors": BlockValidationService.format_validation_errors(
                    validation_result
                ),
                "warnings": BlockValidationService.format_validation_warnings(
                    validation_result
                ),
                "message": "Node validation completed",
            }

        except Exception as e:
            return {
                "node_id": str(node.id),
                "node_name": node.name,
                "is_valid": False,
                "errors": [f"Validation failed: {str(e)}"],
                "warnings": [],
                "message": "Validation failed with error",
            }


class NodeConnectionService:
    """Service layer for node connection operations."""

    @staticmethod
    def create_connection(
        canvas: StoryCanvas, connection_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a new connection between nodes."""
        try:
            with transaction.atomic():
                connection = NodeConnection.objects.create(
                    canvas=canvas, **connection_data
                )

                # Update canvas connection count
                canvas.connection_count = canvas.connections.count()
                canvas.save()

                return {
                    "connection": connection.to_dict(),
                    "message": "Connection created successfully",
                }

        except Exception as e:
            raise ValidationError(f"Failed to create connection: {str(e)}")

    @staticmethod
    def delete_connection(connection: NodeConnection) -> dict[str, Any]:
        """Delete a connection."""
        try:
            with transaction.atomic():
                canvas = connection.canvas
                connection.delete()

                # Update canvas connection count
                canvas.connection_count = canvas.connections.count()
                canvas.save()

                return {
                    "message": "Connection deleted successfully",
                    "connection_id": str(connection.id),
                }

        except Exception as e:
            raise ValidationError(f"Failed to delete connection: {str(e)}")


class CanvasTriggerService:
    """Service layer for canvas trigger operations."""

    @staticmethod
    def get_canvas_trigger(canvas: StoryCanvas) -> Optional[dict[str, Any]]:
        """
        Get trigger for a canvas.

        Args:
            canvas: StoryCanvas instance

        Returns:
            Dictionary containing trigger data or None
        """
        try:
            trigger = CanvasTrigger.objects.get(canvas=canvas)
            return trigger.to_dict()
        except CanvasTrigger.DoesNotExist:
            return None

    @staticmethod
    def create_canvas_trigger(
        canvas: StoryCanvas, trigger_data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Create a new trigger for a canvas.

        Args:
            canvas: StoryCanvas instance
            trigger_data: Dictionary containing trigger data

        Returns:
            Dictionary containing created trigger
        """
        try:
            # Check if trigger already exists
            if hasattr(canvas, "trigger") and canvas.trigger:
                raise ValidationError("Canvas already has a trigger")

            with transaction.atomic():
                trigger = CanvasTrigger.objects.create(
                    canvas=canvas,
                    # created_at and updated_at set automatically
                    **trigger_data,
                )

                return {
                    "trigger": trigger.to_dict(),
                    "message": "Canvas trigger created successfully",
                }

        except Exception as e:
            raise ValidationError(f"Failed to create canvas trigger: {str(e)}")

    @staticmethod
    def update_canvas_trigger(
        trigger: CanvasTrigger, update_data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Update an existing canvas trigger.

        Args:
            trigger: CanvasTrigger instance to update
            update_data: Dictionary containing update data

        Returns:
            Dictionary containing updated trigger
        """
        try:
            with transaction.atomic():
                for field, value in update_data.items():
                    if hasattr(trigger, field):
                        setattr(trigger, field, value)

                # Trigger updated automatically
                trigger.save()

                return {
                    "trigger": trigger.to_dict(),
                    "message": "Canvas trigger updated successfully",
                }

        except Exception as e:
            raise ValidationError(f"Failed to update canvas trigger: {str(e)}")

    @staticmethod
    def delete_canvas_trigger(trigger: CanvasTrigger) -> dict[str, Any]:
        """
        Delete a canvas trigger.

        Args:
            trigger: CanvasTrigger instance to delete

        Returns:
            Dictionary with deletion confirmation
        """
        try:
            trigger_id = str(trigger.id)
            trigger.delete()

            return {
                "message": "Canvas trigger deleted successfully",
                "trigger_id": trigger_id,
            }

        except Exception as e:
            raise ValidationError(f"Failed to delete canvas trigger: {str(e)}")
