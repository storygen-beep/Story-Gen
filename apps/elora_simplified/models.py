"""
Elora Simplified models for AI agent memory and session management.
"""

import uuid

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from apps.common.compat import ArrayField, SearchVectorField, VectorField

from apps.authentication.models import User
from apps.projects.models import Project


class MemoryKind(models.TextChoices):
    """Types of agent memory."""
    EPISODIC = "episodic", "Episodic (user interactions)"
    SEMANTIC = "semantic", "Semantic (stable facts)"
    FEEDBACK = "feedback", "Feedback (critiques/preferences)"
    ARTIFACTS = "artifacts", "Artifacts (outlines/drafts)"


class AgentMemory(models.Model):
    """
    Agent memory storage for project-scoped context and learning.
    Simple JSON-based storage with tags for retrieval.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="agent_memories"
    )

    # Memory classification
    kind = models.CharField(max_length=20, choices=MemoryKind.choices)
    topic = models.CharField(max_length=100, help_text="Main topic/theme of memory")

    # Memory content
    text = models.TextField(help_text="Memory content/description")
    tags = models.JSONField(default=list, blank=True, help_text="Tags for retrieval")
    refs = models.JSONField(default=dict, blank=True, help_text="References to canvas/node/location IDs")

    # Memory lifecycle
    created_at = models.DateTimeField(auto_now_add=True)
    ttl_days = models.IntegerField(default=90, help_text="Time to live in days")

    class Meta:
        db_table = "elora_agent_memories"
        indexes = [
            models.Index(fields=["project", "kind", "created_at"]),
            models.Index(fields=["project", "topic"]),
            models.Index(fields=["created_at"]),  # For TTL cleanup
        ]

    def __str__(self):
        return f"{self.kind}: {self.topic} ({self.project.name})"

    def is_expired(self):
        """Check if memory has exceeded TTL."""
        if self.ttl_days <= 0:
            return False  # Never expires
        expiry_date = self.created_at + timezone.timedelta(days=self.ttl_days)
        return timezone.now() > expiry_date

    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "id": str(self.id),
            "project_id": str(self.project_id),
            "kind": self.kind,
            "topic": self.topic,
            "text": self.text,
            "tags": self.tags,
            "refs": self.refs,
            "created_at": self.created_at.isoformat(),
            "ttl_days": self.ttl_days,
            "is_expired": self.is_expired(),
        }


class AgentMode(models.TextChoices):
    """Agent operational modes."""
    THINK = "think", "Thinker Mode (brainstorm, critique, reflect)"
    DO = "do", "Doer Mode (execute tools, patch canvases)"


class AgentSession(models.Model):
    """
    Agent session tracking for conversation context and state management.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="agent_sessions"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="agent_sessions"
    )

    # Session state
    mode = models.CharField(max_length=10, choices=AgentMode.choices, default=AgentMode.THINK)
    user_goal = models.TextField(blank=True, help_text="Current user goal/objective")

    # Context tracking
    context_snippets = models.JSONField(default=list, blank=True, help_text="Retrieved context snippets")
    feedback_topics = models.JSONField(default=list, blank=True, help_text="Active feedback topics")
    last_tool = models.CharField(max_length=100, blank=True, help_text="Last tool called")

    # Session lifecycle
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "elora_agent_sessions"
        indexes = [
            models.Index(fields=["project", "user", "is_active"]),
            models.Index(fields=["is_active", "updated_at"]),
        ]

    def __str__(self):
        return f"Session {self.mode} - {self.project.name} ({self.user.email})"

    def end_session(self):
        """End the current session."""
        self.is_active = False
        self.ended_at = timezone.now()
        self.save()

    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "id": str(self.id),
            "project_id": str(self.project_id),
            "user_id": str(self.user_id),
            "mode": self.mode,
            "user_goal": self.user_goal,
            "context_snippets": self.context_snippets,
            "feedback_topics": self.feedback_topics,
            "last_tool": self.last_tool,
            "is_active": self.is_active,
            "started_at": self.started_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
        }


# Entity/Edge Model for Cross-Entity Querying


class EntityType(models.TextChoices):
    """Types of entities in the system."""
    CANVAS = "canvas", "Story Canvas"
    LOCATION = "location", "World Location"
    CHARACTER = "character", "Character"
    NPC = "npc", "Non-Player Character"
    MEMORY = "memory", "Agent Memory"
    PROJECT = "project", "Project"
    TRIGGER = "trigger", "Canvas Trigger"
    SCHEDULE = "schedule", "Trigger Schedule"


class Entity(models.Model):
    """
    Universal entity model for cross-entity querying and relationships.

    Following Section 11 of elora_agent_doc.md - Entity-agnostic storage
    with denormalized snapshots for search and relationship traversal.
    """

    entity_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity_type = models.CharField(max_length=50, choices=EntityType.choices)

    # Basic identification
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="entities"
    )

    # Versioning and content
    version = models.IntegerField(default=1)
    summary = models.TextField(blank=True, help_text="Short description for display")
    json_data = models.JSONField(default=dict, blank=True, help_text="Denormalized snapshot for search")
    text = models.TextField(blank=True, help_text="Searchable text concatenation")
    tags = ArrayField(
        models.CharField(max_length=100),
        default=list,
        blank=True,
        help_text="Tags for filtering and search"
    )

    # Hybrid Search Fields
    search_vector = SearchVectorField(null=True, blank=True, help_text="PostgreSQL tsvector for BM25 full-text search")
    embedding = VectorField(
        dimensions=1536,  # OpenAI text-embedding-3-small dimension
        null=True,
        blank=True,
        help_text="OpenAI semantic embedding vector for similarity search"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "elora_entities"
        indexes = [
            # Core query patterns
            models.Index(fields=["project", "entity_type"]),
            models.Index(fields=["project", "slug"]),
            models.Index(fields=["project", "entity_type", "name"]),
            # Search patterns
            models.Index(fields=["project", "entity_type", "updated_at"]),
            # Tag-based filtering (GIN index for array contains)
            # Note: GIN index on tags would be added via raw SQL in migration
            # Hybrid search indexes (specialized indexes added via raw SQL in migration):
            # - GIN index on search_vector for BM25 full-text search
            # - HNSW index on embedding for vector similarity search
        ]
        unique_together = [["project", "entity_type", "slug"]]

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            # Ensure unique slug within project and entity_type
            while Entity.objects.filter(
                project=self.project,
                entity_type=self.entity_type,
                slug=slug
            ).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.entity_type}: {self.name} ({self.project.name})"

    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "entity_id": str(self.entity_id),
            "entity_type": self.entity_type,
            "name": self.name,
            "slug": self.slug,
            "project_id": str(self.project_id),
            "version": self.version,
            "summary": self.summary,
            "json_data": self.json_data,
            "text": self.text,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class Predicate(models.TextChoices):
    """Relationship predicates between entities."""
    USES_LOCATION = "USES_LOCATION", "Uses Location"
    HAS_CHARACTER = "HAS_CHARACTER", "Has Character"
    LINKS_TO = "LINKS_TO", "Links To"
    TRIGGERS = "TRIGGERS", "Triggers"
    BELONGS_TO = "BELONGS_TO", "Belongs To"
    DERIVES_FROM = "DERIVES_FROM", "Derives From"
    MENTIONS = "MENTIONS", "Mentions"
    CONTAINS = "CONTAINS", "Contains"
    HAS_TRIGGER = "HAS_TRIGGER", "Has Trigger"
    LOCATED_AT = "LOCATED_AT", "Located At"
    HAS_SCHEDULE = "HAS_SCHEDULE", "Has Schedule"


class Edge(models.Model):
    """
    Typed relationships between entities.

    Enables graph-aware retrieval and cross-entity queries like:
    "Show canvases that use Kitchen location" or
    "Find characters in canvases within Entrance Hall"
    """

    edge_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relationship triple: subject -> predicate -> object
    subject = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="outgoing_edges"
    )
    predicate = models.CharField(max_length=100, choices=Predicate.choices)
    object = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="incoming_edges"
    )

    # Scoping and metadata
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="edges"
    )
    weight = models.FloatField(default=1.0, help_text="Relationship strength/importance")
    evidence = models.JSONField(
        default=dict,
        blank=True,
        help_text="Evidence of relationship (field path, text span, etc.)"
    )

    # Versioning support
    version_range = ArrayField(
        models.CharField(max_length=20),
        default=list,
        blank=True,
        help_text="Version range where this relationship applies"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "elora_edges"
        indexes = [
            # Forward traversal (subject -> predicate -> object)
            models.Index(fields=["subject", "predicate"]),
            # Reverse traversal (object <- predicate <- subject)
            models.Index(fields=["object", "predicate"]),
            # Project scoped queries
            models.Index(fields=["project", "predicate"]),
            # Query by predicate type
            models.Index(fields=["predicate", "project"]),
        ]
        unique_together = [["subject", "predicate", "object"]]  # Prevent duplicate edges

    def __str__(self):
        return f"{self.subject.name} {self.predicate} {self.object.name}"

    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "edge_id": str(self.edge_id),
            "subject": {
                "entity_id": str(self.subject.entity_id),
                "name": self.subject.name,
                "entity_type": self.subject.entity_type,
            },
            "predicate": self.predicate,
            "object": {
                "entity_id": str(self.object.entity_id),
                "name": self.object.name,
                "entity_type": self.object.entity_type,
            },
            "project_id": str(self.project_id),
            "weight": self.weight,
            "evidence": self.evidence,
            "version_range": self.version_range,
            "created_at": self.created_at.isoformat(),
        }
