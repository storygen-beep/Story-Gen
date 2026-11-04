"""Scene-writing helpers for the first_term build: Python data in, TOML text out.

A canvas is a dict; nodes hold blocks and choices. step() builds a ladder step's
trigger straight from the ledger's declared step (place, window, gate, counter), so
the canvas and the declaration cannot drift (gates.py `ladders move forward`).
"""
import json
import re
from tomlw import q, v, cond, flag, trait, ntrait, boost_off, add, setv, nadd, fset, funset, DAYS

# A lock on a scene release 1 does not write (DECISIONS 124) was shown greyed as "(Next release)"; LO 2026-11-03
# ("(Next release) no dont even show the option"): those buttons are gone. The counter stays for the gate code below.
# Release 1 now reaches Corruption 60, so a "(Needs Corruption 60)" lock would open onto "It comes later".
# A hidden counter gated at 1: the engine prints "(Corruption N+ (you have M))" beside a locked trait
# gate only when its value is 2 or more (v2.py:16462-16468), and a flag gate fails the build's
# flag-chain check unless something sets it. Nothing raises this counter in release 1.
NEXT_RELEASE = trait("release_2_written", "gte", 1)
NEXT_RELEASE_TEXT = "That's in the next release of First Term."

STATE = json.load(open("/Users/a0000/Desktop/Desktop_Archive_Backup/story_gen/story_gen_web_app/story_gen_django/games/first_term/v2_state.json"))
LADDERS = {c["id"]: c["ladder"] for c in STATE["board"]["characters"] if c.get("ladder")}


# ── blocks ──
def P(text, **props):
    """props: e.g. not_speech=True on a paragraph whose quote is a sign, a text message or code, not a voice."""
    b = {"type": "paragraph", "content": text}
    if props:
        b["props"] = props
    return b


def D(npc, text):
    return {"type": "dialog", "content": text, "props": {"speaker": "npc", "npcId": npc}}


def ME(text):
    return {"type": "dialog", "content": text, "props": {"speaker": "player"}}


def WHO(text):
    return {"type": "dialog", "content": text, "props": {"speaker": "unknown"}}


# ── speech (skill register.md "Speech is a UI component", LO 2026-11-03) ──
# Every spoken line is a dialog block with its speaker; a quote inside a paragraph counts as narration.
# The signed beats write speech as quotes inside paragraphs. speech() keeps every word: it cuts the paragraph
# at each quote, drops the quote marks, turns a trailing comma inside the quote into a period, and capitalises
# a narration fragment that now starts a block. Nothing else changes.
QUOTE_RX = re.compile(r'("[^"]+")')
SPOKEN_RX = re.compile(r'"[A-Z@][^"]{3,}"')   # the scan that finds a paragraph still carrying speech
NOT_SPEECH = "TEXT"   # speaker code: the quote is a sign, a text on a screen, a note or code, and stays inline
UNKNOWN = "?"         # speaker code: a stranger with no NPC (WHO, speaker "unknown")


def _say(code, line):
    if code == "ME":
        return ME(line)
    if code == UNKNOWN:
        return WHO(line)
    assert code.startswith("npc_"), code
    return D(code, line)


def speech(text, speakers):
    """One paragraph's text in, a block list out: narration and dialog in the order of the text.
    `speakers` names each quote in order: "ME", an npc id, UNKNOWN, or NOT_SPEECH (kept inside the paragraph,
    which is then marked not_speech)."""
    parts = QUOTE_RX.split(text)
    quotes = [x for x in parts if x.startswith('"') and x.endswith('"') and len(x) > 1]
    assert len(quotes) == len(speakers), (text[:60], len(quotes), list(speakers))
    blocks, buf, inline, i = [], "", False, 0

    def flush():
        nonlocal buf, inline
        frag = buf.strip()
        if frag:
            frag = frag[0].upper() + frag[1:]
            blocks.append(P(frag, not_speech=True) if inline else P(frag))
        buf, inline = "", False

    for part in parts:
        if part.startswith('"') and part.endswith('"') and len(part) > 1:
            code = speakers[i]; i += 1
            if code == NOT_SPEECH:
                buf += part; inline = True
                continue
            flush()
            line = part[1:-1].strip()
            if line.endswith(","):
                line = line[:-1] + "."
            blocks.append(_say(code, line))
        else:
            buf += part
    flush()
    return blocks


def _voice_blocks(blocks, table, cid, in_pool=False):
    out = []
    for b in blocks:
        if b.get("type") == "paragraph" and SPOKEN_RX.search(b.get("content", "")) \
                and not (b.get("props") or {}).get("not_speech"):
            quotes = [x[1:-1] for x in QUOTE_RX.findall(b["content"])]
            if table is None or not all(x in table for x in quotes):
                missing = [x for x in quotes if table is None or x not in table]
                if table is not None:
                    raise KeyError(f"{cid}: no speaker for {missing} (speech_table.py)")
                print(f"speech: {cid}: paragraph still quotes {missing[:2]} (no speech_table entry)", file=__import__("sys").stderr)
                out.append(b)
                continue
            new = [x for p in speech(b["content"], [table[x] for x in quotes]) for x in thought_split(p)]
            if in_pool and len(new) > 1:   # a pool entry is ONE block: keep the cut lines together
                new = [GC({"version": "1.0", "logic": "AND", "items": []}, *new)]
            out.extend(new)
            continue
        if b.get("type") == "paragraph" and THOUGHT_RX.search(b.get("content", "")):
            new = thought_split(b)
            if in_pool and len(new) > 1:
                new = [GC({"version": "1.0", "logic": "AND", "items": []}, *new)]
            out.extend(new)
            continue
        if b.get("blocks"):
            b = dict(b, blocks=_voice_blocks(b["blocks"], table, cid, b.get("type") == "block_pool"))
        out.append(b)
    return out


# ── her thought is a thought block (skill register.md :32-33, :855-856; pass 3 B6, 2026-11-03) ──
# The signed beats write her thought as *italics* inside the paragraph, where the thought-vs-speech lint can't
# see it and the screen shows it as narration. thought_split() cuts the paragraph at each italic span the way
# speech() cuts at quotes: narration, then T(the thought, without the asterisks), then narration. Every word
# stays. A span that starts lower-case is text on a screen (a phone message, a sticky note), not her voice,
# and stays inside the paragraph.
THOUGHT_RX = re.compile(r"\*([A-Z][^*]*)\*")


def thought_split(b):
    if b.get("type") != "paragraph" or not THOUGHT_RX.search(b.get("content", "")):
        return [b]
    props = {k: v for k, v in (b.get("props") or {}).items()}
    out = []
    for i, part in enumerate(THOUGHT_RX.split(b["content"])):
        part = part.strip()
        if not part:
            continue
        if i % 2:
            out.append(T(part))
        else:
            out.append(dict(P(part[0].upper() + part[1:]), **({"props": props} if props else {})))
    return out


def voice_canvas(canvas):
    """Apply speech_table.SPEECH to every quoted paragraph of a canvas (called by emit)."""
    from speech_table import SPEECH
    table = SPEECH.get(canvas.get("id"))
    for n in canvas.get("nodes") or []:
        n["blocks"] = _voice_blocks(n["blocks"], table, canvas.get("id"))
    return canvas


def T(text):
    return {"type": "thought_bubble", "content": text, "props": {"speaker": "player"}}


def G(c, *blocks):
    """A group that stands alone. Wrapped in a one-item block_pool, because ADJACENT groups
    render as one if/elseif chain (v2.py:17138-17146) and a one-item pool renders its child
    directly (v2.py:17153-17155): the wrapper breaks the chain and adds no randomness."""
    return {"type": "block_pool", "blocks": [{"type": "group", "conditions": c, "blocks": list(blocks)}]}


def GC(c, *blocks):
    """A group meant to chain with the groups beside it (mutually exclusive bands)."""
    return {"type": "group", "conditions": c, "blocks": list(blocks)}


def top_or_dress(text):
    """A signed beat says "your top"; in a dress-slot item that's "your dress" (reader, 2026-11-01). Two flat groups."""
    if "your top" not in text:
        return [P(text)]
    return [G(cond(*[{"type": "clothing_item", "item_id": d, "operator": "unequipped"} for d in DRESSES]), P(text))] + \
           [G(cond({"type": "clothing_item", "item_id": d, "operator": "equipped"}), P(text.replace("your top", "your dress"))) for d in DRESSES]

DRESSES = ("zoe_party_dress", "laura_blue_dress")   # the two dresses she goes out in


def POOL(*blocks, pid=None, bag=False):
    """bag=True: a shuffle bag, no entry repeats until all have shown (seen_weight = 0, DECISIONS 112)."""
    b = {"type": "block_pool", "blocks": list(blocks)}
    if pid:
        b["props"] = {"id": pid, "memory": "seen"}
        if bag:
            b["props"]["seen_weight"] = 0
    return b


def IMG(file, desc, *queries):
    return {"type": "image", "props": {"file": file, "description": desc, "search_queries": list(queries)}}


def VID(desc, *queries, file=None, pool_dir=None):
    props = {"description": desc, "search_queries": list(queries)}
    if pool_dir:
        props["pool_dir"] = pool_dir
    else:
        props["file"] = file
    return {"type": "video", "props": props}


def odds_bands(meter, chance):
    """(pass 3 D52, the-surfaces.md R3: "the odds ride the same trait as the content") a walk-in's substitution odds
    in three bands on HER meter that its answers pay: under 20, 20-39, 40 and up (the stage lines). The lowest band
    keeps the signed odds (DECISIONS 148: 0.25, or 0.5 with C4's unlocked door or C2's loud TV); the world leans
    x1.4 and x1.8 as she climbs, never past 0.9. Returns [(chance, condition items)], mutually exclusive.
    `meter` None: a walk-in with no heat and no pay keeps one flat rule."""
    if not meter:
        return [(chance, [])]
    return [(chance, [trait(meter, "lt", 20)]),
            (min(0.9, round(chance * 1.4, 2)), [trait(meter, "gte", 20), trait(meter, "lt", 40)]),
            (min(0.9, round(chance * 1.8, 2)), [trait(meter, "gte", 40)])]


def own_media(tree, tag):
    """(pass 3 B37, register.md "ONE ASSET, ONE BLOCK") give every media block in a COPIED canvas or node list its
    own asset: `_<tag>` goes in before the tier suffix (sex/x_t4 -> sex/x_<tag>_t4; a file keeps its extension).
    The media review dedupes by file, so a copy sharing the original's asset would never get its own verdict."""
    if isinstance(tree, list):
        for x in tree:
            own_media(x, tag)
    elif isinstance(tree, dict):
        props = tree.get("props") if tree.get("type") in ("video", "image") else None
        if isinstance(props, dict):
            for k in ("pool_dir", "file"):
                if props.get(k):
                    props[k] = re.sub(r"(_t\d)((?:\.\w+)?)$", rf"_{tag}\1\2", props[k], count=1) \
                        if re.search(r"_t\d(?:\.\w+)?$", props[k]) else re.sub(r"((?:\.\w+)?)$", rf"_{tag}\1", props[k], count=1)
        for x in tree.values():
            own_media(x, tag)
    return tree


# ── choices ──
def with_duration(text, mins):
    """the-clock.md C4 (pass 3 H28): a click that moves the clock an hour or more says how long, in brackets, in
    one form ("Clock out (3h).", "Pack up (1h 30m)."). The tag is built from the same `mins` the choice charges,
    so it cannot drift from the spend (gate `the label keeps its time`). A spoken line keeps its quote whole."""
    h, m = divmod(int(mins), 60)
    tag = f"({h}h{f' {m}m' if m else ''})"
    t = text.rstrip()
    if t.endswith(".") and not t.endswith('."'):
        return f"{t[:-1]} {tag}."
    return f"{t} {tag}"


def go(text, node=None, loc=None, mins=None, eff=None, flags=None, cond_=None, wardrobe=None,
       costs=None, locked=None, swl=False, consumes=False, final=False, retry=None, ret=False, mods=None):
    if mins is not None and mins >= 60 and not re.search(r"\(\s*\d", text):
        text = with_duration(text, mins)
    c = {"text": text}
    if node:
        c["targetType"] = "node"
        c["nodeId"] = node
    elif ret:
        c["targetType"] = "return"
    else:
        c["targetType"] = "location"
        c["locationId"] = loc
    if mins is not None:
        c["time_progression_minutes"] = mins
    if cond_:
        c["conditions"] = cond_
    if swl:
        c["show_when_locked"] = True
    if locked:
        c["locked_text"] = locked
    elif swl and cond_ and NEXT_RELEASE in (cond_.get("items") or []):
        c["locked_text"] = text   # a story lock says its why in its own label (gates: a locked door says why)
    if costs:
        c["costs"] = costs
    if eff:
        c["effects"] = eff
    if flags:
        c["flagEffects"] = flags
    if wardrobe:
        c["wardrobeEffects"] = wardrobe
    if mods:
        c["modifier_effects"] = mods
    if consumes:
        c["consumes"] = True
    if final:
        c["final"] = True
    if retry is not None:
        c["retry_after_days"] = retry
    return c


def node(nid, name, blocks, choices):
    return {"id": nid, "name": name, "blocks": blocks, "choices": choices}


# ── the late flags (Q69, iteration 002 part 3) ──
# Each outing that ends after 22:00 sets its own flag (late_party, late_shift, late_date) and, with it,
# came_home_late; the street never does (LO, 2026-10-09, DECISIONS 75). Each is read for 4 hours, and
# her bed clears them all (home.py room_sleep).
def late_for(key):
    return {"type": "hours_since_flag", "subject": "player", "flag_key": key, "operator": "lt", "value": 4}


LATE_READ = {"came_home_late": late_for("came_home_late"),
             # the night Jake took her out, read for 6 hours (jake_saturday_date sheet; ledger L25)
             "jake_date_went": {"type": "hours_since_flag", "subject": "player", "flag_key": "jake_date_went",
                                "operator": "lt", "value": 6}}


def mark_late(canvas, key, split=True):
    """Every choice that leaves the canvas sets `key` and came_home_late. split=True (a scene that
    can run before 22:00): the choice is written twice, the 22:00-06:00 copy setting the flags."""
    fl = [fset(key), fset("came_home_late")]
    for n in canvas["nodes"]:
        out = []
        for c in n["choices"]:
            if c.get("targetType") == "node":
                out.append(c)
                continue
            if not split:
                c["flagEffects"] = list(c.get("flagEffects", [])) + fl
                out.append(c)
                continue
            for a, b, late in (("22:00", "06:00", True), ("06:00", "22:00", False)):
                d = json.loads(json.dumps(c))
                items = list((d.get("conditions") or {}).get("items", [])) + [
                    {"type": "time_of_day", "start_time": a, "end_time": b}]
                d["conditions"] = cond(*items)
                if late:
                    d["flagEffects"] = list(d.get("flagEffects", [])) + fl
                out.append(d)
        n["choices"] = out
    return canvas


# ── a booking a text makes (DECISIONS 87): the yes sets `<x>_booked`, the scene it booked reads it ──
# Showing up clears it, so the no-show text (phone.py) only arrives when she never came.
def clear_on_leave(canvas, *keys):
    """Every choice that leaves the canvas unsets each booking key."""
    for n in canvas["nodes"]:
        for c in n["choices"]:
            if c.get("targetType") != "node":
                c["flagEffects"] = list(c.get("flagEffects", [])) + [funset(k) for k in keys]
    return canvas


def sex_takes_needs(out, cid, node_id, text):
    """A one-time partnered sex step takes energy and hygiene like the repeatable acts (heat_a ACT_COSTS /
    ACT_HYGIENE, 10 each), on the choice out of the act. The ledger's board.needs says partnered sex takes both
    (pass 4 E95); the steps took neither. Clamped at 0: a need is a 0-100 meter."""
    hits = 0
    for c in out:
        if c["id"] != cid:
            continue
        for n in c["nodes"]:
            if n["id"] != node_id:
                continue
            for ch in n["choices"]:
                if ch["text"] == text:
                    ch["effects"] = list(ch.get("effects", [])) + [
                        {"targetType": "player", "trait": "energy", "op": "add", "value": -10, "clamp": True},
                        {"targetType": "player", "trait": "hygiene", "op": "add", "value": -10, "clamp": True}]
                    hits += 1
    assert hits, (cid, node_id, text)


# pass 4 A57 (the-heat-ladder.md H4, "her line changes with her level"): on a walk-in's answer screen, last before
# she picks, one short thought of hers by the stage of the meter its answers read: being seen reads Exhibitionism
# (Covered / Daring / Showing / Watched), the taboo reads Corruption (Good Girl / Curious / Bold / Hungry). The lines
# are wants, never acts, so they stay true whichever button she then takes. Each canvas gets its own four lines (one
# shared line pasted into many canvases fails `one pool, one place`), short, so the screen still says more than she
# thinks (lint `thoughts outweigh speech`). The bands are one if/elseif chain (GC) with an always-true else, one
# bound a band (each bound is a tier gate site, gate `the climb is where you said it is`); when a group already
# ends the screen they are standalone G bands instead, so they cannot join its chain.
def her_band_line(canvases, lines_by_canvas):
    """lines_by_canvas: {cid: (meter, [line under 20, under 40, under 60, 60 and up])}."""
    done = set()
    for c in canvases:
        if c["id"] not in lines_by_canvas:
            continue
        meter, texts = lines_by_canvas[c["id"]]
        assert len(texts) == 4, c["id"]
        ans = next(n for n in c["nodes"] if n["id"] == "answer")
        if ans["blocks"][-1].get("type") != "group":
            lines = [GC(cond(trait(meter, "lt", hi)), T(t)) for hi, t in zip((20, 40, 60), texts)]
            lines.append(GC(cond({"type": "worn_exposure", "operator": "gte", "value": 0}), T(texts[3])))   # the else
        else:
            bounds = [(None, 20), (20, 40), (40, 60), (60, None)]
            lines = [G(cond(*([trait(meter, "gte", lo)] if lo is not None else []),
                            *([trait(meter, "lt", hi)] if hi is not None else [])), T(t)) for (lo, hi), t in zip(bounds, texts)]
        ans["blocks"] = list(ans["blocks"]) + lines
        done.add(c["id"])
    assert done == set(lines_by_canvas), set(lines_by_canvas) - done


def booked_split(choice, key, eff=(), flags=()):
    """The choice written twice with the same text: the booked copy pays `eff` on top and clears
    `key`; the other copy is the choice as it was. Conditions don't nest, so both are AND lists."""
    assert (choice.get("conditions") or {}).get("logic", "AND") == "AND", choice["text"]
    base = list((choice.get("conditions") or {}).get("items", []))
    yes, no = json.loads(json.dumps(choice)), json.loads(json.dumps(choice))
    yes["conditions"] = cond(*base, flag(key))
    yes["effects"] = list(yes.get("effects", [])) + list(eff)
    yes["flagEffects"] = list(yes.get("flagEffects", [])) + list(flags) + [funset(key)]
    no["conditions"] = cond(*base, flag(key, False))
    return [yes, no]


def lift_line(blocks, quote, speaker):
    """Split the paragraph holding `"quote"` into before / a dialog block / after, word for word
    (iteration 002, part 7: a one-time step with a person speaks). Walks into groups and pools."""
    out = []
    for b in blocks:
        if b.get("type") == "paragraph" and f'"{quote}"' in b["content"]:
            before, after = b["content"].split(f'"{quote}"', 1)
            if before.strip():
                out.append(P(before.strip()))
            out.append(D(speaker, quote) if speaker != "player" else ME(quote))
            if after.strip():
                out.append(P(after.strip()))
        else:
            if b.get("blocks"):
                b = dict(b, blocks=lift_line(b["blocks"], quote, speaker))
            out.append(b)
    return out


def here_at(npc, loc):
    return {"type": "npc_at_location", "location_id": loc, "npc_id": npc, "operator": "is_present"}


MEDIA_TYPES = ("image", "video")


def _and_items(conds, items):
    """An AND conditions block with `items` added. An OR block can't take them: wrap it in a G first."""
    if not conds:
        return cond(*items)
    assert str(conds.get("logic", "AND")).upper() == "AND" or len(conds.get("items") or []) <= 1, \
        "pin_blocks: an OR group can't carry an AND pin; wrap it in G(cond(*ANY), ...) first"
    return dict(conds, logic="AND", items=list(conds.get("items") or []) + list(items))


def pin_blocks(blocks, *items):
    """Put presence items (here_at) on every text block of a screen, so each line shows only while the person it
    names is where the line needs them (the truth rule; gates `a named person is where the line says` reads a
    group's npc_at_location items as the engine's own check). No nesting level is added where one can be avoided,
    because the importer flattens past depth 4 (template_import.py:8444):
    - a group gets the items on its own conditions (adjacent groups stay one if/elseif chain, every link pinned);
    - a one-group pool (G) gets them on its group;
    - a pool of several entries goes inside one GC (group > pool > entry stays inside depth 4);
    - any other text block goes inside a G of its own. Media blocks are left as they are."""
    out = []
    for b in blocks:
        t = b.get("type")
        if t in MEDIA_TYPES:
            out.append(b)
        elif t == "group":
            out.append(dict(b, conditions=_and_items(b.get("conditions"), items)))
        elif t == "block_pool" and len(b.get("blocks") or []) == 1 and b["blocks"][0].get("type") == "group":
            g = b["blocks"][0]
            out.append(dict(b, blocks=[dict(g, conditions=_and_items(g.get("conditions"), items))]))
        elif t == "block_pool":
            out.append(GC(cond(*items), b))
            out[-1]["_pinned_pool"] = True
        else:
            out.append(G(cond(*items), b))
    # a GC round a pool must not sit next to another group, or the two would join one chain
    for i, b in enumerate(out):
        if b.pop("_pinned_pool", False):
            for j in (i - 1, i + 1):
                if 0 <= j < len(out):
                    assert out[j].get("type") != "group", "pin_blocks: a pinned pool sits next to a group"
    return out


def require_present(out, cid, *items):
    """Add presence checks to a canvas's trigger (iteration 002, part 7): the person a scene shows is
    where their row puts them when it can fire, which the truth gates read off these items."""
    for canvas in out:
        if canvas["id"] == cid:
            canvas["trigger"]["conditions"]["items"] += list(items)
            return
    raise KeyError(cid)


# ── the ledger's gate spelling → canvas condition items ──
def gate_item(g):
    if g.get("type") == "modifier":
        return {"type": "modifier", "modifier_key": g["modifier_key"], "operator": g["operator"]}
    if g.get("flag") in LATE_READ and g.get("op", "is_true") == "is_true":
        return LATE_READ[g["flag"]]
    if "flag" in g:
        return flag(g["flag"], g.get("op", "is_true") == "is_true")
    if g.get("npc"):
        return ntrait(g["npc"], g["trait"], g["op"], g["value"])
    return trait(g["trait"], g["op"], g["value"])


def ledger_step(npc, n):
    lad = LADDERS[npc]
    st = next(s for s in lad["steps"] if s["n"] == n)
    return lad["counter"], st


def on_activity(target, *items):
    """A one-time scene that opens from an activity instead of firing on entry (LO, 2026-11-04, Q2; gate `nothing
    one-time at the shop or wardrobe`): a substitution rule at chance 1 on the host. The target keeps its own trigger
    (window, gates, its person, parking), marked substitution_only so it never auto-fires; the engine checks all of
    that on the target before it swaps in (setup._tryRule, isCanvasValid, canTriggerCanvas)."""
    return {"target_canvas_id": target, "chance": 1.0, "conditions": cond(*items)}


def step_trigger(npc, n, extra_counters=(), bind_npc=True, priority=10, retry_days=1):
    """The trigger of ladder step n: place, window, the declared gate + the counter at n-1."""
    counter, st = ledger_step(npc, n)
    w = st.get("when") or {}
    items = [trait(counter, "eq", n - 1)]
    for c2, n2 in extra_counters:      # a shared step reads a second ladder's counter as its own
        items.append(trait(c2, "eq", n2 - 1))
    items += [gate_item(g) for g in st.get("gate") or []]
    t = {"location": st["where"], "is_repeatable": False, "priority": priority, "is_active": True,
         "consume_on": "exit", "retry_after_days": retry_days,
         "schedules": [{"weekdays": [DAYS[d[:3]] for d in ww["days"]], "start_time": ww["from"], "end_time": ww["to"]}
                       for ww in [w] + ([st["when_also"]] if st.get("when_also") else [])],
         "conditions": cond(*items)}
    if bind_npc:
        t["npc"] = npc
        t["requires_npc"] = npc
    return t


# ── emit ──
def _emit_block(b, L):
    L.append("\n[[canvases.nodes.blocks]]")
    for k in ("type", "content"):
        if k in b:
            L.append(f"{k} = {q(b[k])}")
    if "conditions" in b:
        L.append(f"conditions = {v(b['conditions'])}")
    if "blocks" in b:
        L.append("blocks = [")
        for ib in b["blocks"]:
            L.append(f"  {v(ib)},")
        L.append("]")
    if "props" in b:
        L.append(f"props = {v(b['props'])}")


_DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _clock(hhmm):
    h, m = (int(x) for x in hhmm.split(":"))
    suf = "AM" if h < 12 else "PM"
    h12 = h % 12 or 12
    return f"{h12}{':' + str(m).zfill(2) if m else ''} {suf}" if hhmm != "00:00" else "midnight"


def _days(wds):
    wds = sorted(set(wds))
    if wds == list(range(7)):
        return "Every day"
    if wds == list(range(5)):
        return "Weekdays"
    if wds == [5, 6]:
        return "Weekends"
    return ", ".join(_DAY_NAMES[d] for d in wds)


def hours_phrase(schedules):
    """'Weekdays, 11:45 AM-1 PM' for a canvas's schedule rows (the closed line, the-clock.md C5)."""
    parts = []
    for s in schedules or []:
        p_ = f"{_days(s.get('weekdays', list(range(7))))}, {_clock(s['start_time'])}-{_clock(s['end_time'])}"
        if p_ not in parts:
            parts.append(p_)
    return "; ".join(parts)   # every row: a dropped row hid when it opens (pass 4 H66)


def with_closed_line(canvas):
    """(alignment pass 2, 2026-11-03) A repeatable solo activity with hours stays on screen when it is shut and says
    when it opens (the-clock.md C5; gate `a closed activity says when it opens`). Added here so no canvas can miss it;
    an author's own message wins."""
    t = canvas.get("trigger") or {}
    # An event that happens to her (the guy beside her, the lecturer's word, a drink handed to her) never lists its
    # hours: hours go only on an activity she chooses (the-clock.md C5; LO, 2026-11-03). The mark rides in
    # trigger.metadata, which the importer ignores and the gate reads.
    if canvas.get("event"):
        t.setdefault("metadata", {})["kind"] = "event"
        return canvas
    if (t.get("is_repeatable") and t.get("schedules") and not t.get("npc") and not t.get("requires_npc")
            and t.get("trigger_mode") != "random" and not t.get("show_when_blocked")):
        t["show_when_blocked"] = True
        t.setdefault("cooldown_message", hours_phrase(t["schedules"]))
    return canvas


def emit(canvas):
    # The writer session's screens replace their PLACEHOLDER blocks here (writer.py; LO, 2026-10-09).
    from writer import fill
    canvas = fill(canvas)
    # A node may carry `pin`: presence items put on its whole screen AFTER the writer's screen is swapped in
    # (pin_blocks; first_term truth pass, 2026-11-03)
    for n in canvas["nodes"]:
        if n.get("pin"):
            n["blocks"] = pin_blocks(n["blocks"], *n.pop("pin"))
    canvas = voice_canvas(with_closed_line(canvas))
    L = ["\n[[canvases]]", f"id   = {q(canvas['id'])}", f"name = {q(canvas['name'])}"]
    if canvas.get("description"):
        L.append(f"description = {q(canvas['description'])}")
    t = canvas.get("trigger")
    if t:
        L.append("\n[canvases.trigger]")
        for k, val in t.items():
            if k in ("schedules", "conditions", "metadata"):
                continue
            L.append(f"{k} = {v(val)}")
        if t.get("conditions"):
            L.append(f"conditions = {v(t['conditions'])}")
        for s in t.get("schedules") or []:
            L.append("\n[[canvases.trigger.schedules]]")
            for k, val in s.items():
                L.append(f"{k} = {v(val)}")
        if t.get("metadata"):
            L.append("\n[canvases.trigger.metadata]")
            for k, val in t["metadata"].items():
                L.append(f"{k} = {v(val)}")
    for n in canvas["nodes"]:
        L.append("\n[[canvases.nodes]]")
        L.append(f"id   = {q(n['id'])}")
        L.append(f"name = {q(n['name'])}")
        for b in n["blocks"]:
            _emit_block(b, L)
        L.append("\n[canvases.nodes.exit_block]")
        L.append('type = "choices"')
        for c in n["choices"]:
            # A cost is deducted on the click (engine.md §33); an effect that repeats it would charge twice
            # (iteration 002: found live, the corner shop took $40). Drop the repeat.
            if c.get("costs") and c.get("effects"):
                paid = {(x["trait"], -int(x["value"])) for x in c["costs"]}
                c["effects"] = [e for e in c["effects"]
                                if not (e.get("targetType") == "player" and e.get("op") == "add"
                                        and (e.get("trait"), e.get("value")) in paid)]
                if not c["effects"]:
                    del c["effects"]
            L.append("\n[[canvases.nodes.exit_block.choices]]")
            for k, val in c.items():
                L.append(f"{k} = {v(val)}")
    return "\n".join(L) + "\n"


def emit_card(card):
    L = ["\n[[quest_cards]]"]
    for k, val in card.items():
        if isinstance(val, list) and val and isinstance(val[0], dict):
            L.append(f"{k} = [")
            for i in val:
                L.append(f"  {v(i)},")
            L.append("]")
        else:
            L.append(f"{k} = {v(val)}")
    return "\n".join(L) + "\n"


STAGE = {"corruption": {20: "Curious", 40: "Bold", 60: "Hungry"},
         "exhibitionism": {20: "Daring", 40: "Showing", 60: "Watched"}}
TRAIT_NAME = {"corruption": "Corruption", "exhibitionism": "Exhibitionism", "want": "Lust", "warmth": "Love",
              "power": "Dominance", "laura_suspicion": "Mom's suspicion", "intelligence": "Intelligence"}
NPC_NAME = {"npc_ryan": "Ryan", "npc_laura": "Laura", "npc_mark": "Mark", "npc_tom": "Tom", "npc_zoe": "Zoe",
            "npc_hale": "Dr. Hale", "npc_jake": "Jake"}
COUNTER_OWNER = {lad["counter"]: npc for npc, lad in LADDERS.items()}
# A flag a step needs, said as what she has done (a goal renders its label, engine.md §44).
FLAG_WORDS = {
    "came_home_late": "Come home late, after ten at night (in the last four hours)",
    "rent_starts": "The rent has started",
    # W8 (LO 2026-11-03) adds a Wednesday date, but his steps 3 and 4 read a Saturday one, which these labels name
    "jake_date_went": "Go out with Jake on a Saturday",
    "jake_date_booked": "Book a Saturday with Jake",
    # Zoe's step 5 needs him; he is met only at Figure drawing (LO 2026-11-02: the label said "Cocky guy met")
    "cocky_guy_met": "Meet Jake's teammate at Figure drawing (Tuesday or Thursday morning, Wednesday after lunch)",
    "mark_saw_her": "Mark's first accident: the garage, a Saturday",
    "cafe_let_it": "Let a customer's hand stay, on a café shift",
    "cafe_job": "Get the job at the café",
}


def _spec_trait_labels():
    """The game's own name for each counter ([[traits.labels]] in 0_systems_spec.toml). A card goal fell back to the
    raw key ("zoe_dares_done 4", "cafe_footfall 15") for every counter TRAIT_NAME doesn't list (LO 2026-11-03)."""
    import os
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "toml_phases", "0_systems_spec.toml")
    text = open(path, encoding="utf-8").read()
    return dict(re.findall(r'\[\[traits\.labels\]\]\s*\nkey\s*=\s*"([^"]+)"\s*\nlabel\s*=\s*"([^"]+)"', text))


SPEC_LABEL = _spec_trait_labels()
# A counter whose name alone doesn't say what to do: the goal says how it moves (cafe.py l2_play, l2_flirt, l3_let).
COUNTER_WORDS = {
    "cafe_footfall": "Café regulars {v}: play along or flirt back on a busy shift, or let a hand stay",
    # (Chrome play 2026-11-03: "The café's name -5" read as a number, not a task)
    "cafe_name": "Let customers' hands stay on café shifts, until the café gets a name for it",
    "cafe_shifts_worked": "Work {v} café shifts",
    "rent_short_weeks": "A Sunday short on the rent",
    # pass 3 J36 (engine.md:1074-1075): a counter goal says where, what to do and when, not a bare number
    "zoe_dares_done": "Take {v} of Zoe's dares at her Friday party, late",
    "laura_gaps_watched": "Watch Laura through her door or the bathroom door at night, {v} times",
}
# pass 3 J36: a meter goal names its feeder (the-voice.md R3: a place, a person, a verb, and the window when there is
# one). NPC_FEED is what raises his or her meter (the feeders in the build: hub_ryan_*, walkin_*_ryan, home_event_ryan_*,
# garden_sun; hub_laura_*, home_event_laura_robe). STAGE_WAY is what pays her in the stage BELOW the value, the same acts
# extras.py's tier cards name (engine.md section 23: never the button the value itself opens).
NPC_FEED = {
    ("npc_ryan", "want"): "let him see you at home: your towel in the hall, the shower, the lounger under his window, his room in the evenings",
    ("npc_laura", "warmth"): "spend time with her: breakfast on weekday mornings, cooking, dinner and the dishes on her evenings in the kitchen",
}
STAGE_WAY = {
    ("corruption", 20): "stay and look: the park couple, the library stacks, a door left open at home at night",
    ("corruption", 40): "touch yourself in your bed, in the shower or in a college toilet stall; watch the couple in the park",
    ("corruption", 60): "get on Ryan's couch with him, pull Jake into the gym locker room, walk the street with nothing under your skirt",   # pass 4: the watched dares need Corruption 60 now
    # pass 4 G15: the park and street dress codes open no bra / a short skirt at Corruption 20 for a Covered player
    ("exhibitionism", 20): "let someone walk in on your shower; once you're Curious, run in the park and walk the street",
    ("exhibitionism", 40): "let them look at the campus gym and in class, run in the park, walk the street in your short skirt, leave the changing-room curtain open, take your bra off in the college toilet, let the towel slip at home",
    ("exhibitionism", 60): "show off on the lounger in the garden, walk the street with no panties and let the wind have your skirt, drop the towel at home",
}


def counter_label(key, val):
    if key in COUNTER_WORDS:
        return COUNTER_WORDS[key].format(v=val)
    return f"{TRAIT_NAME.get(key) or SPEC_LABEL.get(key, key)} {val}"


def card_goals(st, counter):
    """(goals, notes) from a ledger step's gate. Another person's counter and a modifier go in the tip."""
    goals, notes = [], []
    for g in st.get("gate") or []:
        if g.get("type") == "modifier":
            notes.append("not while tipsy")
            continue
        if g.get("flag"):
            f = g["flag"]
            if f == "came_home_late":
                goals.append({"hours_since_flag": f, "op": "lt", "value": 4, "label": FLAG_WORDS[f]})
            else:
                goals.append({"flag": f, "op": g.get("op", "is_true"),
                              "label": FLAG_WORDS.get(f, f.replace("_", " ").capitalize())})
            continue
        key, val = g["trait"], g["value"]
        if key in COUNTER_OWNER and key != counter:
            owner = COUNTER_OWNER[key]
            other = next((x for x in LADDERS[owner]["steps"] if x["n"] == val), None)
            event = other["canvas"].split("_", 2)[2].replace("_", " ") if other else f"step {val}"
            notes.append(f"after {NPC_NAME.get(owner, owner)}'s \u201c{event}\u201d")
            continue
        if g.get("npc"):
            goals.append({"type": "trait", "subject": "npc", "npc_id": g["npc"], "trait": key, "op": g["op"],
                          "value": val, "label": f"{NPC_NAME.get(g['npc'], g['npc'])}'s {TRAIT_NAME.get(key, key)} {val}"
                                                  + (f": {NPC_FEED[(g['npc'], key)]}" if (g["npc"], key) in NPC_FEED else "")})
        else:
            stage = STAGE.get(key, {}).get(val)
            label = counter_label(key, val) + (f" ({stage})" if stage else "") \
                + (f": {STAGE_WAY[(key, val)]}" if (key, val) in STAGE_WAY else "")
            goals.append({"type": "trait", "subject": "player", "trait": key, "op": g["op"], "value": val, "label": label})
    return goals, notes


def step_cards(npc, texts, met_flag=None, terminal_text=None, closed_text=None, skip=(), pointer=None):
    """One card per step (counter eq n-1): the tip names place and time (the step's hint), and the
    goals are the step's real requirements, never the counter (B84; gate `a card shows the real gates`).
    A step with no gate shows only its place and time. A terminal card; a closed card for a final no."""
    lad = LADDERS[npc]
    counter = lad["counter"]
    out = []
    steps = sorted(lad["steps"], key=lambda s: s["n"])
    for s in steps:
        n = s["n"]
        if n in skip:
            continue
        when = [{"type": "trait", "subject": "player", "trait": counter, "op": "eq", "value": n - 1}]
        # C3 (skill, LO 2026-11-03): every card after the meeting carries the met flag; a pointer step (the meeting
        # itself is this step) carries a heading in place of the name instead
        if met_flag and not (pointer and pointer[0] == n):
            when.append({"flag": met_flag, "op": "is_true"})
        text, label = texts[n]
        goals, notes = card_goals(s, counter)
        label = re.sub(r"\s*\([^()]*\b(?:Curious|Daring|Bold|Showing|Hungry|Watched)\b[^()]*\)", "", label)
        tip = label + ("; " + "; ".join(notes) if notes else "")
        card = {"npc_id": npc, "priority": 10, "text": text, "tip": tip, "when": when, "ready_canvas": s["canvas"]}
        if goals:
            card["goals"] = goals
        if pointer and pointer[0] == n and met_flag:
            # (pass 3 C38, the-first-hour.md "every ladder card carries the met flag") the pointer card is the
            # unmet one: met flag is_false + heading. A meeting can come before the step (Hale: an ordinary
            # Psychology class sets hale_met), so the same step also gets a named card with is_true.
            out.append(dict(card, when=when + [{"flag": met_flag, "op": "is_false"}], heading=pointer[1]))
            card = dict(card, when=when + [{"flag": met_flag, "op": "is_true"}])
        elif pointer and pointer[0] == n:
            card["heading"] = pointer[1]
        out.append(card)
    top = steps[-1]["n"]
    if terminal_text:
        out.append({"npc_id": npc, "priority": 10, "text": terminal_text[0],
                    "when": [{"type": "trait", "subject": "player", "trait": counter, "op": "gte", "value": top}]
                            + ([{"flag": met_flag, "op": "is_true"}] if met_flag else []),
                    "terminal": True, "terminal_text": terminal_text[1]})
    if closed_text:
        out.append({"npc_id": npc, "priority": 20, "text": closed_text,
                    "when": [{"type": "trait", "subject": "player", "trait": counter, "op": "lt", "value": 0}]
                            + ([{"flag": met_flag, "op": "is_true"}] if met_flag else []),
                    "terminal": True, "terminal_text": "This path is closed."})
    return out


ALL_GARMENTS = ["plain_bra", "sports_bra", "plain_panties", "tshirt", "thin_top", "jeans", "leggings",
                "sleep_shorts", "short_skirt", "sleep_shirt", "towel", "cafe_uniform_normal",
                "cafe_uniform_sexy", "laura_blue_dress", "zoe_party_dress", "sneakers"]
# LO, 2026-11-04: she leaves in what she came in. REMEMBER goes before the first thing that takes her clothes off;
# DRESS_BACK is the way out. The plain set comes first so a garment taken since, or nothing kept, still leaves her
# dressed. A towel or the sleep clothes are never kept, so "Get dressed." after a shower gives back what she wore before it.
REMEMBER = {"action": "remember_outfit", "unless_wearing": ["towel", "sleep_shirt", "sleep_shorts"]}
RESTORE = {"action": "restore_outfit"}
STRIP = [REMEMBER] + [{"action": "unequip", "item_id": g} for g in ALL_GARMENTS if g != "sneakers"]
DRESS_DAY = [{"action": "equip", "item_id": g} for g in ("plain_bra", "plain_panties", "tshirt", "jeans", "sneakers")]
DRESS_BACK = DRESS_DAY + [RESTORE]


def no_node(nid, blocks, dest, retry, eff=None, flags=None, label="Go.", mins=3):
    """The written no: a short reply screen; its exit parks the step (retry) and moves something."""
    return node(nid, "No", blocks, [go(label, loc=dest, mins=mins, retry=retry, eff=eff, flags=flags)])


# The curfew (college sheet: a week, read by days since set) is a counter: set to 7 when Laura
# grounds her, one off every night in [engine.daily_tick]. One condition reads it either way.
CURFEW_ON = cond(trait("curfew_days", "gt", 0))
NO_CURFEW_ITEM = trait("curfew_days", "eq", 0)
CURFEW_EFF = [setv("curfew_days", 7)]


# ── one beat worded by what she wears, as one beat (fix_g3c, 2026-11-03) ──
# A beat that names her top is worded once per wardrobe case (a top, a dress, a uniform, a bra only, bare). As a chain
# of whole-beat copies, every case carried the full beat: zoe_dares came to 4,491 words of narration for about 600
# the player can read, which is what tipped `somebody speaks` over 5:1, and the copies pasted into zoe_02's kiss.
# Here the sentences every case shares print once, and only the sentences that differ sit in a chain of exclusive
# groups. Every case still reads exactly its own words, in the same order.
_CASE_SENT_RX = re.compile(r"(?<=[.!?*])\s+(?=[A-Z\"*])")


def chain_by_sentence(variants):
    """variants: [(conditions, text)], exclusive and in chain order. Blocks: shared runs as P, differing runs as GC."""
    split = [_CASE_SENT_RX.split(t) for _, t in variants]
    whole = [GC(c, P(t)) for c, t in variants]
    if len({len(s) for s in split}) != 1:
        return whole
    out, i, n = [], 0, len(split[0])
    while i < n:
        same = all(s[i] == split[0][i] for s in split)
        j = i
        while j < n and all(s[j] == split[0][j] for s in split) == same:
            j += 1
        if same:
            out.append(P(" ".join(split[0][i:j])))
        else:
            out += [GC(c, P(" ".join(s[i:j]))) for (c, _), s in zip(variants, split)]
        i = j
    texts = [b["content"] for b in out if b.get("type") == "paragraph"] + \
            [x["content"] for b in out if b.get("type") == "group" for x in b["blocks"]]
    if any(t.count('"') % 2 or t.count("*") % 2 for t in texts):   # a cut inside a quote or a thought: keep whole copies
        return whole
    return out
