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
        "title": "Alif",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/01alef.png", "scale": (0.04, 0.4),
             "sound": "../assets/sounds/alphabitSound/01alef.wav", "sound_repeat": 3,  "sound_interval": 10000}
        ]
    },

    # Slide 2 - Ba
    {
        "title": "Baa",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/02ba.png", "scale": (0.20, 0.22), "offset": {"x": 0, "y": 90},
             "sound": "../assets/sounds/alphabitSound/02ba.wav", "sound_repeat": 3,  "sound_interval": 10000}
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
