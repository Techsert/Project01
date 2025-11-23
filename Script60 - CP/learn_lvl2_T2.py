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
        "title": "LVL 2 Intro",
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
        "title": "LVL 2 ",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/01alef.png", "sound": "../assets/sounds/alphabitSound/01alef.wav", "delay": 0, "scale": (0.04, 0.40), "position": "center"}
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

