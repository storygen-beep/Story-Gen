"""
Schedule adapter for converting TriggerSchedule objects to Entity/Edge records.

Implements the entity-agnostic vision by converting trigger schedule domain objects
into searchable Entity records with temporal information and relationships.
"""

import logging
from typing import Any

from apps.stories.models import TriggerSchedule

from ..models import EntityType
from .base import BaseAdapter

logger = logging.getLogger(__name__)


class ScheduleAdapter(BaseAdapter):
    """
    Adapter for converting TriggerSchedule objects to Entity/Edge records.

    Extracts schedule timing, metadata, and relationships (trigger->schedule)
    into the entity-agnostic storage format for temporal queries.

    Part of hybrid approach: separate schedule entities for granular temporal queries
    while trigger entities contain embedded schedule data for convenience.
    """

    def get_entity_type(self) -> EntityType:
        """Schedule entities use 'schedule' type."""
        return EntityType.SCHEDULE

    def extract_entity_data(self, schedule: TriggerSchedule) -> dict[str, Any]:
        """
        Extract entity data from TriggerSchedule.

        Args:
            schedule: TriggerSchedule instance

        Returns:
            Entity data dictionary
        """
        # Create schedule summary
        summary_parts = [schedule.name]

        if schedule.start_time:
            time_str = schedule.start_time.strftime("%H:%M")
            time_period = self._extract_time_period(schedule.start_time)
            summary_parts.append(f"at {time_str} ({time_period})")

        if schedule.end_time:
            end_time_str = schedule.end_time.strftime("%H:%M")
            summary_parts.append(f"until {end_time_str}")

        # Process weekdays array
        if schedule.weekdays:
            weekday_names = [self._get_weekday_name(day) for day in schedule.weekdays if 0 <= day <= 6]
            if weekday_names:
                if len(weekday_names) == 7:
                    summary_parts.append("daily")
                elif len(weekday_names) == 5 and all(day < 5 for day in schedule.weekdays):
                    summary_parts.append("weekdays")
                elif len(weekday_names) == 2 and all(day >= 5 for day in schedule.weekdays):
                    summary_parts.append("weekends")
                else:
                    summary_parts.append(f"on {', '.join(weekday_names)}")

        summary = f"Schedule: {' '.join(summary_parts)}"
        if hasattr(schedule, 'trigger') and schedule.trigger:
            summary += f" for {schedule.trigger.canvas.name}"

        # Create JSON snapshot of schedule data
        # Process weekdays for JSON storage
        weekday_names = []
        if schedule.weekdays:
            weekday_names = [self._get_weekday_name(day) for day in schedule.weekdays if 0 <= day <= 6]

        json_data = {
            'trigger_id': str(schedule.trigger_id) if schedule.trigger_id else None,
            'name': schedule.name,
            'start_time': schedule.start_time.strftime("%H:%M") if schedule.start_time else None,
            'end_time': schedule.end_time.strftime("%H:%M") if schedule.end_time else None,
            'start_hour': schedule.start_time.hour if schedule.start_time else None,
            'start_minute': schedule.start_time.minute if schedule.start_time else None,
            'weekdays': schedule.weekdays,
            'weekday_names': weekday_names,
            'time_period': self._extract_time_period(schedule.start_time) if schedule.start_time else None,
            'created_at': schedule.created_at.isoformat(),
            'updated_at': schedule.updated_at.isoformat(),
        }

        # Add trigger context if available
        if hasattr(schedule, 'trigger') and schedule.trigger:
            json_data.update({
                'canvas_id': str(schedule.trigger.canvas_id),
                'canvas_name': schedule.trigger.canvas.name,
                'location_id': str(schedule.trigger.location_id) if schedule.trigger.location_id else None,
                'location_name': None,  # Location name lookup would require separate query
                'trigger_is_active': schedule.trigger.is_active,
            })

        # Generate searchable text
        searchable_text = self._extract_schedule_text(schedule)

        return {
            'entity_type': self.get_entity_type(),
            'name': summary,
            'version': 1,  # Schedule versioning not implemented yet
            'summary': summary,
            'json_data': json_data,
            'text': searchable_text,
            'tags': self._generate_schedule_tags(schedule),
        }

    def extract_relationships(self, schedule: TriggerSchedule) -> list[tuple[str, str, str]]:
        """
        Extract relationships from TriggerSchedule.

        Relationships:
        - trigger HAS_SCHEDULE schedule (reverse handled by TriggerAdapter)

        Args:
            schedule: TriggerSchedule instance

        Returns:
            List of (subject_id, predicate, object_id) tuples
        """
        # Relationships are primarily handled by TriggerAdapter
        # This is here for completeness but typically returns empty list
        # to avoid duplicate relationships
        return []

    def _extract_schedule_text(self, schedule: TriggerSchedule) -> str:
        """
        Extract searchable text from schedule and its properties.

        Args:
            schedule: TriggerSchedule instance

        Returns:
            Concatenated searchable text
        """
        text_parts = []

        # Add schedule identifier
        text_parts.append("schedule")

        # Add schedule name
        text_parts.append(schedule.name)

        # Add time information
        if schedule.start_time:
            time_str = schedule.start_time.strftime("%H:%M")
            text_parts.append(f"time {time_str}")
            text_parts.append(str(schedule.start_time.hour))
            text_parts.append(str(schedule.start_time.minute))

            # Add time period
            time_period = self._extract_time_period(schedule.start_time)
            text_parts.append(time_period)

        if schedule.end_time:
            end_time_str = schedule.end_time.strftime("%H:%M")
            text_parts.append(f"until {end_time_str}")

        # Add weekday information
        if schedule.weekdays:
            for day in schedule.weekdays:
                if 0 <= day <= 6:
                    weekday_name = self._get_weekday_name(day)
                    text_parts.append(f"day {weekday_name}")
                    text_parts.append(weekday_name.lower())
                    text_parts.append(str(day))

        # Add trigger context if available
        if hasattr(schedule, 'trigger') and schedule.trigger:
            text_parts.append(schedule.trigger.canvas.name)
            if schedule.trigger.location_id:
                text_parts.append(f"location-{schedule.trigger.location_id}")
                text_parts.append("location")

        # Schedule model doesn't have metadata field - skipping metadata text

        # Schedule doesn't have is_active - all existing schedules are considered active
        text_parts.append("active schedule")

        return ' '.join(text_parts)

    def _generate_schedule_tags(self, schedule: TriggerSchedule) -> list[str]:
        """
        Generate tags for schedule categorization and filtering.

        Args:
            schedule: TriggerSchedule instance

        Returns:
            List of tags
        """
        tags = ['schedule']

        # Add time-based tags
        if schedule.start_time:
            time_period = self._extract_time_period(schedule.start_time)
            tags.append(f"time-{time_period}")
            tags.append(f"hour-{schedule.start_time.hour}")

            # Add broader time categories
            if schedule.start_time.hour < 12:
                tags.append('am')
            else:
                tags.append('pm')

        # Add day-based tags
        if schedule.weekdays:
            weekday_count = len(schedule.weekdays)
            if weekday_count == 7:
                tags.append('daily')
            elif weekday_count == 5 and all(day < 5 for day in schedule.weekdays):
                tags.append('weekdays')
            elif weekday_count == 2 and all(day >= 5 for day in schedule.weekdays):
                tags.append('weekend')
            else:
                # Add individual day tags
                for day in schedule.weekdays:
                    if 0 <= day <= 6:
                        weekday_name = self._get_weekday_name(day)
                        tags.append(f"day-{weekday_name.lower()}")
                        tags.append(f"dow-{day}")

                # Add broader day categories
                if any(day < 5 for day in schedule.weekdays):
                    tags.append('includes-weekday')
                if any(day >= 5 for day in schedule.weekdays):
                    tags.append('includes-weekend')

        # Schedule doesn't have is_active field - all schedules are considered active if they exist

        # Add trigger context tags if available
        if hasattr(schedule, 'trigger') and schedule.trigger:
            tags.append('trigger-linked')
            canvas_type = getattr(schedule.trigger.canvas, 'canvas_type', None)
            if canvas_type:
                tags.append(f"canvas-{canvas_type}")

            if schedule.trigger.location_id:
                tags.append('located')
                tags.append(f"location-{schedule.trigger.location_id}")
            else:
                tags.append('location-independent')
        else:
            tags.append('orphaned')

        # Schedule model doesn't have metadata field - skipping metadata tags

        # Add frequency tags (if we can infer patterns)
        # This could be extended with more sophisticated pattern detection
        tags.append('single-occurrence')  # Default, could be enhanced

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

    def sync_all_schedules(self, force_update: bool = False) -> dict[str, Any]:
        """
        Sync all schedules in project to Entity records.

        Args:
            force_update: Force update all schedules

        Returns:
            Sync statistics
        """
        # Import here to avoid circular imports
        from apps.stories.models import TriggerSchedule

        schedules = TriggerSchedule.objects.filter(
            trigger__canvas__project_id=self.project_id,
            trigger__canvas__deleted_at__isnull=True
        ).select_related('trigger__canvas')

        stats = {
            'total_schedules': schedules.count(),
            'synced_entities': 0,
            'synced_relationships': 0,
            'errors': []
        }

        logger.info(f"Syncing {stats['total_schedules']} schedules for project {self.project_id}")

        for schedule in schedules:
            try:
                result = self.full_sync(schedule, force_update=force_update)
                stats['synced_entities'] += 1
                stats['synced_relationships'] += result['relationship_count']
            except Exception as e:
                error_msg = f"Failed to sync schedule {schedule.id}: {str(e)}"
                logger.error(error_msg)
                stats['errors'].append(error_msg)

        logger.info(f"Schedule sync complete: {stats['synced_entities']}/{stats['total_schedules']} entities, "
                   f"{stats['synced_relationships']} relationships, {len(stats['errors'])} errors")

        return stats
