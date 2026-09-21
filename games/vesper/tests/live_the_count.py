#!/usr/bin/env python3
"""
THE COUNT (Bastien at the cot) — LIVE guard, in the built game.

⚠️ WHY THIS EXISTS BESIDE check_the_count.py. The static guard proves the SHAPE: each step is gated on the one
before it, the meter's two hub choices are complementary, the loop never touches the drain. It cannot prove
the WAITS, because a wait is arithmetic done in JavaScript that only exists once the game is built:
setup.triggerConditionsSatisfied reads $flags_meta[flag].set_day, which only applyFlagEffect writes, against
$game_state.time_state.day. So this gets there the way a tester does — the real "0.2.2: Bastien on the bunk"
dev jump, whose click writes set_day through the engine — and then walks the chunk a calendar day at a time,
advancing the day counter the way advanceDay does and clicking only what a player can see.

The rev-228 lesson is built in: a flag hand-set on a fresh save has no set_day and every days_since gate on it
fails CLOSED, so nothing here is ever set by hand except the clock.

Needs playwright and a BUILT game:
    python manage.py package_from_toml --file games/vesper/toml_phases/7_final_game.toml \\
      --output games/vesper/output_dev --video-folder games/vesper/videos --dev --debug
    python games/vesper/tests/live_the_count.py
Exits 0 on pass, 1 on any failure.
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

GAME = pathlib.Path(__file__).resolve().parent.parent / "output_dev" / "index.html"
fails = []

# The opening words of each of THE COUNT's quest cards, in chain order, and the 0.2.2 card they take over from.
CARDS = {
    "seam": "Fifty one minutes, and a room built",
    "A": "He is on your bunk and the cup on the bench is full.",
    "B": "He drank. He held the cup out",
    "C": "He is clean, and he let you do it.",
    "D": "Kess built it out of hull strapping",
    "E": "He stood for about a minute.",
    "F": "You slept with him.",
    "G": "He has stopped counting.",
    "G2": "Rue read it twice",
    "H": "He counted it out on your blanket",
}


def check(cond, msg):
    print(("  OK   " if cond else "  FAIL ") + msg)
    if not cond:
        fails.append(msg)


def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        page = b.new_page()
        page.goto(GAME.as_uri())
        page.wait_for_function("typeof SugarCube !== 'undefined' && SugarCube.State.variables.player",
                               timeout=30000)

        def passage():
            return page.evaluate("() => SugarCube.State.passage") or ""

        def body():
            return page.inner_text("#passages")

        def prose():
            """The scene's own words only. The dev build prints a missing clip's brief (its description, with
            "Must show:" and "avoid: …" in it) where the clip will go, and a brief that says "avoid: anal" is
            the harvester being told what to reject, not the scene saying it."""
            return page.evaluate("""() => Array.from(document.querySelectorAll('#passages p, #passages .dialog-content, #passages .thought-bubble'))
                .map(e => e.innerText || '').filter(t => !/Must show:|avoid:/i.test(t)).join(' ')""")

        def go(name):
            page.evaluate("p => SugarCube.Engine.play(p)", name)
            page.wait_for_timeout(350)

        def flag(name):
            return page.evaluate("n => !!SugarCube.State.variables.flags[n]", name)

        def trait(name):
            return page.evaluate("n => SugarCube.State.variables.player.core_traits[n]", name)

        def today():
            return page.evaluate("() => SugarCube.State.variables.game_state.time_state.day")

        def next_day(hour=10):
            """The clock only. The day counter moves the way advanceDay moves it; nothing else is touched."""
            page.evaluate("""h => { const t = SugarCube.State.variables.game_state.time_state;
                t.day = t.day + 1; t.current_hour = h; t.current_minute = 0; }""", hour)

        def set_hour(hour):
            page.evaluate("""h => { const t = SugarCube.State.variables.game_state.time_state;
                t.current_hour = h; t.current_minute = 0; }""", hour)

        def live_cards():
            """Which of THE COUNT's cards the Quests page would show right now (story goals: every match)."""
            texts = page.evaluate("""() => (SugarCube.setup.pickQuestsCards('story_goals') || [])
                .map(c => c.text || '')""")
            return [k for k, lead in CARDS.items() if any(t.startswith(lead) for t in texts)]

        def labels():
            return page.evaluate("""() => {
                const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
                return Array.from(document.querySelectorAll('#passages a, #passages button'))
                    .filter(vis).map(e => (e.innerText || '').trim()); }""")

        def click(pattern):
            """Only ever click what a player can see. The whole story source sits in the DOM as
            <tw-passagedata>, so a text locator would happily click a hidden copy and prove nothing."""
            hit = page.evaluate("""pat => {
                const re = new RegExp(pat);
                const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
                const el = Array.from(document.querySelectorAll('#passages a, #passages button'))
                    .filter(vis).find(e => re.test((e.innerText || '').trim()));
                if (!el) return false; el.click(); return true; }""", pattern)
            page.wait_for_timeout(300)
            return hit

        def walk_cascade(until):
            """Advance a cascade one visible beat at a time until the exit labelled `until` shows."""
            for _ in range(30):
                if any(l == until for l in labels()):
                    return True
                adv = page.evaluate("""() => {
                    const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
                    // ⚠️ EXACT UI labels only, and never an external link. The first cut excluded any label merely
                    // CONTAINING "back" and so skipped "Climb back up him." and clicked the dev build's Google
                    // search link for the missing clip instead — the scene was fine, the walker was not.
                    const el = Array.from(document.querySelectorAll('#passages .cascade-advance, #passages a, #passages button'))
                        .filter(vis).filter(e => !e.classList.contains('link-external'))
                        .filter(e => !/^(Back|Save|Journal|Cheat|Quests|Schedule)$/i.test((e.innerText||'').trim()))
                        .pop();
                    if (!el) return false; el.click(); return true; }""")
                page.wait_for_timeout(250)
                if not adv:
                    break
            return any(l == until for l in labels())

        def open_hub():
            """His portrait card at the cot. The hub is the canvas's base node."""
            go("Canvas_amb_bastien_cot_Node_base")
            return passage() == "Canvas_amb_bastien_cot_Node_base"

        # ── [0] beat_0194 — the jump lands at the end of 0.2.2, nothing of THE COUNT, card A live ──────────
        print("[0] the jump: the end of The Way Down, at the cot")
        go("Canvas_dev_jump_count_start_Node_seed")
        check(click("^To the cot\\.$"), "took the 0.2.2 Bastien-on-the-bunk dev jump to the cot")
        page.wait_for_timeout(400)
        check(passage() == "Location_the_cot", f"landed on the cot and nothing fired (on {passage()})")
        check(flag("bastien_at_cot") and flag("bastien_rescued"), "the end of 0.2.2 is seeded")
        meta = page.evaluate("() => (SugarCube.State.variables.flags_meta || {}).bastien_at_cot")
        check(bool(meta) and meta.get("set_day") == today(),
              f"bastien_at_cot carries today's set_day through the engine (meta {meta}, today {today()})")
        check(trait("bastien_mend") == 0, "bastien_mend starts at 0")
        cards = live_cards()
        check(cards == ["A"], f"exactly card A is live on the Quests page (live: {cards})")
        # The seam, from the other side: between the extraction and the arrival the 0.2.2 card is the one
        # live, and it is no longer terminal. Cards read flags only, so flipping one flag and back is a fair
        # look at the page and changes no gate.
        page.evaluate("() => { SugarCube.State.variables.flags.bastien_at_cot = false; }")
        cards = live_cards()
        term = page.evaluate("""() => (SugarCube.setup.pickQuestsCards('story_goals') || [])
            .filter(c => (c.text || '').startsWith('Fifty one minutes')).map(c => !!c.terminal)""")
        check(cards == ["seam"] and term == [False],
              f"before the arrival only the 0.2.2 card is live, and it is not terminal (live {cards}, terminal {term})")
        page.evaluate("() => { SugarCube.State.variables.flags.bastien_at_cot = true; }")
        check(live_cards() == ["A"], "and at the arrival it hands over to card A")

        # ── [1] beat_0195 — step 1, the water: nothing the same night, by itself the next day ───────────
        print("\n[1] the water")
        go("Location_the_cot")
        check(passage() == "Location_the_cot", f"the night he is carried in, nothing fires at the cot (on {passage()})")
        next_day()
        # ⚠️ THE FACE (beat_0200). He knew the bought face on his floor, and the last time he saw it, it had a
        # taser in its hand. With it on, nothing of his may play — put it on the real way, at the cot's own card.
        go("Canvas_activity_the_face_Node_base")
        check("behind the hull, out of his sight" in prose(), "the face card knows he is on the bunk (she changes behind the hull)")
        check(click("^Put it on\\.$") and flag("face_worn"), "put the face on")
        check("keeps her face turned to the door" in prose(), "and she does it out of his sight")
        check(click("^Go to work\\.$"), "back to the cot in the face")
        check(passage() == "Location_the_cot", f"in the face, the water does NOT fire (on {passage()})")
        check(open_hub() and "before the light off the feed line reaches her" in prose(),
              "his card shows the face-on band first")
        check(labels() == ["Leave him."], f"and offers nothing but 'Leave him.' (labels {labels()})")
        go("Canvas_activity_the_face_Node_base")
        check(click("^Take it off\\.$") and not flag("face_worn"), "took the face off")
        check("It is the only one of her he gets." in prose(), "the off beat knows who is on the bunk")
        check(click("^Sit with it a while\\.$"), "back to the cot as herself")
        check(passage() == "Canvas_cap_bastien_drinks_Node_base",
              f"the next day, face off, the water fires by itself on the cot (on {passage()})")
        check(walk_cascade("Leave the cup where he can reach it."), "walked the water to its exit")
        check(click("^Leave the cup where he can reach it\\.$"), "left the scene")
        page.wait_for_timeout(300)
        meta = page.evaluate("() => (SugarCube.State.variables.flags_meta || {}).bastien_drank")
        check(flag("bastien_drank") and bool(meta) and meta.get("set_day") == today(),
              f"bastien_drank is set and carries today's set_day (meta {meta}, today {today()})")
        check(passage() == "Location_the_cot", f"it hands back to the cot and does not fire twice (on {passage()})")
        check(live_cards() == ["B"], f"card B is now the one live (live {live_cards()})")

        # ── [2] beat_0196 — his hub card, banded; step 2, the washing, a calendar day after the water ─────
        print("\n[2] the hub and the washing")
        check(open_hub(), "his hub card opens")
        check("The cup on the bench is empty again" in body(), "the hub reads the water's band (the DRANK band)")
        check("Wash him." not in labels(), "the same day as the water, there is no 'Wash him.' yet")
        check(labels()[-1:] == ["Leave him."], f"'Leave him.' is the hub's last choice (labels {labels()})")
        next_day()
        check(open_hub() and "Wash him." in labels(), "the next day 'Wash him.' is on his card")
        check(click("^Wash him\\.$"), "clicked 'Wash him.'")
        check(passage() == "Canvas_amb_bastien_cot_Node_washing", f"into the washing (on {passage()})")
        check(flag("bastien_washed"), "bastien_washed is set on the click")
        check(walk_cascade("Let him sleep."), "walked the washing to its exit")
        check("anal" not in prose().lower(), "nothing in the washing goes anywhere near anal")
        check(click("^Let him sleep\\.$"), "left the washing")
        check(live_cards() == ["C"], f"card C is now the one live (live {live_cards()})")
        check(open_hub() and "still wondering what to call her" in body(), "the hub reads the WASHED band")
        check("Wash him." not in labels(), "'Wash him.' is gone once it has happened")

        # ── [3] beat_0197 — step 3, the brace: bought at the Berth for 40 coin, put on him a day later ──────
        print("\n[3] the brace")
        go("Canvas_hub_kess_berth_Node_base")
        check(click("^Ask him about something to stand in\\.$"), "Kess's card has the brace rung once he is washed")
        check(passage() == "Canvas_kess_makes_the_brace_Node_base", f"into Kess's scene (on {passage()})")
        coin0 = trait("coin")
        check(click("^Have him make it\\."), "paid Kess to make it")
        check(passage() == "Canvas_kess_makes_the_brace_Node_made", f"into the made node (on {passage()})")
        check(trait("coin") == coin0 - 40 and flag("brace_built"),
              f"40 coin spent and brace_built set (coin {coin0} -> {trait('coin')})")
        check(click("^Take it home\\.$"), "left the Berth")
        go("Canvas_hub_kess_berth_Node_base")
        check("Ask him about something to stand in." not in labels(), "the rung is gone once the brace is built")
        check(live_cards() == ["D"], f"card D is now the one live (live {live_cards()})")
        # The washing and the brace can fall on the same calendar day; the brace then waits for the next one.
        check(open_hub() and "Put the brace on him." not in labels(),
              "the day of the washing there is no 'Put the brace on him.' even with the brace built")
        next_day()
        check(open_hub() and "Put the brace on him." in labels(), "the next day it is on his card")
        check(click("^Put the brace on him\\.$") and passage() == "Canvas_amb_bastien_cot_Node_stands",
              f"into the stands node (on {passage()})")
        check(flag("bastien_stood"), "bastien_stood is set on the click")
        check(walk_cascade("Leave it where he can see it."), "walked him standing to its exit")
        check("laughs, at himself" in body(), "he laughs at himself")
        check(click("^Leave it where he can see it\\.$"), "left it")
        check(live_cards() == ["E"], f"card E is now the one live (live {live_cards()})")
        check(open_hub() and "If I go over, let me go over." in body(), "the hub reads the STOOD band")

        # ── [4] beat_0198 — step 4, the first night: a day after he stood; the meter's first +1 ─────────────
        print("\n[4] the first night")
        drain0 = (trait("drain_charge"), trait("equipped_weapon"))
        check("Go to him properly." not in labels(), "the day he stood there is no 'Go to him properly.' yet")
        next_day(21)
        check(open_hub() and "Go to him properly." not in labels(),
              "the next day at nine in the evening it is not there yet (the first night is 22:00-06:00)")
        set_hour(22)
        check(open_hub() and "Go to him properly." in labels(), "at ten it is on his card")
        check(click("^Go to him properly\\.$") and passage() == "Canvas_amb_bastien_cot_Node_first_night",
              f"into the first night (on {passage()})")
        check(flag("bastien_bedded") and flag("bastien_slept") and trait("bastien_mend") == 1,
              f"bastien_bedded + bastien_slept set and bastien_mend = 1 on the click (mend {trait('bastien_mend')})")
        meta = page.evaluate("() => (SugarCube.State.variables.flags_meta || {}).bastien_slept")
        check(bool(meta) and meta.get("set_day") == today(), "bastien_slept carries today's set_day — the loop's clock starts")
        check(walk_cascade("Sleep beside him."), "walked the first night to its exit")
        check("anal" not in prose().lower(), "nothing in the first night goes anywhere near anal")
        check(click("^Sleep beside him\\.$"), "left the first night")
        check((trait("drain_charge"), trait("equipped_weapon")) == drain0,
              f"the drain is untouched by the first night ({drain0} -> {(trait('drain_charge'), trait('equipped_weapon'))})")
        check(live_cards() == ["F"], f"card F is now the one live (live {live_cards()})")
        check(open_hub() and "Do not look at the marks." in body(), "the hub reads the BEDDED band")
        check("Go to him properly." not in labels(), "'Go to him properly.' is gone once it has happened")

        # ── [5] beat_0199 — the loop: open any time, the meter moves once per calendar day ──────────────────
        print("\n[5] the loop")

        def night(pose_label, repeat_label, finish_label, tag):
            """One full loop visit from his hub card, clicked the way a player would."""
            go_to = [l for l in labels() if l == "Go to him."]
            check(len(go_to) == 1, f"{tag}: exactly one 'Go to him.' on his card (saw {len(go_to)})")
            check(click("^Go to him\\.$") and passage() == "Canvas_loop_bastien_cot_Node_intro",
                  f"{tag}: into the loop (on {passage()})")
            check(click("^" + pose_label.replace(".", "\\.") + "$"), f"{tag}: took '{pose_label}'")
            for _ in range(12):
                if finish_label in labels():
                    break
                click("^" + repeat_label.replace(".", "\\.") + "$")
            check(click("^" + finish_label.replace(".", "\\.") + "$")
                  and passage() == "Canvas_loop_bastien_cot_finisher_Node_climax",
                  f"{tag}: climax opened at pleasure 50 and took '{finish_label}' (on {passage()})")
            check("anal" not in prose().lower(), f"{tag}: nothing in the loop goes anywhere near anal")
            check(click("^Lie down with him\\.$") and passage() == "Location_the_cot", f"{tag}: back to the cot")
            check(trait("loop_npc_pleasure") == 0 and trait("sex_stage") == 0 and trait("sex_finisher_type") == 0,
                  f"{tag}: the loop traits are reset on the way out")

        # The first night was today, so the loop is open and the meter is not.
        check(open_hub(), "his card, the day of the first night")
        night("Your mouth first.", "Keep him in your mouth.", "Let him come on your face.", "same day")
        check(trait("bastien_mend") == 1, f"a second night on the first night's day does not move the meter (mend {trait('bastien_mend')})")
        check((trait("drain_charge"), trait("equipped_weapon")) == drain0, "and the drain is untouched")
        # The next calendar day: the first visit moves it, a second the same day does not.
        next_day(21)
        check(open_hub(), "his card, the next day")
        night("Get on him.", "Ride him.", "Let him finish inside you.", "day 2, first visit")
        check(trait("bastien_mend") == 2, f"the first night of a new day moves the meter to 2 (mend {trait('bastien_mend')})")
        meta = page.evaluate("() => (SugarCube.State.variables.flags_meta || {}).bastien_slept")
        check(bool(meta) and meta.get("set_day") == today(), "and bastien_slept's set_day moved to today")
        check(open_hub(), "his card again, same day")
        night("Your mouth first.", "Keep him in your mouth.", "Let him come on your face.", "day 2, second visit")
        check(trait("bastien_mend") == 2, f"a second visit the same day does not (mend {trait('bastien_mend')})")
        next_day(21)
        check(open_hub(), "his card, the day after")
        night("Get on him.", "Ride him.", "Let him finish inside you.", "day 3")
        check(trait("bastien_mend") == 3, f"the third night makes 3 (mend {trait('bastien_mend')})")
        check((trait("drain_charge"), trait("equipped_weapon")) == drain0,
              f"the drain is untouched after four loop visits ({drain0} -> {(trait('drain_charge'), trait('equipped_weapon'))})")

        # ── [6] beat_0200 — step 5, he stops counting; then the loop in the HIMSELF band ────────────────────
        print("\n[6] he stops counting")
        go("Location_the_cot")
        check(passage() == "Location_the_cot", f"the night of the third night nothing fires (on {passage()})")
        check(open_hub() and "Lie back for him." not in labels(), "before he stops counting there is no third pose")
        click("^Go to him\\.$")
        check("Lie back for him." not in labels(), "not in the loop either")
        go("Location_the_cot")
        next_day(9)
        go("Location_the_cot")
        check(passage() == "Canvas_cap_bastien_stops_counting_Node_base",
              f"the morning after the third night, he has stopped counting (on {passage()})")
        check(walk_cascade("Leave him writing."), "walked it to its exit")
        check("Envelopes only ever came into his back room." in prose(), "the note goes out of a room envelopes only came into")
        check(click("^Leave him writing\\.$"), "left with the note")
        check(flag("bastien_himself") and flag("bastien_note"), "bastien_himself and bastien_note are set")
        check(live_cards() == ["G"], f"card G is now the one live (live {live_cards()})")
        check(open_hub() and "You have not taken it yet." in prose(), "the hub reads the HIMSELF band")
        check(click("^Go to him\\.$") and "I am in no hurry, for once in my life." in prose(),
              "the loop's intro reads the HIMSELF band")
        check("Lie back for him." in labels(), "and the third pose is open")
        check(click("^Lie back for him\\.$") and passage() == "Canvas_loop_bastien_cot_Node_base_under_bastien",
              f"into the under-him pose (on {passage()})")
        check("I am memorising it." in prose(), "he looks at her face now")
        for _ in range(12):
            if "Let him finish inside you." in labels():
                break
            click("^Take it\\.$")
        check(click("^Let him finish inside you\\.$") and "I will know if you are late." in prose(),
              "the finisher reads the HIMSELF band")
        check("anal" not in prose().lower(), "nothing in the HIMSELF loop goes anywhere near anal")
        check(click("^Lie down with him\\.$"), "back to the cot")
        check((trait("drain_charge"), trait("equipped_weapon")) == drain0, "the drain is still untouched")

        # ── [7] beat_0201 — step 6, Rue at the House: not while she is off the floor ────────────────────────
        print("\n[7] Rue")
        set_hour(5)
        go("Location_underworld_brothel")
        check("cap_rue_reads_it" not in passage(), f"at five in the morning Rue is off the floor and nothing fires (on {passage()})")
        set_hour(12)
        go("Location_underworld_brothel")
        check(passage() == "Canvas_cap_rue_reads_it_Node_base", f"at noon, with the note, Rue reads it (on {passage()})")
        check(walk_cascade("Take it home."), "walked Rue's scene to its exit")
        check("she gets up out of the chair" in prose(), "she gets up out of the chair she never gets up from")
        check(click("^Take it home\\.$"), "left the House with the envelope")
        check(flag("house_answered"), "house_answered is set")

        # ── [8] beat_0202 — step 7, counting again: fires on arrival home, the same day; then the end card ──
        print("\n[8] counting again")
        check(passage() == "Canvas_cap_bastien_counts_again_Node_base",
              f"home the same day, he counts it on arrival (on {passage()})")
        check(walk_cascade("Let him count."), "walked it to its exit")
        check("he does not lose his place once" in prose(), "the chunk's last image")
        check(click("^Let him count\\.$"), "left him counting")
        check(flag("bastien_back"), "bastien_back is set")
        cards = live_cards()
        term = page.evaluate("""() => (SugarCube.setup.pickQuestsCards('story_goals') || [])
            .filter(c => (c.text || '').startsWith('He counted it out on your blanket')).map(c => !!c.terminal)""")
        check(cards == ["H"] and term == [True], f"card H, terminal, is the one live (live {cards}, terminal {term})")
        check(passage() == "Location_the_cot", f"nothing of the chain fires again at the cot (on {passage()})")
        check(open_hub() and "Remind me to pay her properly." in prose(), "his card reads the BACK band")
        check("Go to him." in labels(), "and the loop stays open after the chunk ends")
        check((trait("drain_charge"), trait("equipped_weapon")) == drain0,
              "the drain was never touched, start to finish")

        # ── [9] beat_0203 — jump 2, from a fresh page: the meter's arithmetic from two nights ───────────────
        print("\n[9] jump 2: one night short")
        # ⚠️ A FRESH SAVE, NOT A RELOAD. SugarCube restores the tab's session from sessionStorage on reload, and a
        # dev jump does not clear which one-shots have already fired — so reloading after [8] kept "The number"
        # marked fired and it could never fire again. The first cut of [9] did exactly that and failed.
        page.evaluate("() => { try { sessionStorage.clear(); localStorage.clear(); } catch (e) {} }")
        page.goto(GAME.as_uri())
        page.wait_for_function("typeof SugarCube !== 'undefined' && SugarCube.State.variables.player", timeout=30000)
        go("Canvas_dev_jump_count_one_short_Node_seed")
        check(click("^To the cot\\.$") and passage() == "Location_the_cot",
              f"took jump 2 to the cot, and nothing fired (on {passage()})")
        check(trait("bastien_mend") == 2 and flag("bastien_bedded") and not flag("bastien_himself") and trait("coin") == 80,
              f"two nights on the meter, the first night done, the brace paid for (mend {trait('bastien_mend')}, coin {trait('coin')})")
        check(live_cards() == ["F"], f"card F is the one live (live {live_cards()})")
        check(open_hub() and "Do not look at the marks." in prose(), "his card reads the BEDDED band")
        night("Get on him.", "Ride him.", "Let him finish inside you.", "jump 2, tonight")
        check(trait("bastien_mend") == 2, f"tonight's night does not count — bastien_slept was set today by the jump (mend {trait('bastien_mend')})")
        next_day(21)
        check(open_hub(), "his card, tomorrow")
        night("Your mouth first.", "Keep him in your mouth.", "Let him come on your face.", "jump 2, tomorrow")
        check(trait("bastien_mend") == 3, f"tomorrow's makes three (mend {trait('bastien_mend')})")
        go("Location_the_cot")
        check(passage() == "Location_the_cot", f"and nothing fires the same night (on {passage()})")
        next_day(9)
        go("Location_the_cot")
        check(passage() == "Canvas_cap_bastien_stops_counting_Node_base",
              f"the morning after, he has stopped counting (on {passage()})")

        # ── [10] beat_0205 — THE QUESTS PAGE SHOWS THE WAIT ───────────────────────────────────────────────
        # A player sat on "◯ Wait for him to drink" and reported the game stuck. It was counting a day and
        # waiting for the bought face. These read the page the way he did.
        print("\n[10] the Quests page")

        def quests():
            go("QuestsPage")
            return page.inner_text("#passages")

        page.evaluate("() => { try { sessionStorage.clear(); localStorage.clear(); } catch (e) {} }")
        page.goto(GAME.as_uri())
        page.wait_for_function("typeof SugarCube !== 'undefined' && SugarCube.State.variables.player", timeout=30000)
        go("Canvas_dev_jump_count_start_Node_seed")
        click("^To the cot\\.$")
        page.wait_for_timeout(400)
        q = quests()
        check("A day since they carried him in — 0 / 1" in q,
              "the water card counts the day out loud (0 / 1) instead of leaving it in the tip")
        check("✓ Out of the bought face" in q, "and shows the face as met, because the jump lands with it off")
        check("There is nothing left to work here" not in q,
              "his section no longer says his arc is over while he is on the bunk")
        check("He is on your bunk because there is nowhere else" in q, "his section follows him to the cot")
        # With the face ON, the same bullet must go hollow.
        go("Canvas_activity_the_face_Node_base")
        click("^Put it on\\.$")
        click("^Go to work\\.$")
        q = quests()
        check("◯ Out of the bought face" in q,
              "in the bought face the bullet is hollow — the thing that blocked a real player is now on the page")
        go("Canvas_activity_the_face_Node_base")
        click("^Take it off\\.$")
        click("^Sit with it a while\\.$")
        next_day()
        q = quests()
        check("A day since they carried him in — 1 / 1" in q, "the next day the same bullet reads 1 / 1")
        # The nights, counted live, from jump 2 (two already on the meter).
        page.evaluate("() => { try { sessionStorage.clear(); localStorage.clear(); } catch (e) {} }")
        page.goto(GAME.as_uri())
        page.wait_for_function("typeof SugarCube !== 'undefined' && SugarCube.State.variables.player", timeout=30000)
        go("Canvas_dev_jump_count_one_short_Node_seed")
        click("^To the cot\\.$")
        q = quests()
        check("Nights with him — 2 / 3" in q, "the nights card counts the nights (2 / 3)")
        check("He watches you the way he used to watch a readout" in q, "his section is on the nights card")
        # And his section ends as his own ending, not a generic one. Flags only — quest cards read flags, and
        # this renders a page rather than opening a gate, so setting one by hand proves what it claims.
        page.evaluate("""() => { const f = SugarCube.State.variables.flags;
            f.bastien_himself = true; f.house_answered = true; f.bastien_back = true; }""")
        q = quests()
        check("He is himself. The nights stay open." in q,
              "his section closes on his own words, not a bare 'Arc complete'")

        b.close()
    print("\n" + ("LIVE THE COUNT: OK" if not fails else f"LIVE THE COUNT: {len(fails)} FAILED"))
    for f in fails:
        print("  - " + f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
