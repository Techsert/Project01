# learn_lvl2_T1.py - COMPLETE REPLACEMENT


from video_slide_base import VideoSlidePlayer
from profile_system import mark_learning_topic_complete


# ==========================================================
# SLIDE DATA
# ==========================================================
SLIDES_T1 = [
    {
        "title": "Introduction",
        "narration": "../assets/sounds/Learn_lvl2_T1/intro.ogg",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/bg_ft.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/Learn_lvl1_T3/intro09.png", "delay": 0, "scale": (0.3, 0.6), "position": "center", "offset": {"x": 0, "y": 0}},
            
            {"path": "../assets/img/alphabitSound/Letters/01alef.png", "delay": 5500, "scale": (0.03, 0.2), "position": "center", "offset": {"x": 1000, "y": -265}},
            
            {"path": "../assets/img/alphabitSound/Letters/02ba.png", "delay": 6000, "scale": (0.1, 0.1), "position": "center", "offset": {"x": 500, "y": -170}},
            
            {"path": "../assets/img/alphabitSound/Letters/03ta.PNG", "delay": 6500, "scale": (0.1, 0.1), "position": "center", "offset": {"x": 1000, "y": 205}},
            
            {"path": "../assets/img/alphabitSound/Letters/04tha.PNG", "delay": 7500, "scale": (0.1, 0.1), "position": "center", "offset": {"x": 500, "y": 205}},


            {"path": "../assets/img/learn_lvl2_T1/baa.png", "delay": 30500, "scale": (0.1, 0.16), "position": "center", "offset": {"x": -400, "y": 0}},
            {"path": "../assets/img/learn_lvl2_T1/fat7a.png", "delay": 29000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": -475, "y": -170}},
            {"path": "../assets/img/learn_lvl2_T1/baa.png", "delay": 30500, "scale": (0.1, 0.16), "position": "center", "offset": {"x": -830, "y": 0}},
            {"path": "../assets/img/learn_lvl2_T1/kasra.png", "delay": 29300, "scale": (0.03, 0.05), "position": "center", "offset": {"x": -930, "y": 140}},
            {"path": "../assets/img/learn_lvl2_T1/baa.png", "delay": 30500, "scale": (0.1, 0.16), "position": "left", "offset": {"x": 300, "y": 0}},
            {"path": "../assets/img/learn_lvl2_T1/dama.png", "delay": 29600, "scale": (0.03, 0.05), "position": "left", "offset": {"x": 350, "y": -170}},
        ]
    },
    
]

# ==========================================================
# RUN FUNCTION
# ==========================================================
def run_learn_lvl2_T1(screen, main_app):
    """Launch Topic 1 - Introduction (no navigation, single slide)."""
    player = VideoSlidePlayer(
        screen=screen,
        main_app=main_app,
        slides=SLIDES_T1,
        level=2,
        has_navigation=False
    )
    player.topic = "T1"  # ✅ SET TOPIC IDENTIFIER
    player.run()

    # ✅ Mark completion after player exits
    profile_name = main_app.selected_profile.get("name") if main_app.selected_profile else None
    if profile_name:
        mark_learning_topic_complete(profile_name, 2, "T1")
        print(f"✅ Completed Learning Level 2 - Topic T1")
