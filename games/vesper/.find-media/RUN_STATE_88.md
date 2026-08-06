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
