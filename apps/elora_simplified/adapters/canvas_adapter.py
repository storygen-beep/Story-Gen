"""
Canvas adapter for converting StoryCanvas objects to Entity/Edge records.

Implements the entity-agnostic vision by converting story canvas domain objects
into searchable Entity records with relationships stored as Edge records.
"""

import logging
from typing import Any

from apps.stories.models import StoryCanvas

from ..models import EntityType, Predicate
from .base import BaseAdapter

logger = logging.getLogger(__name__)


class CanvasAdapter(BaseAdapter):
    """
    Adapter for converting StoryCanvas objects to Entity/Edge records.

    Extracts canvas content, metadata, and relationships (canvas->location)
    into the entity-agnostic storage format.
    """

    def get_entity_type(self) -> EntityType:
        """Canvas entities use 'canvas' type."""
        return EntityType.CANVAS

    def extract_entity_data(self, canvas: StoryCanvas) -> dict[str, Any]:
        """
        Extract entity data from StoryCanvas with embedded trigger/schedule data.

        Args:
            canvas: StoryCanvas instance

        Returns:
            Entity data dictionary
        """
        # Extract searchable text from nodes and trigger/schedule data
        searchable_text = self._extract_canvas_text(canvas)

        # Extract embedded trigger information for hybrid approach
        trigger_data = self._extract_embedded_trigger_data(canvas)

        # Create JSON snapshot of canvas data with embedded trigger/schedule
        json_data = {
            'canvas_type': canvas.canvas_type,
            'status': canvas.status,
            'metadata': canvas.metadata,
            'node_count': canvas.nodes.count(),
            'has_trigger': trigger_data['has_trigger'],
            'created_at': canvas.created_at.isoformat(),
            'updated_at': canvas.updated_at.isoformat(),
            # Embedded trigger/schedule data for fast queries
            'embedded_trigger': trigger_data,
        }

        return {
            'entity_type': self.get_entity_type(),
            'name': canvas.name,
            'version': 1,  # Canvas versioning not implemented yet
            'summary': canvas.description or f"{canvas.canvas_type.title()} canvas with {canvas.nodes.count()} nodes",
            'json_data': json_data,
            'text': searchable_text,
            'tags': canvas.tags or [],
        }

    def extract_relationships(self, canvas: StoryCanvas) -> list[tuple[str, str, str]]:
        """
        Extract relationships from StoryCanvas.

        Current relationships:
        - canvas USES_LOCATION location (if trigger exists)
        - canvas BELONGS_TO project (implicit via project scoping)

        Args:
            canvas: StoryCanvas instance

        Returns:
            List of (subject_id, predicate, object_id) tuples
        """
        relationships = []
        canvas_id = str(canvas.id)

        # Canvas -> Location relationship (via trigger)
        if hasattr(canvas, 'trigger') and canvas.trigger and canvas.trigger.location_id:
            location_id = str(canvas.trigger.location_id)
            relationships.append((canvas_id, Predicate.USES_LOCATION, location_id))
            logger.debug(f"Found canvas->location relationship: {canvas.name} uses {canvas.trigger.location_id}")

        # Note: BELONGS_TO project relationship is implicit via Entity.project foreign key
        # Could add explicit edge if needed: relationships.append((canvas_id, Predicate.BELONGS_TO, str(canvas.project_id)))

        return relationships

    def _extract_canvas_text(self, canvas: StoryCanvas) -> str:
        """
        Extract searchable text from canvas, nodes, and embedded trigger/schedule data.

        Args:
            canvas: StoryCanvas instance

        Returns:
            Concatenated searchable text
        """
        text_parts = []

        # Add canvas name and description
        text_parts.append(canvas.name)
        if canvas.description:
            text_parts.append(canvas.description)

        # Add node content
        for node in canvas.nodes.all():
            if node.name:
                text_parts.append(node.name)

            # Extract content from BlockNote format
            if node.node_data and isinstance(node.node_data, dict):
                blocks = node.node_data.get('blocks', [])
                for block in blocks:
                    content = block.get('content', '').strip()
                    if content:
                        text_parts.append(content)

            # Add exit block text if present
            if node.exit_block:
                text_parts.append(str(node.exit_block))

        # Add trigger and schedule searchable text
        trigger_text = self._extract_trigger_schedule_text(canvas)
        if trigger_text:
            text_parts.append(trigger_text)

        return ' '.join(text_parts)

    def get_canvas_by_slug(self, slug: str) -> StoryCanvas:
        """
        Get StoryCanvas by slug for convenience.

        Args:
            slug: Canvas slug

        Returns:
            StoryCanvas instance
        """
        return StoryCanvas.objects.get(
            project_id=self.project_id,
            slug=slug,
            deleted_at__isnull=True
        )

    def sync_all_canvases(self, force_update: bool = False) -> dict[str, Any]:
        """
        Sync all canvases in project to Entity records.

        Args:
            force_update: Force update all canvases

        Returns:
            Sync statistics
        """
        canvases = StoryCanvas.objects.filter(
            project_id=self.project_id,
            deleted_at__isnull=True
        ).prefetch_related('nodes')

        stats = {
            'total_canvases': canvases.count(),
            'synced_entities': 0,
            'synced_relationships': 0,
            'errors': []
        }

        logger.info(f"Syncing {stats['total_canvases']} canvases for project {self.project_id}")

        for canvas in canvases:
            try:
                result = self.full_sync(canvas, force_update=force_update)
                stats['synced_entities'] += 1
                stats['synced_relationships'] += result['relationship_count']
            except Exception as e:
                error_msg = f"Failed to sync canvas {canvas.id} ({canvas.name}): {str(e)}"
                logger.error(error_msg)
                stats['errors'].append(error_msg)

        logger.info(f"Canvas sync complete: {stats['synced_entities']}/{stats['total_canvases']} entities, "
                   f"{stats['synced_relationships']} relationships, {len(stats['errors'])} errors")

        return stats

    def _extract_embedded_trigger_data(self, canvas: StoryCanvas) -> dict[str, Any]:
        """
        Extract embedded trigger/schedule data for hybrid approach.

        This provides fast access to trigger information without separate queries,
        while separate Trigger/Schedule entities enable granular queries.

        Args:
            canvas: StoryCanvas instance

        Returns:
            Embedded trigger data dictionary
        """
        trigger_data = {
            'has_trigger': False,
            'trigger_id': None,
            'is_active': False,
            'location_id': None,
            'location_name': None,
            'location_type': None,
            'trigger_condition': None,
            'schedule_count': 0,
            'schedules': [],
            'has_active_schedules': False,
            'time_periods': [],
            'weekdays': [],
            'earliest_time': None,
            'latest_time': None,
        }

        # Check if canvas has trigger
        if not (hasattr(canvas, 'trigger') and canvas.trigger):
            return trigger_data

        trigger = canvas.trigger
        trigger_data.update({
            'has_trigger': True,
            'trigger_id': str(trigger.id),
            'is_active': trigger.is_active,
            'trigger_condition': trigger.conditions,
        })

        # Add location information
        if trigger.location_id:
            trigger_data.update({
                'location_id': str(trigger.location_id),
                'location_name': None,  # Location name lookup would require separate query
                'location_type': None,  # Location type lookup would require separate query
            })

        # Add schedule information
        if hasattr(trigger, 'schedules'):
            schedules = []
            time_periods = set()
            weekdays = set()
            times = []

            for schedule in trigger.schedules.all():
                # Process weekdays array
                weekday_names = []
                if schedule.weekdays:
                    weekday_names = [self._get_weekday_name(day) for day in schedule.weekdays if 0 <= day <= 6]

                schedule_data = {
                    'id': str(schedule.id),
                    'name': schedule.name,
                    'start_time': schedule.start_time.strftime("%H:%M") if schedule.start_time else None,
                    'end_time': schedule.end_time.strftime("%H:%M") if schedule.end_time else None,
                    'weekdays': schedule.weekdays,
                    'weekday_names': weekday_names,
                    'time_period': self._extract_time_period(schedule.start_time) if schedule.start_time else None,
                }
                schedules.append(schedule_data)

                # Collect time periods and weekdays for tags
                if schedule.start_time:
                    time_period = self._extract_time_period(schedule.start_time)
                    time_periods.add(time_period)
                    times.append(schedule.start_time)

                if schedule.weekdays:
                    for day in schedule.weekdays:
                        if 0 <= day <= 6:
                            weekday_name = self._get_weekday_name(day)
                            weekdays.add(weekday_name)

            trigger_data.update({
                'schedule_count': len(schedules),
                'schedules': schedules,
                'has_active_schedules': len(schedules) > 0,  # All existing schedules are considered active
                'time_periods': list(time_periods),
                'weekdays': list(weekdays),
                'earliest_time': min(times).strftime("%H:%M") if times else None,
                'latest_time': max(times).strftime("%H:%M") if times else None,
            })

        return trigger_data

    def _extract_trigger_schedule_text(self, canvas: StoryCanvas) -> str:
        """
        Extract searchable text from trigger and schedule information.

        Args:
            canvas: StoryCanvas instance

        Returns:
            Trigger/schedule searchable text
        """
        text_parts = []

        # Check if canvas has trigger
        if not (hasattr(canvas, 'trigger') and canvas.trigger):
            return ""

        trigger = canvas.trigger

        # Add trigger-related text
        text_parts.append("trigger")
        if trigger.is_active:
            text_parts.append("active trigger")
        else:
            text_parts.append("inactive trigger")

        # Add location information
        if trigger.location_id:
            text_parts.append(f"location-{trigger.location_id}")
            text_parts.append("location")
            text_parts.append(f"located at {trigger.location_id}")

        # Add trigger condition
        if trigger.conditions:
            text_parts.append(str(trigger.conditions))

        # Add schedule information
        if hasattr(trigger, 'schedules'):
            for schedule in trigger.schedules.all():
                text_parts.append("schedule")
                text_parts.append(schedule.name)

                if schedule.start_time:
                    time_str = schedule.start_time.strftime("%H:%M")
                    text_parts.append(f"time {time_str}")
                    time_period = self._extract_time_period(schedule.start_time)
                    text_parts.append(time_period)

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

                text_parts.append("active schedule")

        return ' '.join(text_parts)

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
