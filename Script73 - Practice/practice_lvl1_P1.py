# practice_lvl1_P1.py - Practice 1 for Level 1 (covers T1 and T2 content)
import pygame
import config
from practice_base import PracticeBase
from profile_system import mark_learning_topic_complete

PRACTICE_QUESTIONS = [
    {
        "sound": "01alef-s.wav",
        "options": [
            {"file": "01alef01.png", "size": (151, 700)},
            {"file": "08dal.png", "size": (250, 285)},
            {"file": "26heh.png", "size": (400, 400)}
        ],
        "answer": 0,
        "margin": 200
    },
    {
        "sound": "02ba-s.wav",
        "options": [
            {"file": "27waw.png", "size": (300, 450)},
            {"file": "02ba.png", "size": (500, 375), "y_offset": 140},
            {"file": "25noon.png", "size": (450, 450)}
        ],
        "answer": 1,
        "margin": 200
    },
    # Add more questions covering T1 and T2 content
]

class PracticeLevel1_P1(PracticeBase):
    """Practice 1 for Level 1 - Covers T1 and T2"""
    
    def __init__(self):
        super().__init__(level=1)
        self.practice_id = "T4"
    
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
        mark_learning_topic_complete(profile_name, 1, "T4")
    
    main_app.audio_manager.play_bg_music()
