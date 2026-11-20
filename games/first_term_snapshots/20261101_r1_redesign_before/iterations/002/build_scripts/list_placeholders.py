"""Every PLACEHOLDER block in the built TOML: canvas, node, the sheet file:line, what it stands for.
Usage: python3 list_placeholders.py  (prints a Markdown table for BUILD_LOG.md). Read only."""
import os, re, tomllib
HERE = os.path.dirname(os.path.abspath(__file__))
G = tomllib.load(open(os.path.join(HERE, "..", "..", "..", "toml_phases", "7_final_game.toml"), "rb"))
PAT = re.compile(r"PLACEHOLDER — (\S+) \((.*?)\)\.")


def walk(blocks):
    for b in blocks or []:
        yield b
        yield from walk(b.get("blocks"))


rows = []
for c in G.get("canvases", []):
    for n in c.get("nodes", []):
        for b in walk(n.get("blocks")):
            m = PAT.search(b.get("content", "") or "")
            if m:
                rows.append((c["id"], n["id"], m.group(1), m.group(2)))
print(f"{len(rows)} placeholders\n")
print("| # | canvas | node | sheet file:line | what goes here |")
print("|---|---|---|---|---|")
for i, (c, n, ref, what) in enumerate(rows, 1):
    print(f"| {i} | `{c}` | `{n}` | `{ref}` | {what} |")
