#!/usr/bin/env python3
"""Turn a design-site artifact page (an HTML fragment) into something runnable.

The Artifact tool publishes a *fragment*: no doctype, no <html>/<head>/<body>, with
<title>, <style> and <script> written inline. That is right for an artifact and wrong
for everything else, so this script has two modes:

  preview  page.html out_dir            one wrapped index.html, for local screenshots and scans
  export   page.html site_dir [brief]   a real site folder (index.html + css/ + js/ + assets/)
                                        plus <site_dir>.zip next to it

Only the standard library is used.
"""
import base64
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

# What the artifact skeleton gives the page for free. Reproduced here so the preview
# and the exported site render the same way the artifact did.
SKELETON_RESET = (
    "body{margin:0;font:14px system-ui,sans-serif}"
    "img{max-width:100%}"
    "[hidden]{display:none!important}"
)

TITLE_RE = re.compile(r"<title\b[^>]*>(.*?)</title>", re.S | re.I)
STYLE_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.S | re.I)
HEAD_TAG_RE = re.compile(r"<(?:meta|link)\b[^>]*>", re.I)
SCRIPT_RE = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.S | re.I)
DATA_URI_RE = re.compile(r"data:(image/[a-z0-9.+-]+|font/[a-z0-9.+-]+);base64,([A-Za-z0-9+/=]+)", re.I)
ARTIFACT_ONLY_META_RE = re.compile(r'<meta\s+name="claude:[^"]*"[^>]*>', re.I)

EXTENSIONS = {
    "image/png": "png", "image/jpeg": "jpg", "image/webp": "webp", "image/gif": "gif",
    "image/svg+xml": "svg", "image/avif": "avif", "font/woff2": "woff2", "font/woff": "woff",
}


def split_fragment(fragment):
    """Pull title, head tags, styles and inline scripts out of the fragment."""
    title_match = TITLE_RE.search(fragment)
    title = title_match.group(1).strip() if title_match else "Untitled"
    body = TITLE_RE.sub("", fragment, count=1)

    styles = [m.group(1).strip() for m in STYLE_RE.finditer(body)]
    body = STYLE_RE.sub("", body)

    head_tags = [t for t in HEAD_TAG_RE.findall(body) if not ARTIFACT_ONLY_META_RE.fullmatch(t)]
    body = HEAD_TAG_RE.sub("", body)

    inline_scripts = []

    def take_inline(match):
        attrs, code = match.group(1), match.group(2)
        is_external = re.search(r"\bsrc\s*=", attrs, re.I)
        is_data_block = re.search(r'type\s*=\s*"(?:application/(?:ld\+)?json|text/template)"', attrs, re.I)
        if is_external or is_data_block:
            return match.group(0)  # library tags and JSON blocks stay where they are
        inline_scripts.append(code.strip())
        return ""

    body = SCRIPT_RE.sub(take_inline, body)
    return title, head_tags, styles, inline_scripts, body.strip()


def document(title, head_tags, head_extra, body, lang="en"):
    head = "\n".join(
        ['<meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
         f"<title>{title}</title>"] + head_tags + head_extra
    )
    return f'<!doctype html>\n<html lang="{lang}">\n<head>\n{head}\n</head>\n<body>\n{body}\n</body>\n</html>\n'


def preview(page_path, out_dir):
    title, head_tags, styles, scripts, body = split_fragment(page_path.read_text(encoding="utf-8"))
    out_dir.mkdir(parents=True, exist_ok=True)
    css = SKELETON_RESET + "\n" + "\n\n".join(styles)
    js = "\n;\n".join(scripts)
    html = document(title, head_tags, [f"<style>\n{css}\n</style>"],
                    body + (f"\n<script>\n{js}\n</script>" if js else ""))
    target = out_dir / "index.html"
    target.write_text(html, encoding="utf-8")
    print(json.dumps({"preview": str(target), "bytes": len(html.encode())}))


def extract_assets(text, assets_dir, url_prefix, written):
    """Replace embedded data: URIs with real files so the site is editable and cacheable."""
    def to_file(match):
        mime, payload = match.group(1).lower(), match.group(2)
        raw = base64.b64decode(payload)
        name = f"asset-{hashlib.sha1(raw).hexdigest()[:10]}.{EXTENSIONS.get(mime, 'bin')}"
        if name not in written:
            assets_dir.mkdir(parents=True, exist_ok=True)
            (assets_dir / name).write_bytes(raw)
            written.add(name)
        return f"{url_prefix}{name}"
    return DATA_URI_RE.sub(to_file, text)


def export(page_path, site_dir, brief_path):
    title, head_tags, styles, scripts, body = split_fragment(page_path.read_text(encoding="utf-8"))
    if site_dir.exists():
        shutil.rmtree(site_dir)  # an export is a full replacement of the previous export
    (site_dir / "css").mkdir(parents=True)

    written = set()
    assets_dir = site_dir / "assets"
    css = SKELETON_RESET + "\n\n" + "\n\n".join(styles)
    css = extract_assets(css, assets_dir, "../assets/", written)
    body = extract_assets(body, assets_dir, "assets/", written)
    (site_dir / "css" / "styles.css").write_text(css + "\n", encoding="utf-8")

    head_extra = ['<link rel="stylesheet" href="css/styles.css">']
    brief = {}
    if brief_path and brief_path.exists():
        brief = json.loads(brief_path.read_text(encoding="utf-8"))
        shutil.copy(brief_path, site_dir / "design-brief.json")
        description = (brief.get("message") or {}).get("meta_description")
        if description:
            safe = description.replace('"', "&quot;")
            head_extra.insert(0, f'<meta name="description" content="{safe}">')

    if scripts:
        (site_dir / "js").mkdir()
        (site_dir / "js" / "main.js").write_text("\n;\n".join(scripts) + "\n", encoding="utf-8")
        body += '\n<script src="js/main.js"></script>'

    (site_dir / "index.html").write_text(document(title, head_tags, head_extra, body), encoding="utf-8")

    zip_path = site_dir.parent / f"{site_dir.name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(site_dir.rglob("*")):
            if file.is_file():
                archive.write(file, Path(site_dir.name) / file.relative_to(site_dir))

    files = sorted(str(f.relative_to(site_dir)) for f in site_dir.rglob("*") if f.is_file())
    print(json.dumps({"site": str(site_dir), "zip": str(zip_path), "files": files}, indent=2))


def main():
    if len(sys.argv) < 4 or sys.argv[1] not in ("preview", "export"):
        sys.exit(__doc__)
    mode, page, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    if mode == "preview":
        preview(page, out)
    else:
        export(page, out, Path(sys.argv[4]) if len(sys.argv) > 4 else None)


if __name__ == "__main__":
    main()
