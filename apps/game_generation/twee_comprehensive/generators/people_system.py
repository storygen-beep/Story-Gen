"""Course of Temptation's people system for the v2 engine (2026-11-25): the run-time half.

Emitted only under `[engine.people] system = "cot"` (project.metadata["people_system"],
built by apps/projects/services/people_system.py). Every piece here is either the script
below or a short hook the generator splices into an engine function; with the switch off
each hook is the empty string, so a game without it builds byte for byte as before.

CoT's source, cited by line below:
/Users/a0000/Documents/Process_Review_20260925/round1_evidence/scripts/_cot_js.txt and the
passages under
/Users/a0000/Documents/Player_Legibility_Study_20260825/corpus/course-of-temptation/passages/.

Hooks left for CoT systems this engine does not have (each is one named stub in the
script): romance and trust (read as 0), turn-ons (the lust tipping point's 100..500 spread
and the lust gain multiplier), hygiene (the gain cut to a tenth), likability, reputation
mismatch, exes and partners, and other people's own relationships (Loyal / Cheater).
"""
from __future__ import annotations

import json
from typing import Any

_PEOPLE_SYSTEM_JS = r"""
// ===== [engine.people] system = "cot": CoT's people system =====
setup.people_cfg = %%CFG%%;
(function () {
var C = setup.people_cfg, P = setup.peopleSys = {};
var FEELINGS = ["friendship", "lust", "control"];
// CoT setup.Skills.default_increase and daily_caps, by her current level (_cot_js.txt:83479).
var SKILL_GAIN = [10, 7, 6, 5, 4, 3, 3, 3, 3, 3, 0, 0];
var SKILL_CAP = [30, 21, 18, 15, 12, 9, 9, 9, 9, 9, 0, 0];

function slugOf(who) {
    if (C.npcs[who]) return who;
    var m = setup.npc_slug_map || {};
    for (var s in m) { if (m[s] === who) return s; }
    return String(who);
}
function npcOf(who) {
    return (State.variables.npcs || {})[String(setup.resolveNpcId(slugOf(who)))] || null;
}
function today() {
    var gs = State.variables.game_state || {};
    return (gs.time_state && gs.time_state.day) || 0;
}
function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
        .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
P.slug = slugOf;

// ── feelings, traits ──
P.feeling = function (who, key) {
    var n = npcOf(who);
    return Number(n && n.core_traits && n.core_traits[key]) || 0;
};
P.hasTrait = function (who, name) {
    var c = C.npcs[slugOf(who)];
    return !!c && c.traits.indexOf(name) !== -1;
};
// CoT has_any_inclination(name, set): one of their traits stands in the set.
P.hasAny = function (who, set) {
    var c = C.npcs[slugOf(who)];
    return !!c && c.traits.some(function (t) { return ((C.traits[t] || {}).sets || []).indexOf(set) !== -1; });
};
// CoT is_sexpartner reads the sex memory; here it is the flag sex_partner_<npc id>.
P.isSexPartner = function (who) {
    return (State.variables.flags || {})["sex_partner_" + slugOf(who)] === true;
};
// CoT professor_intimacy (_cot_js.txt:117980): 2 once a sex partner, else the stored 0/1/2.
P.intimacy = function (who) {
    return P.isSexPartner(who) ? 2 : P.feeling(who, "intimacy");
};
// CoT desired_relationship's lusttippoint (_cot_js.txt:114822-114836).
P.tippingPoint = function (who) {
    var c = C.npcs[slugOf(who)] || {};
    var tip = 300;  // HOOK turn-ons: CoT sets 100/200/400/500 by npc_turnon_factor
    if (c.gender === "female") tip += 100;
    if (P.hasAny(who, "slut")) tip -= 200;
    if (P.hasTrait(who, "Chaste")) tip += 800;
    return tip;
};

// ── what they want from her: CoT desired_relationship (_cot_js.txt:114752-115010) ──
P.want = function (who) {
    var slug = slugOf(who), c = C.npcs[slug];
    if (!c) return "indifferent";
    if (c.want) return c.want;  // CoT pdata["desired relationship"]
    var friendship = P.feeling(slug, "friendship"), lust = P.feeling(slug, "lust");
    var attracted = !!c.attracted;
    var faculty = !!(c.faculty || c.professor);
    // HOOKS, each a CoT system this engine does not have yet.
    var romance = P.feeling(slug, "romance");  // 0 until a romance feeling exists
    var mistrusts = false;                     // trust <= -200
    var repOk = true;                          // reputation_mismatch
    var dates = false;                         // is_dating
    var free = true;                           // !inotherrelationship || mightcheat (Loyal, Cheater)
    var single = true;                         // !inotherrelationship
    if (c.professor) {
        if (!attracted) return "indifferent";
        if (P.intimacy(slug) >= 2) return romance > lust ? "date" : "fuckbuddy";
        return "indifferent";
    }
    var masc = c.gender === "male", femme = c.gender === "female";
    var young = !(Number(c.age) >= 35);
    var sexpartner = P.isSexPartner(slug);
    var tip = P.tippingPoint(slug);
    var chaste = P.hasTrait(slug, "Chaste"), asexual = P.hasTrait(slug, "Asexual");
    var casualsex = P.hasAny(slug, "casualsex"), active = P.hasAny(slug, "active");
    var dominant = P.hasAny(slug, "dominant"), forceful = P.hasAny(slug, "forceful");
    var datespeople = !faculty && !P.hasAny(slug, "nodating");

    if (romance > 0 && romance > lust && dates && single && repOk && !mistrusts && attracted) return "date";
    if (romance >= 100 && young && single && attracted) {
        if (datespeople && romance > lust && repOk && !mistrusts) return "date";
        if (casualsex && lust > romance) return "fuckbuddy";
        return datespeople ? "date" : "friend";
    }
    if (romance >= 400 && datespeople && single && repOk && !mistrusts && attracted) {
        return (casualsex && lust > romance) ? "fuckbuddy" : "date";
    }
    if (lust >= tip || (lust > 0 && sexpartner)) {
        if (friendship <= -100) {
            if (!asexual && masc && (active || casualsex) && !chaste && free) return "hatefuck";
            if (!asexual && femme && (dominant || casualsex) && !chaste && free) return "hatefuck";
            return faculty ? "indifferent" : "rival";
        }
        if (!asexual && friendship >= 100 && free && active && !chaste) return "fuckbuddy";
        if (friendship >= 100 && young && single) {
            if (datespeople && romance > lust && repOk && !mistrusts && attracted) return "date";
            if (casualsex && lust > romance) return "fuckbuddy";
            if (!datespeople) return "friend";
            return (repOk && !mistrusts && attracted) ? "date" : "friend";
        }
        if (!asexual && masc && forceful && free) return "hatefuck";
        return friendship >= 100 ? "friend" : "indifferent";
    }
    if (friendship >= 200) {
        return (!asexual && attracted && free && (active || casualsex) && !chaste) ? "fuckbuddy" : "friend";
    }
    if (friendship <= -100) {
        if (attracted && !asexual && free && !chaste && ((masc && active) || (femme && dominant) || casualsex)) return "hatefuck";
        return faculty ? "indifferent" : "rival";
    }
    // HOOK likability and turn-ons: CoT's last three branches read likability_factor and
    // npc_turnon_factor; with neither system the answer is its final "indifferent".
    return "indifferent";
};

// ── which fixed traits she knows: CoT filter_known_traits (_cot_js.txt:117394-117420) ──
P.shownTraits = function (who) {
    var c = C.npcs[slugOf(who)];
    return c ? c.traits.filter(function (t) { return C.traits[t] && !C.traits[t].hidden; }) : [];
};
P.traitKnown = function (who, name) {
    var t = C.traits[name];
    if (!t || t.hidden) return false;
    var score = 0;
    if (t.kind === "personality") {
        var f = P.feeling(who, "friendship");
        score = Math.max(f, -2 * f, P.feeling(who, "romance"));
    } else if (t.kind === "sex" && P.isSexPartner(who)) {
        score = P.feeling(who, "lust");
    }
    return score > t.threshold;
};
P.knownTraits = function (who) {
    return P.shownTraits(who).filter(function (t) { return P.traitKnown(who, t); });
};

// ── effects: CoT alter_attitude (_cot_js.txt:113265-113315) ──
// A lust gain on a person who is not attracted to her is dropped.
// HOOK hygiene (a gain cut to a tenth) and turn-ons (a lust gain scaled) would sit here.
P.dropEffect = function (targetType, npcId, key, op, value) {
    if (targetType !== "npc" || key !== "lust" || op !== "add" || !(value > 0)) return false;
    var c = C.npcs[slugOf(npcId)];
    return !!c && !c.attracted;
};
// The value a people-system number settles at, or null for any other trait: a feeling in
// -1000..1000, a professor's intimacy 0..2, one of her skills a whole number in 0..1000.
P.settle = function (targetType, key, next) {
    var lo, hi;
    if (targetType === "npc" && FEELINGS.indexOf(key) !== -1) { lo = -1000; hi = 1000; }
    else if (targetType === "npc" && key === "intimacy") { lo = 0; hi = 2; }
    else if (targetType === "player" && C.skills[key]) { lo = 0; hi = 1000; next = Math.round(next); }
    else return null;
    return Math.max(lo, Math.min(hi, next));
};
// "Seen": CoT stamps lastInteraction whenever a feeling is altered. A scene with the
// person refreshes that day too, but only a feeling change starts the clock.
P.touched = function (targetType, npcId, key) {
    if (targetType !== "npc" || FEELINGS.indexOf(key) === -1) return;
    var n = npcOf(npcId);
    if (n) n.people_seen = today();
};
P.sceneWith = function (npcUuid) {
    var n = (State.variables.npcs || {})[String(npcUuid)];
    if (n && typeof n.people_seen === "number") n.people_seen = today();
};
// CoT decay_attitudes + attitude_to_mean (_cot_js.txt:113317-113383), once a day: a person
// not seen for more than 14 days moves 10 toward +100 or -100 and stops there. Friendship
// and lust only; control never fades. A value inside -100..100 never moves.
P.fadeDay = function () {
    if (!C.fade) return;
    var now = today();
    Object.keys(C.npcs).forEach(function (slug) {
        var n = npcOf(slug);
        if (!n || !n.core_traits || typeof n.people_seen !== "number" || !(now - n.people_seen > 14)) return;
        ["friendship", "lust"].forEach(function (key) {
            var v = Number(n.core_traits[key]) || 0;
            if (v > 100) n.core_traits[key] = Math.max(v - 10, 100);
            else if (v < -100) n.core_traits[key] = Math.min(v + 10, -100);
        });
    });
};

// ── her skills: CoT skill_level, skillleveled, raise_skill (_cot_js.txt:96720-96790) ──
P.isSkill = function (key) { return !!C.skills[key]; };
P.skillLevel = function (key) {
    var v = Number(((State.variables.player || {}).core_traits || {})[key]) || 0;
    return Math.floor(Math.max(0, Math.min(1000, v)) / 100);
};
// A level-1 gate always passes ("otherwise it's very hard to level some things through use").
P.skillLeveled = function (key, level) { return level <= P.skillLevel(key) || level === 1; };
// What passing a gate of `gate` adds, before the daily cap: the gain for her level, cut
// when the gate is far from her level.
P.skillGain = function (key, gate) {
    var lvl = P.skillLevel(key), amount = SKILL_GAIN[lvl] || 0, over = lvl - Number(gate);
    if (over >= 3) amount /= 3;
    else if (over <= -3) amount /= 4;
    else if (over === 2) amount /= 2.5;
    else if (over === 1 && lvl > 1) amount /= 1.5;
    else if (over === -1) amount /= 2;
    else if (over === -2) amount /= 3;
    return amount;
};
// The daily cap for her level, shared by every gain of that skill today. Returns what is added.
P.skillAllow = function (key, val) {
    if (!C.skills[key] || !(val > 0)) return val;
    var cap = SKILL_CAP[P.skillLevel(key)] || 0;
    var gs = State.variables.game_state = State.variables.game_state || {};
    var log = gs.skill_raised = gs.skill_raised || {};
    if (!log[key] || log[key].day !== today()) log[key] = { day: today(), used: 0 };
    var take = Math.min(val, cap, Math.max(0, cap - log[key].used));
    log[key].used += take;
    return take;
};
// The sidebar's number: a skill reads as its level, anything else as it is.
P.shownValue = function (key) {
    return C.skills[key] ? P.skillLevel(key) : ((State.variables.player || {}).core_traits || {})[key];
};

// ── conditions: npc_wants, npc_has_trait, skill_level ──
P.isCondition = function (type) { return type === "npc_wants" || type === "npc_has_trait" || type === "skill_level"; };
P.checkCondition = function (it) {
    if (it.type === "skill_level") return P.skillLeveled(it.skill, Number(it.level));
    var ok = false;
    if (it.type === "npc_wants") {
        var w = P.want(it.npc_id);
        ok = Array.isArray(it.any_of) ? it.any_of.indexOf(w) !== -1 : w === it.value;
    } else if (it.type === "npc_has_trait") {
        ok = it.set ? P.hasAny(it.npc_id, it.set) : P.hasTrait(it.npc_id, it.trait);
    }
    return it.operator === "is_false" ? !ok : ok;
};

// ── the People view (DisplayNPCWidgets.txt:413-565 the meters, 585-609 the traits) ──
function pct(v) { return Math.max(0, Math.min(100, v / 10)); }
// Friendship, or "Dislike" when negative; Lust; and their Dominance (control above 0) or
// Submission, shown as CoT shows it: from 100 either way, or from the first point for a
// person with a dominant or submissive trait. "Attracted" is never shown. The page's other
// show_traits rows follow.
P.meterRows = function (slug, rest) {
    var f = P.feeling(slug, "friendship"), l = P.feeling(slug, "lust"), c = P.feeling(slug, "control");
    var rows = [{ label: f < 0 ? "Dislike" : "Friendship", value: f, pct: pct(Math.abs(f)) },
                { label: "Lust", value: l, pct: pct(l) }];
    if (Math.abs(c) >= 100 || ((P.hasAny(slug, "submissive") || P.hasAny(slug, "dominant")) && Math.abs(c) > 0)) {
        var g = (C.npcs[slug] || {}).gender;
        rows.push({ label: (g === "male" ? "His" : g === "female" ? "Her" : "Their") + (c < 0 ? " Submission" : " Dominance"),
                    value: c, pct: pct(Math.abs(c)) });
    }
    var names = FEELINGS.map(function (k) { return setup.traitLabel ? setup.traitLabel(k) : k; });
    return rows.concat((rest || []).filter(function (r) { return names.indexOf(r.label) === -1; }));
};
// CoT works the want out and never prints it; scenes read it through `npc_wants`. The dialog shows
// no want line (LO 2026-11-25: "Remove the ... want line").
function bubble(label, cls, tip) {
    return '<div class="npc-display-infobubble ' + cls + '" title="' + esc(tip) + '">' + esc(label) + '</div>';
}
// The Personality block: a bubble per known trait, then "???" for each one not yet known;
// nothing at all until the first is known (CoT).
P.viewHtml = function (slug) {
    var h = "", shown = P.shownTraits(slug), known = P.knownTraits(slug);
    if (known.length > 0) {
        h += '<div class="personality-traits-container"><div class="display-npc-personalty-traits-header">Personality</div>' +
            '<div class="npc-display-infobubble-container">';
        known.forEach(function (t) {
            h += bubble(t, C.traits[t].kind === "sex" ? "known-trait-sexy" : "known-trait-personality", C.traits[t].description);
        });
        for (var i = 0; i < shown.length - known.length; i++) h += bubble("???", "unknown-trait", "This trait is unknown.");
        h += '</div></div>';
    }
    return h;
};
})();
"""

# ── hooks spliced into engine functions (generators/v2.py) ───────────────────────────────
# v2's script is one f-string; these are plain strings returned by a helper, so they carry
# single braces.

# applyTraitEffect, before the operation: a dropped effect changes nothing.
HOOK_DROP = """
    // [engine.people] — a lust gain on a person who is not attracted is dropped.
    if (setup.peopleSys.dropEffect(targetType, npcId, key, op, value)) return;
"""

# applyTraitEffect, before the 0-100 clamp: a people-system number has its own range.
HOOK_SETTLE = """
    // [engine.people] — a feeling, an intimacy or a skill keeps its own range.
    var _peopleValue = setup.peopleSys.settle(targetType, key, next);
    if (_peopleValue !== null) { next = _peopleValue; clampFlag = false; }
"""

# applyTraitEffect, after the write: a feeling change is "seen today".
HOOK_TOUCHED = """
    setup.peopleSys.touched(targetType, npcId, key);  // [engine.people] — seen today
"""

# applyAndNotifyTrait, after [engine.daily_caps]: her skill's daily cap.
HOOK_SKILL_CAP = """
  // [engine.people] — a skill rises under CoT's daily cap for her level.
  if (targetType === 'player' && (op || 'add') === 'add' && setup.peopleSys.isSkill(trait) && Number(val) > 0) {
    val = setup.peopleSys.skillAllow(trait, Number(val));
    if (!(val > 0)) return;
  }
"""

# markCanvasTriggered, where a canvas's NPC is marked as met today.
HOOK_SCENE = """
            setup.peopleSys.sceneWith(npcUuid);  // [engine.people] — a scene with them"""

# advanceDay, at the end of the day roll.
HOOK_DAY = """
    // [engine.people] — people not seen for 14 days cool toward +100 / -100.
    setup.peopleSys.fadeDay();
"""

# triggerConditionsSatisfied, among the item types.
HOOK_CONDITION = """
            // [engine.people] — npc_wants, npc_has_trait, skill_level.
            if (setup.peopleSys.isCondition(type)) {
                results.push(setup.peopleSys.checkCondition(it));
                continue;
            }
"""

# checkSingleCondition (the second evaluator): the same answer as the first.
HOOK_SINGLE_CONDITION = """
    // [engine.people] — one implementation, the people system's.
    if (item && setup.peopleSys.isCondition(item.type)) return setup.peopleSys.checkCondition(item);
"""

# The sidebar's trait dump prints a skill as its level.
SIDEBAR_VALUE = "<<print $player.core_traits[_k]>>"
SIDEBAR_VALUE_PEOPLE = "<<print setup.peopleSys.shownValue(_k)>>"


def people_system_js(cfg: dict[str, Any]) -> str:
    """The script, with the resolved config spliced in as JSON."""
    return _PEOPLE_SYSTEM_JS.replace(
        "%%CFG%%", json.dumps(cfg, ensure_ascii=False, sort_keys=True)
    )


def skill_gain_js(value: dict[str, Any]) -> str:
    """The JS expression for a `skill_gate` effect value ({type: "skill_gain", skill, level})."""
    return f"setup.peopleSys.skillGain({json.dumps(str(value['skill']))}, {int(value['level'])})"


# ── the People view ([ui] people_page = "cot", generators/cot_pages.py) ──────────────────

_VIEW_METERS_OLD = (
    "return setup.castTraitRows ? setup.castTraitRows(slug, npcOf(slug)) : [];"
)
_VIEW_METERS_NEW = "return setup.peopleSys.meterRows(slug, setup.castTraitRows ? setup.castTraitRows(slug, npcOf(slug)) : []);"
_VIEW_TALK_OLD = "    var talk = talkOf(slug);\n"
_VIEW_TALK_NEW = (
    "    if (known) h += setup.peopleSys.viewHtml(slug);\n" + _VIEW_TALK_OLD
)

PEOPLE_VIEW_CSS = """
/* [engine.people] system = "cot": the Personality bubbles and the want line. */
.view-person .personality-traits-container { margin-top: 10px; }
.view-person .display-npc-personalty-traits-header { font-weight: bold; margin-bottom: 6px; }
.view-person .unknown-trait { opacity: 0.55; }
"""


def people_view_js(js: str) -> str:
    """CoT's People dialog script with the people system's meters, traits and want in it.
    Each splice names the exact line it replaces, so an edit to the dialog that moves one
    fails the build here instead of silently dropping the feature."""
    for old in (_VIEW_METERS_OLD, _VIEW_TALK_OLD):
        if js.count(old) != 1:
            raise ValueError(
                f"people_system: the People dialog no longer has the line {old!r}"
            )
    return js.replace(_VIEW_METERS_OLD, _VIEW_METERS_NEW).replace(
        _VIEW_TALK_OLD, _VIEW_TALK_NEW
    )
