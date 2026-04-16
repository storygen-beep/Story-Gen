"""Custom User model for authentication."""

import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserRole(models.TextChoices):
    """User role choices."""

    ADMIN = "admin", "Admin"
    CREATOR = "creator", "Creator"
    COLLABORATOR = "collaborator", "Collaborator"
    VIEWER = "viewer", "Viewer"


class UserStatus(models.TextChoices):
    """User status choices."""

    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    SUSPENDED = "suspended", "Suspended"
    PENDING = "pending", "Pending"


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)

        # Generate username if not provided
        if "username" not in extra_fields or not extra_fields["username"]:
            base_username = email.split("@")[0]
            counter = 1
            username = base_username
            while self.model.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"
                counter += 1
            extra_fields["username"] = username

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", UserRole.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model with enhanced fields for compatibility with FastAPI."""

    # Use UUID for compatibility with FastAPI
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Override email to be required and unique
    email = models.EmailField(unique=True)

    # Make username optional but unique when provided
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)

    # Profile fields to match FastAPI
    full_name = models.CharField(max_length=255, null=True, blank=True)
    avatar_url = models.URLField(max_length=500, null=True, blank=True)

    # Role and status
    role = models.CharField(
        max_length=20, choices=UserRole.choices, default=UserRole.CREATOR
    )
    status = models.CharField(
        max_length=20, choices=UserStatus.choices, default=UserStatus.ACTIVE
    )

    # Verification status
    is_verified = models.BooleanField(default=False)

    # OAuth fields for future use
    oauth_provider = models.CharField(max_length=50, null=True, blank=True)
    oauth_id = models.CharField(max_length=255, null=True, blank=True)

    # Track last login for API compatibility
    last_login_at = models.DateTimeField(null=True, blank=True)

    # Use email as the username field for authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (
        []
    )  # Remove email from required fields since it's the USERNAME_FIELD

    # Use custom manager
    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def save(self, *args, **kwargs):
        """Override save to handle username generation."""
        if not self.username and self.email:
            # Generate username from email if not provided
            base_username = self.email.split("@")[0]
            counter = 1
            username = base_username
            while User.objects.filter(username=username).exclude(pk=self.pk).exists():
                username = f"{base_username}_{counter}"
                counter += 1
            self.username = username
        super().save(*args, **kwargs)

    def update_last_login(self):
        """Update last login timestamp."""
        self.last_login_at = timezone.now()
        self.save(update_fields=["last_login_at"])

    def to_dict(self):
        """Convert user to dictionary for API response compatibility."""
        return {
            "id": str(self.id),  # Convert UUID to string
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "avatar_url": self.avatar_url,
            "role": self.role,
            "status": self.status,
            "is_verified": self.is_verified,
            "display_name": self.full_name or self.username or self.email.split("@")[0],
            "created_at": self.date_joined.isoformat() if self.date_joined else None,
            "last_login_at": self.last_login_at.isoformat()
            if self.last_login_at
            else None,
        }

    @property
    def is_active_status(self):
        """Check if user has active status."""
        return self.status == UserStatus.ACTIVE

    def __str__(self):
        return self.email
