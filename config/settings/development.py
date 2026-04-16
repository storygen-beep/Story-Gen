"""
Development settings for story_gen_django project.
"""

from .base import *

# Development-specific settings
DEBUG = True

ALLOWED_HOSTS = ["*", "13.200.228.229"]

# Development-specific apps (install later)
# INSTALLED_APPS += [
#     'debug_toolbar',
#     'django_extensions',
# ]

# Development-specific middleware (install later)
# MIDDLEWARE += [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# ]

# Database
DATABASES["default"]["NAME"] = config("DB_NAME", default="story_gen_django_dev")

# Debug Toolbar Configuration
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

# CORS - More permissive for development
CORS_ALLOW_ALL_ORIGINS = True

# Email backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Logging - Normal level for development
LOGGING["handlers"]["console"]["level"] = "INFO"
LOGGING["loggers"]["django"]["level"] = "INFO"
LOGGING["loggers"]["apps"]["level"] = "INFO"

# Cache - Use dummy cache for development
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# File upload settings for development
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
