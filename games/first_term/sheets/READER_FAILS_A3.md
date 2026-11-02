# Reader fails, pass a3 — signed 2026-11-02 (LO: "Signed, go with your recs, skip the play check")

> **Written 2026-11-02**, after LO's "Go on" (the remaining reader fails, next after the release door). Source: three
> `v2-reader` passes on today's build (2026-11-02), on every test except the truth and clothes tests, which pass a3
> already ran:
> - home: `reader_a3_home.md`
> - college: `reader_a3_college.md`
> - out: `reader_a3_out.md`
>
> The a2 list is stale: today's builds closed 13 of its rows. This list holds **68 fails**:
> - 58 still open from a2
> - 10 new
>
> **Kind:**
> - **line:** a line is added or changes
> - **button:** a choice is added or changes
> - **gate:** a condition changes
> - **write:** a new short screen
> - **pay:** a no or a stay that moves something

## Three calls first (they decide many rows)

**A. The hub nos** (home 5–8, out 8, 10, 14).
- *Problem:* a hub's "Leave him to it." or "Goodnight, Mr. Vance." moves nothing.
  The signed parked nos (DECISIONS 127) don't cover hubs.
- *My pick:* each no gets a small cost on him (his Want +1, "he wanted it more") and one line from him. No new counters.
- *The other way:* count hub nos as parked, and these 7 rows close with no change.

**B. Counters the readers proposed** (out 8, 12, 13, 26: "a counter of times she walked past", a talk counter).
- *My pick:* none. A no moves his Want +1, as in A. A talk screen gets a second pool line, not a new counter.
- *Reason:* new state that nothing else reads is the "made-up stat" the truth rule warns about.

**C. Screens that need new writing:**
- home 3: front step, the E60 "Let the street see."
- home 14: Laura's "Ask what she saw in your room." placeholder
- home 10: garden, "Let Mark look."
- home 15: couch, "Stay a while."
- out 25: park run, "Walk it instead."

*My pick:* write home 14 from its signed sheet line, and write a short screen for the other four with `v2-prose`, measured.
*The other way:* hide each button until a later release writes it.

## Home (16)

| # | canvas | fail (test) | fix | kind |
|---|---|---|---|---|
| 1 | `hub_mark_living_room` | Channel 5 opens the explicit beat with no earlier sign that Mark wants it (want) | gate "Channel 5" on `mark_saw_her`, like "Leave it on." | gate |
| 2 | `laura_04_she_saw_you` | she whispers "Ryan."; nothing she must have seen shows her wanting Ryan (want) | `laura_alone_in_bed` (which laura_04 requires) gets one ungated line: Laura listening toward Ryan's wall | line |
| 3 | `front_step` | one button, "Go back in."; the E60 showing choice was never built (hook) | build "Let the street see." (E60, 07:00–21:00): a passer-by's reaction and a price | write · C |
| 4 | `hub_laura_kitchen` | "Come upstairs after." can only be ignored (no) | "Not tonight, Mom." costs her Warmth −1 | button |
| 5–6 | `hub_mark_kitchen`, `hub_mark_living_room` | "Come here." (towel, Power 60): only "Leave him to it." (no) | "Get dressed." His Want +1; Mark: "Suit yourself." | button · A |
| 7–8 | `hub_ryan_room`, `hub_ryan_living_room` | "One pull." (Want 70): only "Leave him to it." (no) | "Hold the knot. \"Not tonight.\"" His Want +1; Ryan: "Tease." | button · A |
| 9 | `front_step` | the E60 panties line can show at night next to "nobody stops", and nobody reacts (low heat) | E60 lines only 07:00–21:00, plus a watcher and a not-yet (rides on 3) | gate + line |
| 10 | `garden_sun` | "Let Mark look." has no stage gate and leads to no screen; "Play up to…" lands on one line (low heat) | "Let Mark look." needs Curious or Daring and gets a short screen with his reaction; "Play up to…" shows only when bra-only or with lotion | gate + write · C |
| 11 | `home_event_laura_robe` | the robe slips but nothing is named (low heat) | "her robe slips open over her tits" | line |
| 12 | `home_event_mark_reach` | below Corruption 40, no reaction and no not-yet (low heat) | he steps back fast, hips turned away: "Mind yourself, @player." | line |
| 13 | `home_event_ryan_towel` | the bold and curious versions have no not-yet (low heat) | each ends on "Not here. Mom's up." | line |
| 14 | `hub_laura_kitchen` | "Ask what she saw in your room." opens a PLACEHOLDER (low heat) | write it from `npc_laura.md:96` | write · C |
| 15 | `living_couch` | "Stay a while." has no screen (low heat) | a short screen: he answers and holds back ("Not with your mother home.") | write · C |
| 16 | `mark_03_shorts` | below Exhibitionism 20, talk only, no body (low heat) · new | both openings: "His eyes go down your legs under the table." | line |

## College (26)

| # | canvas | fail (test) | fix | kind |
|---|---|---|---|---|
| 17 | `hub_hale_class` | at grade 40+ nothing points ahead (hook) | the 40+ bands add "Thursday, @player. My office." (from his step 2 on; before it, "See me if you're stuck.") | line |
| 18 | `hub_hale_office` | at steps 1 and 3 the only exit is goodbye (hook) | step 1 "Thursday. After six."; step 3 "Same time next week." | line |
| 19 | `hub_ta_class` | only the under-40 line points anywhere (hook) | the 40+ bands add "My door's open afternoons." | line |
| 20 | `hub_zoe_canteen` | Mon–Wed at step 1 or 3+, no forward line (hook) · new | "Friday's coming, babe. Start planning." | line |
| 21 | `hub_zoe_class` | no forward line at step 1 or 3+ (hook) · new | add a forward line to her pool ("Party's Friday. You're coming.") | line |
| 22 | `jake_04_sneak_him_in` | the yes path's last screen points at nothing (hook) · new | Jake mumbles "Next Saturday. Same room." | line |
| 23 | `zoe_park_dare` | neither branch points at a next dare (hook) | Zoe: "Next weekend I'm daring you worse." | line |
| 24 | `college_exam_art` | "No." gets no answer (no) | he: "Your loss." His Want +1 (A) | line + pay |
| 25–26 | `college_class_figure`, `meet_figure` | "let them look" / "Half the easels…" puts a group on an E20 act (low heat) | "…and let him look." · "The guy at the next easel has stopped drawing the model." | line + button |
| 27 | `college_event_desk_guy` | the Look screen names nothing of hers (low heat) | "Your thighs press together under the desk." | line |
| 28 | `college_event_dress_code` | "eyes go to your skirt" (low heat) | "to your bare thighs below the skirt" | line |
| 29 | `hub_hale_office` | the braless branch names nothing (low heat) | "His eyes go to your nipples through your top. He keeps the desk between you." | line |
| 30–34 | `hub_jake_{canteen,class,gym,party,quad}` | Zoe's-dress branch, no not-yet (low heat) | add "Later. When they're not looking." | line |
| 35 | `hub_ta_class` | no act held back (low heat) | "She starts to say 'come by my office', and doesn't." | line |
| 36–41 | `hub_zoe_{apartment,bedroom,canteen,class,party_house,quad}` | the skirt branch is talk only (low heat) | "Her eyes go down your bare legs to the hem and she bites her lip. \"Not here, babe.\"" | line |
| 42 | `hub_cocky_class` | no body; the price is in one pool line only (low heat) · new | "your thighs under your hem"; the fixed line carries his price ("Midterm answers cost a look.") | line |

## Out (26)

| # | canvas | fail (test) | fix | kind |
|---|---|---|---|---|
| 43 | `cafe_coffee` | before Tom, nothing points ahead (hook) · new | "Behind the till, the HIRING sign has a coffee ring on it." | line |
| 44 | `park_run` | no next step (hook) | "Zoe runs here weekends. She'd make you go further." (once `zoe_met`; otherwise "Same time tomorrow.") | line |
| 45 | `party_house_soak` | nothing points forward (hook) | the knee guy: "Same tub next Saturday?" | line |
| 46–48 | `street_seen_{nobra,nopanties,skirt}` | shop and car versions point at nothing (hook) | shop: "He'll be out front tomorrow."; car: "The same car's parked at the corner the next time you look." (car stays one line) | line |
| 49 | `town_event_whistle` | "Not a chance." at every stage (voice) | "Not a chance." under E40; E40+: "Not for a ride." | gate + line |
| 50 | `hub_cocky_party` | "Walk past him." moves nothing (no) | his Want +1; "Your loss." (A) | pay · A |
| 51 | `hub_tom_cafe` | `tight` has only "Take it." (no) | "Leave it on the counter." Tom: "Your call." No pay (it's the uniform, not him) | button |
| 52 | `hub_vance_porch` | "Goodnight, Mr. Vance." moves nothing (no) | at Want 30+, his Want +1 (A) | pay · A |
| 53 | `park_hidden` | `park_cool_zoe` is set and never read (no) | replace it with Zoe's Want −1, as `party_cool_zoe` reads | pay |
| 54 | `party_house_soak` | the knee is refused in narration only (no) | "Move it away." / "Leave it." (Leave it: both meters +1, cap 59; Move it: his line only) | button |
| 55 | `street_seen_nopanties` | two offers refused in narration (no) | leave as narration: the street is a one-screen witness, so a button per offer is a new branch. Mark this row "accepted, B" | none · B |
| 56 | `town_event_whistle` | "Walk faster." sets only the daily flag (no) | leave it: a random daily street event, and walking off is its no. Mark this row "accepted, B" | none · B |
| 57 | `cafe_shift` | the lunch screen names nothing of hers (low heat) | "...stops, eyes on your ass." | line |
| 58 | `hub_cocky_party` | Sat 00–02, no not-yet (low heat) | a gate-off line: "Not here. Find me later." | line |
| 59 | `hub_tom_cafe` | the tight version names nothing (low heat) · new | "He looks once, at your tits in it, and makes himself look at the till." | line |
| 60 | `hub_vance_porch` | under Want 30, no body; 30–59, no not-yet (low heat) | under 30: "His eyes go to your legs and come back up slow."; 30–59 adds "One evening you'll sit with me." | line |
| 61 | `park_selfie` | a photo pays from Exhibitionism 0 (low heat) | "Post it." needs E20; below that, "Delete it." only | gate |
| 62 | `park_walk` | "You let it be a problem." on the skirt alone (low heat) | below E40 she grabs the hem; "You let it be a problem." behind E40 | gate + line |
| 63 | `party_house_soak` | the kissing-friends draw has no reaction to her (low heat) | cut it from the pool | line |
| 64 | `town_event_jogger` | names nothing (low heat) | "looks back at your ass, twice" | line |
| 65 | `town_event_vance` | names nothing (low heat) | "lowers it to look at your legs" | line |
| 66 | `vance_meeting` | no not-yet (low heat) | "We'll talk properly some evening." | line |
| 67 | `park_run` | "Walk it instead." takes back a run already shown (solo) | move the run text behind the run buttons; "Walk it instead." gets a short walk screen | write · C |
| 68 | `hub_cocky_party` | "Talk with him a while." is the same every visit (next step) | a second and third pool line (B, no counter) | line |

## Seen by the readers, outside the tests, fixed with the rest
- `zoe_02`: "Give it back." shows before Zoe has the bra. The button becomes "Ask for it back."
- `hub_cocky_class`: "Talk a while." shows no talk. It becomes a pool line he says.
- `hale_thursdays`: the description says "(Curious, Daring)", but the trigger needs Corruption 40 and Exhibitionism 40. Description fixed.
- `cafe_shift` `l3_let`: the strangers' grope plays to a whole table at Corruption 40. The heat ladder puts an audience at stage 4. Not changed here: these are explicit beats, a stage call for LO.

## After the sign
1. Sheets first.
2. The five C screens by `v2-prose`, measured with `gates.py --beat`.
3. Build, then gates against 62/89.
4. A `v2-reader` pass on the touched canvases.
5. A probe for the gated rows (1, 10, 49, 61, 62) and the new buttons.
