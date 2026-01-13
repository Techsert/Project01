# ==========================================================
# quiz_lvl2.py - FAT-HAH
# ==========================================================
from quiz_game_base import QuizGameBase
import pygame

# Questions for Level 2
QUESTIONS = [
    {
        "sound": "01alef-f.wav",
        "options": [
	    {"file": "01alef-f.png", "size": (180, 680)}, 
	    {"file": "01alef.png", "size": (151, 600)}, 
	    {"file": "01alef-k.png", "size": (151, 650), "y_offset": 175}, 
	    {"file": "01alef-d.png", "size": (181, 770)}
	],
        "answer": 0,
        "margin": 450
    },
    {
        "sound": "02ba-f.wav",
        "options": [
	    {"file": "02ba-d.png", "size": (500, 590)}, 
	    {"file": "02ba-f.png", "size": (500, 520)}, 
	    {"file": "02ba.png", "size": (500, 375)}, 
	    {"file": "02ba-k.png", "size": (500, 430), "y_offset": 50},
	],
        "answer": 1,
        "margin": 200
    },
]

class QuizLevel2(QuizGameBase):
    """Quiz Level 2"""
    
    def __init__(self):
        super().__init__(level=2)
        self.quiz_id = "Q2"  # ✅ Added Topic Identifier
    
    def get_questions(self):
        """Return questions for this level"""
        return QUESTIONS


def run_quiz_lvl2(screen, main_app):
    """Launch Quiz Level 2 with main app's profile"""
    # Ensure pygame is initialized
    if not pygame.get_init():
        pygame.init()
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    app = QuizLevel2()
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
