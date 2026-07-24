# Steps 0 + 1 — the creative seed (fantasy + setup)

The pre-ledger opening. Steps 0 and 1 run as **one short creative conversation** before any structure
exists: first lock the *fantasy* (Step 0), then plant the *seed* (Step 1). Both are plain-words creative
choices written into `design_book.md`. **Nothing technical here** — no traits, no flags, no TOML, no
build. The whole job is to give the later steps something good to grow from.

This is where the **ledger is born** (at the end, as a phase tracker). Until it exists the dispatch
starts here by default.

---

## Step 0 — the fantasy (the head of the whole pipeline)
A generic fantasy guarantees a forgettable game no matter how good the machinery. So before anything,
clear two gates. Run them with the user (Mode A — these are the most crucial forks in the whole game).

**(1) Pick the PROTAGONIST POV first — it decides which fantasies even work.**
- **Female PC** → self-corruption / rise-via-seduction / becoming-the-one-in-power (madam, queen). This
  is **cascade-native** — "corrupt yourself before others" is literally the female-PC model. Default here.
- **Male PC** → acquisition / power / harem. A male-PC harem fantasy on a female PC (or vice-versa) is
  *wrong-shaped*, not just weak.

**(2) The fantasy must clear the THREE-PART bar** (not just "is it a fantasy?"):
- **POV-fit** — chosen *for* this protagonist's POV.
- **A sharp specific charge** — a *reversal* (powerless → queen), a *taboo*, or a *transformation* — NOT
  generic acquisition ("have all the women"). The charge is the engine of desire.
- **Carries its own two-act shape** — a strong fantasy *implies its own progression*; you don't staple a
  cascade on afterward.

**(3) Declare the DESIRE SPAN.** State which registers the fantasy covers across its acts — the **genders**
of the core targets and the **flavor of desire** (romantic longing / transactional heat / **conquest** —
wanting to break-and-own a person). A fantasy can span more than one, but it must be **chosen, not
stumbled into** — a player who came for one register shouldn't be ambushed by another.

**The test:** *"would someone pick this over the ten other inherit-the-house games?"* If not, it's not ready.

**Worked contrast:**
- ✗ "Inherit your father's estate and make the women yours." Passes "one sentence," but generic
  acquisition, no sharp charge, no built-in shape → competent-but-forgettable.
- ✓ **(female PC)** "Broke waitress at a sleazy bar a man owns → seduce and corrupt *him* until you take
  the bar from under him → then build it into your own empire, recruiting and corrupting other women into
  your stable until you're the madam the city answers to." POV-fit ✓; sharp charge (power reversal +
  seduction-as-weapon) ✓; built-in two acts (take the man → build the empire) ✓.

*(This bar fires ONCE, on the game's founding fantasy. Every pitch after it — a beat, an arc, an NPC, an
expansion — answers to `references/pitching.md` instead: the five parts + the heat test.)*

**The 8 qualities (carried as a check through EVERY later step, not just here):** sharp fantasy · legible
pull · no grind · reward drip + payoff · desirable characters · paced escalation · the charge · reactive
coherent world. The core: **the genre runs on DESIRE.** Anything downstream that fails one of these is cut
or fixed.

---

## Step 1 — the seed (the bare creative skeleton)
A short interview (one question at a time via AskUserQuestion, 2–4 options + a recommendation; skip
anything the concept already answers — state the default, don't ask). Five plain-words things, nothing
technical:

1. **Premise / setting / player.** Who the player is, where, the central hook. The POV is **inherited from
   Step 0** — don't re-ask it. Include the creative-level call: is the player named / customizable? (the
   *decision*, not the `@`-token wiring — that's authoring).
2. **Cast — names + roles only.** List the characters as *people*: "Sal the bartender, Dee the supplier,
   Marcus a regular." **No arc shape, no voice, no vocab ceiling, no stats** — those are Step 3/4. Casting
   (Step 3) will derive the roles the cascade needs and reshape this list; here it's just names.
3. **World map — the locations.** The places the game happens (the bar, the back room, the apartment, the
   docks). Creative geography only — no `is_container` / lock / schedule decisions (those are authoring).
4. **Which systems exist — yes/no only.** Does the game use **phone** / **clothing** / **rent** /
   **player portrait** (a state-reactive sidebar image)? A pure scope choice ("this game has a phone").
   Not the wiring/TOML homes (those are authoring). Clothing is worth flagging early since the
   **reactive world** (Step 2) — and the player portrait's undress axis — ride it.
5. **Voice — the PERSON the game is written in.** One word, and it is **locked for the life of the game**:
   - **`second` — "You take the stool."** The DEFAULT. It's what Road to Success does, and it's what every
     rule and example in `references/rts-flat-prose.md` is written in. Pick it unless there's a real reason.
   - **`first` — "I take the stool."** A confessional / diary-voiced protagonist.
   - **`third` — "She takes the stool."** A protagonist the player *watches* rather than *inhabits* (the
     still-point / owned-weapon PC — `vesper`). It costs second-person immediacy — and that immediacy is what
     makes the aroused body *the player's own*, so third person **cools the porn** (the player spectates
     someone else's heat, `rts-flat-prose.md` Rule 9). Buy it on purpose, and only for a story-first dark game
     where that cooling is the point.

   > **"Person" is NOT "POV."** In this skill **POV** means the protagonist's **gender** (Step 0 above).
   > This is the *grammar*. They're different questions and both get asked.

   Ask it (Mode A) — it changes every line of prose in the game and **cannot be changed later** without a
   full-corpus rewrite. Record it as `register.person` in the ledger, and set `narration_person` in the
   game's TOML `[settings]` so the engine labels player dialogue to match (a `third`-person game with the
   default setting renders "**You:**" over prose that says "she" — that shipped once already).

There is **no scope question** — every game is the full game (slice was removed).

---

## Born here: the ledger (phase tracker)
At the end of this conversation, create `games/<slug>/authoring_state.json` from `references/ledger-schema.md`
with **`pipeline_phase` set** and **`register.person` set** (the two fields the seed is responsible for; the
phase advances as the pipeline proceeds, the person never changes). `structure_registry` / `plan` stay
**empty** — there's no structure yet. The ledger is bookkeeping JSON: it compiles nothing, can't fail a
build, and lets the skill resume at the right step. (The dispatch reads `pipeline_phase`, not "does the file
exist.")

## Output (only the seed sections of `design_book.md`)
- **World setup** — the fantasy (POV · the 3-part-bar fantasy line · the desire span), **the register
  (person)**, premise, player, the systems-in-use yes/no.
- **Cast** — names + roles.
- **Locations** — the map.

It does **NOT** write: the per-subject story design (Step 4), the blueprint (Step 5), the story/economy spine
(Step 2), the feedback review (Step 6), or any TOML / ledger structure / green build (Step 7).

## Why setup is creative-only
Plumbing decided early goes stale — you don't know which flag/trait a scene needs until you write that
scene. Choosing them now means guessing wrong and carrying the wrong schema forward. Keep the user in the
creative seat; the engine translation happens later, by the agent.

## Self-check
- POV picked **before** the fantasy; the fantasy clears the **3-part bar** (not just "one sentence").
- The desire span is **declared** (genders + flavors across acts), not stumbled into.
- The seed has all five: premise/player · cast (names+roles only) · map · systems yes/no · **person**.
- The **person** is declared (`second` unless argued otherwise) and understood to be immutable — and it is
  NOT the same question as POV (gender).
- **No** arc shapes / stats / TOML / green build authored here.
- The ledger exists with `pipeline_phase` + `register.person`; `design_book.md` has the seed sections.
- Hand off: *"Seed locked — moving to top-level design (the engine + economy + desire ladder)."* → Step 2.

## Cross-references
- `references/run-mode.md` (Mode A/B, the interaction discipline) · `references/ledger-schema.md` (the
  ledger born here) · Step 2 = `references/step-2-toplevel.md`.
