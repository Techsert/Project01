# learn_lvl1_T2.py - COMPLETE REPLACEMENT
# This is the ENTIRE file - delete everything and use only this

import pygame
import config
from video_slide_base import NavigableVideoSlidePlayer

# ==========================================================
# SLIDE DATA
# ==========================================================
SLIDES_T2 = [
    # Intro slide
    {
        "title": "Alphabet Names",
        "background_image": {
            "path": "../assets/img/alphabitSound/bg-nt.png",
            "scale": (0.95, 0.78),
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
        "title": "حرف الألف",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/01alef.png", "sound": "../assets/sounds/alphabitSound/01alef.wav", "delay": 0, "scale": (0.04, 0.40), "position": "center"}
        ]
    },

    # Slide 2 - Ba
    {
        "title": "حرف الباء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/02ba.png", "sound": "../assets/sounds/alphabitSound/02ba.wav", "delay": 0, "scale": (0.20, 0.30), "position": "center"}
        ]
    },
        # Slide 3 - Ta
    {
        "title": "حرف التاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/03ta.png", "sound": "../assets/sounds/alphabitSound/03ta.wav", "delay": 0, "scale": (0.20, 0.35), "position": "center"}
        ]
    },
        # Slide 4 - Tha
    {
        "title": "حرف الثاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/04tha.png", "sound": "../assets/sounds/alphabitSound/04tha.wav", "delay": 0, "scale": (0.20, 0.38), "position": "center"}
        ]
    },
            # Slide 5 - Gem
    {
        "title": "حرف الجيم",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/05geem.png", "sound": "../assets/sounds/alphabitSound/05geem.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 6 - 7a
    {
        "title": "حرف الحاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/06ha.png", "sound": "../assets/sounds/alphabitSound/06-7a.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 7 - 7'a
    {
        "title": "حرف الخاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/07ka.png", "sound": "../assets/sounds/alphabitSound/07-7-a.wav", "delay": 0, "scale": (0.15, 0.45), "position": "center"}
        ]
    },
            # Slide 8 - Dal
    {
        "title": "حرف الدال",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/08dal.png", "sound": "../assets/sounds/alphabitSound/08dal.wav", "delay": 0, "scale": (0.10, 0.30), "position": "center"}
        ]
    },
            # Slide 9 - Thal
    {
        "title": "حرف الذال",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/09thal.png", "sound": "../assets/sounds/alphabitSound/09thal.wav", "delay": 0, "scale": (0.10, 0.40), "position": "center"}
        ]
    },
            # Slide 10 - Ra
    {
        "title": "حرف الراء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/10ra.png", "sound": "../assets/sounds/alphabitSound/10ra.wav", "delay": 0, "scale": (0.10, 0.35), "position": "center"}
        ]
    },
            # Slide 11 - Zay
    {
        "title": "حرف الزاي",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/11zay.png", "sound": "../assets/sounds/alphabitSound/11zay.wav", "delay": 0, "scale": (0.10, 0.40), "position": "center"}
        ]
    },
            # Slide 12 - Sen
    {
        "title": "حرف السين",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/12sen.png", "sound": "../assets/sounds/alphabitSound/12sen.wav", "delay": 0, "scale": (0.20, 0.35), "position": "center"}
        ]
    },
            # Slide 13 - Shen
    {
        "title": "حرف الشين",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/13shen.png", "sound": "../assets/sounds/alphabitSound/13shen.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },
            # Slide 14 - Sad
    {
        "title": "حرف الصاد",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/14sad.png", "sound": "../assets/sounds/alphabitSound/14sad.wav", "delay": 0, "scale": (0.20, 0.35), "position": "center"}
        ]
    },
            # Slide 15 - Dad
    {
        "title": "حرف الضاد",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/15dad.png", "sound": "../assets/sounds/alphabitSound/15dad.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },
            # Slide 16 - Taa
    {
        "title": "حرف الطاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/16taa.png", "sound": "../assets/sounds/alphabitSound/16taa.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },
            # Slide 17 - Zaa
    {
        "title": "حرف الظاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/17zaa.png", "sound": "../assets/sounds/alphabitSound/17zaa.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },
            # Slide 18 - Aen
    {
        "title": "حرف العين",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/18aen.png", "sound": "../assets/sounds/alphabitSound/18ayn.wav", "delay": 0, "scale": (0.15, 0.40), "position": "center"}
        ]
    },
            # Slide 19 - Gaen
    {
        "title": "حرف الغين",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/19gean.png", "sound": "../assets/sounds/alphabitSound/19gean.wav", "delay": 0, "scale": (0.15, 0.45), "position": "center"}
        ]
    },
            # Slide 20 - Feh
    {
        "title": "حرف الفاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/20feh.png", "sound": "../assets/sounds/alphabitSound/20feh.wav", "delay": 0, "scale": (0.20, 0.30), "position": "center"}
        ]
    },
            # Slide 21 - Kf
    {
        "title": "حرف القاف",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/21kf.png", "sound": "../assets/sounds/alphabitSound/21kf.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 22 - Kaf
    {
        "title": "حرف الكاف",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/22kaf.png", "sound": "../assets/sounds/alphabitSound/22kaf.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 23 - Lam
    {
        "title": "حرف اللام",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/23lam.png", "sound": "../assets/sounds/alphabitSound/23lam.wav", "delay": 0, "scale": (0.10, 0.35), "position": "center"}
        ]
    },
            # Slide 24 - Meam
    {
        "title": "حرف الميم",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/24meam.png", "sound": "../assets/sounds/alphabitSound/24meam.wav", "delay": 0, "scale": (0.10, 0.35), "position": "center"}
        ]
    },
            # Slide 25 - Noon
    {
        "title": "حرف النون",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/25noon.png", "sound": "../assets/sounds/alphabitSound/25noon.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 26 - Heh
    {
        "title": "حرف الهاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/26heh.png", "sound": "../assets/sounds/alphabitSound/26heh.wav", "delay": 0, "scale": (0.15, 0.30), "position": "center"}
        ]
    },
                # Slide 27 - Waw
    {
        "title": "حرف الواو",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/27waw.png", "sound": "../assets/sounds/alphabitSound/27waw.wav", "delay": 0, "scale": (0.10, 0.35), "position": "center"}
        ]
    },
                # Slide 28 - Yaa
    {
        "title": "حرف الياء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/28yaa.png", "sound": "../assets/sounds/alphabitSound/28yaa.wav", "delay": 0, "scale": (0.20, 0.35), "position": "center"}
        ]
    },
                # End Slid
    {
        "title": "أحسنت",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/coach.png", "sound": "../assets/sounds/alphabitSound/welldone01.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
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
        has_navigation=True  # Enable next/prev buttons
    )
    player.run()
