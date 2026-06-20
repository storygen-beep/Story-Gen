#!/bin/bash
# Sync description symlinks for jacks_world
# Usage: ./sync_descriptions.sh [--dry-run] [--collection NAME] [--clean]

cd "$(dirname "$0")/../.."
source venv/bin/activate
python manage.py sync_descriptions jacks_world "$@"
