"""Who says each quoted line in the signed prose (skill register.md "Speech is a UI component", LO 2026-11-03).

canv.emit() runs every canvas through canv.voice_canvas(), which cuts each paragraph that quotes speech into
narration and dialog blocks (canv.speech) by this table: canvas id -> {the words inside the quote marks: speaker}.
Speakers: "ME" (her), an npc id, "?" (a stranger with no NPC, rendered as speaker "unknown"), or "TEXT" (not a
voice: a text on a screen or code; the quote stays inside the paragraph, marked not_speech).
Each speaker was read from the scene: the attribution ("he says", "you tell him"), who is in the room, and who
the line answers. A canvas listed here must name every quote in its quoted paragraphs, or the build stops.
"""
R, K, L, M, Z, H, J = "npc_ryan", "npc_kayla", "npc_laura", "npc_mark", "npc_zoe", "npc_hale", "npc_jake"
ME, WHO, TEXT = "ME", "?", "TEXT"

SPEECH = {
    # ── Ryan ──
    "ryan_04_feet_in_his_lap": {"Yeah, babe. I'm alone.": R, "Mm-hm,": R},
    "ryan_05_thin_walls": {
        "Quiet. They'll hear.": R,
        "Harder. Don't stop. Right there, Ryan, right there.": K,   # Kayla, through the wall
        "What? ... Nothing?": K, "Nothing,": R, "Go to sleep.": R, "...@player.nickname?": R,
        "What was that?": K, "Pipes,": R,
        "Morning, @player.nickname.": K, "Morning,": ME, "Thin walls.": ME,
        "Shower's free. Go on. I'm not going anywhere.": K,
    },
    "ryan_06_after_the_shower": {"I heard you through the wall, @player.nickname.": R, "Babe?": K},
    "ryan_07_kayla_cant_know": {
        "@player.nickname. What are you doing?": R, "Jesus,": R,
        "Don't you dare.": ME, "Fuck. @player.nickname. She'll keep calling.": R, "Then let her.": ME,
        "@player.nickname, fuck, she's calling,": R,
    },
    "ryan_08_two_knocks_first_sex": {
        "@player.nickname,": R, "Fuck,": R, "Fuck, @player.nickname,": R, "@player.nickname": R,
        "Harder,": ME, "Laura,": R,
        "Quiet,": R, "Fuck. Quiet.": R,
        "Don't,": R, "Don't move.": R,
        "@player.nickname. I'm close.": R, "Inside,": ME, "Do it.": ME,
        "Close,": R, "Fuck. Don't move.": R,
        "I'm close,": R, "Fuck, @player.nickname.": R,
    },
    "hub_ryan_room": {
        # hot1: her teasing at his door
        "Texting Kayla?": ME, "Was.": R, "What's the pillow for, Ryan?": ME, "Nothing. Go away.": R,
        "Liar.": ME, "Not tonight. Ask me nicely tomorrow.": ME,
        "So what's Kayla worth? Dinner? Or does she just get your bed?": ME, "Get out, @player.nickname.": R,
        "You don't want me out.": ME, "Is that for Kayla too?": ME, "Night, Ryan. Maybe tomorrow.": ME,
        "Hey. What's Kayla worth to you? Out of ten.": ME, "Ten. Obviously.": R,
        "Liar. You put your phone down when I walked in.": ME, "Not tonight, Ryan. Keep the sock.": ME,
        # hot4: he watches from the chair
        "Jesus, @player.nickname,": R, "Look, don't touch,": ME, "I know, @player.nickname. I know.": R,
        "Rules are rules,": ME, "Then go slow,": R, "Let me see it, @player.nickname.": R,
        # hot5: she runs it
        "Keep looking,": R, "Slower,": ME, "@player.nickname, please.": R, "Now. Come on me.": ME,
        "Faster,": ME, "@player.nickname, I'm close.": R, "Not yet.": ME, "Now. All over me.": ME,
        "Ask,": ME, "Can I come, @player.nickname?": R, "No. Look at my cunt first.": ME, "Ask me nicely.": ME,
        "Please. Please let me.": R, "Go on. Right there.": ME,
    },
    "hub_ryan_kitchen": {"Eat your dinner, @player.nickname,": R},
    "hub_ryan_living_room": {
        "Comfy, @player.nickname?": R, "Feet, @player.nickname. Seriously?": R,
        "Don't start,": R, "Screw the game,": R,
        "What was that?": ME, "Nothing. Watch the game, @player.nickname.": R, "Say it. Out loud.": ME,
        "You're in your underwear and I'm hard. Happy?": R,
        "Problem?": ME, "Shut up.": R, "Tell me why you're fixing yourself, Ryan. Use the word.": ME,
        "Because my cock's hard, @player.nickname. Because of your tits.": R,
        "Everything okay down there?": ME, "It's fine.": R, "Then say why you did that.": ME,
        "Your ass. In those panties. It's making me hard.": R, "Louder.": ME,
        "Your ass is making my cock hard, @player.nickname.": R,
        "Slow,": R, "He's right there.": R,
        "Quiet,": ME, "Or he walks in.": ME,
        "@player,": M, "You two want popcorn?": M, "We're good,": ME,   # Mark calls from the next room
    },
    # ── Laura ──
    "laura_04_she_saw_you": {"Ryan.": L},
    "bathroom_shower": {"Leave some hot water, sweetheart!": L},
    # ── Mark ──
    "hub_mark_garage": {
        "Take your time, @player,": M, "Jesus, @player. Laura's in the house.": M,
        "Jesus, @player.": M,   # the same line on a Saturday, when Laura is out (mark.py, truth pass 2026-11-03)
        "You know what you look like right now, @player?": M, "That's not laundry, @player. That's a show.": M,
    },
    "hub_mark_kitchen": {"Salt.": M, "You missed one,": M},
    "mark_00_the_dryer": {"Tap's loose. Here.": M, "@player. Take the towel.": M},
    "home_event_mark_asleep": {"Leave it, @player,": M},
    # ── Zoe ──
    "zoe_03_hot_tub": {
        "Make room, babe's here.": Z, "Your tits are floating, babe,": Z,
        "Going in for more drinks.": WHO,   # one of her friends
        "Take it off, babe,": Z, "Just for me. Nobody else is here.": Z,
        "Everything on you is wet anyway. I can see your nipples, babe. I want to see your tits.": Z,
        "Babe,": Z, "Look at you.": Z, "You came in like that? All night?": Z,
        "Took you long enough, babe.": Z, "You could've asked,": ME,
        "@player.nickname. Where've you been?": R, "Zoe's.": ME,   # Ryan on the landing
    },
    "zoe_05_no_dare": {"Say it, babe.": Z, "Lick me,": ME, "Please.": ME},
    "hub_zoe_quad": {"Let them.": Z},
    "zoe_dares": {
        "Start the song,": ME, "Eyes only,": Z, "Look all you want,": ME,
        "Till the song ends, babe,": Z,
        "Not those,": ME, "Say please.": ME, "Please,": "npc_cocky_guy", "Good boy,": Z,
        "Slower,": Z, "Her nipples. Yes. Like that.": Z,   # Zoe telling him how
    },
    "park_hidden": {"Quiet, babe,": Z},
    "zoe_bathroom_face": {"Two minutes!": ME},
    # ── Hale ──
    "hale_04_claire_knocks": {
        "Tell me what you feel, @player. Bare your tits first.": H, "Out loud,": H,
        "Your thumb. My nipple's going hard.": ME, "Again.": H, "It's hot. The heat goes all the way down.": ME,
        "Say it.": H, "I'm wet. Your hand on my tit is making me wet.": ME,
        "Keep talking.": H, "Your hand is on my ribs,": ME, "My thigh.": ME, "The inside. Higher.": ME,
        "Right there,": ME,
    },
    "hale_thursdays": {
        "Tell me what you feel, @player.": H, "Your hands,": ME, "Be specific.": H,
        "You're squeezing my tits,": ME, "My nipples are hard.": ME, "Good. Go on.": H,
        "I feel it between my thighs.": ME, "I'm wet.": ME,
        "Stand there,": H, "Tell me what you feel.": H, "Your hands on my ass,": ME, "I feel hot. I feel wet.": ME,
        "And now?": H, "Where is the heat, @player?": H, "Between my thighs,": ME, "And here?": H,
        "My nipples. They're hard.": ME,
        "Top off, @player.": H, "Touch yourself. Tell me what you feel.": H, "It's hot,": ME,
        "It's swollen. I want your hand there.": ME,
        "Describe it, @player. Precisely.": H, "Small circles. It aches.": ME, "Keep talking.": H,
        "My nipples are hard. My thighs are shaking.": ME, "More detail.": H, "It's swollen,": ME,
        "Please don't stop.": ME,
        "Slower,": H, "Now tell me.": H, "I'm close,": ME, "I'm so close it hurts.": ME,
    },
    # ── Jake ──
    "jake_03_my_boyfriend": {
        "Is anyone up?": J, "Nobody,": ME, "Not yet.": ME, "Shame,": J, "I want them to see you're mine, @player.": J,
        "God, @player,": J,
        "Ryan, this is Jake. My boyfriend.": ME, "Great.": R, "Your brother hates me.": J,
        "Next Saturday?": TEXT,   # Jake's text on her phone
        "Okay, @player. Next Saturday, then?": J, "Next Saturday,": ME,
    },
    "jake_04_sneak_him_in": {
        "Look at you, gorgeous,": J, "Fuck me,": ME, "Fuck, gorgeous,": J,
        "Shh, gorgeous. The whole house will hear.": J,
    },
    "jake_saturday_date": {
        "God, you're gorgeous,": J, "C'mon, gorgeous. Right here.": J, "God, you're so wet.": J,
        "Hands on the wheel,": ME, "@player,": J, "Oh god, @player.": J,
        "Quiet, gorgeous,": J, "Fuck, gorgeous,": J,
    },
    # ── the café ──
    "cafe_shift": {
        "Are you on the menu?": WHO, "Ten,": WHO,   # the guys in the back booth
        "I get off when you stop staring at my tits.": ME, "I'll think about it,": ME,
        "Not today, hon.": ME, "Doll,": "npc_gary", "Your food's here, sir.": ME,
    },
    # ── college ──
    "college_class_figure": {"Look at the weight of her,": "npc_art_lecturer", "Draw that.": "npc_art_lecturer"},
    "meet_figure": {"First thing you learn,": "npc_art_lecturer", "She's not a shape. Get that weight down, the tits, the thighs, all of it.": "npc_art_lecturer"},
    "college_dean_office": {"Your timetable": TEXT},   # a SugarCube <<link>> label, not a voice
    "lecture_timetable": {"Your timetable": TEXT},
    # ── home ──
    "living_couch": {"Jesus, @player.nickname.": R},
    "ryan_door_ajar": {"@player.nickname.": R},
    "garden_sun": {"Somebody's going to look out a window,": R},
    "home_event_ryan_towel": {"Not here. Mom's up.": R},
    "home_event_ryan_door": {"Night, @player.nickname,": R},
    # ── town ──
    "town_event_whistle": {"Get in, baby. I'll give you a ride.": WHO},
    "street_seen_nopanties": {"Come in a minute.": WHO, "Get in.": WHO},
}
