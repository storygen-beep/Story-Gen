"""Play every declared ladder with playtest.reach_step (the same call gates.py --ship makes)
and print one line per step. Usage: python3 reach_all.py [npc ...]"""
import json, os, sys
ROOT = "/Users/a0000/Desktop/Desktop_Archive_Backup/story_gen/story_gen_web_app/story_gen_django"
sys.path.insert(0, os.path.join(ROOT, ".claude/skills/author-game-v2/scripts"))
import playtest  # noqa

# ⚠️ harness gap (logged as a B-item): the starting canvas's passages are named
# StartingCanvas_<id>_Node_<node>, and playtest.play / reach_step only know Canvas_.
# Patched HERE, in the scratch driver, never in the skill.
_orig_passage = playtest.passage
def _passage(page):
    p = _orig_passage(page)
    return p[len("Starting"):] if isinstance(p, str) and p.startswith("StartingCanvas_") else p
playtest.passage = _passage
_orig_play = playtest.play
def _play(page, canvas, node="base", settle=250, tries=12):
    start = "StartingCanvas_%s_Node_%s" % (canvas, node)
    if page.evaluate("(n) => SugarCube.Story.has(n)", start):
        page.evaluate("(n) => SugarCube.Engine.play(n)", start)
        page.wait_for_timeout(settle)
        return True
    return _orig_play(page, canvas, node, settle, tries)
playtest.play = _play

build = os.path.join(ROOT, "games/first_term/output/index.html")
toml = os.path.join(ROOT, "games/first_term/toml_phases/7_final_game.toml")
state = json.load(open(os.path.join(ROOT, "games/first_term/v2_state.json")))
game = playtest._load(toml)
only = set(sys.argv[1:])
total = reached = 0
for ch in state["board"]["characters"]:
    lad = ch.get("ladder")
    if not lad or (only and ch["id"] not in only):
        continue
    with playtest.open_game(build) as (page, errors):
        res = playtest.reach_step(page, game, lad, len(lad["steps"]))
    for r in res:
        total += 1
        reached += bool(r["reached"])
        print(f"{ch['id']:10s} step {r['n']}  {'REACHED' if r['reached'] else 'NOT    '}  {r['canvas']:34s} clicks={r['clicks']} {r['why']}")
    missing = len(lad["steps"]) - len(res)
    if missing:
        print(f"{ch['id']:10s} … {missing} later step(s) not tried (the ladder stopped)")
    if errors:
        print("   page errors:", errors[:3])
print(f"\n{reached}/{total} steps tried were reached")
