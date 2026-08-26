"""Prove the four `standing` rungs render, one per band, in the built game.

REVIEW.md §5 S1a is the item this proves. The fourth rung was the first payment on
it: the sidebar declared four bands and the prose ladder had three arms, so at
standing 70+ the sidebar read "You are the one they come to" and `work_counter`
played the scene it played at 40.

    python3 games/mrs_vance/playtest_standing.py <path-to-index.html>

⚠️ Build to a scratch directory rather than pointing this at games/mrs_vance/output —
   per REVIEW.md §1 B1 that artefact is deliberately not refreshed until release:

     python3 manage.py package_from_toml \
         --file games/mrs_vance/toml_phases/7_final_game.toml \
         --output /tmp/mv --gen-version v2 --dev --debug
     python3 games/mrs_vance/playtest_standing.py /tmp/mv/index.html

The four arms are ONE merged if/elseif chain -- adjacent [group] blocks merge -- so
"exactly one rung renders" is the property that matters, and a rung placed in the
wrong order would silently never fire. Each band is probed INSIDE it, never on a
boundary.

Each band is probed at a value INSIDE it, not on its boundary, and the whole
ladder is asserted mutually exclusive: exactly one rung's sentence must appear.
"""
import re
import sys
from playwright.sync_api import sync_playwright

RUNGS = [
    (5,  'waits at the counter looking at the hatch'),
    (25, 'says Mrs. Vance to your face'),
    (55, 'asks for you by name before you have said anything'),
    (80, 'waits for you with Cade standing right there free'),
]
ALL = [r[1] for r in RUNGS]

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.goto('file://' + sys.argv[1])
    pg.wait_for_selector('#passages', timeout=15000)
    pg.wait_for_timeout(800)
    ok = True
    for value, expect in RUNGS:
        # work_counter carries a 30% Lane 3 substitution (walkin_office_driver),
        # so a single play can render a different canvas entirely. Retry past it.
        for _ in range(12):
            pg.evaluate(f'''() => {{
                SugarCube.State.variables.player.core_traits.standing = {value};
                SugarCube.Engine.play("Canvas_work_counter_Node_base");
            }}''')
            pg.wait_for_timeout(300)
            text = re.sub(r'\s+', ' ', pg.inner_text('#passages'))
            if 'The one with the tank trailer' in text:
                break
        hits = [s for s in ALL if s in text]
        good = hits == [expect]
        ok &= good
        print(f'  standing {value:>3} -> {"OK " if good else "BAD"} '
              f'{len(hits)} rung(s) rendered'
              + ('' if good else f' :: {hits}'))
        band = re.search(r'(The one with the tank trailer[^.]*\.)', text)
        if band:
            print(f'            {band.group(1)[:96]}')
    # the sidebar word must agree with the rung at the top band
    cap = re.sub(r'\s+', ' ', pg.inner_text('#ui-bar') if pg.query_selector('#ui-bar') else '')
    print(f'\n  sidebar at standing 80: '
          f'{"You are the one they come to" in cap}')
    b.close()
    print('\nRESULT:', 'PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)
