# learn_lvl2_T2.py - COMPLETE REPLACEMENT
# This is the ENTIRE file - delete everything and use only this

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
        "title": "Arabic Alphabet Sounds",
        "narration": "../assets/sounds/learn_lvl2/learn_lvl2_T2.ogg",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/Learn_lvl1_T3/intro09.png", "delay": 0, "scale": (0.3, 0.6), "position": "left", "offset": {"x": 500, "y": 0}},

            {"path": "../assets/img/learn_lvl2/10ra.png", "delay": 5500, "scale": (0.05, 0.18), "position": "center", "offset": {"x": 700, "y": 100}},
            {"path": "../assets/img/learn_lvl2/11zay01.png", "delay": 5500, "scale": (0.05, 0.18), "position": "center", "offset": {"x": 530, "y": 100}},
            {"path": "../assets/img/learn_lvl2/21kf.PNG", "delay": 5500, "scale": (0.1, 0.16), "position": "center", "offset": {"x": 300, "y": 100}},

            {"path": "../assets/img/main/delete_icon.png", "delay": 6500, "duration": 7000, "scale": (0.06, 0.1), "position": "center", "offset": {"x": -150, "y": 0}, "flash_count": 20, "flash_speed": 200},

            {"path": "../assets/img/main/delete_icon.png", "delay": 10500, "duration": 3000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 750, "y": -235}, "flash_count": 5, "flash_speed": 200},
            {"path": "../assets/img/main/delete_icon.png", "delay": 10500, "duration": 3000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 555, "y": -235}, "flash_count": 5, "flash_speed": 200},
            {"path": "../assets/img/main/delete_icon.png", "delay": 10500, "duration": 3000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 300, "y": -235}, "flash_count": 5, "flash_speed": 200},

            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 17000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 750, "y": -35}, "duration": 4000},
            {"path": "../assets/img/learn_lvl2/kasra.png", "delay": 17000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 555, "y": 260}, "duration": 4000},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 17000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 300, "y": -35}, "duration": 4000},

            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 22000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 750, "y": -35}, "duration": 8000},
            {"path": "../assets/img/learn_lvl2/kasra.png", "delay": 23000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 555, "y": 260}, "duration": 7000},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 22000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 300, "y": -35}, "duration": 8000},

            {"path": "../assets/img/learn_lvl2/dama.png", "delay": 30000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 950, "y": -250}},
            {"path": "../assets/img/learn_lvl2/dd.png", "delay": 30000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 800, "y": -250}},
            {"path": "../assets/img/learn_lvl2/fat7a.png", "delay": 30000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 650, "y": -250}},
            {"path": "../assets/img/learn_lvl2/FF-kk.png", "delay": 30000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 500, "y": -250}},
            {"path": "../assets/img/learn_lvl2/shada.png", "delay": 30000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 350, "y": -250}},
            {"path": "../assets/img/learn_lvl2/sh-d.png", "delay": 30000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 200, "y": -250}},
            {"path": "../assets/img/learn_lvl2/sh-f.png", "delay": 30000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 50, "y": -250}},
            {"path": "../assets/img/learn_lvl2/sokon.png", "delay": 30000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": -100, "y": -250}},

            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 38000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 300, "y": -35}, "flash_count": 5, "flash_speed": 200},
            {"path": "../assets/img/learn_lvl2/kasra.png", "delay": 39500, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 555, "y": 260}, "flash_count": 5, "flash_speed": 200},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 41000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 750, "y": -35}, "flash_count": 5, "flash_speed": 200},
            
            


            
            
            
        ],
        "texts": [
            {
                "text": "Ra",
                "delay": 9000,
                "position": "center",
                "offset": {"x": 750, "y": -150},
                "size_ratio": 0.06,
                "color": (0, 100, 200),
                "bold": True,
                "flash_count": 0,
                "flash_speed": 0,
                "duration": 4500
            },
            {
                "text": "Zay",
                "delay": 10000,
                "position": "center",
                "offset": {"x": 555, "y": -150},
                "size_ratio": 0.06,
                "color": (0, 100, 200),
                "bold": True,
                "flash_count": 0,
                "flash_speed": 0,
                "duration": 3500
            },
            {
                "text": "Qaf",
                "delay": 10500,
                "position": "cwnter",
                "offset": {"x": 300, "y": -150},
                "size_ratio": 0.06,
                "color": (0, 100, 200),
                "bold": True,
                "flash_count": 0,
                "flash_speed": 0,
                "duration": 3000
            }
        ]  # ✅ ADDED COMMA HERE
    },  # ✅ This comma was already here
    # Other
    {
        "title": "الحُروف العَرَبية",
        "narration": "../assets/sounds/alphabitSound/intro.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/hard.png", "delay": 4000, "scale": (0.25, 0.55), "position": "center"},
        ]
    },
    # Slide 1 - Alef
    {
        "title": "حرف الألف",
        "narration": "../assets/sounds/alphabitSound/01alef-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/01alef.png", "delay": 0, "scale": (0.05, 0.50), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/01alef-f.png", "sound": "../assets/sounds/alphabitSound/01alef-f.wav", "delay": 3000, "scale": (0.05, 0.45), "position": "center-right", "offset": {"x": -200, "y": 0}},
            {"path": "../assets/img/alphabitSound/01alef-k.png", "sound": "../assets/sounds/alphabitSound/01alef-k.wav", "delay": 7000, "scale": (0.05, 0.45), "position": "center"},
            {"path": "../assets/img/alphabitSound/01alef-d.png", "sound": "../assets/sounds/alphabitSound/01alef-d.wav", "delay": 10000, "scale": (0.05, 0.45), "position": "center-left", "offset": {"x": 180, "y": 0}}
        ]
    },
    # Slide 2 - Ba
    {
       "title": "حرف الباء",
        "narration": "../assets/sounds/alphabitSound/02ba-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/02ba.png", "delay": 0, "scale": (0.20, 0.45), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/02ba-f.png", "sound": "../assets/sounds/alphabitSound/02ba-f.wav", "delay": 3000, "scale": (0.15, 0.40), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/02ba-k.png", "sound": "../assets/sounds/alphabitSound/02ba-k.wav", "delay": 7000, "scale": (0.15, 0.40), "position": "center", "offset": {"x": 0, "y": 70}},
            {"path": "../assets/img/alphabitSound/02ba-d.png", "sound": "../assets/sounds/alphabitSound/02ba-d.wav", "delay": 11000, "scale": (0.15, 0.40), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
]
# ==========================================================
# RUN FUNCTION
# ==========================================================
def run_learn_lvl2_T2(screen, main_app):
    """Launch Topic 2 - Alphabet Sounds (with navigation)."""
    print("[RUNNING] learn_lvl2_T2.run_learn_lvl2_T2")
    player = NavigableVideoSlidePlayer(
        screen=screen,
        main_app=main_app,
        slides=SLIDES_T2,
        level=2,
        has_navigation=True
    )
    player.topic = "T2"  # ✅ SET TOPIC IDENTIFIER
    player.run()

    # ✅ Mark completion after player exits
    profile_name = main_app.selected_profile.get("name") if main_app.selected_profile else None
    if profile_name:
        mark_learning_topic_complete(profile_name, 2, "T2")
        print(f"✅ Completed Learning Level 2 - Topic T2")

