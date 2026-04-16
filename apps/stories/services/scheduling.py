"""
Service layer for trigger scheduling functionality.
Handles business logic for creating, managing, and evaluating trigger schedules.
"""

import uuid
from datetime import datetime, time, timedelta
from typing import Any, Optional
import copy

from django.core.exceptions import ValidationError
from django.db.models import Q

from apps.stories.models import CanvasTrigger, TriggerSchedule


class TriggerScheduleService:
    """Business logic for trigger scheduling operations"""

    @staticmethod
    def create_schedule(trigger: CanvasTrigger, schedule_data: dict) -> TriggerSchedule:
        """
        Create a new schedule for a trigger.

        Args:
            trigger: The CanvasTrigger to schedule
            schedule_data: Dictionary containing schedule parameters

        Returns:
            Created TriggerSchedule instance

        Raises:
            ValidationError: If schedule data is invalid
        """
        # Validate schedule data
        validated_data = TriggerScheduleService.validate_schedule_data(schedule_data)

        # Create the schedule
        schedule = TriggerSchedule.objects.create(
            trigger=trigger,
            **validated_data
        )

        return schedule

    @staticmethod
    def get_active_triggers_at(current_weekday: int, current_time: time) -> list[CanvasTrigger]:
        """
        Get all triggers that should be active at the specified time.

        Args:
            current_weekday: Day of week (0=Monday, 6=Sunday)
            current_time: Time of day

        Returns:
            List of CanvasTrigger instances that should be active
        """
        # Find schedules that match the current time
        matching_schedules = TriggerSchedule.objects.filter(
            weekdays__contains=[current_weekday],
            start_time__lte=current_time,
            trigger__is_active=True
        ).filter(
            Q(end_time__isnull=True) |  # Point triggers
            Q(end_time__gte=current_time)  # Range triggers
        ).select_related('trigger')

        # Return the triggers
        return [schedule.trigger for schedule in matching_schedules]

    @staticmethod
    def get_triggers_for_timespan(start_time: time, end_time: time, weekday: int) -> list[CanvasTrigger]:
        """
        Get all triggers active during a specific time span on a given weekday.

        Args:
            start_time: Start of time range
            end_time: End of time range
            weekday: Day of week (0=Monday, 6=Sunday)

        Returns:
            List of CanvasTrigger instances active during the timespan
        """
        # Find overlapping schedules
        matching_schedules = TriggerSchedule.objects.filter(
            weekdays__contains=[weekday],
            trigger__is_active=True
        ).filter(
            # Schedule starts before timespan ends AND
            # (Schedule has no end time OR schedule ends after timespan starts)
            start_time__lt=end_time
        ).filter(
            Q(end_time__isnull=True, start_time__gte=start_time) |  # Point triggers in range
            Q(end_time__gt=start_time)  # Range triggers that overlap
        ).select_related('trigger')

        return [schedule.trigger for schedule in matching_schedules]

    @staticmethod
    def get_next_trigger_time(trigger_id: uuid.UUID, after_time: datetime) -> Optional[datetime]:
        """
        Calculate the next time a trigger will fire after the specified datetime.

        Args:
            trigger_id: UUID of the trigger
            after_time: Calculate next occurrence after this time

        Returns:
            Next trigger datetime or None if no future occurrences
        """
        try:
            trigger = CanvasTrigger.objects.get(id=trigger_id, is_active=True)
        except CanvasTrigger.DoesNotExist:
            return None

        schedules = trigger.schedules.all()
        next_times = []

        current_date = after_time.date()
        current_time = after_time.time()

        # Check up to 14 days in the future
        for days_ahead in range(14):
            check_date = current_date + timedelta(days=days_ahead)
            check_weekday = check_date.weekday()  # 0=Monday

            for schedule in schedules:
                if check_weekday in schedule.weekdays:
                    # For current day, only consider times after current time
                    if days_ahead == 0 and schedule.start_time <= current_time:
                        continue

                    next_datetime = datetime.combine(check_date, schedule.start_time)
                    next_times.append(next_datetime)

        return min(next_times) if next_times else None

    @staticmethod
    def validate_schedule_data(schedule_data: dict) -> dict:
        """
        Validate and clean schedule data.

        Args:
            schedule_data: Raw schedule data dictionary

        Returns:
            Validated and cleaned schedule data

        Raises:
            ValidationError: If data is invalid
        """
        # Work on a copy to avoid mutating caller-provided data (important for agent tool args)
        data = copy.deepcopy(schedule_data) if isinstance(schedule_data, dict) else {}
        errors = {}

        # Required fields
        required_fields = ['name', 'weekdays', 'start_time']
        for field in required_fields:
            if field not in data:
                errors[field] = f"{field} is required"

        # Validate weekdays
        if 'weekdays' in data:
            weekdays = data['weekdays']
            if not isinstance(weekdays, list) or not weekdays:
                errors['weekdays'] = "weekdays must be a non-empty list"
            elif not all(isinstance(day, int) and 0 <= day <= 6 for day in weekdays):
                errors['weekdays'] = "weekdays must contain integers between 0-6 (0=Monday, 6=Sunday)"

        # Validate time fields
        for time_field in ['start_time', 'end_time']:
            if time_field in data and data[time_field] is not None:
                time_value = data[time_field]
                if isinstance(time_value, str):
                    try:
                        # Convert string to time object
                        data[time_field] = datetime.strptime(time_value, '%H:%M').time()
                    except ValueError:
                        errors[time_field] = f"{time_field} must be in HH:MM format"
                elif not isinstance(time_value, time):
                    errors[time_field] = f"{time_field} must be a time object or HH:MM string"

        # Validate time range
        if 'start_time' in data and 'end_time' in data:
            start = data.get('start_time')
            end = data.get('end_time')
            if end is not None and start and end <= start:
                errors['end_time'] = "end_time must be after start_time"

        if errors:
            raise ValidationError(errors)

        return data

    @staticmethod
    def get_schedule_conflicts(trigger_id: uuid.UUID) -> list[dict[str, Any]]:
        """
        Check for scheduling conflicts with other triggers.

        Args:
            trigger_id: UUID of the trigger to check

        Returns:
            List of conflict descriptions
        """
        conflicts = []

        try:
            trigger = CanvasTrigger.objects.get(id=trigger_id)
            schedules = trigger.schedules.all()

            for schedule in schedules:
                # Find overlapping schedules from other triggers
                overlapping = TriggerSchedule.objects.filter(
                    weekdays__overlap=schedule.weekdays,
                    start_time__lt=(schedule.end_time or schedule.start_time),
                    trigger__canvas=trigger.canvas
                ).filter(
                    Q(end_time__isnull=True, start_time__gte=schedule.start_time) |
                    Q(end_time__gt=schedule.start_time)
                ).exclude(trigger=trigger).select_related('trigger__canvas')

                for conflict_schedule in overlapping:
                    conflicts.append({
                        'schedule_id': str(schedule.id),
                        'schedule_name': schedule.name,
                        'conflicting_schedule_id': str(conflict_schedule.id),
                        'conflicting_schedule_name': conflict_schedule.name,
                        'conflicting_trigger_name': conflict_schedule.trigger.canvas.name,
                        'weekdays': list(set(schedule.weekdays) & set(conflict_schedule.weekdays)),
                        'time_overlap': f"{max(schedule.start_time, conflict_schedule.start_time)} - {min(schedule.end_time or schedule.start_time, conflict_schedule.end_time or conflict_schedule.start_time)}"
                    })

        except CanvasTrigger.DoesNotExist:
            pass

        return conflicts

    @staticmethod
    def update_schedule(schedule_id: uuid.UUID, update_data: dict) -> TriggerSchedule:
        """
        Update an existing schedule.

        Args:
            schedule_id: UUID of the schedule to update
            update_data: Dictionary of fields to update

        Returns:
            Updated TriggerSchedule instance

        Raises:
            ValidationError: If update data is invalid
            TriggerSchedule.DoesNotExist: If schedule not found
        """
        schedule = TriggerSchedule.objects.get(id=schedule_id)

        # Validate update data
        validated_data = TriggerScheduleService.validate_schedule_data(update_data)

        # Update fields
        for field, value in validated_data.items():
            setattr(schedule, field, value)

        schedule.save()
        return schedule

    @staticmethod
    def delete_schedule(schedule_id: uuid.UUID) -> bool:
        """
        Delete a schedule.

        Args:
            schedule_id: UUID of the schedule to delete

        Returns:
            True if deleted successfully
        """
        try:
            schedule = TriggerSchedule.objects.get(id=schedule_id)
            schedule.delete()
            return True
        except TriggerSchedule.DoesNotExist:
            return False

    @staticmethod
    def get_trigger_schedules(trigger_id: uuid.UUID) -> list[TriggerSchedule]:
        """
        Get all schedules for a specific trigger.

        Args:
            trigger_id: UUID of the trigger

        Returns:
            List of TriggerSchedule instances
        """
        return list(TriggerSchedule.objects.filter(trigger_id=trigger_id).order_by('start_time'))

    @staticmethod
    def preview_trigger_schedule(schedule_id: uuid.UUID, days_ahead: int = 7) -> list[dict[str, Any]]:
        """
        Preview when a trigger will fire over the next N days.

        Args:
            schedule_id: UUID of the schedule to preview
            days_ahead: Number of days to preview (default: 7)

        Returns:
            List of trigger times with metadata
        """
        try:
            schedule = TriggerSchedule.objects.get(id=schedule_id)
        except TriggerSchedule.DoesNotExist:
            return []

        preview_times = []
        today = datetime.now().date()

        for days in range(days_ahead):
            check_date = today + timedelta(days=days)
            check_weekday = check_date.weekday()

            if check_weekday in schedule.weekdays:
                trigger_datetime = datetime.combine(check_date, schedule.start_time)
                preview_times.append({
                    'date': check_date.isoformat(),
                    'weekday': check_weekday,
                    'weekday_name': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][check_weekday],
                    'start_time': schedule.start_time.strftime('%H:%M'),
                    'end_time': schedule.end_time.strftime('%H:%M') if schedule.end_time else None,
                    'trigger_datetime': trigger_datetime.isoformat()
                })

        return preview_times

    @staticmethod
    def create_multiple_schedules(trigger_id: uuid.UUID, schedules_data: list[dict]) -> list[TriggerSchedule]:
        """
        Create multiple schedules for a trigger in a single operation.

        Args:
            trigger_id: UUID of the trigger
            schedules_data: List of schedule data dictionaries

        Returns:
            List of created TriggerSchedule instances

        Raises:
            ValidationError: If any schedule data is invalid
            CanvasTrigger.DoesNotExist: If trigger not found
        """
        trigger = CanvasTrigger.objects.get(id=trigger_id)
        created_schedules = []

        for schedule_data in schedules_data:
            schedule = TriggerScheduleService.create_schedule(trigger, schedule_data)
            created_schedules.append(schedule)

        return created_schedules
