#!/usr/bin/env python3
"""
THE COUNT (Bastien at the cot) — static guard.

⚠️ WHY THIS EXISTS. The chunk is seven one-time steps and a loop, and almost every rule that holds it
together is a GATE, not prose: each step waits a calendar day after the one before it, the meter moves once
per day while the loop stays open, the loop never takes from him (no anal, no drain), Rue's beat does not
fire into an empty room, and he keeps exactly one repeatable canvas at the cot. Every one of those can be
broken by a one-line edit with the build staying green. This reads the merged TOML and fails loudly instead.

The day arithmetic itself (flags_meta set_day against time_state.day) only exists in the built game, so it
is walked live by live_the_count.py. This file proves the SHAPE.

Design: games/vesper/design_the_count.md.  Run from the repo root, after a merge:
    python games/vesper/tests/check_the_count.py
    python games/vesper/tests/check_the_count.py /tmp/mutated_final_game.toml   # negative tests
Exits 0 on pass, 1 on any failure.
"""
import os
import sys

try:
    import tomllib
except ModuleNotFoundError:                      # py<3.11
    import tomli as tomllib                      # type: ignore

GAME = os.path.join(os.path.dirname(__file__), "..", "toml_phases", "7_final_game.toml")
# An optional path argument points the guard at a mutated copy — which is how it is negative-tested.
if len(sys.argv) > 1:
    GAME = sys.argv[1]

# The chain, in order. Every quest card opens on one of these and closes on the next, and every step waits
# on the one before it. The 0.2.2 end card sits in front of it and hands over at the arrival.
CHAIN = ["bastien_at_cot", "bastien_drank", "bastien_washed", "brace_built", "bastien_stood",
         "bastien_bedded", "bastien_himself", "house_answered", "bastien_back"]
# Every flag this chunk owns. The first dev jump must unset all of them, so taking it twice (or after the
# second jump) lands in the same state.
COUNT_FLAGS = ["bastien_drank", "bastien_washed", "brace_built", "bastien_stood", "bastien_bedded",
               "bastien_slept", "bastien_himself", "bastien_note", "house_answered", "bastien_back"]
# What a finished 0.2.2 run has set — read out of the 0.2.2 canvases' own flagEffects at beat_0194.
# bunker_seen is left out on purpose: it is only set on a loud run, and a quiet run is a finished run too.
WAY_DOWN_DONE = ["bastien_alive_known", "rescue_agreed", "route_learned", "yard_part_found", "link_built",
                 "bastien_found_alive", "bastien_rescued", "bastien_at_cot"]

fails: list[str] = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


def report() -> int:
    if fails:
        print(f"THE COUNT GUARD: {len(fails)} FAILED")
        for f in fails:
            print("  - " + f)
        return 1
    print("THE COUNT GUARD: OK")
    return 0


def card_live(card, flags):
    """A quest card's `when` over a flag state (flag clauses only — the chain is all flags)."""
    for cl in card.get("when") or []:
        if "flag" not in cl:
            continue
        cur = bool(flags.get(cl["flag"], False))
        if cl.get("op") == "is_true" and not cur:
            return False
        if cl.get("op") == "is_false" and cur:
            return False
    return True


def card_reads(card):
    return {cl.get("flag") for cl in (card.get("when") or []) if cl.get("flag")}


def items_of(conds):
    return (conds or {}).get("items") or []


def holds(conds, flags, traits, day_waits_met=True):
    """Evaluate a v1.0 conditions block over a flag/trait state. days_since_flag holds when the flag is set
    and `day_waits_met` (the static guard cannot see the calendar — live_the_count.py walks that); anything
    this guard does not model (presence, clock) is taken as satisfied, which can only over-report a clash."""
    res = []
    for it in items_of(conds):
        t = it.get("type")
        if t == "flag":
            cur = bool(flags.get(it.get("flag_key"), False))
            res.append(cur if it.get("operator") == "is_true" else not cur)
        elif t == "days_since_flag":
            ok = bool(flags.get(it.get("flag_key"), False))
            op = it.get("operator")
            res.append(ok and (day_waits_met if op in ("gte", "gt") else not day_waits_met))
        elif t == "trait" and it.get("subject") == "player":
            cur, v = traits.get(it.get("trait_key"), 0), it.get("value")
            res.append({"gte": cur >= v, "gt": cur > v, "lte": cur <= v, "lt": cur < v,
                        "eq": cur == v, "ne": cur != v}.get(it.get("operator"), True))
        else:
            res.append(True)
    if (conds or {}).get("logic") == "OR":
        return any(res) if res else True
    return all(res)


def days_since_on(conds, flag):
    return any(it.get("type") == "days_since_flag" and it.get("flag_key") == flag
               and it.get("operator") == "gte" and it.get("value") == 1 for it in items_of(conds))


def flag_item(conds, flag, op):
    return any(it.get("type") == "flag" and it.get("flag_key") == flag and it.get("operator") == op
               for it in items_of(conds))


def sets_flag(canvas, flag):
    """Every flagEffects entry anywhere in the canvas (choices and location exits) that sets `flag`."""
    hits = []

    def walk(o):
        if isinstance(o, dict):
            if o.get("flag") == flag and o.get("op") == "set" and o.get("targetType") == "player":
                hits.append(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(canvas)
    return hits


def main() -> int:
    with open(GAME, "rb") as fh:
        doc = tomllib.load(fh)
    canvases = {c["id"]: c for c in doc.get("canvases", [])}
    cards = doc.get("quest_cards", [])

    # ── 1 · beat_0194 — the meter, the quest chain, the seam, the first dev jump ─────────────────────────
    player = doc.get("player") or {}
    check(player.get("core_traits", {}).get("bastien_mend") == 0,
          "1: player core_traits has no bastien_mend = 0 (a save missing the key must read it as 0)")
    labels = {l.get("key"): l for l in (doc.get("traits") or {}).get("labels", [])}
    check(labels.get("bastien_mend", {}).get("hidden") is True,
          "1: bastien_mend is not declared hidden in [[traits.labels]] — the raw number would show on the Stats page")

    ours = [c for c in cards if card_reads(c) & (set(CHAIN) | {"bastien_rescued"})
            and not c.get("npc_id")]
    # The seam: the shipped 0.2.2 end card hands over at the arrival and is no longer the end of anything.
    seam = [c for c in ours if "bastien_rescued" in card_reads(c)
            and any(cl.get("flag") == "bastien_rescued" and cl.get("op") == "is_true" for cl in c.get("when", []))
            and not any(cl.get("flag") == "link_built" for cl in c.get("when", []))]
    check(len(seam) == 1, f"1: expected exactly one 0.2.2 end card on bastien_rescued, found {len(seam)}")
    if seam:
        s = seam[0]
        check(any(cl.get("flag") == "bastien_at_cot" and cl.get("op") == "is_false" for cl in s.get("when", [])),
              "1: the 0.2.2 end card is not upper-gated `bastien_at_cot is_false` — it would sit over the new chain")
        check(not s.get("terminal") and not s.get("terminal_text"),
              "1: the 0.2.2 end card is still terminal — the page would say 'chapter complete' over THE COUNT")
    # One card per link of the chain: opens on CHAIN[i], closes on CHAIN[i+1]; the last is terminal.
    for i, opener in enumerate(CHAIN):
        closer = CHAIN[i + 1] if i + 1 < len(CHAIN) else None
        hits = []
        for c in ours:
            w = c.get("when") or []
            opens = any(cl.get("flag") == opener and cl.get("op") == "is_true" for cl in w)
            closes = closer is None or any(cl.get("flag") == closer and cl.get("op") == "is_false" for cl in w)
            if opens and closes:
                hits.append(c)
        check(len(hits) == 1, f"1: expected one card opening on {opener}"
                              f"{' and closing on ' + closer if closer else ''}, found {len(hits)}")
        if closer is None and hits:
            check(hits[0].get("terminal") is True and hits[0].get("terminal_text"),
                  "1: the last card (bastien_back) is not the terminal end card")
    # Exactly one of our cards is live at every point on the chain, from the rescue to the end.
    state = {"bastien_rescued": True}
    walk = [dict(state)]
    for f in CHAIN:
        state[f] = True
        walk.append(dict(state))
    for st in walk:
        live = [c for c in ours if card_live(c, st)
                and not any(cl.get("flag") == "bastien_rescued" and cl.get("op") == "is_false" for cl in c.get("when", []))]
        on = [k for k, v in st.items() if v][-1]
        check(len(live) == 1, f"1: {len(live)} quest cards live at once after {on} (want exactly 1)")
    for c in ours:
        if card_reads(c) & set(CHAIN):
            check("—" not in (c.get("text", "") + c.get("tip", "")),
                  "1: a COUNT quest card carries a dash — the legibility bar forbids them on cards")

    # The first dev jump: the end of 0.2.2, nothing of THE COUNT, at the cot.
    jump = canvases.get("dev_jump_count_start")
    check(jump is not None, "1: dev_jump_count_start is missing")
    if jump:
        chs = [ch for n in jump.get("nodes", []) for ch in ((n.get("exit_block") or {}).get("choices") or [])]
        check(len(chs) == 1 and chs[0].get("locationId") == "the_cot",
              "1: dev_jump_count_start must have one exit, to the_cot")
        fe = {e["flag"]: e["op"] for ch in chs for e in ch.get("flagEffects", [])}
        for f in WAY_DOWN_DONE:
            check(fe.get(f) == "set", f"1: dev_jump_count_start does not SET {f} (a finished 0.2.2 run has it)")
        for f in COUNT_FLAGS:
            check(fe.get(f) == "unset", f"1: dev_jump_count_start does not UNSET {f} (the jump must be idempotent)")
        te = [e for ch in chs for e in ch.get("effects", []) if e.get("trait") == "bastien_mend"]
        check(any(e.get("op") == "set" and e.get("value") == 0 for e in te),
              "1: dev_jump_count_start does not zero bastien_mend")
        src = canvases.get("dev_jump_way_down_start")
        if src:
            src_w = [ch.get("wardrobeEffects") for n in src.get("nodes", [])
                     for ch in ((n.get("exit_block") or {}).get("choices") or [])]
            check([ch.get("wardrobeEffects") for ch in chs] == src_w,
                  "1: dev_jump_count_start's wardrobe differs from the 0.2.2 jump it was copied from")

    # ── the chain as states, seeded from the first dev jump (the real end of 0.2.2) ────────────────────
    # Every later section walks these. Each state is (label, flags, traits). The seed matters: older cot
    # one-shots are gated on flags from earlier acts, and only a real seed shows whether they stay quiet.
    seed, seed_traits = {}, {}
    if jump:
        for ch in chs:
            for e in ch.get("flagEffects", []):
                seed[e["flag"]] = (e["op"] == "set")
            for e in ch.get("effects", []):          # later rows win, as the engine applies them in order
                if e.get("targetType") == "player" and e.get("op") == "set":
                    seed_traits[e["trait"]] = e.get("value")
    steps = [("arrived", {}, 0), ("drank", {"bastien_drank": True}, 0),
             ("washed", {"bastien_washed": True}, 0), ("brace", {"brace_built": True}, 0),
             ("stood", {"bastien_stood": True}, 0),
             ("first night", {"bastien_bedded": True, "bastien_slept": True}, 1),
             ("second night", {}, 2), ("third night", {}, 3),
             ("stopped counting", {"bastien_himself": True, "bastien_note": True}, 3),
             ("rue answered", {"house_answered": True}, 3), ("back", {"bastien_back": True}, 3)]
    chain_states, fl = [], dict(seed)
    for label, add, mend in steps:
        fl.update(add)
        chain_states.append((label, dict(fl), dict(seed_traits, bastien_mend=mend)))

    def cot_oneshots_live(flags, traits, day_waits_met=True, location="the_cot"):
        out = []
        for cid, c in canvases.items():
            t = c.get("trigger") or {}
            if (t.get("location") != location or t.get("is_repeatable") is not False
                    or t.get("is_active") is False or t.get("substitution_only")):
                continue
            if holds(t.get("conditions"), flags, traits, day_waits_met):
                out.append(cid)
        return out

    # ── 2 · beat_0195 — step 1, the water (his move: an auto-fire the day after the arrival) ────────────
    c = canvases.get("cap_bastien_drinks")
    check(c is not None, "2: cap_bastien_drinks is missing")
    if c:
        t = c.get("trigger") or {}
        check(t.get("location") == "the_cot" and t.get("is_repeatable") is False and t.get("is_active") is True,
              "2: cap_bastien_drinks must be an active one-shot located at the_cot")
        cond = t.get("conditions")
        check(flag_item(cond, "bastien_at_cot", "is_true") and flag_item(cond, "bastien_drank", "is_false"),
              "2: cap_bastien_drinks is not gated bastien_at_cot is_true + bastien_drank is_false")
        check(days_since_on(cond, "bastien_at_cot"),
              "2: cap_bastien_drinks does not wait a calendar day (days_since_flag bastien_at_cot gte 1)")
        check(len(sets_flag(c, "bastien_drank")) == 1, "2: cap_bastien_drinks must set bastien_drank exactly once")
        live = cot_oneshots_live(chain_states[0][1], chain_states[0][2])
        check(live == ["cap_bastien_drinks"],
              f"2: the morning after the arrival, the water must be the only cot auto-fire that can hold (got {live})")
        live = cot_oneshots_live(chain_states[0][1], chain_states[0][2], day_waits_met=False)
        check(live == [], f"2: on the night of the arrival nothing may fire at the cot (got {live})")
    # Across the whole chain, at most one cot auto-fire can hold in any state.
    for label, fls, trs in chain_states:
        live = cot_oneshots_live(fls, trs)
        check(len(live) <= 1, f"2: {len(live)} cot auto-fires can hold at once after '{label}': {live}")

    # ── 3 · beat_0196 — the hub rewrite, and step 2, the washing ──────────────────────────────────────
    hub = canvases.get("amb_bastien_cot") or {}
    ht = hub.get("trigger") or {}
    check(ht.get("npc") == "npc_bastien" and ht.get("requires_npc") == "npc_bastien"
          and ht.get("is_repeatable") is True and ht.get("priority") == 2 and ht.get("location") == "the_cot",
          "3: amb_bastien_cot must stay his repeatable portrait hub at the cot, pri 2 (id, npc, requires_npc)")
    hub_nodes = {n["id"]: n for n in hub.get("nodes", [])}
    base = hub_nodes.get("base") or {}

    def group_flags(blocks):
        out = set()
        for b in blocks:
            if b.get("type") == "group":
                out |= {it.get("flag_key") for it in items_of((b.get("props") or {}).get("conditions"))
                        if it.get("type") == "flag"}
        return out
    banded = group_flags(base.get("blocks", []))
    for f in ("bastien_drank", "bastien_washed", "bastien_stood", "bastien_bedded", "bastien_himself",
              "bastien_back"):
        check(f in banded, f"3: the hub's base text has no band on {f} — it would read the same before and after")
    hub_choices = (base.get("exit_block") or {}).get("choices") or []

    def hub_choice(label):
        return [ch for ch in hub_choices if ch.get("text") == label]
    check(bool(hub_choices) and hub_choices[-1].get("text") == "Leave him."
          and hub_choices[-1].get("locationId") == "the_cot",
          "3: 'Leave him.' must stay the hub's last choice, back to the cot")
    wash = hub_choice("Wash him.")
    check(len(wash) == 1, "3: the hub has no single 'Wash him.' choice")
    if wash:
        w = wash[0]
        check(w.get("nodeId") in ("washing", "amb_bastien_cot.washing"), "3: 'Wash him.' must enter the hub's washing node")
        wc = w.get("conditions")
        check(flag_item(wc, "bastien_drank", "is_true") and flag_item(wc, "bastien_washed", "is_false")
              and days_since_on(wc, "bastien_drank"),
              "3: 'Wash him.' is not gated drank + not washed + a calendar day after the water")
        check(any(e.get("flag") == "bastien_washed" and e.get("op") == "set" for e in w.get("flagEffects", [])),
              "3: bastien_washed must be set ON the 'Wash him.' click (effects ride the choice)")
    wn = hub_nodes.get("washing")
    check(wn is not None, "3: the hub has no washing node")

    def videos(node):
        out = []

        def walk(bl):
            for b in bl:
                if b.get("type") == "video":
                    out.append(b.get("props") or {})
                elif b.get("type") == "group":
                    walk(b.get("blocks", []))
        walk((node or {}).get("blocks", []))
        return out

    def node_text(node):
        out = []

        def walk(o):
            if isinstance(o, dict):
                if o.get("type") in ("paragraph", "dialog", "thought_bubble") and "content" in o:
                    out.append(o["content"])
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk((node or {}).get("blocks", []))
        return " ".join(out)

    def pool_ok(node, pool_dir, tag):
        v = [p for p in videos(node) if p.get("pool_dir") == pool_dir]
        check(len(v) == 1 and v[0].get("pool") == 4 and v[0].get("description") and v[0].get("search_queries"),
              f"{tag}: needs exactly one video block {pool_dir}, pool 4, with description + search_queries")
    if wn:
        pool_ok(wn, "sex/bastien_cot_wash_t5", "3")
        check("anal" not in node_text(wn).lower(), "3: the washing mentions anal — the chunk never goes there")
        wx = (wn.get("exit_block") or {})
        check(wx.get("type") == "location" and (wx.get("config") or {}).get("locationId") == "the_cot",
              "3: the washing must exit to the cot")

    # ── 4 · beat_0197 — step 3, the brace: bought from Kess for coin, then put on him at the cot ────────
    kb = canvases.get("kess_makes_the_brace")
    check(kb is not None, "4: kess_makes_the_brace is missing")
    if kb:
        t = kb.get("trigger") or {}
        # The kess_makes_the_link shape: a located trigger (so brace_built has a located setter for the hub
        # choice that reads it) and substitution_only (so it never renders as a bare link under Kess's card).
        check(t.get("location") == "kess_berth" and t.get("substitution_only") is True,
              "4: kess_makes_the_brace must be located @kess_berth and substitution_only (the link's shape)")
        check(not t.get("costs") and "coin" not in str(t.get("conditions")),
              "4: the coin is on the TRIGGER — a player who cannot pay would lose the scene as well as the brace")
        tc = t.get("conditions")
        check(flag_item(tc, "bastien_washed", "is_true") and flag_item(tc, "brace_built", "is_false"),
              "4: kess_makes_the_brace is not gated bastien_washed is_true + brace_built is_false")
        buy = [ch for n in kb.get("nodes", []) for ch in ((n.get("exit_block") or {}).get("choices") or [])
               if any(e.get("flag") == "brace_built" and e.get("op") == "set" for e in ch.get("flagEffects", []))]
        check(len(buy) == 1 and buy[0].get("costs") == [{"trait": "coin", "value": 40}],
              "4: exactly one choice sets brace_built, and it costs 40 coin (the link's price)")
        made = {n["id"]: n for n in kb.get("nodes", [])}.get("made") or {}
        check(((made.get("exit_block") or {}).get("config") or {}).get("locationId") == "the_cot",
              "4: the brace scene's prose carries it to the cot, so its exit must go to the cot")
    kh = canvases.get("hub_kess_berth") or {}
    rung = [ch for n in kh.get("nodes", []) for ch in ((n.get("exit_block") or {}).get("choices") or [])
            if str(ch.get("nodeId", "")).startswith("kess_makes_the_brace")]
    check(len(rung) == 1, "4: hub_kess_berth has no single rung into kess_makes_the_brace")
    if rung:
        rc = rung[0].get("conditions")
        check(flag_item(rc, "bastien_washed", "is_true") and flag_item(rc, "brace_built", "is_false"),
              "4: the brace rung on Kess's card is not gated washed + not built")
    stand = hub_choice("Put the brace on him.")
    check(len(stand) == 1, "4: the hub has no single 'Put the brace on him.' choice")
    if stand:
        sc = stand[0].get("conditions")
        check(flag_item(sc, "brace_built", "is_true") and flag_item(sc, "bastien_stood", "is_false")
              and days_since_on(sc, "bastien_washed"),
              "4: 'Put the brace on him.' is not gated built + not stood + a calendar day after the washing")
        check(any(e.get("flag") == "bastien_stood" and e.get("op") == "set" for e in stand[0].get("flagEffects", [])),
              "4: bastien_stood must be set on the 'Put the brace on him.' click")
        check(stand[0].get("nodeId") in ("stands", "amb_bastien_cot.stands"), "4: the brace choice must enter the stands node")
    check("stands" in hub_nodes, "4: the hub has no stands node")

    # ── 5 · beat_0198 — step 4, the first night (Tier-3, once-only) ────────────────────────────────────
    DRAIN_KEYS = ("drain_charge", "equipped_weapon", "anal_active")

    def touches(obj, keys):
        return any(k in str(obj) for k in keys)
    fn = hub_choice("Go to him properly.")
    check(len(fn) == 1, "5: the hub has no single 'Go to him properly.' choice")
    if fn:
        f0 = fn[0]
        fc = f0.get("conditions")
        check(flag_item(fc, "bastien_stood", "is_true") and flag_item(fc, "bastien_bedded", "is_false")
              and days_since_on(fc, "bastien_stood"),
              "5: 'Go to him properly.' is not gated stood + not bedded + a calendar day after he stood")
        check(any(it.get("type") == "time_of_day" and it.get("start_time") == "22:00" and it.get("end_time") == "06:00"
                  for it in items_of(fc)),
              "5: the first night is a night scene (torch off, him asleep in the dark) — it needs time_of_day 22:00-06:00")
        fe = {(e.get("flag"), e.get("op")) for e in f0.get("flagEffects", [])}
        check(("bastien_bedded", "set") in fe and ("bastien_slept", "set") in fe,
              "5: the first night must set bastien_bedded AND bastien_slept (the loop's once-a-day clock starts here)")
        check([e for e in f0.get("effects", []) if e.get("trait") == "bastien_mend"]
              == [{"targetType": "player", "trait": "bastien_mend", "op": "add", "value": 1}],
              "5: the first night must add exactly 1 to bastien_mend (it is the first of the nights)")
        check(not touches(f0, DRAIN_KEYS), "5: the first night's choice touches the drain")
        check(f0.get("nodeId") in ("first_night", "amb_bastien_cot.first_night"), "5: it must enter the first_night node")
    fnn = hub_nodes.get("first_night")
    check(fnn is not None, "5: the hub has no first_night node")
    if fnn:
        pool_ok(fnn, "sex/bastien_cot_first_night_t5", "5")
        check("anal" not in node_text(fnn).lower(), "5: the first night mentions anal — the chunk never goes there")
        check(not touches(fnn, DRAIN_KEYS), "5: the first night's node touches the drain")
        beats = [b for b in fnn.get("blocks", []) if b.get("type") == "cascade"]
        n = len(beats[0]["props"]["beats"]) if beats else 0
        check(10 <= n <= 20, f"5: the capstone should be 10-20 beats (more beats, not thicker ones) — has {n}")

    # ── 6 · beat_0199 — the loop, and the once-a-day pair that paces the meter while the loop stays open ──
    RESET = {("loop_npc_pleasure", 0), ("sex_stage", 0), ("sex_finisher_type", 0), ("anal_active", 0),
             ("sex_entry_origin", 0)}

    def resets(effects):
        return RESET <= {(e.get("trait"), e.get("value")) for e in effects or [] if e.get("op") == "set"}
    pair = hub_choice("Go to him.")
    check(len(pair) == 2, f"6: the hub needs exactly two 'Go to him.' choices (the once-a-day pair), has {len(pair)}")
    if len(pair) == 2:
        paced = [ch for ch in pair if any(it.get("type") == "days_since_flag" and it.get("flag_key") == "bastien_slept"
                                          and it.get("operator") == "gte" and it.get("value") == 1
                                          for it in items_of(ch.get("conditions")))]
        free = [ch for ch in pair if any(it.get("type") == "days_since_flag" and it.get("flag_key") == "bastien_slept"
                                         and it.get("operator") == "lt" and it.get("value") == 1
                                         for it in items_of(ch.get("conditions")))]
        check(len(paced) == 1 and len(free) == 1,
              "6: the pair must be days_since(bastien_slept) gte 1 and lt 1 — exact complements, one visible any day")
        for ch in pair:
            check(flag_item(ch.get("conditions"), "bastien_bedded", "is_true"),
                  "6: a 'Go to him.' is not gated on bastien_bedded (the loop opens at the first night)")
            check(ch.get("nodeId") == "loop_bastien_cot.intro", "6: a 'Go to him.' does not enter loop_bastien_cot.intro")
            check(resets(ch.get("effects")), "6: a 'Go to him.' does not reset the five loop traits (the hub_grier entry)")
            check(not touches(ch, ("drain_charge", "equipped_weapon")), "6: a 'Go to him.' touches the drain")
        if paced and free:
            pm = [e for e in paced[0].get("effects", []) if e.get("trait") == "bastien_mend"]
            check(pm == [{"targetType": "player", "trait": "bastien_mend", "op": "add", "value": 1}],
                  "6: the paced 'Go to him.' must add exactly 1 to bastien_mend")
            check(any(e.get("flag") == "bastien_slept" and e.get("op") == "set" for e in paced[0].get("flagEffects", [])),
                  "6: the paced 'Go to him.' must re-set bastien_slept (that re-set IS the once-a-day clock)")
            check(not [e for e in free[0].get("effects", []) if e.get("trait") == "bastien_mend"]
                  and not free[0].get("flagEffects"),
                  "6: the free 'Go to him.' must not move the meter or the clock — that would be a free night")
    # Nothing but the located hub ever writes the meter.
    writers = sorted({cid for cid, cv in canvases.items()
                      if '"bastien_mend"' in str(cv).replace("'", '"') and cid not in ("dev_jump_count_start",
                                                                                         "dev_jump_count_one_short")
                      and any(e.get("trait") == "bastien_mend"
                              for n in cv.get("nodes", []) for ch in ((n.get("exit_block") or {}).get("choices") or [])
                              for e in ch.get("effects", []))})
    check(writers == ["amb_bastien_cot"], f"6: bastien_mend is written outside the hub: {writers}")
    loop, fin = canvases.get("loop_bastien_cot"), canvases.get("loop_bastien_cot_finisher")
    check(loop is not None and fin is not None, "6: loop_bastien_cot and loop_bastien_cot_finisher must both exist")
    if loop and fin:
        for cv in (loop, fin):
            check(not cv.get("trigger"), f"6: {cv['id']} must be TRIGGERLESS (only the hub reaches it)")
            txt = " ".join(node_text(n) for n in cv.get("nodes", []))
            check("anal" not in txt.lower(), f"6: {cv['id']} mentions anal — the chunk never goes there")
            check(not touches(cv, ("drain_charge", "equipped_weapon")), f"6: {cv['id']} touches the drain")
            bad = [e for n in cv.get("nodes", []) for ch in ((n.get("exit_block") or {}).get("choices") or [])
                   for e in ch.get("effects", [])
                   if (e.get("trait") == "anal_active" and e.get("value") != 0)
                   or (e.get("trait") == "sex_finisher_type" and e.get("value") not in (0, 1))
                   or (e.get("trait") == "sex_stage" and e.get("value") not in (0, 1))]
            check(not bad, f"6: {cv['id']} writes an anal state (anal_active, finisher 2, or stage 2): {bad}")
        ln = {n["id"]: n for n in loop.get("nodes", [])}
        for nid in ("intro", "base_oral_bastien", "base_ride_bastien"):
            check(nid in ln, f"6: loop_bastien_cot has no {nid} node")
        climaxes = [ch for n in loop.get("nodes", []) for ch in ((n.get("exit_block") or {}).get("choices") or [])
                    if ch.get("nodeId") == "loop_bastien_cot_finisher.climax"]
        check(len(climaxes) >= 2, "6: the loop has fewer than two climax choices")
        for ch in climaxes:
            check(any(it.get("trait_key") == "loop_npc_pleasure" and it.get("operator") == "gte" and it.get("value") == 50
                      for it in items_of(ch.get("conditions"))),
                  f"6: climax choice '{ch.get('text')}' is not gated loop_npc_pleasure gte 50")
        pool_ok(ln.get("base_oral_bastien"), "sex/bastien_cot_oral_t5", "6")
        pool_ok(ln.get("base_ride_bastien"), "sex/bastien_cot_ride_t5", "6")
        fn_ = {n["id"]: n for n in fin.get("nodes", [])}
        cl = fn_.get("climax")
        check(cl is not None, "6: the finisher has no climax node")
        if cl:
            ex = (cl.get("exit_block") or {}).get("choices") or []
            check(ex and all(resets(ch.get("effects")) and ch.get("locationId") == "the_cot" for ch in ex),
                  "6: every finisher exit must reset the five loop traits and return to the cot")
            fins = {v.get("pool_dir") for v in videos(cl)}
            check({"sex/bastien_cot_finish_facial_t5", "sex/bastien_cot_finish_inside_t5"} <= fins,
                  "6: the finisher needs both finish pools (facial, inside)")
    # He keeps exactly one repeatable canvas at the cot.
    reps = [cid for cid, cv in canvases.items()
            if (cv.get("trigger") or {}).get("location") == "the_cot"
            and (cv.get("trigger") or {}).get("is_repeatable") is True
            and not (cv.get("trigger") or {}).get("substitution_only")
            and "npc_bastien" in ((cv.get("trigger") or {}).get("npc"), (cv.get("trigger") or {}).get("requires_npc"))]
    check(reps == ["amb_bastien_cot"], f"6: he must keep exactly one repeatable canvas at the cot, has {reps}")
    # Every pool in the chunk is its own asset (the one-asset-one-block rule).
    allpools = [v.get("pool_dir") for cid in ("amb_bastien_cot", "loop_bastien_cot", "loop_bastien_cot_finisher")
                for n in (canvases.get(cid) or {}).get("nodes", []) for v in videos(n)]
    check(len(allpools) == len(set(allpools)), f"6: a pool folder is used by two blocks: {allpools}")
    # ⚠️ AND ACROSS THE WHOLE GAME, not just the chunk. The first cut named three of THE COUNT's pools
    # sex/bastien_loop_oral_t5 / _finish_facial_t5 / _finish_inside_t5 — which ARE The Face's back-room loop
    # (loop_bastien_backroom, 1c), with its own clips on disk. The cot loop would have played the back room.
    # This section only checked uniqueness inside the chunk, so it passed. Found at beat_0204's media audit.
    game_pools = [v.get("pool_dir") for cv in canvases.values() for n in cv.get("nodes", []) for v in videos(n)
                  if v.get("pool_dir")]
    for pd in allpools:
        check(game_pools.count(pd) == 1, f"6: pool {pd} is also used elsewhere in the game — two scenes, one shelf")
        check(pd.startswith("sex/bastien_cot_"), f"6: pool {pd} is outside THE COUNT's sex/bastien_cot_* family")

    # ── 7 · beat_0200 — step 5, he stops counting; and the HIMSELF band across the loop ─────────────────
    sc = canvases.get("cap_bastien_stops_counting")
    check(sc is not None, "7: cap_bastien_stops_counting is missing")
    if sc:
        t = sc.get("trigger") or {}
        check(t.get("location") == "the_cot" and t.get("is_repeatable") is False and t.get("is_active") is True,
              "7: cap_bastien_stops_counting must be an active one-shot located at the_cot")
        cond = t.get("conditions")
        check(any(it.get("type") == "trait" and it.get("trait_key") == "bastien_mend" and it.get("operator") == "gte"
                  and it.get("value") == 3 for it in items_of(cond)),
              "7: he stops counting at bastien_mend gte 3 — three nights — and at no other number")
        check(flag_item(cond, "bastien_himself", "is_false") and days_since_on(cond, "bastien_slept"),
              "7: step 5 must be gated not-yet-himself + the morning after the third night (days_since bastien_slept gte 1)")
        check(len(sets_flag(sc, "bastien_himself")) == 1 and len(sets_flag(sc, "bastien_note")) == 1,
              "7: step 5 must set bastien_himself and bastien_note, once each")
        check(any(it.get("type") == "time_of_day" and it.get("start_time") == "06:00" and it.get("end_time") == "22:00"
                  for it in items_of(cond)),
              "7: step 5 needs time_of_day 06:00-22:00 — a third night that crosses midnight lands on the next "
              "calendar day, and without the clock item he 'stops counting this morning' as she climbs off him")
    states = {label: (fls, trs) for label, fls, trs in chain_states}
    live = cot_oneshots_live(*states["second night"])
    check(live == [], f"7: after only two nights nothing may fire at the cot (got {live})")
    live = cot_oneshots_live(*states["third night"])
    check(live == ["cap_bastien_stops_counting"],
          f"7: the morning after the third night, stopping counting is the only cot auto-fire (got {live})")
    live = cot_oneshots_live(*states["third night"], day_waits_met=False)
    check(live == [], f"7: the night of the third night nothing fires (got {live})")
    if loop:
        ln = {n["id"]: n for n in loop.get("nodes", [])}
        for nid in ("intro", "base_oral_bastien", "base_ride_bastien"):
            g = next((b for b in (ln.get(nid) or {}).get("blocks", []) if b.get("type") == "group"), None)
            check(g is not None and flag_item((g.get("props") or {}).get("conditions"), "bastien_himself", "is_true"),
                  f"7: loop node {nid}'s FIRST band must be HIMSELF (it must win once he has stopped counting)")
        under = ln.get("base_under_bastien")
        check(under is not None, "7: the loop has no base_under_bastien pose")
        if under:
            pool_ok(under, "sex/bastien_cot_under_t5", "7")
        # From every OTHER node — the pose's own self-loop ("Take it.") is already inside it.
        into = [ch for n in loop.get("nodes", []) if n["id"] != "base_under_bastien"
                for ch in ((n.get("exit_block") or {}).get("choices") or [])
                if ch.get("nodeId") == "base_under_bastien"]
        check(bool(into) and all(flag_item(ch.get("conditions"), "bastien_himself", "is_true") for ch in into),
              "7: every way into the under-him pose must be gated bastien_himself (he cannot get over her before)")
    if fin:
        cl = {n["id"]: n for n in fin.get("nodes", [])}.get("climax") or {}
        casc = next((b for b in cl.get("blocks", []) if b.get("type") == "cascade"), None)
        gs = [b for b in (casc["props"]["beats"][0].get("blocks", []) if casc else []) if b.get("type") == "group"]
        check(len(gs) == 4 and all(flag_item((g.get("props") or {}).get("conditions"), "bastien_himself", "is_true")
                                   for g in gs[:2]),
              "7: the finisher's prose needs four bands, the two HIMSELF ones first")

    # ── 8 · beat_0201 — step 6, Rue at the House ─────────────────────────────────────────────────────────
    rr = canvases.get("cap_rue_reads_it")
    check(rr is not None, "8: cap_rue_reads_it is missing")
    if rr:
        t = rr.get("trigger") or {}
        check(t.get("location") == "underworld_brothel" and t.get("is_repeatable") is False
              and t.get("is_active") is True and t.get("priority") == 10,
              "8: cap_rue_reads_it must be an active one-shot at underworld_brothel, pri 10")
        cond = t.get("conditions")
        check(flag_item(cond, "bastien_note", "is_true") and flag_item(cond, "house_answered", "is_false")
              and flag_item(cond, "rue_introduced", "is_true"),
              "8: Rue's beat must be gated note carried + not yet answered + Rue already introduced")
        check(any(it.get("type") == "npc_at_location" and it.get("npc_id") == "npc_rue"
                  and it.get("location_id") == "underworld_brothel" and it.get("operator") == "is_present"
                  for it in items_of(cond)),
              "8: Rue's beat has no npc_at_location … is_present — it would fire into an empty room (open item 5's defect)")
        check(len(sets_flag(rr, "house_answered")) == 1, "8: Rue's beat must set house_answered exactly once")
        st_fl, st_tr = states["stopped counting"]
        live = cot_oneshots_live(st_fl, st_tr, location="underworld_brothel")
        check(live == ["cap_rue_reads_it"],
              f"8: with the note carried, Rue's beat must be the only House auto-fire that can hold (got {live})")

    # ── 9 · beat_0202 — step 7, counting again (Tier-3), and the chain's end ───────────────────────────
    ca = canvases.get("cap_bastien_counts_again")
    check(ca is not None, "9: cap_bastien_counts_again is missing")
    if ca:
        t = ca.get("trigger") or {}
        check(t.get("location") == "the_cot" and t.get("is_repeatable") is False and t.get("is_active") is True,
              "9: cap_bastien_counts_again must be an active one-shot located at the_cot")
        cond = t.get("conditions")
        check(flag_item(cond, "house_answered", "is_true") and flag_item(cond, "bastien_back", "is_false"),
              "9: step 7 must be gated Rue answered + not yet back")
        check(len(sets_flag(ca, "bastien_back")) == 1, "9: step 7 must set bastien_back exactly once")
        casc = [b for n in ca.get("nodes", []) for b in n.get("blocks", []) if b.get("type") == "cascade"]
        n = len(casc[0]["props"]["beats"]) if casc else 0
        check(10 <= n <= 20, f"9: the last capstone should be 10-20 beats, has {n}")
    live = cot_oneshots_live(*states["rue answered"])
    check(live == ["cap_bastien_counts_again"],
          f"9: with Rue's envelope, counting again must be the only cot auto-fire (got {live})")
    live = cot_oneshots_live(*states["back"])
    check(live == [], f"9: once he is back, nothing of the chain may fire again at the cot (got {live})")

    # ── 10 · beat_0203 — the second dev jump: one night short of him stopping counting ──────────────────
    j2 = canvases.get("dev_jump_count_one_short")
    check(j2 is not None, "10: dev_jump_count_one_short is missing")
    if j2:
        chs2 = [ch for n in j2.get("nodes", []) for ch in ((n.get("exit_block") or {}).get("choices") or [])]
        check(len(chs2) == 1 and chs2[0].get("locationId") == "the_cot", "10: jump 2 must have one exit, to the_cot")
        fe2 = {e["flag"]: e["op"] for ch in chs2 for e in ch.get("flagEffects", [])}
        through = ["bastien_drank", "bastien_washed", "brace_built", "bastien_stood", "bastien_bedded", "bastien_slept"]
        after = ["bastien_himself", "bastien_note", "house_answered", "bastien_back"]
        for f in WAY_DOWN_DONE + through:
            check(fe2.get(f) == "set", f"10: jump 2 does not SET {f}")
        for f in after + ["face_worn"]:
            check(fe2.get(f) == "unset", f"10: jump 2 does not UNSET {f}")
        te2 = {}
        for ch in chs2:
            for e in ch.get("effects", []):
                if e.get("targetType") == "player" and e.get("op") == "set":
                    te2[e["trait"]] = e.get("value")
        check(te2.get("bastien_mend") == 2, f"10: jump 2 must land with two nights on the meter (bastien_mend {te2.get('bastien_mend')})")
        check(te2.get("coin") == 80, f"10: jump 2 must have the brace's 40 coin spent (coin {te2.get('coin')})")
        if jump:
            check([ch.get("wardrobeEffects") for ch in chs2] == [ch.get("wardrobeEffects") for ch in chs],
                  "10: jump 2's wardrobe differs from jump 1's")
        st2 = {k: (v == "set") for k, v in fe2.items()}
        live = cot_oneshots_live(st2, dict(te2))
        check(live == ["cap_bastien_stops_counting"] or live == [],
              f"10: jump 2's landing state must not fire anything but (on a later day) stopping counting — got {live}")
        live = cot_oneshots_live(st2, dict(te2), day_waits_met=False)
        check(live == [], f"10: on jump 2's own day nothing may fire at the cot (got {live})")

    # ── 7a · beat_0200 — THE FACE AT THE COT. He looked at her bought face across his own floor for four months
    # and the last time he saw it, it had a taser in its hand. face_worn is a toggle she works at the cot
    # (activity_the_face). If any scene with him could play while she wears it, "he never learns who she is"
    # is one click from broken. So every surface of his that shows her to him waits for the face to be off.
    face_off = lambda conds: flag_item(conds, "face_worn", "is_false")
    for cid in ("cap_bastien_drinks", "cap_bastien_stops_counting", "cap_bastien_counts_again"):
        cv = canvases.get(cid)
        if cv:
            check(face_off((cv.get("trigger") or {}).get("conditions")),
                  f"7a: {cid} can fire while she is wearing the face he knew on his floor (needs face_worn is_false)")
    for label in ("Wash him.", "Put the brace on him.", "Go to him properly.", "Go to him."):
        for ch in hub_choice(label):
            check(face_off(ch.get("conditions")),
                  f"7a: '{label}' can be taken while she is wearing the bought face (needs face_worn is_false)")
    first_band = next((b for b in base.get("blocks", []) if b.get("type") == "group"), None)
    check(first_band is not None and flag_item((first_band.get("props") or {}).get("conditions"), "face_worn", "is_true"),
          "7a: the hub's FIRST band must be the face-on band — it has to win over every step band")
    tf = canvases.get("activity_the_face") or {}
    tfn = {n["id"]: n for n in tf.get("nodes", [])}
    for nid in ("base", "on", "off"):
        check(any(flag_item((b.get("props") or {}).get("conditions"), "bastien_at_cot", "is_true")
                  for b in (tfn.get(nid) or {}).get("blocks", []) if b.get("type") == "group"),
              f"7a: activity_the_face.{nid} has no band for him being on the bunk — she would change faces in front of him")
    if jump:
        check(fe.get("face_worn") == "unset" if (fe := {e["flag"]: e["op"] for ch in chs for e in ch.get("flagEffects", [])}) else False,
              "7a: dev_jump_count_start must land with the face OFF, the state THE COUNT is played in")

    return report()


if __name__ == "__main__":
    sys.exit(main())
