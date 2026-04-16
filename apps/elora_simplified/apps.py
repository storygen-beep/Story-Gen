"""
Elora Simplified Django App Configuration.
"""

from django.apps import AppConfig


class EloraSimplifiedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.elora_simplified'
    verbose_name = 'Elora AI Agent (Simplified)'
