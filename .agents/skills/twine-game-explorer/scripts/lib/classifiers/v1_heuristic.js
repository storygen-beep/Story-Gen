// v1 classifier — the original regex+position approach.
//
// Wraps the existing `choices.js` functions behind the Classifier interface.
// Preserved verbatim so old BTF runs can still be reproduced for comparison.
// New games will likely NOT work well with this; prefer v2_behavioral.js.

'use strict';

const { Classifier } = require('./interface');
const choicesMod = require('../choices');

class V1HeuristicClassifier extends Classifier {
  name() { return 'v1-heuristic'; }
  describe() { return 'regex + x-position filtering; shaped around BTF-style games'; }

  async classify(items, context) {
    const { frameBox, sidebarRightEdge, priorMenu } = context;
    const filtered = choicesMod.filterToContentRegion(items, {
      sidebarRightEdge,
      frameWidth: frameBox && frameBox.width,
    });
    const uniq = choicesMod.dedupByText(filtered);
    const klass = choicesMod.classify(uniq, { priorMenu });

    // Translate to the common shape
    let decisions = [];
    let advance = null;
    if (klass.type === 'advance' || klass.type === 'single') {
      advance = uniq[0] || null;
    } else if (['branch', 'payment', 'quiz', 'location', 'action_loop', 'other'].includes(klass.type)) {
      decisions = uniq;
      if (!decisions.length) {
        advance = choicesMod.pickAdvance(filtered, { sidebarRightEdge });
      }
    } else {
      advance = choicesMod.pickAdvance(filtered, { sidebarRightEdge });
    }

    const rejected = (filtered._rejected || []).slice(0, 20);
    return {
      decisions,
      advance,
      safe_to_ignore: rejected,
      menu_type: klass.type,
      meta: klass.meta || null,
    };
  }

  // v1 doesn't learn from outcomes — it's pure pattern matching.
  async observeOutcome() {}
  async load() {}
  async persist() {}
}

module.exports = { V1HeuristicClassifier };
