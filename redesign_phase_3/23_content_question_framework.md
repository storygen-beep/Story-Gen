# The CONTENT-QUESTION FRAMEWORK — the five subjects + the generate/review split

The content layer reorganized from **mechanism** (lanes/tiers/the roster table) to **subject** (the unit a
novelist holds): five subjects of plain-language, experiential questions that work as **both** a design spine
**and** a review checklist. The same artifact runs in two modes across two pipeline steps — **Step 4
generates** against it, **Step 5 reviews** against it.

**Status:** wired into the skill 2026-06-13. Operational artifact = `references/content-framework.md` (the 107
questions). This doc is the *rationale* + the *validation record*. Pre-restructure skill snapshot:
`redesign_phase_3/_skill_snapshot_2026-06-13_pre_content_framework/` (restore = copy `author-game/` back).
Builds on `06`/`07` (casting + arcs), `09` (desire ladder), `11` (reactive world), `13` (economy), `17`
(frontier), `22` (the machine). **Retires `18` as a *step***: the content-roster step is replaced, not refined.

---

## The problem this solves
Step 5 ("content roster") was confusing because it **overlapped Step 4**: its roster re-listed scenes Step 4
had already decided (organized **by lane** = mechanism), while a whole content category — the **player's own
lewd track** (solo acts, flashing, job-lewd, the economy) — had **no home** and got starved (the Last Call
blind spot). Two failures, one root cause: content was organized by *plumbing*, not by the *thing a writer
reasons about*. "Who decides the scenes?" had two muddy answers (Step 4 *and* Step 5), so the user kept hearing
"we're deciding scenes that are already decided."

## The fix: organize by subject; split generate from review
**Five subjects** (each a cluster of experiential questions; full text in `content-framework.md`):
1. **Fantasy & Shape** — the whole game (fantasy, desire ladder, acts, **the opening**, **the systems
   on/off**, **the fail-state declaration**, the frontier). *Owned by Step 2.*
2. **YOU** — the player's own thread: what raises HER, the economy as content, the items, the non-corruption
   ladders, the supply-vs-demand audit. *The blind-spot track, now a mandatory first subject.*
3. **THEM** — each NPC as a person (the 10-section R7 brief) + the web between them.
4. **What Changes When** — the reactivity web: when any state changes, what becomes different (incl. **§4F When
   she loses ground** — the negative axis).
5. **The World** — places, time, the reactive public, the phone, the sidebar.

**Step 4 = GENERATE, Step 5 = REVIEW.** The framework's two modes split across two steps, which dissolves the
overlap: every scene now falls out of exactly one subject, decided once.
- **Step 4 (`step-4-deep-design.md`)** deep-designs each subject **one at a time**, in fixed order
  **PLAYER → NPCs → WORLD → REACTIVITY** = **supply → demand → stage**. The player's feeder track (supply) is
  sized before the NPC floors (demand) that gate on it; the world (stage) is dressed before the reactivity pass
  wires it. Enforced by the ledger `deep_design` block (don't start NPCs until `player == done`; reactivity
  last). The validated per-NPC R7 brief survives verbatim as **Pass 2**.
- **Step 5 (`step-5-feedback.md`)** runs the same questions against the finished game as a checklist — every NO
  is a gap; fix before authoring. The roster table is **deleted** (the subject briefs already hold every
  scene). The two load-bearing old-roster checks survive as framework clusters: the **supply-vs-demand
  balance** (§2E, owned at generate-time, confirmed here) and the **machine/DAG verify** (§4E).

**§1 → Step 2.** Step 2 gained the §8 declarations (the opening / cold start, the systems on/off, the
fail-state) — it already owned the desire ladder and the frontier.

**The navigation** (the user's original "propose the next move with choices" ask) re-attaches in
`run-mode.md` → "Navigation at junctions": Step 4 proposes the next subject/NPC, Step 5 proposes the next gap.

## Validation (against `games/the_inheritance`)
A review pass (Step 5 in miniature) ran the framework against the fully-built inheritance design book. The
**new questions held up** — kept nearly all, **2 refinements** applied to `content-framework.md`:
- **split** §4 "money-repricing" into a **money/leverage** half and a **renown/standing** half (one half's rich
  coverage was masking the other's absence);
- **regroup** the scattered negative-axis questions into one **§4F "When she loses ground"** cluster.

As a **bonus**, the review surfaced **8 real content gaps in the inheritance** (a game review, not a framework
flaw) — flagged for that game's *next* Step-5 run, NOT fixed in this skill-only pass:
- **MAJOR** — the negative axis is decorative: the advertised foreclosure clock + Margaret's scheme are never
  wired to actually bite (no fail-state, no decay; forward is the only direction). Caught by §1C + §4F.
- **NOTABLE** — no real owned-item economy (Margaret's intoxicant is prose baked into the apex capstone, not an
  acquired item — §2C); the phone underdelivers its own §0 promise (§5F); 3 of 4 repeatable loops have no
  in-loop menu (§3G); no sidebar/HUD authored (§5F).
- **MINOR** — no standing-over-others reactivity (§4A); no cross-cast body-state axis (§4D); `margaret_scheming`
  has no per-threshold firings (§4B).

The point the validation proves: a good question with no answer is a **content gap in plain language** — which
is exactly what makes the framework a review surface, not a gate dump.

## Self-check (the restructure is coherent)
- Both modes run off ONE artifact (`content-framework.md`) → design and review can't drift.
- The player track is a **mandatory first subject** → the blind spot cannot recur (an empty §2 is a visible gap).
- Supply→demand→stage is **enforced by the ledger**, not just advised.
- The overlap is gone: §3 = the old Step-4 R7 work; §2/§4/§5 = what Step 5 was reaching for; the roster is
  replaced, not fed.
- Backward-compatible: phases renamed (`npc_arcs`→`deep_design`, `roster`→`feedback`) **with read-aliases**;
  `schema_version` stays 2 (additive); a game at `authoring` (the inheritance) is untouched.

## Cross-references
`references/content-framework.md` (the operational question set) · `references/step-4-deep-design.md` (Step 4,
generate) · `references/step-5-feedback.md` (Step 5, review) · `references/step-2-toplevel.md` §8 (the §1
declarations) · `references/run-mode.md` (navigation at junctions) · `references/ledger-schema.md`
(`deep_design`/`feedback` blocks + aliases). Supersedes `18` (the content-roster step). Relates to `22` (the
machine — §4E), `09` (desire ladder — §1B), `11` (reactive world — §4C/§5B), `13` (economy — §2C), `17`
(frontier — §1F).
