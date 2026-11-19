"""The writer session's screens (iterations/002/placeholders/NN_<canvas>_<node>.txt), read the way
beat_mark_table_*.txt is read: the build never hand-edits 7_final_game.toml, it swaps a node's
PLACEHOLDER block for the screen at emit time (canv.emit calls fill()).

LO, 2026-10-09: placeholders #1-3, #21-39 and #41-43 are filled; Laura's 18 (#4-20, #40) stay
PLACEHOLDER. The screen files are the writer's and are read, never written, here.

File format (the writer's): the text between "=== SCREEN" and "=== VARIANTS"/"=== MEASURED".
A blank line starts a new beat. A line that is only a quotation is a dialog block (its speaker
is given below, in reading order); a line with narration around a quotation stays a paragraph;
*text* is her thought. VARIANTS are written as groups on a gate; their placement is coded in
VARIANTS below, one entry per variant, as the file words it."""
import copy, os, re
from canv import P, D, ME, T, G, GC

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "..", "placeholders")
FILLED = set(range(1, 4)) | set(range(21, 40)) | set(range(41, 44))   # never #4-20, #40 (Laura)

NPC = {**{n: "npc_ryan" for n in (1, 2, 3, 34, 35, 38, 39, 43)},
       **{n: "npc_mark" for n in (21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 36, 37, 41, 42)},
       31: "npc_zoe", 32: "npc_hale", 33: "npc_hale"}
# Who says each quotation-only line of the SCREEN, in reading order: N = the person, M = her.
SPEAKERS = {2: "NM", 3: "M", 21: "NMN", 22: "N", 23: "NM", 24: "N", 25: "NM", 27: "N", 28: "NM",
            34: "NM", 35: "M", 36: "NM", 37: "N", 38: "NM", 39: "NM", 41: "N"}

ANY = {"type": "worn_exposure", "operator": "gte", "value": 0}          # always true: the chain's else
def wt(v): return {"type": "worn_type", "operator": "eq", "value": v}
def slot(s, on=True): return {"type": "clothing_slot", "slot": s, "operator": "equipped" if on else "unequipped"}
LAURA_IN_KITCHEN = {"type": "npc_at_location", "location_id": "home_kitchen", "npc_id": "npc_laura", "operator": "is_present"}
def corr(op, v): return {"type": "trait", "subject": "player", "trait_key": "corruption", "operator": op, "value": v}
def tod(a, b): return {"type": "time_of_day", "start_time": a, "end_time": b}
CLAIRE_MET = {"type": "flag", "subject": "player", "flag_key": "claire_met", "operator": "is_true"}
BRA_ONLY = [slot("top", False), slot("dress", False), slot("bra")]
TOPS_AND_BRAS = [{"action": "unequip", "item_id": i} for i in ("tshirt", "thin_top", "plain_bra", "sports_bra")]

# (file #, beat #, op, where, [conditions], [(speaker or None, line), ...])
#   op "after_beat": its own beat after beat N · "after_sentence" / "replace_sentence": in the beat's
#   first line, `where` = sentence number (1-based) or the sentence's text · "replace_lines": the
#   beat's quotation-only lines are replaced · "replace_line": the whole line holding sentence `where`.
VARIANTS = [
    (1, 1, "after_beat", None, [LAURA_IN_KITCHEN], [(None, "Your mom asks him to pass the salt. He passes it without looking at her, because he's looking at you.")]),
    (21, 1, "after_sentence", 1, [wt("sleep_shirt")], [(None, "Your sleep shirt rides up to the tops of your thighs when you stretch. He watches the hem, not the TV.")]),
    (22, 2, "replace_sentence", 1, [wt("sleep_shirt")], [(None, "You pull your sleep shirt off over your head and drop it on the floor.")]),
    (22, 1, "replace_lines", None, [wt("sleep_shirt")], [("N", '"Twenty. The shirt."')]),
    (25, 1, "replace_lines", None, [wt("sleep_shirt")], [(None, "Your sleep shirt slides down your thighs to your hips."),
                                                         ("N", '"Your mother lets you sit like that?"'), ("M", '"Like what?"'), ("N", '"Like that."')]),
    (26, 2, "replace_sentence", 1, [wt("sleep_shirt")], [(None, "You take the hem of your sleep shirt in both fists and lift it, slow, over your stomach, over your ribs, up over your tits.")]),
    (27, 1, "after_beat", None, [LAURA_IN_KITCHEN], [(None, "Your mom talks about her day. Mark nods at her and keeps his eyes on your mouth.")]),
    (29, 1, "after_sentence", 1, [wt("short_skirt")], [(None, "Your short skirt rides up the backs of your thighs.")]),
    (30, 2, "replace_sentence", 2, [wt("short_skirt")], [(None, "You reach back and flip your short skirt up over your ass.")]),
    (30, 2, "replace_sentence", 2, [wt("sleep_shirt")], [(None, "You reach back and pull your sleep shirt up over your ass.")]),
    (30, 2, "after_sentence", "Your ass is right there for him.", [slot("underwear")], [(None, "Your panties are pulled tight across it, and his eyes follow the cotton.")]),
    (30, 2, "after_sentence", "Your ass is right there for him.", [slot("underwear", False)], [(None, "There's nothing under it. Your ass is bare.")]),
    (35, 1, "replace_sentence", "His fingers slide around your sides and stay there.", [slot("bra")], [(None, "His fingers slide under your bra strap and stay under it.")]),
    (36, 1, "after_sentence", 1, [wt("shorts")], [(None, "Your shorts ride high on your legs.")]),
    (37, 2, "replace_sentence", 1, [slot("bra"), slot("top", False), slot("dress", False)],
     [(None, "You roll onto your front, reach back and unhook your bra. The straps fall loose to either side.")]),
    # ── Writer fix pass (LO, 2026-10-10) ──
    # 1 · clothes: the bra comes off with the sleep shirt when she wears one; the lift takes the bra with it;
    #     the dishes line names the garment she has on; the strap needs a bra; broad daylight needs the day.
    (22, 2, "replace_sentence", 1, [wt("sleep_shirt"), slot("bra")], [(None, "You pull your sleep shirt off over your head, reach back and unhook your bra, and drop both on the floor.")]),
    (26, 2, "replace_sentence", 1, [slot("top"), slot("bra")], [(None, "You take your hem in both fists and lift it, slow, with your bra caught up in it, over your stomach, over your ribs, up over your tits.")]),
    (26, 2, "replace_sentence", 1, [wt("sleep_shirt"), slot("bra")], [(None, "You take the hem of your sleep shirt in both fists and lift it, slow, over your stomach, over your ribs, and you push your bra up with it, over your tits.")]),
    (30, 2, "replace_sentence", 2, [wt("towel")], [(None, "You reach back and lift the towel up over your ass.")]),
    (30, 2, "replace_sentence", 2, [wt("cafe_uniform")], [(None, "You reach back and pull your uniform up over your ass.")]),
    (30, 2, "replace_sentence", 2, [wt("laura_dress")], [(None, "You reach back and pull the blue dress up over your ass.")]),
    (30, 2, "replace_sentence", 2, [wt("party_dress")], [(None, "You reach back and pull your dress up over your ass.")]),
    (35, 2, "replace_sentence", "Your step-brother's hands are on you out in the open garden.", [tod("07:00", "19:00")],
     [(None, "Your step-brother's hands are on you in broad daylight.")]),
    # 3 · Claire by name only once she's been met; otherwise his wife.
    (33, 2, "replace_sentence", '"My wife\'s here at half past."', [CLAIRE_MET], [(None, '"Claire\'s here at half past."')]),
    # 5 · at Curious her voice pushes back a little (SP2 stage 2, "warming up"); Bold and up keep the screen's voice.
    (2, 1, "replace_lines", None, [corr("lt", 40)], [("N", '"You\'re distracting me, @player.nickname."'), ("M", '"Then I\'ll move them."')]),
    (2, 2, "replace_line", "He wants this.", [corr("lt", 40)],
     [(None, "*This is Ryan. Your step-brother. You should take your feet back. He picks the controller back up one-handed, and the other hand stays on you, so you leave them where they are.*")]),
    (21, 2, "replace_sentence", "Let him count.", [corr("lt", 40)],
     [(None, "He's your mom's husband. You should tuck your legs back under you. You don't.")]),
    (25, 2, "replace_sentence", "Let him look.", [corr("lt", 40)],
     [(None, "You think about putting your feet down. You keep them where they are.")]),
]

# Unconditional changes to the screen's own text, made before the variants: (file #, old, new).
EDITS = [
    (26, "The rent is seventy-five.", "That's a piece of the rent."),               # 2 · the rent rises; no number
    (33, '"Claire\'s here at half past."', '"My wife\'s here at half past."'),         # 3 · the base is his wife
    (35, "His fingers slide under the strap and stay under it.", "His fingers slide around your sides and stay there."),  # 1 · no bra, no strap
    (35, "Your step-brother's hands are on you in broad daylight.", "Your step-brother's hands are on you out in the open garden."),
]

# 6 · a forward hook, appended to the screen's last beat: (file #, line).
HOOKS = [
    (1, "*After dinner he'll go up to his room. You wonder if he'll leave his door open tonight.*"),
    (23, "*Next time you bring your washing down, you'll leave something smaller on top.*"),
    (24, "*He'll be at that bench the next time you bring your basket down. You already know you'll let him fold them again.*"),
    (41, "*Next time he wants something off that shelf, you'll be standing right under it.*"),
    (42, "*Tomorrow he'll act like it never happened. You want to see if he can.*"),
]

# 4 · the paid looks' second voice: SP2's "warming up" (shocked, honest, then she does it) under Hungry,
# the bold voice from Hungry (stage 4) up. Its own beat after beat N: (file #, beat #, [(conds, line)]).
VOICES = [
    (22, 1, [([corr("gte", 60)], "*You were waiting for him to ask. You'd have done it for ten.*"),
             ([corr("lt", 60)], "*Your step-father wants you to strip for twenty dollars. Your face goes hot, and your hands go to your clothes anyway.*")]),
    (24, 1, [([corr("gte", 60)], "*You lean back on the washer to watch. You want him to take his time.*"),
             ([corr("lt", 60)], "*He's going to fold those panties in front of you, and you're going to let him. Your face is burning.*")]),
    (26, 1, [([corr("gte", 60)], "*You put your coffee down. You were hoping he'd ask.*"),
             ([corr("lt", 60)], "*Your step-father, at the breakfast table. Your face goes hot, and you reach for your hem anyway.*")]),
    (30, 1, [([corr("gte", 60)], "*You were already bent over for him. Now he's paying for it.*"),
             ([corr("lt", 60)], "*He wants you to stay bent over for him. Your face burns over the dishwasher. You don't stand up.*")]),
    (37, 1, [([corr("gte", 60)], "*The fence is low. You don't care who's on the other side of it.*"),
             ([corr("lt", 60)], "*Out here, in the open, and the fence is low. Your heart's going fast, and you do it anyway.*")]),
]

# The catch-all of a screen whose own lines name her clothes is the check its choice already makes,
# so the line sits behind a garment check and not worn_exposure (gate: her clothes are named exactly).
GUARD = {36: BRA_ONLY, 37: [slot("dress", False)]}

# The choices into a screen, split by what she wears so each screen's lines are true: (canvas, node) ->
# [(extra condition items, wardrobe effects or None)]; each choice into the node is copied once per entry.
CHOICES = {
    # "You strip to the waist": the top and the bra come off; a sleep shirt comes off whole; no dress.
    ("hub_mark_living_room", "hl_beer_touch"): [([slot("dress", False)], TOPS_AND_BRAS),
                                                ([wt("sleep_shirt")], [{"action": "unequip", "item_id": i} for i in ("sleep_shirt", "plain_bra", "sports_bra")])],
    # the lift needs a hem: a top or the sleep shirt
    ("hub_mark_kitchen", "hl_breakfast_touch"): [([slot("top"), slot("dress", False)], None), ([wt("sleep_shirt")], None)],
    # "stay bent": something on her bottom half for the screen to name
    ("hub_mark_kitchen", "hl_dishes_touch"): [([slot("bottom")], None), ([slot("dress")], None)],
    # the lotion goes on a bare back, down to a waistband: no top, no dress
    ("garden_sun", "sun_ryan_touch"): [([slot("top", False), slot("dress", False)], None)],
    # "strip to the waist" on the grass: the top and the bra come off; no dress
    ("garden_sun", "sun_mark_paid"): [([slot("dress", False)], TOPS_AND_BRAS)],
}

SENT = re.compile(r'(?<=[.!?])\s+(?=[A-Z"*])')
PURE_QUOTE = re.compile(r'"[^"]*"')


def _screen(path):
    text = open(path, encoding="utf-8").read()
    body = text.split("=== SCREEN", 1)[1].split("\n", 1)[1]
    body = re.split(r"\n=== (?:VARIANTS|MEASURED)", body)[0]
    beats, cur = [], []
    for raw in body.splitlines():
        line = raw.strip()
        if not line:
            if cur:
                beats.append(cur)
                cur = []
            continue
        cur.append(line)
    if cur:
        beats.append(cur)
    return beats


def _speak(n, line, speaker):
    """One line to one block."""
    if line.startswith("*") and line.endswith("*"):
        return T(line.strip("*"))
    if PURE_QUOTE.fullmatch(line):
        inner = line[1:-1]
        return ME(inner) if speaker == "M" else D(NPC[n], inner)
    return P(line)


def _apply(lines, spk, op, where, new):
    """One variant applied to a beat's lines (with their speakers). Returns (lines, speakers)."""
    lines, spk = list(lines), list(spk)
    if op == "replace_lines":
        idx = [i for i, l in enumerate(lines) if PURE_QUOTE.fullmatch(l)]
        assert idx and idx == list(range(idx[0], idx[-1] + 1)), "spoken lines must be one run"
        return (lines[:idx[0]] + [l for _, l in new] + lines[idx[-1] + 1:],
                spk[:idx[0]] + [s for s, _ in new] + spk[idx[-1] + 1:])
    # a sentence number counts in the beat's first line; a sentence's text is found in any of its lines
    li = 0 if isinstance(where, int) else next(i for i, l in enumerate(lines) if where in SENT.split(l.strip("*")))
    if op == "replace_line":                     # the whole line that holds the sentence
        assert len(new) == 1
        return lines[:li] + [new[0][1]] + lines[li + 1:], spk[:li] + [new[0][0]] + spk[li + 1:]
    thought = lines[li].startswith("*") and lines[li].endswith("*")
    sents = SENT.split(lines[li].strip("*") if thought else lines[li])
    k = (where - 1) if isinstance(where, int) else sents.index(where)
    text = " ".join(l for _, l in new)
    if op == "replace_sentence":
        sents[k] = text
    elif op == "after_sentence":
        sents.insert(k + 1, text)
    lines[li] = ("*" + " ".join(sents) + "*") if thought else " ".join(sents)
    return lines, spk


def _edit(beats, n):
    """EDITS and HOOKS on the screen's own text, before anything reads it."""
    for m, old, new in EDITS:
        if m == n:
            hits = [(bi, li) for bi, b in enumerate(beats) for li, l in enumerate(b) if old in l]
            assert len(hits) == 1, f"#{n}: edit {old!r} found {len(hits)} times"
            bi, li = hits[0]
            beats[bi][li] = beats[bi][li].replace(old, new)
    for m, line in HOOKS:
        if m == n:
            beats[-1].append(line)
    return beats


def _blocks(n):
    beats = _edit(_screen(_files()[n]), n)
    any_ = GUARD.get(n, [ANY])
    order = iter(SPEAKERS.get(n, ""))
    spk_beats = [[next(order) if PURE_QUOTE.fullmatch(l) else None for l in b] for b in beats]
    assert next(order, None) is None, f"#{n}: more speakers given than quotation-only lines"
    out = []
    for bi, (lines, spk) in enumerate(zip(beats, spk_beats), 1):
        mine = [v for v in VARIANTS if v[0] == n and v[1] == bi and v[2] != "after_beat"]
        if not mine:
            out += [_speak(n, l, s) for l, s in zip(lines, spk)]
        else:
            # slots: variants at the same spot are alternatives; the chain is every combination,
            # most conditions first, the plain beat last (ANY): adjacent groups are one if/elseif.
            slots = {}
            for v in mine:
                slots.setdefault((v[2] == "replace_lines", v[3]), []).append(v)
            combos = [([], [])]
            for alts in slots.values():
                combos = [(c + [None], a) for c, a in combos] + [(c + [v], a + v[4]) for c, a in combos for v in alts]
            chain = []
            for picks, conds in sorted(combos, key=lambda x: -len(x[1])):
                ls, ss = lines, spk
                for v in picks:
                    if v:
                        ls, ss = _apply(ls, ss, v[2], v[3], v[5])
                chain.append(GC({"version": "1.0", "logic": "AND", "items": conds or any_},
                                *[_speak(n, l, s) for l, s in zip(ls, ss)]))
            out.append(G({"version": "1.0", "logic": "AND", "items": any_}, *chain))   # its own chain
        for v in VARIANTS:
            if v[0] == n and v[1] == bi and v[2] == "after_beat":
                out.append(G({"version": "1.0", "logic": "AND", "items": v[4]}, *[_speak(n, l, s) for s, l in v[5]]))
        for m, at, alts in VOICES:
            if m == n and at == bi:
                # wrapped in the paid look's own Bold check (its choice needs it), not a clothing level
                out.append(G({"version": "1.0", "logic": "AND", "items": GUARD.get(n, [corr("gte", 40)])},
                             *[GC({"version": "1.0", "logic": "AND", "items": c}, _speak(n, line, None)) for c, line in alts]))
    return out


_FILES = None
def _files():
    global _FILES
    if _FILES is None:
        _FILES = {}
        for f in sorted(os.listdir(DIR)):
            m = re.match(r"(\d\d)_.*\.txt$", f)
            if m:
                _FILES[int(m.group(1))] = os.path.join(DIR, f)
    return _FILES


def _key(n):
    """(canvas, node) from the file name: NN_<canvas>_<node>.txt, node = the last of the known ids."""
    stem = os.path.basename(_files()[n])[3:-4]
    for node in ("hl_dinner_tease", "hl_tv_tease", "hl_tv_touch", "hl_beer_tease", "hl_beer_touch", "hl_laundry_tease",
                 "hl_laundry_touch", "hl_breakfast_tease", "hl_breakfast_touch", "hl_cook_tease", "hl_dishes_tease",
                 "hl_dishes_touch", "kiss_bare", "hand", "sun_ryan_tease", "sun_ryan_touch", "sun_mark_tease",
                 "sun_mark_paid", "ev_curious", "ev_bold"):
        if stem.endswith("_" + node):
            return stem[: -len(node) - 1], node
    raise ValueError(stem)


_SCREENS = None
def screens():
    """{(canvas, node): (file #, blocks)} for every filled placeholder."""
    global _SCREENS
    if _SCREENS is None:
        _SCREENS = {_key(n): (n, _blocks(n)) for n in sorted(_files()) if n in FILLED}
    return _SCREENS


def _swap(blocks, new):
    out, hit = [], 0
    for b in blocks or []:
        if b.get("type") == "paragraph" and str(b.get("content", "")).startswith("PLACEHOLDER —"):
            out += new
            hit += 1
            continue
        if b.get("blocks"):
            inner, h = _swap(b["blocks"], new)
            if h:
                b = dict(b, blocks=inner)
                hit += h
        out.append(b)
    return out, hit


USED, SPLIT = set(), set()
def fill(canvas):
    """Swap each filled node's PLACEHOLDER block for the writer's screen (called by canv.emit)."""
    for node in canvas.get("nodes") or []:
        hit = screens().get((canvas.get("id"), node.get("id")))
        if hit:
            n, new = hit
            node["blocks"], h = _swap(node["blocks"], new)
            assert h == 1, f"#{n} {canvas['id']}.{node['id']}: expected one PLACEHOLDER block, found {h}"
            USED.add(n)
    for node in canvas.get("nodes") or []:
        out = []
        for ch in node.get("choices") or []:
            split = CHOICES.get((canvas.get("id"), str(ch.get("nodeId") or "")))
            if not split or ch.get("targetType") != "node":
                out.append(ch)
                continue
            for extra, wardrobe in split:
                c = copy.deepcopy(ch)
                cc = c.get("conditions") or {"version": "1.0", "logic": "AND", "items": []}
                assert cc.get("logic", "AND") == "AND"
                c["conditions"] = dict(cc, items=list(cc.get("items") or []) + list(extra))
                if wardrobe:
                    c["wardrobeEffects"] = list(c.get("wardrobeEffects") or []) + wardrobe
                out.append(c)
            SPLIT.add((canvas.get("id"), ch.get("nodeId")))
        node["choices"] = out
    return canvas
