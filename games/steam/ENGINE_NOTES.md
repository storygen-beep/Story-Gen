# Engine notes — found live while play-testing Steam v0.1

**Status: LIVE-VERIFIED, NOT SOURCE-CITED.** Every fact below was observed in a headless
Chromium session driving `games/steam/output/index.html` on 2026-08-12. None of them carry a
`v2.py` line reference yet, so **they do not meet the bar for `references/engine.md`**, which
requires a `file:line` for every claim. They are parked here deliberately. Promoting any of
them means reading `apps/game_generation/twee_comprehensive/generators/v2.py` first and
attaching the citation — that work is not done.

Each one cost a failed test run, and each one *failed in a way that looked like a bug in the
game rather than a bug in the harness*. That is why they are worth writing down: the failure
mode is a false alarm, not an error message.

The working harness is `games/steam/playtest.py`.

---

## 1. `State` and `Engine` are not bare globals — they hang off `window.SugarCube`

```js
typeof State        // "undefined"
typeof SugarCube    // "object"
SugarCube.State.variables       // the real state
SugarCube.Engine.play('Canvas_<id>_Node_<node>')
SugarCube.setup.<helper>
```

**What it looks like when you get it wrong:** `ReferenceError: State is not defined`, thrown
from inside `page.evaluate`, on a page that is otherwise running perfectly. Easy to misread as
the build being broken.

Our own memory note on play-testing built games says to "set `State.variables`" — that phrasing
is fine at a devtools console, where SugarCube's globals are reachable, but it is wrong from a
Playwright evaluate context in this build. Go through `SugarCube.` there.

---

## 2. `time_state.current_day` is a day NAME string, not an index

```js
SugarCube.State.variables.game_state.time_state
// { current_hour: 7, current_minute: 0, current_day: "Monday", current_week: 1, day: 1 }
```

`current_hour` and `current_minute` are integers. `current_day` is `"Monday"`, `"Tuesday"`, …
The separate `day` field is a numeric day counter, not a weekday.

**What it looks like when you get it wrong:** writing `current_day = 0` (an index, as
`[[npcs.schedules]] weekdays` uses) does not throw. The clock simply stops matching any
weekday, so **every** NPC drops out of **every** location, and the schedule grid reads as
totally broken when it is completely fine. This produced a full page of red FAILs against a
game whose schedules were correct.

To move the clock in a test:

```js
const ts = SugarCube.State.variables.game_state.time_state;
ts.current_day = "Thursday"; ts.current_hour = 19; ts.current_minute = 0;
```

---

## 3. Presence: use `setup.getNpcsPresentAtLocation(slug)`

```js
SugarCube.setup.getNpcsPresentAtLocation('the_scrub_room')   // → NPCs there now
SugarCube.setup.getNpcLocation('npc_del')                    // → a location UUID, not a slug
SugarCube.setup._getNpcUuidToSlug()                          // uuid → slug map
SugarCube.setup._getLocUuidToSlug()                          // ditto for locations
```

`getNpcLocation` returning a UUID matches the existing memory note on UUID-vs-slug presence
diagnosis. The practical consequence for a test harness: printing its result gives you
`del@[object Object]` or an empty string, which reads like "nobody is anywhere" — another
false alarm. Resolve through the uuid→slug maps, or ask the location instead of the NPC.

There is **no** `setup.checkConditions` / `evaluateConditions` in this build. The condition
entry points are `triggerConditionsSatisfied`, `checkSingleCondition`, and — separately, for
quest cards — `checkQuestsCondition`.

---

## 4. `pickQuestsCards` accepts exactly one scope: `"story_goals"`

```js
SugarCube.setup.pickQuestsCards('story_goals')   // → matching top-tier cards
SugarCube.setup.pickQuestsCards('all')           // → []   (and every other string)
SugarCube.setup.pickQuestsCard('npc_del')        // → the single highest-priority npc card
```

From the shipped function itself: `if (scope !== "story_goals") return [];`

**What it looks like when you get it wrong:** `0 cards matched`, which is indistinguishable
from the failure `engine.md` §23 warns about — `quests_engine = "v2"` switched on with no cards
authored, rendering a heading with nothing under it. I reported Steam as having an empty
guidance page on this basis. It did not; the scope string was wrong. Verify against
`setup.quests_cards.length` (the loaded card array) before concluding anything.

---

## 5. Playwright text selectors break on the rendered labels

The age-gate link renders as `✓ I am 18 or older - Enter Game`, and choice text throughout the
game uses curly apostrophes. `page.click('#story a.link-internal:has-text("…")')` times out
after 30s against a link that is demonstrably present in the DOM.

Click by substring from inside the page instead:

```js
const els = [...document.querySelectorAll('#story a.link-internal')];
els.find(e => e.textContent.includes('I am 18 or older')).click();
```

---

## 6. Cascade-beat markup is entity-encoded in the page source

Dialogue inside a `cascade` beat appears in `index.html` as `&lt;strong&gt;Ivo:&lt;/strong&gt;`,
not `<strong>Ivo:</strong>`. A regex over the raw HTML for `<strong>` finds nothing and reports
"NO SPEAKER TAG" for lines that render correctly.

Unescape twice before asserting on rendered markup:

```python
import html
flat = html.unescape(html.unescape(page_source))
```

This is what turned the `gates.py` dialogue-attribution lint from an apparent 11 real defects
into what it is — a false-positive class. An explicit `npcId` on a `dialog` block renders the
right name whether or not the canvas binds that NPC via `requires_npc` / `npc`.

---

## The one that was a real defect, for contrast

Everything above is a harness problem. The dialogue lint did also catch one genuine error:
June had a `dialog` block on `rung_street_hotel`, which is at `spring_street`, where she has no
schedule row — she was speaking in a place the game never puts her. That is now reported speech
in a paragraph. The lint is noisy, but it is not useless; read every hit, then decide.
