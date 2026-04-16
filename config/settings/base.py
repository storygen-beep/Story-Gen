"""
Base Django settings for story_gen_django project.
This file contains settings common to all environments.
"""

from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security
SECRET_KEY = config(
    "SECRET_KEY", default="django-insecure-development-key-change-in-production"
)
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = ["*"]

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
]

LOCAL_APPS = [
    "apps.authentication",
    "apps.projects",
    "apps.world",
    "apps.stories",
    "apps.characters",
    "apps.npcs",
    "apps.worlds",
    "apps.common",
    "apps.game_generation",
    "apps.ai_tools",
    "apps.elora_simplified",
    "apps.assets",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# URL Configuration - Disable slash appending for FastAPI compatibility
APPEND_SLASH = False

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database
_db_engine = config("DB_ENGINE", default="django.db.backends.postgresql")
_is_sqlite = "sqlite" in _db_engine

if _is_sqlite:
    DATABASES = {
        "default": {
            "ENGINE": _db_engine,
            "NAME": BASE_DIR / config("DB_NAME", default="db.sqlite3"),
        }
    }
else:
    _db_options: dict[str, object] = {"connect_timeout": 10}
    _db_sslmode = config("DB_SSLMODE", default="", cast=str).strip()
    if _db_sslmode:
        _db_options["sslmode"] = _db_sslmode
    _db_hostaddr = config("DB_HOSTADDR", default="", cast=str).strip()
    if _db_hostaddr:
        _db_options["hostaddr"] = _db_hostaddr

    DATABASES = {
        "default": {
            "ENGINE": _db_engine,
            "NAME": config("DB_NAME", default="story_gen_django"),
            "USER": config("DB_USER", default="postgres"),
            "PASSWORD": config("DB_PASSWORD", default=""),
            "HOST": config("DB_HOST", default="localhost"),
            "PORT": config("DB_PORT", default="5432"),
            "CONN_MAX_AGE": 600,
            "OPTIONS": _db_options,
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Optional: Cloudflare R2 (S3-compatible) media storage via django-storages
# Enabled when R2_ENABLED=true in environment.
R2_ENABLED = config("R2_ENABLED", default=False, cast=bool)
if R2_ENABLED:
    # Ensure django-storages is available
    INSTALLED_APPS += ["storages"]

    # Core S3 settings (Cloudflare R2 is S3-compatible)
    AWS_ACCESS_KEY_ID = config("R2_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("R2_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = config("R2_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = (
        config("R2_ENDPOINT_URL", default="")
        or f"https://{config('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com"
    )
    AWS_S3_REGION_NAME = "auto"
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_S3_ADDRESSING_STYLE = "virtual"

    # URL behavior
    # Sanitize public domain from env (allow with/without scheme)
    _raw_public = (config("R2_PUBLIC_DOMAIN", default="") or "").strip()
    AWS_S3_CUSTOM_DOMAIN = None
    if _raw_public:
        try:
            from urllib.parse import urlparse

            # If scheme missing, urlparse would put host into path; prefix '//' to parse netloc
            parsed = urlparse(
                _raw_public if "://" in _raw_public else f"//{_raw_public}", scheme=""
            )
            domain = parsed.netloc or parsed.path
            # Strip any trailing slashes
            domain = domain.rstrip("/")
            AWS_S3_CUSTOM_DOMAIN = domain or None
        except Exception:
            # Fallback to raw (best effort)
            AWS_S3_CUSTOM_DOMAIN = (
                _raw_public.lstrip("https://").lstrip("http://").rstrip("/") or None
            )
    # Force https protocol for custom domain URLs
    AWS_S3_URL_PROTOCOL = "https:"
    AWS_QUERYSTRING_AUTH = config("R2_SIGNED_URLS", default=True, cast=bool)
    # Object behavior
    AWS_DEFAULT_ACL = None
    AWS_S3_FILE_OVERWRITE = False

    # Use S3 storage backend for all FileField/ImageField
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom User Model
AUTH_USER_MODEL = "authentication.User"

# REST Framework Configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FormParser",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# JWT Configuration
from datetime import timedelta

SIMPLE_JWT = {
    # Extended token expiry times
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),  # 1 day for better UX
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # 7 days like FastAPI
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "sub",  # Match FastAPI's claim structure
    "TOKEN_TYPE_CLAIM": "token_type",
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:3000,http://127.0.0.1:3000",
    cast=lambda v: [s.strip() for s in v.split(",")],
)

CORS_ALLOW_CREDENTIALS = True

# API Documentation
SPECTACULAR_SETTINGS = {
    "TITLE": "Story Generation Platform API",
    "DESCRIPTION": "API for the Django-based story generation platform",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "django.log",
            "formatter": "verbose",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": True,
        },
        "apps": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# Create logs directory if it doesn't exist
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

OPENAI_API_KEY = config("OPENAI_API_KEY")

# Elora AI Assistant Configuration (with Pydantic validation)
ELORA_CONFIG = {
    "enabled": config("ELORA_ENABLED", default=True, cast=bool),
    "openai_api_key": config(
        "OPENAI_API_KEY",
    ),
    "model": config("ELORA_MODEL", default="gpt-4o"),
    "temperature": float(config("ELORA_TEMPERATURE", default="0.5")),
    "max_tokens": int(config("ELORA_MAX_TOKENS", default="1500")),
    "memory_token_limit": int(config("ELORA_MEMORY_TOKEN_LIMIT", default="4000")),
    "request_timeout": int(config("ELORA_REQUEST_TIMEOUT", default="30")),
    "max_iterations": int(config("ELORA_MAX_ITERATIONS", default="7")),
    "max_history": int(config("ELORA_MAX_HISTORY", default="50")),
    "session_timeout": int(config("ELORA_SESSION_TIMEOUT", default="3600")),
}

# AI Models Configuration for Elora Service
AI_MODELS = {
    "gpt-4o": {
        "provider": "openai",
        "model_name": "gpt-4o",
        "api_key": config("OPENAI_API_KEY"),
    },
    "gpt-4o-mini": {
        "provider": "openai",
        "model_name": "gpt-4o-mini",
        "api_key": config("OPENAI_API_KEY"),
    },
    "gpt-4": {
        "provider": "openai",
        "model_name": "gpt-4",
        "api_key": config("OPENAI_API_KEY"),
    },
    "gpt-3.5-turbo": {
        "provider": "openai",
        "model_name": "gpt-3.5-turbo",
        "api_key": config("OPENAI_API_KEY"),
    },
    "claude-3-sonnet": {
        "provider": "anthropic",
        "model_name": "claude-3-sonnet-20240229",
        "api_key": config("ANTHROPIC_API_KEY", default=""),
    },
    "claude-3-haiku": {
        "provider": "anthropic",
        "model_name": "claude-3-haiku-20240307",
        "api_key": config("ANTHROPIC_API_KEY", default=""),
    },
    "grok-beta": {
        "provider": "x",
        "model_name": "grok-beta",
        "api_key": config("X_API_KEY", default=""),
    },
}

# vLLM Captioning Configuration (JoyCaption server)
VLLM_CAPTIONING = {
    "enabled": config("VLLM_CAPTIONING_ENABLED", default=False, cast=bool),
    "base_url": config("VLLM_BASE_URL", default="http://joycaption:8000/v1"),
    "model": "fancyfeast/llama-joycaption-alpha-two-hf-llava",
    "api_key": "EMPTY",
    "max_tokens": config("VLLM_MAX_TOKENS", default=150, cast=int),
    "temperature": 0.6,
    "timeout": 60,
    "max_image_side": 672,
}

# Frame Extraction & Captioning Configuration
ASSET_FRAME_EXTRACTION = {
    "enabled": config("ASSET_FRAME_EXTRACTION_ENABLED", default=True, cast=bool),
    "frame_interval_sec": config("FRAME_INTERVAL_SEC", default=2.0, cast=float),
    "caption_batch_size": config("CAPTION_BATCH_SIZE", default=4, cast=int),
    "caption_timeout_sec": config("CAPTION_TIMEOUT_SEC", default=30, cast=int),
}

# Grok AI Clip Description Generation
GROK_CLIP_DESCRIPTIONS = {
    "enabled": config("GROK_CLIP_DESCRIPTIONS_ENABLED", default=False, cast=bool),
    "api_key": config("X_API_KEY", default=""),
    "api_base_url": config("GROK_API_BASE_URL", default="https://api.x.ai/v1"),
    "model": config("GROK_MODEL", default="grok-4-fast"),
    "temperature": config("GROK_TEMPERATURE", default=0.7, cast=float),
    "max_tokens": config("GROK_MAX_TOKENS", default=800, cast=int),
    "min_frames": config("GROK_MIN_FRAMES", default=3, cast=int),
    "timeout": config("GROK_TIMEOUT_SEC", default=30, cast=int),
}
