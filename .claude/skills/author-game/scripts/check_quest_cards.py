#!/usr/bin/env python3
"""Quest-card guard — the guidance page is the one surface a LOST player opens.

    python .claude/skills/author-game/scripts/check_quest_cards.py \
        games/<slug>/toml_phases/7_final_game.toml

Why this exists
---------------
Two players read a shipped game of ours and said the prose made the story hard to
follow. The legibility rules that came out of that (`references/rts-flat-prose.md`
Rules 11-14) are measured by `author-game-v2/scripts/gates.py`, and §7 check 8 tells
you to run it. **It does not read quest cards.** G43 builds its model from canvases
and reads `Beat.text`; `quest_cards` is a sibling key of `canvases` and never enters
that model. Measured on vesper at rev 195: the gate reports 115 dashes for the whole
game while the 79 quest cards alone hold 153, at 161.5 per 10k words against the
game's 16.5 and a ceiling of 35.

So the densest, hardest-to-read prose in the game was the page whose entire job is to
un-confuse somebody, and no instrument looked at it. That is the SAME failure that
produced the original complaint — doctrine without a counter — one surface over.

What it measures
----------------
PROSE, per card and in aggregate, on `text` + `tip` + `ready_text` + `terminal_text`:

  * dashes per 10k words          Rule 11.  ceiling 35.  field p50 0.99, p90 17.5
  * `, which is` glosses per 1k   Rule 12 L1.  field max 0.24
  * negation sentences            Rule 12 L2.  field max 25.76%
  * median sentence length        Rule 2.  ceiling 14
  * sentences over 25 words       reported, not gated

STRUCTURE, because both of these shipped undetected on vesper and both were found by
hand:

  * THE GOALS ARE A CHAIN — consecutive story goals should be a daisy, each shut by the
    flag that opens the next. Where that holds, exclusivity is PROVED without guessing
    at state. Where it breaks, the two are independent and the page can show both.
  * EVERY LADDER HAS A SECTION — the QuestsPage widget builds its per-character list
    FROM the cards (`_allCards` -> distinct `npc_id`), so a character with a hub and no
    cards has no section at all. On vesper the two NEW characters of the release were
    the two with no section, while five finished ones all read "Arc complete".

Honest limits
-------------
The chain check is a PROPERTY and not a simulation. It proves exclusivity where the
daisy holds and says nothing about where it breaks, because a spine card can open on a
flag no other card names and no reading of the cards alone can tell a real gap from a
canvas-set one. A break is printed for a human to read, never failed.

Speech is NOT exempt here, unlike gates.py's narration-only basis. A quest card has no
speaker: every word on it is the game talking to the player in its own voice, so a dash
in a card is never "how English writes an interruption".

Exit code: 1 if any gated measure fails or the chain is broken, else 0.
"""
import re
import statistics
import sys

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    sys.stderr.write(
        "check_quest_cards: needs Python 3.11+ (tomllib). Run under the project venv.\n"
    )
    sys.exit(2)

# ── the bars, all quoted from rts-flat-prose.md Rules 2 / 11 / 12 ──────────────
DASH_CEILING = 35.0        # per 10k words. field p50 0.99, p90 17.46, max 35.41
GLOSS_CEILING = 0.24       # per 1k words. field max
NEGATION_CEILING = 25.76   # % of sentences. field max
SENTENCE_CEILING = 14      # median words. field median 10

CARD_TEXT_KEYS = ("text", "tip", "ready_text", "terminal_text")

_GLOSS = re.compile(r",\s*(which|who)\s+(means|is|are|was|were)\b", re.I)
_NEG = re.compile(
    r"\b(not|never|no|nothing|nobody|none|cannot|nor|neither)\b"
    r"|n't\b",
    re.I,
)


def _card_words(card):
    return " ".join(str(card.get(k, "")) for k in CARD_TEXT_KEYS).strip()


def _sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def _measure(text):
    words = len(re.findall(r"[A-Za-z][A-Za-z'-]*", text))
    sents = _sentences(text)
    lens = [len(s.split()) for s in sents]
    return {
        "words": words,
        "sentences": len(sents),
        "dashes": len(re.findall(r"—|–", text)),
        "glosses": len(_GLOSS.findall(text)),
        "negations": sum(1 for s in sents if _NEG.search(s)),
        "median": statistics.median(lens) if lens else 0,
        "over25": sum(1 for n in lens if n > 25),
    }


def _rate(n, words, per):
    return (n / words * per) if words else 0.0


# ── the chain walk ─────────────────────────────────────────────────────────────
def _clause_key(c):
    return c.get("flag") or c.get("trait")


def _holds(clause, flags, traits):
    key, op, val = _clause_key(clause), clause.get("op"), clause.get("value")
    if key is None:
        return True
    if clause.get("flag"):
        cur = flags.get(key, False)
        if op == "is_true":
            return bool(cur)
        if op == "is_false":
            return not cur
        return True
    cur = traits.get(key, 0)
    return {
        "lt": cur < (val or 0),
        "lte": cur <= (val or 0),
        "gte": cur >= (val or 0),
        "gt": cur > (val or 0),
        "eq": cur == val,
        "ne": cur != val,
    }.get(op, True)


def _live(card, flags, traits):
    return all(_holds(c, flags, traits) for c in (card.get("when") or []))


def _chain_breaks(cards):
    """The DAISY property: card N closes on exactly what card N+1 opens on.

    ⚠️ A PROPERTY, NOT A SIMULATION, and that is deliberate. The first cut of this check
    walked a synthetic state forward and reported overlaps no player can reach, because
    a spine card can open on a flag NO other card names — set by a canvas rather than by
    the card before it — and the walk cannot see that from the cards alone. It bridged
    158 of 207 states and then reported a spurious pair.

    What the doctrine actually claims is checkable without guessing: consecutive story
    goals are a daisy, each one shut by the flag that opens the next
    ("the fifteenth time a card in this game closes on the next one's setter",
    5_scenes.toml). Where that holds, exclusivity is PROVED — the two cards read the same
    key with opposite operators and cannot both be live. Where it breaks, the two cards
    are independent and the page can show both; that is legal for a game whose acts run
    in parallel, so it is REPORTED and not failed.

    A card with no `when` at all is always live and is the one thing here that IS a
    defect: it renders on top of every state the game will ever reach.
    """
    spine = [(i, c) for i, c in enumerate(cards) if not c.get("npc_id")]
    closers = []   # (index, the key this card is shut by)
    problems, runs, run = [], [], 0

    for i, c in spine:
        when = c.get("when") or []
        if not when and not c.get("terminal_text"):
            problems.append(f"card #{i} carries no `when` — it renders in every state of the game")
        shut = [(_clause_key(cl), cl.get("op")) for cl in when
                if (cl.get("flag") and cl.get("op") == "is_false")
                or (cl.get("trait") and cl.get("op") in ("lt", "lte"))]
        closers.append((i, {k for k, _ in shut}))

    for n in range(len(closers) - 1):
        i, shut = closers[n]
        j, _ = closers[n + 1]
        opens = {_clause_key(cl) for cl in (spine[n + 1][1].get("when") or [])
                 if (cl.get("flag") and cl.get("op") == "is_true")
                 or (cl.get("trait") and cl.get("op") in ("gte", "gt", "eq"))}
        if shut & opens:
            run += 1
        else:
            if run:
                runs.append(run + 1)
            run = 0
    if run:
        runs.append(run + 1)

    chained = sum(r - 1 for r in runs)
    return len(spine), chained, runs, problems


def _ladders_without_cards(game):
    """Characters with a CLIMB and no section on the page.

    ⚠️ A PORTRAIT HUB ALONE IS NOT A LADDER, and that distinction is the whole gate. A
    bartender, a mechanic and a madam all render portrait hubs and none of them is a
    thing the player climbs — failing those would be the "walls state their key" error,
    firing on surfaces that are obeying the doctrine.

    The test is a GATED RUNG: a choice on that character's own hub whose condition reads
    that character's `relation`. That is what makes a hub a ladder, and a ladder with no
    card is a climb the guidance page never mentions.
    """
    carded = {c["npc_id"] for c in (game.get("quest_cards") or []) if c.get("npc_id")}
    ladders = set()
    for c in game.get("canvases") or []:
        trig = c.get("trigger") or {}
        npc = trig.get("npc")
        if not npc or not trig.get("is_repeatable"):
            continue
        for n in c.get("nodes") or []:
            for ch in ((n.get("exit_block") or {}).get("choices") or []):
                for it in (ch.get("conditions") or {}).get("items") or []:
                    if (it.get("subject") == "npc" and it.get("npc_id") == npc
                            and it.get("trait_key") == "relation"):
                        ladders.add(npc)
    return sorted(ladders - carded)


def main(argv):
    if len(argv) != 2:
        sys.stderr.write(__doc__.split("Why this exists")[0])
        return 2
    with open(argv[1], "rb") as fh:
        game = tomllib.load(fh)

    cards = game.get("quest_cards") or []
    if not cards:
        print("QUEST-CARD GUARD: no quest_cards in this game — nothing to check.")
        return 0

    joined = " ".join(_card_words(c) for c in cards)
    agg = _measure(joined)
    w = agg["words"]
    dash_rate = _rate(agg["dashes"], w, 10_000)
    gloss_rate = _rate(agg["glosses"], w, 1_000)
    neg_pct = (agg["negations"] / agg["sentences"] * 100) if agg["sentences"] else 0.0

    fails = []
    print(f"QUEST-CARD GUARD — {len(cards)} cards, {w} words, {agg['sentences']} sentences\n")

    def line(label, value, bar, ok, note):
        nonlocal fails
        print(f"  [{'PASS' if ok else 'FAIL'}]  {label:<26s} {value:<24s} {note}")
        if not ok:
            fails.append(label)

    line("prose texture", f"{dash_rate:.1f} dashes/10k", DASH_CEILING,
         dash_rate <= DASH_CEILING,
         f"ceiling {DASH_CEILING:.0f} · field p50 0.99, p90 17.5 · {agg['dashes']} total")
    line("the sentence explains itself", f"{gloss_rate:.2f} glosses/1k", GLOSS_CEILING,
         gloss_rate <= GLOSS_CEILING,
         f"field max {GLOSS_CEILING} · {agg['glosses']} total")
    line("what did not happen", f"{neg_pct:.1f}% of sentences", NEGATION_CEILING,
         neg_pct <= NEGATION_CEILING,
         f"field max {NEGATION_CEILING}% · {agg['negations']} sentences")
    line("sentence length", f"median {agg['median']:.0f} words", SENTENCE_CEILING,
         agg["median"] <= SENTENCE_CEILING,
         f"ceiling {SENTENCE_CEILING} · {agg['over25']} sentences over 25 words")

    total, chained, runs, problems = _chain_breaks(cards)
    longest = max(runs) if runs else 0
    line("the goals are a chain", f"{chained}/{max(total - 1, 1)} links", 0, not problems,
         f"each goal shut by the flag that opens the next · longest unbroken run {longest} cards")
    for p in problems:
        print(f"          · {p}")
    if runs:
        print(f"          · runs of {sorted(runs, reverse=True)} · a break is two independent goals, "
              f"legal when acts run in parallel — read it, do not assume it")

    orphans = _ladders_without_cards(game)
    line("every ladder has a section", f"{len(orphans)} without cards", 0, not orphans,
         "a portrait hub with no card renders NO section on the page")
    for o in orphans:
        print(f"          · {o} has a standing hub and no quest card — no section, no guidance")

    # the worst offenders, so a rewrite has somewhere to start
    worst = sorted(
        ((_rate(_measure(_card_words(c))["dashes"], _measure(_card_words(c))["words"], 10_000), i)
         for i, c in enumerate(cards) if _measure(_card_words(c))["words"] >= 40),
        reverse=True,
    )[:6]
    if worst and worst[0][0] > DASH_CEILING:
        print("\n  densest cards by dash rate:")
        for rate, i in worst:
            if rate <= DASH_CEILING:
                break
            when = " AND ".join(
                f"{_clause_key(cl)} {cl.get('op')}" for cl in (cards[i].get("when") or [])
            ) or "(always)"
            print(f"          · card #{i:<3d} {rate:6.1f}/10k   WHEN {when}")

    print()
    if fails:
        print(f"  {len(fails)} measure(s) failed: {', '.join(fails)}")
        return 1
    print("  all measures pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
