# Next beat pitch — The Archive 1b, opening chunk: **"Ground"**

## Where the game actually is (so you can check my read)

- **The Archive 1a is finished and terminal.** Beats 0056–0067 are validated. Wren
  seduced and drained Calloway (the *where*), drained Colm in the Undertow back room
  (the *who* → Vane), saw the vault wall herself, blackmailed Vane, pulled her build-file
  out — and the close fired: the watcher tripped, Vane warned her and ran, Mercer panicked
  and bailed, **she kept the file.** That's the last thing that happens in the shipped build.
- **1b was designed *and* on-ramped — then you shelved it for this release.** The revised
  close (Wren's bargain for the controller), the Kess safehouse handoff (`kess_1b_open`),
  the Reach rest-bed (`activity_kess_cot`), and the dev-jump (`dev_jump_1b_start`) all exist
  as commented-out blocks in commit `08ec2e1` (rev 96). You said "cut that off, this release
  is 1a." So the on-ramp is built and parked, not missing.
- **The map for 1b is already stubbed.** `underworld_gate / _strip / _brothel / _pit /
  _market`, `crew_den`, `bastiens`, `kess_berth`, and the Reach (`loc_reach`,
  `the_waterfront`, `the_anchor`) are all registered locations. The world 1b lives in
  already exists on the map — it's just not wired to content yet.

**My honest read:** the next real *content* is 1b, full stop — 1a has nothing left but a
media pass. But don't open 1b on top of a half-shipped 1a. Two things, in order:

1. **First, the housekeeping you already planned:** `beat_0055` + `beat_0065` (the media
   passes) → clean **0.1.4** ship. Two beats, no new design. This is not a pitch, it's
   closing the loop so 1a lands clean before the next arc pulls focus.
2. **Then this** — the concrete proposal below.

---

## The proposal: 1b opens on **"Ground"** — the flight, the safehouse, and the file opened

**The fantasy of the chunk (one line):** she got out of the Spire holding the one file
that says what she is — and now, gone to ground in the underworld with a panicking master
on a leash she still can't cut, she finally *reads it.*

This is the payload the whole Archive was built to earn. 1a was the heist; **1b opens by
paying off what was stolen.** I want the reveal — *Vance's humanoid program, many subjects,
Wren the one at its center* — to land **early in 1b, as this chunk's button**, not held for
ten more beats. She's holding the file at the end of 1a; making the player carry an unopened
file across a whole arc wastes the strongest card on the table. (This is a real fork — see
**Fork A** — but that's my recommendation.)

### The build order (4 beats, one verified-green increment per turn)

**Beat 1 — The flight (Lane 1, located auto-fire capstone).**
Re-enable the shelved handoff. The close drops her into the Reach; Mercer is already
running scared. She gets him out — and the **controller passes into her keeping as the
lever.** Not "she takes it by force"; she can't cut the leash (Failing core), so she holds
*him* holding it — helping him run is how she gets a hand on it. Engine: an auto-fire
`priority ≥ 9`, `is_repeatable = false` capstone at the underworld gate / Kess's berth, sets
a `flight_done`-type flag, single Continue. This is the seam between 1a's ending and 1b's
sandbox — it exists to re-home the player somewhere with a bed and a Charge source (the whole
reason the on-ramp was built: post-close she was stranded Spire-side with a battery that only
went *down*).

**Beat 2 — Go to ground (Lane 2/3 texture + the rest-bed).**
Kess's berth becomes the base of operations. Re-wire `activity_kess_cot` — the Reach rest-bed
that restores Charge — so the underworld sandbox is *survivable* (fixes the stranded-battery
dead-end). Kess is already cast as the recurring debt-holder (`kess_debt`, untraceable coin);
she reads bodies as hardware and doesn't ask what the file is. A couple of dying-Reach ambients
(room-only random one-shots, set nothing), and the safehouse *feels* like a safehouse. Plain
RTS-flat, ~35–40 words a beat.

**Beat 3 — The file opened (Lane 4 capstone — Tier-3 earned, the one place prose spends).**
Alone in the berth, she opens the build-file. This is a **solo interior** — no NPC in the room,
so it's the earned narrated exception, not a dialogue beat. The horror lands in stages: a Vance
program, *humanoid subjects*, a roster — and then her own designation in it, at the center.
Third person (the game's locked register). This is the gut-punch the whole Archive was for, and
**Mercer never knew** the asset he ran is the very thing he sent her to steal. Sample register
(Tier-3, once-only — this is where the prose is *allowed* to spend):

> The file opens the way old files open — slow, indifferent, built to outlast whoever reads
> them. A program. Not a project: a *program*, running years before she has any memory of
> running. Subjects, plural. A roster of them, each a line, each a life someone decided to
> make. She scrolls because she can't not. Her own designation is not near the top. It is at
> the center — the one they built the others *around.* Mercer sent her to steal a secret. He
> sent her to steal herself.

**Beat 4 — The thread forward (Lane 1 dispatcher).**
Name the next target and open the hub. Vane fled *here*; Bastien — her old captor — owns this
ground. The reckoning is the arc, not this chunk: this beat just points at it and hands the
wheel back. Sets the 1b spine on the Quests page (one Story-Goal directive sentence).

### What this chunk deliberately does NOT do

Bastien's actual reckoning (his flip / drain / the kill-or-love reserved with Cain), Vane as a
kept asset, the crew growing (Kess + Mercer + Vane) — all of that is **1b proper**, the chunks
after this one. "Ground" is the *landing*: get her safe, pay off the file, aim her at Bastien.
Self-contained, shippable, and it earns the thing 1a promised.

---

## The forks where you steer (I'm not building these blind)

**Fork A — where the file-reveal lands.**
- **(my rec) Early — the button of this chunk.** She reads it in the safehouse; the horror is
  the payload of "Ground." Strongest card played when it's hot.
- **Held — after the Bastien reckoning.** She carries it unopened until she's forced Bastien to
  help her decode/verify it. More delayed gratification, but it parks the strongest beat behind
  a lot of grind, and the design docs already flag her "unnamed pull toward it" — which reads
  like *she opens it soon.*

**Fork B — the program's age.** The one number left open in the whole Archive design (§14): how
many years back Vance ran the humanoid program = how long Wren has existed. It's flavor, not
blocking, but the reveal prose quotes it, so I need it before Beat 3. My instinct: a number that
predates her earliest memory by enough to be a violation — she remembers ~2 years; make the
program **older than she is aware of being alive** (e.g. "seven years," when she can only account
for two). Give me a number or say "pick one."

**Fork C — Bastien's texture (names the arc, not this chunk).** He's cast capture-and-flip —
revealed at the captivity kidnap, his flip + drain deferred. When 1b reaches him: does she
**flip him to an asset** (he joins the running crew), **drain him for power** (a warm tap like
Calloway/Colm, but he *knows* what she is), or is the real payoff **reserved for the Cain
kill-or-love end** and Bastien is just the gate to it? Doesn't block "Ground," but your answer
shapes everything after it, so I'd rather hear it now than guess later.

---

## Cost / risk

- **Scope:** ~4 beats + the two housekeeping media beats to ship 0.1.4 first. Most of the
  geography and the on-ramp already exist — this is wiring parked blocks to content, not building
  a new zone from scratch.
- **Save-safety:** 1a was never publicly shipped past 0.1.3 with zero Archive content, and 1b only
  **adds** (new flags, the reveal capstone, the re-enabled on-ramp) — no renamed live ids, no
  rescaled stats, no title change. Clean.
- **The one thing to watch:** re-enabling `activity_kess_cot` and the Charge restore is load-bearing,
  not optional polish — without a bed and a Charge source in the underworld, the 1b sandbox is the
  same stranded-battery dead-end that got the on-ramp built in the first place. Beat 2 is a
  correctness fix wearing a texture beat's clothes.

**Say yes and I'll ship 0.1.4 first, then build "Ground" one green beat at a time — starting
with the flight handoff. Or edit any of A/B/C and I'll re-aim before I touch TOML.**
