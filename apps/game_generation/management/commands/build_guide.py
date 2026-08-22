"""
Management command to render a game's player guide (markdown) into a PDF.

The guide is HAND-WRITTEN prose that lives beside the game but is not generated
from it: games/<slug>/guide/guide.md. This command is only a renderer --
markdown in, styled PDF out. It reads the game TOML for exactly one thing, the
version stamp, so a published guide can never claim a build it wasn't written
against.

Usage:
    python manage.py build_guide --game vesper
    python manage.py build_guide --game vesper --style scripts/guide_styles/dossier
    python manage.py build_guide --guide path/to/guide.md --output out.pdf --html debug.html

The output PDF is gitignored on purpose -- this repo is public and serves the
GitHub Pages portal, so a committed guide would be a free download. Commit the
markdown, upload the PDF.
"""

import os
import sys
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

try:
    import tomllib
except ImportError:
    import tomli as tomllib

# WeasyPrint loads pango/harfbuzz through ctypes, and on macOS those live in
# /opt/homebrew/lib, which is not on the default dyld search path. This must run
# BEFORE weasyprint is imported. It cannot be done from a wrapper shell script:
# macOS SIP strips DYLD_* across an exec of a system binary, so an exported var
# silently never arrives.
if sys.platform == "darwin":
    os.environ.setdefault("DYLD_FALLBACK_LIBRARY_PATH", "/opt/homebrew/lib")

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_STYLE = REPO_ROOT / "scripts" / "guide_styles" / "dossier"

MD_EXTENSIONS = [
    "meta",          # the Key: value front matter (title, cover art)
    "tables",        # the guide is mostly threshold tables
    "attr_list",     # {: .class } hooks for one-off styling
    "admonition",    # !!! warning / !!! spoiler callout boxes
    "toc",           # heading anchors; CSS target-counter supplies page numbers
    "sane_lists",
    "smarty",        # real quotes and dashes -- it is a typeset document
]


def first(meta, key, default=""):
    """python-markdown's meta extension yields every value as a list."""
    return meta.get(key, [default])[0]


class Command(BaseCommand):
    help = "Render a game's hand-written guide markdown into a print-ready PDF"

    def add_arguments(self, parser):
        parser.add_argument(
            '--game',
            type=str,
            help='Game slug; resolves games/<slug>/guide/guide.md and stamps the '
                 'version from games/<slug>/toml_phases/7_final_game.toml',
        )
        parser.add_argument(
            '--guide',
            type=str,
            help='Explicit path to the guide markdown (overrides --game)',
        )
        parser.add_argument(
            '--style',
            type=str,
            default=str(DEFAULT_STYLE),
            help=f'Directory holding template.html + style.css (default: {DEFAULT_STYLE})',
        )
        parser.add_argument(
            '--output',
            type=str,
            help='Destination PDF (default: games/<slug>/guide/<slug>_guide_v<version>.pdf)',
        )
        parser.add_argument(
            '--html',
            type=str,
            help='Also write the intermediate HTML here, for debugging the layout',
        )
        parser.add_argument(
            '--jpeg-quality',
            type=int,
            default=80,
            help='JPEG quality for embedded images (default: 80)',
        )
        parser.add_argument(
            '--dpi',
            type=int,
            default=150,
            help='Resample embedded images above this DPI (default: 150)',
        )

    def handle(self, *args, **options):
        slug = options.get('game')
        guide_path = self._resolve_guide(slug, options.get('guide'))
        style_dir = Path(options['style'])

        for required in ('template.html', 'style.css'):
            if not (style_dir / required).exists():
                raise CommandError(f'Style directory is missing {required}: {style_dir}')

        version, release = self._read_version(slug)

        html = self._render_html(guide_path, style_dir, version, release)

        if options.get('html'):
            Path(options['html']).write_text(html, encoding='utf-8')
            self.stdout.write(f'  html    {options["html"]}')

        output = self._resolve_output(options.get('output'), slug, guide_path, version)
        self._write_pdf(html, guide_path, output, options['jpeg_quality'], options['dpi'])

        size_kb = output.stat().st_size / 1024
        self.stdout.write(self.style.SUCCESS(f'  pdf     {output} ({size_kb:,.0f} KB)'))

    # -- resolution -------------------------------------------------------

    def _resolve_guide(self, slug, explicit):
        if explicit:
            path = Path(explicit)
        elif slug:
            path = REPO_ROOT / 'games' / slug / 'guide' / 'guide.md'
        else:
            raise CommandError('Pass --game <slug> or --guide <path>')

        if not path.exists():
            raise CommandError(f'Guide markdown not found: {path}')
        return path

    def _read_version(self, slug):
        """The version stamp comes from the game, never from the guide's front
        matter -- a guide that names the wrong build is worse than an unstamped
        one. Returns (None, None) when there is no game to read."""
        if not slug:
            return None, None

        toml_path = REPO_ROOT / 'games' / slug / 'toml_phases' / '7_final_game.toml'
        if not toml_path.exists():
            self.stdout.write(self.style.WARNING(
                f'  note    no merged TOML at {toml_path}; using the version in the front matter'
            ))
            return None, None

        with open(toml_path, 'rb') as fh:
            project = tomllib.load(fh).get('project', {})
        return project.get('version'), project.get('release_date')

    def _resolve_output(self, explicit, slug, guide_path, version):
        if explicit:
            path = Path(explicit)
        elif slug:
            stamp = f'_v{version}' if version else ''
            path = guide_path.parent / f'{slug}_guide{stamp}.pdf'
        else:
            path = guide_path.with_suffix('.pdf')
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    # -- rendering --------------------------------------------------------

    CODES_MARKER = '{{codes}}'

    def _substitute_codes(self, source, guide_path, version):
        """Replace the {{codes}} marker with a table built from the game's codes file.

        Generated, never hand-typed. The packager bakes hashes of the same file into
        the build, so a guide that documents a code the build will not accept cannot
        happen — which is the one failure a paying reader would discover for us.

        The row labels and hints come from the game's own cheat-page TOML, so the
        chapter says what each code actually buys without a second copy of that text
        drifting out of date.
        """
        if self.CODES_MARKER not in source:
            self.stdout.write(self.style.WARNING(
                f'  note    no {self.CODES_MARKER} marker in {guide_path.name}; the guide '
                f'will carry no cheat codes'
            ))
            return source

        codes_path = guide_path.parent / 'codes.toml'
        if not codes_path.exists():
            raise CommandError(
                f'{guide_path.name} asks for {self.CODES_MARKER} but there is no '
                f'{codes_path}. That file is untracked on purpose — it holds the codes, '
                f'and this repo is public.'
            )

        with open(codes_path, 'rb') as fh:
            data = tomllib.load(fh)
        codes = data.get('codes') or {}
        declared = str(data.get('version', '') or '').strip()
        if not codes:
            raise CommandError(f'{codes_path}: [codes] is empty.')
        if version and declared and declared != version:
            raise CommandError(
                f'{codes_path}: codes are for v{declared} but the game is v{version}. '
                f'Codes are scoped to a release — a guide stamped with one version and '
                f'codes from another is the exact thing this check exists to stop.'
            )

        rows = self._cheat_rows(guide_path)
        lines = [
            '| Cheat | Code | What it opens |',
            '|---|---|---|',
        ]
        # Authored order, not the codes file's — the guide should read in the order the
        # page presents, and a dict literal's order is an accident of editing.
        for row_id, label, hint in rows:
            if row_id not in codes:
                continue
            lines.append(f'| {label} | `{codes[row_id]}` | {hint or "—"} |')
        for row_id, word in codes.items():
            if row_id not in {r[0] for r in rows}:
                lines.append(f'| {row_id} | `{word}` | — |')

        table = '\n'.join(lines)
        return source.replace(self.CODES_MARKER, table)

    ROSTER_MARKER = '{{roster}}'
    WEEKDAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    def _substitute_roster(self, source, guide_path):
        """Replace {{roster}} with a who/where/when table from the game's schedules.

        Generated for the same reason the codes are: a reader sent to the wrong place
        at the wrong hour concludes the game is broken, and schedules move between
        releases more often than almost anything else in a build.
        """
        if self.ROSTER_MARKER not in source:
            return source

        data = self._merged_toml(guide_path)
        if data is None:
            raise CommandError(
                f'{guide_path.name} asks for {self.ROSTER_MARKER} but the merged TOML '
                f'was not found next door in toml_phases/.'
            )

        names = {loc['id']: loc.get('name', loc['id'])
                 for loc in data.get('locations') or [] if 'id' in loc}
        lines = ['| Who | Where | When | Doing what |', '|---|---|---|---|']
        for npc in data.get('npcs') or []:
            for i, sched in enumerate(npc.get('schedules') or []):
                weekdays = sched.get('weekdays') or []
                when = ('Every day' if len(weekdays) == 7 or not weekdays
                        else ', '.join(self.WEEKDAY_NAMES[d] for d in weekdays
                                       if 0 <= d < 7))
                lines.append(
                    # The name is printed once per person; the extra rows hang under it,
                    # so a person with three shifts reads as one entry, not three people.
                    f'| {"**" + npc.get("name", "") + "**" if i == 0 else ""} '
                    f'| {names.get(sched.get("location"), sched.get("location", "?"))} '
                    f'| {when}, {sched.get("start_time")}–{sched.get("end_time")} '
                    f'| {sched.get("activity", "—")} |'
                )
        return source.replace(self.ROSTER_MARKER, '\n'.join(lines))

    def _merged_toml(self, guide_path):
        path = guide_path.parent.parent / 'toml_phases' / '7_final_game.toml'
        if not path.exists():
            return None
        with open(path, 'rb') as fh:
            return tomllib.load(fh)

    def _cheat_rows(self, guide_path):
        """(id, label, hint) per authored cheat row, in the order the page shows them."""
        data = self._merged_toml(guide_path)
        if data is None:
            return []
        page = (data.get('ui') or {}).get('cheat_page') or {}
        rows = []
        for g in page.get('grants') or []:
            label = g.get('button_text') or g.get('label') or g.get('id')
            rows.append((g.get('id'), label, g.get('hint')))
        return rows

    def _render_html(self, guide_path, style_dir, version, release):
        try:
            import markdown
        except ImportError as exc:
            raise CommandError(
                'markdown is not installed. Run:\n'
                '  uv pip install --python venv/bin/python markdown'
            ) from exc

        source = guide_path.read_text(encoding='utf-8')
        # Two tables are GENERATED; every other word in the guide is hand-written.
        # These two are the ones a reader would be actively misled by if they went
        # stale -- a code that does not work, and a person who is not where the book
        # says. Substituted into the MARKDOWN, before conversion, so the chapters get
        # real headings and land in the table of contents like any other.
        source = self._substitute_codes(source, guide_path, version)
        source = self._substitute_roster(source, guide_path)

        md = markdown.Markdown(extensions=MD_EXTENSIONS, output_format='html5')
        body = md.convert(source)
        meta = md.Meta

        # The TOC extension wraps its list in a div; the template places the
        # list itself so the wrapper is stripped.
        toc = md.toc.replace('<div class="toc">', '').rstrip()
        if toc.endswith('</div>'):
            toc = toc[: -len('</div>')]

        template = (style_dir / 'template.html').read_text(encoding='utf-8')
        stylesheet = (style_dir / 'style.css').read_text(encoding='utf-8')

        # Plain substitution, not str.format -- the template carries literal CSS
        # and HTML braces that any brace-based formatter would choke on.
        slots = {
            '{{title}}': first(meta, 'title', 'Guide'),
            '{{subtitle}}': first(meta, 'subtitle'),
            '{{version}}': version or first(meta, 'version'),
            '{{release}}': release or first(meta, 'release'),
            '{{byline}}': first(meta, 'byline'),
            '{{cover}}': first(meta, 'cover'),
            '{{stylesheet}}': stylesheet,
            '{{toc}}': toc,
            '{{body}}': body,
        }
        for slot, value in slots.items():
            template = template.replace(slot, value)
        return template

    def _write_pdf(self, html, guide_path, output, jpeg_quality, dpi):
        try:
            from weasyprint import HTML
        except ImportError as exc:
            raise CommandError(
                'weasyprint is not installed. Run:\n'
                '  uv pip install --python venv/bin/python weasyprint'
            ) from exc
        except OSError as exc:
            raise CommandError(
                f'weasyprint could not load its native libraries: {exc}\n'
                'On macOS: brew install pango'
            ) from exc

        # base_url is the guide folder so `../output/videos/portraits/x.jpg`
        # resolves the same way it does previewing the markdown in an editor.
        HTML(string=html, base_url=str(guide_path.parent)).write_pdf(
            output,
            optimize_images=True,
            jpeg_quality=jpeg_quality,
            dpi=dpi,
        )
