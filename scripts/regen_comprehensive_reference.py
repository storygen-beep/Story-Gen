#!/usr/bin/env python3
"""Regenerate prompts_v2/COMPREHENSIVE_SYSTEM_REFERENCE.md — mechanical concat of the
canonical source files (Doc 66 §6.5 / §8). Re-run on any source-file change.

Order: 00_LEGACY_IGNORE → schema/01-03 → doctrine/01-10 → reference/01-04 → stages/01-04.
Each section: '## N. <name>' + '**Source:** `path`' + '---' + body, joined by a 79-char ═ rule.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "prompts_v2"
RULE = "═" * 79

# (display_name, relative_path) in canonical reading order.
SOURCES = [
    ("00_LEGACY_IGNORE", "00_LEGACY_IGNORE.md"),
    ("01_engine_capabilities", "schema/01_engine_capabilities.md"),
    ("02_toml_schema", "schema/02_toml_schema.md"),
    ("03_example_toml", "schema/03_example_toml.md"),
    ("01_rts_principles", "doctrine/01_rts_principles.md"),
    ("02_three_lanes_plus_capstone", "doctrine/02_three_lanes_plus_capstone.md"),
    ("03_arc_shapes", "doctrine/03_arc_shapes.md"),
    ("04_authoring_rules", "doctrine/04_authoring_rules.md"),
    ("05_rts_flat_prose", "doctrine/05_rts_flat_prose.md"),
    ("06_design_brief_template", "doctrine/06_design_brief_template.md"),
    ("07_anti_patterns", "doctrine/07_anti_patterns.md"),
    ("08_kink_vocab_ceilings", "doctrine/08_kink_vocab_ceilings.md"),
    ("09_trait_catalog", "doctrine/09_trait_catalog.md"),
    ("10_location_design", "doctrine/10_location_design.md"),
    ("11_clothing_design", "doctrine/11_clothing_design.md"),
    ("12_rent_economy_design", "doctrine/12_rent_economy_design.md"),
    ("13_phone_design", "doctrine/13_phone_design.md"),
    ("01_rts_overview", "reference/01_rts_overview.md"),
    ("02_rts_scene_catalog", "reference/02_rts_scene_catalog.md"),
    ("03_rts_walkthrough_panel", "reference/03_rts_walkthrough_panel.md"),
    ("04_rts_hud_world_model", "reference/04_rts_hud_world_model.md"),
    ("01_game_book_prompt", "stages/01_game_book_prompt.md"),
    ("02_toml_generation_prompt", "stages/02_toml_generation_prompt.md"),
    ("03_image_finder_prompt", "stages/03_image_finder_prompt.md"),
    ("04_game_listing_prompt", "stages/04_game_listing_prompt.md"),
]


def anchor(n, name):
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return f"#{n}-{slug}"


def main():
    out = []
    out.append("# prompts_v2 — Comprehensive System Reference\n")
    out.append("\n**Status:** Single concatenated reference. Generated mechanically from "
               "the source files in canonical reading order. Regenerate via "
               "`scripts/regen_comprehensive_reference.py` when source files change.\n")
    out.append("\n**How to use:** if you want the FULL prompts_v2 corpus in one file "
               "(single-load LLM context), this is it. For day-to-day work, prefer the "
               "individual source files.\n\n---\n\n## Table of Contents\n\n")
    for i, (name, rel) in enumerate(SOURCES, 1):
        out.append(f"{i}. [{name}]({anchor(i, name)}) — `prompts_v2/{rel}`\n")
    out.append("\n---\n\n")
    for i, (name, rel) in enumerate(SOURCES, 1):
        body = (ROOT / rel).read_text()
        out.append(f"\n{RULE}\n\n## {i}. {name}\n\n**Source:** `prompts_v2/{rel}`\n\n---\n\n")
        out.append(body)
        if not body.endswith("\n"):
            out.append("\n")
    target = ROOT / "COMPREHENSIVE_SYSTEM_REFERENCE.md"
    target.write_text("".join(out))
    print(f"wrote {target}  ({target.stat().st_size:,} bytes, {len(SOURCES)} sources)")


if __name__ == "__main__":
    main()
