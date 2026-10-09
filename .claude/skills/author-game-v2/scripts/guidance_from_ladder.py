#!/usr/bin/env python3
"""
guidance_from_ladder.py — one quest card per ladder step, with place and time.

Usage:
    python3 scripts/guidance_from_ladder.py <game-slug>              # TOML to stdout
    python3 scripts/guidance_from_ladder.py <slug> --out PATH        # TOML to a scratch file
    python3 scripts/guidance_from_ladder.py <path/to/game.toml> --state PATH

WHY. The field's best guidance is one line per character step that says WHERE and
WHEN (Round 3 §2.5; being lost is the genre's top complaint). The skill used to key
cards to meter bands, which tells the player a number and not a place. Every step in
`board.characters[].ladder` already declares its canvas, its place and its window, so
the mechanical half of each card is generated here and the author writes only the
words (`the-voice.md` R2).

What it writes, per person with a ladder:
    one card per step n — `when` = counter eq n-1; `goals` = the step's real gate (each
    meter with its number, each of their own numbers, each flag as words to write), never
    the counter itself, which renders "— n-1 / n" and tells the player nothing (B84, B110;
    gate `a card shows the real gates`); a `tip` naming the place and the window, plus any
    gate a goal cannot show (another person's step, a modifier); `ready_canvas` = the
    step's canvas, so when every goal is met the card prints Ready with the place and the
    hours (v2.py:18008-18011); and a placeholder `text` (this script writes no prose);
    one terminal card after the last step.
    Goals can be a flag, a trait (hers, or theirs with `npc_id`), days or hours since a
    flag, or a weekday (template_import.py:1290-1316); nothing else can be a goal.

With no built TOML yet (the board and sheets phases, B52) it reads the ledger alone and
names places and people by id.

It writes TOML only, to stdout or `--out`, and REFUSES any path inside `games/`: the
author pastes the cards into a phase file after writing their lines. Always exits 0
unless the arguments are wrong.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gates  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
DAYS = gates._PR_DAYS


def _q(s):
    return json.dumps(str(s), ensure_ascii=False)


def days_phrase(days):
    """'every day' · 'weekdays' · 'weekends' · 'Mon, Wed' from day names or 0-6."""
    idx = sorted({d for d in (gates._ladder_day(x) for x in days or []) if d is not None})
    if idx == list(range(7)):
        return "every day"
    if idx == [0, 1, 2, 3, 4]:
        return "weekdays"
    if idx == [5, 6]:
        return "weekends"
    return ", ".join(DAYS[i] for i in idx)


def place_time(step, loc_names):
    where = step.get("where") or ""
    when = step.get("when") or {}
    place = loc_names.get(where) or where or "<place>"
    window = f"{when.get('from', '')}–{when.get('to', '')}".strip("–")
    hours = f"{days_phrase(when.get('days')) if when else ''} {window}".strip()
    return f"{place}, {hours}" if hours else place


def _num(v):
    return int(v) if isinstance(v, float) and v.is_integer() else v


def goals_and_notes(gate, counters, trait_names, npc_names):
    """(goal TOML items, tip notes) for a step's `gate` list (state.md:432)."""
    goals, notes = [], []
    for it in gate or []:
        if not isinstance(it, dict):
            continue
        if it.get("type") == "modifier":
            notes.append(f"not while {it.get('modifier_key')} is "
                         f"{'on' if it.get('operator') == 'is_inactive' else 'off'}")
            continue
        if it.get("flag"):
            op = it.get("op") or "is_true"
            goals.append(f"{{ flag = {_q(it['flag'])}, op = {_q(op)}, "
                         f"label = {_q('<what she has done: ' + it['flag'] + ' — write it>')} }}")
            continue
        key = it.get("trait")
        if not key:
            continue
        who = it.get("npc")
        if key in counters and counters[key] != who:
            owner = counters[key]
            notes.append(f"after {npc_names.get(owner, owner)}'s step {_num(it.get('value'))}")
            continue
        name = trait_names.get(key, key)
        if who:
            label = f"{npc_names.get(who, who)}'s {name} {_num(it.get('value'))}"
            goals.append(f"{{ type = \"trait\", subject = \"npc\", npc_id = {_q(who)}, trait = {_q(key)}, "
                         f"op = {_q(it.get('op'))}, value = {_num(it.get('value'))}, label = {_q(label)} }}")
        else:
            label = f"{name} {_num(it.get('value'))}"
            goals.append(f"{{ type = \"trait\", subject = \"player\", trait = {_q(key)}, "
                         f"op = {_q(it.get('op'))}, value = {_num(it.get('value'))}, label = {_q(label)} }}")
    return goals, notes


def cards_for(who, ladder, loc_names, npc_names, counters=None, trait_names=None):
    counter = ladder.get("counter")
    counters = dict(counters or {}, **{counter: who})
    steps = sorted(ladder.get("steps") or [], key=lambda s: s.get("n", 0))
    out = [f"# ── {npc_names.get(who, who)} — {len(steps)} step(s), counter `{counter}` "
           f"(generated by guidance_from_ladder.py; write every <…> before pasting) ──"]
    for s in steps:
        n = s.get("n")
        pt = place_time(s, loc_names)
        goals, notes = goals_and_notes(s.get("gate"), counters, trait_names or {}, npc_names)
        tip = pt + ("; " + "; ".join(notes) if notes else "")
        out += [
            "",
            "[[quest_cards]]",
            f"npc_id       = {_q(who)}",
            f"text         = {_q('<her line for step ' + str(n) + ' — write it>')}",
            f"tip          = {_q(tip)}",
            f"when         = [ {{ type = \"trait\", subject = \"player\", trait = {_q(counter)}, "
            f"op = \"eq\", value = {n - 1} }} ]",
            f"goals        = [ {', '.join(goals)} ]",
            f"ready_canvas = {_q(s.get('canvas') or '')}",
        ]
    if steps:
        k = steps[-1].get("n")
        out += [
            "",
            "[[quest_cards]]",
            f"npc_id        = {_q(who)}",
            f"text          = {_q('<where she stands with them after the last step — write it>')}",
            f"when          = [ {{ type = \"trait\", subject = \"player\", trait = {_q(counter)}, "
            f"op = \"gte\", value = {k} }} ]",
            "terminal      = true",
            f"terminal_text = {_q('<what the next release opens — the-voice.md R5>')}",
        ]
    return out


def generate(game, state):
    """The TOML text for every declared ladder, or '' when none is declared."""
    board = (state or {}).get("board") or {}
    loc_names = {l.get("id"): l.get("name") or l.get("id")
                 for l in list(board.get("locations") or []) + list(game.get("locations") or [])
                 if isinstance(l, dict)}
    npc_names = {n.get("id"): n.get("name") or n.get("id")
                 for n in list(board.get("characters") or []) + list(game.get("npcs") or [])
                 if isinstance(n, dict)}
    trait_names = {t.get("key"): t.get("label") for t in ((game.get("traits") or {}).get("labels") or [])
                   if isinstance(t, dict) and t.get("key") and t.get("label")}
    ladders = gates._declared_ladders(state)
    counters = {lad.get("counter"): who for who, lad in ladders if lad.get("counter")}
    blocks = []
    for who, lad in ladders:
        blocks.append("\n".join(cards_for(who, lad, loc_names, npc_names, counters, trait_names)))
    return "\n\n".join(blocks) + ("\n" if blocks else "")


def under_games(path):
    games = os.path.realpath(os.path.join(REPO, "games"))
    p = os.path.realpath(path)
    return p == games or p.startswith(games + os.sep)


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    opts = {}
    for flag in ("--out", "--state"):
        if flag in args:
            i = args.index(flag)
            opts[flag] = args[i + 1] if i + 1 < len(args) else ""
            del args[i:i + 2]
    if not args:
        print(__doc__)
        return 2
    arg = args[0]
    if arg.endswith(".toml"):
        toml_path = arg
        state_path = opts.get("--state") or os.path.join(
            os.path.dirname(os.path.dirname(arg)), "v2_state.json")
    else:
        toml_path = os.path.join(REPO, "games", arg, "toml_phases", "7_final_game.toml")
        state_path = opts.get("--state") or os.path.join(REPO, "games", arg, "v2_state.json")
    out = opts.get("--out")
    if out is not None and under_games(out):
        print(f"refused: {out} is inside games/ — write to a scratch file and paste the cards "
              f"into a phase file after writing their lines")
        return 2
    state = json.load(open(state_path, encoding="utf-8")) if os.path.exists(state_path) else {}
    if os.path.exists(toml_path):
        game = gates._load(toml_path)
    elif state:
        game = {}          # B52: before the build, the ledger alone (names fall back to ids)
        print(f"# no build yet ({os.path.relpath(toml_path, REPO)}): cards from the ledger alone",
              file=sys.stderr)
    else:
        print(f"not found: {toml_path}")
        return 2
    text = generate(game, state)
    if not text:
        print("no ladder declared — nothing to generate (board.characters[].ladder, state.md)")
        return 0
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {text.count('[[quest_cards]]')} card(s) to {out}")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
