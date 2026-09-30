# The idea — Billable Hours: her moment

> One page, written after the Want and before the world. Doctrine: `references/the-want.md` §0 and §6.
> §1–3 signed by LO 2026-09-30. §4: LO picked Pitch M (Martin) 2026-09-30.

---

## 1. The fantasy — what the player comes here to feel

**The premise LO picked:** premise L, a mix:

- [ ] Fall by need
- [x] **Rise by want**: she wants to be kept on, then the contract, then more. *(the goal, a rival, something that repeats)*
- [x] **Taboo at home**: the house, and who is in the next room.
- [ ] Mystery

**In one sentence, what does the player come here to feel?** The same three people run her house
and her job, and every step she takes at the firm is a risk at home, and the other way round.

**The model to beat:** Cupid's Way. **What ours does better:** Cupid's Way keeps the step-family at
home and the world in the city (*"You lived together with your parents and step-brother, meanwhile
your sister lived down in the city"*, `cupids-way.txt:7133`). Ours puts the step-father, the
step-brother and her mother in the same building as her job, so the two halves of the game share
their people.

**Which moments does this game promise?**

- [x] her firsts: the first time at the firm, the first "briefing", the first night with the door
  unlocked.
- [x] being seen: Ethan across the landing, the associates, the Velvet Room crowd.
- [x] her body as the price for something she needs: Theo's account, Callahan's review.
- [x] taboo at home: Martin, Ethan, and Diane asleep upstairs.
- [x] a consequence she has to live with: Pierce's file, and what Diane hears.

## 2. The promise — what keeps pulling the player forward

- **The goal:** be kept on at the week-12 review. **When it ends, the next goal:** the full-time
  contract, which Martin has to co-sign. **After that:** Ethan's desk, meaning she outranks the
  step-brother who said she didn't earn it.
- **The mystery:** none declared. The pull is the goal chain.
- **The rival:** Ethan (`npc_ethan`). He wants her gone from the firm. He lives across the landing.

The hold (the Friday payment) goes flat at $350 and stops pushing; the goal chain doesn't.

## 3. The people who carry it

**The companion:** Jade (`npc_jade`), one step ahead. She left the firm and dances at the Velvet Room.
Not the rival.

**The pressure-man:** Martin (`npc_martin`). Every Friday in his study. **The price of her no:** the
payment is due in cash that week, and he says so to Diane at dinner. **Her way out:** Theo's money
pays Martin in full, for a week.

**Her face:** one performer, kept across the game. **LO picks.** No media harvest runs from here.

## 4. The first step with one person — not the game's opening

**LO picked M — Martin, 2026-09-30.** E and T are kept below as later steps for SP2.

**Step 1 with Martin — the first Friday. Eight lines:**

1. **The fantasy:** taboo at home. Her mother is down the hall, the study door is shut, and the man
   she owes is the man who got her the job. He has never touched her, and tonight she decides how
   close she sits.
2. **The temptation, and his want before it:** every morning from day 1 he passes her at breakfast
   with "Friday, Emma." and his eyes stay a beat too long (the leak). On the first payday Friday he took
   the $250 at breakfast. After dinner he calls her into the study and asks for her pay stub ("I want to see what
   Callahan thinks you're worth"), pats the arm of his chair and says "Sit." He moves first.
3. **Her answers, and his no:** stay standing by the desk (parked: "Next Friday, then.") · sit on
   the arm, hands in her lap · lean into his shoulder while he reads · don't move when his hand
   settles on her knee · leave the envelope on the desk and go (ends his path; the payment stays a
   plain transaction).
4. **Her voice at her level:** low, "It's all there. You can count it." High, "Read it slowly. I'm
   in no hurry."
5. **Who notices:** Diane knocks with his coffee, finds her on the arm of his chair and smiles:
   "Look at you two. I knew you'd come round to him." From then on she takes her coffee upstairs on
   Fridays, so Friday evenings in the house are unwatched.
6. **What sticks, and he remembers:** `martin_friday_sat` (1–3) or `martin_friday_parked`;
   `diane_blessed_fridays`; Martin's want rises (amount set on the board). Next Friday: "Your
   chair's free." At level 3 he adds "You didn't move your knee."
7. **The moment to remember:** taboo at home. His line when the door closes behind Diane: "Your
   mother thinks this is sweet."
8. **The door it opens, and the clip:** the goal chain. He reads the stub like a review: "Callahan
   will ask me about you. What should I tell him?", which is the contract he will have to co-sign.
   Clip intent: an older man in a leather armchair in a lamp-lit study, a young woman in an office
   blouse and skirt on the chair arm, his hand on her knee, her eyes on the door. A tease, not
   explicit. No harvest runs from here.

*Line 2 amended 2026-09-30 (LO, at SP4): the engine's rent page takes the money at breakfast
(`engine.md` §26), so the study scene is about the stub, not the envelope. Findings F4.*

**Leads to:** step 2, the second Friday. Diane has gone upstairs, nobody knocks, and his hand is on
her knee before she answers. It ends on "Same time next Friday. Bring the stub. Leave the jacket
downstairs." Guidance card: "Friday after dinner: Martin's study. Bring $250, and the stub."

### Later steps (not picked)

### Pitch E — Ethan · being_seen · `house`
Step 1. Leak on the landing hub: "His door is open an inch. It's only ever open when yours is."
Her first memo comes home in Ethan's red ink, with a note that reads the start flag. The bathroom
door never latches. Answers: wedge it shut (parked) · an inch open, back turned · open, turn round
under the water · "You can stop pretending you came out for water." · ask Martin to fix the lock
(ends his path). He may be the one who walks off. Martin notices at breakfast. Sets
`ethan_saw_bathroom` / `ethan_saw_front`, Ethan counter 0→1. Next: the firm copier after hours.
Serves Want §4 Early: "she knows Ethan can see through the bathroom door and she doesn't shut it."
~7 beats, one explicit.

### Pitch T — Theo · body_as_payment · `hotel_bar`
Step 1, the week after Martin's first Friday, $100 left. Leak on the firm hub: "That's about a
minute, Emma. Put it on my bill." Callahan sends her across with signing pages. Theo: "Your firm
bills me six-fifty an hour. This hour I'm paying you. Sit, take the jacket off, and let me look at
you while I drink." Answers: on the clock for the firm (parked) · drink, jacket on, he talks
(no money, information) · jacket off for the hour, $200 · name her own price, $250, "That's what
my Friday costs" (gated on a boldness rung not yet on the board) · send him to Callahan (ends his
path). Martin notices the crisp cash on Friday: "Resourceful." Sets `theo_hour_paid` /
`theo_knows_friday` / `theo_hour_talked`, Theo counter 0→1. Next: "the second hour", Thursday.
Serves IDEA §3: "Theo's money pays Martin in full, for a week." ~9 beats, clothed tease clip.

**How the opening hands over to it:** the opening is her first Monday. It ends at dinner on day 1
with Martin's first "Friday, Emma.", which is the leak. The week plays, and step 1 fires Friday after
dinner in the study.
