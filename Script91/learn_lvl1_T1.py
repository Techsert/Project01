# learn_lvl1_T1.py - Introduction Video


from video_slide_base import VideoSlidePlayer
from profile_system import mark_learning_topic_complete

# ==========================================================
# SLIDE DATA
# ==========================================================
SLIDES_T1 = [
    {
        "title": "Introduction To The Arabic Language",
        "background_image": {
            "path": "../assets/img/alphabitSound/bg-tr.png",
            "scale": (0.95, 0.8),
            "position": "center"
        },
        "video": {
            "path": "../assets/videos/Lvl1_Topic1_slide1_NoSound.mp4",
            "audio_path": "../assets/sounds/Learn_lvl1_T1/lvl1_topic1_Slide1.wav",
            "audio_delay": 0.1,
            "scale": (0.3, 0.5),
            "position": "center"
        }
    }
]

# ==========================================================
# RUN FUNCTION
# ==========================================================
def run_learn_lvl1_T1(screen, main_app):
    """Launch Topic 1 - Introduction (no navigation, single slide)."""
    player = VideoSlidePlayer(
        screen=screen,
        main_app=main_app,
        slides=SLIDES_T1,
        level=1,
        has_navigation=False
    )
    player.topic = "T1"  # ✅ SET TOPIC IDENTIFIER
    player.run()

    # ✅ Mark completion after player exits
    profile_name = main_app.selected_profile.get("name") if main_app.selected_profile else None
    if profile_name:
        mark_learning_topic_complete(profile_name, 1, "T1")
        print(f"✅ Completed Learning Level 1 - Topic T1")
