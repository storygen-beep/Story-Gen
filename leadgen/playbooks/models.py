"""Playbooks: the per-business instructions the shared engine runs on.

The playbook body is a JSON document rather than columns, so a new industry
is a new IndustryTemplate row, not a migration. Every edit creates a new
PlaybookVersion; messages record which version produced them.
"""

from django.db import models

from accounts.models import Organization, TimeStampedModel


class IndustryTemplate(TimeStampedModel):
    slug = models.SlugField(unique=True, help_text='e.g. "real_estate_dubai"')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Same shape as PlaybookVersion.content; copied into a new playbook at onboarding.
    default_content = models.JSONField(default=dict)

    def __str__(self):
        return self.name


class Playbook(TimeStampedModel):
    organization = models.OneToOneField(
        Organization, on_delete=models.CASCADE, related_name="playbook"
    )
    template = models.ForeignKey(
        IndustryTemplate, null=True, blank=True, on_delete=models.SET_NULL
    )
    current_version = models.ForeignKey(
        "PlaybookVersion", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    def __str__(self):
        return f"Playbook for {self.organization}"

    def publish(self, content, changed_by=""):
        """Save content as the next version and make it live."""
        last = self.versions.order_by("-number").first()
        version = PlaybookVersion.objects.create(
            playbook=self,
            number=(last.number + 1) if last else 1,
            content=content,
            changed_by=changed_by,
        )
        self.current_version = version
        self.save(update_fields=["current_version", "updated_at"])
        return version


class PlaybookVersion(models.Model):
    playbook = models.ForeignKey(Playbook, on_delete=models.CASCADE, related_name="versions")
    number = models.PositiveIntegerField()
    # Sections: profile, goal, questions, scoring, handoff, voice, rules, follow_up.
    content = models.JSONField()
    changed_by = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["playbook", "number"], name="unique_playbook_version")
        ]
        ordering = ["-number"]

    def __str__(self):
        return f"{self.playbook} v{self.number}"


class KnowledgeItem(TimeStampedModel):
    """The only facts the AI may state. Anything not here gets a human handoff."""

    class Kind(models.TextChoices):
        LISTING = "listing", "Listing"
        FAQ = "faq", "FAQ"
        OFFER = "offer", "Offer"

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="knowledge_items"
    )
    kind = models.CharField(max_length=16, choices=Kind.choices)
    title = models.CharField(max_length=300)
    body = models.TextField(blank=True)
    # Structured listing facts (price, bedrooms, area, portal reference) for matching.
    attributes = models.JSONField(default=dict, blank=True)
    # Portal listing reference, used to match an incoming inquiry to its listing.
    external_ref = models.CharField(max_length=100, blank=True, db_index=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.kind}] {self.title}"
