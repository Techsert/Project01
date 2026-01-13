# practice_lvl1_P2.py - Practice 2 for Level 1 (covers T2 and T3 content)

import pygame
import config
from practice_base import PracticeBase
from profile_system import mark_learning_topic_complete

PRACTICE_QUESTIONS = [
    {
        "sound": "03ta-s.wav",
        "options": [
            {"file": "03ta.png", "size": (500, 440)},
            {"file": "12sen01.png", "size": (520, 440)},
            {"file": "10ra.png", "size": (300, 450)}
        ],
        "answer": 0,
        "margin": 200
    },
    # Add more questions covering T2 and T3 content
]

class PracticeLevel1_P2(PracticeBase):
    """Practice 2 for Level 1 - Covers T2 and T3"""
    
    def __init__(self):
        super().__init__(level=1)
        self.practice_id = "T5"
    
    def get_questions(self):
        return PRACTICE_QUESTIONS


def run_practice_lvl1_P2(screen, main_app):
    """Launch Practice 2 for Level 1"""
    if not pygame.get_init():
        pygame.init()
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    app = PracticeLevel1_P2()
    app.screen = screen
    app.W, app.H = screen.get_size()
    app.audio_manager = main_app.audio_manager
    app.main_app = main_app
    
    app.run()
    
    # ✅ Mark completion
    from profile_system import mark_learning_topic_complete
    profile_name = main_app.selected_profile.get("name") if main_app.selected_profile else None
    if profile_name:
        mark_learning_topic_complete(profile_name, 1, "T5")
    
    main_app.audio_manager.play_bg_music()
