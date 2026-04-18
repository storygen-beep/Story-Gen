# Static health — new-life-project

Generated: 2026-04-17T07:55:06.139Z

## Verdict: ❌ FAIL

| Metric | Value | Bar | Result |
|---|---|---|---|
| definite_ambiguous_rate | 1.9% | ≤ 5.0% | ✅ |
| potential_ambiguous_rate | 1.1% | ≤ 20.0% | ✅ |
| dynamic_goto_rate | 0.2% | ≤ 10.0% | ✅ |
| effective_gate_unknown_rate | 42.1% | ≤ 30.0% | ❌ |
| complex_setter_density | 0.5% | < 5.0% | ✅ |

## 1. Click-text ambiguity

Edges bucketed by (source_passage, click_text). Raw duplicate buckets (≥2 edges sharing the key): **250**. Most of these are expanded `<<if>>/<<elseif>>` chains where only one gate fires at a time — not a real runtime ambiguity.

**Definite ambiguous** (≥2 edges in the bucket evaluate to `true` on initial state — autopilot *cannot* disambiguate):
- 61 / 3294 edges (1.9%)

**Top offenders:**
- `trainDestination` → "Step off" × 9 (gates: 3 true, 6 unknown, 0 false)
- `trainSit` → "Step off" × 9 (gates: 3 true, 6 unknown, 0 false)
- `trainStand` → "Step off" × 9 (gates: 3 true, 6 unknown, 0 false)
- `buffMan` → "Clean up" × 2 (gates: 2 true, 0 unknown, 0 false)
- `cafeDefault` → "Finish tasks" × 2 (gates: 2 true, 0 unknown, 0 false)
- `cafeDishes` → "Finish shift" × 2 (gates: 2 true, 0 unknown, 0 false)
- `cafeWait` → "Finish shift" × 2 (gates: 2 true, 0 unknown, 0 false)
- `crookedMan` → "Clean up" × 2 (gates: 2 true, 0 unknown, 0 false)
- `roudyMan` → "Clean up" × 2 (gates: 2 true, 0 unknown, 0 false)
- `slimMan` → "Clean up" × 2 (gates: 2 true, 0 unknown, 0 false)

**Potential ambiguous** (bucket has ≥2 edges with gates that could fire concurrently at runtime — typically due to temp vars / runtime-computed state the evaluator flags as `unknown`):
- 37 / 3294 edges (1.1%)

**Top offenders:**
- `Phone` → "Tap to view" × 4 (gates: 0 true, 2 unknown, 2 false)
- `swimLake` → "Exit waters" × 3 (gates: 0 true, 3 unknown, 0 false)
- `city` → "Upscale apartments" × 2 (gates: 0 true, 2 unknown, 0 false)
- `city` → "JJ's PI" × 2 (gates: 0 true, 2 unknown, 0 false)
- `lilyEndFuck` → "Clean up" × 2 (gates: 0 true, 2 unknown, 0 false)
- `endDayDad` → "End your date" × 2 (gates: 0 true, 2 unknown, 0 false)
- `oldPhonePic` → "Personal" × 2 (gates: 0 true, 2 unknown, 0 false)
- `church` → "Hide in the walls" × 2 (gates: 0 true, 2 unknown, 0 false)
- `churchSpycam` → "Leave" × 2 (gates: 0 true, 2 unknown, 0 false)
- `losHuevasTrain` → "Enter" × 2 (gates: 0 true, 2 unknown, 0 false)

## 2. Dynamic-goto coverage gap

- 3 / 1636 passages contain `<<goto $var>>` or similar (0.2%)

**Sample passages:**
- `oldPhoneText` → `<<goto $oldphonePIN>>`
- `oldPhoneApps` → `<<goto $oldphonePIN>>`
- `oldPhonePic` → `<<goto $oldphonePIN>>`

## 3. Gate-eval on initial state

- 1799 edges have non-empty gate stack
- true: 269 | false: 758 | unknown: 772
- raw unknown rate: 42.9%

**Unknown breakdown by gate variable class:**
- temp-var-only (`_var` — resolves at runtime): 15
- story-var-only (`$var` — real evaluator gap): 595
- mixed: 162

**Effective unknown rate** (temp-only gates excluded since they resolve at runtime when the current passage is being rendered): 42.1%

**Sample story-var unknown gates** (these are the real evaluator gaps — autopilot will see `unknown` here even at runtime):
- `Cafe` → `cafeJob` (click: "Apply for a job at the cafe") — [if] $period lte 5 ∧ [if] $job is "No job" ∧ [if] visited("cafeJob") is 0
- `Cafe` → `cafeJob` (click: "Apply for your job back...") — [if] $period lte 5 ∧ [if] $job is "No job" ∧ [else] !(visited("cafeJob") is 0)
- `Laptop` → `laptopMails` (click: ""Emails (" + $emails + ")"") — [if] $emails gte 1
- `Library` → `chloeArch` (click: "Ask Chloe about archived buildings") — [if] $doubleQuest is true && visited("chloeArch") is 0
- `Library` → `bookSex` (click: "Find the Kama Sutra") — [if] $period lte 5 ∧ [if] $booksRead gte 70
- `PI` → `questPI` (click: "null") — [if] $questPI is true
- `Park` → `parkBike` (click: "Ride your bike around the park") — [if] $period lte 5 ∧ [if] $bike is true && $bikeCond eq "good"
- `Phone` → `GMA` (click: "GMA Banking") — [if] $atm is true
- `Phone` → `phoneNotes` (click: "Check your notes") — [else] !(ndef $notesArray)
- `Phone` → `messageRalph` (click: "Tap to view") — [if] $ralphText is true

## 4. Complex setters

- total variables: 668
- parsed setters: 2845
- complex (unparseable) setters: 15
- parse errors: 15
- skipped script blocks: 20
- skipped widget passages: 64
- complex setter density: 0.5%
- indexing coverage: `partial`
