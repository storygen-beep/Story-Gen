"""The ledger's `decided` list (third pass, group 1, LO 2026-11-03): "Write every 'later' and
'waive' into the ledger with its reason (G54, promises[]). The checks should show them as
decided, not failing." `references/state.md` has the key.

  · a FAIL gate whose every detail row an entry covers is DECIDED, with the decision and why;
  · rows no entry covers keep it FAIL, and each covered row is tagged;
  · a lint gets the same, read from its full list even when it prints only the first rows;
  · an entry naming a gate that passes, a lint that lists nothing, an unknown name, or a match
    that hits no row is stale (the lint `a decision that no longer applies`);
  · `--ship` lets a DECIDED BLOCK row through only for `waive`, or for `later release` with a
    `promises[]` row naming the entry;
  · shape.py does the same for its own checks.

Fixtures are written here; nothing in games/ is read or written.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates  # noqa: E402
import shape  # noqa: E402
import test_gates_ws5 as ws5  # noqa: E402

SCRIPT = os.path.join(os.path.dirname(HERE), "gates.py")


def entry(gate, match=None, decision="later release", why="it waits for release 2", id="X1"):
    return {"id": id, "gate": gate, "match": match, "decision": decision, "why": why,
            "signed": "LO 2026-11-03"}


def fail_row(name="location fill", detail=("cafe: declared 9,000 words, delivered 3,443",
                                           "corner_shop: declared 1,000 words, delivered 35")):
    return {"gate": name, "pass_": False, "na": False, "few": False, "parked": False,
            "headline": "13/37 on their own budget", "detail": list(detail)}


# ── gates ────────────────────────────────────────────────────────────────────
def test_every_row_covered_is_decided_with_the_reason():
    r = fail_row()
    gates._apply_decided([r], {"decided": [entry("location fill")]})
    assert r["status"] == "DECIDED"
    assert r["headline"].startswith("DECIDED (later release, it waits for release 2) — ")
    assert r["pass_"] is False                         # decided is not a pass


def test_a_row_no_entry_covers_keeps_it_fail_and_tags_the_covered_one():
    r = fail_row()
    gates._apply_decided([r], {"decided": [entry("location fill", ["corner_shop"])]})
    assert r["status"] == "FAIL"
    assert "1 of 2 row(s) decided" in r["headline"]
    assert r["detail"][0] == "cafe: declared 9,000 words, delivered 3,443"
    assert r["detail"][1].endswith("(decided: later release, it waits for release 2)")


def test_two_entries_covering_every_row_are_decided_and_say_which_is_which():
    r = fail_row()
    gates._apply_decided([r], {"decided": [
        entry("location fill", ["cafe"], id="A"),
        entry("location fill", ["corner_shop"], decision="waive", why="an area", id="B")]})
    assert r["status"] == "DECIDED"
    assert "later release, it waits for release 2; waive, an area" in r["headline"]
    assert r["detail"][1].endswith("(decided: waive, an area)")


def test_a_gate_with_no_rows_is_matched_on_its_headline():
    r = fail_row(detail=())
    gates._apply_decided([r], {"decided": [entry("location fill", ["13/37"])]})
    assert r["status"] == "DECIDED"


def test_no_ledger_and_no_key_change_nothing_but_add_a_status():
    for state in (None, {}):
        r = fail_row()
        gates._apply_decided([r], state)
        assert r["status"] == "FAIL" and "decided" not in r["headline"]


def test_stale_entries_are_listed():
    ok = {"gate": "adult wording", "pass_": True, "na": False, "headline": "fine", "detail": []}
    r = fail_row()
    state = {"decided": [
        entry("adult wording", id="P"),                          # the gate passes now
        entry("location fill", ["zoe_flat"], id="M"),            # the match hits nothing
        entry("no such check", id="U"),                          # no check prints it
        entry("dispatch depth", id="L"),                         # a lint that printed nothing
        entry(None, id="N"),                                     # no check covers it: recorded
        {"id": "B", "gate": "location fill", "decision": "maybe", "why": ""},   # malformed
    ]}
    results = gates._apply_decided([ok, r], state)
    stale = dict(gates._decided_stale(results, {}, state))
    assert "passes now" in stale["P"]
    assert "'zoe_flat' hits no row of `location fill`" in stale["M"]
    assert "no gate, lint or shape.py check" in stale["U"]
    assert "lists nothing now" in stale["L"]
    assert "N" not in stale
    assert any("not read" in why and "'maybe'" in why for who, why in stale.items())
    block = gates._decided_stale_block(list(stale.items()))
    assert f"lint · {gates.DECIDED_STALE_LINT} — 5 entries" in block


def test_a_shape_check_name_is_not_stale_in_gates():
    state = {"decided": [entry("her life has threads", id="S")]}
    assert gates._decided_stale(gates._apply_decided([], state), {}, state) == []


# ── lints: the full list behind the printed rows ─────────────────────────────
def _lint_text(rows, n):
    """What main() captures for one lint that prints `rows[:n]` through `_rows`."""
    gates._DECIDED_CAPTURE.update(on=True, lists=[])
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        print("  lint · dispatch depth — 3 dispatching activities")
        for h in gates._rows(rows, n):
            print(f"          · {h}")
        if len(rows) > n:
            print(f"          · … and {len(rows) - n} more")
        print("          (a LIST, never a score)")
    gates._DECIDED_CAPTURE["on"] = False
    return buf.getvalue()


def test_a_lint_every_row_covered_is_decided():
    text = _lint_text(["living_tv: 4 outcomes", "bath: 2 outcomes"], 8)
    out, st = gates._decided_lints(text, gates._decided_entries(
        {"decided": [entry("dispatch depth")]})[0])
    assert "lint · dispatch depth — DECIDED (later release, it waits for release 2) — 3 disp" in out
    assert st["dispatch depth"]["status"] == "DECIDED"
    assert gates._DECIDED_MARK not in out and "\x00" not in out


def test_a_lint_match_reaches_a_row_it_does_not_print():
    rows = ["living_tv: 4 outcomes", "bath: 2 outcomes", "porch: 1 outcome"]
    text = _lint_text(rows, 1)                                 # prints one, hides two
    out, st = gates._decided_lints(text, gates._decided_entries(
        {"decided": [entry("dispatch depth", ["porch"])]})[0])
    assert st["dispatch depth"]["rows"] == 3 and st["dispatch depth"]["decided_rows"] == 1
    assert st["dispatch depth"]["unhit"] == []                 # hidden, but it is there
    assert "1 of 3 row(s) decided" in out and "… and 2 more" in out


def test_a_lint_partly_covered_tags_its_printed_row():
    text = _lint_text(["living_tv: 4 outcomes", "bath: 2 outcomes"], 8)
    out, st = gates._decided_lints(text, gates._decided_entries(
        {"decided": [entry("dispatch depth", ["bath"], decision="waive", why="one bath")]})[0])
    assert st["dispatch depth"]["status"] == "partly decided"
    assert "· bath: 2 outcomes (decided: waive, one bath)" in out
    assert "· living_tv: 4 outcomes\n" in out


def test_a_lint_record_row_is_matched_on_its_fields():
    rows = [{"canvas": "cafe_1", "line": "He smiles."}, {"canvas": "shop_2", "line": "No."}]
    text = _lint_text(rows, 0)
    _out, st = gates._decided_lints(text, gates._decided_entries(
        {"decided": [entry("dispatch depth", ["shop_2"])]})[0])
    assert st["dispatch depth"]["decided_rows"] == 1


def test_outside_main_rows_is_a_plain_slice():
    assert gates._rows([1, 2, 3], 2) == [1, 2]


# ── --ship ───────────────────────────────────────────────────────────────────
def _ship(decision, promises=None):
    r = fail_row("every system has a card")
    state = {"decided": [entry("every system has a card", decision=decision, id="F47")],
             "promises": promises or []}
    gates._apply_decided([r], state)
    return gates._decided_block_verdict("every system has a card", r)


def test_ship_waive_does_not_block():
    ok, head, _d = _ship("waive")
    assert ok is True and gates._ship_tag(ok, head) == "DECIDED"


def test_ship_later_release_without_a_promise_blocks():
    ok, head, _d = _ship("later release")
    assert ok is False and "no promises[] row (F47) still blocks" in head
    assert gates._ship_tag(ok, head) == "FAIL"


def test_ship_later_release_with_its_promise_does_not_block():
    ok, _h, _d = _ship("later release", [{"text": "the home_life card", "made_in": "0.1",
                                          "paid_in": None, "decided": "F47"}])
    assert ok is True
    ok, _h, _d = _ship("later release", [{"text": "x", "decided": ["A2", "F47"]}])
    assert ok is True
    ok, _h, _d = _ship("later release", [{"text": "F47 mentioned but not named"}])
    assert ok is False


def test_ship_an_undecided_fail_still_blocks():
    r = fail_row("every system has a card")
    gates._apply_decided([r], {})
    assert gates._decided_block_verdict("every system has a card", r)[0] is False


# ── shape.py ─────────────────────────────────────────────────────────────────
def test_shape_rows_decided_partly_and_stale():
    rows = [("dependencies resolve", False, "35 declared",
             ["from npc_laura step 5: no such step", "from npc_tom step 4: no such step"]),
            ("a step's variables are declared", False, "6 flags", ["npc_zoe step 5: x"]),
            ("her life has threads", True, "5 thread(s)", [])]
    state = {"decided": [entry("dependencies resolve", ["npc_laura"], id="D"),
                         entry("a step's variables are declared", decision="waive", id="V"),
                         entry("her life has threads", id="T"),
                         entry("dependencies resolve", ["npc_nobody"], id="Z")]}
    out, stale = gates.apply_decided_rows(rows, state)
    assert out[0][1] is False and out[0][3][0].endswith("(decided: later release, it waits "
                                                        "for release 2)")
    assert out[1][1] == "decided" and out[1][2].startswith("DECIDED (waive, ")
    assert dict(stale) == {"T": "`her life has threads` passes now — the decision has "
                                "nothing left to cover",
                           "Z": "match 'npc_nobody' hits no row of `dependencies resolve`"}


def test_shape_main_prints_decided(tmp_path, capsys):
    path = tmp_path / "v2_state.json"
    path.write_text(json.dumps({"phase": "idea", "decided": [
        entry("every person is an adult", id="ADULT")]}))
    shape.main([str(path)])
    out = capsys.readouterr().out
    assert "ADULT: " in out or "[DECIDED]  every person is an adult" in out


# ── end to end: the text report, the tally and --json ────────────────────────
def _fixture(tmp_path, decided):
    d = tmp_path / "games" / "fx" / "toml_phases"
    d.mkdir(parents=True)
    g = ws5.base_game()
    lines = ['[project]', 'id = "fx"', 'name = "fx"', 'starting_canvas = "opening"']
    (d / "7_final_game.toml").write_text("\n".join(lines) + "\n" + ws5._toml_rest(g))
    (tmp_path / "games" / "fx" / "v2_state.json").write_text(json.dumps({"decided": decided}))
    return str(d / "7_final_game.toml")


def _run(path, *args, cwd):
    p = subprocess.run([sys.executable, SCRIPT, path, *args], capture_output=True, text=True,
                       cwd=cwd)
    return p.returncode, p.stdout


def test_end_to_end_text_and_json(tmp_path):
    path = _fixture(tmp_path, [])
    _rc, out = _run(path, "--json", cwd=str(tmp_path))
    fails = [r["gate"] for r in json.loads(out)["gates"] if r["status"] == "FAIL"]
    assert fails, "the fixture needs a failing gate to decide"
    os.remove(tmp_path / "games" / "fx" / "v2_state.json")
    import shutil
    shutil.rmtree(tmp_path / "games")
    path = _fixture(tmp_path, [entry(fails[0], id="E1"), entry("not a check", id="E2")])

    rc, out = _run(path, cwd=str(tmp_path))
    assert f"[DECIDED]  {fails[0]}" in out
    assert f"  ·  1 decided  ·  {len(fails) - 1} fail" in out
    assert f"lint · {gates.DECIDED_STALE_LINT} — 1 entry" in out and "E2: names" in out
    assert "\x00" not in out
    assert rc == (0 if len(fails) == 1 else 1)

    rc, out = _run(path, "--json", cwd=str(tmp_path))
    j = json.loads(out)
    row = next(r for r in j["gates"] if r["gate"] == fails[0])
    assert row["status"] == "DECIDED" and row["decided"][0]["id"] == "E1"
    assert j["tally"]["decided"] == 1
    assert j["decided"]["stale"][0]["id"] == "E2"
