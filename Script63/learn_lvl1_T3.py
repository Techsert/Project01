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
##    {
##        "title": "Introduction To The Arabic Language",
##        "background_image": {
##            "path": "../assets/img/alphabitSound/bg-tr.png",
##            "scale": (0.95, 0.8),
##            "position": "center"
##        },
##        "video": {
##            "path": "../assets/videos/Lvl1_Topic3_slide1.mp4",
##            "audio_path": "../assets/sounds/Learn_lvl1_T3/Lvl1_Topic3_slide1.wav",
##            "scale": (0.3, 0.5),
##            "position": "center"
##        }
##    },
    
    # Slide 1 - حرف الألف
    {
        "title": "Revision",
        "narration": "../assets/sounds/Learn_lvl1_T3/Learn_lvl1_T3-1.wav",
        "images": [
##            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/bg-ft.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/Learn_lvl1_T3/intro09.png", "delay": 0, "scale": (0.1, 0.4), "position": "left", "offset": {"x": 250, "y": 50}},
            {"path": "../assets/img/main/Strongest01.png", "delay": 7500, "scale": (0.4, 0.3), "position": "center", "offset": {"x": 0, "y": 0}, "duration": 4000},
            {"path": "../assets/img/main/Qurann.png", "delay": 14000, "scale": (0.3, 0.5), "position": "center", "offset": {"x": 0, "y": 0}, "duration": 4000},
            {"path": "../assets/img/main/28letters.png", "delay": 19000, "scale": (0.3, 0.2), "position": "center", "offset": {"x": 0, "y": 0}, "duration": 3000},
            {"path": "../assets/img/main/arrows.png", "delay": 22500, "scale": (0.3, 0.5), "position": "center", "offset": {"x": 700, "y": 0}, "duration": 4000},



            
            {"path": "../assets/img/Learn_lvl1_T3/intro09.png", "delay": 30000, "scale": (0.1, 0.4), "position": "left", "offset": {"x": 250, "y": 50}, "sound": "../assets/sounds/Learn_lvl1_T3/Learn_lvl1_T3-2.wav"},

            {"path": "../assets/img/alphabitSound/Letters/01alef.png", "delay": 39500, "scale": (0.02, 0.15), "position": "right", "offset": {"x": -400, "y": -265}},
            
            {"path": "../assets/img/alphabitSound/Letters/02ba.png", "delay": 40000, "scale": (0.07, 0.07), "position": "right", "offset": {"x": -520, "y": -170}},
            
            {"path": "../assets/img/alphabitSound/Letters/03ta.PNG", "delay": 40600, "scale": (0.07, 0.07), "position": "center", "offset": {"x": 775, "y": -205}},
            
            {"path": "../assets/img/alphabitSound/Letters/04tha.PNG", "delay": 41000, "scale": (0.07, 0.07), "position": "center", "offset": {"x": 450, "y": -205}},
            
            {"path": "../assets/img/alphabitSound/Letters/05geem.PNG", "delay": 41700, "scale": (0.05, 0.13), "position": "center", "offset": {"x": 170, "y": -250}},            
            {"path": "../assets/img/alphabitSound/Letters/06ha.png", "delay": 42200, "scale": (0.05, 0.13), "position": "center", "offset": {"x": -80, "y": -250}},            
            {"path": "../assets/img/alphabitSound/Letters/07ka.PNG", "delay": 42700, "scale": (0.05, 0.18), "position": "center", "offset": {"x": -340, "y": -285}},
            
            {"path": "../assets/img/alphabitSound/Letters/08dal.PNG", "delay": 43200, "scale": (0.04, 0.09), "position": "center", "offset": {"x": -580, "y": -220}},            
            {"path": "../assets/img/alphabitSound/Letters/09thal.PNG", "delay": 44000, "scale": (0.04, 0.13), "position": "center", "offset": {"x": -800, "y": -250}},
            
            {"path": "../assets/img/alphabitSound/Letters/10ra.PNG", "delay": 44500, "scale": (0.04, 0.09), "position": "left", "offset": {"x": 630, "y": -220}},
            {"path": "../assets/img/alphabitSound/Letters/11zay.PNG", "delay": 45000, "scale": (0.04, 0.13), "position": "left", "offset": {"x": 400, "y": -250}},

            
            
            {"path": "../assets/img/alphabitSound/Letters/12sen.PNG", "delay": 45500, "scale": (0.07, 0.09), "position": "right", "offset": {"x": -550, "y": 100}},
            {"path": "../assets/img/alphabitSound/Letters/13shen.PNG", "delay": 46100, "scale": (0.07, 0.15), "position": "right", "offset": {"x": -860, "y": 65}},

            {"path": "../assets/img/alphabitSound/Letters/14sad.PNG", "delay": 46600, "scale": (0.07, 0.1), "position": "center", "offset": {"x": 420, "y": 105}},
            {"path": "../assets/img/alphabitSound/Letters/15dad.PNG", "delay": 47100, "scale": (0.07, 0.13), "position": "center", "offset": {"x": 100, "y": 80}},

            {"path": "../assets/img/alphabitSound/Letters/16taa.PNG", "delay": 47700, "scale": (0.07, 0.13), "position": "center", "offset": {"x": -220, "y": 20}},
            {"path": "../assets/img/alphabitSound/Letters/17zaa.PNG", "delay": 48300, "scale": (0.07, 0.13), "position": "center", "offset": {"x": -535, "y": 20}},

            {"path": "../assets/img/alphabitSound/Letters/18aen.PNG", "delay": 48900, "scale": (0.05, 0.12), "position": "center", "offset": {"x": -820, "y": 25}},            
            {"path": "../assets/img/alphabitSound/Letters/19gean.PNG", "delay": 49500, "scale": (0.05, 0.16), "position": "center", "offset": {"x": -1075, "y": 0}},

            

            {"path": "../assets/img/alphabitSound/Letters/20feh.PNG", "delay": 49900, "scale": (0.07, 0.1), "position": "right", "offset": {"x": -450, "y": 350}},
            {"path": "../assets/img/alphabitSound/Letters/21kf.PNG", "delay": 50600, "scale": (0.06, 0.1), "position": "right", "offset": {"x": -780, "y": 350}},

            {"path": "../assets/img/alphabitSound/Letters/22kaf.PNG", "delay": 51000, "scale": (0.07, 0.15), "position": "center", "offset": {"x": 530, "y": 315}},
            {"path": "../assets/img/alphabitSound/Letters/23lam.PNG", "delay": 51600, "scale": (0.05, 0.15), "position": "center", "offset": {"x": 230, "y": 310}},

            {"path": "../assets/img/alphabitSound/Letters/24meam.PNG", "delay": 52300, "scale": (0.03, 0.15), "position": "center", "offset": {"x": 0, "y": 310}},
            {"path": "../assets/img/alphabitSound/Letters/25noon.PNG", "delay": 52900, "scale": (0.05, 0.1), "position": "center", "offset": {"x": -240, "y": 350}},

            {"path": "../assets/img/alphabitSound/Letters/26heh.PNG", "delay": 53400, "scale": (0.06, 0.1), "position": "center", "offset": {"x": -550, "y": 350}},

            {"path": "../assets/img/alphabitSound/Letters/27waw.PNG", "delay": 53900, "scale": (0.06, 0.1), "position": "center", "offset": {"x": -870, "y": 350}},

            {"path": "../assets/img/alphabitSound/Letters/28yaa.PNG", "delay": 54400, "scale": (0.06, 0.1), "position": "left", "offset": {"x": 475, "y": 350}},
            
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
