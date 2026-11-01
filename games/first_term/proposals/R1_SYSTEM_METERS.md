# [READY] Release 1 system 2 — the two meters, working together

> Signed by LO: LO, 2026-11-01 ("Signed."). Step 4 of the release-1 redesign (DECISIONS 99–102), system 2 of 4.
> Changes the signed `sheets/systems/wardrobe.md` and the meter rules of DECISIONS 78; on LO's sign those
> are rewritten to match and re-signed.

## What's there today (measured 2026-11-01, `toml_phases/5_scenes.toml`)
- **Clothes are already gated by body part.** The street's door (`1_metadata_and_locations.toml:300-307`):
  a short skirt or no bra needs Exhibitionism 20, no panties needs Exhibitionism 40, a towel or the sleep
  shirt never goes out. This matches CoT (underwear 2–3, breasts 4, genitals 5: `heat_study/p2_cot.md:36`).
- **But the two meters almost never touch.** Of 106 effects that raise her meters, **3** raise both; 43 raise
  only Corruption, 60 only Exhibitionism. Of 207 conditions that read them, **27** read both.
- **Wearing it pays nothing.** Going out in the skirt raises no meter. Only the two wardrobe events (+1,
  marked "guess" on the sheet) do.
- LO (2026-10-31): "first to wear something short she need corruption, after that increases her corruption
  and exhibition both, learn how top games work on this matter."

## How CoT does it (`heat_study/p2_cot.md:25-40`)
- Her yes is a gated button, and **one scene offers buttons from different meters**: "Classic and
  effective, you're all for it" (Exhibitionism 4), "Could be exciting..." (Submission 2), "Not gonna happen".
- Being seen is a system: **the act raises the meter it uses**; more witnesses give more; an accident gives
  half; **every attracted witness gains lust for her and remembers it**.

## The design

### 1. Each meter has one job
- **Corruption is what she does:** her nerve, her acts, her yes to a person.
- **Exhibitionism is what she shows:** her clothes, her body, being seen.

### 2. The first time takes nerve (LO's rule)
- **Going out in a level for the first time needs Corruption *or* Exhibitionism at that level.**

  | going out in | needs |
  |---|---|
  | a short skirt, or no bra | Corruption 20 **or** Exhibitionism 20 |
  | no panties | Corruption 40 **or** Exhibitionism 40 |
  | a towel, the sleep shirt, underwear, naked | never, this release (as built) |

- So a girl who's done things (Corruption) can dare to wear it, and a girl who's used to being seen
  (Exhibitionism) wears it easily. Today only the second road exists.
- The door's message names both numbers: "Not in that skirt. Not yet. (Needs Corruption 20 or
  Exhibitionism 20.)" (the DECISIONS 90 rule: name the number).

### 3. Wearing it out raises both
- **The first day out in each level pays Corruption +1 and Exhibitionism +1.** After that, each day out in it
  pays **Exhibitionism +1** (once a day).
- It's paid by a once-a-day street scene: someone sees what she's wearing. Mr. Vance on his porch, a guy at
  the corner shop, a car slowing down. That's the witness (taste columns: who sees). Its line changes by
  what she wears and by her level.
- Caps stay as DECISIONS 78: a meter pays only while she's under her stage cap (19, 39, 59).

### 4. An act raises the meter it uses (both, when it's both)

| the act | pays |
|---|---|
| she shows herself to someone, by choice (a flash, a towel slip, naked for Ryan) | Exhibitionism (+1 everyday, +3 a big first) **and Corruption +1** |
| she does something with someone, unseen (a kiss, a handjob, sex behind a door) | Corruption only |
| she does something with someone, **seen** (Mark's TV in the next room, a party) | **both** |
| she touches herself alone | Corruption only |
| an accident (seen in the towel when she didn't choose it) | **nothing** (DECISIONS 78, stricter than CoT's half) |

### 5. Mixed acts need both meters
- An act that shows **and** is sexual with someone needs **both** stage numbers.
  Example: "Naked in his room" (Ryan, Showing) stays Exhibitionism 40; the handjob under the blanket
  with Mark's TV next door needs Corruption 40 **and** Exhibitionism 20.
- Each person's step sheet names which of its buttons are mixed. The rule goes on every sheet.

### 6. One scene, buttons from both meters
- Where a scene offers a yes, it offers **two kinds of yes plus the no**: a showing yes (by Exhibitionism) and
  a doing yes (by Corruption).
  Example, Zoe's dare: "Flash them." (Daring) · "Kiss him." (Curious) · "Not tonight."
- Both go to the same next screen with a different first line, like CoT. The player builds whichever meter
  is hers.

### 7. Witnesses remember
- When she shows herself by choice to a named man, **his Lust +1** (most scenes already do this, e.g. the
  towel slip). A stranger's look pays nothing to anyone; it's the street scene's line.

## Against the taste columns
- **who sees:** the street scene gives every outfit a witness; rule 7 makes him remember.
- **how she says yes:** rule 6, two kinds of yes on the same screen.
- **what changes after:** both meters move, so her voice and her options change together.

## Engine and build work (for after the sign)
- The street door: each rule gets a second `lt` item for Corruption (block only when **both** are under the
  level). That's AND of two items, so no nested condition is needed (B70).
- The street scene: one repeatable canvas on `street`, once a day (`out_shown_today` in the daily tick), with
  a first-time-per-level flag that pays Corruption +1.
- The meter rule in each person's step sheet (step 5 of the redesign): every button's pays and gate checked
  against rules 4 and 5.
- The two wardrobe events lose "guess": they pay by rule 4.

## Not decided here
- Whether underwear-only goes out at Showing in a later release (stays home-only now).
