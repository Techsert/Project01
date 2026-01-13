# learn_lvl2_T1.py - Introduction


from video_slide_base import VideoSlidePlayer
from profile_system import mark_learning_topic_complete


# ==========================================================
# SLIDE DATA
# ==========================================================
SLIDES_T1 = [
    {
        "title": "Introduction",
        "narration": "../assets/sounds/Learn_lvl2/learn_lvl2_T1.wav",
        "images": [
            # Base
##            {"path": "../assets/img/alphabitSound/grid01.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/alphabitSound/bg_ft.png", "delay": 0, "scale": (0.95, 0.80), "position": "center"},
            {"path": "../assets/img/Learn_lvl1_T3/intro09.png", "delay": 0, "scale": (0.3, 0.6), "position": "center", "offset": {"x": -200, "y": 0}},
            # Sec 01
            {"path": "../assets/img/alphabitSound/Letters/01alef.png", "delay": 7500, "scale": (0.03, 0.2), "position": "center", "offset": {"x": 1000, "y": -265}, "duration": 13500},
            {"path": "../assets/img/alphabitSound/Letters/02ba.png", "delay": 8300, "scale": (0.1, 0.1), "position": "center", "offset": {"x": 500, "y": -170}, "duration": 12700},
            {"path": "../assets/img/alphabitSound/Letters/03ta.PNG", "delay": 9200, "scale": (0.1, 0.1), "position": "center", "offset": {"x": 1000, "y": 205}, "duration": 11800}, 
            {"path": "../assets/img/alphabitSound/Letters/04tha.PNG", "delay": 10100, "scale": (0.1, 0.1), "position": "center", "offset": {"x": 500, "y": 205}, "duration": 10900},
            # Sec 02
            {"path": "../assets/img/learn_lvl2/10ra.png", "delay": 27700, "scale": (0.05, 0.18), "position": "center", "offset": {"x": 700, "y": 100}},
            {"path": "../assets/img/learn_lvl2/11zay01.png", "delay": 27700, "scale": (0.05, 0.18), "position": "center", "offset": {"x": 530, "y": 100}},
            {"path": "../assets/img/learn_lvl2/21kf.PNG", "delay": 27700, "scale": (0.1, 0.16), "position": "center", "offset": {"x": 300, "y": 100}},

##            {"path": "../assets/img/main/stop.png", "delay": 28700, "duration": 7000, "scale": (0.06, 0.15), "position": "center", "offset": {"x": -150, "y": 0}, "flash_count": 20, "flash_speed": 200},

            {"path": "../assets/img/main/stop.png", "delay": 33100, "duration": 2900, "scale": (0.05, 0.2), "position": "center", "offset": {"x": 750, "y": -235}, "flash_count": 3, "flash_speed": 300},
            {"path": "../assets/img/main/stop.png", "delay": 33100, "duration": 2900, "scale": (0.05, 0.2), "position": "center", "offset": {"x": 555, "y": -235}, "flash_count": 3, "flash_speed": 300},
            {"path": "../assets/img/main/stop.png", "delay": 33100, "duration": 2900, "scale": (0.05, 0.2), "position": "center", "offset": {"x": 300, "y": -235}, "flash_count": 3, "flash_speed": 300},

            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 44000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 750, "y": -35}, "duration": 4000, "flash_count": 2, "flash_speed": 500},
            {"path": "../assets/img/learn_lvl2/kasra.png", "delay": 44000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 555, "y": 260}, "duration": 4000, "flash_count": 2, "flash_speed": 500},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 44000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 300, "y": -35}, "duration": 4000, "flash_count": 2, "flash_speed": 500},

            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 49000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 750, "y": -35}, "flash_count": 1, "flash_speed": 350},
            {"path": "../assets/img/learn_lvl2/kasra.png", "delay": 50000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 555, "y": 260}, "flash_count": 1, "flash_speed": 350},
            {"path": "../assets/img/learn_lvl2/fat7a-R.png", "delay": 49000, "scale": (0.03, 0.05), "position": "center", "offset": {"x": 300, "y": -35}, "flash_count": 1, "flash_speed": 350},
            
        ],
        "texts": [
            {
                "text": "Ra",
                "delay": 31200,
                "position": "center",
                "offset": {"x": 750, "y": -150},
                "size_ratio": 0.06,
                "color": (0, 100, 200),
                "bold": True,
                "flash_count": 0,
                "flash_speed": 0,
                "duration": 4900
            },
            {
                "text": "Zay",
                "delay": 32400,
                "position": "center",
                "offset": {"x": 555, "y": -150},
                "size_ratio": 0.06,
                "color": (0, 100, 200),
                "bold": True,
                "flash_count": 0,
                "flash_speed": 0,
                "duration": 3700
            },
            {
                "text": "Qaf",
                "delay": 32900,
                "position": "center",
                "offset": {"x": 300, "y": -150},
                "size_ratio": 0.06,
                "color": (0, 100, 200),
                "bold": True,
                "flash_count": 0,
                "flash_speed": 0,
                "duration": 3200
            }
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
