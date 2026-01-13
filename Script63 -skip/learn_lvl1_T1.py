# learn_lvl1_T1.py - UPDATED TO USE SPRITE ANIMATIONS
# Shows both the OLD way (video) and NEW way (sprite animation)

from video_slide_base import NavigableVideoSlidePlayer
from profile_system import mark_learning_topic_complete

# ==========================================================
# ✅ NEW: SPRITE ANIMATION SLIDE DATA
# ==========================================================
# IMPORTANT: Update these values based on your actual sprite sheet!
# Run: python smart_convert_video.py <video> --scale 0.5
# It will tell you the exact frame_width, frame_height, and num_frames to use

SLIDES_T1_SPRITE = [
    {
        "title": "Introduction To The Arabic Language",
        "background_image": {
            "path": "../assets/img/alphabitSound/bg-tr.png",
            "scale": (0.95, 0.8),
            "position": "center"
        },
        "animation": {
            "type": "sprite_sheet",
            "path": "../assets/animations/Lvl1_Topic1_slide1.png",
            
            # ✅ CORRECT VALUES FOR YOUR SPRITE SHEET:
            "frame_width": 600,   # ← Your actual frame width
            "frame_height": 840,  # ← Your actual frame height
            "num_frames": 1304,   # ← Your actual frame count
            
            "fps": 30,
            "loop": False,
            "scale": (0.5, 0.6),  # Scale up since frames are small (110x140)
            "position": "center",
            "audio_path": "../assets/sounds/Learn_lvl1_T1/lvl1_topic1_Slide1.wav"
        }
    }
]

# ==========================================================
# ✅ ALTERNATIVE: USING INDIVIDUAL FRAME FILES
# ==========================================================
# Use this if you extracted video frames as separate PNG files
SLIDES_T1_FRAMES = [
    {
        "title": "Introduction To The Arabic Language",
        "background_image": {
            "path": "../assets/img/alphabitSound/bg-tr.png",
            "scale": (0.95, 0.8),
            "position": "center"
        },
        "animation": {
            "type": "individual_frames",  # Load from separate files
            "path": [  # List of frame paths
                f"../assets/animations/lvl1_topic1_slide1/frame_{i:04d}.png"
                for i in range(30)  # 30 frames
            ],
            "fps": 30,
            "loop": False,
            "scale": (0.3, 0.5),
            "position": "center",
            "audio_path": "../assets/sounds/Learn_lvl1_T1/lvl1_topic1_Slide1.wav"
        }
    }
]

# ==========================================================
# OLD: VIDEO SLIDE DATA (kept for backwards compatibility)
# ==========================================================
SLIDES_T1_VIDEO_OLD = [
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
            "scale": (0.3, 0.5),
            "position": "center"
        }
    }
]

# ==========================================================
# RUN FUNCTION
# ==========================================================
def run_learn_lvl1_T1(screen, main_app):
    """Launch Topic 1 - Introduction (using sprite animation for better performance)."""
    
    # ✅ Use sprite animation slides (RECOMMENDED)
    # Choose one based on your asset format:
    slides = SLIDES_T1_SPRITE  # If you have a sprite sheet
    # slides = SLIDES_T1_FRAMES  # If you have individual frame files
    # slides = SLIDES_T1_VIDEO_OLD  # Legacy video (slower)
    
    player = NavigableVideoSlidePlayer(
        screen=screen,
        main_app=main_app,
        slides=slides,
        level=1,
        has_navigation=False
    )
    player.topic = "T1"
    player.run()

    # ✅ Mark completion after player exits
    profile_name = main_app.selected_profile.get("name") if main_app.selected_profile else None
    if profile_name:
        mark_learning_topic_complete(profile_name, 1, "T1")
        print(f"✅ Completed Learning Level 1 - Topic T1")


# ==========================================================
# ✅ CONVERSION HELPER SCRIPT
# ==========================================================
def convert_video_to_sprite_sheet():
    """
    Helper function to convert your existing video to sprite sheet.
    Run this once to prepare your assets.
    """
    import pygame
    from sprite_animation import extract_frames_from_video, create_sprite_sheet
    
    pygame.init()
    
    # Step 1: Extract frames from video
    video_path = "../assets/videos/Lvl1_Topic1_slide1_NoSound.mp4"
    frames_dir = "../assets/animations/lvl1_topic1_slide1_frames"
    extract_frames_from_video(video_path, frames_dir, max_frames=None)
    
    # Step 2: Combine frames into sprite sheet
    sprite_sheet_path = "../assets/animations/lvl1_topic1_slide1.png"
    create_sprite_sheet(frames_dir, sprite_sheet_path, frames_per_row=10)
    
    print("✅ Conversion complete!")
    print(f"   Sprite sheet: {sprite_sheet_path}")
    print(f"   You can now delete the frames folder to save space")


# Uncomment to run conversion:
# if __name__ == "__main__":
#     convert_video_to_sprite_sheet()
