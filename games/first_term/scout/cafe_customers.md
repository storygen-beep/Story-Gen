# Scout card — café / waitress customers (system)

> Scouted 2026-10-31 for first_term (LO asked for it; saved verbatim on LO's yes, 2026-10-31). The skill: covered in part by `templates/cards/job.md` (rows "people",
> "pay ladder", "lewd ladder", "reads": CoT River Rat tables, CW waitress). It does not cover escalation that comes from customers
> while the boss stays out of it, the outfit roll, tips scaled by her response, or business and reputation consequences.
> Games used: In Her Own Hands (IHOH), corrupted-city, Course of Temptation (CoT). Counts only: none.
> Model: IHOH, the Diner (manager Alex). Contrast: corrupted-city, Peter's diner (the boss sells her, and the diner's
> fame spreads into the town); CoT, River Rat (the owner holds a line, and the uniform and clientele follow her flirtiness).

All files: IHOH = `round2/passages/in-her-own-hands.txt`; corrupted-city = `corrupted-city.txt` extracted with
`cv0_audit/extract_html.py`; CoT = LEG passages and `round9b/data/world_src/`.

| field | the model (IHOH Diner) | cite |
|---|---|---|
| how it starts | Laptop job ad ("going the extra mile"), then an interview with Alex. "a flat hourly plus tips", "Paydays will be the 14th and 28th". Hired at `$work.wg to 5` (IHOH's $5/h), Alex friendship +5. Uniforms stay at the diner. | in-her-own-hands.txt:1609 [WaitressApply]; :3165, :3176, :3179 [WaitressInterview] |
| steps | 1 Clock in: shift is 6 h if she starts 09:00–15:00, else until 22:00 · 2 Change: 1 in 2 shifts the only clean uniform is a size too small ("My ass was practically hanging out"), exhibitionism +0.5, the line cook snickers · 3 One scene drawn from a 20-slot shuffled deck (`pluck`, refilled when <2 left) · 4 If the grope flag is set, a 2-in-9 grope roll; she picks "Go with it and flirt back" or "Get pissed off" · 5 Tips screen | :63987–63991 [DinerWorkMain]; :64007 [DinerWorkStartMain]; :64037–64048 [DinerWorkStartBase2]; :64062–64069 [DinerWorkSceneSelect]; :4468 [DinerWorkScene1]; :49448, :49453 [Diner_Groping1] |
| the customers, level by level | Random customers, nobody named. Look: tables "whispered as I walked away… sideways glances" (the too-small uniform). Comment: a table of guys, "Are you on the menu tonight?"; she answers "Not tonight, hon" and leans over the check. Her own flirting: she picks a "mark" each shift. Grope, first time: an older man grabs her under the skirt; she pulls his hand off ("Your meal is here, sir."). A coworker then says "Sometimes a little groping goes a long way in terms of tips". After that, groping is a standing roll on every shift. One customer becomes a named man: a married man at a booth with his wife leaves his card under the check ("Devilish Dad", later Mr. Jones). He comes back on a later shift and asks her out. Two side kinds: she hands her number to a sports team in the side room; women on "Ladies night" flirt with her | :11472 [DinerWorkScene8]; :11524–11528 [DinerWorkScene9]; :11389 [DinerWorkScene7]; :11560, :11572, :11581 [DinerWorkScene5]; :11625, :11633 [DinerWorkScene2]; :14302–14357 [DevDadDiner1], [DevDadDiner1A]; :11411 [DinerWorkScene3]; :11443 [DinerWorkScene4] |
| amounts seen | IHOH tips = random(10, worktime×10 + 2×(beauty bonus + fitness bonus)), **×2 if she went with a grope this shift**. A line shows at $150 or more ("my choices seem to have paid off"). Wage = hours × $5, paid on the 14th and 28th. Energy −10 per hour. Each scene adds arousal +5 (+10 for the card scene); flirt +0.1 per scene; going with a grope: flirt +0.5, exhibitionism +0.2; getting pissed off: flirt −0.2, exhibitionism −0.2 | :15420–15430 [DinerWorkEnd]; :6638 [DinerPaycheck]; :49490 [Diner_Groping2]; :49534 [Diner_Groping3] |
| the boss | Alex never sells her and never sets a price. He looks: "Alex, my manager, was keeping a close watch", he hides an erection behind the counter, and she steers clear (Alex attraction +2). He runs "Ladies night" "to bring in more business" over the staff's objection. In one grope opening he "looked over his waitstaff approvingly". He pays her and, if she quits, is "not thrilled" | :11493, :11504 [DinerWorkScene10]; :11443 [DinerWorkScene4]; [Diner_Groping1] (_scene1 = 4); [DinerPaycheck]; [DinerWorkQuit] |
| her no, written | First grope: she pulls the hand away, and the text says she can't make a scene "at the risk of my job". Every later grope gives her a choice, and the no has 3 random texts ("I don't think so . . .", "Excuse me . . . !", "Let's just not . . . ok?") that cost flirt and exhibitionism and give no doubled tip. To the man with the card she can say "End the conversation and get back to work (ends path)" (only if she threw the card away); otherwise the scene runs straight into his request, with no no. "Not tonight, hon" answers the menu comment | :11560 [DinerWorkScene5]; [Diner_Groping3]; :14327–14328 [DevDadDiner1] |
| reads | uniform roll (1 in 2), beauty and fitness bonus (tips), `$work.dnr.grp` (grope roll on), `$GropedNow` (tip ×2), `$xr.dd.m` / `$xr.dd.card` / `$xr.dd.stop` (the named-man route), `$sex.v.v` (gate on the card scene), clock hour, energy, `$tox.dr` > 2 ("I can't show up to work drunk"), a 30-hour cap (on one hiring route) | :4059–4066 [DinerBase]; :64071 [DinerWorkSceneSelect]; :38161 [WaitressApply2B] |
| writes | cash (tips each shift), `$work.hrs` (wage at payday), flirt, exhibitionism, arousal, bisexual +0.5 (Ladies night), `$DickPix` (team scene), Alex attraction, the named man's flags | scenes above; :11421 [DinerWorkScene3] |
| how it pays off | money (tips, doubled when she goes along) · a person: one customer becomes a dom route (date at the bar, calls) · the team number opens texted pictures (`$DickPix`) · no sex on the diner floor in IHOH | [DevDadDate1A]; :11421 |
| how it repeats | every shift, drawn from the shuffled deck, so variants recur only after the deck runs low. The grope roll repeats once the flag is set. The scenes don't get stronger with her stats; only the tips grow | :64062–64069; :15420 |
| business, reputation, footfall | **IHOH keeps no reputation, footfall or customer-memory counter for the diner.** The only business line is Alex's Ladies night | :11443 |

### Contrast 1 — corrupted-city, Peter's diner (the boss drives it; the diner's fame reaches the town)
- **Shape:** a straight line. `$cafeEvent` goes up one step per "Serve Customers" visit, 1 to 18, with no roll and no deck.
  Each shift has Clean, Talk to Suzie (a coworker) and Serve. (`corrupted-city.txt:9026–9040 [CafeHub]`; `:10698 [CustomerEvents]`)
- **Customer levels:**
  - 1: a woman shouts at her over the outfit ("I'm not the one walking around in that outfit"); co-owner Christine throws her out.
  - 2: a customer takes a "creepshot".
  - 3–4: the same older man returns two shifts running. First he gropes her and she says nothing; then his hand goes further and she stops him ("Hey, watch it!"). He leaves, and Suzie films it "for my TikTok".
  - 5: a customer reads a priced menu: "if I tip one hundred dollars, I get to grope your ass… two hundred?" Peter answers "Yes!" for her, then "Make sure to tell your friends about us."
  - (`:10708–10839`)
- **The boss:** after the outfit stage, co-owners Peter and Christine say business is failing. Peter brings a "revealing maid outfit" because "Customers might frequent here more" (`:9093–9107`). At the next step he says "The customers tip more when you let them touch you!" (`:9151`).
- **Her no at the boss step:** "That's too far. I won't do it!" (`:9171`). Peter swears at her, she quits, and she leaves "for the final time" into the brothel route, with "You should find a job before your rent is due" (`:9201–9203`).
- **Consequence counters:**
  - Stage 5 sets public perception `$pp = "Free Use Maid"` (shown in the sidebar), corruption +5, dignity −5 (`:10839`; `:5852 [StoryCaption]`).
  - Stage 6: women grope her too, "share their experience on social media" (`:10849`).
  - From stage 7, out on the street in daytime, a fan stops her: "You're the maid from Peter's diner… **The diner is always packed now**, and we can never get in." He pays $50 to grope her (`:589–618 [CityHub]`, reads `$pp` and `$cafeEvent gte 7`, once: `$fanMet`).
  - Stage 13: Peter: "we've earned enough money these past few weeks to close for at least a day or two" (`:11048`).
- **Pay:** a flat $120 a shift (`:9339`). Customer money goes to Peter: "counting all the money he's receiving from the ludicrous menu prices and the tips" (`:11168`).
- **How it differs:** the boss sets the prices and the customers follow his menu, which is the opposite of IHOH. In return it has what IHOH lacks: the diner gets busier, and her name follows her into the town.

### Contrast 2 — CoT, River Rat (the owner holds a line; the bar changes around her flirtiness)
- **The owner says no:** if she goes topless before the topless uniform exists, the owner stops her: "I know the atmosphere in here has gotten pretty flirty… but... that's not appropriate. I mean, I haven't filed the paperwork for this sort of thing." Her clothes are put back on (`$pc.fix_clothing()`). (`[EventRiverRatServerPostInappropriateTopless]`; gate `cot_20_database_events.js` near :5518)
- **The owner follows the room:** at her flirtiness ≥150, with the top crowd being sports fans or escapists, the owner says "lately we've been leaning more into the 'sexy sports bar' type vibe" and hands out tight uniforms. The next uniforms come at ≥400 and ≥800. One change every 7 days at most, and none once she is bartender. (`[EventRiverRatOwnerChangeUniformSporty]`; `cot_20_database_events.js:5998–6008`)
- **Who comes in:** six crowd types (Elite, Reveler, Punter "tempted by sexiness", Escapist, Sports Fan, Geek), each with a tip multiplier of 0.667–1.1. Bar upgrades, uniforms included, shift each type's attraction; the Sporty uniform gives Punter +1 (`cot_02_riverrat_job.js:8–49`, `:596–604`, `:960–1003`).
- **Customers react to her:** customer events read her clothes and flirtiness, e.g. remove bra (flirt ≥50, bra worn and not visible), underwear events (≥100). (`cot_20_database_events.js:5447–5464`)
- **How it differs:** the owner never sells her to the customers. He pulls her back when she goes past what the bar allows, and he changes the uniform only after her flirtiness has already shifted the mood.

## What players said
- IHOH: *"What all do I get in the matter of Quest, while working in the Diner? Is it just people groping and flirting?"* (mopoga#135188)
- CoT: *"Is there a way to talk to customers, ask names or plan dates with customers while working at the River Rat?"* (mopoga#131818)
- CoT: *"Highly compliant waitress with high lust customers gets you a gangbang"* (mopoga#151398/r1)

## Not found / gaps
- **No IHOH counter** for diner reputation, footfall, or a customer's memory of her; only the one named man has flags.
- **IHOH truth gap in the source:** scenes 5, 8 and 10 describe the too-small uniform, but the scene pick never checks the uniform roll (`:64007` vs `:64060–64104`). On a normal-uniform shift those lines are false.
- **Ella's case** is not in these sources: a boss who never sells her but notices both lost reputation and more customers. IHOH's Alex only watches; corrupted-city's Peter both sells her and banks the rush; CoT's owner draws a line and updates the uniform. None of them complains that the place's name is suffering.
- **Corrupting the boss:** IHOH stops at Alex's attraction +2 and her keeping away; no Alex route was found in the diner passages. Corrupted-city has Peter and Christine at stages 13–16, but they were not traced past the cites above. Not traced.
- **Other pass-list games:**
  - Shady Deals: she owns the nightclub and brothel; she does not serve tables.
  - Wasteland-lewdness: her diner is a place to eat and refill water.
  - In-their-own-hands: the waitress is an NPC who serves them.
  - Curse-of-the-abyss: 1 outfit line.
  - Untangled-mind: 0 waitress hits.
  - Cupid's Way: covered in `job.md` and boss-driven.
  - New-lust, amore, free-cities-origins: no server job found.

Source files: `~/Documents/Great_Games_Study_20260926/round2/passages/in-her-own-hands.txt` (model); corrupted-city extracted to a scratch file by the scout (line numbers above come from that extraction); `~/Documents/Great_Games_Study_20260926/round9b/data/world_src/cot_02_riverrat_job.js` and `cot_20_database_events.js`; `~/Documents/Player_Legibility_Study_20260825/corpus/course-of-temptation/passages/EventRiverRatServerPostInappropriateTopless.txt` and `EventRiverRatOwnerChangeUniformSporty.txt`.

Adults-only note: some source lines in the IHOH grope and card scenes and in corrupted-city's stage 7 use younger-sounding words; this card describes those scenes without them and quotes none of them.
