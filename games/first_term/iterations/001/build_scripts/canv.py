"""Scene-writing helpers for the first_term build: Python data in, TOML text out.

A canvas is a dict; nodes hold blocks and choices. step() builds a ladder step's
trigger straight from the ledger's declared step (place, window, gate, counter), so
the canvas and the declaration cannot drift (gates.py `ladders move forward`).
"""
import json
from tomlw import q, v, cond, flag, trait, ntrait, boost_off, add, setv, nadd, fset, funset, DAYS

STATE = json.load(open("/Users/a0000/Desktop/Desktop_Archive_Backup/story_gen/story_gen_web_app/story_gen_django/games/first_term/v2_state.json"))
LADDERS = {c["id"]: c["ladder"] for c in STATE["board"]["characters"] if c.get("ladder")}


# ── blocks ──
def P(text):
    return {"type": "paragraph", "content": text}


def D(npc, text):
    return {"type": "dialog", "content": text, "props": {"speaker": "npc", "npcId": npc}}


def ME(text):
    return {"type": "dialog", "content": text, "props": {"speaker": "player"}}


def WHO(text):
    return {"type": "dialog", "content": text, "props": {"speaker": "unknown"}}


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


def POOL(*blocks, pid=None):
    b = {"type": "block_pool", "blocks": list(blocks)}
    if pid:
        b["props"] = {"id": pid, "memory": "seen"}
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


# ── choices ──
def go(text, node=None, loc=None, mins=None, eff=None, flags=None, cond_=None, wardrobe=None,
       costs=None, locked=None, swl=False, consumes=False, final=False, retry=None, ret=False, mods=None):
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


# ── the ledger's gate spelling → canvas condition items ──
def gate_item(g):
    if g.get("type") == "modifier":
        return {"type": "modifier", "modifier_key": g["modifier_key"], "operator": g["operator"]}
    if "flag" in g:
        return flag(g["flag"], g.get("op", "is_true") == "is_true")
    if g.get("npc"):
        return ntrait(g["npc"], g["trait"], g["op"], g["value"])
    return trait(g["trait"], g["op"], g["value"])


def ledger_step(npc, n):
    lad = LADDERS[npc]
    st = next(s for s in lad["steps"] if s["n"] == n)
    return lad["counter"], st


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
         "schedules": [{"weekdays": [DAYS[d[:3]] for d in w["days"]], "start_time": w["from"], "end_time": w["to"]}],
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


def emit(canvas):
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


def step_cards(npc, texts, met_flag=None, terminal_text=None, closed_text=None, skip=()):
    """One card per step (counter eq n-1), the tip naming place and time; a terminal card;
    a closed card for a final no (counter -1)."""
    lad = LADDERS[npc]
    counter = lad["counter"]
    out = []
    steps = sorted(lad["steps"], key=lambda s: s["n"])
    for s in steps:
        n = s["n"]
        if n in skip:
            continue
        when = [{"type": "trait", "subject": "player", "trait": counter, "op": "eq", "value": n - 1}]
        if met_flag:
            when.append({"flag": met_flag, "op": "is_true"})
        text, label = texts[n]
        out.append({"npc_id": npc, "priority": 10, "text": text, "tip": s["hint"], "when": when,
                    "goals": [{"type": "trait", "subject": "player", "trait": counter, "op": "gte",
                               "value": n, "label": label}],
                    "ready_canvas": s["canvas"]})
    top = steps[-1]["n"]
    if terminal_text:
        out.append({"npc_id": npc, "priority": 10, "text": terminal_text[0],
                    "when": [{"type": "trait", "subject": "player", "trait": counter, "op": "gte", "value": top}],
                    "terminal": True, "terminal_text": terminal_text[1]})
    if closed_text:
        out.append({"npc_id": npc, "priority": 20, "text": closed_text,
                    "when": [{"type": "trait", "subject": "player", "trait": counter, "op": "lt", "value": 0}],
                    "terminal": True, "terminal_text": "This path is closed."})
    return out


ALL_GARMENTS = ["plain_bra", "sports_bra", "plain_panties", "tshirt", "thin_top", "jeans", "leggings",
                "sleep_shorts", "short_skirt", "sleep_shirt", "towel", "cafe_uniform_normal",
                "cafe_uniform_sexy", "laura_blue_dress", "zoe_party_dress", "sneakers"]
STRIP = [{"action": "unequip", "item_id": g} for g in ALL_GARMENTS if g != "sneakers"]
DRESS_DAY = [{"action": "equip", "item_id": g} for g in ("plain_bra", "plain_panties", "tshirt", "jeans", "sneakers")]


def no_node(nid, blocks, dest, retry, eff=None, flags=None, label="Go.", mins=3):
    """The written no: a short reply screen; its exit parks the step (retry) and moves something."""
    return node(nid, "No", blocks, [go(label, loc=dest, mins=mins, retry=retry, eff=eff, flags=flags)])


# The curfew (college sheet: a week, read by days since set) is a counter: set to 7 when Laura
# grounds her, one off every night in [engine.daily_tick]. One condition reads it either way.
CURFEW_ON = cond(trait("curfew_days", "gt", 0))
NO_CURFEW_ITEM = trait("curfew_days", "eq", 0)
CURFEW_EFF = [setv("curfew_days", 7)]
