# Skill test findings — billable_hours

The first game built on the fixed author-game-v2 skill (branch `skill/v2-test-fixes-engine`). Each
entry records what happened, the file:line, and what was expected. None of these has been worked
around quietly; every one was raised with LO when it came up.

---

## F1 · `want.cast[].keeps` has no value for a person who does not climb (2026-09-30, phase: want)

**What happened.** The Want's cast includes two people whose job is a system rather than a ladder:
Diane, the mother, who is the house's schedule, and Pierce, head of HR, who is the risk. The
`keeps` enum offers only three values: `"step counter + memory flags" | "want + warmth" |
"want + power"` (`references/state.md:78-79`). The W1 table (`references/the-meters.md:96-102`)
frames every row as "the men keep…". `templates/want.md` §5 names its column "what she wants
from him". I wrote `"none — a schedule system"` / `"none — a risk system"`, which is outside the
enum.

**Checked, not guessed.** Nothing validates the value: `grep -n keeps scripts/gates.py
scripts/shape.py` shows no reader of `want.cast[].keeps` (shape.py:498 reads the age only).
So the off-enum value is silent today.

**Expected.** Either a declared value for a non-climbing person (`"none"`), or a line in
`the-want.md` §6 saying every cast member must climb. The skill currently implies the second
without saying it, and premises with a mother as "the price tag" or a man who is
"the consequence" need the first.

## F2 · `--words` lists the closed forms `stepbrother / stepfather / stepsister` (2026-09-30, phase: want)

**What happened.** `gates.py --words games/billable_hours/WANT.md` listed `stepbrother ×2`,
`stepfather ×2` and `stepsister ×2` among the "17 word(s) the 27-game field does not use". A scratch
file reading `step-brother … step-sister` returned `0 of 7 words sit outside the field's shared
vocabulary`. The field spells it with a hyphen (`cupids-way.txt:7133`: *"your parents and
step-brother"*).

**Not a false red.** The mode is a list and exits 0, and SKILL.md says "a list, never a score". So
this is not a defect in the checker. It is a note for authoring: write the hyphenated form in
player-facing text, and it will not show up on the list. It's recorded because a
taboo-at-home game will hit this in every step-family noun.

## F3 · `shape.py` fails `the promise has a beat this release` in lenient mode (2026-09-30, phase: idea)

**What happened.** After LO picked the step and `release_page.her_moment` was recorded (as
`templates/idea.md` §4 instructs: "Record the chosen step as `release_page.her_moment`"), `shape.py
billable_hours` in lenient mode (phase `idea`) printed:

```
[FAIL]  the promise has a beat this release        release_page.promise_alive is empty — which beat keeps the goal or mystery alive?
2 pass · 1 fail · 0 warn · 12 n/a
```

**File:line.** `scripts/shape.py:257-259` calls `row(..., False, ...)` without a strict guard. The
sibling rows for the same SP7 page report n/a when lenient: `release_page.door` at `:246` and
`release_page.weeks` at `:187` both use `False if strict else None`. The module docstring (`:8`)
says the script is "strict once the phase is `spine` or later".

**Expected.** At phase `idea`, `promise_alive` has not been written yet: it belongs to SP7, the
spine's release page, which is the next phase. It should be n/a in lenient mode, like the door and
the weeks. The red is not the game's fault, and the author is pushed to fill in an SP7 field early
just to make it go away. Not worked around: `promise_alive` stays empty until SP7 is written.

## F4 · The Want and the Pitcher both invite a scene that narrates the payment, and the engine forbids it (2026-09-30, phase: spine)

**What happened.** `templates/want.md:24` asks for "the hold… with a face and a moment it comes due".
`the-want.md:184` gives the example *"Friday, $260, and the landlord counts it at the desk"*. Following
that, I wrote WANT §2 as "He collects it in person, in his study, after dinner", and all three
Pitchers read it. The chosen pitch (M) has her hand over the $250 envelope in the study. Only at
SP4, reading `the-economy.md` R3 and `engine.md` §26, did the conflict show up:

- `engine.md` §26: *"DO NOT ALSO WRITE THE PAYMENT AS A CANVAS… If the engine takes the money, the
  authored scene beside it must be about something else."*
- The demand arms at 00:00 on `due_day` and intercepts on her next location screen
  (`v2.py:6168`, `:17397-17406`, as cited in §26). That is breakfast, not after dinner.

**File:line.** `templates/want.md:24` · `references/the-want.md:184-186` · `.claude/agents/v2-pitcher.md`
(no mention of §26, rent or payment: `grep -n "26\|rent\|payment\|settle"` finds only the
`body_as_payment` kind name at `:19`).

**Expected.** Since the Want and the idea page come before the engine files are read, the skill
should say at the Want (or in the pitch pack when `want.hold_kind = "bill"`) that the engine's rent
page collects the money at 00:00 on the due day, and that authored scenes sit beside the payment,
never on it. Instead a signed Want and a picked pitch both have to be amended at the spine.

**Not worked around.** SP4 lists three amendments (when he collects, step 1 without the envelope,
the balance under `stages`) for LO to sign. WANT and IDEA are unchanged until LO answers.

## F5 · The spine names a step's place before the board has rooms, so the board forces a re-sign (2026-09-30, phase: board)

**What happened.** SP2 (signed) gives every step a `where`. At the spine, the only places are
`want.places[]` (house, firm, club, hotel_bar), so Martin's study steps and Ethan's landing step were
written `where = "house"`. The board then split the house into rooms (`house` = the kitchen,
`her_room`, `landing`, `study`) and gave each person a schedule. `shape.py` then printed:

```
[FAIL]  the person is there at the step's hour     3/7 steps
        · npc_martin step 1: npc_martin's schedule does not cover house 19:00-22:00 on Fri
        · npc_ethan step 1: npc_ethan's schedule does not cover house 21:00-23:30 on Mon, Tue, Wed, Thu
```

**This red is correct.** The steps really do name the wrong room. The finding is about sequencing:
`shape.py:65-66` says "Places come with the board, which follows the spine", and `the-spine.md` says
"The spine changes only between releases". A spine that must name places before the places exist has
to be re-signed at the board, which is inside a release cycle, not between two.

**Expected.** Either the spine names zones and the board resolves rooms (and `ladders move forward`
reads it that way), or the-spine.md says plainly that SP2's `where` and SP7's `places` are
provisional until the board. Not worked around: the SP2/SP7 amendment was taken to LO.

## F6 · Parallel `v2-prose` agents overwrite each other's measurement file (2026-09-30, phase: board / sheets)

**What happened.** Nine `v2-prose` agents ran at once, one per explicit beat, as SKILL.md allows
("When you launch multiple agents for independent work…"). `.claude/agents/v2-prose.md:51-52` tells
each one to write its draft to `<scratchpad>/beat.txt` and run `gates.py --beat` on that file. Every
agent used the same path, so they measured each other's text. B7's agent reported "4 explicit
words" and a word list with `clit, cunt`, which are words from B4. Re-measured on its own file, B7
is 75 words, 5 explicit (`ass, cock, tits`), median 14. Three other agents noticed the clash
themselves and switched to private file names.

**File:line.** `.claude/agents/v2-prose.md:51-52` (the fixed `beat.txt` path).

**Expected.** Each call measures its own file, for example `<scratchpad>/beat_<id>.txt`, or the
agent file says not to run them in parallel. Otherwise the returned numbers can be about another
beat entirely, and they are the only numbers the caller sees.

**Not worked around quietly.** All nine beats were re-measured by the author, each from its own
file under `scratchpad/final/`. The numbers on the scene sheets come from that run, not from the
agents' reports.

## F7 · `world reachable` fails the rooms under a second root that the skill tells you to build (2026-10-01, phase: sheets → build)

**What happened.** The board is `two_hub`: two roots joined by the bus, as `the-map.md` R3 says a
game with two separate grounds should be built: *"make them two roots joined by a travel canvas…
Gate 11 walks on foot, so it exempts the second root only when that root is marked `offscreen` or
sealed"*. `gates.py billable_hours` printed:

```
[FAIL]  world reachable                  5/9 locations reachable on foot from her_room
        · club is not reachable and is not marked offscreen/sealed
        · downtown is not reachable and is not marked offscreen/sealed
        · firm is not reachable and is not marked offscreen/sealed
        · hotel_bar is not reachable and is not marked offscreen/sealed
```

**File:line.** `scripts/gates.py:7582-7587`: `exempt = {l["id"] for l in locs if l.get("offscreen") or
l.get("auto_exit") is False}`. The walk does not follow canvas location exits (the bus), and the
exemption covers only the flagged location itself, never the rooms whose `entry_from` is that
root. Marking downtown `auto_exit = false` clears downtown but leaves its three rooms stranded.
Marking the rooms too would remove their engine-built "Leave" links (`template_import.py`
`TemplateLocation.auto_exit`: "no auto Leave link"), which strands the player for real.

**Expected.** Either the walk follows `targetType = "location"` exits on repeatable canvases (the bus
is one), or an exempt root exempts the rooms under it. As it stands, the shape R3 prescribes cannot
pass gate 11.

**Not worked around.** downtown is marked `auto_exit = false` (it is sealed: only the bus reaches
it, and it has no parent, so it loses no Leave link). firm, hotel_bar and club are left as they
are, and the red stays.

## F8 · `--beat`'s act-rung readout cannot see "gropes", "fondles" or "nuzzles" (2026-10-01, build)

**What happened.** The v2-prose agent writing B12 (a grope on the bus) reported its act rungs as
`none`. Checked: `scripts/gates.py:345-346` is
`re.compile(r"\b(kiss(?:e[sd]|ing)?|caress|fondl|nuzzl|grope|touch(?:es|ed|ing)?)\b")`. The group
ends in `\b`, so the stems `fondl` and `nuzzl` never match any real word, and `caress` and `grope`
match only their bare forms. Tested: `grope` True; `gropes`, `groped`, `groping`, `fondle`, `fondled`
all False.

**Impact.** Small. `RUNGS` feeds a lint and the `--beat` readout only ("Used by a LINT ONLY", `:336`);
no gate moves. `EXPLICIT` (`:311-315`) has no trailing `\b` on those stems and still counts
"gropes". But the readout told the prose agent its beat named no act, and an agent optimising for
it would rewrite good prose to the bare word.

**Expected.** Stem forms with an inflection group, like the `kiss(?:e[sd]|ing)?` beside them.

## F9 · The reader's test 1 fails the stranger scenes the skill prescribes (2026-10-01, build)

**What happened.** `v2-reader` test 1 (`.claude/agents/v2-reader.md`, the nine-test table): *"On a
sexual step … an earlier canvas … already showed him wanting it … No earlier sign = FAIL."* It
returned FAIL for `jade_01_first_night` (the corridor, the man at the bar), and reader B returned
FAIL for `walkin_bar` and `walkin_club_lap`, all for the same reason: *"a stranger who first appears
in this canvas."*

**The contradiction.** `references/the-arc.md` A15: *"Night one may carry one hot moment from a
stranger or a one-off — never the paid route and never the main man"*, and
`references/the-release.md` § first release: *"First explicit beat early — from a stranger or a
one-off."* The skill tells the author to put night one's heat on a stranger, and the reader fails
every stranger, because a stranger has no earlier canvas by definition. Reader B improvised a rule
for it ("the same canvas's lower band counts as the earlier sign"), and reader A didn't, so two
readers on the same kind of scene disagree.

**Expected.** Test 1's "earlier sign" is scoped to a named person with a ladder (A13 is about
"his" want on a relationship), or the reader has a stated rule for strangers and walk-ons. Until
then these FAILs need LO's waiver (`release_page.reader_waivers`), because the author would be
breaking A15 to clear them.

**Not worked around.** Nothing was rewritten to clear these three FAILs. They are listed for LO.
