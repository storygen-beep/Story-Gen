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

Sentence length per canvas lives in joints.py, not here.
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
        low = word.lower().strip("'’-")
        if word.startswith("@"):
            slug = low.lstrip("@").split(".")[0]
            out.append(("ref", word, genders.get(slug, UNKNOWN)))
            continue
        if low in ROLE_GENDER:
            out.append(("ref", word, ROLE_GENDER[low]))
            continue
        # A capitalised word that does not open a sentence is a name.
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
    print(f"\n  readable — {label}")
    print(f"  {len(hits)} pronoun(s) with nothing to point at\n")
    if hits:
        print("  A PRONOUN WITH NO ANTECEDENT — the player cannot tell who this is")
        for cid, nid, word, line, one_shot in hits:
            mark = "  <-- ONE-SHOT, may be the player's first sight of them" if one_shot else ""
            print(f"    \"{word}\"  {cid} / {nid}{mark}")
            print(f"           {line}")
        print()
    else:
        print("  every third-person pronoun has somebody named or roled ahead of it\n")

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

    print("  A LIST, NEVER A SCORE. Fragments are legitimate writing. What is not")
    print("  legitimate is a sentence the reader cannot resolve — see process/README.md §5a")
    print("  for the three forces that produce these, and §5b for the ladder that fixes them.\n")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
