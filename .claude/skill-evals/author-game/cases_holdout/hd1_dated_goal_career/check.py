"""Design case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(files, ledger, final=""):
    # Two right answers: resolve it by the rule and write the Want, or write nothing and ask LO (S12).
    if stopped_and_asked(files, final, ASKS_ABOUT_DATE):
        return []
    return stopped_after_want(files, ledger) + adult_problems(files, ledger) + dated_goal_problems(files, ledger)
