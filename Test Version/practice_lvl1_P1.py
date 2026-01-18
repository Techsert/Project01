# practice_lvl1_P1.py - Practice Alphabet Names
import pygame
import config
from practice_base import PracticeBase
from profile_system import mark_learning_topic_complete

# practice_lvl1_P1.py - UPDATED QUESTIONS

PRACTICE_QUESTIONS = [
    {
        "type": "drag_drop",
        "sound": "01alef-s.wav",
        "items": [            
            {
                "id": "ba",
                "file": "02ba.png",
                "size": (200, 150),
                "x": 305,
                "y": 150,
            },

            {
                "id": "Alef",
                "file": "01alef.png",
                "size": (50, 210),
                "x": -25,
                "y": 40,
                "correct_zone": "target_zone" # Correct Answer
            },
            
            {
                "id": "ta",
                "file": "03ta.png",
                "size": (200, 140),
                "x": -475,
                "y": 105,
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -300,
                "w": 250,
                "h": 330
            },
        ]
    },

]

class PracticeLevel1_P1(PracticeBase):
    """Practice 1 for Level 1 - Covers T1 and T2"""
    
    def __init__(self):
        super().__init__(level=1)
        self.practice_id = "P1"
    
    def get_questions(self):
        return PRACTICE_QUESTIONS


def run_practice_lvl1_P1(screen, main_app):
    """Launch Practice 1 for Level 1"""
    if not pygame.get_init():
        pygame.init()
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    app = PracticeLevel1_P1()
    app.screen = screen
    app.W, app.H = screen.get_size()
    app.audio_manager = main_app.audio_manager
    app.main_app = main_app
    
    app.run()
    
    # ✅ Mark completion
    from profile_system import mark_learning_topic_complete
    profile_name = main_app.selected_profile.get("name") if main_app.selected_profile else None
    if profile_name:
        mark_learning_topic_complete(profile_name, 1, "P1")
    
    main_app.audio_manager.play_bg_music()
