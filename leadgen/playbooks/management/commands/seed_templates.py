"""Load (or refresh) the industry templates shipped in playbooks/templates_data/.

Usage: python manage.py seed_templates
"""

import json
from pathlib import Path

from django.core.management.base import BaseCommand

from playbooks.models import IndustryTemplate

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates_data"

TEMPLATE_NAMES = {
    "real_estate_dubai": "Real estate – Dubai",
}


class Command(BaseCommand):
    help = "Create or update industry templates from templates_data/*.json"

    def handle(self, *args, **options):
        for path in sorted(TEMPLATES_DIR.glob("*.json")):
            slug = path.stem
            template, created = IndustryTemplate.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": TEMPLATE_NAMES.get(slug, slug.replace("_", " ").title()),
                    "default_content": json.loads(path.read_text()),
                },
            )
            self.stdout.write(f"{'Created' if created else 'Updated'} template {template.slug}")
