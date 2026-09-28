# OPENING — the screen walk  `[REVIEW]`

**Shape: STAGED OPEN, cast load ONE.** F1 is a consistency rule — the cast load and the word budget
have to agree. Exactly one person enters, is described, speaks, and states what he wants. Nobody
else is named. Marty, Rae and Tobin do not exist yet; each arrives through their own meeting.

⚠️ **The defect F1 names is the middle** — a cold open carrying a staged open's payload. Our
measured failure named six people, two of whom were not in the game. This names one, and he is on
screen.

---

<pre>
  #  canvas · node                    what is on the screen                      the button
 ────────────────────────────────────────────────────────────────────────────────────────────────
  0  Start                 <b>engine</b>     title card · age gate                      "✓ I am 18 or older - Enter Game"
  1  CustomizeCharacters   <b>engine</b>     2 fields · headings are the engine's       "Continue to Game"
                                       our only authored text is <b>player_description</b>
 ────────────────────────────────────────────────────────────────────────────────────────────────
  2  intake · <i>the_room</i>                the county office, 15:00 Tuesday.          "He opens the folder."
                                       Four weeks served. A chair. No name yet.
  3  intake · <i>the_file</i>                DELGADO speaks. He is about to read        <b>THE START CHOICE — 3 buttons</b>
                                       the top sheet back to her.                  "Let him read it."      → past_paper
                                                                                   "Say it before he does." → past_hands
                                                                                   "Ask what it says."      → past_wheel
  4  intake · <i>the_terms</i>               He states all of it: the box, the          "Sign it."
                                       radius, eight o'clock, the sheet,
                                       Tuesday at two. Sets <b>met_delgado</b>.
     ── location exit ── ▶  <b>her_room</b> · +100 min · flagEffects met_delgado · effects battery set 100
 ────────────────────────────────────────────────────────────────────────────────────────────────
     <b>THE FUNNEL ENDS.</b>  her_room, Tuesday 16:40.
     Live at that minute:  the dock (battery) · the wardrobe · the stairwell and the laundry
                           through it are one click down ·
                           <b>martys is open until 19:00 and card_the_sheet points at it</b>
</pre>

**Rows 0 and 1 go in even though we do not author them.** Leaving them off is how a sheet describes
an opening the player never has. `Start` renders the title and the age gate; declaring one
`[[player.customization_fields]]` builds `CustomizeCharacters` and **repoints the age gate at it**
(`v2.py:1065`, `v2.py:9251`).

---

## The creation screen — 2 fields, both read back

W1: the field reads every created value a median of **four** times and the median game leaves
**none** unread. Ours read 12 times across 14 fields with **6 read nowhere at all**.

| field | type | reads |
|---|---|---|
| `name` | text (reserved id → `$player.name`) | Delgado says it · the sheet prints it · Marty says it · Rae never does, and that is characterisation |
| `look` | select — what the file photo shows: *cropped short* · *grown out* · *dyed back* | the file at screen 3 · the mirror in her room · the county office row · Tobin, once |

**Two, not three.** Field median is 3 and W3 sets **no threshold, deliberately** — the largest
creation screen in the corpus is 59 fields and the only one anyone asked to skip, at n = 1. Two
fields that are read four times each beats three where one is dead.

⚠️ **`player_description` is the only text we own on that screen** (`v2.py:9509`). Written, or the
game ships the engine's product voice as the second thing a player reads.

---

## The start choice — F1 + `the-want.md` §1

The scene already asks it: he has the folder open and he reads the top sheet back to everyone. **A
memory, not a slider**, and no stat screen.

| button | flag | what it buys — REACH, never flavour |
|---|---|---|
| *"Ask what it says."* | `past_wheel` | she can drive. Marty's van on deliveries — the only legitimate way to touch the edge of the zone in week one |
| *"Let him read it."* | `past_paper` | she can keep books. Marty's ledger by week three, and the hours sheet becomes a document she knows how to alter |
| *"Say it before he does."* | `past_hands` | nobody in the block leans on her twice. Opens the refusal side |

**Read at 5 sites each** — the three work surfaces at `martys`, plus a paired privilege rung on two
of them. **Additive only**: each original rung keeps its numbers and gains `<flag> is_false`, so
nothing closes and a pre-choice save reads what it read yesterday.

⚠️ **The placement trap.** Adjacent `[group]` blocks merge into ONE if/elseif chain and first match
wins (`v2.py:14637`). `work_counter` and `work_books` both already carry a band ladder. **Separate
each past-band from it with a non-`group` block** or that ladder is silently unreachable for every
player carrying a past.

---

## F3 · the handover lands on an open door

```
[time] starting_hour = 15, Tuesday          15:00   ← Delgado's own window is Tue 14:00-16:00
intake, three nodes                         ~15:00
location exit, time_progression 100 min     16:40   her_room  (via bowen_street › the_stairwell)
```

At 16:40 the dock is live, the wardrobe is live, and `martys` is open for another 2h20. **The
opening's last click does not land on a locked world.**

⚠️ **`[time] starting_day` index is NOT asserted here.** The design needs a Tuesday because the
whole game orbits Tuesday at two; the index that produces one is verified at build, not guessed.

## F4b · the opening refuses nothing

Three screens, seven buttons, and not one of them says no to the player. The start choice colours
and gates; it does not block. Course of Temptation's opening carries seven conditionals and **not
one refusal**, and it is the largest in the corpus.

## F5 / F8 · one flag, one character

`met_delgado` opens **Delgado's hub and nothing else.** Three of six v2 games gated the whole cast
on one opening flag — `back_home`'s `arrival_done` opens four hubs — which is the cold-spawn cast
with a coat on.

⚠️ **Marty, Rae and Tobin have NO schedule rows until their meeting fires.**
`getNpcsWithSchedules` (`v2.py:3537`) surfaces every declared NPC on the Schedule page from day one
regardless of any gate, so a schedule given early spoils the entrance.
