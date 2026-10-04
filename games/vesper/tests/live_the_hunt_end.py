"""0.2.3 ending, live: the take -> the table -> the cradles in one unbroken run (taken at an hour outside both
Kess's and Cain's rows), the end card, then the shell stays visible on the Site by day and night, and Bastien's
cradle line. Run from the repo root against output_dev (built --dev --debug):  python games/vesper/tests/live_the_hunt_end.py
"""
import pathlib,sys
from playwright.sync_api import sync_playwright
url=(pathlib.Path(__file__).resolve().parent.parent / 'output_dev' / 'index.html').as_uri()
fails=[];errs=[]
def ok(c,m): print(('OK   ' if c else 'FAIL ')+m); c or fails.append(m)
TS="SugarCube.State.variables.game_state.time_state"; CT="SugarCube.State.variables.player.core_traits"
def flag(pg,f): return pg.evaluate(f"(function(){{var F=SugarCube.State.variables.flags; return Array.isArray(F)?F.includes('{f}'):!!F['{f}'];}})()")
def at(pg,h): pg.evaluate(f"{TS}.current_hour={h}; {TS}.current_minute=0")
def play(pg,p): pg.evaluate(f"SugarCube.Engine.play('{p}')"); pg.wait_for_timeout(300); return pg.inner_text('#passages')
def psg(pg): return pg.evaluate("SugarCube.State.passage")
def walk(pg,exit_text):
    for i in range(25):
        if pg.query_selector(f"#passages a:has-text('{exit_text}')"): return True
        links=[l for l in pg.query_selector_all('#passages a') if l.is_visible()]
        if not links: return False
        links[-1].click(); pg.wait_for_timeout(200)
    return False
def side(pg): return pg.inner_text('#ui-bar') if pg.query_selector('#ui-bar') else ''
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url); pg.evaluate("localStorage.clear()"); pg.reload()
    pg.wait_for_function('window.SugarCube && SugarCube.State.variables.player',timeout=30000)
    play(pg,'Canvas_dev_jump_hunt_take_Node_seed'); pg.click("#passages a:has-text('To the berth.')"); pg.wait_for_timeout(300)
    # take at 13:00 -> lands 01:03: outside Kess's hours AND outside Cain's — the run must not stop
    at(pg,13); play(pg,'Canvas_activity_draw_her_out_Node_base'); pg.click("#passages a:has-text('Draw her out.')"); pg.wait_for_timeout(300)
    walk(pg,'Get Kess.'); pg.click("#passages a:has-text('Get Kess.')"); pg.wait_for_timeout(500)
    ok(psg(pg)=='Canvas_cap_the_table_Node_base', f"the table fires on arrival at {pg.evaluate(TS+'.current_hour')}:00, outside Kess's hours ({psg(pg)})")
    ok(walk(pg,'Carry her to the Site.'), "walked the table")
    t=pg.inner_text('#passages')
    for line in ("Kess has waited up for them","from Sabin's piece","This unit will be reported lost.","Now. Before I think about it."): ok(line in t, f"renders: {line}")
    pg.click("#passages a:has-text('Carry her to the Site.')"); pg.wait_for_timeout(500)
    ok(flag(pg,'vega_dismantled') and pg.evaluate(CT+".vega_damage")==0, "vega_dismantled, damage 0")
    ok(psg(pg)=='Canvas_cap_the_cradles_Node_base', f"the cradles fire on arrival at the Site at {pg.evaluate(TS+'.current_hour')}:00 ({psg(pg)})")
    ok(walk(pg,'Not tonight.'), "walked the cradles")
    t=pg.inner_text('#passages')
    for line in ("Mind her head","like a coat on a hook","I said I would sit with it","Two cradles. Now she knows why."): ok(line in t, f"renders: {line}")
    pg.click("#passages a:has-text('Not tonight.')"); pg.wait_for_timeout(400)
    ok(flag(pg,'cradles_ready'), "cradles_ready")
    qt=play(pg,'QuestsPage'); ok('That is where this build ends' in qt and 'Chapter complete' in qt and 'lying in the second cradle' in qt, "end card L")
    ok('&amp;#x27;' not in qt and '&#x27;' not in qt, "no escaped apostrophes")
    # the shell stays visible
    at(pg,14); t=play(pg,'Location_the_site'); ok('The cradles' in t, "day: 'The cradles' card on the Site")
    t=play(pg,'Canvas_site_the_cradles_Node_base'); ok('Vega lies in the second cradle' in t and 'coat over the back of it' in t and 'Still here' not in t, "day: Vega in the cradle, Cain's coat on the chair")
    at(pg,22); t=play(pg,'Canvas_site_the_cradles_Node_base'); ok('Vega lies in the second cradle' in t and 'Still here. I said I would be.' in t and 'coat over the back' not in t, "night: Cain in the chair")
    play(pg,'Location_the_site'); ok(psg(pg)!='Canvas_cap_the_cradles_Node_base', "the cradle scene does not fire twice")
    at(pg,15); t=play(pg,'Canvas_amb_bastien_cot_Node_base'); ok("She is in Marrow's cradle, then." in t and 'wages. His men are back' not in t, "Bastien's cradle line wins over the crew band")
    b.close()
ok(not errs, f"js errors {errs[:3]}")
print("LIVE THE HUNT END: " + ("OK" if not fails else f"{len(fails)} FAILED"))
sys.exit(1 if fails else 0)
