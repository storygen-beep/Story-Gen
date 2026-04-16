#!/usr/bin/env python
"""
Create a Django superuser if one doesn't exist.
"""

import os
import sys

import django

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

from django.contrib.auth import get_user_model


def create_superuser():
    """Create superuser if it doesn't exist."""
    User = get_user_model()

    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")
    username = os.environ.get(
        "DJANGO_SUPERUSER_USERNAME", None
    )  # Optional for custom user model

    # Check if superuser already exists (use email since it's the USERNAME_FIELD)
    if not User.objects.filter(email=email).exists():
        # Create superuser using email as primary identifier
        create_kwargs = {"email": email, "password": password}

        # Add username if provided
        if username:
            create_kwargs["username"] = username

        user = User.objects.create_superuser(**create_kwargs)
        print(f'Superuser with email "{email}" created successfully!')
        print(f'Generated username: "{user.username}"')
    else:
        print(f'Superuser with email "{email}" already exists.')


if __name__ == "__main__":
    create_superuser()
