"""
Testing settings for story_gen_django project.
"""

from .base import *

# Testing-specific settings
DEBUG = False

ALLOWED_HOSTS = ["testserver"]

# Use in-memory database for faster tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}


# Disable migrations during tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

# Password hashers - Use MD5 for faster tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Cache - Use dummy cache for tests
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Email backend for tests
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Media files - Use temporary directory
import tempfile

MEDIA_ROOT = tempfile.mkdtemp()

# Ensure tests use local filesystem storage to avoid network and keep isolation
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# Logging - Suppress logs during tests
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "root": {
        "handlers": ["null"],
    },
    "loggers": {
        "django": {
            "handlers": ["null"],
            "propagate": False,
        },
        "apps": {
            "handlers": ["null"],
            "propagate": False,
        },
    },
}

# JWT - Shorter lifetime for tests
from datetime import timedelta

SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(minutes=5)
SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"] = timedelta(minutes=30)
