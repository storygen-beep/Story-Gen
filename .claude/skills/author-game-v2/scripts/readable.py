"""readable.py — three checks for prose a player cannot follow. Imported by gates.py.

PRD_IDEAS_AND_CRAFT IC6. Three checks, each for a line a player cannot follow on first
play:

  A · a pronoun with nobody on screen to point at — "Your aunt doesn't know he paid",
      where "aunt" is who "he" is NOT;
  B · short lines with no verb — the shape compressed prose takes ("Five bucks.
      Quick.");
  C · a past event the player was never given — "What happened on Friday?", on the
      first morning, when nothing had.

The pronoun set follows `[settings] narration_person`; the "universal" flags (a gate
that proves nothing) are passed in by the caller instead of hard-coded; the role list
carries US and UK words; and B accepts a word ending in -ed as a verb, the same rule the
field was measured with.

Every result is a LIST for a human to read. None of these is a verdict: A and C have
no field figure at all, and B's share is only printed beside the field's.
"""
import re

PROSE_TYPES = ("paragraph", "thought_bubble")

# Third person SINGULAR only. they/them are left out on purpose: they hit plural common
# nouns ("bins … one of them").
PRONOUN = re.compile(r"\b(he|him|his|she|her|hers)\b", re.I)
MALE, FEMALE, UNKNOWN = "m", "f", "?"
PRONOUN_GENDER = {"he": MALE, "him": MALE, "his": MALE,
                  "she": FEMALE, "her": FEMALE, "hers": FEMALE}

# A role identifies a person without naming them, and its gender is the whole point:
# "mum" does not answer "he".
ROLE_GENDER = {
    "mum": FEMALE, "mother": FEMALE, "mom": FEMALE, "sister": FEMALE,
    "stepsister": FEMALE, "step-sister": FEMALE, "daughter": FEMALE, "stepmom": FEMALE,
    "stepmother": FEMALE, "wife": FEMALE, "aunt": FEMALE, "barmaid": FEMALE,
    "girlfriend": FEMALE, "waitress": FEMALE, "landlady": FEMALE,
    "dad": MALE, "father": MALE, "stepdad": MALE, "step-dad": MALE, "stepfather": MALE,
    "brother": MALE, "stepbrother": MALE, "step-brother": MALE, "son": MALE,
    "husband": MALE, "uncle": MALE, "barman": MALE, "boyfriend": MALE, "waiter": MALE,
    # genderless roles still identify SOMEBODY, so they answer either pronoun
    "cousin": UNKNOWN, "housemate": UNKNOWN, "roommate": UNKNOWN,
    "flatmate": UNKNOWN, "neighbour": UNKNOWN, "neighbor": UNKNOWN,
    "boss": UNKNOWN, "manager": UNKNOWN, "landlord": UNKNOWN,
    "teacher": UNKNOWN, "professor": UNKNOWN, "lecturer": UNKNOWN, "tutor": UNKNOWN,
    "coach": UNKNOWN, "officer": UNKNOWN, "friend": UNKNOWN, "driver": UNKNOWN,
    "nurse": UNKNOWN, "bartender": UNKNOWN, "owner": UNKNOWN, "client": UNKNOWN,
}

# An unnamed person introduced as a common noun is exactly who a pronoun then means.
PERSON_NOUNS = {
    "man": MALE, "men": MALE, "guy": MALE, "bloke": MALE, "lad": MALE, "boy": MALE,
    "woman": FEMALE, "women": FEMALE, "girl": FEMALE, "lady": FEMALE,
    "somebody": UNKNOWN, "someone": UNKNOWN, "person": UNKNOWN, "people": UNKNOWN,
    "stranger": UNKNOWN, "customer": UNKNOWN, "student": UNKNOWN, "nobody": UNKNOWN,
}

# Capitalised mid-sentence without being anybody's name.
NOT_A_NAME = {
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
    "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december",
    "i", "you", "your", "the", "a", "an", "it", "he", "she", "they",
}

# Approximate on purpose: there is no tagger, so a curated list, a contraction rule, a
# subject-then-word rule and an -ed rule. It misses some and over-calls others, which
# is tolerable because B is a list a human reads.
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
# A subject pronoun followed by another word is a finite clause essentially always.
SUBJECT_VERB = re.compile(r"^\W*(you|he|she|it|they|we|i|there|that|this)\s+\w+", re.I)

WEEKDAY = "monday|tuesday|wednesday|thursday|friday|saturday|sunday"
WEEKDAY_NAMES = tuple(WEEKDAY.split("|"))

# (pattern, why, needs_a_flag). The patterns are narrow on purpose: a weekday on its
# own is a standing fact (her shift IS Tuesday); what is listed is a reference to one
# PAST occasion. needs_a_flag marks the lines that claim the PLAYER REMEMBERS a thing
# — no meter threshold can establish a memory, only a flag can.
EVENT_PATTERNS = (
    (re.compile(rf"\babout (?:the \w+ on )?(?:{WEEKDAY})\b", re.I),
     "somebody is expected to know what happened that day", False),
    (re.compile(rf"\b(?:{WEEKDAY}) night\b", re.I),
     "a specific night, which the clock never recorded", False),
    (re.compile(rf"\b(?:was|were|had)\b[^.!?]*\b(?:{WEEKDAY})\b", re.I),
     "puts her somewhere on a named day, in the past", False),
    (re.compile(rf"\bon a (?:{WEEKDAY})\b", re.I),
     "one particular day, in a canvas that fires on any of them", False),
    (re.compile(r"\bthe thing on\b", re.I),
     '"the thing" is an event the player has to recognise', True),
    (re.compile(r"\byou know which one\b", re.I),
     "claims she remembers a particular occasion", True),
    (re.compile(r"\bwhat happened\b(?!\s+to\s+(?:it|that|this|them|him|her|the)\b)", re.I),
     "points at an event without naming it", True),
    (re.compile(r"\b(?:last night|last week|the other day|that night)\b", re.I),
     "a past occasion the state may not have", False),
)


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


def scan(text, genders=None):
    """Refs and pronouns in reading order. An UNKNOWN ref answers either pronoun."""
    genders = genders or {}
    out = []
    for m in re.finditer(r"@\w+(?:\.\w+)?|[A-Za-z][A-Za-z'’-]*", text):
        word = m.group(0)
        low = word.lower().strip("'’-")
        for suffix in ("'s", "’s", "s'", "s’"):          # the possessive is still the name
            if low.endswith(suffix) and len(low) > len(suffix):
                low = low[: -len(suffix)] if suffix.startswith(("'", "’")) else low[:-1]
                break
        if word.startswith("@"):
            out.append(("ref", word, genders.get(low.lstrip("@").split(".")[0], UNKNOWN)))
            continue
        if low in ROLE_GENDER:
            out.append(("ref", word, ROLE_GENDER[low]))
            continue
        if low in PERSON_NOUNS:
            out.append(("ref", word, PERSON_NOUNS[low]))
            continue
        if low in genders:                                  # a cast name counts anywhere
            out.append(("ref", word, genders[low]))
            continue
        before = text[:m.start()].rstrip()
        sentence_initial = (not before) or before[-1] in ".!?\"”"
        if word[0].isupper() and not sentence_initial and low not in NOT_A_NAME:
            out.append(("ref", word, genders.get(low, UNKNOWN)))
            continue
        if PRONOUN.fullmatch(low):
            out.append(("pro", word, PRONOUN_GENDER[low]))
    return out


def events(node, genders=None):
    """Refs and pronouns on one screen. A dialog block with an npcId is a ref: the
    speaker's name renders above the line."""
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
    exit_block = node.get("exit_block") or {}
    for choice in exit_block.get("choices") or []:
        if isinstance(choice.get("text"), str):
            out.extend(scan(choice["text"], genders))
    if isinstance(exit_block.get("text"), str):
        out.extend(scan(exit_block["text"], genders))
    return out


def npc_genders(game):
    """slug / name -> gender, from each NPC's declared `role` (no gender field exists)."""
    out = {}
    for npc in game.get("npcs") or []:
        role = str(npc.get("role") or "").lower()
        gender = next((g for word, g in ROLE_GENDER.items()
                       if g != UNKNOWN and re.search(rf"\b{re.escape(word)}\b", role)),
                      UNKNOWN)
        slug = str(npc.get("id") or "")
        out[slug] = gender
        out[slug[4:] if slug.startswith("npc_") else slug] = gender
        if npc.get("name"):
            out[str(npc["name"]).lower()] = gender
    return out


def guaranteed_referents(canvas, genders=None):
    """For each node, the referents present on EVERY path to it from the entry."""
    nodes = canvas.get("nodes") or []
    if not nodes:
        return {}
    ids = [n.get("id") for n in nodes]
    introduced = {n.get("id"): {(p, g) for k, p, g in events(n, genders) if k == "ref"}
                  for n in nodes}
    edges = {i: set() for i in ids}
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
    for _ in range(len(ids) + 2):
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


def _answers(known, want):
    return any(g == UNKNOWN or g == want for _, g in known)


def _first_line(node):
    for block in blocks_of(node):
        if block.get("type") in PROSE_TYPES and isinstance(block.get("content"), str):
            text = block["content"]
            return text if len(text) <= 88 else text[:85] + "…"
    return ""


def dangling(game):
    """Check A over canvases and locations. Returns (rows, note).

    A canvas with `npc` on its trigger is skipped: the player clicked that person's name
    to get there. In third-person narration the protagonist's own pronoun is on every
    screen, so the check does not run and says so.
    """
    person = str((game.get("settings") or {}).get("narration_person") or "second")
    if person == "third":
        return [], "not run — third-person narration puts her own pronoun on every screen"
    genders = npc_genders(game)
    rows = []
    for canvas in game.get("canvases") or []:
        trigger = canvas.get("trigger") or {}
        if trigger.get("npc"):
            continue
        one_shot = trigger.get("is_repeatable") is False
        arriving = guaranteed_referents(canvas, genders)
        for node in canvas.get("nodes") or []:
            known = set(arriving.get(node.get("id")) or set())
            for kind, payload, gender in events(node, genders):
                if kind == "ref":
                    known.add((payload, gender))
                elif not _answers(known, gender):
                    rows.append((not one_shot, f"{canvas.get('id')}/{node.get('id')}: "
                                 f"\"{payload}\" — {_first_line(node)}"))
                    break
    # A place's text is read on every entry, with nothing before it.
    for loc in game.get("locations") or []:
        fields = [(f, loc.get(f)) for f in ("description", "blocked_message")]
        fields += [("description_variant", v.get("text"))
                   for v in loc.get("description_variants") or [] if isinstance(v, dict)]
        for field, text in fields:
            if not isinstance(text, str):
                continue
            known = set()
            for kind, payload, gender in scan(text, genders):
                if kind == "ref":
                    known.add((payload, gender))
                elif not _answers(known, gender):
                    excerpt = text if len(text) <= 88 else text[:85] + "…"
                    rows.append((True, f"{loc.get('id')}.{field}: \"{payload}\" — {excerpt}"))
                    break
    return [r for _, r in sorted(rows)], ""        # one-shot screens first


def _gated(conditions, universal):
    any_gate = flag_gate = False
    for cond in conditions or []:
        for item in cond.get("items") or []:
            if not isinstance(item, dict):
                continue
            kind, key = item.get("type"), item.get("flag_key")
            if kind == "flag" and key in universal:
                continue
            any_gate = True
            flag_gate = flag_gate or kind == "flag"
    return any_gate, flag_gate


def _scoped_blocks(node):
    """(block, conditions in scope, inside a pool). A group adds its conditions; a
    block_pool adds nothing and never can — it picks at random."""
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


def unearned_events(game, universal=(), needs_clothing=None):
    """Check C. `universal` = flags true for essentially the whole game, which prove
    nothing about any one event. A canvas whose schedule pins exactly the day a line
    names has that day proved.

    `needs_clothing` switches it to the truth rule's rule 5 (her clothes): a dict of
    `find(text, block)` -> [(phrase, garment)] — the lines that name her clothes — and
    `backed(canvas, node, conditions, garment, text, phrase)` -> whether a check backs
    it. Both come from the caller, which knows the game's own catalog."""
    universal = set(universal)
    rows = []
    for canvas in game.get("canvases") or []:
        trigger = canvas.get("trigger") or {}
        tc = trigger.get("conditions")
        trigger_conditions = [tc] if isinstance(tc, dict) and tc.get("items") else []
        pinned = {WEEKDAY_NAMES[i] for s in trigger.get("schedules") or []
                  for i in s.get("weekdays") or [] if isinstance(i, int) and 0 <= i < 7}
        for node in canvas.get("nodes") or []:
            for block, scope, in_pool in _scoped_blocks(node):
                if block.get("type") not in PROSE_TYPES + ("dialog",):
                    continue
                text = block.get("content")
                if not isinstance(text, str):
                    continue
                if needs_clothing:
                    for phrase, garment in needs_clothing["find"](text, block):
                        if not needs_clothing["backed"](canvas, node, trigger_conditions + scope,
                                                        garment, text, phrase):
                            rows.append(f"{canvas.get('id')}/{node.get('id')}: \"{phrase}\" — "
                                        f"names her clothes with no clothing check behind it"
                                        + (" (inside a block_pool)" if in_pool else ""))
                    continue
                for pattern, why, needs_flag in EVENT_PATTERNS:
                    hit = pattern.search(text)
                    if not hit:
                        continue
                    named = {d for d in WEEKDAY_NAMES
                             if re.search(rf"\b{d}\b", hit.group(0), re.I)}
                    if named and named == pinned:
                        break
                    any_gate, flag_gate = _gated(trigger_conditions + scope, universal)
                    if not any_gate or (needs_flag and not flag_gate):
                        rows.append(f"{canvas.get('id')}/{node.get('id')}: "
                                    f"\"{hit.group(0).strip()}\" — {why}"
                                    + (" (inside a block_pool)" if in_pool else ""))
                    break
    return rows


def is_verbless(sentence, cap=8):
    """True / False for a sentence of 1..cap words; None when it is longer."""
    words = sentence.split()
    if not (0 < len(words) <= cap):
        return None
    low = {w.lower().strip(".,!?;:'’\"") for w in words}
    if low & FINITE_VERBS or CONTRACTED.search(sentence) or SUBJECT_VERB.match(sentence):
        return False
    if any(len(w) > 3 and w.endswith("ed") for w in low):
        return False
    return True


def verbless(game):
    """Check B. Returns (rows, sentences seen). Paragraph and thought text only."""
    rows, seen = [], 0
    for canvas in game.get("canvases") or []:
        for node in canvas.get("nodes") or []:
            for block in blocks_of(node):
                if block.get("type") not in PROSE_TYPES or not isinstance(block.get("content"), str):
                    continue
                for sentence in re.split(r"(?<=[.!?])\s+", block["content"]):
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    seen += 1
                    if is_verbless(sentence):
                        rows.append(f"{canvas.get('id')}/{node.get('id')}: {sentence}")
    return rows, seen
