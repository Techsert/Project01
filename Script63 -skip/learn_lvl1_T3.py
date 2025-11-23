# learn_lvl1_T3.py - COMPLETE REPLACEMENT
# This is the ENTIRE file - delete everything and use only this

import pygame
import config
from video_slide_base import NavigableVideoSlidePlayer
from profile_system import mark_learning_topic_complete


# ==========================================================
# SLIDE DATA
# ==========================================================
SLIDES_T3 = [
    {
        "title": "Introduction To The Arabic Language",
        "background_image": {
            "path": "../assets/img/alphabitSound/bg-tr.png",
            "scale": (0.95, 0.8),
            "position": "center"
        },
        "video": {
            "path": "../assets/videos/Lvl1_Topic3_slide1.mp4",
            "audio_path": "../assets/sounds/Learn_lvl1_T3/Lvl1_Topic3_slide1.wav",
            "scale": (0.3, 0.5),
            "position": "center"
        }
    },
    
    # Slide 1 - حرف الألف
    {
        "title": "Revision",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/main/NotReady.png", "sound": "", "delay": 0, "scale": (0.65, 0.45), "position": "center"}
        ]
    },
    
]

# ==========================================================
# RUN FUNCTION
# ==========================================================
def run_learn_lvl1_T3(screen, main_app):
    """Launch Topic 3."""
    player = NavigableVideoSlidePlayer(
        screen=screen,
        main_app=main_app,
        slides=SLIDES_T3,
        level=1,
        has_navigation=True
    )
    player.topic = "T3"  # ✅ SET TOPIC IDENTIFIER
    player.run()

    # ✅ Mark completion after player exits
    profile_name = main_app.selected_profile.get("name") if main_app.selected_profile else None
    if profile_name:
        mark_learning_topic_complete(profile_name, 1, "T3")
        print(f"✅ Completed Learning Level 1 - Topic T3")
