"""
Management command to check which media files from a TOML exist in the media folder.

Uses extension-agnostic matching - if TOML says intro.mp4 but intro.gif exists,
it will be detected as found.

Usage:
    python manage.py check_media --file two_weeks/two_weeks.toml --media two_weeks/media
    python manage.py check_media --file game.toml --media media/ --missing-only
"""

from pathlib import Path
from collections import defaultdict

from django.core.management.base import BaseCommand, CommandError

from apps.common.media_blocks import block_media_paths, block_media_pool

try:
    import tomllib
except ImportError:
    import tomli as tomllib


# Extension sets for media type detection
VIDEO_EXTENSIONS = {'.mp4', '.webm', '.mov', '.m4v', '.avi', '.mkv'}
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp'}
ALL_MEDIA_EXTENSIONS = VIDEO_EXTENSIONS | IMAGE_EXTENSIONS


class Command(BaseCommand):
    help = 'Check which media files from TOML exist in media folder'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            required=True,
            help='Path to TOML game definition file',
        )
        parser.add_argument(
            '--media',
            type=str,
            required=True,
            help='Path to media folder',
        )
        parser.add_argument(
            '--missing-only',
            action='store_true',
            help='Only show missing files',
        )

    def handle(self, *args, **options):
        toml_path = Path(options['file'])
        media_path = Path(options['media'])
        missing_only = options['missing_only']

        # Validate paths
        if not toml_path.exists():
            raise CommandError(f"TOML file not found: {toml_path}")
        if not media_path.exists():
            raise CommandError(f"Media folder not found: {media_path}")

        # Parse TOML
        self.stdout.write(f"Loading TOML: {toml_path}")
        with open(toml_path, 'rb') as f:
            toml_data = tomllib.load(f)

        # Scan media folder
        self.stdout.write(f"Scanning media folder: {media_path}")
        available_files = self._scan_media_folder(media_path)
        self.stdout.write(f"Found {len(available_files)} media files\n")

        # Extract media references from TOML
        media_refs = self._extract_media_references(toml_data)

        # Check each file and categorize
        results = self._check_files(media_refs, available_files)

        # Get project title
        project_title = toml_data.get('project', {}).get('title', 'Unknown')

        # Print report
        self._print_report(project_title, results, missing_only)

    def _scan_media_folder(self, media_path: Path) -> set:
        """Scan media folder and return set of relative paths."""
        files = set()
        for file in media_path.rglob('*'):
            if file.is_file() and file.suffix.lower() in ALL_MEDIA_EXTENSIONS:
                relative = file.relative_to(media_path)
                # Normalize to forward slashes
                files.add(str(relative).replace('\\', '/'))
        return files

    def _find_media_file(self, requested_path: str, available_files: set) -> str | None:
        """Find file with extension-agnostic matching."""
        normalized = requested_path.replace('\\', '/')

        # Exact match first
        if normalized in available_files:
            return normalized

        # Extension-agnostic search
        base_path = str(Path(normalized).with_suffix(''))
        for file_path in available_files:
            file_base = str(Path(file_path).with_suffix(''))
            if file_base == base_path:
                return file_path

        return None

    def _extract_media_references(self, toml_data: dict) -> list:
        """Extract all media file references from TOML canvases."""
        refs = []

        canvases = toml_data.get('canvases', [])
        for canvas in canvases:
            canvas_id = canvas.get('id', 'unknown')
            canvas_name = canvas.get('name', canvas_id)

            # Check all nodes
            nodes = canvas.get('nodes', [])
            for node in nodes:
                for block in node.get('blocks', []):
                    self._extract_from_block(block, canvas_id, canvas_name, refs)

                # Also check exit_block
                exit_block = node.get('exit_block', {})
                if exit_block:
                    self._extract_from_block(exit_block, canvas_id, canvas_name, refs)

            # Check canvas-level blocks
            for block in canvas.get('blocks', []):
                self._extract_from_block(block, canvas_id, canvas_name, refs)

        return refs

    def _extract_from_block(self, block: dict, canvas_id: str, canvas_name: str, refs: list):
        """Extract every media reference a single block declares.

        The three call sites above were hand-duplicated copies of this, all
        reading `props['file']` — so a pool block (`files = [...]`, no `file`)
        was invisible in all three and its slots never appeared as missing.
        `block_media_paths` returns one path per pool entry, and each becomes its
        own row because each is a separate file to find and install.
        """
        block_type = block.get('type')
        if block_type not in ('video', 'image'):
            return
        props = block.get('props', {}) or {}

        if block_type == 'video':
            description = props.get('description', '')
        else:
            description = props.get('alt', '') or props.get('description', '')

        # A FOLDER pool contributes ONE ref for the whole block — its filenames
        # live on disk, not in the TOML. `pool_target` is what we were aiming for,
        # so a half-filled pool reports "2/4" instead of passing as complete.
        # Must match api/v1/game_review.py's treatment or the two enumerators
        # drift apart again, which is what apps/common/media_blocks.py exists to stop.
        pool_spec = block_media_pool(props)
        if pool_spec is not None:
            refs.append({
                'type': block_type,
                'file': pool_spec['dir'],
                'description': description,
                'canvas_id': canvas_id,
                'canvas_name': canvas_name,
                'pool_dir': pool_spec['dir'],
                'pool_target': pool_spec['target'],
            })
            return

        for file_path in block_media_paths(props):
            refs.append({
                'type': block_type,
                'file': file_path,
                'description': description,
                'canvas_id': canvas_id,
                'canvas_name': canvas_name,
            })

    def _categorize(self, canvas_id: str, file_path: str) -> tuple[str, str]:
        """Categorize a media reference by section and subsection."""
        canvas_lower = canvas_id.lower()
        file_lower = file_path.lower()

        # Check file path first for better categorization
        if file_lower.startswith('endings/') or 'ending_' in file_lower:
            return 'Endings', ''
        elif file_lower.startswith('solo/') or 'solo_' in canvas_lower:
            return 'Solo Activities', ''
        elif file_lower.startswith('activities/'):
            # Extract activity name for sub-grouping
            # activities/morning_coffee_t1.mp4 -> morning_coffee
            filename = Path(file_path).stem
            parts = filename.rsplit('_t', 1)
            if len(parts) == 2 and parts[1].isdigit():
                activity_name = parts[0].replace('_', ' ').title()
                return 'Activities', activity_name
            return 'Activities', 'Other'
        elif file_lower.startswith('scenes/bathroom/') or 'shower' in file_lower:
            return 'Solo Activities', 'Shower'
        elif file_lower.startswith('scenes/') or canvas_lower.startswith('scene_'):
            return 'Story Scenes', ''
        elif file_lower.startswith('images/'):
            return 'Images', ''
        else:
            return 'Other', ''

    def _check_files(self, media_refs: list, available_files: set) -> dict:
        """Check each file and organize results by category."""
        results = defaultdict(lambda: defaultdict(list))

        for ref in media_refs:
            file_path = ref['file']

            if ref.get('pool_dir'):
                # A folder pool is satisfied by CONTENTS, not by one filename.
                # `_scan_media_folder` already returns a flat set of relative
                # paths, so counting the folder's members needs no extra I/O.
                prefix = ref['pool_dir'].rstrip('/') + '/'
                count = sum(1 for p in available_files if p.startswith(prefix))
                target = ref['pool_target']
                category, subsection = self._categorize(ref['canvas_id'], file_path)
                results[category][subsection].append({
                    'file': f"{ref['pool_dir']}/  [pool {count}/{target}]",
                    # Anything in the folder renders, so it is FOUND. Falling
                    # short of target is a shortfall, not a hole — reported in
                    # the label rather than as a missing file.
                    'found': count > 0,
                    'found_as': f"{count} file{'' if count == 1 else 's'}" if count else None,
                    'description': ref['description'][:50] if ref['description'] else '',
                    'type': ref['type'],
                })
                continue

            found_as = self._find_media_file(file_path, available_files)

            category, subsection = self._categorize(ref['canvas_id'], file_path)

            results[category][subsection].append({
                'file': file_path,
                'found': found_as is not None,
                'found_as': found_as,
                'description': ref['description'][:50] if ref['description'] else '',
                'type': ref['type'],
            })

        return results

    def _print_report(self, title: str, results: dict, missing_only: bool):
        """Print formatted report."""
        self.stdout.write("\n" + "═" * 80)
        self.stdout.write(f"MEDIA CHECK: {title}")
        self.stdout.write("═" * 80 + "\n")

        # Calculate totals
        category_stats = {}
        total_found = 0
        total_missing = 0

        for category, subsections in results.items():
            cat_found = 0
            cat_total = 0
            for subsection, items in subsections.items():
                for item in items:
                    cat_total += 1
                    if item['found']:
                        cat_found += 1
            category_stats[category] = {'found': cat_found, 'total': cat_total}
            total_found += cat_found
            total_missing += (cat_total - cat_found)

        # Print summary
        self.stdout.write("## Summary\n")
        self.stdout.write(f"{'Category':<20} {'Total':>8} {'Found':>8} {'Missing':>8}")
        self.stdout.write("-" * 50)

        # Define category order
        category_order = ['Story Scenes', 'Endings', 'Activities', 'Solo Activities', 'Images', 'Other']
        for category in category_order:
            if category in category_stats:
                stats = category_stats[category]
                missing = stats['total'] - stats['found']
                self.stdout.write(
                    f"{category:<20} {stats['total']:>8} {stats['found']:>8} {missing:>8}"
                )

        self.stdout.write("-" * 50)
        total = total_found + total_missing
        self.stdout.write(f"{'TOTAL':<20} {total:>8} {total_found:>8} {total_missing:>8}\n")

        # Print each category
        for category in category_order:
            if category not in results:
                continue

            subsections = results[category]
            stats = category_stats[category]

            self.stdout.write("\n" + "─" * 80)
            self.stdout.write(f"## {category} ({stats['found']}/{stats['total']})")
            self.stdout.write("─" * 80)

            # Sort subsections
            sorted_subsections = sorted(subsections.keys())

            for subsection in sorted_subsections:
                items = subsections[subsection]

                # Calculate subsection stats
                sub_found = sum(1 for i in items if i['found'])
                sub_total = len(items)

                if subsection:
                    complete = " ✓ Complete" if sub_found == sub_total else ""
                    self.stdout.write(f"\n### {subsection} ({sub_found}/{sub_total}){complete}\n")

                # Print table header
                self.stdout.write(f"{'St':<3} {'File':<45} {'Found As':<25}")
                self.stdout.write("-" * 75)

                # Sort items by file path
                sorted_items = sorted(items, key=lambda x: x['file'])

                for item in sorted_items:
                    if missing_only and item['found']:
                        continue

                    status = "✓" if item['found'] else "✗"
                    file_display = item['file']
                    if len(file_display) > 43:
                        file_display = "..." + file_display[-40:]

                    found_display = item['found_as'] if item['found_as'] else "—"
                    if len(found_display) > 23:
                        found_display = "..." + found_display[-20:]

                    self.stdout.write(f"{status:<3} {file_display:<45} {found_display:<25}")

        self.stdout.write("\n" + "═" * 80)
        self.stdout.write(f"Total: {total_found} found, {total_missing} missing")
        self.stdout.write("═" * 80 + "\n")
