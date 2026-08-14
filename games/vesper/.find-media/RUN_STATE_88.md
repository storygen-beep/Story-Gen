# 88-slot approved-NSFW v3 harvest — run state (2026-08-06)

**Resume rule:** a slot is DONE if `media_options.json` → `queries[slot_key]` is non-empty.
Regenerate the todo list with that test against `v3_run_88_brief.json`; never re-issue a slot
that already has chips (the per-agent dedupe guard also enforces this, but check first).

## Contract every agent gets
- Axes are STATED in the brief, never re-derived from `type`/`media_type` (that was the 2A bug).
  FORMAT (file extension) → extraction regex only. CONTENT (band/tier) → dialect, histogram
  reading, grid glance. All 88 are `content_axis: act`.
- Gate BEFORE the write: extract + histogram + ONE grid screenshot, then stock.
- Stock with ONE `options/add_bulk` call. `hosts` POSTed RAW as `[[host,count],…]`.
- Animated slots: click "More results" ONCE. Still slots: twice pays.
- Install nothing, prune nothing, never `options/clear`/`options/remove`/`grab`.
- Captcha = HARD STOP for the whole run, never solved.
- **Agents must NOT write `run_manifest.json`** — no lock, concurrent RMW drops entries.
  The driver writes all 88 rows in ONE pass at the end.
- Every agent closes its own tab (memory: ~350 MB per grid tab on an 8 GB machine).

## Concurrency
Rolling cap 6. Binding constraint is RAM, not the extension. Watch Chrome RSS between waves;
drop to 4 if free+reclaimable falls under ~800 MB.

## Owed to the skill at end of run
1. The measured poison list + the porn-native-vs-trade-native occupation rule → SKILL.md
   §Iteration poisoned-token list.
2. `run_manifest.json` has no lock but the skill mandates fan-out → §Evidence-and-persistence.
3. `queries/add` does not echo `hosts`; verify by re-reading the chip → chrome_route.md §5.
4. Animated slots: second "More results" click is wasted → chrome_route.md §4.
5. A thin shelf on a precise query is not a failure (precise tag pages are PornHub-tile heavy,
   .jpg thumbs the animated regex can't use) → §Iteration stop conditions.

## COVERAGE GAPS — for LO, authoring decisions not query bugs
These beats are NOT retrievable at their band. Agents spent their allowed rounds and stopped
per the setting-driven stop rule; the shelves carry the nearest honest proxy.

1. **The dry-dock / work-cradle interior** (12x `salvage_session_*_t4`). `dock`, `dry dock`,
   `shipyard` are all homograph or water-sense traps; `engine room`, `foundry`, `hangar` are
   not in the porn corpus and drop silently. Proxies that DID bind: construction site,
   warehouse, basement, garage, machine shop, auto repair shop, junkyard, salvage yard.
   Shelves are right on BODY STATE, approximate on ROOM.
2. **The crew man balking** (`cell_he_does_not_stop_a_crew_man_balks_t5`). "pulls out",
   "steps back", "stops", "staring" are narrative-process words with no corpus behind them.
   Nearest proxy stocked = the cuckold/observer aisle (a clothed man apart, not participating).
   Agent's own suggestion, worth considering: **re-cut the beat so the media carries only the
   gangbang and the PROSE carries the balk.**
3. Dim/low-light room qualifiers generally — unsearchable at t5; light level has to be picked
   by eye off the shelf.

### Added 2026-08-14, from the 23-slot Mercer/Kess seed-query rewrite (pre-harvest)

4. **The calm, unhurried hold** (`sex/mercer_print_throat_t5`). The corpus splits this beat and
   offers neither half whole: the gentle-blowjob aisle has no hold, the `face fuck` aisle has
   the hold plus the aggression the beat's own `Avoid:` rejects. `hold` / `held` / `down` /
   `keeps her there` return prone-on-a-bed and supine-throat-grab — 0 survivors
   (`lexicon.md:187`); the hand at the back of the head is `NO KNOWN TERM` and has already
   killed a pool (`lexicon.md:115`). Proxy seeded: `deepthroat` + `hair pulling`, the only
   measured-live vocabulary for the hold. **Shelf will be right on POSITION and on the hold;
   approximate on REGISTER.** Judging criterion, never a query term: take the clips where his
   stance is still and his free hand idle; reject visible impact, slapping, shouting.
   **Authoring alternative** (same shape as gap #2): re-cut so the media carries only the
   kneeling oral and the PROSE carries the hold.

5. **"Unhurried, absent-minded, talks past her"** — the affect in 9 of the 15 Mercer t5
   contracts. Affect is not queryable (`lexicon.md:894`) and `unhurried` belongs to the
   `wrecked`/`senseless` written-erotica class that retrieves the fiction aisle
   (`lexicon.md:468-475`). Two proxies seeded instead: pace tags (`deep stroking`,
   `long stroke`) on MID-ACT beats only — never on a finish beat, where pace outranks the
   finish anchor (`lexicon.md:652-661`, `:676-680`) — and `cmnf` / `casting couch` /
   `quickie clothes on` on the three `print_*` handling beats, which converts the affect into
   the wardrobe fact that carries it (he never undresses). **Shelves will be right on ACT,
   POSITION and WARDROBE; approximate on TEMPERAMENT.** Expect the pace buckets to run warm,
   and expect the `facial` vocabulary to deliver the smiling-at-camera bucket
   (`lexicon.md:892-905`) — pick against it by eye.

6. **The switch from vaginal to anal** (`sex/mercer_print_anal_t5`). Not retrievable: `anal`
   holds a query inside porn but does not select the act bent-over — three independent
   confirmations (`lexicon.md:24`, `:861`, where carrying `anal` cost host purity and gained
   nothing) — and "pulls out" / "switches to" are narrative-process words with no corpus
   (gap #2's class). The shelf can only carry from-behind anal; the switch itself has to read
   as a cut or be carried by the prose. Ship the act as `unverified` per `lexicon.md:28`.

### Also noted in the same pass — a gate limit, not a coverage gap

`sex/mercer_print_tits_t5` and `sex/mercer_print_ass_t5` are non-penetrative handling beats
wearing a `_t5` filename, so `validate_queries.py` demands an `ACT_ANCHORS` member (t4 is
exempt, t5 is not) and no anchor in its 24-word list is true of these beats. Their 6 seeds ship
with a known `no_act_anchor` flag each, by LO's call on 2026-08-14 — adding `fuck` would steer
both shelves to penetration, which both beats' own `Avoid:` clause rejects. The vocabulary used
(`cmnf` / `groping` / `clothed` / `quickie clothes on`) is measured-live at 75 urls on
`colm_backroom_t4`. **Assert the residual is exactly 6 and confined to these two slots** — do
not read the validator's non-zero exit as a new failure.

### Added 2026-08-14 — gaps MEASURED during the 23-slot harvest (not predicted)

Gaps 4-6 above were written before the run, from doctrine. These were found by agents on live grids.
All are AUTHORING decisions for LO, not query bugs — every one had its allowed rounds spent.

7. **The squalid ROOM, across every still slot.** The recurring shape of this run: **subject strong,
   setting weak.** The person-doing-an-action lever reliably buys the actor and the right host crowd, but
   the "bare concrete back room under one bulb" register keeps losing to whatever aisle the actor belongs
   to. Specifics: `mercer_print.jpg` — `bare concrete` never bit, shelves are bars and domestic interiors;
   `mercer_room_hub.jpg` — the two chips BRACKET the room (one cleaner-but-emptier, one grimier-but-derelict)
   and neither is it; `mercer_room.jpg` — **"windowless" is not retrievable as a photographic attribute**
   (a window is how a photographer lights an interior, so the corpus barely has windowless rooms).
   **Decision for LO: accept subject-right/room-approximate, or fund a dedicated room pass.**

8. **Props are unretrievable and the reason is structural.** `mercer_room_hub` — no crate-as-table with a
   bottle on it, anywhere. `mercer_print` — the woman's coat over a crate is absent. `kess_extraction` — the
   sealed file and the tiny component do not exist as a staged photograph. **This is not a query failure:
   naming the prop is exactly what flips a still query into the SHOPPING aisle (see the purchasable-noun
   class in `lexicon.md`).** Props have to be carried by the prose or dropped from the beat.

9. **`kess_file_shape` — the two-people-over-paperwork composition is unreached.** The shelf covers the room,
   the low lamp and the dim industrial register, but skews to a LONE man with papers STACKED rather than two
   figures across a bench with papers spread flat. `documents` + `two people talking` is business-stock
   vocabulary and owns that query shape. Reseeded to `two workers reading a chart in a dark factory`; not
   re-run.

10. **`kess_install` — composition bought at the cost of the room.** The winning lever was the REAL-WORLD
    ANALOG (`tattoo artist working on back of woman lying down in dark studio`) — two figures, one prone, one
    working the body with a fine tool under a low lamp. **But the room now reads TATTOO PARLOUR** (brick,
    framed flash art), not a steel industrial bench, and many stocked subjects are SUPINE rather than
    face-down. The true dim-industrial room was in hand at 94 pure-stock urls but only ever had ONE figure.
    Composition or room — the agent chose composition. Reversible if LO prefers the room.

11. **`mercer_hands_on` — the beat sits between two aisles and neither contains it.** The clean-band corpus
    offers "hand on thigh" as a MACRO CROP (no faces, no second figure, no room) or "couple sitting" as a
    LIFESTYLE TWO-SHOT (bright, smiling, both-young or both-old). Four searches never produced a wide
    two-shot of an OLDER man and a YOUNGER woman, seated, dim, hand on her leg. Thinnest shelf of the run
    (100). **Untested lead:** `harassment` is the stock-caption phrase for a non-consensual hand-on-leg
    two-shot and carries both the age gap and the unwilling second figure — see `lexicon.md` for the two
    cautions before running it.

12. **`mercer_undertow` — `underground` never bit.** Both shelves read as a warm ground-level PUB, not a dim
    basement bar. Google has no stock supply for "underground bar with a man in it", and pushing harder pulls
    empty-interior venue shots with NO PERSON, which is the worse failure for this slot. Subject and room
    class are right and the man is in frame; the basement look is the gap.

13. **The AFFECT axes are mutually exclusive on the two hardest sex slots.**
    - `lockup_finish_facial`: **slack affect and a visible standing man sit at opposite ends of the shelf.**
      The slackest bucket (`cum all over her face`, ~10% smiling) is largely POV, so his standing body is out
      of frame; the buckets that show the heavy older man are the MOST performative (~70% tongue-out /
      camera-address). Overall ~15% of the shelf is explicitly smiling-at-camera — the standing human reject.
    - `anal_drain` / `anal_answered`: **no query landed aftermath AND the man in frame together**, across 11
      attempts on two slots. Aftermath vocabulary returns solo drip/gape close-ups; male vocabulary returns
      mid-act. **No query anywhere retrieves the instant of stillness AFTER** — the corpus is mid-act or
      post-withdrawal with nothing between, and the words that would name it (`spent`, `still`, `slumps`,
      `wrecked`) are measured poison. Best proxy is the `fat old man prone bone` inventory, judged on a
      clip's CLOSING frames.

14. **Judge these four pools on the ANIMATION, not the thumbnail.** On the anal-finish slots roughly 35-45%
    of the shelf is AFTERMATH (gape, drip, cum already out) rather than the moment of finishing, and the
    beats' avoid-band (pull-out, external cumshot) runs throughout. **Both are indistinguishable from a target
    clip as a still image.** Same for `print_tits`/`print_ass`, where the avoid-list (penetration, anal, bent
    over, kneeling, spanking) rules out a large share of what landed.
