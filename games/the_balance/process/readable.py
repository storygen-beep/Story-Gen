#!/usr/bin/env python3
"""Can a player actually read this screen — a LIST, never a score.

Run from the repo root:

    venv/bin/python games/the_balance/process/readable.py [slug]
    venv/bin/python games/the_balance/process/readable.py --toml <path>   # any TOML, for regression

WHY THIS EXISTS
---------------
LO read the shipped opening and asked who paid, and how the player was meant to
know. Screen one of the game ended:

    "Your mum doesn't know he paid."

and the player had met nobody. No name, no role, no antecedent anywhere on the
screen. That is not a typo. Three forces push every beat the same way and nothing
in the build pushes back:

1. EVERY WRITING THRESHOLD IS A MAXIMUM. `gates.py:7390` is the whole thing in one
   line — `gate("sentence length", ... med_sent <= SENTENCE_CEILING, ...)`. It passes
   MORE comfortably the shorter you write; a median of 3 words clears it by the
   widest possible margin. Same direction for DASH_CEILING, NARRATION_DIALOGUE_
   CEILING, MENU_CEILING, FIELD_NEGATION_MAX. The floors that exist are about
   explicit content and media volume, not about whether a sentence can be read.
   Grep that file for `too short`, `sentence_floor`, `min_words`, `finite verb` or
   `antecedent` and nothing comes back. THAT is the gap this file fills.
2. THE BEAT BUDGET MAKES GRAMMAR THE CHEAPEST CUT. ~35-40 words per beat is correct
   and measured. But when you shop for words to lose, the subject and the verb are
   the cheapest, because they carry no information: "You turned eighteen last month"
   (5 words) -> "Eighteen last month." (3 words). The fact survives; the sentence
   does not; nothing measures the sentence.
3. CAVEMAN ULTRA BLEEDS. CLAUDE.md:60 puts this repo's CHAT in a register that drops
   articles and likes fragments, and CLAUDE.md:86 says outright "A beat is persisted
   text. Compression has never governed a beat and must not start." The prose is
   written in the same session as the chat. "Eighteen last month." IS caveman ultra.

⚠️ WHY THIS IS NOT A COMPRESSION SCORE. `register.md:1041-1043` measured fragment
density across the field and REFUSED a threshold — the range is 5.3% to 58.6% and
nothing survives it. Fragments are legitimate: "Six hours. You had two seconds."
is correct writing. So this file scores nothing. It finds two defects that are
FACTS rather than judgments, and prints them for a human to read — the same
contract as joints.py and tokens.py.

A third check joined them on 2026-09-16, after LO read the college scenes and
asked "What happened on Tuesday?? People are talking about it in college??".
Nothing had happened on Tuesday. That is check A one level out: a pronoun points
at a PERSON with nobody to point at, "the thing on Tuesday" points at an EVENT
that never happened. Same failure, so it lives in the same file.

Sentence length per canvas lives in joints.py, not here.

HOW TO PROVE THIS FILE STILL WORKS
----------------------------------
A check that cannot catch the bug that caused it is decoration. Each check has a
commit whose TOML it MUST flag — run it with --toml against that revision:

    git show 5f8424a:games/the_balance/toml_phases/7_final_game.toml > /tmp/a.toml
    venv/bin/python games/the_balance/process/readable.py --toml /tmp/a.toml
    # check A must flag canvas_opening / wake — "Your mum doesn't know he paid."

    git show 1c9837c:games/the_balance/toml_phases/7_final_game.toml > /tmp/c.toml
    venv/bin/python games/the_balance/process/readable.py --toml /tmp/c.toml
    # check C must flag 5: gil_notices, paige_is_nice and bree_takes_it_home (all
    # three in a block_pool), picked_quad's "you know which one", and
    # friday_payment/less "about Tuesday" — plus dinner and picked_stop on the
    # eyeball list. Against HEAD it must find ZERO.
"""

import pathlib
import re
import sys
import tomllib

PROSE_TYPES = ("paragraph", "thought_bubble")

# Third person SINGULAR only. This game declares narration_person = "second", so the
# protagonist is always "you"/"your" and can never be a dangling pronoun.
#
# ⚠️ they/them/their are deliberately NOT here. Measured over this game they produced
# 12 hits and every one was a plural common noun doing its job — "bins … one of them",
# "twenty minutes and you spend every one of them". A plural pronoun in this register
# almost never points at a person, so including it buys noise and no signal.
PRONOUN = re.compile(r"\b(he|him|his|she|her|hers)\b", re.I)
MALE, FEMALE, UNKNOWN = "m", "f", "?"
PRONOUN_GENDER = {"he": MALE, "him": MALE, "his": MALE,
                  "she": FEMALE, "her": FEMALE, "hers": FEMALE}

AT_TOKEN = re.compile(r"@(\w+)")

# A role identifies a person without naming them, which is exactly the fix the
# opening needed — so any of these standing in the prose is an antecedent.
#
# ⚠️ AND THE GENDER IS THE WHOLE POINT. Without it this check does not catch the bug
# that caused it. The opening's screen one read "Your mum doesn't know he paid." An
# earlier version saw "mum", called it a referent, and passed the line — but "mum" is
# who "he" is NOT. A referent only answers a pronoun when their genders can agree.
ROLE_GENDER = {
    "mum": FEMALE, "mother": FEMALE, "mom": FEMALE, "sister": FEMALE,
    "stepsister": FEMALE, "step-sister": FEMALE, "daughter": FEMALE,
    "wife": FEMALE, "aunt": FEMALE, "barmaid": FEMALE, "girlfriend": FEMALE,
    "dad": MALE, "father": MALE, "stepdad": MALE, "step-dad": MALE,
    "brother": MALE, "stepbrother": MALE, "step-brother": MALE, "son": MALE,
    "husband": MALE, "uncle": MALE, "barman": MALE, "boyfriend": MALE,
    # genderless roles still identify SOMEBODY, so they answer either pronoun
    "cousin": UNKNOWN, "housemate": UNKNOWN, "roommate": UNKNOWN,
    "flatmate": UNKNOWN, "neighbour": UNKNOWN, "neighbor": UNKNOWN,
    "boss": UNKNOWN, "manager": UNKNOWN, "landlord": UNKNOWN,
    "teacher": UNKNOWN, "lecturer": UNKNOWN, "tutor": UNKNOWN,
    "officer": UNKNOWN, "friend": UNKNOWN, "driver": UNKNOWN, "nurse": UNKNOWN,
}

# ⚠️ A PERSON NOUN IS AN ANTECEDENT TOO. Found by reading this lint's own output:
# it flagged "the man at the window table puts a ten under his saucer" and
# "Somebody two seats along ... She does not say what", and in both the prose is
# correct — an unnamed person introduced as a common noun is exactly who the pronoun
# then refers to. Without these the lint blames the game for its own blind spot.
PERSON_NOUNS = {
    "man": MALE, "men": MALE, "guy": MALE, "bloke": MALE, "lad": MALE, "boy": MALE,
    "woman": FEMALE, "women": FEMALE, "girl": FEMALE, "lady": FEMALE,
    "somebody": UNKNOWN, "someone": UNKNOWN, "person": UNKNOWN, "people": UNKNOWN,
    "stranger": UNKNOWN, "customer": UNKNOWN, "student": UNKNOWN, "nobody": UNKNOWN,
}

# Words that are capitalised mid-sentence without being anybody's name. Without
# this list every weekday and month reads as a character.
NOT_A_NAME = {
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december",
    "i", "you", "your", "the", "a", "an", "it", "he", "she", "they",
}

# Approximate, and deliberately so — see the note on check B in main(). Finite
# verbs and auxiliaries common to this register. A sentence carrying none of these
# AND under the length cap is listed for a human to look at; it is not a verdict.
FINITE_VERBS = {
    "am", "is", "are", "was", "were", "be", "been", "being",
    "has", "have", "had", "do", "does", "did", "done",
    "will", "would", "can", "could", "shall", "should", "may", "might", "must",
    "goes", "go", "went", "gone", "comes", "come", "came", "gets", "get", "got",
    "says", "say", "said", "tells", "tell", "told", "asks", "ask", "asked",
    "puts", "put", "takes", "take", "took", "gives", "give", "gave",
    "looks", "look", "looked", "sits", "sit", "sat", "stands", "stand", "stood",
    "runs", "run", "ran", "walks", "walk", "walked", "turns", "turn", "turned",
    "knows", "know", "knew", "wants", "want", "wanted", "needs", "need", "needed",
    "pays", "pay", "paid", "costs", "cost", "starts", "start", "started",
    "keeps", "keep", "kept", "leaves", "leave", "left", "makes", "make", "made",
    "opens", "open", "opened", "shuts", "shut", "closes", "close", "closed",
    "works", "work", "worked", "eats", "eat", "ate", "drinks", "drink", "drank",
    "watches", "watch", "watched", "waits", "wait", "waited", "moves", "move",
    "holds", "hold", "held", "pulls", "pull", "pulled", "pushes", "push", "pushed",
    "lets", "let", "lives", "live", "lived", "means", "mean", "meant",
    "hears", "hear", "heard", "sees", "see", "saw", "feels", "feel", "felt",
    "thinks", "think", "thought", "brings", "bring", "brought", "sends", "send",
    "smells", "smell", "smelled", "drags", "drag", "dragged", "catches", "catch",
    "mention", "mentions", "mentioned", "beats", "beat", "counts", "count",
}
CONTRACTED = re.compile(r"\b\w+n't\b|\b\w+'(s|re|ve|ll|d|m)\b", re.I)

# ── check C · an event the player was never given ────────────────────────────
#
# LO, 2026-09-16: "What happened on Tuesday?? People are talking about it in
# college??" Nothing had happened on Tuesday. Three characters referred to it on
# the first morning of the game.
#
# THIS IS CHECK A ONE LEVEL OUT. A pronoun points at a PERSON; "the thing on
# Tuesday" points at an EVENT. Both fail the same way — the prose assumes a memory
# the player was never given — so they belong in the same file.
#
# ⚠️ THE PATTERNS ARE DELIBERATELY NARROW, and the narrowness is the whole design.
# A weekday on its own is NOT a hit: this game's shifts really are Tuesday and
# Sunday, Friday really is the payment, classes really are Monday/Wednesday and
# Tuesday/Thursday. Those are standing facts the game declares, and flagging them
# would bury the real hits — which is exactly how an earlier version of this file
# reported 22 rows with 15 of its own bugs among them. What is listed is a
# reference to a SPECIFIC PAST OCCASION.
WEEKDAY = "monday|tuesday|wednesday|thursday|friday|saturday|sunday"
WEEKDAY_NAMES = tuple(WEEKDAY.split("|"))

# Each row is (pattern, why, needs_a_flag).
#
# ⚠️ needs_a_flag IS THE INTERESTING COLUMN. Most of these can honestly be carried
# by a METER, because a meter can encode an occurrence: attend_3 below 40 means she
# really did skip the class, dare_chain at 1 means she really did the dare. But
# three of them do not claim that a thing happened — they claim THE PLAYER
# REMEMBERS IT ("you know which one", "the thing on", a bare "what happened"). No
# threshold can establish a memory. Those need a flag, and a trait-only gate leaves
# them on the defect list.
EVENT_PATTERNS = (
    (re.compile(rf"\babout (?:the \w+ on )?(?:{WEEKDAY})\b", re.I),
     "somebody is expected to know what happened that day", False),
    (re.compile(rf"\b(?:{WEEKDAY}) night\b", re.I),
     "a specific night, which the clock never recorded", False),
    (re.compile(rf"\b(?:was|were|had)\b[^.!?]*\b(?:{WEEKDAY})\b", re.I),
     "puts her somewhere on a named day, in the past", False),
    # "on a Tuesday" is a particular unnamed Tuesday. "is a Thursday" is not — that
    # is one of her shifts, and an earlier draft of this pattern flagged it.
    (re.compile(rf"\bon a (?:{WEEKDAY})\b", re.I),
     "one particular day, in a canvas that fires on any of them", False),
    (re.compile(r"\bthe thing on\b", re.I),
     '"the thing" is an event the player has to recognise', True),
    (re.compile(r"\byou know which one\b", re.I),
     "claims she remembers a particular occasion", True),
    # "what happened TO IT" carries its own antecedent — the money she just said she
    # has not got. Only the bare form points off the screen.
    (re.compile(r"\bwhat happened\b(?!\s+to\s+(?:it|that|this|them|him|her|the)\b)", re.I),
     "points at an event without naming it", True),
    (re.compile(r"\b(?:last night|last week|the other day|that night)\b", re.I),
     "a past occasion the state may not have", False),
)

# A flag that is true for essentially the whole game proves nothing about any
# particular event. `opening_done` is set on screen three and never unset, so a
# canvas gated only on it is, for this check, ungated.
UNIVERSAL_FLAGS = {"opening_done"}


# A curated verb list will always miss something — "You use it." has a verb and an
# earlier version listed it. This catches the misses syntactically instead of growing
# the list forever: a subject pronoun followed by another word is a finite clause in
# English essentially always, whatever the verb happens to be.
SUBJECT_VERB = re.compile(r"^\W*(you|he|she|it|they|we|i|there|that|this)\s+\w+", re.I)


def blocks_of(node):
    """Every block a node renders, in render order, flattened through containers."""
    out = []

    def walk(blocks):
        for block in blocks or []:
            if not isinstance(block, dict):
                continue
            out.append(block)
            props = block.get("props") or {}
            for beat in props.get("beats") or []:
                walk(beat.get("blocks"))
            walk(props.get("blocks") or block.get("blocks"))

    walk(node.get("blocks"))
    return out


def events(node, genders=None):
    """(kind, payload) in the order the player meets them on this one screen.

    kind is "ref" (somebody is now identified) or "pro" (a third-person pronoun).

    ⚠️ A `dialog` block naming an npcId counts as a REF, and this is not a guess:
    the generator renders the speaker's name in a <strong> and the role in a
    <span class="dialog-role"> above the line (verified in the built HTML). Seeing
    "Gil / step dad" over a speech bubble identifies him as surely as prose does.
    """
    out = []
    for block in blocks_of(node):
        kind = block.get("type")
        props = block.get("props") or {}
        if kind == "dialog" and props.get("npcId"):
            slug = str(props["npcId"])
            out.append(("ref", f"speaker {slug}", (genders or {}).get(slug, UNKNOWN)))
        text = block.get("content")
        if kind in PROSE_TYPES + ("dialog",) and isinstance(text, str):
            out.extend(scan(text, genders))
    # Choice labels render under the prose, so they are read last.
    exit_block = node.get("exit_block") or {}
    for choice in exit_block.get("choices") or []:
        if isinstance(choice.get("text"), str):
            out.extend(scan(choice["text"], genders))
    if isinstance(exit_block.get("text"), str):
        out.extend(scan(exit_block["text"], genders))
    return out


def scan(text, genders=None):
    """Walk one string left to right, emitting refs and pronouns in order.

    Every ref carries a gender so that dangling() can tell whether it could
    actually be the person a later pronoun means. UNKNOWN answers either pronoun,
    which is the conservative choice: it suppresses a hit rather than inventing one.
    """
    genders = genders or {}
    out = []
    for m in re.finditer(r"@\w+(?:\.\w+)?|[A-Za-z][A-Za-z'’-]*", text):
        word = m.group(0)
        # ⚠️ STRIP THE POSSESSIVE BEFORE ANY LOOKUP. "Tasha's wardrobe … her lights"
        # was flagged because "tasha's" is not "tasha" in the cast list, and the
        # capitalisation fallback then skipped it for sitting at a sentence start.
        # A name in the possessive is still the antecedent.
        low = word.lower().strip("'’-")
        for suffix in ("'s", "’s", "s'", "s’"):
            if low.endswith(suffix) and len(low) > len(suffix):
                low = low[: -len(suffix)] if suffix.startswith(("'", "’")) else low[:-1]
                break
        if word.startswith("@"):
            slug = low.lstrip("@").split(".")[0]
            out.append(("ref", word, genders.get(slug, UNKNOWN)))
            continue
        if low in ROLE_GENDER:
            out.append(("ref", word, ROLE_GENDER[low]))
            continue
        if low in PERSON_NOUNS:
            out.append(("ref", word, PERSON_NOUNS[low]))
            continue
        # ⚠️ A CAST NAME COUNTS WHEREVER IT SITS, sentence-initial included. The
        # position rule below exists to stop "Monday" reading as a character; applying
        # it to a declared NPC name made the lint flag "Owen watches you do it … that
        # is how he says a thing is yours" and "Bree is telling it … in her version".
        # Both are correct prose. Check the cast list before the position heuristic.
        if low in genders:
            out.append(("ref", word, genders[low]))
            continue
        # Otherwise: a capitalised word that does not open a sentence is a name.
        before = text[:m.start()].rstrip()
        sentence_initial = (not before) or before[-1] in ".!?\"”"
        if word[0].isupper() and not sentence_initial and low not in NOT_A_NAME:
            out.append(("ref", word, genders.get(low, UNKNOWN)))
            continue
        if PRONOUN.fullmatch(low):
            out.append(("pro", word, PRONOUN_GENDER[low]))
    return out


def npc_genders(game):
    """slug / name -> gender, derived from each NPC's DECLARED `role`.

    No NPC in this schema carries a gender field, so nothing here is invented: the
    role is authored ("step dad", "mum", "step sister") and ROLE_GENDER reads it.
    An NPC whose role is genderless ("cafe owner", "runs the crowd") stays UNKNOWN
    and answers either pronoun, which is the safe direction.
    """
    out = {}
    for npc in game.get("npcs") or []:
        role = str(npc.get("role") or "").lower()
        gender = next((g for word, g in ROLE_GENDER.items()
                       if g != UNKNOWN and re.search(rf"\b{re.escape(word)}\b", role)),
                      UNKNOWN)
        slug = str(npc.get("id") or "")
        out[slug] = gender
        out[slug.removeprefix("npc_")] = gender
        if npc.get("name"):
            out[str(npc["name"]).lower()] = gender
    return out


def guaranteed_referents(canvas, genders=None):
    """For each node, the referents present on EVERY path to it from the entry.

    A "must" analysis, not a "may" one: if any route reaches this screen without
    anybody being identified, a pronoun here is dangling on that route, and that is
    the route some player takes. Entry node starts empty.
    """
    nodes = canvas.get("nodes") or []
    if not nodes:
        return {}
    ids = [n.get("id") for n in nodes]
    introduced = {
        n.get("id"): {(p, g) for k, p, g in events(n, genders) if k == "ref"}
        for n in nodes
    }

    edges = {i: set() for i in ids}          # node -> successors
    for node in nodes:
        for choice in (node.get("exit_block") or {}).get("choices") or []:
            if choice.get("targetType") != "node":
                continue
            target = str(choice.get("nodeId") or "").split(".")[-1]
            if target in edges:
                edges[node.get("id")].add(target)

    preds = {i: set() for i in ids}
    for src, dsts in edges.items():
        for dst in dsts:
            preds[dst].add(src)

    entry = ids[0]
    IN = {i: (set() if i == entry or not preds[i] else None) for i in ids}
    for _ in range(len(ids) + 2):            # small graphs; a fixpoint converges fast
        changed = False
        for i in ids:
            if i == entry or not preds[i]:
                continue
            known = [IN[p] | introduced[p] for p in preds[i] if IN[p] is not None]
            new = set.intersection(*known) if known else set()
            if IN[i] != new:
                IN[i], changed = new, True
        if not changed:
            break
    return {i: (IN[i] or set()) for i in ids}


def answers(known, want):
    """Could any referent already on screen be the person this pronoun means?

    Genders must be able to AGREE — an UNKNOWN referent answers either pronoun, a
    FEMALE one never answers "he". This is the whole reason the check catches the
    bug it was written for: screen one named "your mum" and then said "he paid".
    """
    return any(g == UNKNOWN or g == want for _, g in known)


def dangling(game):
    """Check A — a pronoun the player has nothing to attach to."""
    genders = npc_genders(game)
    hits = []
    for canvas in game.get("canvases") or []:
        trigger = canvas.get("trigger") or {}
        # ⚠️ THE EXEMPTION THAT STOPS THIS BEING NOISE. A canvas with an `npc` on its
        # trigger renders as that person's own link at the location, so the player
        # clicked their name to get here and "he" is anchored before a word is read.
        # The opening carries no npc on its trigger, which is exactly why it was bare.
        if trigger.get("npc"):
            continue
        one_shot = trigger.get("is_repeatable") is False
        arriving = guaranteed_referents(canvas, genders)
        for node in canvas.get("nodes") or []:
            known = set(arriving.get(node.get("id")) or set())
            for kind, payload, gender in events(node, genders):
                if kind == "ref":
                    known.add((payload, gender))
                elif not answers(known, gender):
                    hits.append((canvas.get("id"), node.get("id"), payload,
                                 first_line(node), one_shot))
                    break
    # One-shots first: a repeatable screen is read by somebody who has been playing,
    # a one-shot is often somebody's first sight of a person.
    return sorted(hits, key=lambda h: (not h[4], h[0], h[1]))


def dangling_locations(game):
    """Check A, again, over the text of a PLACE.

    ⚠️ ADDED AFTER THIS LINT MISSED FOUR. It walked canvases only, and a room's
    description is read on EVERY entry — more often than any canvas. `the_kitchen`
    said "the chore list is on the fridge in his handwriting", `nate_room` opened
    "His door is at the end of the landing", and neither names anybody. A location
    has no arrival context at all: you walked in, and the first thing on screen is
    the description, so there is nothing before it by definition.

    These surfaces resolve @tokens (v2.py:10035 description, :9910 blocked_message,
    :10059 variants), so the fix is the same one the opening used.
    """
    genders = npc_genders(game)
    hits = []
    for loc in game.get("locations") or []:
        fields = [(f, loc.get(f)) for f in ("description", "blocked_message")]
        fields += [("description_variant", v.get("text"))
                   for v in loc.get("description_variants") or []]
        for field, text in fields:
            if not isinstance(text, str):
                continue
            known = set()
            for kind, payload, gender in scan(text, genders):
                if kind == "ref":
                    known.add((payload, gender))
                elif not answers(known, gender):
                    excerpt = text if len(text) <= 88 else text[:85] + "…"
                    hits.append((loc.get("id"), field, payload, excerpt))
                    break
    return hits


def gates(conditions):
    """(constrains state at all, constrains it with a FLAG) for a condition list.

    Any flag / trait / npc item is the author reaching for a condition, which is the
    work this check asks for. A universal flag does not count: `opening_done` is set
    on screen three and never unset, so a canvas gated only on it is, for this
    check, ungated. A FLAG is a record that a thing HAPPENED; a trait threshold is a
    level, which is usually enough and is never enough for a claimed memory.
    """
    any_gate = flag_gate = False
    for cond in conditions or []:
        for item in (cond.get("items") or []):
            if not isinstance(item, dict):
                continue
            kind, key = item.get("type"), item.get("flag_key")
            if kind == "flag" and key in UNIVERSAL_FLAGS:
                continue
            any_gate = True
            if kind == "flag":
                flag_gate = True
    return any_gate, flag_gate


def scoped_blocks(node):
    """(block, conditions in scope, inside a pool) for every block a node renders.

    ⚠️ blocks_of() flattens the containers away, which is right for check A and
    wrong here: this check is ENTIRELY about what encloses a line. A `group` adds
    its conditions to the scope of everything inside it. A `block_pool` adds
    nothing and never can — it renders as `<<set _bp to random(0, N)>>` over its
    members (v2.py:15088) and reads no conditions at any depth. That is the
    mechanism behind every hit this check was written for.
    """
    out = []

    def walk(blocks, scope, in_pool):
        for block in blocks or []:
            if not isinstance(block, dict):
                continue
            props = block.get("props") or {}
            kind = block.get("type")
            inner = scope
            if kind == "group":
                cond = props.get("conditions") or block.get("conditions")
                if isinstance(cond, dict) and cond.get("items"):
                    inner = scope + [cond]
            out.append((block, inner, in_pool))
            for beat in props.get("beats") or []:
                walk(beat.get("blocks"), inner, in_pool)
            walk(props.get("blocks") or block.get("blocks"), inner,
                 in_pool or kind == "block_pool")

    walk(node.get("blocks"), [], False)
    return out


def pinned_weekdays(canvas):
    """Weekday names the canvas's own trigger schedules pin it to.

    A line may name the day it actually fires on. `[[canvases.trigger.schedules]]`
    carries `weekdays` as engine indices, 0 = Monday (engine.md §24.2).
    """
    days = set()
    trigger = canvas.get("trigger") or {}
    for sched in trigger.get("schedules") or []:
        for idx in sched.get("weekdays") or []:
            if isinstance(idx, int) and 0 <= idx < 7:
                days.add(WEEKDAY_NAMES[idx])
    return days


def unearned_events(game):
    """Check C — a line about an event, with nothing in scope that proves it.

    Returns (defects, unpinned_days). The first is a list in the same sense as
    check A: the state cannot back the claim, so the player cannot either. The
    second is an eyeball list — the event IS gated, but the line names a DAY the
    gate never recorded, which is the half that gating alone does not fix.
    """
    defects, unpinned = [], []
    for canvas in game.get("canvases") or []:
        trigger_conditions = []
        tc = (canvas.get("trigger") or {}).get("conditions")
        if isinstance(tc, dict) and tc.get("items"):
            trigger_conditions.append(tc)
        pinned = pinned_weekdays(canvas)

        for node in canvas.get("nodes") or []:
            for block, scope, in_pool in scoped_blocks(node):
                if block.get("type") not in PROSE_TYPES + ("dialog",):
                    continue
                text = block.get("content")
                if not isinstance(text, str):
                    continue
                for pattern, why, needs_flag in EVENT_PATTERNS:
                    hit = pattern.search(text)
                    if not hit:
                        continue
                    named = {d for d in WEEKDAY_NAMES
                             if re.search(rf"\b{d}\b", hit.group(0), re.I)}
                    # ⚠️ A SCHEDULE IS A GATE, BUT ONLY AN EXACT ONE. friday_payment
                    # says "on a Friday" and fires on nothing else —
                    # `[[canvases.trigger.schedules]]` weekdays = [4]. That day is
                    # proved, whatever the conditions say, so it is not a hit.
                    # `named <= pinned` was wrong here and let a real one through: a
                    # canvas scheduled all seven days would "prove" any day it cared
                    # to name, which is the claim itself.
                    if named and named == pinned:
                        break
                    any_gate, flag_gate = gates(trigger_conditions + scope)
                    row = (canvas.get("id"), node.get("id"), hit.group(0).strip(),
                           why, text if len(text) <= 96 else text[:93] + "…", in_pool)
                    if not any_gate or (needs_flag and not flag_gate):
                        defects.append(row)
                    elif named:
                        unpinned.append(row)
                    break
    return defects, unpinned


def first_line(node):
    for block in blocks_of(node):
        if block.get("type") in PROSE_TYPES and isinstance(block.get("content"), str):
            text = block["content"]
            return text if len(text) <= 88 else text[:85] + "…"
    return ""


def verbless(game, cap=8):
    """Check B — short sentences carrying no finite verb.

    APPROXIMATE ON PURPOSE. There is no part-of-speech tagger here, so this is a
    curated verb list plus a contraction rule, and it will miss some and over-call
    others. That is tolerable precisely because it is a LIST and not a gate: a human
    reads the lines and decides. Pairing "no verb" with "under `cap` words" is what
    keeps the noise down — a long sentence with no verb is rare, a short one is the
    shape the three forces above actually produce.
    """
    rows = []
    for canvas in game.get("canvases") or []:
        for node in canvas.get("nodes") or []:
            for block in blocks_of(node):
                if block.get("type") not in PROSE_TYPES:
                    continue
                text = block.get("content")
                if not isinstance(text, str):
                    continue
                for sentence in re.split(r"(?<=[.!?])\s+", text):
                    sentence = sentence.strip()
                    words = sentence.split()
                    if not (0 < len(words) <= cap):
                        continue
                    low = {w.lower().strip(".,!?;:'’\"") for w in words}
                    if (low & FINITE_VERBS or CONTRACTED.search(sentence)
                            or SUBJECT_VERB.match(sentence)):
                        continue
                    rows.append((canvas.get("id"), node.get("id"), len(words), sentence))
    return rows


def main():
    args = sys.argv[1:]
    if args[:1] == ["--toml"]:
        merged, label = pathlib.Path(args[1]), args[1]
    else:
        slug = args[0] if args else "the_balance"
        merged, label = pathlib.Path(f"games/{slug}/toml_phases/7_final_game.toml"), slug
    if not merged.exists():
        sys.exit(f"no TOML at {merged} — run merge_toml_phases.py first")

    game = tomllib.loads(merged.read_text(encoding="utf-8"))

    hits = dangling(game)
    loc_hits = dangling_locations(game)
    print(f"\n  readable — {label}")
    print(f"  {len(hits) + len(loc_hits)} pronoun(s) with nothing to point at "
          f"({len(hits)} on a screen, {len(loc_hits)} in a place's own text)\n")
    if loc_hits:
        print("  IN A LOCATION DESCRIPTION — read on EVERY entry, and nothing precedes it")
        for lid, field, word, excerpt in loc_hits:
            print(f"    \"{word}\"  {lid}.{field}")
            print(f"           {excerpt}")
        print()
    if hits:
        print("  A PRONOUN WITH NO ANTECEDENT — the player cannot tell who this is")
        for cid, nid, word, line, one_shot in hits:
            mark = "  <-- ONE-SHOT, may be the player's first sight of them" if one_shot else ""
            print(f"    \"{word}\"  {cid} / {nid}{mark}")
            print(f"           {line}")
        print()
    elif not loc_hits:
        print("  every third-person pronoun has somebody named or roled ahead of it\n")

    bad_events, unpinned_days = unearned_events(game)
    if bad_events:
        print(f"  {len(bad_events)} line(s) about an event the player was never given")
        print("  A CLAIM THE STATE CANNOT BACK — nothing on this route says it happened\n")
        for cid, nid, phrase, why, line, in_pool in bad_events:
            mark = "  <-- IN A block_pool, WHICH CAN NEVER BE GATED" if in_pool else ""
            print(f"    \"{phrase}\"  {cid} / {nid}{mark}")
            print(f"           {why}")
            print(f"           {line}")
        print()
    else:
        print("  every line about a past event has something in scope that proves it\n")

    if unpinned_days:
        print(f"  {len(unpinned_days)} line(s) name a DAY the gate never recorded "
              f"— NOT defects, a list to eyeball")
        print("  The event is gated. The day is the other half: a meter counts THAT she")
        print("  came in late, never WHICH NIGHT. If the state cannot name the day,")
        print("  neither can the character.\n")
        for cid, nid, phrase, why, line, in_pool in unpinned_days:
            print(f"    \"{phrase}\"  {cid} / {nid}")
            print(f"           {line}")
        print()

    rows = verbless(game)
    if rows:
        opening = [r for r in rows if r[0] == "canvas_opening"]
        rest = [r for r in rows if r[0] != "canvas_opening"]
        print(f"  {len(rows)} short sentence(s) with no finite verb — NOT defects, a list to eyeball")
        print("  register.md measured fragments across the field and REFUSED a threshold")
        print("  (5.3%-58.6%). These are ranked by where a fragment costs most: the screens")
        print("  a player reads before they have any context.\n")
        for cid, nid, n, s in opening + rest[:12]:
            mark = "  <-- first screens" if cid == "canvas_opening" else ""
            print(f"    {n:2d}w  {cid} / {nid}{mark}")
            print(f"         {s}")
        if len(rest) > 12:
            print(f"    … and {len(rest) - 12} more")
        print()

    print("  A LIST, NEVER A SCORE. Fragments are legitimate writing, and so is an hour")
    print("  the game actually declares — a shift really does start at seven, ten, one,")
    print("  four and seven. What is not legitimate is a sentence the reader cannot")
    print("  resolve, or an event they were never given.")
    print("  See process/README.md §5a for the three forces that produce these,")
    print("  and §5b for the ladder that fixes them.\n")
    return 1 if (hits or loc_hits or bad_events) else 0


if __name__ == "__main__":
    sys.exit(main())
