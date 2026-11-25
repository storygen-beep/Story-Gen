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

All markup is built in JavaScript and put into the dialog with jQuery, like
setup.castScheduleHtml, so no SugarCube macro sits between two others (each line break
between v2 macros renders as <br>).
"""
from __future__ import annotations

import html
import json
from typing import Any

# ── Quests = CoT's Hints page ────────────────────────────────────────────────

# The sidebar button. CoT wraps the button in <span class="glow"> until $firsttime.tutorial
# is set, which the page sets when it is opened; $hints_opened is ours.
HINTS_JOURNAL_BUTTON_WIDGET = """<<widget "journalButton">>
<!-- Quests - CoT's Hints page in a dialog; the button glows until it is first opened -->
<div id="journal-btn-widget">
  <<if $hints_opened>><<link "Quests">><<run setup.openHints()>><</link>><<else>><span class="glow"><<link "Quests">><<run setup.openHints()>><</link>></span><</if>><span class="nav-i">📋</span>
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

// $selectedHintCats / $selectedHintStatuses, every box ticked at first (StoryHints.txt).
// A category added by a later release starts ticked in an old save too.
function filters() {
    var v = State.variables;
    if (!v.selectedHintCats) v.selectedHintCats = {};
    setup.hintCategories().forEach(function (c) { if (v.selectedHintCats[c] === undefined) v.selectedHintCats[c] = true; });
    if (!v.selectedHintStatuses) {
        v.selectedHintStatuses = {};
        STATUSES.forEach(function (s) { v.selectedHintStatuses[s] = true; });
    }
}

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

// <<displaystoryhint>>: "Hint:", the text ("end" is CoT's line), then the walkthrough link.
function hintLine(entry, text, color) {
    var h = '<br><div class="indent hint-line" style="' + color + '"><b>Hint:</b> ' + (text === "end" ? END_LINE : text);
    if (entry.walkthrough && setup.walkthroughs[entry.walkthrough]) {
        h += '<br><br>For a detailed walkthrough, with potential spoilers, <a class="link-internal hints-see-here" data-wt="' +
            esc(entry.walkthrough) + '">see here</a>.';
    }
    return h + '</div>';
}

// <<statichinttext>>: the title, the category on the right, the description.
function staticText(entry, color) {
    return '<span style="' + color + '"><span class="large">' + entry.title + '</span>' +
        '<span class="hint-category" style="float: right">' + entry.category + '</span><br><br>' +
        '<div class="indent">' + (entry.description || "") + '<br></div></span>';
}

// <<hintlist>>.
setup.hintsListHtml = function () {
    filters();
    var v = State.variables;
    var anyStatus = STATUSES.some(function (s) { return v.selectedHintStatuses[s] === true; });
    var anyCat = Object.keys(v.selectedHintCats).some(function (c) { return v.selectedHintCats[c] === true; });
    if (!anyStatus) return "Select at least one status to display!";
    if (!anyCat) return "Select at least category to display!";
    var out = "";
    setup.story_hints.forEach(function (entry) {
        if (v.selectedHintCats[entry.category] !== true) return;
        if (!holds(entry.when)) return;
        var st = setup.hintState(entry);
        if (v.selectedHintStatuses[st.status] !== true) return;
        if (st.status === "Completed ✅") {
            var grey = "color: #aaa";
            out += '<div class="rounded-border" style="overflow: hidden">' + staticText(entry, grey) +
                '<div><span style="float: right">✅</span><span>' + hintLine(entry, st.text, grey) + '</span></div></div><br>';
        } else {
            var c = "color: inherit";
            out += '<div class="rounded-border">' + staticText(entry, c) + hintLine(entry, st.text, c) +
                (st.single ? '<br>' : '') + '</div><br>';
        }
    });
    return out;
};

function box(label, attr, on) {
    return '<span class="hint-category-label"><label><input type="checkbox" ' + attr + (on ? ' checked' : '') +
        '> ' + label + '</label></span>';
}

// StoryHints: the filter table, then the list.
setup.hintsHtml = function () {
    filters();
    var v = State.variables;
    var cats = setup.hintCategories().map(function (c) {
        return box(c, 'data-hint-cat="' + esc(c) + '"', v.selectedHintCats[c] === true);
    }).join("");
    var stats = STATUSES.map(function (s) {
        return box(s, 'data-hint-status="' + esc(s) + '"', v.selectedHintStatuses[s] === true);
    }).join("");
    return '<div id="hintfilters"><table class="options-table">' +
        '<tr><td class="options-col-label">Categories</td><td>' + cats + '</td></tr>' +
        '<tr><td>&nbsp;</td></tr>' +
        '<tr><td class="options-col-label">Progress</td><td>' + stats + '</td></tr>' +
        '</table></div><br><br><div id="hintlist" class="nokeys">' + setup.hintsListHtml() + '</div>';
};

// The sidebar button: the page marks itself seen (CoT's $firsttime.tutorial), in a dialog.
setup.openHints = function () {
    State.variables.hints_opened = true;
    Dialog.setup("Quests", "hints-dialog");
    jQuery(Dialog.body()).empty().append(setup.hintsHtml());
    Dialog.open();
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
    var h = '<br><button id="help-backward" tabindex="0" title="Back to hints page" aria-label="Back to hints page" type="button" role="button">◀</button> <b>Back to hints page</b><br>';
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

setup.openWalkthrough = function (id) {
    var w = setup.walkthroughs[id];
    Dialog.setup("Walkthrough: " + (w ? w.title : ""), "hints-dialog");
    jQuery(Dialog.body()).empty().append(setup.walkthroughHtml(id));
    Dialog.open();
};

// A box redraws the list (StoryHints.txt's change handler).
jQuery(document).on("change", "#hintfilters input", function () {
    filters();
    var v = State.variables;
    var cat = this.getAttribute("data-hint-cat");
    if (cat !== null) v.selectedHintCats[cat] = this.checked;
    else v.selectedHintStatuses[this.getAttribute("data-hint-status")] = this.checked;
    jQuery("#hintlist").empty().append(setup.hintsListHtml());
});
jQuery(document).on("click", "#hintlist .hints-see-here", function () {
    setup.openWalkthrough(this.getAttribute("data-wt"));
});
jQuery(document).on("click", "#help-backward", function () { setup.openHints(); });
})();
"""

_HINTS_CSS = """
/* [ui] quests_layout = "hints": CoT's Hints page. */
@keyframes hints-glow {
    0%, 100% { box-shadow: 0 0 2px 0 rgba(255, 214, 102, 0.25); }
    50% { box-shadow: 0 0 10px 3px rgba(255, 214, 102, 0.85); }
}
.glow { display: inline-block; border-radius: 4px; animation: hints-glow 1.6s ease-in-out infinite; }
.hints-dialog .rounded-border { border: 1px solid var(--theme-border, #555); border-radius: 10px; padding: 10px 12px; }
.hints-dialog .large { font-size: 1.25em; }
.hints-dialog .indent { margin-left: 1.25em; }
.hints-dialog .notice { color: var(--theme-accent, #7ec8e3); }
.hints-dialog .highlight { color: var(--theme-accent, #7ec8e3); font-weight: bold; }
.hints-dialog .options-table td { vertical-align: top; padding: 2px 6px; }
.hints-dialog .options-col-label { font-weight: bold; white-space: nowrap; }
.hints-dialog .hint-category-label { display: inline-block; margin: 0 14px 4px 0; white-space: nowrap; }
.hints-dialog #help-backward { cursor: pointer; padding: 2px 8px; }
"""


def quests_hints_passages(metadata: dict[str, Any]) -> str:
    """The passages that replace the V2 cards QuestsPage under `[ui] quests_layout = "hints"`.
    QuestsPage stays as a passage (it is an info page and old links name it); the sidebar
    button opens the same markup in a dialog."""
    hints = metadata.get("story_hints") or []
    wts = {w["id"]: w for w in (metadata.get("walkthroughs") or [])}
    js = _HINTS_JS.replace(
        "%%STORY_HINTS%%", json.dumps(hints, ensure_ascii=False)
    ).replace("%%WALKTHROUGHS%%", json.dumps(wts, ensure_ascii=False))
    return (
        ":: QuestsHintsScript [script]" + js + "\n"
        ":: QuestsHintsStyles [stylesheet]" + _HINTS_CSS + "\n"
        ":: QuestsPage\n"
        "<<nobr>><<run State.variables.hints_opened = true>><<print setup.hintsHtml()>><</nobr>>\n"
        '<<link "← Back">><<run setup.smartBack()>><</link>>\n'
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
// "People (N)" where the passage is a place (CoT's passage_safe), else "People".
setup.peopleButtonLabel = function () {
    var safe = setup.isRerenderSafe ? setup.isRerenderSafe(State.passage) : true;
    return safe ? "People (" + setup.peopleHere().length + ")" : "People";
};
setup.peopleTabMembers = function (tabId) {
    if (tabId === "here") return setup.peopleHere();
    return setup.people_order.filter(function (s) {
        return info(s).people_tab === tabId && npcOf(s) && !hiddenNpc(s) && setup.peopleKnown(s);
    });
};

function traitValue(slug, key) {
    var t = (npcOf(slug) || {}).core_traits || {};
    return Number(t[key]) || 0;
}
// <<sortpeople>>: the sort links' orders; relevance is the file order.
function sorted(list) {
    var by = State.variables.socialsort;
    if (!by || by === "relevance") return list.slice();
    var m = /^(.*) (high-low|low-high)$/.exec(by);
    return list.slice().sort(function (a, b) {
        if (by === "alpha") return setup.peopleShownName(a).localeCompare(setup.peopleShownName(b));
        if (by === "z-alpha") return setup.peopleShownName(b).localeCompare(setup.peopleShownName(a));
        if (m) return m[2] === "high-low" ? traitValue(b, m[1]) - traitValue(a, m[1]) : traitValue(a, m[1]) - traitValue(b, m[1]);
        return 0;
    });
}
function meterRows(slug) {
    return setup.castTraitRows ? setup.castTraitRows(slug, npcOf(slug)) : [];
}
function meter(pct) {
    return '<span class="people-meter"><span class="people-meter-fill" style="width:' + pct + '%"></span></span>';
}

// <<displaypeoplebody>>.
setup.peopleBodyHtml = function () {
    var tab = setup.people_tabs[setup.peopleUi.tab] || setup.people_tabs[0];
    var list = sorted(setup.peopleTabMembers(tab.id));
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
        var known = setup.peopleKnown(slug), npc = npcOf(slug) || {};
        h += '<div class="view-people-person" data-slug="' + esc(slug) + '"><div class="view-people-person-header">' +
            '<div class="view-people-person-name"><a class="link-internal" data-slug="' + esc(slug) + '">' + esc(setup.peopleShownName(slug)) + '</a></div></div>';
        if (known && info(slug).role) h += '<div class="view-people-person-niche faded small">' + esc(info(slug).role) + '</div>';
        h += '<div class="status-meter-labeled">';
        meterRows(slug).forEach(function (r) { h += '<span class="status-meter-label">' + esc(r.label) + '</span>' + meter(r.pct); });
        h += '</div></div>';
    });
    return h + '</div><div class="view-people-list-footer">Click a person to see more.</div>';
};

function tabBarHtml() {
    return setup.people_tabs.map(function (t, i) {
        var on = i === setup.peopleUi.tab;
        return '<button class="tabgroup-button' + (on ? ' active' : '') + '" data-tab-index="' + i +
            '" type="button" role="tab" aria-selected="' + on + '"><span class="tabgroup-button-emoji">' + t.emoji +
            '</span><span class="tabgroup-button-label">' + esc(t.label) + '</span></button>';
    }).join("");
}

// <<socialfiltertoolbar>>: "Filter Options", folded until opened; the search, "Clear all
// filters" and the sort links. CoT's badge and personality filters are left out (no system).
function toolbarHtml() {
    var open = !!State.variables.showsocialfilter;
    var h = '<div id="social-filter-toolbar-content"><br><div id="shop-filter-toolbar" class="shop-filter-toolbar">' +
        '<div class="shop-filter-toolbar-header"><span class="shop-filter-toolbar-header-text bold">Filter Options</span>' +
        '<span id="social-filter-minrestore" class="shop-filter-toolbar-header-minrestore nokeys"><a class="link-internal">' +
        (open ? "" : "") + '</a></span></div>';
    if (open) {
        h += '<div class="shop-search-container nokeys"><div class="shop-search"><div class="shop-search-icon">🔎</div>' +
            '<div class="social-search-input"><input type="text" autocomplete="off" value="' + esc(setup.peopleUi.search) + '"></div>' +
            '<div class="shop-clear-button"><a class="link-internal people-search-clear">×</a></div></div></div>';
        h += '<br><a class="link-internal people-clear-filters">Clear all filters</a><br>';
        var sorts = [["alpha", "Sort by name (a -> z)"], ["z-alpha", "Sort by name (z -> a)"]];
        (setup.cast_show_traits || []).forEach(function (k) {
            var label = (setup.traitLabel ? setup.traitLabel(k) : k).toLowerCase();
            sorts.push([k + " high-low", "Sort by " + label + " (high → low)"]);
            sorts.push([k + " low-high", "Sort by " + label + " (low → high)"]);
        });
        h += '<div id="social-sort">' + sorts.map(function (s) {
            return '<a class="link-internal people-sort" data-sort="' + esc(s[0]) + '">' + esc(s[1]) + '</a>';
        }).join(" ") + ' <span class="social-sort-relevance"><a class="link-internal people-sort" data-sort="relevance">Sort by relevance</a></span></div>';
    }
    return h + '</div></div>';
}

setup.peopleDialogHtml = function () {
    return toolbarHtml() + '<br><div class="tabgroup tabgroup-people"><div class="tabgroup-bar">' + tabBarHtml() +
        '</div><div class="tabgroup-content" role="tabpanel"><div id="display-people-body">' + setup.peopleBodyHtml() + '</div></div></div>';
};

function showPeople() {
    setup.peopleUi.page = 0;
    Dialog.setup("People", "social");
    jQuery(Dialog.body()).empty().append(setup.peopleDialogHtml());
    Dialog.open();
}
// The sidebar button opens on People Here with a clear search.
setup.peopleOpen = function () {
    setup.peopleUi.tab = 0;
    setup.peopleUi.search = "";
    showPeople();
};
function redrawBody() { jQuery("#display-people-body").empty().append(setup.peopleBodyHtml()); }

// ── View Person (DisplayNPC.txt) ──
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
// <<displaynpctalkto>>: with them, where a Talk row is; greyed when its costs are short, as
// the portrait is; "again" once used today (CoT's $interactionstoday).
function talkOf(slug) {
    if (setup.isRerenderSafe && !setup.isRerenderSafe(State.passage)) return null;
    var loc = here();
    if (!loc || setup.getNpcsAtLocation(loc).indexOf(slug) === -1) return null;
    var pick = (setup.selectNpcPortraitCanvasesForLocation(loc) || {})[slug];
    if (pick) {
        var rec = ((State.variables.game_state || {}).trigger_history || {})[String(pick.id)];
        return { passage: pick.passageName, blocked: false,
                 again: !!(rec && rec.dayKey === setup.getCurrentDayKey() && rec.dayCount > 0) };
    }
    var list = ((setup.help_data || {}).locationCanvases || {})[loc] || [];
    for (var i = 0; i < list.length; i++) {
        var c = list[i];
        if (!c.isRepeatable || (c.triggerMode || "manual") === "random" || c.npcId !== slug || c.hiddenFromLocation) continue;
        if (!setup.isCanvasSelectable(c) || !setup.canTriggerActivity(c.name || c.id, c.maxPerDay)) continue;
        if (c.costs && c.costs.length > 0 && !setup.checkCostsAffordable(c.costs)) return { passage: c.passageName, blocked: true, again: false };
    }
    return null;
}

setup.peopleViewHtml = function (slug) {
    var npc = npcOf(slug) || {}, known = setup.peopleKnown(slug), stranger = info(slug).stranger_name || "";
    var name = npc.name || slug;
    var h = '<div class="npc-display-container"><div class="npc-display-header"><div class="npc-display-header-buttons">' +
        '<button id="view-people-backward" tabindex="0" title="Return to nearby people menu" aria-label="Return to nearby people menu" type="button" role="button">◀</button></div>' +
        '<div class="npc-display-identity"><div class="npc-display-avatar">' + (known ? esc(initials(name)) : "??") + '</div>' +
        '<div class="npc-display-identity-contents">';
    h += known ? '<div class="npc-display-fullname npc-display-fullname-known">' + esc(name) + '</div>'
               : '<div class="npc-display-fullname npc-display-fullname-unknown">???</div>';
    if (known) {
        var subs = [info(slug).role, npc.relationship].filter(Boolean).map(function (s) {
            return '<span class="npc-display-subtitle">' + esc(s) + '</span>';
        });
        if (subs.length) h += '<div class="npc-display-subtitles">' + subs.join(" · ") + '</div>';
    }
    if (stranger) h += '<div class="npc-display-anonname" style="font-style: italic; font-size: 0.85em;">' + aOrAn(stranger) + ' ' + esc(stranger) + '.</div>';
    h += '</div></div>';
    if (known && hasPhoneThread(slug)) {
        h += '<div class="npc-display-infobubble-container"><div class="npc-display-infobubble npc-display-infobubble-contact" title="You have their number and you can call or text them.">' +
            '<span class="npc-display-infobubble-emoji">📱</span> Phone contact</div></div>';
    }
    h += '</div><div class="tabgroup"><div class="tabgroup-bar"><button class="tabgroup-button active" type="button" role="tab" aria-selected="true">' +
        '<span class="tabgroup-button-label">Overview</span></button></div><div class="tabgroup-content" role="tabpanel">';
    if (known) {
        var rows = meterRows(slug);
        if (rows.length) {
            h += '<div class="status-meter-labeled npc-display-status-meters">' + rows.map(function (r) {
                return '<div class="npc-display-status-meter-container"><div class="npc-display-status-meter"><span class="status-meter-label">' +
                    esc(r.label) + '</span><br><br>' + meter(r.pct) + '</div></div>';
            }).join("") + '</div>';
        }
    }
    var talk = talkOf(slug);
    h += '<div class="display-npc-contact-container">';
    if (talk) {
        var who = known ? name : "them";
        var text = (talk.again ? "💭 " : "💬 ") + "Talk to " + who + (talk.again ? " again" : "");
        h += '<div class="display-npc-action-header">Actions</div><span class="display-npc-button">' + (talk.blocked
            ? '<span class="people-talk-blocked">' + esc(text) + '</span>'
            : '<a class="link-internal people-talk" data-passage-to="' + esc(talk.passage) + '">' + esc(text) + '</a>') + '</span>';
    }
    h += '</div>';
    if (known) {
        var id = setup.resolveNpcId(slug);
        if (setup.castHasSchedule && setup.castHasSchedule(slug)) {
            var today = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                .indexOf(State.variables.game_state.time_state.current_day);
            h += '<details class="people-accordion"><summary>Schedule</summary>' + setup.castScheduleHtml(id, today < 0 ? 0 : today) + '</details>';
        }
        var card = setup.pickQuestsCard(slug);
        if (card && card.tip) h += '<div class="people-tip">' + esc(card.tip) + '</div>';
    } else {
        h += "You're not sure who this is.";
    }
    return h + '</div></div></div>';
};

setup.peopleView = function (slug) {
    Dialog.setup("View Person", "view-person");
    jQuery(Dialog.body()).empty().append(setup.peopleViewHtml(slug));
    Dialog.open();
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
$d.on("click", "#view-people-page-backward", function () { setup.peopleUi.page -= 1; redrawBody(); });
$d.on("click", "#view-people-page-forward", function () { setup.peopleUi.page += 1; redrawBody(); });
$d.on("click", "#view-people-backward", function () { showPeople(); });
$d.on("click", ".social .shop-filter-toolbar-header-minrestore a", function () {
    State.variables.showsocialfilter = !State.variables.showsocialfilter;
    jQuery("#social-filter-toolbar-content").replaceWith(toolbarHtml());
});
// A click on the toolbar's bare background folds or opens it too.
$d.on("click", ".social .shop-filter-toolbar", function (ev) {
    if (jQuery(ev.target).is("input, label, select, textarea, .link-internal")) return;
    jQuery(this).find(".shop-filter-toolbar-header-minrestore a").trigger("click");
});
var debounce = null;
$d.on("input", ".social .social-search-input input[type=text]", function () {
    setup.peopleUi.search = jQuery(this).val();
    clearTimeout(debounce);
    debounce = setTimeout(function () { setup.peopleUi.page = 0; redrawBody(); }, 250);
});
function clearSearch() {
    jQuery(".social-search-input input[type=text]").val("");
    setup.peopleUi.search = "";
    setup.peopleUi.page = 0;
    redrawBody();
}
$d.on("click", ".social .people-search-clear", clearSearch);
$d.on("click", ".social .people-clear-filters", clearSearch);
$d.on("click", ".social .people-sort", function () {
    var by = this.getAttribute("data-sort");
    if (by === "relevance") delete State.variables.socialsort;
    else State.variables.socialsort = by;
    setup.peopleUi.page = 0;
    redrawBody();
});
$d.on("click", ".view-person .people-talk", function () {
    var to = this.getAttribute("data-passage-to");
    Dialog.close();
    Engine.play(to);
});
$d.on(":dialogclosed", function () { setup.peopleUi.search = ""; });
})();
"""

_PEOPLE_CSS = """
/* [ui] people_page = "cot": CoT's People and View Person dialogs. */
.social .shop-filter-toolbar { border: 1px solid var(--theme-border, #555); border-radius: 8px; padding: 6px 10px; cursor: pointer; }
.social .shop-filter-toolbar-header { display: flex; justify-content: space-between; align-items: center; }
.social .shop-filter-toolbar-header-minrestore a { font-family: "tme-fa-icons"; text-decoration: none; }
.social .shop-search { display: flex; align-items: center; gap: 6px; margin-top: 8px; cursor: default; }
.social .social-search-input { flex: 1; }
.social .social-search-input input { width: 100%; box-sizing: border-box; }
.social #social-sort a { display: inline-block; margin: 4px 10px 0 0; }
.social .social-sort-relevance { display: inline-block; }
.social .tabgroup-bar, .view-person .tabgroup-bar { display: flex; flex-wrap: wrap; gap: 4px; border-bottom: 1px solid var(--theme-border, #555); }
.social .tabgroup-button, .view-person .tabgroup-button { background: transparent; border: 1px solid transparent; border-bottom: none; border-radius: 6px 6px 0 0; padding: 6px 10px; cursor: pointer; color: inherit; }
.social .tabgroup-button.active, .view-person .tabgroup-button.active { border-color: var(--theme-border, #555); background: rgba(255, 255, 255, 0.06); }
.social .tabgroup-button-emoji { margin-right: 4px; }
.social .tabgroup-content, .view-person .tabgroup-content { padding-top: 10px; }
.social .view-people-title { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.social .view-people-title > div:first-child { flex: 1; }
.social .view-people-page-button-container button, .view-person #view-people-backward { cursor: pointer; padding: 2px 8px; }
.social .view-people-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 8px; }
.social .view-people-person { border: 1px solid var(--theme-border, #555); border-radius: 8px; padding: 8px 10px; cursor: pointer; }
.social .view-people-person-name { font-weight: bold; }
.social .view-people-person-niche { font-size: 0.85em; opacity: 0.7; }
.social .view-people-list-footer, .social .view-people-empty { margin-top: 10px; opacity: 0.8; }
.social .status-meter-labeled, .view-person .status-meter-labeled { display: grid; grid-template-columns: auto 1fr; gap: 2px 8px; align-items: center; margin-top: 6px; font-size: 0.85em; }
.view-person .npc-display-status-meters { display: flex; flex-wrap: wrap; gap: 12px; }
.view-person .npc-display-status-meter-container { flex: 1; min-width: 120px; }
.people-meter { display: inline-block; width: 100%; height: 8px; border-radius: 4px; background: rgba(255, 255, 255, 0.12); overflow: hidden; vertical-align: middle; }
.people-meter-fill { display: block; height: 100%; background: var(--theme-accent, #7ec8e3); }
.view-person .npc-display-identity { display: flex; align-items: center; gap: 12px; margin: 8px 0; }
.view-person .npc-display-avatar { width: 56px; height: 56px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.3em; font-weight: bold; background: rgba(255, 255, 255, 0.12); flex-shrink: 0; }
.view-person .npc-display-fullname { font-size: 1.3em; font-weight: bold; }
.view-person .npc-display-subtitles { font-size: 0.9em; opacity: 0.85; }
.view-person .npc-display-infobubble-container { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 6px; }
.view-person .npc-display-infobubble { border: 1px solid var(--theme-border, #555); border-radius: 12px; padding: 2px 10px; font-size: 0.85em; }
.view-person .display-npc-action-header { font-weight: bold; margin: 12px 0 6px; }
.view-person .display-npc-button { display: inline-block; margin-right: 10px; }
.view-person .people-talk-blocked { opacity: 0.45; }
.view-person .people-accordion { margin-top: 12px; border: 1px solid var(--theme-border, #555); border-radius: 8px; padding: 6px 10px; }
.view-person .people-accordion summary { cursor: pointer; font-weight: bold; }
.view-person .people-tip { margin-top: 10px; }
"""


def people_cot_passages(
    cast_page: dict[str, Any], npc_people: dict[str, dict[str, str]]
) -> str:
    """The cast section under `[ui] people_page = "cot"`: the sidebar button ("People (N)"),
    the dialog's script and styles, and CastPage as a passage (it is an info page)."""
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
    return (
        ":: CastWidgets [widget nobr]\n"
        '<<widget "castButton">>\n'
        '<div id="cast-btn-widget">\n'
        f"  <<set _peopleLabel to setup.peopleButtonLabel()>><<link _peopleLabel>><<run setup.peopleOpen()>><</link>>{icon_span}\n"
        "</div>\n"
        "<</widget>>\n"
        "\n:: PeopleCotScript [script]" + js + "\n"
        ":: PeopleCotStyles [stylesheet]" + _PEOPLE_CSS + "\n"
        ":: CastPage\n"
        "<<nobr>><<run setup.peopleOpen()>><</nobr>>\n"
        '<<link "← Back">><<run setup.smartBack()>><</link>>\n'
    )
