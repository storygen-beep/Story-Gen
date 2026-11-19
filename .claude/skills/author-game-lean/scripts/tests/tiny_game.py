"""The tiny throwaway game the check and hook tests share: two canvases on approved card p1, one dev canvas,
and a built row in STATE.md. Built in a temp folder; nothing in games/ is read."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import approve  # noqa: E402

META = '[project]\nstarting_canvas = "start"\n\n[[locations]]\nid = "home"\n'


def canvas(cid, name=None, **trigger):
    t = {"location": "home", "is_active": "true", **trigger}
    lines = [f'[[canvases]]\nid = "{cid}"\nname = "{name or cid}"\n\n[canvases.trigger]']
    lines += [f"{k} = {v}" if v in ("true", "false") else f'{k} = "{v}"' for k, v in t.items()]
    lines.append(f'\n[[canvases.nodes]]\nid = "a"\n')
    return "\n".join(lines) + "\n"


STATE = """# STATE: tiny (tiny)

## Release 1: skeleton

| piece | what | approved | built | checked | played |
|---|---|---|---|---|---|
| p1 | the start | 2026-11-19 | 2026-11-19 | | |

Next step: build — p1
"""


def make_game(where):
    """A clean game at <where>/tiny."""
    g = Path(where) / "tiny"
    (g / "toml_phases").mkdir(parents=True)
    (g / "cards").mkdir()
    (g / "toml_phases" / "1_metadata_and_locations.toml").write_text(META)
    (g / "toml_phases" / "5_scenes.toml").write_text(canvas("start") + "\n" + canvas("kitchen"))
    (g / "toml_phases" / "6_dev_shortcuts.toml").write_text(canvas("dev_jump_x", name="Dev jump: to the kitchen"))
    (g / "STATE.md").write_text(STATE)
    (g / "cards" / "p1.md").write_text("PIECE p1 · <person>, step 1: <name>\nBuilds: start, kitchen\n")
    approve.approve(g, "p1", "yes", date="2026-11-19")
    return g
