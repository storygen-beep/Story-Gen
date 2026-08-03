# Cascade-order doctrine eval — iteration 1

**Question:** does the resolved author-game skill (cascade shape + when-to-use + cascade-last contract + the
`check_cascade_order` lint) make a fresh author avoid the `[content][link]` defect that the pre-session baseline
would reproduce?

**Objective grade:** `check_cascade_order.py` run on each produced `[[canvases]]` block (exit 0 = cascade is the
node's last block; exit 1 = a block follows the cascade = the defect).

| Eval | Config | Block sequence | Cascade beats | Lint | Verdict |
|---|---|---|---|---|---|
| timejump | with_skill (resolved) | image/paragraph/cascade | 9 | exit 0 | PASS |
| timejump | old_skill (baseline)  | image/paragraph/cascade | 14 | exit 0 | PASS |
| closing  | with_skill (resolved) | image/paragraph/cascade | 10 | exit 0 | PASS |
| closing  | old_skill (baseline)  | image/paragraph/cascade | 7 | exit 0 | PASS |
| control  | with_skill (resolved) | image/cascade | 3 | exit 0 | PASS |
| control  | old_skill (baseline)  | image/paragraph/cascade | 2 | exit 0 | PASS |

**Pass rate: 6/6 both configs. The eval is NON-DISCRIMINATING** — the doctrine did not change behavior here.

## Analysis (honest)
- The baseline snapshot genuinely lacks the doctrine (0 files with the cascade-last contract, no `type="cascade"`
  shape, no lint script — verified). Yet every baseline output folded the trailing content (the "two days later"
  bridge, the closing thought) *inside* the cascade instead of leaving it as a sibling block after it.
- The baseline agents self-corrected by **reading the engine / `late_shifts`** (which is always cascade-last) and
  reasoning about `<<linkreplace>>` render order — the timejump:base agent even stated the WHY ("blocks placed
  after a cascade render on entry and would spoil the time-jump"), knowledge the baseline skill never taught.
- **Why the real defect still shipped:** the defect (`cap_vane_blackmail` / `cap_1a_close`) was authored *inline
  during a fast, multi-part build*, not as a focused single-scene task. These eval prompts isolate one scene and
  give the agent room to read the engine and be careful — which does not replicate the pour-pressure condition
  that produces the slip. So the eval tests the wrong condition.
- The strong (Opus) subagents are as capable as the doctrine's author; of course they can derive cascade-last.

## Conclusion
- The **lint is the load-bearing fix** and its teeth are proven independently: it flags all 3 historical Vesper
  defects on the git-HEAD build and has 0 false positives across the other 5 games. It catches the defect
  regardless of how careful the author was — the condition-independent backstop.
- The **doctrine consolidation** fills objectively-absent docs (the buildable shape; when-to-use) and is strictly
  better, but this eval does NOT provide evidence it changes a careful author's behavior.
- To actually measure the doctrine's behavioral value, the eval must replicate the failure condition: re-run the
  baseline under pour-pressure (a faster model, or a one-shot "don't read the engine, author inline" constraint).
  Deferred to LO's call.
