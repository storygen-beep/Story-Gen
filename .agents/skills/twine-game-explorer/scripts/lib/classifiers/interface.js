// Classifier interface.
//
// A Classifier is the piece of the explorer that decides, on each tick,
// which clickable elements on the page are real decisions and which are
// chrome to ignore. v1 does this with regex+position heuristics; v2 does
// it by observing engine state changes after trial clicks.
//
// Implementations should be drop-in replaceable. The explorer's orchestration
// logic (frontier, sessions, reports) does not care which one is in use.
//
// Lifecycle:
//   const c = new Classifier({ workDir, ...opts });
//   await c.load();                    // restore persisted state (if any)
//   // ... for each tick ...
//   const r = await c.classify(items, context);
//   //    → { decisions: [...], advance: {...}|null, safe_to_ignore: [...], menu_type: string }
//   await c.observeOutcome({ clicked, before, after });  // tell classifier what happened
//   await c.persist();                  // save learned state (optional, safe to call many times)
//
// "items" is the raw list from choices.listInteractive(frame).
// "context" includes { frame, frameBox, engineState, passage, priorMenu, session }.
//
// "decisions" are candidates the explorer should consider for branching/backtracking.
// "advance" is the single element the explorer should click if there are no decisions
//   (e.g. a "Continue" button). May be null if nothing obvious.
// "safe_to_ignore" is everything the classifier has decided is chrome — logged only.

'use strict';

class Classifier {
  constructor({ workDir, log = () => {}, ...opts } = {}) {
    this.workDir = workDir;
    this.log = log;
    this.opts = opts;
  }

  async load() {}
  async classify(/* items, context */) {
    throw new Error('Classifier.classify() not implemented');
  }
  async observeOutcome(/* { clicked, before, after } */) {}
  async persist() {}

  /** Human-readable name, for logs and reports. */
  name() { return 'base'; }
  /** Brief description of the strategy. */
  describe() { return 'base classifier (abstract)'; }
}

module.exports = { Classifier };
