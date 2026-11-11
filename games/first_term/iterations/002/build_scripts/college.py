"""College (sheets/systems/college.md, scenes college_*.md): the four classes, the guy beside her,
the dress-code warning, the midterms, the office hubs, the dean, Laura reading the grades.
Explicit screens pasted as signed."""
from canv import *
from tomlw import tod, wd

H, N = "npc_hale", "npc_nadia"
ART, BUS, TA, DEAN = "npc_art_lecturer", "npc_business_lecturer", "npc_bio_ta", "npc_dean"
DESK, RIVAL, STUDY, COCKY, MODEL = "npc_desk_guy", "npc_rival", "npc_study_guy", "npc_cocky_guy", "npc_figure_model"
Z, L = "npc_zoe", "npc_laura"
out = []
cards = []

from classes import sched, PSYCH, BUSI, BIO, FIG, LATE_MINUTES   # one source with the timetable screen


def at_start(rows, mins=15):
    """The first quarter-hour of each class slot (iteration 002, part 8, reader): a canvas that opens a
    class, or spends the class, fires only while the class is starting, never in its last minute."""
    def plus(t):
        h, m = map(int, t.split(":")); m += mins
        return f"{h + m // 60:02d}:{m % 60:02d}"
    return [dict(r, end_time=plus(r["start_time"])) for r in rows]
HUNGRY = trait("corruption", "gte", 60)
WATCHED = trait("exhibitionism", "gte", 60)
DARING_STATE = cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"},
                    {"type": "worn_type", "operator": "eq", "value": "short_skirt"}, logic="OR")
CAP_BOLD = 59
# A Daring act (Exhibitionism 20) stops paying at the top of Daring, so repeating it cannot carry her through Showing
# (the-arc.md A4 and "Each act pays only inside its own stage"; pass 3 G8, G13).
CAP_DARING = 39
# The two clothing sets DARING_STATE and the risky buttons cover (copy fixes B, DECISIONS 125): a line that
# names her body has to be true for the set on screen, so it splits into one group per set. They never overlap.
BRALESS = {"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}
SKIRT_WITH_BRA = [{"type": "clothing_slot", "slot": "bra", "operator": "equipped"},
                  {"type": "worn_type", "operator": "eq", "value": "short_skirt"}]

def by_clothes(braless_blocks, skirt_blocks, *after):
    """The risky screen's text: one group for braless, one for skirt-with-a-bra, then the lines true for both."""
    return [G(cond(BRALESS), *braless_blocks), G(cond(*SKIRT_WITH_BRA), *skirt_blocks), *after]

# Each class its own lines (iteration 002, part 4: sweep A5-09, A5-15; gate one pool, one place).
POOLS = {
    "psych": {
        "focus": ["You take notes on attachment theory until your hand cramps. Somewhere in the second half it clicks, and you feel smart. That part is new.",
                  "Dr. Hale walks through a case study, a man who couldn't feel fear. You write down every word of it, and you understand all of it."],
        "chat": ["Nadia whispers through the lecture: who's seeing who, which TA cries in the parking lot. You learn nothing about psychology.",
                 "You and Nadia pass notes in the margin of her reader. By the end the margin's full and the slides are a blur."],
        "doze": ["You sink down in your seat and let Dr. Hale's voice turn into a warm hum. You wake when the room starts packing up.",
                 "Your eyes close somewhere around the third slide. Nadia nudges you awake for the last five minutes."],
        "eyes": "In the front row you can feel the whole room behind you. What you're wearing is doing its job.",
        "tired": "Too tired to take in a word of Psychology. Doze, or skip."},
    "business": {
        "focus": ["Supply, demand, a case about a shoe company that went bust. You fill two pages and could argue it either way.",
                  "The gray man talks in bullet points, and you write them all down. It's dull, but it's on the exam."],
        "chat": ["The guy in the row behind leans forward to whisper answers before the lecturer asks the questions. You learn more about him than about markets.",
                 "You whisper about Friday with the girl beside you until the lecturer says your name, flat, without looking up."],
        "doze": ["You prop your chin on your hand and drift. The lecturer's voice never changes pitch, which makes it easy.",
                 "Margins and percentages, slide after slide. You nod off twice, and you catch yourself both times."],
        "eyes": "You can feel the study guy's eyes on the back of your neck. What you're wearing is doing its job.",
        "tired": "Too tired for margins and percentages. Doze, or skip."},
    "bio": {
        "focus": ["Cells, then more cells. You label the diagram until it makes sense, and by the end it does.",
                  "The TA goes through the heart valve by valve, pink to the ears. You take careful notes and understand all of it."],
        "chat": ["You whisper with the girl beside you through the slides, about everything but biology.",
                 "The back row passes a phone along with somebody's party photos on it. You look at every one."],
        "doze": ["The hall is warm and the TA's voice is soft. You put your head on the desk and lose twenty minutes.",
                 "You sit with your eyes half shut while the slides click past. Your body thanks you, but your notes don't."],
        "eyes": "From the front of the hall, the TA keeps looking and looking away. What you're wearing is doing its job.",
        "tired": "Too tired to label a single cell. Doze, or skip."},
    "figure": {
        "focus": ["You draw without looking up until the lecturer calls time. By the end your page holds her shoulder, her hip, the line of her back, and it looks like a person.",
                  "You fill three sheets with fast, loose sketches. The last one is good, and you know it is."],
        "chat": ["You draw with one hand and whisper with the girl at the next easel. Your drawing is mostly elbows.",
                 "Charcoal on your fingers, you talk through the pose about everything but the model. The lecturer clears her throat at you twice."],
        "doze": ["The lamp is warm and the room is quiet except for charcoal on paper. You stop drawing and let your eyes close.",
                 "You sit back from the easel and let the room go soft. Your page stays half a shoulder."],
        # reader a3 #25-26 (DECISIONS 131): one watcher at Exhibitionism 20, not a room of easels (H1: a group is stage 4)
        "eyes": "The guy at the next easel has stopped drawing the model. His stare crawls over you, and your nipples go tight.",
        "tired": "Too tired to hold the charcoal straight. Doze, or skip."},
}

# The meet_* canvases are each class's one-time first sitting, so their seat has its own words (gate one pool, one
# place, writing pass 2026-11-04). "First class" only: the canvas waits for her first visit, whatever week that is.
FIRST_POOLS = {
    "business": {
        "focus": ["The gray man is on the definition of profit and doesn't stop. You copy the course outline, the grading scheme and every heading. By the end you know how this class works.",
                  "The gray man hands out the reading list and tells you which three chapters the exam comes from. You underline all three, twice, and you feel ahead of the whole row."],
        "chat": ["The guy with the highlighters whispers the whole course to you: which cases come back on the exam, which week is the killer, who got thrown out last year. You don't write down a word.",
                 "You lean over and ask the girl beside you if he's always like this. She says yes without moving her lips, and she tells you who to sit away from until the gray man stops talking and waits."],
        "doze": ["One slide says Introduction. The next says Introduction, continued. You rest your head on your fist, and you're gone by the third.",
                 "You meant to stay awake for your first class in here. The gray voice doesn't rise or fall once, and your eyes stay shut until chairs start scraping."],
        "eyes": "The guy with the highlighters is leaning forward to look down your back. You didn't dress for a gray room like this, and it shows.",
        "tired": "Your first Business class, and you're too tired to follow one slide of it. Doze, or skip."},
    "bio": {
        "focus": ["The TA goes slowly, one cell on one slide. You draw it, label the parts and copy down what's on the midterm. It's easier than you expected, and you're pleased.",
                  "The TA walks you all through the syllabus, apologizing for it. You read every line and write your name at the top before anyone else does."],
        "chat": ["The girl beside you tells you which seats the TA can't see from and which ones she stares at. It's more useful than the syllabus, and you don't hear a word of the syllabus.",
                 "Somebody passes up a drawing of a skeleton in a party hat, and you have to ask why. You spend the next twenty minutes hearing about the TA's office."],
        "doze": ["The lights go down for the slides, and that's the end of you. You surface at the finish with a stripe of desk on your cheek.",
                 "You put your bag under your head for one minute. The TA's soft voice goes on about membranes, and the minute lasts until the end of class."],
        "eyes": "The TA hasn't learned one name yet, but her eyes keep coming back to you and jumping off again.",
        "eyes_bold": "You dressed to be noticed, and she noticed.",
        "eyes_plain": "You look down at the syllabus with your ears burning, and you wish you'd picked something else to wear.",
        "tired": "Your first Biology class, and the diagrams swim the moment you look at them. Doze, or skip."},
    "figure": {
        "focus": ["Your first class at an easel. Your first drawing looks like a potato with arms. The lecturer says nothing and moves your hand an inch, and by the last pose your drawing has a spine.",
                  "The lecturer calls ten poses at two minutes each, so there's no time to be embarrassed. You stop seeing a naked woman and start seeing weight. Your last sketch stands up by itself."],
        "chat": ["You ask the girl on your other side if this gets less weird. She says no, that's the point, and she spends the rest of the pose telling you who's asked the model out. You draw one knee.",
                 "You whisper through the pose about how long the model has to sit like that. The lecturer taps your worst sketch with one black finger, and you whisper quieter."],
        "doze": ["You've got a stool, a warm lamp across the room and two bad sketches on your page. You rest your head against the easel, and the scratching of charcoal puts you out.",
                 "You meant to rest your eyes through one pose. When you open them the model has moved twice, and your two sketches don't match anything on the stool."],
        "eyes": None,   # cut (reader 2026-11-05): needed cocky_guy_met false, but the button into this screen sets it; his pad line has him here
        "eyes_bold": "You're not sorry about what you wore.",
        "eyes_plain": "You pull your arms in and keep your eyes on your page. You should have worn something else.",
        "tired": "You can barely lift your arm to the paper, and the charcoal slides around in your fingers. Doze, or skip."},
}

# pass 3 A57 (the-heat-ladder.md H4, "her line changes with her level"): her own thought on the risky screen reads her
# Exhibitionism stage. The button opens at 20, so the bands are Daring 20-39, Showing 40-59, Bold 60+, mutually
# exclusive (adjacent groups merge into one chain). Every risky_text ends on a plain block, so this chain stands alone.
def her_bands(daring, showing, bold):
    return [
        G(cond(trait("exhibitionism", "lt", 40)), T(daring)),
        G(cond(trait("exhibitionism", "gte", 40), trait("exhibitionism", "lt", 60)), T(showing)),
        G(cond(trait("exhibitionism", "gte", 60)), T(bold)),
    ]


# Each class, and each first class, its own thought (gate one pool, one place).
RISKY_HER_LINE = {
    "psych": her_bands("Your face burns. Anyone watching could tell you did that on purpose, and your nipples are hard anyway.",
                       "You liked that. You'll do it again next class, and give them a little more.",
                       "That was nothing. You want to be looked at properly, tits and all, and soon."),
    "business": her_bands("In a room this dull, you just did that on purpose. You wonder if he can see how hard your nipples are.",
                          "Better than any case study. Next lecture you'll stretch longer, and make him drop the highlighter.",
                          "One row of highlighters isn't enough. You want the whole front half of this room staring at your tits."),
    "bio": her_bands("Your neck is as pink as hers now. You wonder if she can tell your nipples are hard from up there.",
                     "You like making her drop that pen. Next class you'll see if you can make her lose her slide.",
                     "Forget the pen. You want her to stop the class and look at your tits with the whole hall watching."),
    "figure": her_bands("The model gets paid to sit there. You're doing it free, and you wonder what he's drawn. Your nipples are tight.",
                        "You liked being the one on his page. Next class, give him something harder to draw.",
                        "A sketch isn't enough. You want to be up on that platform with your tits out, and every easel on you."),
    "first_business": her_bands("First class in this room, and you already did that on purpose. You wonder what he makes of you. Your nipples don't mind.",
                                "Not bad for a first lecture. He knows your face now, and you'll make sure he remembers the rest.",
                                "One row is a start. You want every guy in this gray room to know your tits by the end of term."),
    "first_bio": her_bands("One class, and you've already made the TA lose her slide. You wonder why that makes your nipples go hard.",
                           "She blushes at the word reproductive. You liked that, and next class you'll make her say it to your face.",
                           "She told the room her door's open. You want her to shut it and look at your tits properly."),
    "first_figure": her_bands("First class, and he's looking at you, not the naked woman on the stool. You wonder why your nipples like that.",
                              "Your first class, and he's already given up on her for you. Sit closer next class and see how far that goes.",
                              "She gets the lamp and the whole horseshoe. You want that. You want your tits up there under that lamp."),
}

# pass 3 B3/B4: on the risky screen somebody in the room says it out loud, beside her thought (strangers: WHO)
RISKY_SAID = {
    "Psychology": [WHO("Jesus. Are you doing that on purpose?"), ME("Doing what?"), WHO("That. You know what. Do it again.")],
    "Business": [WHO("Do that one more time and I'm failing this class."), ME("So fail it."), WHO("Fuck. Okay. Worth it.")],
    # reader batch 5 (pass 3): no lab coat of hers exists, so the line names what the room can see
    # writing pass 2026-11-04, reader test 12 (H4.3): the price said out loud, by the one person who could report it
    "Biology": [WHO("Hey. You know the whole row can see, right? All of it."), ME("I know."), WHO("Right. Cool. I'll just. Keep looking, then."),
                P("When the room packs up she comes down to the second row hugging her clipboard. She looks at your mouth so she won't look anywhere else."),
                D(TA, "Not in my class, @player. Please. If someone reports it, I have to put my name on it.")],
    "Figure drawing": [WHO("I'm supposed to be drawing her. I've drawn you three times."), ME("Then draw me properly."), WHO("Hold still, then. Don't move. God, don't move."),
                       ME("Like this?"), WHO("Exactly like that. Keep your legs exactly like that.")],
}
# The first sitting of each class says it differently (the first class has its own room to read).
FIRST_SAID = {
    "business": [WHO("You're new in here, right? Do you always sit like that?"), ME("Only when it's boring."), WHO("It's always boring. Please keep sitting like that."),
                 P("When the room packs up, the guy with the highlighters catches you at the end of the row. He goes red, and he can't get his eyes any higher than your chest."),
                 D(STUDY, "You're going to get me thrown out of his class. Not in here, okay? Not where he can see. Are you sitting there next time?")],
    "bio": [WHO("New? Just so you know, the whole row can see. Everything."), ME("Good."), WHO("Okay. Welcome to Biology, I guess."),
            P("She waits until you're packing up, then comes down to the second row and talks to your collarbone."),
            D(TA, "It's only your first class. Not in here. Please. If anyone complains, I'm the one who has to write it up.")],
    "figure": [D(COCKY, "First class, and I've wrecked my drawing of her. That's you on the page now."), ME("Is it any good?"),
               D(COCKY, "It will be. Keep leaning like that. Don't you dare move.")],
}

def eyes_blocks(pools):
    """The room's look on the Daring-clothes line. A first class splits her own sentence by Exhibitionism 20
    (scene reader 2026-11-04): under Daring she didn't dress for this on purpose."""
    if "eyes_bold" not in pools:
        return [P(pools["eyes"])]
    look = [P(pools["eyes"])] if pools["eyes"] else []
    return [*look,
            GC(cond(trait("exhibitionism", "gte", 20)), P(pools["eyes_bold"])),
            GC(cond(trait("exhibitionism", "lt", 20)), P(pools["eyes_plain"]))]


# everyday clothes by stage (DECISIONS 205): the room sees each piece, one line, before her choice
def _wt(t, op="eq"):
    return {"type": "worn_type", "operator": op, "value": t}


CLASS_CLOTHES = {   # two classes, so each line lives on one screen (gate `one pool, one place`)
    "college_class_psych": [
        G(cond(_wt("crop_top")), P("Front row, in the crop top, your belly's bare from the hem to your waistband. Every time you reach down for your pen, the guy in the row behind leans forward to see how far it rides up.")),
        G(cond(_wt("bodycon_dress")), P("In the front-row seat the bodycon dress is halfway up your thighs, but you can't tug it down without the whole row seeing you do it. The guy behind you has stopped writing.")),
        G(cond(_wt("micro_shorts")), P("Front row, in the micro shorts, your bare thighs right up to the crease of your ass on the seat. Every time you shift, the guy in the row behind looks down the back of them.")),
        G(cond(_wt("plunge_dress"), BRALESS), P("The plunge dress is open to your navel, nothing under it, right in front of the lectern. Every time you lean to write, the neckline gapes off your bare tits, and Dr. Hale stares at the back wall for a long time.")),
        # more clothes, round 2 (DECISIONS 208)
        G(cond(_wt("split_skirt")), P("You cross your legs in the front row and the slit in your skirt falls open off your thigh, your whole bare leg out to the hip. The guy in the row behind has stopped pretending to read the slides.")),
        G(cond(_wt("sequin_dress")), P("In the front row the sequin dress catches the projector light every time you breathe. The guy at the end of your row has leaned forward to watch your tits sparkle instead of the slides, but you can't do a thing about it without him seeing.")),
        G(cond(_wt("backless_dress"), BRALESS), P("The backless dress leaves you bare to the base of your spine in the front row. The guy behind you can see there's no bra, no strap, nothing, and when you lean to write he can see the side of your bare tit.")),
    ],
    "college_class_figure": [
        G(cond(_wt("crop_top")), P("Every time you reach up to the top of the paper, the crop top rides up your belly. The guy at the next easel is drawing your waist, not the model's.")),
        G(cond(_wt("bodycon_dress")), P("On the stool the bodycon dress rides up your thighs, but you need both hands for the charcoal. The guy at the next easel isn't drawing the model any more.")),
        G(cond(_wt("micro_shorts")), P("On the stool in the micro shorts, your bare cheeks spread on the seat. The guy at the next easel has turned his board a quarter toward you.")),
        G(cond(_wt("plunge_dress"), BRALESS), P("The plunge dress gapes every time you lean in to the paper, your bare tits loose inside it. The guy at the next easel keeps losing his line.")),
        G(cond(_wt("split_skirt")), P("On the stool the split skirt falls open to the hip on the easel side, your bare leg out, and the guy at the next easel has started drawing it instead of the model.")),
        G(cond(_wt("sequin_dress")), P("The sequin dress throws little lights all over the next easel every time you move your arm. The guy behind it has given up on the model and is drawing the dress, and what's in it.")),
        G(cond(_wt("backless_dress"), BRALESS), P("Every time you reach for the top of the paper, the open side of the backless dress shows the curve of your bare tit. The guy at the next easel has drawn the same line four times.")),
    ],
}


def class_row(cid, name, subj, grade, schedules, lecturer, meet_flags, opening, beside, risky_label, risky_text, extra_blocks=(),
              pools=None, chat_beside=None, her_line=(), said=None, risky_floor=20, risky_cap=CAP_DARING, risky_eff=(), mild=None,
              covered=None):
    """One class visit (the college sheet's rows): Focus · Chat · Doze · Skip · the risky slot.
    No button for a stage this release does not write (LO 2026-11-03: "dont even show the option").
    Once per class window.
    LO, 2026-11-04 (the-heat-ladder.md H1, a group seeing her is stage 4): a raised class passes risky_floor=60,
    risky_cap=79 and campus_talk in risky_eff, and `mild` (label, blocks) is what she does for one person below it,
    Exhibitionism 20 up to the floor, cap 39. her_line then splits: the two lower bands go with the mild screen."""
    mild_buttons, mild_nodes, loud_line = [], [], list(her_line)
    # exhibition phase 1 (LO, 2026-11-08): `covered` = {"look": blocks, "result": blocks, "thoughts": 4 lines}. Under
    # Daring, in the low-cut top, someone in the room looks; her choice is to let it go on (the-heat-ladder.md H1,
    # stage 1). Once a day across all classes (class_look_today).
    cov_cond = cond({"type": "clothing_item", "item_id": "low_top", "operator": "equipped"},
                    {"type": "clothing_slot", "slot": "bra", "operator": "equipped"},
                    trait("exhibitionism", "lt", 20), flag("class_look_today", False),
                    flag("class_late", False))   # late entry (DECISIONS 235): the look and its two buttons are on-time only
    cov_look, cov_button, cov_node = [], [], []
    if covered:
        cov_look = [G(cov_cond, *covered["look"])]
        cov_button = [go("Leave your top as it is.", node="covered", mins=0, flags=list(meet_flags) + [fset("class_look_today")],
                         cond_=cov_cond, eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 19}])]
        bands = [GC(cond(trait("exhibitionism", "lt", b)), T(t)) for b, t in zip((5, 10, 15, 20), covered["thoughts"])]
        cov_button.append(go("Pull your top straight.", node="covered_no", mins=0, flags=list(meet_flags) + [fset("class_look_today")], cond_=cov_cond))
        cov_node = [node("covered", "Leave it", [*covered["result"], *bands], [go("Pack up, slowly.", loc="lecture_hall", mins=90)]),
                    node("covered_no", "Pull it straight", list(covered["no"]), [go("Pack up.", loc="lecture_hall", mins=90)])]
    if mild:
        loud_line = list(her_line)[2:]
        for clothes in ([{"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}],
                        [{"type": "clothing_slot", "slot": "bra", "operator": "equipped"}, {"type": "worn_type", "operator": "eq", "value": "short_skirt"}]):
            mild_buttons.append(go(mild[0], node="risky_mild", mins=0, flags=meet_flags,
                                   cond_=cond(trait("exhibitionism", "gte", 20), trait("exhibitionism", "lt", risky_floor), *clothes),
                                   eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": CAP_DARING}]))
        mild_nodes.append(node("risky_mild", mild[0].rstrip("."), [*mild[1], *list(her_line)[:2]], [go("Pack up, slowly.", loc="lecture_hall", mins=90)]))
    return {
        "id": cid, "name": name,
        "description": f"{subj} class: Focus (energy 10, {grade} +2, intelligence +1) · Chat · Doze (energy +5) · Skip ({grade} -2) · the risky slot ({'Watched, a milder one at Daring' if mild else 'Daring'}).",
        "trigger": {"location": "lecture_hall", "is_repeatable": True, "priority": 5, "is_active": True,
                    "max_triggers_per_day": 1, "schedules": at_start(schedules), "conditions": cond(flag("opening_done"))},
        "nodes": [
            node("class", subj, [*opening, *extra_blocks,
                G(cond(trait("energy", "lt", 20)), T(pools["tired"])),
                G(DARING_STATE, *eyes_blocks(pools)),
                *cov_look,
                *CLASS_CLOTHES.get(cid, []),
            ], [
                # Shut under 20 energy, as the thought says (college.md "The lock", sweep A5-08)
                go("Focus. (90 minutes, 10 energy)", node="focus", mins=0, costs=[{"trait": "energy", "value": 10}], flags=meet_flags,
                   swl=True, cond_=cond(trait("energy", "gte", 20)),
                   eff=[add(grade, 2), add("intelligence", 1, clamp=False)]),
                go("Chat.", node="chat", mins=0, flags=meet_flags),
                go("Doze.", node="doze", mins=0, flags=meet_flags, eff=[{"targetType": "player", "trait": "energy", "op": "add", "value": 5, "cap": 100}]),
                go(risky_label, node="risky", mins=0, flags=meet_flags,
                   cond_=cond(trait("exhibitionism", "gte", risky_floor), {"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}),
                   eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": risky_cap}, *risky_eff]),
                go(risky_label, node="risky", mins=0, flags=meet_flags,
                   cond_=cond(trait("exhibitionism", "gte", risky_floor), {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}, {"type": "worn_type", "operator": "eq", "value": "short_skirt"}),
                   eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": risky_cap}, *risky_eff]),
                *mild_buttons,
                *cov_button,
                go("Skip it.", loc="campus", mins=0, eff=[add(grade, -2) | {"clamp": True}]),   # floor at 0 (gate `a deduction is gated or priced`)
            ]),
            node("focus", "Focus", [POOL(*[P(t) for t in pools["focus"]]), *beside], [go("Pack up.", loc="lecture_hall", mins=90)]),
            node("chat", "Chat", [*(beside if chat_beside is None else chat_beside), POOL(*[P(t) for t in pools["chat"]])], [go("Pack up.", loc="lecture_hall", mins=90)]),
            node("doze", "Doze", [POOL(*[P(t) for t in pools["doze"]])], [go("Wake up.", loc="lecture_hall", mins=90)]),
            node("risky", "Let them look", [*([P(risky_text)] if isinstance(risky_text, str) else list(risky_text)), *(RISKY_SAID.get(subj, []) if said is None else said), *loud_line],
                 [go("Pack up, slowly.", loc="lecture_hall", mins=90)]),
            *mild_nodes,
            *cov_node,
        ]}


# exhibition phase 1 (LO, 2026-11-08): who looks in each class when she's in the low-cut top, under Daring
COVERED = {
    "psych": {"look": [P("The guy on your other side keeps dropping his pen. Every time he leans down for it, his eyes come up level with the front of your low-cut top and stay there a second too long.")],
              "result": [P("You don't tug it up. He drops the pen twice more, red to the ears, and Dr. Hale's slides go past without either of you reading one."),
                         D(DESK, "Same seat next time?"),
                         P("He says it to your tits, not your face. Not here, not with the whole row around you. But you don't say no.")],
              "no": [D(DESK, "Sorry. Sorry."), P("He looks at his pen like it's the most interesting thing in the room. He'll be in the same seat next lecture.")],
              "thoughts": ["He was only looking. It was nothing.", "He looked, and you let him.",
                           "You didn't fix it, and you knew he'd keep looking.", "Next time he won't need the pen."]},
    "business": {"look": [P("Every time you lean forward to write, the low-cut top gapes. In the row behind, the study guy has stopped highlighting. You can feel him looking down the front of it at your tits.")],
                 "result": [P("You keep writing, and you don't pull it closed. His highlighter doesn't move for the rest of the lecture."),
                            D(STUDY, "You can, uh. You can borrow my notes. Any time."),
                            P("He means something else, and you both know it. Not in here.")],
                 "no": [P("You pull it closed. Behind you the highlighter starts squeaking again, fast."), D(STUDY, "Sorry. I was, uh. Reading."), P("He sits behind you every lecture.")],
                 "thoughts": ["He's just a guy looking. It's fine.", "You kept writing, and let him look.",
                              "You wanted him to see down it.", "You wonder how long he'd look if you let him."]},
    "bio": {"look": [P("Halfway through, the TA leans over your bench to check your diagram, and her eyes slide off the page and down the front of your low-cut top to your tits. Her neck goes pink.")],
            "result": [P("You don't sit back. She stays leaning a breath too long, tapping your diagram with her pen and not reading a word of it."),
                       D(TA, "That's. Good. That's good work."),
                       P("She goes back to the front of the hall, pink to the ears. Not here. She'll be round the benches again next week.")],
            "no": [P("You sit back. She straightens up fast and taps your diagram."), D(TA, "Fine. Fine. Carry on."), P("She'll be round the benches again next week.")],
            "thoughts": ["She was checking your work. That's all.", "She looked, and you let her.",
                         "You liked making her blush.", "Next week you'll lean closer when she comes round."]},
    "figure": {"look": [P("He's not even pretending now. Every time you shade, his eyes go down the front of your low-cut top to your tits.")],
               "result": [P("You keep shading and leave it as it is. He grins at you over his pad."),
                          D(COCKY, "Best view in the room. Don't tell her."),
                          dict(P("He means the model. Not yet, and not in front of the lecturer."), release=2),   # DECISIONS 231: it answers his line, and he is release 2
                          # DECISIONS 233 (re-read, the hook): his lines are release 2, so release 1 says what comes next itself
                          dict(P("He's at the easel beside yours every class. Next week he'll be there again, and so will his eyes."), release_until=1)],
               "no": [P("You pull your top straight and turn your easel an inch."), D(COCKY, "Spoilsport. Same easel next week, though."),
                      dict(P("He shrugs and goes back to his pad. He'll be at the same easel next week."), release_until=1)],   # DECISIONS 233
               "thoughts": ["He's an idiot. It meant nothing.", "He looked, and you let him.",
                            "You let him look, and he knew you knew.", "You'll take the same easel next week."]},
}

# ── Psychology (Hale; Nadia beside her; the guy beside her, the rival) ──
out.append(class_row(
    "college_class_psych", "Attend the Psychology lecture", "Psychology", "grade_psych", PSYCH, H,
    [fset("hale_met"), fset("nadia_met"), fset("desk_guy_met")],   # DECISIONS 223: his line says "Psych", so Psych meets him too
    [G(cond(flag("hale_met"), flag("nadia_met")), P("Psychology. Dr. Hale at the lectern in his tweed, the slides already up. Nadia has saved you the seat beside her in the front row, like always.")),
     G(cond(flag("hale_met", False)), P("Psychology. A man in tweed at the lectern, slides already up: Dr. Hale, the timetable says. A girl in big glasses in the front row moves her bag off the seat beside her and pats it."),
       WHO("Sit here. I'm Nadia. Nobody sits at the front for him. You'll see why.")),
     G(cond(trait("hale_step", "gte", 2)), P("He finds you in the front row before he starts. He always does now.")),
     G(cond(trait("hale_step", "gte", 4)), P("He can't look at you for long. He keeps his eyes on the back wall when he talks.")),
     G(cond(flag("desk_guy_met", False)), P("The guy on your other side leans over and copies the date off your page without asking."), D(DESK, "You're in my Business class too. Looks like I sit by you.")),
     G(cond(trait("grade_psych", "lt", 40)), D(H, "Some of you are failing this course. You know who you are.")),
     G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), P("His eyes drop to your thighs. He loses the sentence, steps back behind the lectern, and starts it again.")),
     ],
    [G(cond(trait("hale_step", "lt", 4)), D(N, "He watches you more than the slides. Just saying."))],   # at step 4+ he keeps his eyes on the back wall
    "Sit in the front row and let him look.",
    by_clothes(
        [P("You sit in the front row and don't fold your arms over your chest, and don't cross your legs. Dr. Hale lectures to the back wall for ninety minutes, and every time he forgets and looks down at your chest, his voice goes. Nadia kicks your foot under the desk, grinning.")],
        [P("You sit in the front row and don't fold your arms over your chest, and don't cross your legs. Dr. Hale lectures to the back wall for ninety minutes, and every time he forgets and looks down at your thighs, his voice goes. Nadia kicks your foot under the desk, grinning.")],
        P("As the room packs up, he says it without looking at you."),
        D(H, "Sit like that again, @player, and we'll talk about your grade.")),
    pools=POOLS["psych"], her_line=RISKY_HER_LINE["psych"], covered=COVERED["psych"]))

# ── Business (strict; the rival; the study guy) ──
out.append(class_row(
    "college_class_business", "Attend the Business lecture", "Business", "grade_business", BUSI, BUS,
    [fset("desk_guy_met")],
    [P("Business. The lecturer is a gray man in a gray suit who calls the register and means it."),
     G(cond(flag("desk_guy_met", False)), P("The guy in the next seat leans over and copies the date off your page without asking."), D(DESK, "You're in my Psych class too. Looks like I sit by you.")),   # pass 5 C36: the row that sets the flag names him
     G(cond(flag("study_guy_met")), P("The study guy is already in the row behind you with three highlighters out.")),
     G(cond(flag("rival_met")), P("The rival girl sits where she can watch you.")),
     D(BUS, "Phones away. Eyes up. This is on the exam."),
     dict(G(cond(trait("grade_business", "lt", 40)), D(BUS, "Retakes are by appointment. Honest work only. I won't say it twice.")), release=2),   # DECISIONS 231 (reader): points at a place or person release 1 cuts
     dict(G(cond(trait("grade_business", "lt", 40)), D(BUS, "Honest work only. I won't say it twice.")), release_until=1),
     ],
    [D(STUDY, "You want my notes? You can have my notes. Seriously, any time."),
     G(cond(flag("dress_warned"), flag("rival_met"), {"type": "clothing_slot", "slot": "bra", "operator": "equipped"},
            {"type": "worn_type", "operator": "neq", "value": "short_skirt"}), D(RIVAL, "Nice of you to dress for once."))],
    "Lean back for the guy in the row behind.",
    by_clothes(
        [P("You lean back in your chair and stretch, slowly, arms over your head, so what you're wearing pulls tight across your tits. From the row behind, the guy can see straight down it. He stops highlighting.")],
        [P("You lean back in your chair and stretch, slowly, and your skirt rides up your thighs. The guy in the row behind leans sideways to see more. He stops highlighting.")],
        P("Every time the lecturer turns from the board you sit up straight. He'd write you up for less. Two seats down, a girl watches him watching you, and her mouth gets thinner and thinner."),
        # pass 3 A56 (the-heat-ladder.md H4): the not-yet said out loud, and the hook, the next lecture
        P("When the room packs up, the guy from the row behind leans over your shoulder, red to the ears."),
        D(STUDY, "Not in here, or he'd write us both up. But same seats next lecture?")),
    pools=POOLS["business"], her_line=RISKY_HER_LINE["business"], covered=COVERED["business"]))

# ── Biology (the shy TA; Zoe; the cocky guy) ──
out.append(class_row(
    "college_class_bio", "Attend the Biology lecture", "Biology", "grade_bio", BIO, TA,
    [],
    [P("Biology. The TA runs it, a shy woman in a lab coat who blushes when she has to say reproductive system out loud. The girl beside you whispers through the slides."),
     dict(G(cond(flag("zoe_met", False)), WHO("Find me on the quad. I'm always there. Tuesdays, Thursdays, Fridays.")), release=2),   # DECISIONS 231 (reader): points at a place or person release 1 cuts
     G(cond(flag("zoe_met")), D(Z, "Babe. Look at the TA. She's staring at your legs again."),
       P("The TA catches you catching her. Her neck goes pink, but she only turns to her slide."),
       # the "eyes" line (DARING_STATE: no bra or a short skirt) has her still looking on this same screen
       GC(cond({"type": "clothing_slot", "slot": "bra", "operator": "equipped"}, {"type": "worn_type", "operator": "neq", "value": "short_skirt"}),
         P("She won't look at your legs again, not with the whole hall here."))),
     dict(G(cond(trait("grade_bio", "lt", 40)), D(TA, "If anyone's struggling, my door's open Tuesday to Friday afternoons. Really.")), release=2),   # DECISIONS 233 (re-read): points at a place release 1 cuts
     dict(G(cond(trait("grade_bio", "lt", 40)), D(TA, "If anyone's struggling, ask me after class. Really.")), release_until=1),
     ],
    [G(cond(flag("zoe_met")), D(Z, "Party Friday. I'm not asking."))],
    "Let the TA see.",
    by_clothes(
        [P("You sit up straight in the second row with your shoulders back, and don't fold your arms. Your tits show through what you're wearing. The TA sees. She drops her pen, picks it up, drops it again.")],
        [P("You sit with your knees apart in the second row and don't fix your skirt. The TA can see right up it. She drops her pen, picks it up, drops it again.")],
        P("She spends the rest of the class looking very hard at her slides, her neck pink all the way down to her collar. Twice she opens her mouth to say something about it, and doesn't.")),
    pools=POOLS["bio"], her_line=RISKY_HER_LINE["bio"], covered=COVERED["bio"], risky_floor=60, risky_cap=79, risky_eff=[add("campus_talk", 1, clamp=False)],
    mild=("Catch the TA's eye.", by_clothes(
        [P("You wait until the row is bent over its notes. Then you turn your shoulders to the front and put your arms down, and your nipples push at what you're wearing, on the side nobody else can see. The TA looks up from her slide and sees. Her pen slips out of her fingers and rolls off the lectern.")],
        [P("You wait until the row is bent over its notes. Then you let your knees drift apart under the desk, on the side that faces the front, and nobody else has the angle. The TA looks up from her slide and sees. Her pen slips out of her fingers and rolls off the lectern.")],
        P("When the room packs up she's wiping a board that's already clean, and she doesn't turn around."),
        D(TA, "I didn't see anything, @player. Okay? So don't. Not in here."), ME("See what?")))))

# ── Figure drawing (the model, nude; the art lecturer; Zoe; the cocky guy) — the pose beat every class ──
POSE = ("The model drops her robe on the platform and steps up naked under the lamp. She sits on the stool and turns her shoulder to the room. Her tits are heavy. They sway when she settles. Her nipples are dark and tight in the cold air. Your charcoal follows the curve of her ass where it spreads on the stool. You draw her thighs, pressed together, and the soft crease between them. You can't stop looking. Your face burns. Your own nipples go hard. The lecturer walks the rows behind you. \"Look at the weight of her,\" she says. \"Draw that.\"")
POSE_LATE = ("The model is already up on the stool, naked under the lamp, her shoulder turned to the room. " + POSE.split("turns her shoulder to the room. ", 1)[1])
POSE_END = "You keep drawing the heavy swing of the model's tits, but it's your nipples that ache."
fig = class_row(
    "college_class_figure", "Attend Figure drawing", "Figure drawing", "grade_art", FIG, ART,
    [],
    [G(cond(flag("class_late", False)), P(POSE)), G(cond(flag("class_late")), P(POSE_LATE)),   # late entry: she comes in on the pose
     G(cond(flag("zoe_met")), P("Zoe kicks your ankle under the easel.")),
     G(cond(flag("zoe_met", False)), P("The girl at the next easel kicks your ankle and grins.")),
     P(POSE_END),
     VID("a nude female life model posing on a stool under a lamp in an art class, students drawing at easels", "nude model posing art class students drawing", "life drawing class naked model on stool", pool_dir="sex/figure_class_pose_t4"),
     G(cond(flag("cocky_guy_met")), P("At the next easel, the cocky guy isn't drawing the model. He's drawing you.")),
     ],
    [D(ART, "Better. Look at what's actually there, not what you think is there.")],
    "Lean into your easel and let him look.",   # reader a3 #25-26 (DECISIONS 131): one watcher, as the screen says
    by_clothes(
        [P("You lean into your easel, slow, and your tits hang heavy against what you're wearing, your nipples showing through it. The guy at the next easel gives up on the model completely.")],
        [P("You lean into your easel, slow, and your skirt rides up the backs of your thighs. The guy behind you gives up on the model completely.")],
        P("The lecturer stops behind you, looks at your drawing, looks at you."),
        D(ART, "Clothes stay on in my class, @player. Unless you're on the platform.")),
    pools=POOLS["figure"], chat_beside=[], her_line=RISKY_HER_LINE["figure"], covered=COVERED["figure"])
# reader a3 #25-26 (DECISIONS 131): the risky screen's title names one watcher here too
next(n for n in fig["nodes"] if n["id"] == "risky")["name"] = "Let him look"
out.append(fig)

# ── first classes: meeting the staff (LIVES §6: the lecturers at their first class) ──
def first_class(cid, name, sch, met, people_flags, blocks):
    return {"id": cid, "name": name, "description": f"Meets the {name.lower()} people at the first class. Sets {met}.",
            "trigger": {"location": "lecture_hall", "is_repeatable": False, "priority": 8, "is_active": True,
                        "schedules": at_start(sch), "conditions": cond(flag("opening_done"), flag(met, False))},
            "nodes": [node("first", name, blocks, [go("Find a seat.", loc="lecture_hall", mins=2, flags=[fset(met)] + [fset(f) for f in people_flags])])]}

out.append(first_class("meet_business", "Your first Business class", BUSI, "business_lecturer_met", ["study_guy_met", "rival_met"], [
    P("Business is a gray room with a gray man at the front of it: the Business lecturer, fifty, a suit with no creases, a register in his hand he actually calls."),
    D(BUS, "I don't do extensions. I don't do excuses. I do honest work, and I grade it honestly. Sit down."),
    P("The guy in the row behind you, the one with three highlighters, leans forward. His eyes go to your chest, and he goes red and looks down at his notes."),
    D(STUDY, "You can borrow my notes. Any time. If you, um. If you want."),
    P("There's something else he wants to ask you, but he doesn't ask it, not with the gray man looking."),
    P("A sharp girl in the front row watches you sit and doesn't smile."), WHO("New? Don't take my seat."),
]))
out.append(first_class("meet_bio", "Your first Biology class", BIO, "bio_ta_met", [], [
    P("Biology is taught by the TA, a shy woman of twenty-eight in a lab coat and big earrings, who blushes when she says reproductive."),
    D(TA, "Hi. I'm— I'll be taking you this term. Please don't eat the specimens. That was a joke. Sort of."),
    P("Her eyes go round the room and land on you and skip off you, fast, like she touched something hot."),
    dict(D(TA, "My door's open in the afternoons. If anyone. You know. Needs anything."), release=2),   # DECISIONS 231 (reader): points at a place or person release 1 cuts
    dict(D(TA, "If anyone. You know. Needs anything."), release_until=1),
    P("She says it to all of you, but she's looking at your chest when she runs out of words. She turns to the slides before anyone can ask what she meant."),
]))
out.append(first_class("meet_figure", "Your first Figure drawing class", FIG, "art_lecturer_met", ["cocky_guy_met", "figure_model_met"], [
    P("Easels in a horseshoe round a platform with a stool on it, and a woman in a dressing gown sitting on the edge of the platform drinking from a flask: the model."),
    D(ART, "Figure drawing. Bodies. You'll draw what's there, not what you think is there, and you will not giggle. She's working. Respect it."),
    P("The art lecturer is forty-five, charcoal on her hands, and she looks at every new face like she's measuring it for a frame."),
    D(MODEL, "First years. Lovely. Nobody faint."),
    P("You take an easel halfway round the horseshoe."),
]))
_mf = out[-1]
_mf["nodes"][0]["choices"] = [go("Set up your easel.", node="easel", mins=2)]
_mf["nodes"].append(node("easel", "The next easel", [
    G(cond(flag("jake_met")), P("The guy at the next easel is in a team jacket: Jake's teammate, the cocky one. He looks you over, slow, and grins.")),
    G(cond(flag("jake_met", False)), P("The guy at the next easel is in a team jacket, the cocky kind. He looks you over, slow, and grins.")),
    D(COCKY, "This is going to be a good class."),
], [go("Find your charcoal.", loc="lecture_hall", mins=2,
       flags=[fset("art_lecturer_met"), fset("cocky_guy_met"), fset("figure_model_met")])]))
# The first class runs straight into the lecture (LO, 2026-11-01: "Biology just shows the lecture, nowhere to
# attend"). The meeting screen used to end back in the hall, so the first class read as over. Its last button now
# opens the class's own seat (Focus, Chat, Doze, Skip, the risky slot), copied from the class canvas. The opening
# lines are left out because the meeting has just said them (Figure drawing keeps its pose, which is the class);
# the tired and eyes lines stay.
# Writing pass 2026-11-04 (gate one pool, one place): the seat is built by class_row with its own first-class words,
# not copied from the class canvas, because a player who sits both must read two different things.
import copy
def into_class(meet, seat_canvas, exit_text, keep_opening=False):
    seat = copy.deepcopy(seat_canvas["nodes"])
    own_media(seat, "first")   # pass 3 B37: the copied seat's clips are their own assets (sex/figure_class_pose_first_t4)
    if not keep_opening:
        seat[0]["blocks"] = seat[0]["blocks"][-2:]      # the tired line and the eyes line (class_row's last two)
    last = [n for n in meet["nodes"] if any(c.get("locationId") == "lecture_hall" for c in n["choices"])][-1]
    flags = [f for c in last["choices"] for f in c.get("flagEffects", [])]
    last["choices"] = [go(exit_text, node="class", mins=2, flags=flags)]
    meet["nodes"] += seat
MEETS = {c["id"]: c for c in out if c["id"] in ("meet_business", "meet_bio", "meet_figure")}
_seat_business = class_row(
    "meet_business", "", "Business", "grade_business", BUSI, BUS, [], [],
    [D(STUDY, "I copied out the reading list for you. In case you missed it. Here.")],   # scene reader 2026-11-04: the rival's dress crack is cut, she has only just met her
    "Lean back so the row behind can see.",
    by_clothes(
        [P("You've been in this room ten minutes when you push your chair back and lift your arms, like you're only stretching. Your tits press up against what you're wearing, with nothing under it to hold them. In the row behind, the guy with the highlighters looks straight down your front. His pen runs off the page.")],
        [P("You turn sideways in your new seat and cross one leg slowly over the other, and your skirt climbs your thigh. The guy with the highlighters leans out into the aisle to follow it. His pen runs off the page.")],
        P("You're facing front by the time the gray man turns around, but he reads out the next heading like he's reading out charges. In the front row the sharp girl has twisted in her seat to watch you, and she isn't smiling.")),
    pools=FIRST_POOLS["business"], her_line=RISKY_HER_LINE["first_business"], said=FIRST_SAID["business"],
    risky_floor=60, risky_cap=79, risky_eff=[add("campus_talk", 1, clamp=False)],
    mild=("Stretch for the guy behind you.", by_clothes(
        [P("You've been in this room ten minutes when you stretch, small, one arm up, like your shoulder's stiff. With no bra on, your tits lift under what you're wearing, and only the seat right behind you has the angle. The guy with the highlighters looks, and his ears go red.")],
        [P("You've been in this room ten minutes when you hook one ankle behind the other and let your skirt ride an inch up the back of your thigh. Only the seat right behind you has the angle. The guy with the highlighters looks, and his ears go red.")],
        P("Nobody else looks up. The gray man goes on reading out headings."),
        D(STUDY, "Um. You dropped. No. You didn't drop anything."), ME("No, I didn't."),
        D(STUDY, "Not in here, okay? He'd throw me out. Same seat next time?"))))
_seat_bio = class_row(
    "meet_bio", "", "Biology", "grade_bio", BIO, TA, [], [],
    [G(cond(flag("zoe_met")), D(Z, "Babe. She looked at you and forgot how to talk. This class is going to be my favorite."))],
    "Let the TA see.",
    by_clothes(
        [P("You take the second row for your first class and you don't slouch. Shoulders back, arms down at your sides. Your tits show through what you're wearing, nipples and all. The TA's eyes land there in the middle of a word. The word never comes out, and her clicker jumps two slides.")],
        [P("You take the second row for your first class, let your knees fall open and leave your skirt where it lands. The TA can see right up it from where she's standing. She says nothing, but her clicker jumps two slides, and she has to go back.")],
        P("She gets through the rest of it with her eyes on the back wall and her neck pink to the collar of her lab coat, but she looks at your row once more, and looks away so fast she knocks her water over.")),
    pools=FIRST_POOLS["bio"], her_line=RISKY_HER_LINE["first_bio"], said=FIRST_SAID["bio"],
    risky_floor=60, risky_cap=79, risky_eff=[add("campus_talk", 1, clamp=False)],
    mild=("Catch the TA's eye.", by_clothes(
        [P("Your first class, and while the row around you hunts for pens you turn your shoulders to the front. Your nipples show through what you're wearing, on the side only she can see. The TA's eyes land there, and her clicker jumps a slide.")],
        [P("Your first class, and while the row around you hunts for pens you let your knees fall open under the desk, on the side only she can see. The TA's eyes land there, and her clicker jumps a slide.")],
        P("She goes back a slide without looking up, and she keeps her eyes on the wall after that."),
        D(TA, "Sorry. Wrong one. Nobody saw that. The slide, I mean."), ME("I didn't see a thing."))))
FIRST_POSE = ("The model caps her flask, shrugs the dressing gown off her shoulders and climbs onto the stool with nothing on. Her tits are full and hang low, and the left one rolls against her arm when she turns. Her nipples are wide and brown, and they pull tight in the draft. Her ass flattens on the stool. You draw her thighs and the dark hair where they meet. Your hand isn't steady. Your cheeks are hot, and your own nipples have gone hard. The lecturer comes along the horseshoe behind you. \"First thing you learn,\" she says. \"She's not a shape. Get that weight down, the tits, the thighs, all of it.\"")
FIRST_POSE_LATE = ("The model is already on the stool with nothing on. " + FIRST_POSE.split("with nothing on. ", 1)[1])
_seat_figure = class_row(
    "meet_figure", "", "Figure drawing", "grade_art", FIG, ART, [],
    [G(cond(flag("class_late", False)), P(FIRST_POSE)), G(cond(flag("class_late")), P(FIRST_POSE_LATE)),
     G(cond(flag("zoe_met")), P("Zoe leans around her easel, sees your face and laughs without making a sound.")),
     G(cond(flag("zoe_met", False)), P("The girl on your other side catches you staring and raises her eyebrows.")),
     P("Your page has her tits on it now, badly, twice, but your own nipples won't stop aching."),
     VID("a nude female life model posing on a stool under a lamp in an art class, students drawing at easels", "nude model posing art class students drawing", "life drawing class naked model on stool", pool_dir="sex/figure_class_pose_t4"),
     G(cond(flag("cocky_guy_met")), P("The guy in the team jacket at the next easel has turned his pad so you can see it. He's rubbed the model out of it. It's your neck, and he's started on your chest.")),
     ],
    [D(ART, "That's a start. Now forget everything you think you know about a hip.")],
    "Lean into your easel and let him look.",
    by_clothes(
        [P("You've barely finished that second bad sketch when you stretch up to the top of the paper and stay there. Your tits swing forward against what you're wearing, loose, and your nipples push through it. The guy in that jacket stops pretending to look at the model.")],
        [P("You've barely finished that second bad sketch when you bend to the ledge of your easel and take your time. Your skirt climbs the backs of your thighs. The guy in that jacket stops pretending to look at the model.")],
        P("The lecturer comes back along the horseshoe and stops behind you. She looks at your page, then at you."),
        D(ART, "First lesson. Down here, the clothes stay on. If you want them off, the platform's right there.")),
    pools=FIRST_POOLS["figure"], chat_beside=[], her_line=RISKY_HER_LINE["first_figure"], said=FIRST_SAID["figure"])
next(n for n in _seat_figure["nodes"] if n["id"] == "risky")["name"] = "Let him look"
into_class(MEETS["meet_business"], _seat_business, "Find a seat.")
into_class(MEETS["meet_bio"], _seat_bio, "Find a seat.")
into_class(MEETS["meet_figure"], _seat_figure, "Find your charcoal.", keep_opening=True)   # the pose is the class

# ── late entry (LO playtest 2026-11-12, DECISIONS 235) ──
# The timetable said 8:30-10:00 and the class only opened for 15 minutes, so a player at 8:50 found an empty hall.
# Now each class is open for 45 minutes. In its first 15 she is on time. In the 30 after, the class swaps (a
# substitution, the way the desk guy swaps in: still the one card and the one visit a day) to a short late screen,
# her late line, and from there into the same class with `class_late` set. Late, she stays to the class's end, Focus
# pays +1 instead of +2, and the risky, covered and mild buttons are on-time only. After 45 minutes the door is shut;
# the card and the timetable both say so. The late screen holds only its own lines, so no pool or clip is pasted
# twice (gates `one pool, one place`, `one asset, one block`).
LATE_LINES = {
    "college_class_psych": ([G(cond(flag("hale_met")), P("The door bangs behind you. Dr. Hale stops in the middle of a sentence, taps his pen on the lectern twice, and waits while you edge along the front row to your seat."),
                               D(H, "Nice of you to join us, @player.")),
                             G(cond(flag("hale_met", False)), P("The door bangs behind you. The man at the lectern stops in the middle of a sentence, taps his pen twice, and waits while you edge along the front row to a seat."),
                               WHO("Nice of you to join us."))], "Sit down."),
    "college_class_business": ([P("The register's already been called. The man at the front looks at you over his glasses and writes something next to your name."),
                                D(BUS, "Late is absent with a coat on. Sit down.")], "Sit down."),
    "college_class_bio": ([P("The TA is halfway through a diagram on the board when the door goes. She sees you, goes pink, and loses her place."),
                           D(TA, "Just— sit anywhere. Quietly, please.")], "Sit anywhere."),
    "college_class_figure": ([P("The door bangs behind you. The lecturer looks at the clock, then at you, and points her charcoal at the last free easel."),
                              D(ART, "You've missed the warm-up, @player. Draw fast.")], "Take the last easel."),
    # her first class, late: the meeting's own screen is an on-time welcome, so the late one meets the same people
    # in its own words and goes straight to her seat (reader 2026-11-12: the welcome can't play half an hour in)
    "meet_business": ([P("Your first Business class has already started when you come in. The man at the front is fifty, in a gray suit with no creases, and he stops talking and looks at you over the register."),
                       D(BUS, "I don't do late. I don't do excuses. Sit down."),
                       P("A sharp girl in the front row watches you find a seat and doesn't smile. The guy in the row behind, the one with three highlighters, goes red when you sit down in front of him.")], "Find a seat."),
    "meet_bio": ([P("Your first Biology class has already started. The TA at the front is twenty-eight, in a lab coat and big earrings, halfway through a slide about cells. When the door bangs she jumps and goes pink."),
                  D(TA, "Oh— hi. Sit anywhere. Please.")], "Find a seat."),
    "meet_figure": ([P("Your first Figure drawing class has already started. Easels stand in a horseshoe round a platform, and the model is up on it, naked under the lamp. The lecturer is forty-five, charcoal on her hands, and she looks at the clock and then at you."),
                     D(ART, "Bodies. You draw what's there. You're late, so draw fast.")], "Find your charcoal."),
}
LATE_ROWS = {"college_class_psych": (PSYCH, "grade_psych"), "college_class_business": (BUSI, "grade_business"),
             "college_class_bio": (BIO, "grade_bio"), "college_class_figure": (FIG, "grade_art"),
             "meet_business": (BUSI, "grade_business"), "meet_bio": (BIO, "grade_bio"), "meet_figure": (FIG, "grade_art")}
ON_TIME_ONLY = ("risky", "risky_mild", "covered", "covered_no")   # the screens late doesn't reach
LATE = "class_late"


def _plus(t, mins):
    h, m = map(int, t.split(":")); m += mins
    return f"{h + m // 60:02d}:{m % 60:02d}"


def _and(c, item):
    """`c`'s conditions with one more AND item (a fresh copy: several choices share one condition dict)."""
    cc = copy.deepcopy(c.get("conditions")) if c.get("conditions") else cond()
    assert cc.get("logic", "AND") == "AND", (c.get("text"), "an OR condition can't take one more AND item")
    cc.setdefault("items", []).append(item)
    c["conditions"] = cc
    return c


def _late_exits(c, rows, grade, focus):
    """The late twins of a 90-minute exit: she stays to the end of the class, so the minutes depend on when she came in.
    One twin per 5 minutes of the late window, each spending what is left of the class from the start of its 5
    minutes, so she leaves 0-4 minutes after the class ends (the engine moves the clock by a fixed amount only)."""
    base = c["text"].replace(" (1h 30m)", "")
    out_ = []
    for st, en in sorted({(r["start_time"], r["end_time"]) for r in rows}):
        length = int(en[:2]) * 60 + int(en[3:]) - int(st[:2]) * 60 - int(st[3:])
        for k in range(15, LATE_MINUTES, 5):
            tw = copy.deepcopy(c)
            spend = length - k
            tw["time_progression_minutes"] = spend
            tw["text"] = with_duration(base, spend) if spend >= 60 else base
            tw["flagEffects"] = list(tw.get("flagEffects") or []) + [funset(LATE)]
            if focus:   # late Focus pays +1: the +2 on the way in, -1 on the way out
                tw["effects"] = list(tw.get("effects") or []) + [add(grade, -1) | {"clamp": True}]
            _and(tw, flag(LATE, True))
            out_.append(_and(tw, tod(_plus(st, k), _plus(st, k + 5))))
    return out_


def late_entry(host, rows, grade):
    """Open the host for 45 minutes, swap its late 30 to a late screen, and give its exits late twins."""
    lines, button = LATE_LINES[host["id"]]
    if host["id"].startswith("meet_"):
        # straight to her seat, with the flags the meeting sets on its way into the class
        into = next(c for n in host["nodes"] if n["id"] != "class" for c in n["choices"] if c.get("nodeId") == "class")
        target, flags = "class", list(into.get("flagEffects") or [])
    else:
        target, flags = host["nodes"][0]["id"], []
    late = {"id": host["id"] + "_late", "event": True, "name": (host["name"] or "Class") + ", late",
            "description": f"Late entry to {host['id']} (DECISIONS 235): her late line, then the class with {LATE} set; she stays to its end, Focus +1.",
            "trigger": {"location": "lecture_hall", "is_repeatable": host["trigger"].get("is_repeatable", True), "priority": host["trigger"].get("priority", 5),
                        "is_active": True, "substitution_only": True,
                        "schedules": [dict(r, start_time=_plus(r["start_time"], 15), end_time=_plus(r["start_time"], LATE_MINUTES)) for r in rows],
                        # class_late off: her button sets it and may walk into the host's first screen, which runs the
                        # swap check again; without this the late screen would swap in again, and again
                        "conditions": _and({"conditions": host["trigger"].get("conditions")}, flag(LATE, False))["conditions"]},
            "nodes": [node("late", "Late", list(lines), [go(button, node=f"{host['id']}.{target}", mins=0, flags=flags + [fset(LATE)])])]}
    for n in host["nodes"]:
        new = []
        for c in n["choices"]:
            if c.get("nodeId") in ON_TIME_ONLY:
                new.append(_and(c, flag(LATE, False)))
                continue
            if c.get("nodeId") == "focus":
                c["text"] = c["text"].replace("(90 minutes, 10 energy)", "(10 energy)")
            if c.get("targetType") == "location" and c.get("time_progression_minutes") == 90:
                twins = _late_exits(c, rows, grade, n["id"] == "focus")
                new.append(_and(c, flag(LATE, False)))
                new.extend(twins)
                continue
            if c.get("targetType") == "location" and n["id"] == "class":   # Skip it.
                c["flagEffects"] = list(c.get("flagEffects") or []) + [funset(LATE)]
            new.append(c)
        n["choices"] = new
    ht = host["trigger"]
    ht["schedules"] = [dict(r, end_time=_plus(r["start_time"], LATE_MINUTES)) for r in rows]
    late_tod = cond(*[tod(_plus(r["start_time"], 15), _plus(r["start_time"], LATE_MINUTES)) for r in rows], logic="OR")
    ht["substitutions"] = [{"target_canvas_id": late["id"], "chance": 1.0, "conditions": late_tod}] + list(ht.get("substitutions") or [])
    if ht.get("is_repeatable"):
        ht["show_when_blocked"] = True
        ht["cooldown_message"] = hours_phrase(ht["schedules"]) + " · late after the first 15 minutes"
    return late


out.extend([late_entry(next(c for c in out if c["id"] == cid), rows, grade) for cid, (rows, grade) in LATE_ROWS.items()])
# ── the guy beside her (college_event_desk_guy; Psychology and Business; once a day) ──
# LO playtest 2026-11-10 (DECISIONS 223): it was a button in each class's first 15 minutes and spent the class for no
# grade. Now a walk-in swap from "Attend" (1 in 3, once a day): it IS the class, so every way out pays the class's
# grade +1 (half of Focus: he is the distraction). Which grade comes from the class row the clock is in (PSYCH and
# BUSI never overlap). The swap counts as the class's one visit that day.
def _desk_class_exit(text, eff=(), flags=()):
    rows = [(r, "grade_psych") for r in PSYCH] + [(r, "grade_business") for r in BUSI]
    return [go(text, loc="lecture_hall", mins=90, eff=[*eff, add(g, 1)], flags=[*flags, fset("desk_guy_today")],
               cond_=cond(wd(*r["weekdays"]), tod(r["start_time"], r["end_time"]))) for r, g in rows]


DESK_HAND_A = ("You check the room first. The lecturer faces the board. The row in front has its heads down. The desk hides everything below your elbows, so you slide your hand under it and open his jeans. His cock springs into your fingers, hot and thick, slick at the tip. You stroke his cock slow, root to head, your thumb slipping over the wet tip. He grips the desk edge and breathes through his nose so he won't make a sound. His balls are already drawn up tight. Your face burns and your nipples have gone hard, but you go faster.")
DESK_HAND_B = ("His cock throbs in your fist and his ass lifts off the seat. He comes over your knuckles, under the desk where nobody sees. You wipe your palm on his thigh while his cock twitches against his open jeans.")
out.append({
    "id": "college_event_desk_guy", "event": True, "name": "Notice the guy beside you is hard",   # pass 3 H33/H34 (the-voice.md R1, D11): the name says what happens if she clicks, and never hides the act
    "description": "Walk-in on Attend Psychology / Business (1 in 3, once a day): the guy beside her is hard. Curious: she looks. Hungry: her hand, unseen under the desk (explicit). Every exit pays the class grade +1.",
    "trigger": {"location": "lecture_hall", "is_repeatable": True, "priority": 4, "is_active": True, "substitution_only": True,
                "schedules": PSYCH + BUSI, "conditions": cond(flag("desk_guy_met"), trait("corruption", "gte", 20), flag("desk_guy_today", False))},
    "nodes": [
        node("ask", "Beside you", [
            P("The guy who sits beside you has his jacket across his lap and his jaw clenched. He catches you looking and leans in."),
            D(DESK, "I'm hard. Help me out."),
            # reader 2026-11-10: a repeat after her hand is not a first time
            G(cond(flag("desk_guy_helped", False)), ME("You're joking."), D(DESK, "Do I look like I'm joking? Look at it."),
              T("He said it like he was asking for a pen.")),
            G(cond(flag("desk_guy_helped")), ME("Again? Here?"), D(DESK, "You've done it before. Same row, same jacket."),
              T("He's come in your hand in this row before, and nobody saw.")),
        ], [
            go("Look.", node="watch", mins=3),
            go("Help him.", node="hand", mins=3, cond_=cond(trait("corruption", "gte", 60)), costs=[{"trait": "energy", "value": 10}], eff=[{"targetType": "player", "trait": "hygiene", "op": "add", "value": -10, "clamp": True}]),   # pass 3 E95   # a handjob in a full hall: Hungry (DECISIONS 124)
            go("\"Not here.\"", node="no", mins=1),
        ]),
        node("watch", "Look", [
            P("A girl two seats down has stopped writing and is watching the two of you."),
            P("You look. He moves the jacket an inch so you can see the shape of it straining his jeans, and watches you look, and grins at the board like nothing's happening."),
            P("Your thighs press together under the desk."),   # reader a3 #27 (DECISIONS 131): her body on the Look screen
            D(DESK, "Like what you see?"), ME("Shut up and take notes."), D(DESK, "Next time, then."),
        ], _desk_class_exit("Back to the class.")),
        node("hand", "Under the desk", [
            P(DESK_HAND_A),
            D(DESK, "Fuck. Fuck, don't stop. Somebody's turning round."), ME("Then keep your face still and come."),   # reader 2026-11-10: said before he comes
            P(DESK_HAND_B),
            VID("under a lecture desk a girl's hand in a guy's open jeans, the class facing the front", "handjob under desk in class", "girl hand in guy jeans under lecture desk", pool_dir="sex/desk_guy_hand_t5"),
            P("He zips up and goes back to copying the slides. Next class he'll be in that seat again, with his jacket on his lap."),   # the hook
        ], _desk_class_exit("Wipe your hand.", flags=[fset("desk_guy_helped")], eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 79}])),
        node("no", "Not here", [D(DESK, "Worth a try."), P("Two seats down a girl smirks into her notes."), P("He shrugs and puts his jacket straight and copies the slide like a model student. He keeps glancing at your hands for the rest of the class.")],
             _desk_class_exit("Back to the class.", flags=[fset("desk_guy_refused")])),
    ]})

# the swap rules on the two class rows (DECISIONS 223): 1 in 3; the target's own conditions carry the once a day
for _c in out:
    if _c["id"] in ("college_class_psych", "college_class_business"):
        _c["trigger"]["substitutions"] = list(_c["trigger"].get("substitutions") or []) + [
            {"target_canvas_id": "college_event_desk_guy", "chance": 0.33, "conditions": cond(flag("desk_guy_today", False))}]

# ── the dress-code warning (wardrobe pool, in class; once a day). Twice is a complaint ──
# It fires as the class starts (a class fills its window), and the lecturer is whoever teaches that slot.
def slot_cond(rows):
    return [cond(wd(*w), tod(a, b)) for w, a, b in rows]
WARN_BY = [(H, PSYCH, "Dr. Hale"), (BUS, BUSI, "The Business lecturer"), (TA, BIO, "The TA")]
warn_blocks = [P("Before the class starts, the lecturer calls you down to the front, quiet, while the room fills up.")]
HERE = lambda npc: {"type": "npc_at_location", "location_id": "lecture_hall", "npc_id": npc, "operator": "is_present"}
AWAY = lambda npc: {"type": "npc_at_location", "location_id": "lecture_hall", "npc_id": npc, "operator": "is_absent"}
for npc, rows, who in WARN_BY:
    warn_blocks.append(G(cond(HERE(npc)), D(npc, "This is a lecture hall, not a nightclub. Think about how you come to class.")))
warn_blocks.append(G(cond(AWAY(H), AWAY(BUS), AWAY(TA)),
                     WHO("This is a lecture hall, not a nightclub. Think about how you come to class.")))
warn_blocks += [
    G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}), P("Their eyes go to your chest, where everybody's eyes are going to be all class, and away.")),
    # reader a3 #28 (DECISIONS 131): her body, not the garment
    G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), P("Their eyes go to your bare thighs below the skirt, and away.")),
]
for r in PSYCH + BUSI:
    warn_blocks.append(G(cond(flag("dress_warned"), flag("rival_met"), wd(*r["weekdays"]), tod(r["start_time"], r["end_time"])),
                         P("On your way back to your seat, the rival girl leans out into the aisle with a little smile."),
                         D(RIVAL, "I told the dean's office. Somebody had to.")))
out.append({
    "id": "college_event_dress_code", "event": True, "name": "Get warned about what you're wearing",   # pass 3 H33/H34 (the-voice.md R1, D11): the name says what happens if she clicks, and never hides the act
    "description": "Wardrobe event in class: the slot's lecturer warns her about what she wears (no bra, a short skirt), as the class starts. The first sets dress_warned; after that, a complaint (complaints +1); the rival says so in her own classes. Pays no meter (it is a warning, not her choice). Once a day.",
    "trigger": {"location": "lecture_hall", "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 1,
                "schedules": at_start(PSYCH + BUSI + BIO), "conditions": DARING_STATE},
    "nodes": [node("warning", "Before class", warn_blocks, [
        # (DECISIONS 124, H5) the warning happens to her: it pays her nothing
        go("\"Yes. Sorry.\"", loc="lecture_hall", mins=5, cond_=cond(flag("dress_warned", False)), flags=[fset("dress_warned")]),
        go("\"Yes. Sorry.\"", loc="lecture_hall", mins=5, cond_=cond(flag("dress_warned")),
           eff=[add("complaints", 1, clamp=False)]),
    ])]})

# ── gossip (DECISIONS 207): the cost. At campus talk 40 the rival takes what campus says to the dean's office, once,
# in one of her classes (CoT: being talked about costs her; its rumor scenes cost humiliation, cot_40:1540-1543, and
# its threats never land, which the study counts a weakness, SYNTHESIS.md §1 item 9). Here it lands: complaints +1,
# which the dean's warning reads at 2 (dean_warning), and that sends the letter home. Both answers take the complaint;
# it happens to her, so it pays nothing (H5). ──
out.append({
    "id": "gossip_rival_report", "event": True, "name": "The rival tells the dean",
    "description": "Gossip's cost (DECISIONS 207): at campus_talk 40 the rival reports what campus says about her to the dean's office, once, as a Psychology or Business class starts. complaints +1 on either answer.",
    "trigger": {"location": "lecture_hall", "is_repeatable": False, "priority": 5, "is_active": True,
                "schedules": at_start(PSYCH + BUSI),
                "conditions": cond(flag("opening_done"), flag("rival_met"), trait("campus_talk", "gte", 40))},
    "nodes": [node("report", "Before class", [
        P("The rival girl is waiting by your row with her phone in her hand. She holds it up so you can see the screen: an email, sent, to the dean's office."),
        D(RIVAL, "I wrote down what everyone's saying about you. All of it, word for word. Somebody had to."),
        P("Three rows of people heard her say it. Nobody pretends they didn't. A guy at the end of your row looks at you like he's trying to work out which part is true."),
        T("A complaint with your name on it, on the dean's desk. And she said it to three rows of people first."),
    ], [
        go("\"Enjoy your class.\"", loc="lecture_hall", mins=5, eff=[add("complaints", 1, clamp=False)]),
        go("Sit down and say nothing.", loc="lecture_hall", mins=5, eff=[add("complaints", 1, clamp=False)]),
    ])]})

# ── the midterms (college_exam): weeks 7-8, once per exam, in that subject's slot ──
# reader a3 #24 (DECISIONS 131, call A): a no costs him Want +1. The cocky guy has no core traits in
# people_data.py (core={}), and a pay to a trait he doesn't declare is a made-up stat (call B), so the pay
# switches on by itself once people_data.py gives him a "want" (that file is the lead's to change).
from people_data import PEOPLE as _PEOPLE
COCKY_NO_PAY = []   # C1 (LO 2026-11-03, reverses DECISIONS 131 call A): her no never raises his Want
FLASH = ("The proctor sits at the front, reading. Every head in the row is bent over a page. You check the room once. Then you pull everything up under the desk line, where only he can see. Your tits are bare in the cold hall air. Your nipples go hard at once, tight and aching. His pen stops mid-word. His eyes drop to your tits and stay there. One second. Two. Three. You yank everything down and cover your breasts. He slides his paper to the edge of his desk. Your nipples are still hard, and his stare is still on your chest.")
# Each midterm its own thoughts (gate one pool, one place). Psychology keeps the first words; it has the most classes.
EXAM_TEXT = {
    "psych": {"low": "You know some of this, but not enough of it.", "high": "You studied. You actually know this.",
              "down": "Pens down. The proctor collects the papers row by row. The results go up on the portal next week, and on the office door.",
              "bad": "It went badly. Laura is going to see this on the portal.",
              "bad_high": "You knew that paper. It can't make up for the weeks before it, and Laura is going to see the number on the portal.",
              "mid": "It went fine. A pass, probably. Nobody will say anything.",
              "good": "It went well. For once the portal is going to make Laura smile."},
    "business": {"low": "Margins, break-even, the shoe company. You remember the shoe company and not much else.",
                 "high": "Break-even, fixed costs, the shoe company. You can do every one of these.",
                 "down": "Time. The proctor takes your paper before you've capped your pen and squares the stack like it's money. Grades go up on the portal next week, and on the office door.",
                 "bad": "You failed that by the numbers. Laura will open the portal and ask what she's paying for.",
                 "bad_high": "Every sum on that paper is right. One paper doesn't fix your whole grade, and Laura will open the portal and ask what she's paying for.",
                 "mid_high": "Those sums are right. Your grade's still only a pass, and nobody at home will ask.",
                 "mid": "A pass, if the gray man's feeling generous. Nobody at home will ask.",
                 "good": "You'd bet money on that paper. Laura will see it on the portal, and she'll have nothing to say."},
    "bio": {"low": "You recognize the heart on page one. You can't label half of it.",
            "high": "The heart is on page one, valve by valve. You could label it with your eyes shut.",
            "down": "The clock runs out with half the row still labeling. The proctor carries the papers up the aisle in a stack. You'll see your grade on the portal next week, and on the office door.",
            "bad": "Half those labels were guesses. Laura will read that grade on the portal, and she'll want to talk.",
            "bad_high": "You labeled every valve. It's too late to save your grade, and Laura will read it on the portal, and she'll want to talk.",
            "mid_high": "The heart was right, valve by valve. Your grade stays a pass, and nobody's going to call you about it.",
            "mid": "Enough labels right for a pass, probably. Nobody's going to call you about it.",
            "good": "You labeled the whole heart. Laura gets a good number on the portal for once."},
    "art": {"low": "Anatomy and proportion. You know what a back looks like, but you can't name one muscle in it.",
            "high": "Proportion, foreshortening, the muscles of the back. You've got all of it in your head and your hand.",
            "down": "The proctor calls time and the hall breathes out. Somebody has sketched him on the back of their paper, and it goes in the stack with the rest. Grades go on the portal next week, and on the office door.",
            "bad": "You can draw a back, but you can't name it. Laura will see that grade on the portal, and she won't care about your drawings.",
            "bad_high": "Every muscle in that back is named on your paper. It came too late for your grade, and Laura won't care about your drawings when she sees it on the portal.",
            "mid": "It'll pass. Nobody at home checks the art grade twice.",
            "good": "Top of the horseshoe, maybe. Laura will see this on the portal and say something nice about art class."},
}
WEEKS_7_8 = [{"type": "days_since_flag", "subject": "player", "flag_key": "opening_done", "operator": "gte", "value": 42},
             {"type": "days_since_flag", "subject": "player", "flag_key": "opening_done", "operator": "lt", "value": 56}]
for subj, grade, sch, code in [("Psychology", "grade_psych", PSYCH, "psych"), ("Business", "grade_business", BUSI, "business"),
                               ("Biology", "grade_bio", BIO, "bio"), ("Figure drawing", "grade_art", FIG, "art")]:
    done_f = f"exam_{code}_done"
    out.append({
        "id": f"college_exam_{code}", "name": f"The {subj} midterm",
        "description": f"The {subj} midterm (college_exam), weeks 7-8 in its class slot: Focus (reads intelligence), flirt for the study guy's paper (Curious), or a flash for the cocky guy's (Daring, explicit). Copying +5. Sets {done_f} and midterm_done.",
        "trigger": {"location": "lecture_hall", "is_repeatable": False, "priority": 9, "is_active": True,
                    "schedules": at_start(sch), "conditions": cond(*WEEKS_7_8, flag(done_f, False))},
        "nodes": [
            node("paper", "The midterm", [
                P(f"The {subj} midterm. Desks pulled apart, bags at the front, a proctor reading a paperback by the door. The paper lands face-down in front of you, and the clock on the wall starts."),
                WHO("Phones in your bags. Ninety minutes. Turn your papers over."),   # LO 2026-11-03: the proctor
                WHO("And no talking. Anyone I catch looking at another paper gets a zero."),   # pass 3 B3: the proctor again
                # DECISIONS 210 (reader): with his five chapters she knows the Business paper even under Intelligence 10
                G(cond(trait("intelligence", "lt", 10), *([trait("study_notes", "lt", 5)] if code == "business" else [])), T(EXAM_TEXT[code]["low"])),
                *([G(cond(trait("intelligence", "lt", 10), trait("study_notes", "gte", 5)), T("Margins, break-even, the shoe company. It's his notes, every chapter, word for word, still in your head."))] if code == "business" else []),
                G(cond(trait("intelligence", "gte", 10)), T(EXAM_TEXT[code]["high"])),
            ], [
                go("Focus. Do it yourself.", node="result", mins=90, cond_=cond(trait("intelligence", "gte", 10)), eff=[add(grade, 6)]),
                go("Focus. Do it yourself.", node="result", mins=90, cond_=cond(trait("intelligence", "lt", 10)), eff=[add(grade, 1)]),
                # DECISIONS 210 (goals.py study_notes): all five chapters of his notes, learned, not copied
                *([go("You know his notes by heart.", node="result", mins=90, cond_=cond(trait("study_notes", "gte", 5)), eff=[add(grade, 8)], flags=[fset("exam_by_notes")])]
                  if code == "business" else []),
                # DECISIONS 210: after all five chapters he doesn't need the flirt, only a look (his want, goals.py)
                *([go("Catch the study guy's eye.", node="study_want", mins=5, cond_=cond(ntrait(STUDY, "want", "gte", 5), flag("study_guy_met")))]
                  if code == "business" else []),
                *([go("Flirt with the study guy for his paper.", node="study", mins=5, cond_=cond(trait("corruption", "gte", 20), flag("study_guy_met")))]
                  if code == "business" else []),
                *([go("Look at the cocky guy.", node="price", mins=5, cond_=cond(trait("exhibitionism", "gte", 20), flag("cocky_guy_met")))] if code == "art" else []),
            ]),
            *([node("study_want", "One look", [
                P("You only have to look at him. He's been hoping you'd look over. He goes red, puts his pen down and moves his paper to the corner of his desk, angled your way, then looks at your chest across the gap like it's what he's owed."),
                T("Five chapters of his notes, and he still wants more. He can look."),
            ], [go("Copy.", node="result", mins=85, eff=[add(grade, 5), add("campus_talk", 1, clamp=False)]),
                # reader (DECISIONS 210): his offer can be turned down
                go("Look away and do your own.", node="result", mins=85, eff=[add(grade, 1)])])] if code == "business" else []),
            *([node("study", "The study guy", [
                P("You catch the study guy's eye across the gap and bite your lip and look at his paper and back at him. He goes red to the ears. A minute later his paper is on the corner of his desk, angled your way, and he's staring at the ceiling like a saint."),
            ], [go("Copy.", node="result", mins=85, eff=[add(grade, 5), add("campus_talk", 1, clamp=False)])])] if code == "business" else []),
            *([
            node("price", "His price", [
                G(cond(flag("jake_met")), P("Jake's teammate is at the next desk with his paper finished and his pen behind his ear. He sees you looking at it and leans back in his chair.")),
                G(cond(flag("jake_met", False)), P("The cocky guy from Figure drawing is at the next desk with his paper finished and his pen behind his ear. He sees you looking at it and leans back in his chair.")),
            ], [go("\"What?\"", node="flash_ask", mins=1), go("Look away.", node="result", mins=85, eff=[add(grade, 1)])]),
            node("flash_ask", "Show me", [
                D(COCKY, "Show me and I'll tilt my paper."),
            ], [go("Show him.", node="flash", mins=2, cond_=cond(trait("exhibitionism", "gte", 40))), go("\"No.\"", node="no", mins=1)]),   # a flash with the hall behind it: Showing (DECISIONS 124)
            # reader a3 #24 (DECISIONS 131, call A): her no gets his answer and costs him (his Want +1, when he has one)
            node("no", "Your loss", [
                P("He shrugs and turns his paper face-down, slow, so you watch it go."),
                D(COCKY, "Your loss."),
            ], [go("Back to your own paper.", node="result", mins=83, eff=[add(grade, 1)] + COCKY_NO_PAY)]),
            node("flash", "Three seconds", [
                P(FLASH),
                VID("under a desk in an exam hall a girl lifts her top for the guy at the next desk, rows of students writing", "girl flashes tits during exam under desk", "exam hall flash for answers", file=f"sex/exam_{code}_flash_t4.webm"),
            ], [go("Copy.", node="result", mins=82, eff=[add(grade, 5), {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": CAP_BOLD}],
                   flags=[fset("cocky_exam_deal")])])
            ] if code == "art" else []),
            node("result", "Pens down", [
                P(EXAM_TEXT[code]["down"]),
                WHO("Stay in your seats till I have every paper."),
                WHO("How'd you do? I left question four blank. The whole thing, blank."), ME("Don't ask me. I just want a drink."),   # pass 3 B3: the girl at the next desk
                # scene reader 2026-11-04: the grade is the whole course, so she can know the paper and still sit under 40;
                # the verdict agrees with the Intelligence line on the paper screen
                # reader (DECISIONS 210): exam_by_notes is the Business paper's only, so only its result reads it
                G(cond(trait(grade, "lt", 40), trait("intelligence", "lt", 10), *([flag("exam_by_notes", False)] if code == "business" else [])), T(EXAM_TEXT[code]["bad"])),
                *([G(cond(trait(grade, "lt", 40), trait("intelligence", "lt", 10), flag("exam_by_notes")), T(EXAM_TEXT[code]["bad_high"]))] if code == "business" else []),
                G(cond(trait(grade, "lt", 40), trait("intelligence", "gte", 10)), T(EXAM_TEXT[code]["bad_high"])),
                G(cond(trait(grade, "gte", 40), trait(grade, "lt", 70), trait("intelligence", "lt", 10)), T(EXAM_TEXT[code]["mid"])),
                G(cond(trait(grade, "gte", 40), trait(grade, "lt", 70), trait("intelligence", "gte", 10)), T(EXAM_TEXT[code].get("mid_high", EXAM_TEXT[code]["mid"]))),
                G(cond(trait(grade, "gte", 70)), T(EXAM_TEXT[code]["good"])),
            ], [go("Leave the hall.", loc="campus", mins=5, flags=[fset(done_f), fset("midterm_done")])]),
        ]})

# ── the lecturers in the lecture hall, before and after class (their class hubs) ──
LEAVE_TO = {"lecture_hall": "campus", "art_office": "faculty_floor", "business_office": "faculty_floor",
            "ta_office": "faculty_floor", "dean_office": "faculty_floor"}


# pass 3 D39 (the-surfaces.md R7): the free way out closes the beat, so it answers the person who just spoke
HUB_CLOSE = {"npc_hale": "Leave him to his lectern.", "npc_art_lecturer": "Leave her to her easels.",
             "npc_business_lecturer": "Leave him to his marking.", "npc_bio_ta": "Leave her to her clipboard.",
             "npc_dean": "Leave him to his files."}


def hub(cid, loc, npc, met, name, blocks, choices=None):
    return {"id": cid, "name": name, "description": f"{name}: one line on her grade, one on her clothes.",
            "trigger": {"location": loc, "npc": npc, "requires_npc": npc, "is_repeatable": True, "priority": 6, "is_active": True,
                        "conditions": cond(flag(met))},
            "nodes": [node("hub", name, blocks, choices or [go(HUB_CLOSE[npc], loc=LEAVE_TO[loc])])]}

def grade_lines(npc, grade, low, mid, top, r1=None):
    """r1 = (low, mid, top) for release 1, where the offices are cut (DECISIONS 231): a line that sends her to an
    office ships later, and release 1 gets the copy without it."""
    bands = [cond(trait(grade, "lt", 40)), cond(trait(grade, "gte", 40), trait(grade, "lt", 70)), cond(trait(grade, "gte", 70))]
    out = []
    for i, (c, line) in enumerate(zip(bands, (low, mid, top))):
        if r1 and r1[i] != line:
            out += [dict(G(c, D(npc, line)), release=2), dict(G(c, D(npc, r1[i])), release_until=1)]
        else:
            out.append(G(c, D(npc, line)))
    return out

def clothes_line(npc, line):
    return G(DARING_STATE, D(npc, line))

out.append(hub("hub_hale_class", "lecture_hall", H, "hale_met", "Dr. Hale, at the lectern", [
    P("Dr. Hale is at the lectern with his notes, squaring the edges."),
    # S4 (LO 2026-11-03): he's teaching, so this screen is look-only, and it says why
    P("He's mid-lecture. He catches your eye once, then goes back to his slides."),
    *grade_lines(H, "grade_psych", "You're behind, @player. Come and see me on Thursday.", "Good work. Could be better.", "Best paper in the room. Don't let it go to your head.",
                 r1=("You're behind, @player. Catch up.", "Good work. Could be better.", "Best paper in the room. Don't let it go to your head.")),
    # reader a3 #17 (DECISIONS 131): at grade 40+ a line points at his office. Office hours are Thu 17:00-19:30
    # (his rows); he names it only from his step 2 on, the step where he invites her. This hub fires Mon/Wed/Fri
    # mornings and Thursday 13:00-14:30, so on a Thursday the office is "tonight".
    G(cond(trait("grade_psych", "gte", 40), trait("hale_step", "gte", 2), wd(0, 2, 4)), D(H, "Thursday, @player. My office.")),
    G(cond(trait("grade_psych", "gte", 40), trait("hale_step", "gte", 2), wd(3)), D(H, "Tonight, @player. My office.")),
    G(cond(trait("grade_psych", "gte", 40), trait("hale_step", "lt", 2)), D(H, "See me if you're stuck.")),
    G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), P("His eyes drop to your thighs below your skirt, and he swallows. He steps in tight behind the lectern, so it hides him from the waist down, and squares the notes again.")),
]))
out.append(hub("hub_art_class", "lecture_hall", ART, "art_lecturer_met", "The art lecturer", [
    P("The art lecturer is moving between the easels with a box of charcoal, looking at you the way she looks at the model."),
    # S4 (LO 2026-11-03): she's teaching, so this screen is look-only, and it says why
    P("She's teaching. She holds your eye over an easel for a second, then turns back to the model."),
    *grade_lines(ART, "grade_art", "You're drawing what you expect, not what's there. Look harder.", "Better. Your lines are getting braver.", "You see bodies properly. I'd like to draw you one day."),
    G(cond(BRALESS), P("She looks at your tits the way she looks at the model, slow, measuring the weight, and doesn't pretend she isn't."),
      D(ART, "That's a good line today. I mean the shape under it, not the clothes. Not yet, anyway.")),
    G(cond(*SKIRT_WITH_BRA), P("She looks at your legs, hip to knee, like she's measuring them for paper."),
      D(ART, "That's a good line today. I mean the legs, not the skirt. Not yet, anyway.")),
]))
out.append(hub("hub_business_class", "lecture_hall", BUS, "business_lecturer_met", "The Business lecturer", [
    P("The Business lecturer is writing headings on the board in long straight lines."),
    # S4 (LO 2026-11-03): he's teaching, so the screen is look-only and says why
    P("He's mid-lecture, and he doesn't stop for anyone."),
    # reader batch 5 (pass 3): each band names the next rung, and 40+ names his office (his rows Mon/Wed/Thu/Fri 14:30-18:00)
    *grade_lines(BUS, "grade_business", "Failing. Retakes by appointment.", "Adequate. Seventy is good. You're not at seventy.",
                 "Good. Keep it that way. My door's open in the afternoons.",
                 r1=("Failing. Honest work only.", "Adequate. Seventy is good. You're not at seventy.", "Good. Keep it that way.")),
    clothes_line(BUS, "This isn't a beach, @player."),
], [go("Leave him to his lecture.", loc=LEAVE_TO["lecture_hall"])]))
out.append(hub("hub_ta_class", "lecture_hall", TA, "bio_ta_met", "The Biology TA", [
    P("The TA is sorting a stack of handouts at the front. She turns, sees you, and drops half of them."),
    # S4 (LO 2026-11-03): she's running the class, so the screen is look-only and says why
    P("She gathers them up and hands them out, too busy to stop. She only gets a word in as she puts one on your desk."),   # reader pass 3 b01: she talks below, so "too busy to talk" was false
    # reader a3 #19 (DECISIONS 131): the 40+ bands point at her office too (her rows: ta_office Tue-Fri 14:30-18:00)
    *grade_lines(TA, "grade_bio", "You're, um. You're struggling. My door's open. If you want.", "You're doing fine! Really fine. My door's open afternoons.", "Top marks. Wow. Sorry. Top marks. My door's open afternoons.",
                 r1=("You're, um. You're struggling. Sorry.", "You're doing fine! Really fine.", "Top marks. Wow. Sorry. Top marks.")),
    # writing pass 2026-11-04, reader test 2: how far she looks moves with Exhibitionism, her reaction to being seen
    G(cond(trait("exhibitionism", "lt", 20), {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}, {"type": "worn_type", "operator": "neq", "value": "short_skirt"}), P("She puts your handout down and doesn't look at you at all, but her neck is already pink.")),
    G(cond(trait("exhibitionism", "gte", 20), trait("exhibitionism", "lt", 40)), P("She puts your handout down, and her eyes slip to your mouth before she catches them.")),
    G(cond(trait("exhibitionism", "gte", 40), trait("exhibitionism", "lt", 60)), P("She gets to your desk last, on purpose. Her eyes go down your throat to your chest, and they stay a second longer than she means them to.")),
    G(cond(trait("exhibitionism", "gte", 60)), P("She stops at your desk and doesn't move on. She looks at your chest in front of the whole row, and the handout shakes in her hand."),
      D(TA, "Not in class. Please. Not in class.")),
    # reader a3 #35 (DECISIONS 131): the act she holds back, not only a compliment
    G(cond(BRALESS), P("Her eyes go to your chest, to the shape of you under the fabric, and jump back up to your face. Her neck goes pink."),
      D(TA, "You look— sorry. Nothing. You look nice."),
      P("Her eyes drop to your chest. She looks back at her clipboard, fast, and doesn't finish what she was saying.")),
    G(cond(*SKIRT_WITH_BRA), P("Her eyes go down your legs to the hem of your skirt and jump back up to your face. Her neck goes pink."),
      D(TA, "You look— sorry. Nothing. You look nice."),
      P("Her eyes drop to your chest. She looks back at her clipboard, fast, and doesn't finish what she was saying.")),
]))

# ── the offices (college_office_talk): art, business (the honest retake), TA, the dean ──
out.append(hub("hub_art_office", "art_office", ART, "art_lecturer_met", "The art lecturer's office", [
    P("Canvases against every wall. The art lecturer looks up from a sketch of a woman's back."),
    *grade_lines(ART, "grade_art", "Sit. Show me your book. Ah. Yes. We have work to do.", "You're improving. Draw every day.", "You have an eye. Come and sit for me some time."),
    G(cond(BRALESS), D(ART, "Stand by the window a moment. The light's good on you."),
      P("She's already looking at your tits under what you're wearing, the way she looks at the model, pencil moving."),
      D(ART, "Clothes on today. Some day you'll sit for me properly.")),
    G(cond(*SKIRT_WITH_BRA), D(ART, "Stand by the window a moment. The light's good on you."),
      P("She's already looking at your bare legs below the skirt, pencil moving."),
      D(ART, "Clothes on today. Some day you'll sit for me properly.")),
]))
# S4 (LO 2026-11-03): she isn't busy in her office, so one choice aimed at her. An hour, Figure drawing +1, cap 69.
_ao = out[-1]
_ao["nodes"][0]["choices"] = [go("Show her your sketchbook.", node="book", mins=0), go("Leave her to her drawings.", loc=LEAVE_TO["art_office"])]
_ao["nodes"].append(node("book", "Your sketchbook", [
    P("She turns the pages slowly, and stops on the figures. She takes a pencil and corrects a hip with three lines, without asking."),
    D(ART, "There. You keep drawing what you think a body does. Draw what it's doing."),
], [go("Thank her.", loc=LEAVE_TO["art_office"], mins=60, eff=[{"targetType": "player", "trait": "grade_art", "op": "add", "value": 1, "cap": 69}])]))
out.append(hub("hub_business_office", "business_office", BUS, "business_lecturer_met", "The Business lecturer's office", [
    P("The Business lecturer looks up from his marking and doesn't smile."),
    # scene reader 2026-11-04: the retake is once (business_retake_used is never cleared), so the offer shows only until it is used
    G(cond(trait("grade_business", "lt", 40), flag("business_retake_used")), D(BUS, "Failing. You've had your retake. Nothing else.")),
    G(cond(trait("grade_business", "lt", 40), flag("business_retake_used", False)), D(BUS, "Failing. I can offer an honest retake. Nothing else.")),
    *grade_lines(BUS, "grade_business", "", "You're passing. Keep it honest.", "Good work. Honest work.")[1:],
    # reader pass 3 b00: at 40+ a line points forward (his lecture is on his rows; the retake covers <40)
    G(cond(trait("grade_business", "gte", 40)), D(BUS, "I'll see you in lecture, @player. Front half of the room.")),
    # reader pass 3 b00: the charge is on her body, one group per clothing set; the price is his line
    G(cond(BRALESS), P("His eyes drop to your tits once, to your nipples pushing at the fabric, and come straight back up to your face. His pen doesn't stop."),
      D(BUS, "You can wear what you like. It won't change your grade. Nothing does.")),
    G(cond(*SKIRT_WITH_BRA), P("His eyes go down your bare thighs to the hem of your skirt once, and come straight back up to your face. His pen doesn't stop."),
      D(BUS, "You can wear what you like. It won't change your grade. Nothing does.")),
], [
    go("\"I'll take the retake.\"", node="retake", mins=5, cond_=cond(trait("grade_business", "lt", 40), flag("business_retake_used", False)),
       flags=[fset("business_retake_used")]),
    go(HUB_CLOSE[BUS], loc="faculty_floor"),
]))
out[-1]["nodes"].append(node("retake", "The retake", [
    P("He hands you a paper and points at a chair, and sits watching you for an hour without blinking. You know more than you thought."),
    D(BUS, "Honest work. Thank you."),
], [go("Hand it in.", loc="faculty_floor", mins=60, eff=[add("grade_business", 5)])]))
out.append(hub("hub_ta_office", "ta_office", TA, "bio_ta_met", "The TA's office", [
    P("The TA's office is half a room with a skeleton in the corner wearing a party hat. She jumps when you knock."),
    *grade_lines(TA, "grade_bio", "Oh! Hi. Your grade. Um. We should fix your grade. Sit?", "You're doing well. Do you want tea?", "You're my best student. Don't tell anyone I said that."),
    G(cond(BRALESS), P("She can't keep her eyes off your chest."),
      D(TA, "I like your— never mind. Sit down. Please."),
      P("She gets up to shut the door, stops with her hand on it, and leaves it open.")),
    G(cond(*SKIRT_WITH_BRA), P("Her eyes go down your legs when you sit, and stay."),
      D(TA, "I like your— never mind. Sit down. Please."),
      P("She gets up to shut the door, stops with her hand on it, and leaves it open.")),
]))
# S4 (LO 2026-11-03): a person who isn't busy gets one choice aimed at them. An hour of her help, Biology +1,
# capped at 69 so the top band is still earned in class.
_ta = out[-1]
_ta["nodes"][0]["choices"] = [go("Ask her to help you with Biology.", node="help", mins=0), go("\"It's fine. Really.\"", node="fine", mins=1)]
# scene reader b02 (2026-11-03): the no lands on a screen with her reply, and the hour of help it costs is said
_ta["nodes"].append(node("fine", "It's fine", [
    D(TA, "Oh. Okay. Sure. The offer's there. Afternoons, I'm always here."),
    P("She sits back down too fast and stares at her screen, red to the ears. No help today, and your Biology stays where it is."),
], [go("Leave her to it.", loc=LEAVE_TO["ta_office"])]))
_ta["nodes"].append(node("help", "Her help", [
    P("She pulls her chair round to your side of the desk and goes through your last lab with a pencil, too close, apologising every time her knee touches yours."),
    D(TA, "See? You had it, but you didn't believe it."),
], [go("Thank her.", loc=LEAVE_TO["ta_office"], mins=60, eff=[{"targetType": "player", "trait": "grade_bio", "op": "add", "value": 1, "cap": 69}])]))
# (2026-11-01) met on day 1 now
# (college_dean_office), so the warning line shows only after the warning call (dean_summons).
out.append(hub("hub_dean_office", "dean_office", DEAN, "dean_met", "The dean", [
    P("The dean doesn't get up. He waits for you to sit in the hard chair before he looks at you."),
    G(cond(flag("on_probation")), D(DEAN, "You're on probation. Every grade, every complaint, crosses my desk now.")),
    G(cond(flag("on_probation", False), flag("dean_summons")), D(DEAN, "You've had your warning. Don't make me write another letter.")),
    G(cond(flag("dean_summons", False)), D(DEAN, "Your timetable isn't decoration, @player. Use it.")),
    # scene reader b03 (2026-11-03): his read of her clothes lands on her body, and carries its price
    *by_clothes([P("His eyes stop on your chest, on your nipples pushing at the fabric with no bra under it, and stay there a beat too long for a dean.")],
                [P("His eyes go down to the hem of your skirt and the bare tops of your thighs, and stay there a beat too long for a dean.")],
                G(DARING_STATE, D(DEAN, "Is that what you wear to college? Wear it to my office again and it goes in your file."))),
]))
# S4 (LO 2026-11-03): one choice aimed at the dean. A talk, no counter: his answer reads her grades.
ANY_FAILING = cond(*[trait(g, "lt", 40) for g in ("grade_psych", "grade_business", "grade_bio", "grade_art")], logic="OR")
NONE_FAILING = [trait(g, "gte", 40) for g in ("grade_psych", "grade_business", "grade_bio", "grade_art")]
_dean = out[-1]
_dean["nodes"][0]["choices"] = [go("Ask about your grades.", node="grades", mins=0), go(HUB_CLOSE[DEAN], loc=LEAVE_TO["dean_office"])]
_dean["nodes"].append(node("grades", "Your grades", [
    P("He turns his screen so you can see it, and reads your grades off it without looking at you."),
    # adjacent groups render as one if/elseif chain (canv.G's docstring), so exactly one answer shows
    # pass 3 I60 (SYSTEMS.md:154, :471): probation clears when no grade is failing any more, here, on his word
    GC(cond(flag("on_probation"), *NONE_FAILING), D(DEAN, "All four back over the line. You're off probation. Don't make me put you back on it.")),
    GC(cond(flag("on_probation")), D(DEAN, "Every one of these goes up, or you go home. That's what probation means.")),
    GC(ANY_FAILING, D(DEAN, "Some of these worry me. Fix them before I have to.")),
    GC(cond(flag("on_probation", False)), D(DEAN, "Fine. Keep them there.")),
], [go("\"Thank you, sir.\"", loc=LEAVE_TO["dean_office"], mins=10, cond_=cond(flag("on_probation"), *NONE_FAILING), flags=[funset("on_probation")]),
    go("\"Yes, sir.\"", loc=LEAVE_TO["dean_office"], mins=10, cond_=cond(flag("on_probation", False), *ANY_FAILING["items"], logic="OR"))]))

# ── day 1, the dean's office (college_dean_office.md, signed 2026-11-01, DECISIONS 121): straight from the
#    opening's "Go to campus."; four screens; the timetable; "Go to Psychology." Time: the opening ends about
#    07:50, the walk is 15, so "You're already late" is said at about 08:35 (Psychology starts 08:30). ──
TIMETABLE_LINK = '<<link "Your timetable">><<run setup.openTimetable()>><</link>>'
out.append({
    "id": "college_dean_office", "name": "The dean's office",
    "description": "Day 1, Monday of week one, from the opening: the dean's look, his rules, the timetable, and \"Go to Psychology.\" Sets dean_met.",
    # Not bound to his face: his rows start at dean_met, which this scene sets (the meeting itself).
    "trigger": {"location": "dean_office", "is_repeatable": False, "priority": 10, "is_active": True,
                "schedules": [{"weekdays": [0], "start_time": "08:00", "end_time": "09:00"}],
                "conditions": cond(flag("opening_done"), flag("dean_met", False))},
    "nodes": [
        node("wait", "The dean's office", [
            P("The dean's office smells of carpet and old coffee. He's writing. He doesn't look up, and he doesn't ask you to sit, so you stand."),
            P("When he does look up, he takes his time. Your face, then down, then back up, slowly, like he's reading a form."),
            G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), D(DEAN, "Is that what you're wearing to class?")),
            G(cond({"type": "worn_type", "operator": "neq", "value": "short_skirt"}), D(DEAN, "You're the new one. @player.")),
        ], [go("\"Good morning.\"", node="rules", mins=20, flags=[fset("dean_met")])]),
        node("rules", "The rules", [
            D(DEAN, "Classes are not optional. Your grades come to me. Complaints come to me."),
            P("He taps a folder with one finger."),
            D(DEAN, "Two complaints and you're back in this office. I don't like seeing a student twice."),
        ], [go("\"I understand.\"", node="timetable", mins=5)]),
        node("timetable", "Your timetable", [
            P("He slides a printed sheet across the desk and keeps two fingers on it a second before he lets go."),
            D(DEAN, "Your timetable. Learn it."),
            P(TIMETABLE_LINK),
        ], [go("Fold it into your bag.", node="late", mins=5)]),
        node("late", "Already late", [
            P("He's already looking back at his writing."),
            D(DEAN, "Psychology. Lecture hall. You're already late."),
        ], [go("Go to Psychology.", loc="lecture_hall", mins=15)]),
    ]})

# ── the dean's warning: the call itself (8_phone.toml). It never says where she is and never moves her:
# both answers return her to where she was; the office opens on her map (dean_summons). ──
out.append({
    "id": "dean_warning", "name": "The dean's office",
    "description": "Her first trouble: the dean's warning, by phone. Meets the dean; sets dean_met, dean_summons, on_probation (if failing) and letter_home (laura_suspicion +10). Played by answering the dean's office's call; returns her to where she was.",
    "trigger": {"location": "dean_office", "is_repeatable": False, "priority": 1, "is_active": True, "substitution_only": True},
    "nodes": [node("warning", "The warning", [
        P("The dean's secretary puts you straight through. A dry voice, a man used to being listened to."),
        D(DEAN, "This is the dean. @player, I have your file open in front of me."),
        G(cond(trait("complaints", "gte", 2)), D(DEAN, "Complaints about your conduct in class. Your clothes. This is a college, not a stage.")),
        G(cond(flag("failing_noticed")), D(DEAN, "And your grades. You're failing. I'm putting you on probation.")),
        D(DEAN, "Your parents will be getting a letter. Consider this your warning. My door is on the faculty floor, if you want to argue."),
        T("A letter home. Laura is going to read every word of it."),
    ], [
        go("\"Yes, sir.\"", ret=True, mins=10, cond_=cond(flag("failing_noticed")),
           flags=[fset("dean_met"), fset("dean_summons"), fset("on_probation"), fset("letter_home")], eff=[add("laura_suspicion", 10, clamp=True)]),
        go("\"Yes, sir.\"", ret=True, mins=10, cond_=cond(flag("failing_noticed", False)),
           flags=[fset("dean_met"), fset("dean_summons"), fset("letter_home")], eff=[add("laura_suspicion", 10, clamp=True)]),
    ])]})

# ── Laura reads the grades (the failing chain): moved INTO her kitchen hub as nodes (laura.py PORTAL, pass 3
# C30, the-first-hour.md "a second surface ... is a node inside the first"). Was four solo canvases here. ──

# ── the gym (gym.md; on the street since DECISIONS 225, was campus_gym.md): work out, alone. Jake's training is his hub (jake.py). Once a day:
# `worked_out` cleared at midnight (the home brakes' rule, DECISIONS 77). A sports bra with nothing over
# it is Daring (the gym sheet), and that is when the mirror wall pays.
SPORTS_ONLY = [{"type": "clothing_item", "item_id": "sports_bra", "operator": "equipped"},
               {"type": "clothing_slot", "slot": "top", "operator": "unequipped"},
               {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}]
# Gym clothes (LO, 2026-11-08, DECISIONS 198; exhibition_study/GYM_CLOTHES_PLAN.md): the gym's ladder from normal
# to slutty. The floor reads what she trains in, one line per step, most daring first, each group closed off
# from the others so no two show together. Track pants and the tank open on day 1; the tiny shorts need
# Exhibitionism 40 and the sheer leggings 60 (their own wear locks, 0_systems_spec.toml).
SHEER = {"type": "worn_type", "operator": "eq", "value": "sheer_leggings"}
NOT_SHEER = {"type": "worn_type", "operator": "neq", "value": "sheer_leggings"}
SHORTS = {"type": "worn_type", "operator": "eq", "value": "gym_shorts"}
NOT_SHORTS = {"type": "worn_type", "operator": "neq", "value": "gym_shorts"}
TANK = {"type": "clothing_item", "item_id": "gym_tank", "operator": "equipped"}
NO_TANK = {"type": "clothing_item", "item_id": "gym_tank", "operator": "unequipped"}
TRACK = {"type": "worn_type", "operator": "eq", "value": "track_pants"}
LEGGINGS = {"type": "worn_type", "operator": "eq", "value": "leggings"}
TOP_ON = {"type": "clothing_slot", "slot": "top", "operator": "equipped"}
TSHIRT = {"type": "clothing_item", "item_id": "tshirt", "operator": "equipped"}

from gymkit import BOTTOM_OK, NO_OTHER_TOP, GYM_A, GYM_B, GYM_KITS, CHECKED_IN, NOT_GYM_CLOTHES, kits   # DECISIONS 225


GYM_ACC = "gym_accident_today"   # one gym accident a day, cleared at midnight (0_systems_spec.toml)


def exh(cap):
    return {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": cap}


GYM_FLOOR_BY_CLOTHES = [
    G(cond(SHEER),
      P("The sheer leggings go see-through under the gym lights, and you knew they would. Your ass shows through them on every squat. The whole floor has stopped pretending. Two guys at the rack, the one on the rowing machine, and the guy wiping down the benches all watch your ass go down and come up again."),
      WHO("Hey. Watch it. People bring their kids in here."),
      P("That's the guy at the front desk. He says it loud, and then he stays at his desk. He keeps watching too.")),
    G(cond(SHORTS, NOT_SHEER),
      P("The tiny gym shorts ride up your ass by the second set and stay there. You don't pull them down. Three guys drift over from the rack to use the bench right next to yours, and none of them does a single rep.")),
    G(cond(*SPORTS_ONLY, NOT_SHORTS, NOT_SHEER),
      P("Just the sports bra and your bottoms. Your tits bounce in it with every step across the floor, and in the mirror wall you can see two guys at the rack stop counting their reps. One looks away when you catch him. The other doesn't.")),
    G(cond(TANK, NOT_SHORTS, NOT_SHEER),
      P("The gym tank is tight on you and shows off everything. In the mirror wall a guy at the rack is watching your tits instead of his form. He drops his bar too early.")),
    G(cond(LEGGINGS, TSHIRT),
      P("Leggings and a T-shirt. In the mirror wall the leggings show the whole shape of your ass every time you bend.")),
    G(cond(TRACK, TSHIRT),
      P("Track pants and a T-shirt. Nobody looks twice, and you get a proper workout in.")),
]

out.append({
    "id": "gym_workout", "name": "Work out",
    "description": "The gym (the street, DECISIONS 225): checked in today, in gym clothes. 60 min, energy -15. What she trains in decides who looks: leggings under 20 open the mirror squat (+1, cap 19); a sports bra alone at Daring, +1 cap 39; the tiny shorts at 40, +1 cap 59; the sheer leggings at 60, +1 cap 79 (campus_gym.md, DECISIONS 198). Once a day.",
    "trigger": {"location": "gym_floor", "is_repeatable": True, "priority": 4, "is_active": True,
                "conditions": cond(CHECKED_IN, flag("worked_out", False)),
                # the gym accidents (below): 1 in 4 each, one a day; each checks its own clothes on its own trigger
                "substitutions": [{"target_canvas_id": c, "chance": 0.25, "conditions": cond(flag(GYM_ACC, False))}
                                  for c in ("gym_accident_shorts", "gym_accident_strap", "gym_accident_leggings")]},
    "nodes": [node("floor", "The gym floor", [
        P("Treadmill, then the weights, then the mats. The mirror wall shows you everything you're doing, and everyone else doing it too."),
        WHO("You using that bench, or can I jump in?"),   # LO 2026-11-03: someone on the gym floor
        *GYM_FLOOR_BY_CLOTHES,
        *NOT_GYM_CLOTHES,
    ], [
        # pass 3 D44 (the-surfaces.md R9): an act on her body ends on a screen of it, not a toast; the hour is on the button (H28)
        *kits(go("Work out.", node="worked", mins=60, costs=[{"trait": "energy", "value": 15}],
           eff=[add("energy", -15)], flags=[fset("worked_out")], cond_=cond(flag("worked_out", False)))),
        # the sports bra alone is kit B only (DECISIONS 225)
        go("Work out, and let them look.", node="looked", mins=60, costs=[{"trait": "energy", "value": 15}],
           # pass 4 E94: the two guys at the rack watch her, so campus talks (once a day, worked_out)
           eff=[add("energy", -15), exh(CAP_DARING), add("campus_talk", 1, clamp=False)],
           flags=[fset("worked_out")], cond_=cond(flag("worked_out", False), trait("exhibitionism", "gte", 20), *GYM_B, NOT_SHORTS, NOT_SHEER)),
        # exhibition phase 1 (LO, 2026-11-08): under Daring, in leggings, a look happens; she lets it go on
        *kits(go("Squat facing the mirror wall.", node="set", mins=60, costs=[{"trait": "energy", "value": 15}],
           eff=[add("energy", -15), exh(19)], flags=[fset("worked_out")],
           cond_=cond(flag("worked_out", False), trait("exhibitionism", "lt", 20), LEGGINGS))),
        # gym clothes (DECISIONS 198): the shorts are a Showing act, the sheer leggings a stage-4 one; each pays to its stage's top
        *kits(go("Stretch on the mats facing the rack.", node="mats", mins=60, costs=[{"trait": "energy", "value": 15}],
           eff=[add("energy", -15), exh(CAP_BOLD), add("campus_talk", 1, clamp=False)], flags=[fset("worked_out")],
           cond_=cond(flag("worked_out", False), trait("exhibitionism", "gte", 40), SHORTS, NOT_SHEER))),
        *kits(go("Do your squats anyway.", node="sheer", mins=60, costs=[{"trait": "energy", "value": 15}],
           eff=[add("energy", -15), exh(79), add("campus_talk", 1, clamp=False)], flags=[fset("worked_out")],
           cond_=cond(flag("worked_out", False), trait("exhibitionism", "gte", 60), SHEER,
                      {"type": "clothing_slot", "slot": "underwear", "operator": "equipped"}))),   # with no panties it shows her bare: On Display (80), not this release (DECISIONS 205)
        go("Not today.", loc="gym_floor"),
    ]),
    node("set", "The mirror wall", [
        P("You do your squats facing the mirror wall. In it, a guy at the rack has lost count of his reps. His eyes are on your ass every time you go down."),
        P("You finish the set where he can see: slow, all the way down, and up again with your face hot. He racks the bar and leaves without finishing his."),
        GC(cond(trait("exhibitionism", "lt", 5)), T("He was staring. You just didn't move.")),
        GC(cond(trait("exhibitionism", "lt", 10)), T("You went slower once you saw him looking.")),
        GC(cond(trait("exhibitionism", "lt", 15)), T("You knew he was counting your reps, not his.")),
        GC(cond(trait("exhibitionism", "lt", 20)), T("Leggings were never going to be enough for long.")),
        P("The guys at the rack are in most afternoons. So is the mirror wall."),
    ], [go("Towel off.", loc="gym_floor")]),
    node("worked", "The last set", [
        G(cond({"type": "worn_type", "operator": "neq", "value": "track_pants"}),
          P("You come off the last set dripping, your thighs burning, sweat running down between your tits. In the mirror wall a guy wiping down the next bench watches your ass all the way to the water fountain. He doesn't look away when you catch him.")),
        # in track pants with anything but the T-shirt the floor already had someone looking, so he still is
        G(cond(TRACK, {"type": "clothing_item", "item_id": "tshirt", "operator": "unequipped"}),
          P("You come off the last set dripping, your thighs burning, sweat running down between your tits. In the mirror wall a guy wiping down the next bench watches your ass all the way to the water fountain. He doesn't look away when you catch him.")),
        G(cond(TRACK, TSHIRT),
          P("You come off the last set dripping, your thighs burning, sweat running down between your tits under the T-shirt. Nobody's watching. The track pants did their job.")),
        P("The gym's open every day. The guys at the rack are in most afternoons."),
    ], [go("Towel off.", loc="gym_floor")]),
    node("looked", "Let them look", [
        P("You do the mats last, in the sports bra and nothing over it, and you stretch your hamstrings with your ass up toward the rack. Your tits sit heavy and damp in the bra, and your nipples are hard through it. The two guys at the rack have given up on their sets."),
        WHO("Jesus."),
        P("You hear it under the clank of the plates, and you hold the stretch a breath longer for him."),
        P("They're here most afternoons. They'll be looking for you tomorrow."),
    ], [go("Towel off.", loc="gym_floor")]),
    node("mats", "The mats", [
        # a small group seeing underwear-level skin is stage 3, Showing (the-heat-ladder.md H1, audience check 2026-11-08)
        P("You take the mat right in front of the bench and stretch out in the tiny shorts, legs wide, then folded over with your ass in the air. The shorts are up your crack, the bottom of your ass bare on both sides, and you leave them there. The three guys at the bench beside you aren't even holding their bars."),
        WHO("Bro. Bro, look."),
        P("You go into the next stretch slower, for all three of them. The back of your neck is hot, and between your legs is hotter."),
        GC(cond(trait("exhibitionism", "lt", 60)), T("They'll tell everybody. It'll be all over campus. Good.")),
        GC(cond({"type": "worn_exposure", "operator": "gte", "value": 0}), T("Let them talk. You'd do it again in less.")),
    ], [go("Towel off.", loc="gym_floor")]),
    node("sheer", "Squats in the sheer leggings", [
        P("You do your squats anyway, facing the mirror wall, with the lights straight through the sheer leggings. Every time you go down your ass spreads in them, and the whole floor can see it."),
        P("In the mirror you can see your own panties through the cloth, every line of them. So can the guy on the rowing machine. He's stopped rowing."),
        WHO("I said watch it."),
        P("The desk guy says it, and then he stays at the desk and watches the rest of your set with everybody else."),
        T("He can warn you all he likes. He's still looking."),
        P("Tomorrow the whole floor will be waiting to see what you wear."),
    ], [go("Towel off.", loc="gym_floor")]),
    ]})


# Gym accidents (DECISIONS 198): one a day, 1 in 4 each when she starts a workout, and each reads what she trains in. Whoever sees pays on the moment: there is no meter for a stranger at the
# rack, so the gym's talk goes to campus_talk on both answers (the-heat-ladder.md H5). Fixing it pays her nothing;
# letting it be is her choice and pays to the top of the act's own stage (H1; the-arc.md A4).
def gym_accident(cid, name, conds, blocks, fix, fix_text, let, let_gate, cap, let_text, hook):
    done = [add("energy", -15), add("campus_talk", 1, clamp=False)]
    flags = [fset(GYM_ACC), fset("worked_out")]
    cost = [{"trait": "energy", "value": 15}]
    return {"id": cid, "name": name,
            "description": f"Random gym accident (gym.md, DECISIONS 198, 225): {name}. 1 in 4, one a day; campus talk +1 on both answers, letting it be +1 to cap {cap}.",
            # opens from "Work out" (gym_workout's substitutions, 1 in 4), never on entry: the gym is a changing room now,
            # and a random event there would hide its Change Clothes link (gate `nothing one-time at the shop or wardrobe`)
            "trigger": {"location": "gym_floor", "is_repeatable": True, "priority": 5, "is_active": True, "substitution_only": True,
                        "conditions": cond(flag("opening_done"), CHECKED_IN, flag(GYM_ACC, False), flag("worked_out", False), *conds)},
            "nodes": [
                node("event", name, blocks, [
                    go(fix, node="fix", mins=60, costs=cost, eff=list(done), flags=list(flags)),
                    go(let, node="let", mins=60, costs=cost, eff=done + [exh(cap)], flags=list(flags), cond_=cond(*let_gate) if let_gate else None),
                ]),
                node("fix", fix.rstrip("."), [P(fix_text), P(hook)], [go("Towel off.", loc="gym_floor")]),
                node("let", let.rstrip("."), [P(let_text), P(hook)], [go("Towel off.", loc="gym_floor")]),
            ]}


out.append(gym_accident("gym_accident_leggings", "The leggings go see-through", [LEGGINGS, *GYM_A, {"type": "clothing_slot", "slot": "underwear", "operator": "equipped"}],
    [P("You bend for the bar on your second set, and a guy on the next bench clears his throat."),
     WHO("Hey. You know those go see-through, right? When you bend like that?"),
     P("In the mirror wall you see it. Under the gym lights your leggings have gone thin as tights over your ass, and your panties show right through them.")],
    "Pull your top down over your ass.",
    "You tug your top down as far as it goes and keep it there with one hand for the rest of the workout, face on fire. He goes back to his bench. He keeps glancing at your hand.",
    "Finish the set.", [], 19,
    "You don't cover up. You finish the set, slow, bending all the way down every time, and you know exactly what he's seeing through the leggings. He forgets his own set. When you stand up he's still holding the bar.",
    "He's on that bench most afternoons. He'll be watching what you wear next time."))

out.append(gym_accident("gym_accident_strap", "The strap slips", [*GYM_B, NOT_SHEER, trait("exhibitionism", "gte", 20)],
    [P("You're two minutes into a hard run on the treadmill when the sports bra gives up. One strap slides off your shoulder, and your left tit bounces right out of the cup, nipple and all, in the mirror wall."),
     P("The guy on the next treadmill nearly goes off the back of his.")],
    "Fix it fast.",
    "You slap the treadmill to a stop and yank the bra back up in one move, your face burning. He's still staring when you look round, and he doesn't pretend he wasn't.",
    "Keep running a few steps.", [trait("exhibitionism", "gte", 60)], 79,
    "You keep running. Three steps, four, five, your bare tit bouncing out of the bra for the whole row of treadmills, before you tuck it back in. You don't stop the machine. The guy next to you has stopped his.",
    "He runs at this time most days. He'll take the treadmill next to yours again."))

out.append(gym_accident("gym_accident_shorts", "The shorts ride up", [SHORTS, *GYM_A, NOT_SHEER, trait("exhibitionism", "gte", 40), {"type": "clothing_slot", "slot": "underwear", "operator": "equipped"}],
    [P("You're on the leg press with your knees up to your chest, and the tiny shorts ride all the way up. The whole crotch of them has pulled to one side. From where the guys at the rack are standing, they can see your panties, pulled tight between your legs, and the bare curve of your ass on either side.")],
    "Pull them down.",
    "You let the sled down and pull the shorts straight, quick. Somebody at the rack laughs. Your cheeks are red, and not from the press.",
    "Do the next rep.", [], CAP_BOLD,
    "You don't touch them. You do the next rep, and the one after, knees to your chest each time, the shorts pulled aside, your panties pulled tight between your legs, and nobody at the rack is lifting a thing.",
    "They train here most afternoons. Next time they'll find a reason to use the rack by the leg press."))

# ═════════════ CLASS ACCIDENTS (college.md "Accidents in class", DECISIONS 202) ═════════════
# The clothes go wrong on the way to her seat: the low-cut top when she bends, the short skirt on the tiered
# steps, the sheer blouse under a spilt bottle (CoT's malfunction marks: downblouse 330, flip 189, nipslip 109,
# A_cot.md:224; water goes see-through, :227). 1 in 4, one a day across all classes, opened from the class
# when she comes into the hall as a class starts (trigger_mode random, the street's pattern, town.py; the hall is no
# changing room, so a random event there hides nothing). Not a swap from the class: opening a class counts as its
# one visit that day, so a swapped-in accident would eat the class. Both answers end back in the hall at 0 minutes
# and the class link is still there. The room seeing it pays campus talk +1
# (H5: an accident pays whoever saw it); letting it be pays her +1 to the top of the stage it shows, gated there.
CLASS_ACC = "class_accident_today"
LOW_TOP = {"type": "clothing_item", "item_id": "low_top", "operator": "equipped"}
THIN_TOP = {"type": "clothing_item", "item_id": "thin_top", "operator": "equipped"}
SHORT_SKIRT = {"type": "worn_type", "operator": "eq", "value": "short_skirt"}
BRA_ON = {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}
PANTIES_ON = {"type": "clothing_slot", "slot": "underwear", "operator": "equipped"}
PANTIES_OFF = {"type": "clothing_slot", "slot": "underwear", "operator": "unequipped"}


def class_accident(cid, name, conds, blocks, fix, fix_text, let, let_gate, cap, let_text, hook):
    talk = [add("campus_talk", 1, clamp=False)]
    flags = [fset(CLASS_ACC)]
    return {"id": cid, "name": name,
            "description": f"Random class accident (college.md, DECISIONS 202-203): {name}. 1 in 4, one a day; campus talk +1" + (f" on both answers, letting it be +1 to cap {cap}." if let else "; only the fix this release (letting it be is On Display, 80)."),
            "trigger": {"location": "lecture_hall", "is_repeatable": True, "priority": 6, "is_active": True,
                        "trigger_mode": "random", "chance": 0.25, "schedules": "CLASS_STARTS",   # filled in below
                        "conditions": cond(flag("opening_done"), flag(CLASS_ACC, False), *conds)},
            "nodes": [
                node("event", name, blocks, [
                    go(fix, node="fix", mins=0, eff=list(talk), flags=list(flags)),
                    *([go(let, node="let", mins=0, eff=talk + [exh(cap)], flags=list(flags), cond_=cond(*let_gate) if let_gate else None)] if let else []),
                ]),
                node("fix", fix.rstrip("."), [*fix_text, P(hook)], [go("Wait for class.", loc="lecture_hall", mins=0)]),
                *([node("let", let.rstrip("."), [*let_text, P(hook)], [go("Wait for class.", loc="lecture_hall", mins=0)])] if let else []),
            ]}


PEN = "You drop your pen in the aisle and bend straight down for it from the hip."
out.append(class_accident("class_acc_downblouse_bra", "Down your top", [LOW_TOP, BRA_ON],
    [P(PEN + " The low-cut top falls open off your chest. The guy in the row behind gets the whole view down it: your bra, your tits pushed up in the cups, all of it."),
     WHO("Whoa. Hello.")],
    "Hand over your neckline.",
    [P("You clap a hand flat over your neckline and come up fast, red to the ears, but it's too late. He's grinning at you over his laptop."),
     T("Great. Now he knows what bra you wear.")],
    "Take your time with the pen.", [], 19,
    [P("You don't cover up. You take your time with the pen, and he takes his time looking, right down your top at your tits in the bra. You come up slow."),
     GC(cond(trait("exhibitionism", "lt", 10)), T("You only dropped a pen. That's all it was.")),
     GC(cond(trait("exhibitionism", "lt", 20)), T("He looked the whole time, and you let him.")),
     GC(cond(trait("exhibitionism", "gte", 20)), T("A pen. That's all it takes now."))],
    "He sits in that row every week. Now he watches your top more than the slides."))

out.append(class_accident("class_acc_downblouse_bare", "Down your top", [LOW_TOP, BRALESS],
    [P(PEN + " With no bra under it, the low-cut top just falls open. Your tits swing free inside it, bare, nipples and all, and the guy in the row behind sees every inch of them."),
     WHO("Oh, Jesus. Hello.")],
    "Hand over your neckline.",
    [P("You slap a hand over your chest and straighten up so fast your knee hits the desk. It doesn't help. He's still staring at the hand like it isn't there."),
     T("No bra. Of course today.")],
    "Take your time with the pen.", [trait("exhibitionism", "gte", 60)], 79,
    [P("You stay bent over. You let your bare tits hang in the open top for him while you fish for the pen, your nipples gone hard in the air of the hall. Then you come up and sit down like nothing happened, but your face is hot."),
     T("You knew it would fall open. You bent anyway.")],
    "He sits in that row every week. He saw what's under that top, and he'll be looking for it every time you bend."))

STAIRS = "The lecture hall goes up in steep tiers, and you're climbing to your row with three rows of guys sitting below you."
out.append(class_accident("class_acc_stairs_panties", "Up your skirt", [SHORT_SKIRT, PANTIES_ON],
    [P(STAIRS + " The short skirt doesn't stand a chance. From their seats they're looking straight up it, at your panties tight between your thighs, every step you take."),
     WHO("Nice. Keep going.")],
    "Hold your skirt down.",
    [P("You clamp your skirt to the backs of your thighs with one hand and take the last steps sideways, face burning, but somebody down there laughs anyway."),
     T("Never sitting at the back again.")],
    "Keep climbing.", [trait("exhibitionism", "gte", 40)], CAP_BOLD,
    [P("You don't touch the hem. You keep climbing, slow, one step at a time, and three rows look up your skirt at your panties and the curve of your ass the whole way to your seat.")],
    "They sit in those rows every week. Every time you climb those steps in a skirt, they'll look up."))

out.append(class_accident("class_acc_stairs_bare", "Up your skirt", [SHORT_SKIRT, PANTIES_OFF],
    [P(STAIRS + " Under the short skirt there's nothing. From their seats they're looking straight up it at your bare ass and everything between your legs, every step you take."),
     WHO("Holy shit. She's not wearing any.")],
    "Hold your skirt down.",
    [P("You slap a hand to the back of your skirt and take the rest of the steps sideways, thighs clamped, face on fire. The whispering starts behind you before you've sat down."),
     T("Everybody heard him say it.")],
    None, None, None, None,   # letting it be is On Display (80), not written this release (DECISIONS 203)
    "They sit in those rows every week. They know now what you wear under a skirt, or don't."))

WATER = "You're unscrewing your water bottle when the guy squeezing past knocks your elbow, and half of it goes straight down your front."
out.append(class_accident("class_acc_water_bra", "Soaked through", [THIN_TOP, BRA_ON],
    [P(WATER + " The sheer blouse goes clear the second it's wet. It sticks to you. Your bra shows through it like there's no blouse at all, and so does the shape of your tits in it."),
     WHO("Shit, sorry, sorry. I'll get you a, um. Wow.")],
    "Cover up with your bag.",
    [P("You hold your bag up against your chest for the whole of the walk to your seat, dripping. He doesn't stop saying sorry, but he doesn't stop looking either."),
     T("A see-through blouse and a full water bottle. Smart.")],
    "Let it dry on you.", [], 19,
    [P("You put the bag down. You sit there soaked, your bra and your tits showing through the wet blouse, and you wait for it to dry. Half the row finds a reason to look over."),
     GC(cond(trait("exhibitionism", "lt", 10)), T("It's only water. It'll dry.")),
     GC(cond(trait("exhibitionism", "lt", 20)), T("They looked, and you let them.")),
     GC(cond(trait("exhibitionism", "gte", 20)), T("You could have covered up. You didn't want to."))],
    "He sits on the end of your row. Until it dries, he's going to be looking."))

out.append(class_accident("class_acc_water_bare", "Soaked through", [THIN_TOP, BRALESS],
    [P(WATER + " The sheer blouse goes clear and sticks to your bare tits like wet paper. Your nipples are hard from the cold water, dark through the cloth, and everyone near enough can see all of it."),
     WHO("Shit. Sorry. Shit. I can see your, I'm sorry.")],
    "Cover up with your bag.",
    [P("You crush your bag to your chest and sit hunched behind it, cold and dripping, nipples aching under the wet cloth. He brings you a wad of paper towels and can't look at your face."),
     T("No bra. Of course today.")],
    "Let it dry on you.", [trait("exhibitionism", "gte", 60)], 79,
    [P("You don't cover up. You sit in the wet blouse with your bare tits and your hard nipples showing right through it, and you get your things out like nothing happened. The guy who knocked you can't stop looking."),
     T("Everyone can see them. You don't want it to dry.")],
    "He sits on the end of your row. The blouse won't dry for an hour, and he knows it."))

out.append({
    "id": "lecture_timetable", "name": "Read the timetable on the door",
    "description": "The timetable: when each class is. Writes nothing.",
    "trigger": {"location": "lecture_hall", "is_repeatable": True, "priority": 1, "is_active": True},
    "nodes": [node("timetable", "The timetable", [
        P("The timetable is taped to the door. Somebody has drawn a penis on Thursday, but nobody has rubbed it off."),
        P(TIMETABLE_LINK),
    ], [go("Done.", loc="lecture_hall")])]})

# ═════════════ THE BACK STACKS (library_back_stacks.md, DECISIONS 79) ═════════════
# A Good Girl way up: the couple is an event and pays nothing; "Stay behind the shelf." is her
# choice and pays corruption +1, cap 19. Nobody sees her. Once a day; it opens until 19:45 so
# its 15 minutes of exits land before the library closes at 20:00.
STACKS_SEEN = ("The back aisles are dead quiet. You run a finger along the spines and pull down your book. Then you hear it. A soft knock of books on wood, steady, over and over. A muffled sound under it. You turn the corner. Two seniors fill the dead end of the stacks. She is up on the edge of a low shelf, skirt shoved to her waist, legs locked round him. Her top is pushed up and her tits bounce with every thrust. His jeans hang open. You see his cock slide out of her, wet, and drive back in. His hand is clamped over her mouth. She moans into his palm anyway. Your face goes hot. You stop dead at the end of the aisle. Her nipples are hard. He thrusts again, and the books knock.")
STACKS_STAY = ("You step back behind the next shelf. Three books are missing at eye height. The senior's cock slides out of the girl, wet and shining, then thrusts back in. Her tits bounce with every push. Her nipples are dark and hard. His hand stays clamped over her mouth. She moans into his palm anyway. Her heels dig into his ass and pull him deeper. That is a real cock, inside a real woman, four feet from you. You should look away, but you don't. Your own nipples go tight. You are wet, and you press your thighs together hard. Your hands stay flat on the shelf. She shudders and comes against his palm, hips jerking. Two aisles over, a book trolley squeaks. You hold still behind the shelf with your book, nipples still tight, thighs clenched.")   # reader batch 5 (pass 3): she is still here, so "Move one aisle closer." is true after it
out.append({
    "id": "library_back_stacks", "name": "Find a book in the back stacks",
    "description": "Two seniors (22) in the back stacks: the look pays nothing; staying behind the shelf pays corruption +1, cap 19 (DECISIONS 78-79). Once a day.",
    "trigger": {"location": "library", "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 1,
                "schedules": sched(([0, 1, 2, 3, 4], "08:00", "19:45")), "conditions": cond(flag("opening_done"))},
    "nodes": [
        node("stacks", "The back stacks", [P(STACKS_SEEN),
            WHO("Shh. Quiet. Take my cock and keep quiet."),   # LO 2026-11-03: the senior, in her ear (the park's ceiling: no fuck)
            WHO("I can't. You're too deep. Oh God, I can't be quiet."),   # pass 3 B4: the girl, into his palm
            VID("a couple having sex against a bookshelf at the end of a library aisle, his hand over her mouth", "couple fucking in library stacks", "quiet library sex against bookshelf", pool_dir="sex/library_stacks_seen_t5"),
            # writing pass 2026-11-04, reader test 4: her thought by Corruption (the scene opens at any level)
            G(cond(trait("corruption", "lt", 20)), T("Walk away. Why aren't you walking away? They could turn around and see you.")),
            G(cond(trait("corruption", "gte", 20), trait("corruption", "lt", 40)), T("You wonder what that feels like, with his hand on your mouth and the whole library out there.")),
            G(cond(trait("corruption", "gte", 40), trait("corruption", "lt", 60)), T("You're not leaving. You want to see her come, and you want to see his face when he does.")),
            G(cond(trait("corruption", "gte", 60)), T("That should be you on that shelf. You want his cock, and you want that hand on your mouth."))],
            [go("Stay behind the shelf.", node="stay", mins=5, flags=[fset("saw_the_library_couple")]),
             go("Take the book and go.", loc="library", mins=5, flags=[fset("saw_the_library_couple")])]),
        node("stay", "Behind the shelf", [WHO("You're so wet. Not a sound, or they'll hear."), P(STACKS_STAY),
            VID("seen through a gap in library books, a couple having sex against the shelves", "voyeur watching couple in library", "peeking through bookshelf at couple sex", pool_dir="sex/library_stacks_stay_t5")],
            [go("Back to your desk.", loc="library", mins=10, eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 19}], flags=[fset("saw_the_library_couple")]),
             # C1 (DECISIONS 147): Corruption 5; still hidden, still stage 1. Its screen's exit pays +1, cap 19, and the
             # button pays nothing, so one visit pays +1 whichever way she goes (the-arc.md "+1 for an everyday act"; pass 3 G75)
             go("Move one aisle closer.", node="closer", mins=5, swl=True, cond_=cond(trait("corruption", "gte", 5)),
                flags=[fset("saw_the_library_couple")])]),
        node("closer", "One aisle closer", [
            P("You slide along to the next aisle, the one that backs right onto theirs. The gap between the books is a hand's width. They are close enough to touch."),
            P("You can see the wet shine on his cock every time he pulls out of her. You can hear it. Her tits bounce in his face, and he bites one, and she jerks against his hand and moans into it."),
            P("You hold your breath. If either of them turns their head, they're looking straight at you. Your nipples ache, and you are soaked."),
            WHO("God, you're tight. Don't make a sound."), WHO("Harder. Please. Harder, I don't care who hears."),
            VID("through a gap in library books, very close, a couple having sex against the shelves", "close up voyeur library sex through books", "peeking through bookshelf gap couple close", pool_dir="sex/library_stacks_closer_t5")],
            [go("Back to your desk.", loc="library", mins=10, eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 19}], flags=[fset("saw_the_library_couple")])]),
    ]})

# ── the cocky guy at the next easel (false lines a3 #17-19, DECISIONS 129): his Figure drawing rows need a face ──
out.append({
    "id": "hub_cocky_class", "name": "The next easel",
    "description": "The cocky guy in Figure drawing (his class rows, v2_state.json): a look and a line.",
    "trigger": {"location": "lecture_hall", "npc": COCKY, "requires_npc": COCKY, "is_repeatable": True, "priority": 6,
                "is_active": True, "conditions": cond(flag("cocky_guy_met"))},
    "nodes": [node("easel", "The next easel", [
        P("The cocky guy is at his easel in the horseshoe. He's looking at you, not the model."),
        POOL(D(COCKY, "You're better than the model, you know."),
             D(COCKY, "Sit closer next class. I draw better up close."), pid="cocky_class_lines"),
        # reader a3 #42 (DECISIONS 131): his price on a fixed line, until the Figure drawing midterm is behind her
        P("His eyes go down your tits and back up to your mouth, slow, and his pencil keeps moving."),   # reader a3 verify: her body in any outfit
        G(cond(flag("exam_art_done", False)), D(COCKY, "Midterm answers cost a look.")),
        G(cond(flag("exam_art_done")), D(COCKY, "Anything you want from me costs a look. You know that now.")),
        # reader a3 #42 (DECISIONS 131): her body, not only the hem
        G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), P("His eyes go down your thighs to your hem and stay there while his pencil keeps moving.")),
    ], [go("Talk with him a while.", node="talk", mins=0), go("Leave him to his drawing.", loc="campus")]),
    # reader a3, seen by the readers (DECISIONS 131): "Talk a while." showed no talk. A talk screen, his lines in a
    # shuffle bag (call B: a second and third pool line, no counter). Every entry a group on the trigger's own
    # condition, so the pool is one type (home_items.py's rule).
    node("talk", "At the next easel", [
        POOL(
            GC(cond(flag("cocky_guy_met")), D(COCKY, "You draw like you're scared of the paper. Push harder."),
               P("He reaches over and drags your charcoal down the page in one thick black line. His arm stays pressed against yours after."),
               D(COCKY, "Like that.")),
            GC(cond(flag("cocky_guy_met")), D(COCKY, "Hold still. I'm drawing your mouth."),
               P("He turns his pad round so you can see. It's your mouth, three times over, and in every one it's open."),
               D(COCKY, "That's how I'd keep it.")),
            GC(cond(flag("cocky_guy_met")), D(COCKY, "The lecturer hates me, but she still gives me top marks. Want to know why?"),
               ME("Why?"),
               D(COCKY, "I look properly. Same as I'm looking at you.")),
            pid="cocky_class_talk", bag=True),
    ], [go("Back to your easel.", loc="lecture_hall", mins=20)])]})

# everyday clothes by stage (DECISIONS 205): the crop top and the bodycon in the hall
CROP = {"type": "worn_type", "operator": "eq", "value": "crop_top"}
BODYCON = {"type": "worn_type", "operator": "eq", "value": "bodycon_dress"}
RACK = "Your bag's on the coat rack over the back row, and you have to stretch both arms up to get it down."
out.append(class_accident("class_acc_crop_bra", "The crop top rides up", [CROP, BRA_ON],
    [P(RACK + " The crop top goes up with your arms, right up over your bra, and the whole back row gets your bra and the bottom of your tits in it."),
     WHO("Don't stop on our account.")],
    "Grab it down.",
    [P("You yank the crop top down with one hand and get the bag with the other, face hot. You're quick, but not quick enough. Somebody in the back row claps, slowly."),
     T("Next time, the bag goes under the seat.")],
    "Take your time with the bag.", [trait("exhibitionism", "gte", 20)], CAP_DARING,   # the crop top is worn from 20; a bra flash is Daring (CoT's "Flash your bra" at its 2)
    [P("You don't pull it down. You take your time getting the strap off the hook, both arms up, your bra out for the back row the whole while. Then you let the top fall and go to your seat."),
     GC(cond(trait("exhibitionism", "lt", 25)), T("They looked, and you let them.")),
     GC(cond(trait("exhibitionism", "gte", 25)), T("You hung that bag up there on purpose. Didn't you."))],
    "The back row sits there every class. Now they watch that coat rack."))

out.append(class_accident("class_acc_crop_bare", "The crop top rides up", [CROP, BRALESS],
    [P(RACK + " There's no bra under the crop top, and it goes up with your arms. The bottoms of your bare tits slide out under the hem, full and heavy, nearly to the nipple."),
     WHO("Oh my God. Underboob. Hello.")],
    "Grab it down.",
    [P("You slap the hem down over your tits and get the bag in one grab, face burning. The back row is laughing and nudging each other."),
     T("No bra and a crop top. Genius.")],
    "Take your time with the bag.", [trait("exhibitionism", "gte", 60)], 79,
    [P("You keep your arms up. You work the strap off the hook as slow as you like while the bottoms of your bare tits hang out under the crop top for the whole back row, and a nipple slips out with them. Then you let it fall.")],
    "The back row sits there every class. Now none of them ever looks at the board when you reach for anything."))

SEAT = "You sit down, and the bodycon dress doesn't come with you. It rides up round your hips as you sit, and it stays there."
out.append(class_accident("class_acc_bodycon_panties", "The dress rides up", [BODYCON, PANTIES_ON],
    [P(SEAT + " The guy across the aisle has a straight view up it, to your panties pulled tight between your thighs."),
     WHO("Nice. Very nice.")],
    "Tug it down.",
    [P("You wriggle the dress back down your thighs in your seat, which only makes it worse for a second, and cross your legs hard. It's too late, but you try. He grins at you across the aisle."),
     T("This dress was a mistake. A tight, short mistake.")],
    "Leave it where it is.", [trait("exhibitionism", "gte", 40)], 59,
    [P("You leave it. You sit with the dress round your hips and your knees a little apart, your panties in plain view across the aisle, and you wait for the lecture to start.")],
    "He sits across the aisle every class. He'll be waiting for you to sit down again."))

out.append(class_accident("class_acc_bodycon_bare", "The dress rides up", [BODYCON, PANTIES_OFF],
    [P(SEAT + " There's nothing under it. The guy across the aisle has a straight view up the dress, and there's nothing between him and everything."),
     WHO("Oh my God. Nothing. She's got nothing on.")],
    "Tug it down.",
    [P("You shove the dress down and clamp your thighs shut, red to the roots of your hair. The whisper goes along the row before the lecturer has said a word."),
     T("Everybody in this row knows now.")],
    None, None, None, None,   # letting it be is On Display (80), not written this release (DECISIONS 203)
    "He sits across the aisle every class. He knows what's under that dress now, or isn't."))

# the class accidents roll in the class start windows (DECISIONS 202)
_starts = at_start(PSYCH + BUSI + BIO)   # the accidents are written for the tiered hall, not the easels; the class
# starts, not the 45 minutes the class is now open for (late entry, DECISIONS 235)
assert len(_starts) >= 4
for _c in out:
    if _c["id"].startswith("class_acc_"):
        _c["trigger"]["schedules"] = _starts

# heat proposal B10 (the gym), B16 (the lecture hall) and B20 (the office doors' hub lines), DECISIONS 147 chunk 3
import walkins_out
_done = walkins_out.attach(out)
assert _done == {"gym_workout", "lecture_timetable"}, _done
walkins_out.hub_read(out)

text = "# ── college (sheets/systems/college.md · scenes college_*.md) ──\n" + "".join(emit(c) for c in out)
open(__import__("sys").argv[1], "w").write(text)
print("college:", len(out), "canvases")
