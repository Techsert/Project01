# learn_lvl1_T2.py - Alphabet Names

import pygame
import config
from video_slide_base import NavigableVideoSlidePlayer
from profile_system import mark_learning_topic_complete


# ==========================================================
# SLIDE DATA
# ==========================================================
SLIDES_T2 = [
    # Intro slide
    {
        "title": "Alphabet Names",
        "background_image": {
            "path": "../assets/img/alphabitSound/bg-tr.png",
            "scale": (0.95, 0.80),
            "position": "center"
        },
        "video": {
            "path": "../assets/videos/Lvl1_Topic1_slide2_NoSound.mp4",
            "audio_path": "../assets/sounds/Learn_lvl1_T1/lvl1_topic1_Slide2.wav",
            "scale": (0.3, 0.5),
            "position": "center"
        },
##        "images": [
##            {"path": "../assets/img/boy01.png", "delay": 2000, "scale": (0.1, 0.1), "position": "bottom-right"},
##        ]
    },
    
    # Slide 1 - حرف الألف
    {
        "title": "أ",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/01alef.png", "scale": (0.04, 0.4),
             "sound": "../assets/sounds/alphabitSound/01alef.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },

    # Slide 2 - Ba
    {
        "title": "ب",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/02ba.png", "scale": (0.20, 0.22), "offset": {"x": 0, "y": 90},
             "sound": "../assets/sounds/alphabitSound/02ba.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
        # Slide 3 - Ta
    {
        "title": "ت",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/03ta.png", "scale": (0.20, 0.20), "offset": {"x": 0, "y": -15},
             "sound": "../assets/sounds/alphabitSound/03ta.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
        # Slide 4 - Tha
    {
        "title": "ث",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/04tha.png", "scale": (0.20, 0.24), "offset": {"x": 0, "y": -45},
             "sound": "../assets/sounds/alphabitSound/04tha.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 5 - Gem
    {
        "title": "ج",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/05geem.png", "scale": (0.15, 0.35), "offset": {"x": 0, "y": 100},
             "sound": "../assets/sounds/alphabitSound/05geem.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 6 - 7a
    {
        "title": "ح",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/06ha.png", "scale": (0.15, 0.35), "offset": {"x": 0, "y": 100},
             "sound": "../assets/sounds/alphabitSound/06-7a.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 7 - 7'a
    {
        "title": "خ",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/07ka.png", "scale": (0.15, 0.46), "offset": {"x": 0, "y": 22},
             "sound": "../assets/sounds/alphabitSound/07-7-a.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 8 - Dal
    {
        "title": "د",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/08dal.png", "scale": (0.08, 0.20), "offset": {"x": 0, "y": -12},
             "sound": "../assets/sounds/alphabitSound/08dal.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 9 - Thal
    {
        "title": "ذ",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/09thal.png", "scale": (0.08, 0.30), "offset": {"x": 0, "y": -85},
             "sound": "../assets/sounds/alphabitSound/09thal.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 10 - Ra
    {
        "title": "ر",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/10ra.png", "scale": (0.08, 0.25), "offset": {"x": 0, "y": 75},
             "sound": "../assets/sounds/alphabitSound/10ra.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 11 - Zay
    {
        "title": "ز",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/11zay.png", "scale": (0.08, 0.35), "offset": {"x": 0, "y": 3},
             "sound": "../assets/sounds/alphabitSound/11zay.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 12 - Sen
    {
        "title": "س",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/12sen.png", "scale": (0.18, 0.20), "offset": {"x": 0, "y": 110},
             "sound": "../assets/sounds/alphabitSound/12sen.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 13 - Shen
    {
        "title": "ش",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/13shen.png", "scale": (0.18, 0.32), "offset": {"x": 0, "y": 25},
             "sound": "../assets/sounds/alphabitSound/13shen.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 14 - Sad
    {
        "title": "ص",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/14sad.png", "scale": (0.18, 0.20), "offset": {"x": 0, "y": 110},
             "sound": "../assets/sounds/alphabitSound/14sad.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 15 - Dad
    {
        "title": "ض",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/15dad.png", "scale": (0.18, 0.27), "offset": {"x": 0, "y": 58},
             "sound": "../assets/sounds/alphabitSound/15dad.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 16 - Taa
    {
        "title": "ط",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)}, 
            {"path": "../assets/img/alphabitSound/Letters/16taa.png", "scale": (0.13, 0.27), "offset": {"x": 0, "y": -68},
             "sound": "../assets/sounds/alphabitSound/16taa.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 17 - Zaa
    {
        "title": "ظ",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/17zaa.png", "scale": (0.13, 0.27), "offset": {"x": 0, "y": -68},
             "sound": "../assets/sounds/alphabitSound/17zaa.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 18 - Aen
    {
        "title": "ع",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/18aen.png", "scale": (0.10, 0.275), "offset": {"x": 0, "y": 53},
             "sound": "../assets/sounds/alphabitSound/18ayn.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 19 - Gaen
    {
        "title": "غ",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/19gean.png", "scale": (0.10, 0.35),
             "sound": "../assets/sounds/alphabitSound/19gean.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 20 - Feh
    {
        "title": "ف",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/20feh.png", "scale": (0.18, 0.22), "offset": {"x": 0, "y": -30},
             "sound": "../assets/sounds/alphabitSound/20feh.wav", "sound_repeat": 3,  "sound_interval": 14000}
        ]
    },
            # Slide 21 - Kf
    {
        "title": "ق",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/21kf.png", "scale": (0.13, 0.28),
             "sound": "../assets/sounds/alphabitSound/21kf.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 22 - Kaf
    {
        "title": "ك",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/22kaf.png", "scale": (0.13, 0.35),
             "sound": "../assets/sounds/alphabitSound/22kaf.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 23 - Lam
    {
        "title": "ل",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/23lam.png", "scale": (0.08, 0.39), "offset": {"x": 0, "y": 25},
             "sound": "../assets/sounds/alphabitSound/23lam.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 24 - Meam
    {
        "title": "م",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/24meam.png", "scale": (0.08, 0.30),
             "sound": "../assets/sounds/alphabitSound/24meam.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 25 - Noon
    {
        "title": "ن",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/25noon.png", "scale": (0.15, 0.25),
             "sound": "../assets/sounds/alphabitSound/25noon.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
            # Slide 26 - Heh
    {
        "title": "هـ",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/26heh.png", "scale": (0.13, 0.20), "offset": {"x": 0, "y": -10},
             "sound": "../assets/sounds/alphabitSound/26heh.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
                # Slide 27 - Waw
    {
        "title": "و",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/27waw.png", "scale": (0.08, 0.25), "offset": {"x": 0, "y": 75},
             "sound": "../assets/sounds/alphabitSound/27waw.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
                # Slide 28 - Yaa
    {
        "title": "ي",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/28yaa.png", "scale": (0.15, 0.21), "offset": {"x": 0, "y": 40},
             "sound": "../assets/sounds/alphabitSound/28yaa.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },
                # End Slid
    {
        "title": "Well Done",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/coach.png",
             "sound": "../assets/sounds/alphabitSound/welldone01.wav", "scale": (0.20, 0.40)}
        ]
    },


    
]

# ==========================================================
# RUN FUNCTION
# ==========================================================
def run_learn_lvl1_T2(screen, main_app):
    """Launch Topic 2 - Alphabet Names (with navigation)."""
    print("[RUNNING] learn_lvl1_T2.run_learn_lvl1_T2")
    player = NavigableVideoSlidePlayer(
        screen=screen,
        main_app=main_app,
        slides=SLIDES_T2,
        level=1,
        has_navigation=True
    )
    player.topic = "T2"  # ✅ SET TOPIC IDENTIFIER
    player.run()

    # ✅ Mark completion after player exits
    profile_name = main_app.selected_profile.get("name") if main_app.selected_profile else None
    if profile_name:
        mark_learning_topic_complete(profile_name, 1, "T2")
        print(f"✅ Completed Learning Level 1 - Topic T2")
