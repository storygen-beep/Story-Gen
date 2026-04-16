"""
Trigger adapter for converting CanvasTrigger objects to Entity/Edge records.

Implements the entity-agnostic vision by converting canvas trigger domain objects
into searchable Entity records with embedded scheduling information and relationships.
"""

import logging
from typing import Any

from django.utils.text import slugify

from apps.stories.models import CanvasTrigger

from ..models import EntityType, Predicate
from .base import BaseAdapter

logger = logging.getLogger(__name__)


class TriggerAdapter(BaseAdapter):
    """
    Adapter for converting CanvasTrigger objects to Entity/Edge records.

    Extracts trigger metadata, scheduling information, and relationships
    (trigger->location, trigger->schedules) into the entity-agnostic storage format.

    Part of hybrid approach: separate trigger entities for granular queries
    while canvas entities contain embedded trigger data for convenience.
    """

    def get_entity_type(self) -> EntityType:
        """Trigger entities use 'trigger' type."""
        return EntityType.TRIGGER

    def extract_entity_data(self, trigger: CanvasTrigger) -> dict[str, Any]:
        """
        Extract entity data from CanvasTrigger.

        Args:
            trigger: CanvasTrigger instance

        Returns:
            Entity data dictionary
        """
        # Create trigger summary
        summary = f"Canvas trigger for '{trigger.canvas.name}'"
        if trigger.location_id:
            summary += f" at location {trigger.location_id}"
        if trigger.is_active:
            summary += " (Active)"
        else:
            summary += " (Inactive)"

        # Extract schedule information for embedding
        schedule_info = []
        if hasattr(trigger, 'schedules'):
            for schedule in trigger.schedules.all():
                # Process weekdays array - convert to readable format
                weekday_names = []
                if schedule.weekdays:
                    weekday_names = [self._get_weekday_name(day) for day in schedule.weekdays if 0 <= day <= 6]

                schedule_data = {
                    'id': str(schedule.id),
                    'start_time': schedule.start_time.strftime("%H:%M") if schedule.start_time else None,
                    'end_time': schedule.end_time.strftime("%H:%M") if schedule.end_time else None,
                    'weekdays': schedule.weekdays,
                    'weekday_names': weekday_names,
                    'time_period': self._extract_time_period(schedule.start_time) if schedule.start_time else None,
                    'name': schedule.name,
                }
                schedule_info.append(schedule_data)

        # Create JSON snapshot of trigger data
        json_data = {
            'canvas_id': str(trigger.canvas_id),
            'canvas_name': trigger.canvas.name,
            'location_id': str(trigger.location_id) if trigger.location_id else None,
            'location_name': None,  # Location name lookup would require separate query
            'is_active': trigger.is_active,
            'trigger_condition': trigger.conditions,
            'metadata': trigger.metadata,
            'embedded_schedules': schedule_info,
            'schedule_count': len(schedule_info),
            'has_active_schedules': len(schedule_info) > 0,  # All existing schedules are considered active
            'created_at': trigger.created_at.isoformat(),
            'updated_at': trigger.updated_at.isoformat(),
        }

        # Generate searchable text
        searchable_text = self._extract_trigger_text(trigger)

        return {
            'entity_type': self.get_entity_type(),
            'name': f"{trigger.canvas.name} Trigger",
            'version': 1,  # Trigger versioning not implemented yet
            'summary': summary,
            'json_data': json_data,
            'text': searchable_text,
            'tags': self._generate_trigger_tags(trigger),
        }

    def extract_relationships(self, trigger: CanvasTrigger) -> list[tuple[str, str, str]]:
        """
        Extract relationships from CanvasTrigger.

        Relationships:
        - canvas HAS_TRIGGER trigger
        - trigger LOCATED_AT location (if location exists)
        - trigger HAS_SCHEDULE schedule (for each schedule)

        Args:
            trigger: CanvasTrigger instance

        Returns:
            List of (subject_id, predicate, object_id) tuples
        """
        relationships = []
        trigger_id = str(trigger.id)
        canvas_id = str(trigger.canvas_id)

        # Canvas -> Trigger relationship
        relationships.append((canvas_id, Predicate.HAS_TRIGGER, trigger_id))
        logger.debug(f"Found canvas->trigger relationship: {trigger.canvas.name} has trigger {trigger_id}")

        # Trigger -> Location relationship
        if trigger.location_id:
            location_id = str(trigger.location_id)
            relationships.append((trigger_id, Predicate.LOCATED_AT, location_id))
            logger.debug(f"Found trigger->location relationship: trigger {trigger_id} at location {location_id}")

        # Trigger -> Schedule relationships
        if hasattr(trigger, 'schedules'):
            for schedule in trigger.schedules.all():
                schedule_id = str(schedule.id)
                relationships.append((trigger_id, Predicate.HAS_SCHEDULE, schedule_id))
                logger.debug(f"Found trigger->schedule relationship: trigger {trigger_id} has schedule {schedule_id}")

        return relationships

    def _extract_trigger_text(self, trigger: CanvasTrigger) -> str:
        """
        Extract searchable text from trigger and its properties.

        Args:
            trigger: CanvasTrigger instance

        Returns:
            Concatenated searchable text
        """
        text_parts = []

        # Add canvas name and trigger info
        text_parts.append(trigger.canvas.name)
        text_parts.append("trigger")

        # Add location information
        if trigger.location_id:
            text_parts.append(f"location-{trigger.location_id}")
            text_parts.append("location")

        # Add trigger condition
        if trigger.conditions:
            text_parts.append(str(trigger.conditions))

        # Add metadata text
        if trigger.metadata and isinstance(trigger.metadata, dict):
            for key, value in trigger.metadata.items():
                if isinstance(value, str):
                    text_parts.append(f"{key}: {value}")
                elif isinstance(value, (list, tuple)):
                    text_parts.extend([str(v) for v in value if isinstance(v, str)])

        # Add schedule information
        if hasattr(trigger, 'schedules'):
            for schedule in trigger.schedules.all():
                text_parts.append("schedule")
                text_parts.append(schedule.name)

                if schedule.start_time:
                    time_str = schedule.start_time.strftime("%H:%M")
                    text_parts.append(f"time {time_str}")
                    text_parts.append(self._extract_time_period(schedule.start_time))

                if schedule.end_time:
                    end_time_str = schedule.end_time.strftime("%H:%M")
                    text_parts.append(f"until {end_time_str}")

                # Process weekdays array
                if schedule.weekdays:
                    for day in schedule.weekdays:
                        if 0 <= day <= 6:
                            weekday_name = self._get_weekday_name(day)
                            text_parts.append(f"day {weekday_name}")
                            text_parts.append(weekday_name.lower())

        # Add contextual keywords
        if trigger.is_active:
            text_parts.append("active enabled")
        else:
            text_parts.append("inactive disabled")

        return ' '.join(text_parts)

    def _generate_trigger_tags(self, trigger: CanvasTrigger) -> list[str]:
        """
        Generate tags for trigger categorization and filtering.

        Args:
            trigger: CanvasTrigger instance

        Returns:
            List of tags
        """
        tags = ['trigger']

        # Add canvas-related tags
        tags.append('canvas-trigger')
        canvas_type = getattr(trigger.canvas, 'canvas_type', None)
        if canvas_type:
            tags.append(f"canvas-{canvas_type}")

        # Add location tags
        if trigger.location_id:
            tags.append('located')
            tags.append(f"location-{trigger.location_id}")
        else:
            tags.append('location-independent')

        # Add activity tags
        if trigger.is_active:
            tags.append('active')
        else:
            tags.append('inactive')

        # Add scheduling tags
        if hasattr(trigger, 'schedules'):
            schedule_count = trigger.schedules.count()
            if schedule_count > 0:
                tags.append('scheduled')
                tags.append(f"schedule-count-{schedule_count}")

                # Add time-based tags from schedules
                for schedule in trigger.schedules.all():
                    if schedule.start_time:
                        time_period = self._extract_time_period(schedule.start_time)
                        tags.append(f"time-{time_period}")

                    # Process weekdays array
                    if schedule.weekdays:
                        for day in schedule.weekdays:
                            if 0 <= day <= 6:
                                weekday_name = self._get_weekday_name(day)
                                tags.append(f"day-{weekday_name.lower()}")
            else:
                tags.append('unscheduled')

        # Add metadata-based tags
        if trigger.metadata and isinstance(trigger.metadata, dict):
            for key, value in trigger.metadata.items():
                tag = slugify(key)
                if tag:
                    tags.append(f"meta-{tag}")

        return tags

    def _get_weekday_name(self, day_of_week: int) -> str:
        """
        Convert day of week integer to name.

        Args:
            day_of_week: Integer representing day (0=Monday, 6=Sunday)

        Returns:
            Weekday name
        """
        weekdays = [
            'Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday'
        ]
        if 0 <= day_of_week <= 6:
            return weekdays[day_of_week]
        return f"unknown-day-{day_of_week}"

    def _extract_time_period(self, trigger_time) -> str:
        """
        Extract time period from trigger time.

        Args:
            trigger_time: Time object

        Returns:
            Time period string (morning, afternoon, evening, night)
        """
        if not trigger_time:
            return "anytime"

        hour = trigger_time.hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"

    def sync_all_triggers(self, force_update: bool = False) -> dict[str, Any]:
        """
        Sync all triggers in project to Entity records.

        Args:
            force_update: Force update all triggers

        Returns:
            Sync statistics
        """
        # Import here to avoid circular imports
        from apps.stories.models import CanvasTrigger

        triggers = CanvasTrigger.objects.filter(
            canvas__project_id=self.project_id,
            canvas__deleted_at__isnull=True
        ).select_related('canvas').prefetch_related('schedules')

        stats = {
            'total_triggers': triggers.count(),
            'synced_entities': 0,
            'synced_relationships': 0,
            'errors': []
        }

        logger.info(f"Syncing {stats['total_triggers']} triggers for project {self.project_id}")

        for trigger in triggers:
            try:
                result = self.full_sync(trigger, force_update=force_update)
                stats['synced_entities'] += 1
                stats['synced_relationships'] += result['relationship_count']
            except Exception as e:
                error_msg = f"Failed to sync trigger {trigger.id} ({trigger.canvas.name} trigger): {str(e)}"
                logger.error(error_msg)
                stats['errors'].append(error_msg)

        logger.info(f"Trigger sync complete: {stats['synced_entities']}/{stats['total_triggers']} entities, "
                   f"{stats['synced_relationships']} relationships, {len(stats['errors'])} errors")

        return stats
