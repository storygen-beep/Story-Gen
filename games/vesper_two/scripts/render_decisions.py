#!/usr/bin/env python3
"""Render DECISIONS.md from v2_state.json.

`the-sheets.md` S7: "the decision sheet and v2_state.json are ONE DOCUMENT WRITTEN TWICE."
The recorded incident is a ledger written to a schema nothing consumes -- six gates silently
degraded to backstops while one printed "[top-3 guess -- no v2_state.json]" with the file
sitting right there being read by a different gate.

So the sheet is generated rather than typed beside the ledger. There is one source of truth
and drift is impossible instead of merely discouraged.

Deterministic on purpose: no timestamps, no directory ordering, no dict iteration that the
JSON did not already fix. Running it twice produces a byte-identical file, which is what makes
"is the sheet current?" answerable by re-running it and diffing.

Usage:  python3 games/vesper_two/scripts/render_decisions.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.dirname(HERE)
LEDGER = os.path.join(GAME, "v2_state.json")
OUT = os.path.join(GAME, "DECISIONS.md")

# Bumped by hand when the design changes. NOT datetime.now() -- a generated file that changes
# on every run cannot be diffed to answer "has this drifted?".
AS_OF = "2026-09-03"

# Every gate name emitted by gates.py, extracted from the script rather than remembered, mapped
# to the sheet that discharges it. S6: "nothing a gate requires may be deferred by a sheet" --
# the incident was a walk-in deferred honestly, deliberately, with sign-off, against a GATE that
# then failed 0/5. A deferral is not a pass, so an undischarged gate prints as a known red here.
GATE_OWNER = [
    ("location fill",                       "places/*"),
    ("explicit floor",                      "scenes/*"),
    ("explicit in repeatable",              "scenes/*"),
    ("repeatable explicit media cycles",    "places/*"),
    ("an explicit beat carries a clip",     "scenes/*"),
    ("somebody speaks",                     "scenes/*"),
    ("traversal heat",                      "places/*"),
    ("standing surface",                    "people/*"),
    ("milestones open something",           "people/*"),
    ("meter ceiling",                       "DECISIONS"),
    ("ends on an opening",                  "DECISIONS"),
    ("ascent tiers expand the world",       "systems/cover,service,drain"),
    ("world reachable",                     "DECISIONS"),
    ("every authored node is reachable",    "scenes/*"),
    ("residents have homes",                "DECISIONS"),
    ("guidance exists",                     "DECISIONS"),
    ("no chain ends in silence",            "people/*"),
    ("money gates something",               "systems/coin"),
    ("sinks >= sources",                    "systems/coin"),
    ("no free uncapped income",             "systems/coin"),
    ("a price is on its label",             "places/*"),
    ("the price is in one currency",        "DECISIONS"),
    ("a place is not a catalogue",          "places/*"),
    ("the obligation is charged",           "systems/charge"),
    ("effects use a live op",               "FORMAT"),
    ("a day-cap closes",                    "places/*"),
    ("a spent day still has a door",        "places/*"),
    ("the climb is paid for",               "systems/cover,service,drain"),
    ("a banded meter is not also a number",  "DECISIONS"),
    ("the map is a place",                  "DECISIONS"),
    ("a need shuts a door",                 "systems/charge,clean"),
    ("the walk-in floor",                   "places/*"),
    ("a meter is read",                     "systems/*"),
    ("the wardrobe is read",                "systems/cover"),
    ("a declared garment can be got",       "systems/cover"),
    ("a locked door says why",              "places/*"),
    ("the climb is where you said it is",   "DECISIONS"),
    ("the start choice is read",            "OPENING"),
    ("what money buys opens a door",        "systems/coin"),
    ("she can say no",                      "people/*"),
    ("what she picks is read",              "n/a -- no customization declared"),
    ("speakers are named",                  "scenes/*"),
    ("sentence length",                     "scenes/*"),
    ("prose texture",                       "scenes/*"),
    ("the opening opens a door",            "OPENING"),
    ("every hub is met first",              "OPENING"),
    ("a meeting fires where they are",      "people/*"),
    ("no canvas key is discarded",          "FORMAT"),
    ("the label keeps its time",            "places/*"),
]


def sheet_exists(owner):
    """Does the sheet that discharges this gate actually exist on disk yet?

    The reconciliation is not allowed to claim a sheet that has not been written -- that is
    exactly the failure S6 records, one level up.
    """
    if owner.startswith("n/a"):
        return "n/a"
    if owner == "DECISIONS":
        return "yes"
    if owner == "FORMAT":
        return "yes" if os.path.exists(os.path.join(GAME, "FORMAT.md")) else "NOT YET"
    if owner == "OPENING":
        return "yes" if os.path.exists(os.path.join(GAME, "sheets", "OPENING.md")) else "NOT YET"
    kind, _, which = owner.partition("/")
    d = os.path.join(GAME, "sheets", kind)
    if not os.path.isdir(d):
        return "NOT YET"
    files = {f[:-3] for f in os.listdir(d) if f.endswith(".md")}
    if which == "*":
        return "yes" if files else "NOT YET"
    wanted = {w.strip() for w in which.split(",")}
    missing = sorted(wanted - files)
    return "yes" if not missing else "NOT YET (" + ", ".join(missing) + ")"


def table(rows, head):
    out = ["| " + " | ".join(head) + " |",
           "|" + "|".join(["---"] * len(head)) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return out


def main():
    d = json.load(open(LEDGER))
    b = d["board"]
    w = d["want"]
    L = []

    # Status follows the LEDGER, never a hardcoded string -- the sheets went [READY] when LO
    # signed the map and closed `grays`, and a generated header that still said [REVIEW] would be
    # the document disagreeing with the thing it is generated from.
    status = "[READY]" if d.get("phase") in ("sheets", "release") else "[REVIEW]"
    L += [f"# DECISIONS — Vesper: Undertow  `{status}`", ""]
    L += ["> **GENERATED from `v2_state.json` by `scripts/render_decisions.py`. Do not edit by hand.**",
          "> `the-sheets.md` S7 — the decision sheet and the ledger are one document written twice, so",
          "> here they are one document generated twice. Edit the ledger, re-run the script.",
          f"> As of {AS_OF} · phase `{d['phase']}`.", ""]

    # ---- the map, for signature -------------------------------------------------
    m = b["map"]
    L += ["## The map — THIS IS THE PART THAT NEEDS YOUR SIGNATURE", "",
          f"**Shape.** {m['shape']}", "",
          f"- archetype `{m['archetype']}` · exterior **`{m['exterior']}`** (a ROOT — nothing is its parent)",
          f"- home base `{m['home_base']}`", ""]
    L += table([[k, f"`{v}`"] for k, v in m["homes"].items()], ["character", "sleeps at"])
    L += ["",
          f"- bridges: " + " · ".join(f"`{x['from']}` → `{x['to']}` ({x['costs']['time']}m)"
                                      for x in m["bridges"]), ""]
    L += [f"**`r1_signoff`:** {m['r1_signoff']}", "",
          "> `the-map.md`: *\"A sign-off written by the author of the map is not a sign-off.\"*",
          "> The one question it has to answer: **could someone who has never seen the game draw",
          "> this place from the graph?** That is the half gate 28 cannot see.", ""]

    # ---- reversibility ----------------------------------------------------------
    L += ["## Blocked by reversibility", "",
          "### A · locked forever once v0.1 ships", "",
          f"- `narration_person` = **{d['narration_person']}** — changing it rewrites every line",
          "- the story title **Vesper: Undertow** — in-browser saves namespace off `Util.slugify(title)`",
          "- every canvas id, flag key, trait key and stat scale — renaming one strands every save",
          "", "### B · expensive", "",
          f"- the map shape (`{m['archetype']}`) and which room is the anchor",
          f"- the cast ({len(b['characters'])} people) — media is keyed to them",
          "- which systems exist, and which are `sourced`",
          "", "### C · cheap", "",
          "- every number: rung spacing, fill budgets, prices, decay rates",
          "- all prose, all media, every display name", ""]

    # ---- the keys the gates read ------------------------------------------------
    L += ["## The board, as the gates read it", "",
          f"**`who_climbs`** = `{b['who_climbs']}` — gate 34 wants ≥60% of meter-gating on her own tiers.", "",
          "### Ascent tiers", ""]
    L += table([[f"`{t}`", b["ceilings"][t]] for t in b["ascent_tiers"]], ["tier", "ceiling"])

    L += ["", "### Systems", ""]
    L += table([[f"`{s['id']}`", s["kind"], f"`{s['key']}`",
                 ", ".join(f"`{x}`" for x in s["fed_at"]) or "—",
                 ", ".join(f"`{x}`" for x in s["labels"]) or "—"]
                for s in b["systems"]],
               ["system", "kind", "key", "fed at", "labels"])

    locs = b["locations"]
    total = sum(l["fill"] for l in locs)
    anchor = next(l for l in locs if l["anchor"])
    L += ["", "### Locations", "",
          f"`[INTENT]` **{len(locs)} locations · {total:,} words budgeted · anchor "
          f"`{anchor['id']}` at {anchor['fill']/total*100:.1f}%** (floor 25%). Every figure below is a "
          "BUDGET written before the prose, not a count of prose that exists — gate 1 refuses to "
          "credit a set that is mostly non-round.", ""]
    L += table([[f"`{l['id']}`", l["fill"], "**ANCHOR**" if l["anchor"] else "",
                 "yes" if l["has_cycling_pool"] else "cold",
                 ", ".join(f"`{x}`" for x in l["labels"]), l["job"]]
                for l in locs],
               ["location", "fill", "", "heat", "labels", "job"])

    L += ["", "### Characters", ""]
    L += table([[f"`{c['id']}`", c["surfaces"], c["schedule_rows"],
                 " · ".join(f"`{k}`" for k in c["meters"]), c["why_wanted"]]
                for c in b["characters"]],
               ["character", "surfaces", "sched rows", "meters", "why she wants them"])

    L += ["", "### Needs", ""]
    L += table([[f"`{n['key']}`", n["falls"], n["fills"], n["costs"], f"**{n['shuts']}**"]
                for n in b["needs"]],
               ["need", "falls", "fills", "costs", "shuts (gate 29 reads this)"])

    e = b["economy"]
    L += ["", "### Economy", "",
          f"- currency `{e['currency']}` · written as **{e['symbol']}** · "
          f"`[settings.rent] currency_symbol` must match",
          f"- obligation: {e['obligation']}",
          f"- `[INTENT]` **{e['obligation_amount']} per charge** against `week_income` "
          f"**{e['week_income']}**",
          f"- it MOVES: {e['obligation_moves']}",
          "- sinks: " + " · ".join(e["sinks"]), ""]

    # ---- S10 guidance -----------------------------------------------------------
    L += ["## Guidance — one card per tier (S10)", "",
          "`quests_engine = \"v2\"` lights a sidebar entry and a page, and with no cards it renders a "
          "heading and nothing. No sheet in the format mentioned a quest card; nine were written from "
          "scratch after the first gate run on the game this format came from. Lostness is the genre's "
          "dominant complaint at a **4.7% median share** of player comments against grind's 0.9%.", ""]
    L += table([[f"`{t}`", "`TBD` — written in pass D", "names a place and an hour, never a number"]
                for t in b["ascent_tiers"]] +
               [["the obligation", "`TBD` — written in pass D", "when it is due and who takes it"]],
               ["card", "canvas", "says"])

    # ---- S6 reconciliation ------------------------------------------------------
    rows = [[f"`{g}`", o, sheet_exists(o)] for g, o in GATE_OWNER]
    ready = sum(1 for r in rows if r[2] == "yes")
    na = sum(1 for r in rows if r[2] == "n/a")
    L += ["", "## Gate reconciliation (S6)", "",
          "> *\"Nothing a gate requires may be deferred by a sheet.\"* The incident: a bathroom sheet "
          "said *\"not authored this release, named here so it is not forgotten\"* — honest, "
          "deliberate, signed off, and `the walk-in floor` is a GATE, which then failed 0/5. "
          "**A deferral is not a pass.**", "",
          f"`[INTENT]` **{ready} of {len(rows)} gates have their sheet on disk** "
          f"({na} n/a). Every `NOT YET` below is a KNOWN red, never a silent one. The column is "
          "computed from the filesystem, so this table cannot claim a sheet that has not been written.",
          ""]
    L += table(rows, ["gate", "discharged by", "sheet on disk?"])

    L += ["", "## Decisions log", ""]
    for x in d["decisions"]:
        L += [f"- **{x['at']}** — {x['note']}"]
    L += ["", "## Promises outstanding", ""]
    for x in d["promises"]:
        L += [f"- {x['text']} *(made {x['made_in']}, unpaid)*"]
    L += [""]

    open(OUT, "w").write("\n".join(L))
    print(f"wrote {OUT} · {ready}/{len(rows)} gates have a sheet on disk")


if __name__ == "__main__":
    main()
