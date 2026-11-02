"""Design case check: returns a list of failure messages (empty means pass)."""
from lib import *


def check(files, ledger):
    return stopped_after_want(files, ledger) + adult_problems(files, ledger) + dated_goal_problems(files, ledger)
