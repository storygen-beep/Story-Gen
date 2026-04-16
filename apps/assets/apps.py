from django.apps import AppConfig


class AssetsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.assets"
    verbose_name = "Asset Library"

    def ready(self):
        """Import signal handlers when the app is ready."""
        import apps.assets.signals  # noqa: F401

