#!/usr/bin/env python3
"""Check a set of design directions before the user sees them.

  directions.py a/DESIGN.md b/DESIGN.md c/DESIGN.md [--previous 'sites/*/design-brief.json']

For each direction it reports the "looks generated" tells that can be read from tokens
alone (overused fonts, the AI purple band, the two stock palettes). Across the set it
reports where two directions are too alike to be a real choice. With --previous it also
flags a direction that repeats the fonts of a site already exported from this repo.

It reads the YAML front matter of each DESIGN.md with regular expressions, so it needs
no packages. Exit code is 1 when anything is flagged.
"""
import colorsys
import glob
import itertools
import json
import re
import sys

# Faces so common in generated pages that they read as a default, not a choice.
# Union of the impeccable detector's list and the vendored typography watch list.
OVERUSED_FONTS = {
    "inter", "roboto", "poppins", "montserrat", "open sans", "lato", "space grotesk",
    "plus jakarta sans", "sora", "outfit", "dm sans", "manrope", "geist", "satoshi",
    "general sans", "fraunces", "instrument serif", "arial", "helvetica", "system-ui",
}
ACCENT_KEYS = ("tertiary", "accent", "primary")  # first one present is treated as the accent
GROUND_KEYS = ("neutral", "background", "surface")
MIN_HUE_GAP = 30  # degrees; closer than this, two accents read as the same colour


def front_matter(path):
    text = open(path, encoding="utf-8").read()
    match = re.match(r"---\n(.*?)\n---", text, re.S)
    if not match:
        sys.exit(f"{path}: no YAML front matter")
    return match.group(1)


def block(yaml, key):
    """The indented lines under a top-level key."""
    match = re.search(rf"^{key}:\n((?:[ \t]+.*\n?)+)", yaml, re.M)
    return match.group(1) if match else ""


def read_direction(path):
    yaml = front_matter(path)
    name = re.search(r"^name:\s*(.+)$", yaml, re.M)
    colors = dict(re.findall(r"^\s+([\w-]+):\s*[\"']?(#[0-9a-fA-F]{6})\b", block(yaml, "colors"), re.M))
    fonts = sorted({f.strip().strip("\"'").split(",")[0].strip().strip("\"'")
                    for f in re.findall(r"fontFamily:\s*(.+)", block(yaml, "typography"))})
    return {"path": path, "name": name.group(1).strip().strip("\"'") if name else path, "colors": colors, "fonts": fonts}


def hls(hex_color):
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b)
    return hue * 360, lightness, saturation


def first(colors, keys):
    return next((colors[k] for k in keys if k in colors), None)


def tells(direction):
    found = []
    for font in direction["fonts"]:
        if font.lower() in OVERUSED_FONTS:
            found.append(f"font '{font}' is on the overused list — pick a face for a stated reason or justify it")
    accent, ground = first(direction["colors"], ACCENT_KEYS), first(direction["colors"], GROUND_KEYS)
    if accent:
        hue, lightness, saturation = hls(accent)
        if 245 <= hue <= 300 and saturation > 0.35:
            found.append(f"accent {accent} sits in the purple/violet band that marks generated pages")
        if ground:
            ground_hue, ground_light, ground_sat = hls(ground)
            cream = ground_light > 0.9 and 25 <= ground_hue <= 60 and ground_sat > 0.2
            if cream and 5 <= hue <= 30 and saturation > 0.4:
                found.append("cream ground with a terracotta accent — the stock 'warm editorial' palette")
            if ground_light < 0.1 and 70 <= hue <= 150 and saturation > 0.7 and lightness > 0.45:
                found.append("near-black ground with an acid-green accent — the stock 'dev tool' palette")
    if not direction["fonts"]:
        found.append("no typography tokens found")
    if not accent:
        found.append("no accent colour found (expected one of: " + ", ".join(ACCENT_KEYS) + ")")
    return found


def too_alike(a, b):
    found = []
    shared = set(f.lower() for f in a["fonts"]) & set(f.lower() for f in b["fonts"])
    if shared:
        found.append("share the font " + ", ".join(sorted(shared)))
    accent_a, accent_b = first(a["colors"], ACCENT_KEYS), first(b["colors"], ACCENT_KEYS)
    if accent_a and accent_b:
        (hue_a, _, sat_a), (hue_b, _, sat_b) = hls(accent_a), hls(accent_b)
        gap = min(abs(hue_a - hue_b), 360 - abs(hue_a - hue_b))
        if sat_a > 0.15 and sat_b > 0.15 and gap < MIN_HUE_GAP:
            found.append(f"accent hues only {gap:.0f}° apart ({accent_a}, {accent_b})")
    ground_a, ground_b = first(a["colors"], GROUND_KEYS), first(b["colors"], GROUND_KEYS)
    if ground_a and ground_b and len(found) == 2:
        # Same fonts and same accent family: only flag the ground as well if it is also the same mode.
        if (hls(ground_a)[1] > 0.5) == (hls(ground_b)[1] > 0.5):
            found.append("and both on the same light/dark ground — these are one direction, not two")
    return found


def main():
    args = sys.argv[1:]
    previous_glob = None
    if "--previous" in args:
        index = args.index("--previous")
        previous_glob = args[index + 1]
        del args[index:index + 2]
    if len(args) < 2:
        sys.exit(__doc__)

    directions = [read_direction(p) for p in args]
    report = {"directions": [], "pairs": [], "repeats": []}
    for direction in directions:
        accent = first(direction["colors"], ACCENT_KEYS)
        report["directions"].append({
            "name": direction["name"], "fonts": direction["fonts"], "accent": accent,
            "accentHue": round(hls(accent)[0]) if accent else None, "tells": tells(direction),
        })
    for a, b in itertools.combinations(directions, 2):
        issues = too_alike(a, b)
        if issues:
            report["pairs"].append({"between": [a["name"], b["name"]], "issues": issues})

    if previous_glob:
        for path in glob.glob(previous_glob):
            try:
                look = json.load(open(path, encoding="utf-8")).get("look", {})
            except (OSError, ValueError):
                continue
            used = {str(f).lower() for f in look.get("fonts", [])}
            for direction in directions:
                repeat = used & {f.lower() for f in direction["fonts"]}
                if repeat:
                    report["repeats"].append({"direction": direction["name"], "site": path, "fonts": sorted(repeat)})

    flagged = any(d["tells"] for d in report["directions"]) or report["pairs"] or report["repeats"]
    report["ok"] = not flagged
    print(json.dumps(report, indent=2))
    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()
