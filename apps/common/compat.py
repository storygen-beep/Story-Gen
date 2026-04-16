"""
Database-backend compatibility helpers.

On PostgreSQL: re-exports native ArrayField, SearchVectorField, VectorField.
On SQLite: provides JSONField/TextField stand-ins so models load without error.
"""

from decouple import config
from django.db import models

_engine = config("DB_ENGINE", default="django.db.backends.postgresql")
_is_sqlite = "sqlite" in _engine

if _is_sqlite:
    # Stand-in: stores lists as JSON
    class ArrayField(models.JSONField):
        def __init__(self, base_field=None, size=None, **kwargs):
            super().__init__(**kwargs)

    # Stand-in: plain text column
    class SearchVectorField(models.TextField):
        pass

    # Stand-in: plain text column
    class VectorField(models.TextField):
        def __init__(self, *args, dimensions=None, **kwargs):
            super().__init__(*args, **kwargs)
else:
    from django.contrib.postgres.fields import ArrayField  # noqa: F401
    from django.contrib.postgres.search import SearchVectorField  # noqa: F401
    from pgvector.django import VectorField  # noqa: F401
