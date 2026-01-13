# ==========================================================
# quiz_lvl3.py - SIMPLIFIED VERSION
# ==========================================================
from quiz_game_base import QuizGameBase
import pygame

# Questions for Level 3
QUESTIONS = [
    {
        "sound": "chop.wav",
        "options": [
            {"file": "25noon01.png", "size": (200, 250), "y_offset": -450}, 
            {"file": "09thal01.png", "size": (150, 250)}, 
            {"file": "01alef.png", "size": (150, 390), "y_offset": -450}, 
            {"file": "21kf.png", "size": (200, 270)}, 
            {"file": "27waw.png", "size": (200, 225), "y_offset": -450},
            {"file": "06ha.png", "size": (200, 350)}, 
            {"file": "11zay.png", "size": (200, 270), "y_offset": -450}, 
            {"file": "08dal.png", "size": (150, 200)}, 
            {"file": "04tha.png", "size": (200, 240), "y_offset": -450}, 
            {"file": "15dad.png", "size": (200, 270)}, 
            {"file": "10ra.png", "size": (200, 225), "y_offset": -450}, 
            {"file": "19gean.png", "size": (200, 390)}
        ],
        "answer": [1, 2, 4, 6, 7, 10],
        "margin": 20
    },
    {
        "sound": "./Sound-Location/01alef-v-d_-m.wav",
        "options": [
            {"file": "18aen-m-f.png", "size": (200, 250), "y_offset": -450}, 
            {"file": "01alef-e-f.png", "size": (200, 390)}, 
            {"file": "01alef-f.png", "size": (90, 440), "y_offset": -450}, 
            {"file": "18aen-b-k.png", "size": (200, 200), "y_offset": 80}, 
            {"file": "18aen-m-d.png", "size": (200, 330), "y_offset": -450}, 
            {"file": "01alef-e-k.png", "size": (200, 400), "y_offset": 130}, 
            {"file": "01alef-e-d.png", "size": (200, 440), "y_offset": -450}, 
            {"file": "18aen-e-f.png", "size": (200, 410)}
        ],
        "answer": 6,
        "margin": 150
    },
    {
        "sound": "./Sound-Location/01alef-v-f01_-e.wav",
        "options": [
            {"file": "18aen-m-f.png", "size": (200, 250), "y_offset": -450}, 
            {"file": "01alef-e-f.png", "size": (200, 390)}, 
            {"file": "01alef-f.png", "size": (90, 440), "y_offset": -450}, 
            {"file": "18aen-b-k.png", "size": (200, 200), "y_offset": 80}, 
            {"file": "18aen-m-d.png", "size": (200, 330), "y_offset": -450}, 
            {"file": "01alef-e-k.png", "size": (200, 400), "y_offset": 130}, 
            {"file": "01alef-e-d.png", "size": (200, 440), "y_offset": -450}, 
            {"file": "18aen-e-f.png", "size": (200, 410)}
        ],
        "answer": 1,
        "margin": 150
    },
]

class QuizLevel3(QuizGameBase):
    """Quiz Level 3 """
    
    def __init__(self):
        super().__init__(level=3)
        self.quiz_id = "Q3"  # ✅ Added Topic Identifier
    
    def get_questions(self):
        """Return questions for this level"""
        return QUESTIONS


def run_quiz_lvl3(screen, main_app):
    """Launch Quiz Level 3 with main app's profile"""
    # Ensure pygame is initialized
    if not pygame.get_init():
        pygame.init()
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    app = QuizLevel3()
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
