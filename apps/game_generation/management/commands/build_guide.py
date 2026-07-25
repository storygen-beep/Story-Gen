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

    def _render_html(self, guide_path, style_dir, version, release):
        try:
            import markdown
        except ImportError as exc:
            raise CommandError(
                'markdown is not installed. Run:\n'
                '  uv pip install --python venv/bin/python markdown'
            ) from exc

        md = markdown.Markdown(extensions=MD_EXTENSIONS, output_format='html5')
        body = md.convert(guide_path.read_text(encoding='utf-8'))
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
