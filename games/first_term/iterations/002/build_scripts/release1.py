"""Release 1's own cards (DECISIONS 230): the note at the top of the Quests page. It carries release_until = 1,
so it is in the release 1 build only. The people's stop cards come from canv.step_cards (release_map.STOP_CARDS)."""
import sys

from canv import emit_card
from release_map import RELEASE_NOTE

if __name__ == "__main__":
    text = ("# =============================================================================\n"
            "# First Term — 5 · RELEASE 1 (DECISIONS 230): the release note card\n"
            "# =============================================================================\n")
    text += emit_card(RELEASE_NOTE)
    open(sys.argv[1], "w").write(text)
    print("release1: 1 card")
