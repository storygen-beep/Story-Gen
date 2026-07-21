# Vesper — Locked Design: THE ARCHIVE (Beat 1a + 1b)

> **What this doc is.** The locked design record for the chapter *after* SALVAGE — the chunk that opens on
> the current shipped end-state (leashed, paid-clean, Mercer wary, back in the sandbox). It is built **fresh**
> from what 0.1.4 left live; the older pre-written roadmap (the Calloway/Site/Cain mission ladder as designed
> in `design_book.md`) is **set aside** — this supersedes it for the forward story.
>
> **Status:** ✅ **DESIGN LOCKED with LO 2026-07-20** (flow confirmed beat-by-beat). NOT built. NOT folded
> into `design_book.md` / `authoring_state.json` yet (that happens at build time, on LO's okay). Standalone.
>
> **Scope split (locked):** two shippable chapters.
> - **1a — The Archive (topside / Calloway):** infiltrate, bug, seduce+drain, discover the big theft, get burned. **Build first.**
> - **1b — The Deal (underworld / Bastien):** find the deal, the collision, read the build file, the Mercer trade, the Chairman's shadow.

---

## 0. The spine in one breath

She's sent to rob a company hunter's archive → she bugs his files and his own hidden traitor steals them →
the trail runs into the underworld and toward her old kidnapper (the buyer) → she snatches the thief and the
files at a deal → the files tell her what she is and what her owner's really doing → her boss's own hunter
unknowingly hands him to the top boss → and she trades her fleeing owner his escape for the key to her own
chains, just as the real enemy arrives.

---

## 1. Where this sits

- **On-ramp (shipped, 0.1.4):** Wren is operational again but **leashed** — a control chip Kess found, by
  design, that blocks her from turning her power (drain/emitter) on the man who owns her (Mercer). Core is
  **sealed but still "Failing"**; no cure shipped. Mercer is **wary** (she went dark, someone off-books touched
  his asset) and has dispatched her next target ("Calloway — Vance Securities, runs the hunt for the rogue,
  keeps a file room nobody audits"). The underworld (Kess, the House, the Pit) is her off-books world.
- **Her standing want (from Salvage):** find the controller, cut the chip, become able to turn on her owner —
  the *used → user* turn. This arc **advances** it (she gets the controller) but does **not** resolve it (she
  can't cut yet).
- **The larger arc this opens toward (context, not built here):** the Chairman (Aldous Vance) closing in;
  Bastien's reckoning; Cain, still a reserved shape.

---

## 2. Cast

| Character | Role in this arc | Status |
|---|---|---|
| **Wren** | Protagonist. Owned synthetic, leashed, becoming a handler. | BUILT (player) |
| **Mercer** | Her owner/handler. Secretly disloyal to the Chairman — sends her on this job as *his* private leverage play, not the company's. Ends blown, fled into the underworld (her stash). Does **not** know he's the one who exposed himself. | BUILT (`npc_mercer`) |
| **Calloway** | The mark. Obsessed, humiliated, sidelined company rogue-hunter; keeps a huge **un-indexed** archive; being audited/shut down. She infiltrates his team, proposes the bug, seduces + drains him. Ends her **nemesis** — realizes he was played and reports her up (the fuse that reaches the Chairman). | **NEW** — build `npc_calloway`. First name OPEN. |
| **Vane** | The thief/rogue. Mercenary spy, money-only, no cause; **secretly one of Calloway's own team (the mole)** — hidden in plain sight. Two thefts (small → bug; big → spooked by Wren's closeness). Caught at the deal, **kept alive as her asset**. | **NEW** — build. Name OPEN (placeholder: Vane). |
| **Bastien** | The **buyer** (unknown to Wren until the deal — she works on instinct). Her old kidnapper. **Flees** at the sight of her (his reckoning is deferred). Operates through the Undertow. His Cain-alliance stays reserved. | BUILT (`npc_bastien`); this arc **activates** the arc his kidnap-capstone reserved. |
| **Kess** | Her underworld fixer — found the leash, the only hand that can safely cut it later. Background here. | BUILT (`npc_kess`) |
| **Aldous Vance (the Chairman)** | The top boss. Offstage. Named and signaled **inbound** at the close. Zero retcon — the company is already named for him. | OFFSTAGE — not built as an NPC. |
| **Cain** | RESERVED shape. Off-page, never a speaker/portrait/`npc` object. The docs → Bastien → (reserved: Cain). Never appears. | RESERVED |

Calloway's team is **lean** — Calloway + Vane (the hidden mole) + one or two texture faces (no arcs).

---

## 3. Locations

- **REUSE (built):** `the_waterfront`, `spire_plaza`/foot of Vance Tower, `penthouse` (Mercer's hub);
  the underworld strip + `underworld_bar` (**The Undertow** — Bastien's front, seeded "unseen owner"); Kess's berth.
- **BUILD (new):**
  - **Vance Securities / Calloway's archive** (topside) — where 1a lives (his office + the file room).
  - **The underworld drop** the bug traces to (a waystation — new or a light existing spot).
  - **The deal site** (underworld) — the 1b collision. Can reuse/extend an existing underworld node.
  - **The controller room** (topside, Mercer's world) — the rack of asset controllers (ties to the shipped
    named units Vega/Lyra/Nova; she is *one of many* leashed things).

---

## 4. BEAT 1a — THE ARCHIVE (topside)

The infiltration-and-investigation chapter. **Build first.** Confirmed flow:

1. **Mercer sends her** to rob Calloway's archive → plants her as a **junior analyst** (her cover). To Wren
   it's a plain company errand; she does **not** know his real motive.
2. **Calloway** — the humiliated hunter, un-indexed archive being shut down; his team includes **Vane, secretly
   the thief**. He's guarded (reads her as one more minder sent to watch the crank fail).
3. **She proposes bugging the sensitive docs** with location trackers — a method to catch his ghost. A starving,
   disbelieved hunter jumps at it (first person to take his hunt seriously + bring a real idea) and **approves
   it.** *That's her way in* — it wins his trust/access.
4. **Theft #1 (small):** Vane, a normal thief, steals a first small batch → **the bug moves.** She traces it to
   an **underworld drop** → the thief finds and **destroys** the bug there. So she learns the docs go **into the
   underworld — but NOT who buys them.** (The bug never reveals the buyer.)
5. **Instinct:** she suspects the buyer might be **Bastien** (her old kidnapper, who trades in company secrets)
   → on that hunch she **starts spying on Bastien**, in parallel.
6. **She gets close to Calloway** — the seduction, the **incremental menu** (escalating intimacy). This is the
   chapter's adult content and the access that keeps him unsuspecting. Register = the **belief-lever** (his
   surrender is *finally being believed / allowed to stop being the hunter*), not a literal domme act.
7. **Theft #2 (the big chunk):** **Vane sees Wren moving in close on Calloway → gets spooked → and *this* time
   does the BIG theft** — the big chunk holding **Mercer's target bundle + her own build file.** (Not right after
   theft #1 — later, triggered by her closeness. A few days before the drain.)
8. The seduction peaks → **she drains Calloway:** *"where are the docs?"* → she looks → **nothing there.** →
   **she drains him again** → Calloway: *"a big chunk was just stolen — your target's probably in it."*
   (The drain needs the intimacy to fire and yields only what's in his head. The archive is un-indexed, so only
   he — not any catalog — can point her at the material.)
9. **After the second drain**, through her **spying on Bastien** (overhearing him), she pins down the **next
   deal place** — where the stolen chunk will be sold. (The deal location comes from the Bastien-spying, **not**
   the bug.)
10. → she heads for the deal. **Handoff to 1b.**

**Calloway's arc across 1a:** guarded → **believer** (she brings the method that finally works) → **attached**
(the seduction; a lonely, disbelieved man given the two things he's starving for) → **betrayed.** With no
memory-gap track, his betrayal-turn is **circumstantial**: she gave him the one trap that worked, the trail ran
into the underworld where *only she* could follow, and she vanished after it. He does the math — *she used my own
trap to find the docs for someone else and walked off with my ghost's trail* — becomes her **nemesis**, and
**reports the "analyst" up the chain.** That report is the fuse for 1b.

**What 1a delivers:** a full infiltration + seduction chapter (the Calloway sex content), a clever bug-trap plot,
and a cliffhanger — the trail leads down, and she's made a dangerous enemy about to sell her out.

---

## 5. BEAT 1b — THE DEAL (underworld)

The payoff chapter. Confirmed flow:

1. **She goes to the deal place** she pinned down from spying on Bastien.
2. **The deal:** the seller turns out to be **Vane — Calloway's own mole** (the reveal). The buyer turns out to
   be **Bastien** — her instinct confirmed, her old kidnapper, live in front of her. *(The buyer is only
   confirmed here, at the deal — never before.)*
3. **Bastien sees Wren → panics → bolts**, killing the deal (he knows what she is — his escaped, repaired
   captive). He runs, he doesn't fight. **His reckoning stays for later.**
4. With Bastien gone and Vane exposed, **she catches Vane and grabs the big chunk** (her target + her build
   file). She **keeps Vane alive** — an asset and her thread toward the buyer.
5. **She reads the docs:** her **build file** (*what she is* — dread-first, rationed) and **Mercer's real
   motive** (he's been using her to get **leverage against the Chairman**).
6. **Meanwhile, Calloway's report has reached the Chairman** → traced back to **Mercer** (he placed her cover)
   → the **Chairman (Aldous Vance) confronts Mercer** → Mercer's **panicking, running.** *(No chip/transmitter —
   the cover-trail is the mechanism.)*
7. **She reaches Mercer** — already blown and fleeing → **the trade:** she offers him **safe passage into the
   underworld** (out of the Chairman's reach) for **the key to her leash** (the controller). Cornered, out of
   time, she's his only exit → he **pays**, and takes her to the **controller room** to hand her hers.
8. **She can't cut the chip yet** — it would risk her still-**Failing core** (and needs Kess, the hand, later).
   So she keeps the **key** but stays **leashed.** *(The controller is a key that makes the cut safe/fast, not a
   cutter.)*
9. **1b ends:** she holds her own key but is **still leashed**, her owner has **fled into her world**, her
   **crew is growing** (Kess + Mercer + Vane — she's becoming a handler), **Calloway is now hunting her**, and
   **Aldous Vance is inbound.**

---

## 6. Locked rules

**The chip / the leash**
- The chip is **just the leash** — one function. It blocks her power (drain/emitter) on her **owner (Mercer)**.
  It does **NOT** block lies, negotiation, or trade. (No transmitter, no live-mic, no range mechanic — that idea
  is **dropped**.)
- **Cutting it** = she can finally turn her power on her owner. She **cannot cut in this arc** — it would risk
  her still-**Failing core**, and the cut needs **Kess** (the hand). She leaves with the **controller** (a key
  that makes a later cut safe/fast), not with the chip out.

**How the Chairman comes for Mercer (the fuse)**
- **Calloway's report is the mechanism**, not the chip. Calloway realizes he was played → reports the
  "analyst" who tricked him → the **cover Mercer issued** is the trail → the Chairman traces it to **Mercer**,
  IDs Wren as his asset, and moves on him. Mercer's own scheme hangs him; Wren is the fuse via tradecraft.

**The archive / the bug / the drain**
- Calloway's archive is **un-indexed** — the only map of it is in his head. That's why the **drain** matters
  (knowledge, not keys) and why the **bug** (a physical tracker) is how you trace the goods.
- **The bug** is *her way in* (she proposes it → Calloway approves). It catches **theft #1** (small), traces to
  an **underworld drop**, then is **destroyed**. It **never reveals the buyer.**
- **Two thefts:** #1 small (caught by the bug → the drop); #2 the **big chunk** (target + build file), triggered
  by **Vane seeing Wren get close to Calloway**, a few days before the drain.
- The **drain** needs intimacy (sex) to fire and yields only what's in his head. In 1a it confirms the big chunk
  is gone and her target's in it.
- The **buyer (Bastien) is UNKNOWN until the deal.** Wren works on **instinct** and **spies on Bastien**; the
  **deal location** comes from that spying, not the bug. Bastien is only **confirmed** at the deal.

**Content / register**
- **No danger track.** The memory-gap suspicion mechanic is **cut**; Calloway's betrayal-turn is circumstantial.
- The Calloway seduction reads as the **belief-lever** (surrender = being believed / allowed to stop hunting),
  not a literal domme performance.
- Register: **RTS-flat, third person**, crude and specific. The **build-file discovery** and the **Mercer
  trade** may spend **Tier-3** (earned, once-only). The build file reveals *what she is* **dread-first and
  rationed** — not a full origin dump.

**Reserved / canon discipline**
- **Cain** stays a reserved shape — off-page, never a speaker/portrait/`npc` object. The Bastien → Cain link
  stays **unspoken** this arc.
- **The Chairman = Aldous Vance** — offstage this arc; named and signaled inbound only at the close. Zero
  retcon (company already named for him).
- **Bastien** flees rather than fights — his full reckoning is **deferred** to a later chunk.

**The stash ("team that scales")**
- She keeps **Vane** (caught, alive, an asset) and ends with **Mercer** fled into her world → crew = **Kess +
  Mercer + Vane.** She is becoming a **handler** (used → user). **Plant-only** this arc — NPCs with uses she can
  call on, not a party-combat system.

**Engineering / save-safety**
- **Extend-only.** Do NOT retro-break Mercer's shipped `salvage_relaunch` dispatch — layer new state on top
  (gate on a new beat flag / `salvage_relaunched is_true`).
- The controller **rack** reuses the shipped named units (Vega/Lyra/Nova), not new invention.
- Every new conditions block `version = "1.0"`; gate flag-chains on **hidden traits**, not triggerless flags
  (located-setter rule); reset the shared sex-loop traits on entry/exit of each new sex scene.

---

## 7. Build footprint (the honest cost)

**REUSE (built):** `npc_mercer`, `npc_bastien`, `npc_kess`; `the_waterfront`, `spire_plaza`, `penthouse`, the
Undertow + underworld strip, Kess's berth; the shipped Vega/Lyra/Nova unit names; the shipped `salvage_relaunch`
dispatch (extend, don't touch).

**BUILD (new):**
- `npc_calloway` (the mark + seduction/drain scenes) and `npc_vane` (the mole; the deal reveal; the asset).
- **Locations:** Vance Securities / the archive + file room (1a); the underworld drop the bug hits; the deal
  site (1b, can extend an existing node); the controller room (1b).
- **1a clusters:** the cover/onboarding; the bug proposal + plant; the two-theft/bug trace; the Bastien-spying
  thread; the seduction (incremental menu, count-locked distinct scenes) + the two drains; the discovery
  ("big chunk stolen"); the 1a-ending betrayal seed.
- **1b clusters:** the deal/collision (Vane reveal, Bastien flees, catch Vane, grab the chunk); the build-file
  read (Tier-3); the Mercer-blown state + the trade (Tier-3) + the controller room.
- **New state:** a beat flag, the bug/theft progress, the seduction-ladder progress, `controller_acquired`,
  the stash roster (Vane kept), and the Calloway-report → Mercer-blown gate.

**NET:** two new NPCs, ~three-to-four new locations, and the 1a/1b canvas clusters — the biggest chunk since
captivity, but no engine work, no retcon, no save-break. Sensible to ship **1a first**, **1b second.**

---

## 8. Still open (deferred — do not block the build)

- **The build file's exact contents** — how much of *what she is* the dread-first reveal spends now vs. holds
  for later beats (boundary is locked: partial, rationed; the wording is prose-stage).
- **Vane's name** (placeholder), **Calloway's first name**, and finer team-texture faces.
- The exact **count/shape of the seduction+drain scenes** (two drains are load-bearing: "where?" → nothing →
  "big chunk stolen"; the seduction rungs around them are blueprint-stage).
- Whether the **underworld drop** and **deal site** are new locations or extensions of existing ones.
- All build-layer specifics (flags, canvases, media, the Bastien-spying mechanic's exact scenes).

---

## 9. Canon anchors (shipped bytes this builds on)

- **The leash** — Kess's verdict (`5_scenes.toml` ~5067–5091): governor by design, blocks power on her owner,
  keyed controller needed, core sealed, no cure. This arc keeps all of it and drops the transmitter idea (the
  transmitter never shipped — additive-only, now removed).
- **Mercer's dispatch** — `salvage_relaunch` (`5_scenes.toml:5182–5228`): one-shot auto-fire, sets
  `salvage_relaunched`; the Calloway line (`:5208`) is preserved verbatim. Extend on top.
- **Bastien** — at large, his arc "reserved for a later chunk" (`1_metadata:176`); owns **The Undertow** with a
  seeded "unseen owner" (`1_metadata:543`); already knows Wren is "not quite a girl" and answers to people who'd
  pay for the truth (`5_scenes.toml:2413`); the **Cain-alliance stays OFF, a saved reveal** (`5_scenes.toml:2389`).
- **The Chairman = Aldous Vance** — company named "Vance" throughout; the Chairman never named in shipped bytes.
  Naming him here is zero-retcon.
- **Cain** — named in prose but never an `npc`/speaker/portrait (`5_scenes.toml:3681`); stays a shape.
- **The units** — Vega/Lyra/Nova named in the opening (`2_one_shots`); the controller rack ties to them.

---

*Provenance: designed with LO across a 2026-07-20 conversation; flow confirmed beat-by-beat (1a then 1b).
Build sequence and TOML authoring follow the `author-game` skill (source phases → merge → package → live-test,
one verified piece per turn). Fold into `design_book.md` + `authoring_state.json` at build time, on LO's okay.*
