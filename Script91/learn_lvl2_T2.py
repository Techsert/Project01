# learn_lvl2_T2.py - FAT-HAH

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
        "title": "FAT-HAH",
        "narration": "../assets/sounds/learn_lvl2/learn_lvl2_T2.wav",
        "images": [
            # BASE
##            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/Learn_lvl1_T3/intro09.png", "scale": (0.3, 0.6)},
            
            # SEC 02
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 7000, "scale": (0.07, 0.05), "offset": {"x": -750, "y": 0}},

            {"path": "../assets/img/learn_lvl2/10ra.png", "delay": 9000, "scale": (0.05, 0.18), "offset": {"x": 1000, "y": 0}, "duration": 11500},
            {"path": "../assets/img/learn_lvl2/11zay01.png", "delay": 9000, "scale": (0.05, 0.18), "offset": {"x": 830, "y": 0}, "duration": 11500},
            {"path": "../assets/img/learn_lvl2/21kf.PNG", "delay": 9000, "scale": (0.1, 0.16), "offset": {"x": 600, "y": 0}, "duration": 11500},

            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 9000, "scale": (0.03, 0.05), "offset": {"x": 1050, "y": -155}, "duration": 11500, "flash_count": 3, "flash_speed": 400},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 9000, "scale": (0.03, 0.05), "offset": {"x": 855, "y": -155}, "duration": 11500, "flash_count": 3, "flash_speed": 400},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 9000, "scale": (0.03, 0.05), "offset": {"x": 600, "y": -155}, "duration": 11500, "flash_count": 3, "flash_speed": 400},

            {"path": "../assets/img/alphabitSound/Letters/03ta02.png", "delay": 21000, "scale": (0.09, 0.15), "offset": {"x": 1100, "y": -160}, "duration": None},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 21000, "scale": (0.05, 0.05), "offset": {"x": 1050, "y": -300}, "flash_count": 4, "flash_speed": 400, "duration": None},

            {"path": "../assets/img/alphabitSound/Letters/21kf01.png", "delay": 30000, "scale": (0.09, 0.15), "offset": {"x": 1100, "y": 200}},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 30000, "scale": (0.05, 0.05), "offset": {"x": 1050, "y": 70}, "flash_count": 4, "flash_speed": 400},       
            
        ],
        "texts": [
            # SEC 01
            {
                "text": "FAT-HAH",
                "delay": 3800,
                "position": "center",
                "offset": {"x": -750, "y": -200},
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
                "offset": {"x": -750, "y": 300},
                "size_ratio": 0.19,
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
                "offset": {"x": 600, "y": -115},
                "size_ratio": 0.19,
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
                "offset": {"x": 600, "y": 250},
                "size_ratio": 0.19,
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
        "title": "أ",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/01alef.PNG", "scale": (0.04, 0.4),
             "sound": "../assets/sounds/Learn_lvl2/01Alef-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 1500, "scale": (0.05, 0.05), "offset": {"x": 0, "y": -325},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7500},
        ]
    },
    # Slide 2 - Ba
    {
       "title": "ب",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/02ba02.png", "scale": (0.20, 0.22), "offset": {"x": 0, "y": 90},
             "sound": "../assets/sounds/Learn_lvl2/02Baa-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 1000, "scale": (0.07, 0.07), "offset": {"x": -100, "y": -175},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
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

