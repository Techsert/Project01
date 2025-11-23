# learn_lvl2_T3.py - COMPLETE REPLACEMENT
# This is the ENTIRE file - delete everything and use only this

import pygame
import config
from video_slide_base import NavigableVideoSlidePlayer

# ==========================================================
# SLIDE DATA
# ==========================================================
SLIDES_T3 = [
    # Intro slide
##    {
##        "title": "Revision",
##        "background_image": {
##            "path": "../assets/img/alphabitSound/bg-nt.png",
##            "scale": (0.95, 0.78),
##            "position": "center"
##        },
##        "video": {
##            "path": "../assets/videos/Lvl1_Topic1_slide2_NoSound.mp4",
##            "audio_path": "../assets/sounds/Learn_lvl1_T1/lvl1_topic1_Slide2.wav",
##            "scale": (0.3, 0.5),
##            "position": "center"
##        },
##        "images": [
##            {"path": "../assets/img/boy01.png", "delay": 2000, "scale": (0.1, 0.1), "position": "bottom-right"},
##        ]
##    },
    
    # Slide 1 - حرف الألف
    {
        "title": "Revision LVL 2",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/main/NotReady.png", "sound": "", "delay": 0, "scale": (0.65, 0.45), "position": "center"}
        ]
    },
    
]
# ==========================================================
# RUN FUNCTION
# ==========================================================
def run_learn_lvl2_T3(screen, main_app):
    """Launch Topic 3"""
    player = NavigableVideoSlidePlayer(
        screen=screen,
        main_app=main_app,
        slides=SLIDES_T3,
        level=2,
        has_navigation=True  # Enable next/prev buttons
    )
    player.run()
