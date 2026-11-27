"""Course of Temptation's Hints page and People dialog, for the v2 engine (2026-11-25).

LO: "completely aligned with the cots pages. Dont do anything extra." Both are opt-in and
emitted only by a game that asks, so every other game builds byte for byte as before:

  * `[ui] quests_layout = "hints"` — the QuestsPage passage becomes CoT's StoryHints
    (StoryHints.txt, StoryHintWidgets.txt:7-139), drawn from `[[story_hints]]`, opened in a
    dialog from a sidebar button that glows until first opened (StoryCaption.txt:623-643);
    `[[walkthroughs]]` are CoT's *Walkthrough passages (WalkthroughWidgets.txt,
    HintsBackToOverview.txt).
  * `[ui] people_page = "cot"` — the cast page becomes CoT's People dialog (Social.txt,
    SocialWidgets.txt) and its View Person dialog (DisplayNPC.txt, DisplayNPCWidgets.txt),
    filled from systems the game has: who is met (the quest cards, as castRoster), where
    people are (setup.getNpcsAtLocation), the cast page's meters (setup.castTraitRows), the
    schedule (setup.castScheduleHtml) and the Talk row (the portrait pick).

CoT parts with no system behind them are left out: lust/romance, personality, badges,
favourites, groups, crush, Memories, Physical and Elkbook tabs, the date card, gender, year
and major, the kink-content warnings, the emoji on/off option and the slow-device meter
option. CoT's sources are under
/Users/a0000/Documents/Player_Legibility_Study_20260825/corpus/course-of-temptation/passages/.

Every string the player reads here is CoT's, except the dialog title "Quests" (LO kept the
name) and the schedule accordion's "Schedule" (CoT's is "Nightlife Schedule").

All markup is built in JavaScript, like setup.castScheduleHtml, so no SugarCube macro sits
between two others (each line break between v2 macros renders as <br>).

Pages, not dialogs (LO 2026-11-26: "change guest page and people's page, so they are now modal.
They should have their own page. This design can be ported into that page. And a schedule modal
in the people's page should work like before."): the sidebar buttons go to QuestsPage and
CastPage, a walkthrough to QuestsWalkthrough and a person to PersonPage, each an info page with
← Back. The one dialog left is the person's schedule, the cast page's old pop-up
(setup.castOpenSchedule).
"""
from __future__ import annotations

import html
import json
from typing import Any

from apps.game_generation.twee_comprehensive.generators.people_system import (
    PEOPLE_VIEW_CSS,
    people_view_js,
)

# ── Quests = CoT's Hints page ────────────────────────────────────────────────

# The sidebar button. CoT wraps the button in <span class="glow"> until $firsttime.tutorial
# is set, which the page sets when it is opened; $hints_opened is ours.
HINTS_JOURNAL_BUTTON_WIDGET = """<<widget "journalButton">>
<!-- Quests - the button glows until it is first opened, then shows "N new" (P80) -->
<div id="journal-btn-widget">
  <<if $hints_opened>><<link "Quests">><<run setup.openHints()>><</link>><<print setup.hintsBadgeHtml()>><<else>><span class="glow"><<link "Quests">><<run setup.openHints()>><</link>></span><</if>><span class="nav-i">📋</span>
</div>
<</widget>>"""

_HINTS_JS = r"""
(function () {
setup.story_hints = %%STORY_HINTS%%;
setup.walkthroughs = %%WALKTHROUGHS%%;

// CoT's two statuses (StoryHints.txt). CoT's key is "In Progress   ", padded so that
// slice(0, -3) drops the emoji when emojis are off; the padding never shows.
var STATUSES = ["In Progress", "Completed ✅"];
var END_LINE = "You have reached the end of this storyline... for now! But there may still be recurring events.";

function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
        .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
// Every condition holds (an empty list holds): CoT's setup.evaluate, on the quest cards' evaluator.
function holds(list) {
    for (var i = 0; i < (list || []).length; i++) {
        try { if (!setup.checkQuestsCondition(list[i])) return false; } catch (e) { return false; }
    }
    return true;
}
setup.hintsHolds = holds;

// The categories in file order, each once.
setup.hintCategories = function () {
    var out = [];
    setup.story_hints.forEach(function (h) { if (out.indexOf(h.category) === -1) out.push(h.category); });
    return out;
};

// The redesign (LO 2026-11-27, card P80): the same words in the sidebar's look. A coloured dot
// per category, by its place in the file, so a category keeps its colour.
var DOTS = ["#e8b04b", "#7aa2f7", "#3ecfb8", "#c792ea", "#f28fad", "#f2a65a", "#9bd36b", "#e07a7a"];
function dot(cat) {
    var i = Math.max(0, setup.hintCategories().indexOf(cat));
    return '<span class="hint-dot" style="background:' + DOTS[i % DOTS.length] + '"></span>';
}
// What the page lists right now: every entry whose `when` holds, with its state.
function visible() {
    return setup.story_hints.filter(function (e) { return holds(e.when); })
        .map(function (e) { return { entry: e, st: setup.hintState(e) }; });
}
function lineOf(x) { return x.st.text === "end" ? END_LINE : x.st.text; }
function isDone(x) { return x.st.status === STATUSES[1]; }
// $hints_seen: each storyline's line as she last saw it. Before the first opening nothing is
// seen and nothing counts as changed, so a new game opens with no tags.
setup.hintsChanged = function () {
    var v = State.variables;
    if (!v.hints_opened || !v.hints_seen) return {};
    var out = {};
    visible().forEach(function (x) {
        var seen = v.hints_seen[x.entry.title];
        if (seen !== lineOf(x)) out[x.entry.title] = seen === undefined ? "New" : "Updated";
    });
    return out;
};
function markSeen() {
    var seen = {};
    visible().forEach(function (x) { seen[x.entry.title] = lineOf(x); });
    State.variables.hints_seen = seen;
}
// The sidebar's "N new", shown once the page has been opened (before that the button glows).
setup.hintsBadgeHtml = function () {
    var n = Object.keys(setup.hintsChanged()).length;
    return n > 0 ? '<span class="nav-badge">' + n + ' new</span>' : '';
};
// The tags and the Done fold hold while she is on the page; the chips redraw without re-reading.
setup.hintsUi = { tags: {}, doneOpen: false };

// CoT's display rule (StoryHintWidgets.txt:7-90): walk the pairs; at the first that fails,
// show the text of the last that passed, or "Keep exploring!" when none did. When all pass,
// more than one pair is Completed; a single pair stays In Progress.
setup.hintState = function (entry) {
    var prev = null, hints = entry.hints || [];
    for (var i = 0; i < hints.length; i++) {
        if (!holds(hints[i].when)) return { status: "In Progress", text: prev === null ? "Keep exploring!" : prev, single: false };
        prev = hints[i].text;
    }
    if (prev === null) return { status: "In Progress", text: "Keep exploring!", single: false };
    if (hints.length === 1) return { status: "In Progress", text: prev, single: true };
    return { status: "Completed ✅", text: prev, single: false };
};

// One storyline's card: the title, a tag when its line changed, the category with its dot, the
// description in one muted line, then the line itself ("end" is CoT's end line), and a
// "Walkthrough →" button where the storyline has one.
function cardHtml(x, cls) {
    var e = x.entry, tag = setup.hintsUi.tags[e.title], done = isDone(x);
    var h = '<article class="hint-card' + (cls ? ' ' + cls : '') + (done ? ' hint-done' : '') + '" data-title="' + esc(e.title) + '">' +
        '<div class="hint-card-head"><span class="hint-title">' + e.title + '</span>' +
        (tag ? '<span class="hint-tag">' + tag + '</span>' : '') +
        (done ? '<span class="hint-done-mark">Done</span>' : '') +
        '<span class="hint-category">' + dot(e.category) + e.category + '</span></div>';
    if (e.description) h += '<div class="hint-desc">' + e.description + '</div>';
    h += '<div class="hint-line">' + lineOf(x) + '</div>';
    if (!done && e.walkthrough && setup.walkthroughs[e.walkthrough]) {
        h += '<div><button type="button" class="hint-wt hints-see-here" data-wt="' + esc(e.walkthrough) + '">Walkthrough →</button></div>';
    }
    return h + '</article>';
}

// "Next up": the first open storyline whose category starts "Storyline", else the first open one.
function nextUp(open) {
    for (var i = 0; i < open.length; i++) if (/^Storyline/.test(open[i].entry.category)) return open[i];
    return open[0] || null;
}
function chosenCat() {
    var c = State.variables.hintCat;
    return c && setup.hintCategories().indexOf(c) !== -1 ? c : "All";
}

// The chips, the open cards and the Done fold, redrawn when a chip or the fold is pressed.
setup.hintsListHtml = function () {
    var all = visible(), cat = chosenCat();
    var open = all.filter(function (x) { return !isDone(x); });
    var next = nextUp(open);
    var inCat = function (x) { return cat === "All" || x.entry.category === cat; };
    var cards = open.filter(function (x) { return x !== next && inCat(x); });
    var done = all.filter(function (x) { return isDone(x) && inCat(x); });
    var h = '';
    if (cards.length) h += '<div class="hint-grid">' + cards.map(function (x) { return cardHtml(x); }).join("") + '</div>';
    else if (!done.length) h += '<div class="hint-empty">Keep exploring!</div>';
    if (done.length) {
        var on = setup.hintsUi.doneOpen;
        h += '<div class="hint-done-fold"><button type="button" class="hint-done-toggle" aria-expanded="' + on + '">' +
            (on ? '▾' : '▸') + ' Done (' + done.length + ')</button>';
        if (on) h += '<div class="hint-grid">' + done.map(function (x) { return cardHtml(x); }).join("") + '</div>';
        h += '</div>';
    }
    return h;
};
function chipsHtml() {
    var cats = [];
    visible().forEach(function (x) { if (cats.indexOf(x.entry.category) === -1) cats.push(x.entry.category); });
    var cur = chosenCat();
    return ["All"].concat(cats).map(function (c) {
        return '<button type="button" class="hint-chip' + (c === cur ? ' active' : '') + '" aria-pressed="' + (c === cur) +
            '" data-hint-cat="' + esc(c) + '">' + (c === "All" ? '' : dot(c)) + c + '</button>';
    }).join("");
}

// The whole page: the header (← Back, "Quests", the counts), "Next up", the chips and the list.
// Opening it reads which lines changed since last time, then marks them all seen.
setup.hintsHtml = function () {
    setup.hintsUi.tags = setup.hintsChanged();
    markSeen();
    var all = visible();
    var open = all.filter(function (x) { return !isDone(x); });
    var next = nextUp(open);
    var h = '<div class="cot-head"><a class="link-internal cot-back" tabindex="0">← Back</a>' +
        '<h2 class="cot-page-title">Quests</h2><span class="cot-head-meta">' + open.length + ' open · ' +
        (all.length - open.length) + ' done</span></div>';
    if (next) h += '<section class="hint-next"><div class="hint-next-label">Next up</div>' + cardHtml(next, 'hint-next-card') + '</section>';
    return h + '<div id="hintfilters" class="hint-chips">' + chipsHtml() + '</div>' +
        '<div id="hintlist" class="nokeys">' + setup.hintsListHtml() + '</div>';
};

// The sidebar button goes to the Quests page, which marks itself seen (CoT's
// $firsttime.tutorial). Its own page, not a dialog (LO 2026-11-26: "They should have their own
// page. This design can be ported into that page.").
setup.openHints = function () {
    State.variables.hints_opened = true;
    Engine.play("QuestsPage");
};

// {days_until:N}: CoT's "<<highlight>>N more days<</highlight>>", counted off the day counter.
function days(text) {
    return String(text || "").replace(/\{days_until:(\d+)\}/g, function (m, n) {
        var ts = (State.variables.game_state || {}).time_state || {};
        var left = Math.max(0, Number(n) - (Number(ts.day) || 1));
        return '<span class="highlight">' + left + ' more ' + (left === 1 ? 'day' : 'days') + '</span>';
    });
}

// CoT's markers, as drawn with emojis on (WalkthroughWidgets.txt).
var MARK = { done: "✅", todo: "➡️", idea: "💡", up_to_you: "❓", stop: "🛑" };

// A *Walkthrough passage: the back button (HintsBackToOverview), then the guard's line, or
// Overview and Steps. A step reads ✅ once its `when` holds, else ➡️ and nothing after it
// shows yet; an idea / up-to-you / stop line shows while its `when` holds, and a stop ends it.
setup.walkthroughHtml = function (id) {
    var w = setup.walkthroughs[id];
    // One back, at the top: to the Quests page (P80).
    var h = '<div class="cot-head"><a class="link-internal" id="help-backward" tabindex="0">← Quests</a>' +
        '<h2 class="cot-page-title">' + esc(setup.walkthroughTitle(id)) + '</h2></div>';
    if (!w) return h;
    if (w.guard && !holds(w.guard.when)) return h + '<div>' + days(w.guard.text) + '</div>';
    h += '<div><span class="notice" style="font-size: larger">Overview</span><br><br>' + days(w.overview) +
        '<br><br><span class="notice" style="font-size: larger">Steps</span><br>';
    var steps = w.steps || [];
    for (var i = 0; i < steps.length; i++) {
        var st = steps[i], stop = false, line = null;
        if (st.kind === "step") {
            if (holds(st.when)) line = MARK.done + " " + days(st.done_text);
            else { line = MARK.todo + " " + days(st.todo_text); stop = true; }
        } else if (holds(st.when)) {
            line = MARK[st.kind] + " " + days(st.text);
            stop = st.kind === "stop";
        }
        if (line !== null) h += '<div class="hint-step">' + line + '</div><br>';
        if (stop) break;
    }
    return h + '</div>';
};

// A walkthrough is its own page too; ◀ "Back to hints page" returns to the Quests page.
setup.openWalkthrough = function (id) {
    State.variables.hints_walkthrough = id;
    Engine.play("QuestsWalkthrough");
};
setup.walkthroughTitle = function (id) {
    var w = setup.walkthroughs[id];
    return "Walkthrough: " + (w ? w.title : "");
};

// A chip shows one category ($hintCat; "All" clears it) and redraws the chips and the list.
jQuery(document).on("click", "#hintfilters .hint-chip", function () {
    var cat = this.getAttribute("data-hint-cat");
    if (cat === "All") delete State.variables.hintCat;
    else State.variables.hintCat = cat;
    jQuery("#hintfilters").empty().append(chipsHtml());
    jQuery("#hintlist").empty().append(setup.hintsListHtml());
});
jQuery(document).on("click", "#hintlist .hint-done-toggle", function () {
    setup.hintsUi.doneOpen = !setup.hintsUi.doneOpen;
    jQuery("#hintlist").empty().append(setup.hintsListHtml());
});
jQuery(document).on("click", ".hints-page .hints-see-here", function () {
    setup.openWalkthrough(this.getAttribute("data-wt"));
});
jQuery(document).on("click", "#help-backward", function () { Engine.play("QuestsPage"); });
// ← Back at the top of the Quests and People pages: back to the game, as the old bottom link did.
// Bound under one name, so the People script (which binds it too) never doubles it.
jQuery(document).off("click.cotback").on("click.cotback", ".cot-back", function () { setup.smartBack(); });
})();
"""

# The page header both pages share (P80): ← Back at the top left, the title, then anything on
# the right. Colours are the theme's (v2.py ThemeStyles), so the pages match the sidebar.
_COT_HEAD_CSS = """
.cot-head { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; margin: 0 0 18px; }
.cot-head .cot-page-title { margin: 0; font-size: 1.6em; }
.cot-head > a.link-internal { display: inline-flex; align-items: center; min-height: 40px; padding: 0 14px; border-radius: 10px; background: var(--theme-surface, #262536); border: 1px solid var(--theme-border, #383650); color: var(--theme-text, inherit); text-decoration: none; font-weight: bold; cursor: pointer; }
.cot-head > a.link-internal:hover { background: var(--theme-surface-hover, #2f2d48); }
.cot-head-meta { margin-left: auto; color: var(--theme-text-muted, #a9a6bd); font-size: 0.9em; }
"""

_HINTS_CSS = """
/* [ui] quests_layout = "hints": CoT's Hints page. */
@keyframes hints-glow {
    0%, 100% { box-shadow: 0 0 2px 0 rgba(255, 214, 102, 0.25); }
    50% { box-shadow: 0 0 10px 3px rgba(255, 214, 102, 0.85); }
}
.glow { display: inline-block; border-radius: 4px; animation: hints-glow 1.6s ease-in-out infinite; }
/* "N new" sits on the button's right edge, beside the icon, like the icon an overlay that lets
   clicks through to the link (v2.py's sidebar button family). */
.nav-badge { position: absolute; right: 34px; top: 50%; transform: translateY(-50%); pointer-events: none; padding: 0 7px; border-radius: 9px; font-size: 11px; font-weight: bold; line-height: 18px; background: var(--theme-warning, #e8b04b); color: #16151d; }
.nav-badge:last-child { right: 10px; }
""" + _COT_HEAD_CSS + """
.hints-page .notice { color: var(--theme-accent, #7ec8e3); }
.hints-page .highlight { color: var(--theme-accent, #7ec8e3); font-weight: bold; }
.hints-page .hint-next { display: flex; flex-direction: column; gap: 6px; margin-bottom: 18px; }
.hints-page .hint-next-label { font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase; font-weight: bold; color: var(--theme-warning, #e8b04b); }
.hints-page .hint-card { background: var(--theme-surface, #1f1e29); border: 1px solid var(--theme-border, #383650); border-radius: 12px; padding: 14px 16px; display: flex; flex-direction: column; gap: 6px; min-width: 0; }
.hints-page .hint-next-card { border-color: var(--theme-accent, #7ec8e3); background: var(--theme-surface-hover, #2a2840); padding: 18px 20px; }
.hints-page .hint-next-card .hint-title { font-size: 1.35em; }
.hints-page .hint-next-card .hint-line { font-size: 1.1em; }
.hints-page .hint-card-head { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.hints-page .hint-title { font-weight: bold; font-size: 1.05em; color: var(--theme-text-strong, inherit); }
.hints-page .hint-tag { font-size: 11px; font-weight: bold; padding: 1px 8px; border-radius: 999px; background: var(--theme-warning, #e8b04b); color: #16151d; }
.hints-page .hint-done-mark { font-size: 12px; font-weight: bold; color: var(--theme-success, #3ecfb8); }
.hints-page .hint-category { margin-left: auto; display: inline-flex; align-items: center; gap: 6px; font-size: 12px; color: var(--theme-text-muted, #a9a6bd); }
.hints-page .hint-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.hints-page .hint-desc { font-size: 0.88em; color: var(--theme-text-muted, #a9a6bd); }
.hints-page .hint-line { line-height: 1.5; }
.hints-page .hint-wt { margin-top: 4px; background: transparent; border: 1px solid var(--theme-accent, #7ec8e3); color: var(--theme-text, inherit); border-radius: 8px; padding: 6px 12px; cursor: pointer; font: inherit; font-size: 0.9em; }
.hints-page .hint-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
.hints-page .hint-chip { display: inline-flex; align-items: center; gap: 7px; min-height: 36px; padding: 0 14px; border-radius: 999px; cursor: pointer; font: inherit; font-size: 0.9em; font-weight: bold; background: var(--theme-surface, #1f1e29); color: var(--theme-text, inherit); border: 1px solid var(--theme-border, #383650); }
.hints-page .hint-chip.active { background: var(--theme-text, #ece9f5); color: var(--theme-bg, #16151d); border-color: var(--theme-text, #ece9f5); }
.hints-page .hint-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
.hints-page .hint-empty { color: var(--theme-text-muted, #a9a6bd); padding: 12px 0; }
.hints-page .hint-done-fold { margin-top: 18px; padding-top: 10px; border-top: 1px solid var(--theme-border, #383650); }
.hints-page .hint-done-toggle { background: transparent; border: 0; color: var(--theme-text-muted, #a9a6bd); font: inherit; font-weight: bold; cursor: pointer; min-height: 40px; padding: 0; margin-bottom: 8px; }
.hints-page .hint-done { opacity: 0.6; }
.hints-page .hint-step { line-height: 1.5; }
@media (max-width: 700px) { .hints-page .hint-grid { grid-template-columns: minmax(0, 1fr); } }
"""


def quests_hints_passages(metadata: dict[str, Any]) -> str:
    """The passages that replace the V2 cards QuestsPage under `[ui] quests_layout = "hints"`.
    QuestsPage is the page the sidebar button goes to, and QuestsWalkthrough is a walkthrough
    page; both are info pages (v2.py registers them), so ← Back returns to the game."""
    hints = metadata.get("story_hints") or []
    wts = {w["id"]: w for w in (metadata.get("walkthroughs") or [])}
    js = _HINTS_JS.replace(
        "%%STORY_HINTS%%", json.dumps(hints, ensure_ascii=False)
    ).replace("%%WALKTHROUGHS%%", json.dumps(wts, ensure_ascii=False))
    return (
        ":: QuestsHintsScript [script]" + js + "\n"
        ":: QuestsHintsStyles [stylesheet]" + _HINTS_CSS + "\n"
        # The header, with ← Back at the top, is part of the page's own markup (P80).
        ":: QuestsPage\n"
        '<<nobr>><<run State.variables.hints_opened = true>>'
        '<div class="hints-page"><<print setup.hintsHtml()>></div><</nobr>>\n'
        ":: QuestsWalkthrough\n"
        '<<nobr>><div class="hints-page"><<print setup.walkthroughHtml($hints_walkthrough)>></div><</nobr>>\n'
    )


# ── People = CoT's People dialog ─────────────────────────────────────────────

# CoT's tabs, in its order (Social.txt:39-160), with each tab's title line and empty line
# (SocialWidgets.txt:60-151). Only the tabs a game can fill: People Here always, the rest
# when some [[npcs]] entry is filed under them (template_import.PEOPLE_TABS).
PEOPLE_TAB_TABLE = [
    ("here", "📍", "People Here", "People nearby:", "There are no people here."),
    (
        "romantic_partners",
        "♥️",
        "Romantic Partners",
        "Romantic partner:",
        "You don't have a romantic partner.",
    ),
    ("friends", "😊", "Friends", "Friends:", "You have no friends. Ouch!"),
    (
        "sexual_partners",
        "😗",
        "Sexual Partners",
        "Sexual partners:",
        "You haven't been sexual with anybody yet.",
    ),
    (
        "rivals",
        "👿",
        "Rivals",
        "Rivals:",
        "You don't have any acknowledged enemies. Maybe that's a good thing!",
    ),
    ("coworkers", "💼", "Coworkers", "Coworkers:", "You don't have any coworkers."),
    (
        "acquaintances",
        "👋",
        "Acquaintances",
        "Acquaintances:",
        "There's nobody that you barely know.",
    ),
    (
        "special",
        "🎭",
        "Special",
        "People who fill a particular niche in the story of your life:",
        "You don't know anybody who seems to fill a particular niche in the story of your life.",
    ),
    ("faculty", "🎓", "Faculty", "Known faculty:", "You don't know any faculty yet."),
]

_PEOPLE_JS = r"""
(function () {
setup.people_tabs = %%TABS%%;
setup.npc_people = %%PEOPLE%%;
setup.people_order = %%ORDER%%;
// What the dialog remembers while the game runs: the tab, the page, the search. CoT keeps
// the tab across the View Person dialog and resets it from the sidebar button; the search is
// cleared on close ($socialsearch); the sort ($socialsort) and the toolbar's open state
// ($showsocialfilter) are story variables, as in CoT.
setup.peopleUi = { tab: 0, page: 0, search: "" };
var PER_PAGE = 16;

function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
        .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
function npcOf(slug) {
    var id = (setup.npc_slug_map || {})[slug];
    return id ? (State.variables.npcs || {})[id] : null;
}
function hiddenNpc(slug) {
    var h = setup.hiddenNpcs || {};
    return !!(h[slug] || h[(setup.npc_slug_map || {})[slug]]);
}
function info(slug) { return setup.npc_people[slug] || {}; }
function here() { return String((State.variables.player || {}).current_location || ""); }

// Known = met, by the cast page's rule (setup.castRoster): a person with quest cards is
// known while one card's `when` holds and that card has no `heading`; one with no card is
// always known.
setup.peopleKnown = function (slug) {
    var cards = setup.quests_cards || [];
    if (!cards.some(function (c) { return c && c.npc_id === slug; })) return true;
    var card = setup.pickQuestsCard(slug);
    return !!card && !card.heading;
};
// CoT's list name: the full name, or the anonymous name for a stranger.
setup.peopleShownName = function (slug) {
    var npc = npcOf(slug);
    if (npc && setup.peopleKnown(slug)) return npc.name || slug;
    return info(slug).stranger_name || "???";
};
// Everyone at her place now, met or not ($peopleatlocation), in file order.
setup.peopleHere = function () {
    var loc = here();
    if (!loc) return [];
    var at = setup.getNpcsAtLocation(loc);
    return setup.people_order.filter(function (s) { return at.indexOf(s) !== -1 && !hiddenNpc(s) && npcOf(s); });
};
// The sidebar button reads "People", with "N here" beside it where the passage is a place
// (CoT's passage_safe) and someone is here (P80; it was "People (N)").
setup.peopleHereCount = function () {
    var safe = setup.isRerenderSafe ? setup.isRerenderSafe(State.passage) : true;
    return safe ? setup.peopleHere().length : 0;
};
setup.peopleHereBadgeHtml = function () {
    var n = setup.peopleHereCount();
    return n > 0 ? '<span class="nav-here">' + n + ' here</span>' : '';
};
setup.peopleTabMembers = function (tabId) {
    if (tabId === "here") return setup.peopleHere();
    return setup.people_order.filter(function (s) {
        return info(s).people_tab === tabId && npcOf(s) && !hiddenNpc(s) && setup.peopleKnown(s);
    });
};

// The list is in file order (CoT's "relevance"); the sort links went with P80.
function meterRows(slug) {
    return setup.castTraitRows ? setup.castTraitRows(slug, npcOf(slug)) : [];
}
function meter(pct) {
    return '<span class="people-meter"><span class="people-meter-fill" style="width:' + pct + '%"></span></span>';
}

// <<displaypeoplebody>>.
setup.peopleBodyHtml = function () {
    var tab = setup.people_tabs[setup.peopleUi.tab] || setup.people_tabs[0];
    var list = setup.peopleTabMembers(tab.id);
    var hereNow = setup.peopleHere();
    var q = (setup.peopleUi.search || "").toLowerCase();
    if (q) list = list.filter(function (s) { return setup.peopleShownName(s).toLowerCase().indexOf(q) !== -1; });
    if (list.length === 0) {
        return '<div class="view-people-empty">' + (q ? "There is no one in this category with your current filters applied." : esc(tab.empty)) + '</div>';
    }
    var olen = list.length;
    var pages = Math.floor(olen / PER_PAGE) + (olen % PER_PAGE > 0 ? 1 : 0);
    setup.peopleUi.page = Math.min(setup.peopleUi.page, Math.max(0, pages - 1));
    var starti = PER_PAGE * setup.peopleUi.page, endi = starti + PER_PAGE - 1;
    var shown = list.slice(starti, endi + 1);
    var title = tab.id === "romantic_partners" ? "Romantic partner" + (shown.length > 1 ? "s" : "") + ":" : tab.title;
    var h = '<div class="view-people-title"><div>' + esc(title) + '</div>';
    if (starti > 0 || endi < olen - 1) {
        h += '<div class="view-people-page-button-container">' + (starti > 0
            ? '<button id="view-people-page-backward" tabindex="0" title="Previous page" aria-label="Previous page" type="button" role="button">◀</button>' : '') + '</div>';
        h += '<div>Page ' + (setup.peopleUi.page + 1) + '/' + pages + '</div>';
        h += '<div class="view-people-page-button-container">' + (endi < olen - 1
            ? '<button id="view-people-page-forward" tabindex="0" title="Next page" aria-label="Next page" type="button" role="button">▶</button>' : '') + '</div>';
    }
    h += '</div><div class="view-people-list">';
    shown.forEach(function (slug) {
        var known = setup.peopleKnown(slug), name = setup.peopleShownName(slug);
        // A card (P80): the initials circle ("??" for a stranger), the name, the role, a "Here"
        // dot when they are in her room, then the meters, each label beside its bar.
        h += '<div class="view-people-person" data-slug="' + esc(slug) + '" tabindex="0"><div class="view-people-person-header">' +
            '<div class="people-avatar" aria-hidden="true">' + (known ? esc(initials(name)) : "??") + '</div>' +
            '<div class="people-card-id"><div class="view-people-person-name"><a class="link-internal" data-slug="' + esc(slug) + '">' + esc(name) + '</a></div>';
        if (known && info(slug).role) h += '<div class="view-people-person-niche">' + esc(info(slug).role) + '</div>';
        h += '</div>';
        if (hereNow.indexOf(slug) !== -1) h += '<span class="people-here-dot">Here</span>';
        h += '</div><div class="status-meter-labeled">';
        meterRows(slug).forEach(function (r) { h += '<span class="status-meter-label">' + esc(r.label) + '</span>' + meter(r.pct); });
        h += '</div></div>';
    });
    return h + '</div>';
};

// The tabs as pills with a count (P80). A tab with no one in it yet is greyed, and still opens
// to show its empty line.
function tabBarHtml() {
    return setup.people_tabs.map(function (t, i) {
        var on = i === setup.peopleUi.tab, n = setup.peopleTabMembers(t.id).length;
        return '<button class="tabgroup-button' + (on ? ' active' : '') + (n === 0 ? ' is-empty' : '') + '" data-tab-index="' + i +
            '" type="button" role="tab" aria-selected="' + on + '"><span class="tabgroup-button-emoji">' + t.emoji +
            '</span><span class="tabgroup-button-label">' + esc(t.label) + '</span><span class="tabgroup-button-count">' + n + '</span></button>';
    }).join("");
}

// The header (P80): ← Back, "People", and the search box on the right, always open. CoT's
// "Filter Options" bar and its sort links went.
function headHtml() {
    return '<div class="cot-head"><a class="link-internal cot-back" tabindex="0">← Back</a><h2 class="cot-page-title">People</h2>' +
        '<label class="social-search-input"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">' +
        '<circle cx="11" cy="11" r="7"></circle><path d="M20 20l-4-4"></path></svg>' +
        '<input type="text" autocomplete="off" placeholder="Search" aria-label="Search people" value="' + esc(setup.peopleUi.search) + '"></label></div>';
}

setup.peopleDialogHtml = function () {
    return headHtml() + '<div class="tabgroup tabgroup-people"><div class="tabgroup-bar" role="tablist">' + tabBarHtml() +
        '</div><div class="tabgroup-content" role="tabpanel"><div id="display-people-body">' + setup.peopleBodyHtml() + '</div></div></div>';
};

// The People page and the View Person page are their own pages, not dialogs (LO 2026-11-26:
// "They should have their own page."); the tab is kept between them, as CoT keeps it.
function showPeople() {
    setup.peopleUi.page = 0;
    Engine.play("CastPage");
}
// The sidebar button opens with a clear search, on People Here when someone is here, else on the
// first tab with someone in it (P80).
setup.peopleOpen = function () {
    var tabs = setup.people_tabs, pick = 0;
    for (var i = 0; i < tabs.length; i++) {
        if (setup.peopleTabMembers(tabs[i].id).length > 0) { pick = i; break; }
    }
    setup.peopleUi.tab = pick;
    setup.peopleUi.search = "";
    showPeople();
};
function redrawBody() { jQuery("#display-people-body").empty().append(setup.peopleBodyHtml()); }

// ── View Person (DisplayNPC.txt), redesigned (P80) ──
function initials(name) {
    var parts = String(name || "").trim().split(/\s+/);
    return (parts[0] || "").charAt(0) + (parts.length > 1 ? parts[parts.length - 1].charAt(0) : "");
}
function aOrAn(word) { return /^[aeiou]/i.test(word) ? "An" : "A"; }
function hasPhoneThread(slug) {
    var ps = ((State.variables.game_state || {}).phone) || {};
    var trig = ps.triggered_conversations || {};
    var convs = (setup.phone_data && setup.phone_data.conversations) || [];
    return convs.some(function (c) { return c.npc === slug && trig[c.id]; });
}
// The gender is on the person, or comes from the people system when it is on
// (setup.peopleNpcGender, generators/people_system.py).
function pronoun(npc, slug) {
    var g = String((npc || {}).gender || (setup.peopleNpcGender ? setup.peopleNpcGender(slug) : "") || "").toLowerCase();
    return g === "male" ? "him" : g === "female" ? "her" : "them";
}

// One "← People" at the top; the identity (circle, name, role, relationship, the stranger line);
// one button, Schedule (LO 2026-11-27: "remove talk, only schedule"; talking stays in the room);
// the meters, label beside bar; then "Where to find <him/her>": the card's tip and the phone badge.
setup.peopleViewHtml = function (slug) {
    var npc = npcOf(slug) || {}, known = setup.peopleKnown(slug), stranger = info(slug).stranger_name || "";
    var name = npc.name || slug;
    var h = '<div class="cot-head"><a class="link-internal" id="view-people-backward" tabindex="0">← People</a></div>' +
        '<div class="npc-display-container"><section class="person-card">' +
        '<div class="npc-display-identity"><div class="npc-display-avatar" aria-hidden="true">' + (known ? esc(initials(name)) : "??") + '</div>' +
        '<div class="npc-display-identity-contents">';
    h += known ? '<div class="npc-display-fullname npc-display-fullname-known">' + esc(name) + '</div>'
               : '<div class="npc-display-fullname npc-display-fullname-unknown">???</div>';
    if (known) {
        if (info(slug).role) h += '<div class="npc-display-subtitle">' + esc(info(slug).role) + '</div>';
        if (npc.relationship) h += '<div class="npc-display-relationship">' + esc(npc.relationship) + '</div>';
    }
    if (stranger) h += '<div class="npc-display-anonname">' + aOrAn(stranger) + ' ' + esc(stranger) + '.</div>';
    h += '</div></div>';
    if (known && setup.castHasSchedule && setup.castHasSchedule(slug)) {
        h += '<div class="person-actions"><a class="link-internal person-btn people-schedule" data-slug="' + esc(slug) + '" tabindex="0">' +
            '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">' +
            '<rect x="3" y="5" width="18" height="16" rx="2"></rect><path d="M3 10h18M8 3v4M16 3v4"></path></svg>Schedule</a></div>';
    }
    if (known) {
        var rows = meterRows(slug);
        if (rows.length) {
            h += '<div class="status-meter-labeled npc-display-status-meters">' + rows.map(function (r) {
                return '<span class="status-meter-label">' + esc(r.label) + '</span>' + meter(r.pct);
            }).join("") + '</div>';
        }
    }
    // the personality bubbles (generators/people_system.py splices them in here)
    h += '</section>';
    if (known) {
        var card = setup.pickQuestsCard(slug), phone = hasPhoneThread(slug);
        if ((card && card.tip) || phone) {
            h += '<section class="person-where"><div class="person-where-label">Where to find ' + pronoun(npc, slug) + '</div>';
            if (card && card.tip) h += '<div class="people-tip">' + esc(card.tip) + '</div>';
            if (phone) h += '<div class="npc-display-infobubble npc-display-infobubble-contact" title="You have their number and you can call or text them.">Phone contact</div>';
            h += '</section>';
        }
    } else {
        h += '<div class="person-unknown">You\'re not sure who this is.</div>';
    }
    return h + '</div>';
};

setup.peopleView = function (slug) {
    State.variables.people_view_slug = slug;
    Engine.play("PersonPage");
};

// ── handlers ──
var $d = jQuery(document);
$d.on("click", ".social .tabgroup-button", function () {
    var i = Number(this.getAttribute("data-tab-index"));
    if (i === setup.peopleUi.tab) return;
    setup.peopleUi.tab = i;
    setup.peopleUi.page = 0;
    jQuery(".social .tabgroup-bar").empty().append(tabBarHtml());
    redrawBody();
});
// The whole card opens the person (SocialWidgets.txt: the card clicks its name).
$d.on("click", ".social .view-people-person", function () { setup.peopleView(this.getAttribute("data-slug")); });
$d.on("keydown", ".social .view-people-person", function (ev) {
    if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); setup.peopleView(this.getAttribute("data-slug")); }
});
$d.on("click", "#view-people-page-backward", function () { setup.peopleUi.page -= 1; redrawBody(); });
$d.on("click", "#view-people-page-forward", function () { setup.peopleUi.page += 1; redrawBody(); });
$d.on("click", "#view-people-backward", function () { showPeople(); });
var debounce = null;
$d.on("input", ".social .social-search-input input[type=text]", function () {
    setup.peopleUi.search = jQuery(this).val();
    clearTimeout(debounce);
    debounce = setTimeout(function () { setup.peopleUi.page = 0; redrawBody(); }, 250);
});
// The schedule is the old pop-up (setup.castOpenSchedule): day chips, today picked
// (LO 2026-11-26: "a schedule modal in the people's page should work like before").
$d.on("click", ".view-person .people-schedule", function () {
    setup.castOpenSchedule(this.getAttribute("data-slug"));
});
// ← Back at the top: back to the game. Bound under one name, so the Quests script (which binds it
// too) never doubles it.
$d.off("click.cotback").on("click.cotback", ".cot-back", function () { setup.smartBack(); });
})();
"""

_PEOPLE_CSS = """
/* [ui] people_page = "cot": the People and View Person pages, in the sidebar's look (P80). */
/* "N here", on the button's right edge (as .nav-badge on Quests). */
.nav-here { position: absolute; right: 34px; top: 50%; transform: translateY(-50%); pointer-events: none; font-size: 12px; color: var(--theme-text-muted, #a9a6bd); }
.nav-here:last-child { right: 10px; }
""" + _COT_HEAD_CSS + """
.social .social-search-input { margin-left: auto; display: flex; align-items: center; gap: 8px; min-height: 40px; padding: 0 12px; width: 240px; max-width: 100%; box-sizing: border-box; border-radius: 10px; background: var(--theme-surface, #1f1e29); border: 1px solid var(--theme-border, #383650); color: var(--theme-text-muted, #a9a6bd); }
.social .social-search-input input { flex: 1; min-width: 0; background: transparent; border: 0; outline: none; color: var(--theme-text, inherit); font: inherit; padding: 0; }
.social .tabgroup-bar { display: flex; flex-wrap: wrap; gap: 6px; padding-bottom: 10px; border-bottom: 1px solid var(--theme-border, #383650); }
.social .tabgroup-button { display: inline-flex; align-items: center; gap: 6px; min-height: 38px; padding: 0 14px; border-radius: 999px; cursor: pointer; font: inherit; font-size: 0.9em; font-weight: bold; background: var(--theme-surface, #1f1e29); color: var(--theme-text, inherit); border: 1px solid var(--theme-border, #383650); }
.social .tabgroup-button.active { background: var(--theme-text, #ece9f5); color: var(--theme-bg, #16151d); border-color: var(--theme-text, #ece9f5); }
.social .tabgroup-button.is-empty:not(.active) { background: transparent; opacity: 0.55; }
.social .tabgroup-button-count { font-size: 0.85em; padding: 0 7px; border-radius: 999px; background: rgba(127, 127, 127, 0.22); }
.social .tabgroup-content { padding-top: 14px; }
.social .view-people-title { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; color: var(--theme-text-muted, #a9a6bd); font-size: 0.9em; }
.social .view-people-title > div:first-child { flex: 1; }
.social .view-people-page-button-container button { cursor: pointer; min-height: 32px; padding: 0 10px; border-radius: 8px; }
.social .view-people-list { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
.social .view-people-person { background: var(--theme-surface, #1f1e29); border: 1px solid var(--theme-border, #383650); border-radius: 12px; padding: 14px; cursor: pointer; display: flex; flex-direction: column; gap: 10px; min-width: 0; }
.social .view-people-person:hover, .social .view-people-person:focus { background: var(--theme-surface-hover, #2a2840); outline: none; }
.social .view-people-person-header { display: flex; align-items: center; gap: 12px; }
.social .people-avatar { width: 44px; height: 44px; border-radius: 50%; flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-weight: bold; background: var(--theme-surface-alt, #34324c); }
.social .people-card-id { display: flex; flex-direction: column; min-width: 0; }
.social .view-people-person-name { font-weight: bold; }
.social .view-people-person-name a { color: var(--theme-text-strong, inherit); text-decoration: none; }
.social .view-people-person-niche { font-size: 0.85em; color: var(--theme-text-muted, #a9a6bd); }
.social .people-here-dot { margin-left: auto; display: inline-flex; align-items: center; gap: 6px; font-size: 12px; font-weight: bold; color: var(--theme-success, #3ecfb8); }
.social .people-here-dot::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: currentColor; }
.social .view-people-empty { color: var(--theme-text-muted, #a9a6bd); padding: 12px 0; }
.status-meter-labeled { display: grid; grid-template-columns: max-content minmax(0, 1fr); gap: 6px 10px; align-items: center; font-size: 0.82em; color: var(--theme-text-muted, #a9a6bd); }
.people-meter { display: block; width: 100%; height: 6px; border-radius: 3px; background: rgba(127, 127, 127, 0.25); overflow: hidden; }
.people-meter-fill { display: block; height: 100%; background: var(--theme-accent, #3ecfb8); }
.view-person .npc-display-container { display: flex; flex-direction: column; gap: 14px; max-width: 760px; }
.view-person .person-card, .view-person .person-where { background: var(--theme-surface, #1f1e29); border: 1px solid var(--theme-border, #383650); border-radius: 14px; padding: 20px 22px; display: flex; flex-direction: column; gap: 16px; }
.view-person .npc-display-identity { display: flex; align-items: center; gap: 16px; }
.view-person .npc-display-avatar { width: 72px; height: 72px; border-radius: 50%; flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-size: 1.5em; font-weight: bold; background: var(--theme-surface-alt, #34324c); }
.view-person .npc-display-identity-contents { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.view-person .npc-display-fullname { font-size: 1.5em; font-weight: bold; color: var(--theme-text-strong, inherit); }
.view-person .npc-display-relationship { font-size: 0.9em; color: var(--theme-text-muted, #a9a6bd); }
.view-person .npc-display-anonname { font-size: 0.9em; font-style: italic; color: var(--theme-text-muted, #a9a6bd); }
.view-person .person-actions { display: flex; flex-wrap: wrap; gap: 10px; }
.view-person .person-btn { display: inline-flex; align-items: center; gap: 8px; min-height: 44px; padding: 0 18px; border-radius: 10px; background: var(--theme-surface-hover, #262536); border: 1px solid var(--theme-accent, #5a56a0); color: var(--theme-text, inherit); text-decoration: none; font-weight: bold; cursor: pointer; }
.view-person .npc-display-status-meters { font-size: 0.9em; color: var(--theme-text, inherit); gap: 10px 14px; }
.view-person .npc-display-status-meters .people-meter { height: 8px; border-radius: 4px; }
.view-person .person-where { gap: 10px; padding: 16px 22px; }
.view-person .person-where-label { font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase; font-weight: bold; color: var(--theme-text-muted, #a9a6bd); }
.view-person .npc-display-infobubble-container { display: flex; flex-wrap: wrap; gap: 6px; }
.view-person .npc-display-infobubble { align-self: flex-start; border: 1px solid var(--theme-border, #383650); border-radius: 999px; padding: 2px 12px; font-size: 0.85em; }
.view-person .person-unknown { color: var(--theme-text-muted, #a9a6bd); }
@media (max-width: 900px) { .social .view-people-list { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 700px) { .social .view-people-list { grid-template-columns: minmax(0, 1fr); } .social .social-search-input { width: 100%; } }
"""


def people_cot_passages(
    cast_page: dict[str, Any],
    npc_people: dict[str, dict[str, str]],
    people_system: bool = False,
) -> str:
    """The cast section under `[ui] people_page = "cot"`: the sidebar button ("People", "N here"),
    the dialog's script and styles, and CastPage as a passage (it is an info page).

    `people_system` ([engine.people] system = "cot"): the meters become friendship (or
    Dislike), lust and control on CoT's -1000..1000 scale, and the View Person dialog gains
    the trait bubbles and the want line (generators/people_system.py)."""
    used = {p.get("people_tab") for p in npc_people.values() if p.get("people_tab")}
    tabs: list[dict[str, str]] = [
        {"id": t[0], "emoji": t[1], "label": t[2], "title": t[3], "empty": t[4]}
        for t in PEOPLE_TAB_TABLE
        if t[0] == "here" or t[0] in used
    ]
    icon = html.escape(cast_page.get("button_icon") or "")
    icon_span = f'<span class="nav-i">{icon}</span>' if icon else ""
    js = (
        _PEOPLE_JS.replace("%%TABS%%", json.dumps(tabs, ensure_ascii=False))
        .replace("%%PEOPLE%%", json.dumps(npc_people, ensure_ascii=False))
        .replace("%%ORDER%%", json.dumps(list(npc_people), ensure_ascii=False))
    )
    css = _PEOPLE_CSS
    if people_system:
        js = people_view_js(js)
        css += PEOPLE_VIEW_CSS
    return (
        ":: CastWidgets [widget nobr]\n"
        '<<widget "castButton">>\n'
        '<div id="cast-btn-widget">\n'
        f'  <<link "People">><<run setup.peopleOpen()>><</link>><<print setup.peopleHereBadgeHtml()>>{icon_span}\n'
        "</div>\n"
        "<</widget>>\n"
        "\n:: PeopleCotScript [script]" + js + "\n"
        ":: PeopleCotStyles [stylesheet]" + css + "\n"
        # The header, with ← Back (or ← People) at the top, is part of each page's markup (P80).
        ":: CastPage\n"
        '<<nobr>><div class="social cot-page"><<print setup.peopleDialogHtml()>></div><</nobr>>\n'
        ":: PersonPage\n"
        '<<nobr>><div class="view-person cot-page"><<print setup.peopleViewHtml($people_view_slug)>></div><</nobr>>\n'
    )
