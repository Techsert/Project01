# practice_lvl2_P1.py - Practice 1 for Level 2

import pygame
import config
from practice_base import PracticeBase
from profile_system import mark_learning_topic_complete

PRACTICE_QUESTIONS = [
    # Add questions for Level 2 topics T1-T3
]

class PracticeLevel2_P1(PracticeBase):
    """Practice 1 for Level 2"""
    
    def __init__(self):
        super().__init__(level=2)
        self.practice_id = "T8"
    
    def get_questions(self):
        return PRACTICE_QUESTIONS


def run_practice_lvl2_P1(screen, main_app):
    """Launch Practice 1 for Level 2"""
    if not pygame.get_init():
        pygame.init()
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    app = PracticeLevel2_P1()
    app.screen = screen
    app.W, app.H = screen.get_size()
    app.audio_manager = main_app.audio_manager
    app.main_app = main_app
    
    app.run()
    
    from profile_system import mark_learning_topic_complete
    profile_name = main_app.selected_profile.get("name") if main_app.selected_profile else None
    if profile_name:
        mark_learning_topic_complete(profile_name, 2, "T8")
    
    main_app.audio_manager.play_bg_music()
