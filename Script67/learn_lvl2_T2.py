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
        "title": "FAT-HA",
        "narration": "../assets/sounds/learn_lvl2/learn_lvl2_T2.wav",
        "images": [
            # BASE
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/Learn_lvl1_T3/intro09.png", "delay": 0, "scale": (0.3, 0.6), "position": "left", "offset": {"x": 500, "y": 0}},
            
            # SEC 02
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 7000, "scale": (0.07, 0.05), "position": "center", "offset": {"x": 0, "y": 0}},

            {"path": "../assets/img/learn_lvl2/10ra.png", "delay": 9000, "scale": (0.05, 0.18), "position": "center", "offset": {"x": 1100, "y": 100}, "duration": 11500},
            {"path": "../assets/img/learn_lvl2/11zay01.png", "delay": 9000, "scale": (0.05, 0.18), "position": "center", "offset": {"x": 930, "y": 100}, "duration": 11500},
            {"path": "../assets/img/learn_lvl2/21kf.PNG", "delay": 9000, "scale": (0.1, 0.16), "position": "center", "offset": {"x": 700, "y": 100}, "duration": 11500},

            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 9000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 1150, "y": -55}, "duration": 11500, "flash_count": 3, "flash_speed": 400},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 9000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 955, "y": -55}, "duration": 11500, "flash_count": 3, "flash_speed": 400},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 9000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 700, "y": -55}, "duration": 11500, "flash_count": 3, "flash_speed": 400},

            {"path": "../assets/img/alphabitSound/Letters/03ta02.png", "delay": 21000, "scale": (0.09, 0.15), "position": "center", "offset": {"x": 1100, "y": -110}, "duration": None},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 21000, "scale": (0.05, 0.05), "position": "center", "offset": {"x": 1050, "y": -250}, "flash_count": 4, "flash_speed": 400, "duration": None},

            {"path": "../assets/img/alphabitSound/Letters/21kf01.png", "delay": 30000, "scale": (0.09, 0.15), "position": "center", "offset": {"x": 1100, "y": 250}},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 30000, "scale": (0.05, 0.05), "position": "center", "offset": {"x": 1050, "y": 120}, "flash_count": 4, "flash_speed": 400},       
            
        ],
        "texts": [
            # SEC 01
            {
                "text": "FAT-HA",
                "delay": 3800,
                "position": "center",
                "offset": {"x": 0, "y": -200},
                "size_ratio": 0.15,
                "color": (0, 100, 200),
                "bold": True,
                "flash_count": 0,
                "flash_speed": 0,
                "duration": None
            },
            # SEC 03
            {
                "text": "'A'",
                "delay": 14000,
                "position": "center",
                "offset": {"x": 0, "y": 300},
                "size_ratio": 0.2,
                "color": (0, 100, 200),
                "bold": True,
                "flash_count": 0,
                "flash_speed": 0,
                "duration": None
            },
            {
                "text": "TA",
                "delay": 25000,
                "position": "center",
                "offset": {"x": 700, "y": -50},
                "size_ratio": 0.16,
                "color": (236, 28, 36),
                "bold": False,
                "flash_count": 0,
                "flash_speed": 0,
                "duration": None
            },
            {
                "text": "QA",
                "delay": 32000,
                "position": "center",
                "offset": {"x": 700, "y": 300},
                "size_ratio": 0.16,
                "color": (236, 28, 36),
                "bold": False,
                "flash_count": 0,
                "flash_speed": 0,
                "duration": None
            },
            
        ]  
    },
    # Slide 1 - Alef
    {
        "title": "Alif FAT-HA",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/01alef.PNG", "sound": "../assets/sounds/Learn_lvl2/01Alef-F.wav", "delay": 0, "scale": (0.04, 0.4), "position": "center", "offset": {"x": 0, "y": 0}},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 1500, "scale": (0.05, 0.05), "position": "center", "offset": {"x": 0, "y": -325}, "flash_count": 2, "flash_speed": 400},
        ]
    },
    # Slide 2 - Ba
    {
       "title": "BA FAT-HA",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/02ba02.png", "sound": "../assets/sounds/Learn_lvl2/02Ba-F.wav", "delay": 0, "scale": (0.20, 0.22), "position": "center", "offset": {"x": 0, "y": 90}},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 1000, "scale": (0.05, 0.05), "position": "center", "offset": {"x": -100, "y": -275}, "flash_count": 2, "flash_speed": 400},
        ]
    },
    # Slide 3 Ta
    {
        "title": "حرف التاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/03ta.png", "sound": "../assets/sounds/Learn_lvl2/03Ta-F.wav", "delay": 0, "scale": (0.20, 0.20), "position": "center", "offset": {"x": 0, "y": -15}},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 1000, "scale": (0.05, 0.05), "position": "center", "offset": {"x": -100, "y": -275}, "flash_count": 2, "flash_speed": 400},
        ]
    },
        # Slide 4 - Tha
    {
        "title": "حرف الثاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/04tha.png", "sound": "../assets/sounds/Learn_lvl2/04Tha-F.wav", "delay": 0, "scale": (0.20, 0.24), "position": "center", "offset": {"x": 0, "y": -45}},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 1000, "scale": (0.05, 0.05), "position": "center", "offset": {"x": -100, "y": -275}, "flash_count": 2, "flash_speed": 400},
        ]
    },
            # Slide 5 - Gem
    {
        "title": "حرف الجيم",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/05geem.png", "sound": "../assets/sounds/Learn_lvl2/05-Geam-F.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 1000, "scale": (0.05, 0.05), "position": "center", "offset": {"x": -100, "y": -275}, "flash_count": 2, "flash_speed": 400},
        ]
    },
            # Slide 6 - 7a
    {
        "title": "حرف الحاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/06ha.png", "sound": "../assets/sounds/Learn_lvl2/06-7a-F.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 1000, "scale": (0.05, 0.05), "position": "center", "offset": {"x": -100, "y": -275}, "flash_count": 2, "flash_speed": 400},
        ]
    },
            # Slide 7 - 7'a
    {
        "title": "حرف الخاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/07ka.png", "sound": "../assets/sounds/Learn_lvl2/077'a-F.wav", "delay": 0, "scale": (0.15, 0.46), "position": "center", "offset": {"x": 0, "y": -78}},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 1000, "scale": (0.05, 0.05), "position": "center", "offset": {"x": -100, "y": -275}, "flash_count": 2, "flash_speed": 400},
        ]
    },
            # Slide 8 - Dal
    {
        "title": "حرف الدال",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/08dal.png", "sound": "../assets/sounds/alphabitSound/08dal.wav", "delay": 0, "scale": (0.10, 0.30), "position": "center"},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 1000, "scale": (0.05, 0.05), "position": "center", "offset": {"x": -100, "y": -275}, "flash_count": 2, "flash_speed": 400},
        ]
    },
            # Slide 9 - Thal
    {
        "title": "حرف الذال",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/09thal.png", "sound": "../assets/sounds/alphabitSound/09thal.wav", "delay": 0, "scale": (0.10, 0.40), "position": "center"},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 1000, "scale": (0.05, 0.05), "position": "center", "offset": {"x": -100, "y": -275}, "flash_count": 2, "flash_speed": 400},
        ]
    },
            # Slide 10 - Ra
    {
        "title": "حرف الراء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/10ra.png", "sound": "../assets/sounds/alphabitSound/10ra.wav", "delay": 0, "scale": (0.10, 0.35), "position": "center"},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 1000, "scale": (0.05, 0.05), "position": "center", "offset": {"x": -100, "y": -275}, "flash_count": 2, "flash_speed": 400},
        ]
    },
            # Slide 11 - Zay
    {
        "title": "حرف الزاي",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/11zay.png", "sound": "../assets/sounds/alphabitSound/11zay.wav", "delay": 0, "scale": (0.10, 0.40), "position": "center"},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 1000, "scale": (0.05, 0.05), "position": "center", "offset": {"x": -100, "y": -275}, "flash_count": 2, "flash_speed": 400},
        ]
    },
            # Slide 12 - Sen
    {
        "title": "حرف السين",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/12sen.png", "sound": "../assets/sounds/alphabitSound/12sen.wav", "delay": 0, "scale": (0.20, 0.35), "position": "center"},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 1000, "scale": (0.05, 0.05), "position": "center", "offset": {"x": -100, "y": -275}, "flash_count": 2, "flash_speed": 400},
        ]
    },
            # Slide 13 - Shen
    {
        "title": "حرف الشين",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/13shen.png", "sound": "../assets/sounds/alphabitSound/13shen.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 1000, "scale": (0.05, 0.05), "position": "center", "offset": {"x": -100, "y": -275}, "flash_count": 2, "flash_speed": 400},
        ]
    },
            # Slide 14 - Sad
    {
        "title": "حرف الصاد",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/14sad.png", "sound": "../assets/sounds/alphabitSound/14sad.wav", "delay": 0, "scale": (0.20, 0.35), "position": "center"}
        ]
    },
            # Slide 15 - Dad
    {
        "title": "حرف الضاد",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/15dad.png", "sound": "../assets/sounds/alphabitSound/15dad.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },
            # Slide 16 - Taa
    {
        "title": "حرف الطاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/16taa.png", "sound": "../assets/sounds/alphabitSound/16taa.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },
            # Slide 17 - Zaa
    {
        "title": "حرف الظاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/17zaa.png", "sound": "../assets/sounds/alphabitSound/17zaa.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },
            # Slide 18 - Aen
    {
        "title": "حرف العين",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/18aen.png", "sound": "../assets/sounds/alphabitSound/18ayn.wav", "delay": 0, "scale": (0.15, 0.40), "position": "center"}
        ]
    },
            # Slide 19 - Gaen
    {
        "title": "حرف الغين",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/19gean.png", "sound": "../assets/sounds/alphabitSound/19gean.wav", "delay": 0, "scale": (0.15, 0.45), "position": "center"}
        ]
    },
            # Slide 20 - Feh
    {
        "title": "حرف الفاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/20feh.png", "sound": "../assets/sounds/alphabitSound/20feh.wav", "delay": 0, "scale": (0.20, 0.30), "position": "center"}
        ]
    },
            # Slide 21 - Kf
    {
        "title": "حرف القاف",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/21kf.png", "sound": "../assets/sounds/alphabitSound/21kf.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 22 - Kaf
    {
        "title": "حرف الكاف",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/22kaf.png", "sound": "../assets/sounds/alphabitSound/22kaf.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 23 - Lam
    {
        "title": "حرف اللام",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/23lam.png", "sound": "../assets/sounds/alphabitSound/23lam.wav", "delay": 0, "scale": (0.10, 0.35), "position": "center"}
        ]
    },
            # Slide 24 - Meam
    {
        "title": "حرف الميم",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/24meam.png", "sound": "../assets/sounds/alphabitSound/24meam.wav", "delay": 0, "scale": (0.10, 0.35), "position": "center"}
        ]
    },
            # Slide 25 - Noon
    {
        "title": "حرف النون",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/25noon.png", "sound": "../assets/sounds/alphabitSound/25noon.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 26 - Heh
    {
        "title": "حرف الهاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/26heh.png", "sound": "../assets/sounds/alphabitSound/26heh.wav", "delay": 0, "scale": (0.15, 0.30), "position": "center"}
        ]
    },
                # Slide 27 - Waw
    {
        "title": "حرف الواو",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/27waw.png", "sound": "../assets/sounds/alphabitSound/27waw.wav", "delay": 0, "scale": (0.10, 0.35), "position": "center"}
        ]
    },
                # Slide 28 - Yaa
    {
        "title": "حرف الياء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/28yaa.png", "sound": "../assets/sounds/alphabitSound/28yaa.wav", "delay": 0, "scale": (0.20, 0.35), "position": "center"}
        ]
    },
                # End Slid
    {
        "title": "أحسنت",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/coach.png", "sound": "../assets/sounds/alphabitSound/welldone01.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
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

