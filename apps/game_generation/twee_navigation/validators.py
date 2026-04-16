"""
Twee Navigation System Validators.

Validation logic specific to navigation game generation.
"""

from typing import Any

from apps.projects.models import Project
from apps.world.models import Location


class NavigationValidator:
    """Validator for navigation game requirements."""

    @staticmethod
    def validate_locations(project: Project) -> dict[str, Any]:
        """
        Validate location setup for navigation game.

        Returns:
            Dict with validation results
        """
        result = {"is_valid": True, "errors": [], "warnings": [], "stats": {}}

        locations = list(Location.objects.filter(project=project).prefetch_related('entry_connections'))

        # Compute connection stats from entry/exit fields
        connection_count = 0
        connected_locations = set()
        for loc in locations:
            entries = list(loc.entry_connections.all())
            connection_count += len(entries)
            if entries:
                connected_locations.add(loc.id)
            for e in entries:
                connected_locations.add(e.id)
            if getattr(loc, 'exit_connection', None):
                connected_locations.add(loc.id)
                connected_locations.add(loc.exit_connection_id)

        result["stats"]["location_count"] = len(locations)
        result["stats"]["connection_count"] = connection_count

        # Check for minimum locations
        if locations.count() == 0:
            result["is_valid"] = False
            result["errors"].append("No locations found in project")
            return result

        # Check for orphaned locations
        connected_locations = set()
        for location in locations:
            if location.id not in connected_locations and len(locations) > 1:
                result["warnings"].append(
                    f"Location '{location.name}' has no connections"
                )

        # Check for starting location
        starting_locations = [
            loc for loc in locations if getattr(loc, "is_starting_location", False)
        ]
        if not starting_locations:
            result["warnings"].append(
                "No starting location defined, will use first location"
            )
        elif len(starting_locations) > 1:
            result["warnings"].append(
                "Multiple starting locations found, will use first one"
            )

        return result

    @staticmethod
    def validate_connections(project: Project) -> dict[str, Any]:
        """
        Validate connection setup for navigation game.

        Returns:
            Dict with validation results
        """
        result = {"is_valid": True, "errors": [], "warnings": []}

        locations = list(Location.objects.filter(project=project).prefetch_related('entry_connections'))
        # Validate entries and exits
        for loc in locations:
            for entry in loc.entry_connections.all():
                if entry.id == loc.id:
                    result["warnings"].append(
                        f"Entry connection from location to itself: {loc.id}"
                    )
            if getattr(loc, 'exit_connection_id', None) == loc.id:
                result["warnings"].append(
                    f"Exit connection from location to itself: {loc.id}"
                )

        return result
