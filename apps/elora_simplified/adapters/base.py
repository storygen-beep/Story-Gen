"""
Base adapter pattern for converting domain objects to Entity/Edge records.

Provides the foundation for all domain-specific adapters following the
entity-agnostic architecture.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any

from django.db import transaction

from ..models import EntityType
from ..services.edge_service import EdgeService
from ..services.embedding_service import embedding_service
from ..services.entity_service import EntityService

logger = logging.getLogger(__name__)


class BaseAdapter(ABC):
    """
    Base adapter for converting domain objects to Entity/Edge records.

    Follows the entity-agnostic pattern where all domain knowledge is
    contained within adapters, while Entity/Edge models remain generic.
    """

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.entity_service = EntityService(project_id)
        self.edge_service = EdgeService(project_id)

    @abstractmethod
    def get_entity_type(self) -> EntityType:
        """Return the EntityType for this adapter."""
        pass

    @abstractmethod
    def extract_entity_data(self, domain_obj: Any) -> dict[str, Any]:
        """
        Extract entity data from domain object.

        Args:
            domain_obj: Domain object (Canvas, Location, etc.)

        Returns:
            Entity data dictionary for creation/update
        """
        pass

    @abstractmethod
    def extract_relationships(self, domain_obj: Any) -> list[tuple[str, str, str]]:
        """
        Extract relationships from domain object.

        Args:
            domain_obj: Domain object

        Returns:
            List of (subject_id, predicate, object_id) tuples
        """
        pass

    @transaction.atomic
    def sync_entity(self, domain_obj: Any, force_update: bool = False) -> dict[str, Any]:
        """
        Sync domain object to Entity record.

        Args:
            domain_obj: Domain object to sync
            force_update: Force update even if version hasn't changed

        Returns:
            Entity dictionary
        """
        entity_data = self.extract_entity_data(domain_obj)
        domain_id = str(domain_obj.id)

        # Generate hybrid search fields
        entity_data = self._enhance_with_search_fields(entity_data)

        # Check if entity exists
        existing_entity = self.entity_service.get_by_id(domain_id)

        if existing_entity and not force_update:
            # Check if update needed based on version or updated_at
            if self._needs_update(existing_entity, entity_data):
                logger.info(f"Updating entity {domain_id} ({self.get_entity_type()})")
                return self.entity_service.update_entity(domain_id, entity_data)
            else:
                logger.debug(f"Entity {domain_id} is up to date")
                return existing_entity
        elif existing_entity and force_update:
            logger.info(f"Force updating entity {domain_id} ({self.get_entity_type()})")
            return self.entity_service.update_entity(domain_id, entity_data)
        else:
            # Create new entity with explicit ID
            entity_data['entity_id'] = domain_id
            logger.info(f"Creating new entity {domain_id} ({self.get_entity_type()})")
            return self.entity_service.create_entity(entity_data)

    @transaction.atomic
    def sync_relationships(self, domain_obj: Any) -> list[dict[str, Any]]:
        """
        Sync relationships for domain object.

        Args:
            domain_obj: Domain object

        Returns:
            List of created/updated edge dictionaries
        """
        domain_id = str(domain_obj.id)
        relationships = self.extract_relationships(domain_obj)

        # Clean existing relationships for this entity
        self.edge_service.delete_edges(subject_id=domain_id)

        # Create new relationships
        created_edges = []
        for subject_id, predicate, object_id in relationships:
            try:
                edge_data = {
                    'subject_id': subject_id,
                    'predicate': predicate,
                    'object_id': object_id,
                    'weight': 1.0,
                    'evidence': {
                        'adapter': self.__class__.__name__,
                        'extracted_at': domain_obj.updated_at.isoformat() if hasattr(domain_obj, 'updated_at') else None
                    }
                }
                edge = self.edge_service.create_edge(edge_data)
                created_edges.append(edge)
                logger.debug(f"Created relationship: {subject_id} {predicate} {object_id}")
            except Exception as e:
                logger.warning(f"Failed to create relationship {subject_id} {predicate} {object_id}: {e}")

        logger.info(f"Synced {len(created_edges)} relationships for entity {domain_id}")
        return created_edges

    def _needs_update(self, existing_entity: dict[str, Any], new_entity_data: dict[str, Any]) -> bool:
        """
        Check if entity needs updating based on version or timestamps.

        Args:
            existing_entity: Current entity data
            new_entity_data: New entity data

        Returns:
            True if update needed
        """
        # Simple version-based checking - can be enhanced
        existing_version = existing_entity.get('version', 1)
        new_version = new_entity_data.get('version', 1)

        return new_version > existing_version

    def _enhance_with_search_fields(self, entity_data: dict[str, Any]) -> dict[str, Any]:
        """
        Enhance entity data with search vector and embedding fields.

        Args:
            entity_data: Entity data dictionary

        Returns:
            Enhanced entity data with search fields
        """
        try:
            # Extract searchable text content
            searchable_text = self._extract_searchable_text(entity_data)

            if searchable_text:
                # Generate embedding for semantic search
                try:
                    embedding = embedding_service.generate_embedding(searchable_text)
                    entity_data['embedding'] = embedding
                    logger.debug(f"Generated embedding for entity ({len(embedding)} dimensions)")
                except Exception as e:
                    logger.warning(f"Failed to generate embedding: {e}")
                    entity_data['embedding'] = None

                # Generate search vector for BM25 full-text search
                try:
                    # SearchVector will be generated by the database on save
                    # We set it to None here and let the database trigger handle it
                    entity_data['search_vector'] = None
                    logger.debug("Search vector will be generated by database trigger")
                except Exception as e:
                    logger.warning(f"Failed to set search vector: {e}")
                    entity_data['search_vector'] = None
            else:
                entity_data['embedding'] = None
                entity_data['search_vector'] = None

        except Exception as e:
            logger.error(f"Failed to enhance entity with search fields: {e}")
            entity_data['embedding'] = None
            entity_data['search_vector'] = None

        return entity_data

    def _extract_searchable_text(self, entity_data: dict[str, Any]) -> str:
        """
        Extract searchable text content from entity data.

        Args:
            entity_data: Entity data dictionary

        Returns:
            Combined searchable text content
        """
        text_parts = []

        # Add name (usually the most important)
        if entity_data.get('name'):
            text_parts.append(entity_data['name'])

        # Add summary if available
        if entity_data.get('summary'):
            text_parts.append(entity_data['summary'])

        # Add main text content
        if entity_data.get('text'):
            text_parts.append(entity_data['text'])

        # Add tags as text
        if entity_data.get('tags') and isinstance(entity_data['tags'], list):
            text_parts.extend(entity_data['tags'])

        # Combine all parts
        searchable_text = ' '.join(filter(None, text_parts))
        return searchable_text.strip()

    @transaction.atomic
    def full_sync(self, domain_obj: Any, force_update: bool = False) -> dict[str, Any]:
        """
        Complete sync of entity and relationships.

        Args:
            domain_obj: Domain object
            force_update: Force update even if version hasn't changed

        Returns:
            Dictionary with entity and relationship sync results
        """
        logger.info(f"Full sync for {self.get_entity_type()} {domain_obj.id}")

        # Sync entity first
        entity = self.sync_entity(domain_obj, force_update=force_update)

        # Then sync relationships
        relationships = self.sync_relationships(domain_obj)

        return {
            'entity': entity,
            'relationships': relationships,
            'relationship_count': len(relationships)
        }
