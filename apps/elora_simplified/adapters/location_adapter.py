"""
Location adapter for converting Location objects to Entity/Edge records.

Implements the entity-agnostic vision by converting world location domain objects
into searchable Entity records with spatial and contextual information.
"""

import logging
from typing import Any

from django.utils.text import slugify

from apps.world.models import Location

from ..models import EntityType
from .base import BaseAdapter

logger = logging.getLogger(__name__)


class LocationAdapter(BaseAdapter):
    """
    Adapter for converting Location objects to Entity/Edge records.

    Extracts location metadata, properties, and contextual information
    into the entity-agnostic storage format for spatial queries.
    """

    def get_entity_type(self) -> EntityType:
        """Location entities use 'location' type."""
        return EntityType.LOCATION

    def extract_entity_data(self, location: Location) -> dict[str, Any]:
        """
        Extract entity data from Location.

        Args:
            location: Location instance

        Returns:
            Entity data dictionary
        """
        # Create location summary
        summary = f"{location.location_type.title()} location"
        if location.description:
            summary += f": {location.description[:100]}"
        if location.is_starting_location:
            summary += " (Starting location)"

        # Create JSON snapshot of location data
        json_data = {
            'location_type': location.location_type,
            'is_starting_location': location.is_starting_location,
            'is_accessible': location.is_accessible,
            'properties': location.properties,
            'created_at': location.created_at.isoformat(),
        }

        # Generate searchable text
        searchable_text = self._extract_location_text(location)

        return {
            'entity_type': self.get_entity_type(),
            'name': location.name,
            'version': 1,  # Location versioning not implemented yet
            'summary': summary,
            'json_data': json_data,
            'text': searchable_text,
            'tags': self._generate_location_tags(location),
        }

    def extract_relationships(self, location: Location) -> list[tuple[str, str, str]]:
        """
        Extract relationships from Location.

        Locations are typically terminal nodes in the relationship graph,
        so they don't have outgoing relationships in this implementation.

        Args:
            location: Location instance

        Returns:
            List of (subject_id, predicate, object_id) tuples (empty for locations)
        """
        # Locations are terminal nodes - triggers and canvases point TO them
        # No outgoing relationships needed
        return []

    def _extract_location_text(self, location: Location) -> str:
        """
        Extract searchable text from location and its properties.

        Args:
            location: Location instance

        Returns:
            Concatenated searchable text
        """
        text_parts = []

        # Add location name and description
        text_parts.append(location.name)
        if location.description:
            text_parts.append(location.description)

        # Add location type
        text_parts.append(location.location_type)

        # Add properties text if available
        if location.properties and isinstance(location.properties, dict):
            for key, value in location.properties.items():
                if isinstance(value, str):
                    text_parts.append(f"{key}: {value}")
                elif isinstance(value, (list, tuple)):
                    text_parts.extend([str(v) for v in value if isinstance(v, str)])

        # Add contextual keywords
        if location.is_starting_location:
            text_parts.append("starting location home beginning")
        if location.is_accessible:
            text_parts.append("accessible available")
        else:
            text_parts.append("inaccessible locked")

        return ' '.join(text_parts)

    def _generate_location_tags(self, location: Location) -> list[str]:
        """
        Generate tags for location categorization and filtering.

        Args:
            location: Location instance

        Returns:
            List of tags
        """
        tags = ['location']

        # Add location type
        tags.append(location.location_type)

        # Add accessibility tags
        if location.is_accessible:
            tags.append('accessible')
        else:
            tags.append('inaccessible')

        # Add special flags
        if location.is_starting_location:
            tags.append('starting-location')

        # Add property-based tags
        if location.properties and isinstance(location.properties, dict):
            for key, value in location.properties.items():
                # Add property keys as tags
                tag = slugify(key)
                if tag:
                    tags.append(f"prop-{tag}")

        return tags

    def sync_all_locations(self, force_update: bool = False) -> dict[str, Any]:
        """
        Sync all locations in project to Entity records.

        Args:
            force_update: Force update all locations

        Returns:
            Sync statistics
        """
        locations = Location.objects.filter(project_id=self.project_id)

        stats = {
            'total_locations': locations.count(),
            'synced_entities': 0,
            'synced_relationships': 0,
            'errors': []
        }

        logger.info(f"Syncing {stats['total_locations']} locations for project {self.project_id}")

        for location in locations:
            try:
                result = self.full_sync(location, force_update=force_update)
                stats['synced_entities'] += 1
                stats['synced_relationships'] += result['relationship_count']
            except Exception as e:
                error_msg = f"Failed to sync location {location.id} ({location.name}): {str(e)}"
                logger.error(error_msg)
                stats['errors'].append(error_msg)

        logger.info(f"Location sync complete: {stats['synced_entities']}/{stats['total_locations']} entities, "
                   f"{stats['synced_relationships']} relationships, {len(stats['errors'])} errors")

        return stats
