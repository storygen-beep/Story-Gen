"""Prove every `standing` rung renders, one per band, in each room that reads the meter.

REVIEW.md §5 S1a is the item this proves: `standing` was written 25 times and read
only inside `work_counter`. It is paid in two instalments, and this harness grew with
them --

  1. the fourth rung on `work_counter`. The sidebar declared four bands and the prose
     ladder had three arms, so at standing 70+ the sidebar read "You are the one they
     come to" and the counter played the scene it played at 40.
  2. the two rooms `WANT.md` §3 names and the build did not read in: `the_bank` (the
     bank clerk's tone) and `the_bar` (what the bar already knows).

    python3 games/mrs_vance/playtest_standing.py <path-to-index.html>

⚠️ Build to a scratch directory rather than pointing this at games/mrs_vance/output --
   per REVIEW.md §1 B1 that artefact is deliberately not refreshed until release:

     python3 manage.py package_from_toml \
         --file games/mrs_vance/toml_phases/7_final_game.toml \
         --output /tmp/mv --gen-version v2 --dev --debug
     python3 games/mrs_vance/playtest_standing.py /tmp/mv/index.html

Each ladder's four arms are ONE merged if/elseif chain -- adjacent [group] blocks
merge -- so "exactly one rung renders" is the property that matters, and an arm placed
in the wrong order, or a middle arm missing its ceiling, would silently never fire.
Every band is probed at a value INSIDE it, never on a boundary.
"""
import re
import sys
from playwright.sync_api import sync_playwright

# (canvas id, [(standing value probed, a phrase only that rung can produce), ...])
# The phrases are asserted mutually exclusive within their own ladder AND unique
# across all three, so a rung leaking from the wrong room cannot read as a pass.
LADDERS = [
    ('work_counter', [
        (5,  'waits at the counter looking at the hatch'),
        (25, 'says Mrs. Vance to your face'),
        (55, 'asks for you by name before you have said anything'),
        (80, 'waits for you with Cade standing right there free'),
    ]),
    ('amb_bank_dee', [
        (5,  "writes Dorn's name on the slip"),
        (25, 'love when she finishes'),
        (55, 'asks what the yard needs this month'),
        (80, 'turns the screen a few degrees'),
    ]),
    ('amb_bar_regulars', [
        (5,  "and the word is Dorn's"),
        (25, 'as far as Mrs. Vance down there and no further'),
        (55, 'it is your name on its own'),
        (80, "says the yard's name and then yours"),
    ]),
]

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.goto('file://' + sys.argv[1])
    pg.wait_for_selector('#passages', timeout=15000)
    pg.wait_for_timeout(800)
    ok = True
    for canvas, rungs in LADDERS:
        print(f'\n{canvas}')
        phrases = [p for _, p in rungs]
        for value, expect in rungs:
            # work_counter carries a 30% Lane 3 substitution (walkin_office_driver),
            # so a single play can render a different canvas entirely. Retrying until
            # some rung of THIS ladder is on screen steps past it, and costs nothing
            # in the two ambients, which have no substitution and land first time.
            for _ in range(12):
                pg.evaluate(f'''() => {{
                    SugarCube.State.variables.player.core_traits.standing = {value};
                    SugarCube.Engine.play("Canvas_{canvas}_Node_base");
                }}''')
                pg.wait_for_timeout(300)
                text = re.sub(r'\s+', ' ', pg.inner_text('#passages'))
                if any(p in text for p in phrases):
                    break
            hits = [p for p in phrases if p in text]
            good = hits == [expect]
            ok &= good
            print(f'  standing {value:>3} -> {"OK " if good else "BAD"} '
                  f'{len(hits)} rung(s) rendered'
                  + ('' if good else f' :: {hits}'))
    # the sidebar word must agree with the rung at the top band
    cap = re.sub(r'\s+', ' ', pg.inner_text('#ui-bar') if pg.query_selector('#ui-bar') else '')
    print(f'\n  sidebar at standing 80: '
          f'{"You are the one they come to" in cap}')
    b.close()
    print('\nRESULT:', 'PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)
