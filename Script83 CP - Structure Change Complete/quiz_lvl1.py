# ==========================================================
# quiz_lvl1.py - SIMPLIFIED VERSION
# ==========================================================
import pygame
from quiz_game_base import QuizGameBase


# Questions for Level 1
QUESTIONS = [
    {
        "sound": "01alef-s.wav",
        "options": [
            {"file": "12sen01.png", "size": (520, 440)}, 
            {"file": "01alef01.png", "size": (151, 700)}, 
            {"file": "08dal.png", "size": (250, 285)}, 
            {"file": "26heh.png", "size": (400, 400)}
        ],
        "answer": 1,
        "margin": 350
    },
    {
        "sound": "02ba-s.wav",
        "options": [
            {"file": "27waw.png", "size": (300, 450)}, 
            {"file": "10ra.png", "size": (300, 450)}, 
            {"file": "02ba.png", "size": (500, 375), "y_offset": 140}, 
            {"file": "25noon.png", "size": (450, 450)}
        ],
        "answer": 2,
        "margin": 250
    },
]

class QuizLevel1(QuizGameBase):
    """Quiz Level 1"""
    
    def __init__(self):
        super().__init__(level=1)
        self.quiz_id = "Q1"  # ✅ Added Topic Identifier
    
    def get_questions(self):
        """Return questions for this level"""
        return QUESTIONS


def run_quiz_lvl1(screen, main_app):
    """Launch Quiz Level 1 with main app's profile"""
    if not pygame.get_init():
        pygame.init()
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    app = QuizLevel1()
    app.screen = screen
    app.W, app.H = screen.get_size()
    
    # ✅ Set AudioManager reference
    app.audio_manager = main_app.audio_manager
    
    # ✅ Set main_app reference for profile icon
    app.main_app = main_app
    
    # Re-initialize screen-dependent components
    app._load_backgrounds()
    app._load_start_button()
    app._load_feedback_assets()
    app._load_exit_button()
    
    app.current_profile = main_app.selected_profile.get("name") if main_app.selected_profile else "Guest"
    app.profiles = {app.current_profile: main_app.selected_profile} if main_app.selected_profile else {}
    app.state = "intro"
    app.intro_start_time = pygame.time.get_ticks()
    app.run()
    
    # ✅ Resume background music using AudioManager
    main_app.audio_manager.play_bg_music()
