"""
NPC Management service layer.

Provides business logic for NPC operations including CRUD, validation,
limits enforcement, and template generation.
"""

from typing import Any, Optional

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.projects.models import Project

from .models import NPC, NPCStatus

User = get_user_model()


class NPCService:
    """Service layer for NPC management operations."""

    @staticmethod
    def get_npc_overview(project: Project) -> dict[str, Any]:
        """
        Get comprehensive NPC overview for a project.

        Args:
            project: Project instance

        Returns:
            Dictionary containing NPCs and statistics
        """
        # Get all non-deleted NPCs for the project
        npcs = NPC.objects.filter(
            project=project, deleted_at__isnull=True
        )

        # Convert to dictionary format - include details for frontend compatibility
        npc_list = []
        for npc in npcs:
            npc_list.append(npc.to_dict(include_details=True))

        # Calculate statistics
        total_npcs = len(npc_list)

        # Status distribution
        status_distribution = {}
        for npc in npc_list:
            status = npc.get("status", NPCStatus.CONCEPT.value)
            status_distribution[status] = status_distribution.get(status, 0) + 1

        # Get project NPC limit (default 50)
        max_npcs = getattr(project, "max_npcs", 50)
        completion_percentage = min(100.0, (total_npcs / max(1, max_npcs)) * 100)

        # Location assignments removed - NPCs automatically placed during game generation
        location_assignments = {}

        return {
            "project_id": str(project.id),
            "npcs": npc_list,
            "npc_limits": {
                "max_npcs": max_npcs,
                "remaining_slots": max(0, max_npcs - total_npcs),
            },
            "npc_statistics": {
                "total_npcs": total_npcs,
                "location_assignments": location_assignments,
                "completion_percentage": completion_percentage,
            },
        }

    @staticmethod
    def create_npc_with_validation(
        project: Project, npc_data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Create a new NPC with business validation.

        Args:
            project: Project instance
            npc_data: NPC creation data

        Returns:
            Created NPC dictionary

        Raises:
            ValidationError: If validation fails
        """
        with transaction.atomic():
            # Validate NPC limit
            max_npcs = getattr(project, "max_npcs", 50)
            existing_count = NPC.objects.filter(
                project=project, deleted_at__isnull=True
            ).count()

            if existing_count >= max_npcs:
                raise ValidationError(
                    f"NPC limit reached ({max_npcs}). "
                    f"Current NPCs: {existing_count}"
                )

            # Create NPC instance
            npc = NPC(
                project=project,
                # Timestamps set automatically
                **npc_data,
            )

            # Run Django model validation
            npc.clean()
            npc.save()

            return npc.to_dict(include_details=True)

    @staticmethod
    def get_npc_by_id(project: Project, npc_id: str) -> Optional[dict[str, Any]]:
        """
        Get NPC by ID with project ownership validation.

        Args:
            project: Project instance for ownership validation
            npc_id: NPC UUID string

        Returns:
            NPC dictionary or None if not found
        """
        try:
            npc = NPC.objects.get(id=npc_id, project=project, deleted_at__isnull=True)
            return npc.to_dict(include_details=True)
        except NPC.DoesNotExist:
            return None

    @staticmethod
    def update_npc_with_validation(
        project: Project, npc_id: str, npc_data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Update NPC with business validation.

        Args:
            project: Project instance for ownership validation
            npc_id: NPC UUID string
            npc_data: NPC update data

        Returns:
            Updated NPC dictionary

        Raises:
            ValidationError: If validation fails or NPC not found
        """
        with transaction.atomic():
            try:
                npc = NPC.objects.get(
                    id=npc_id, project=project, deleted_at__isnull=True
                )
            except NPC.DoesNotExist:
                raise ValidationError(f"NPC {npc_id} not found")

            # Update NPC fields
            for field, value in npc_data.items():
                if hasattr(npc, field):
                    setattr(npc, field, value)

            # Update metadata
            # NPC updated automatically
            npc.updated_at = timezone.now()

            # Run Django model validation
            npc.clean()
            npc.save()

            return npc.to_dict(include_details=True)

    @staticmethod
    def delete_npc(project: Project, npc_id: str) -> bool:
        """
        Soft delete NPC with project ownership validation.

        Args:
            project: Project instance for ownership validation
            npc_id: NPC UUID string

        Returns:
            True if deleted successfully

        Raises:
            ValidationError: If NPC not found
        """
        with transaction.atomic():
            try:
                npc = NPC.objects.get(
                    id=npc_id, project=project, deleted_at__isnull=True
                )
            except NPC.DoesNotExist:
                raise ValidationError(f"NPC {npc_id} not found")

            # Soft delete
            npc.soft_delete()
            return True

    @staticmethod
    def update_npc_ai_behavior(
        project: Project, npc_id: str, behavior_data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Update NPC AI behavior configuration.

        Args:
            project: Project instance for ownership validation
            npc_id: NPC UUID string
            behavior_data: AI behavior update data

        Returns:
            Updated behavior dictionary

        Raises:
            ValidationError: If NPC not found
        """
        with transaction.atomic():
            try:
                npc = NPC.objects.get(
                    id=npc_id, project=project, deleted_at__isnull=True
                )
            except NPC.DoesNotExist:
                raise ValidationError(f"NPC {npc_id} not found")

            # Update AI behavior configuration
            if "ai_behavior_config" in behavior_data:
                npc.ai_behavior_config = behavior_data["ai_behavior_config"]

            # NPC updated automatically
            npc.updated_at = timezone.now()
            npc.save()

            return {"npc_id": str(npc.id), "ai_behavior_config": npc.ai_behavior_config}

    @staticmethod
    def get_npc_statistics(project: Project) -> dict[str, Any]:
        """
        Get detailed NPC statistics for a project.

        Args:
            project: Project instance

        Returns:
            Dictionary containing detailed statistics
        """
        npcs = NPC.objects.filter(project=project, deleted_at__isnull=True)

        # Basic counts
        total_npcs = npcs.count()

        # Status distribution
        status_distribution = {}
        for status in NPCStatus:
            count = npcs.filter(status=status.value).count()
            if count > 0:
                status_distribution[status.value] = count

        return {
            "total_npcs": total_npcs,
            "status_distribution": status_distribution,
            "completion_percentage": min(
                100.0, (total_npcs / max(1, getattr(project, "max_npcs", 50))) * 100
            ),
        }

    @staticmethod
    def bulk_update_npcs(
        project: Project,
        npc_ids: list[str],
        update_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Bulk update multiple NPCs.

        Args:
            project: Project instance
            npc_ids: List of NPC UUID strings
            update_data: Data to apply to all NPCs

        Returns:
            Dictionary with update results
        """
        with transaction.atomic():
            npcs = NPC.objects.filter(
                id__in=npc_ids, project=project, deleted_at__isnull=True
            )

            if not npcs.exists():
                raise ValidationError("No valid NPCs found for update")

            updated_count = 0
            for npc in npcs:
                # Update fields
                for field, value in update_data.items():
                    if hasattr(npc, field):
                        setattr(npc, field, value)

                # NPC updated automatically
                npc.updated_at = timezone.now()
                npc.save()
                updated_count += 1

            return {
                "updated_count": updated_count,
                "total_requested": len(npc_ids),
                "success": True,
            }
