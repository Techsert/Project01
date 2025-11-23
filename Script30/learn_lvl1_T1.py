# learn_lvl1_T1.py - COMPLETE REPLACEMENT
# This is the ENTIRE file - delete everything and use only this

from video_slide_base import VideoSlidePlayer

# ==========================================================
# SLIDE DATA
# ==========================================================
SLIDES_T1 = [
    {
        "title": "Introduction To The Arabic Language",
        "background_image": {
            "path": "../assets/img/alphabitSound/bg-nt.png",
            "scale": (0.95, 0.78),
            "position": "center"
        },
        "video": {
            "path": "../assets/videos/Lvl1_Topic1_slide1_NoSound.mp4",
            "audio_path": "../assets/sounds/Learn_lvl1_T1/lvl1_topic1_Slide1.wav",
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
        has_navigation=False  # Single slide, no next/prev buttons
    )
    player.run()
