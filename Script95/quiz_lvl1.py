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
            {"file": "12sen01.png", "size": (520, 390)}, 
            {"file": "01alef01.png", "size": (151, 600)}, 
            {"file": "08dal.png", "size": (250, 285)}, 
            {"file": "26heh.png", "size": (400, 400)}
        ],
        "answer": 1,
        "margin": 350 # custom spacing for this question
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
    {
        "sound": "03ta-s.wav",
        "options": [
            {"file": "21kf.png", "size": (450, 450)},
            {"file": "04tha.png", "size": (500, 417)},
            {"file": "28yaa01.png", "size": (450, 450)},
            {"file": "03ta.png", "size": (500, 354)}],
        "answer": 3,
        "margin": 250   
    },
    {
        "sound": "04tha-s.wav",
        "options": [
            {"file": "04tha.png", "size": (500, 417)},
            {"file": "02ba02.png", "size": (500, 375), "y_offset": 140},
            {"file": "09thal.png", "size": (250, 430)},
            {"file": "17zaa.png", "size": (500, 590)}],
        "answer": 0,
        "margin": 250   
    },
    {
        "sound": "05geem-s.wav",
        "options": [
            {"file": "05geem.png", "size": (426, 540)},
            {"file": "24meam.png", "size": (250, 450)},
            {"file": "12sen.png", "size": (520, 390)},
            {"file": "07ka.png", "size": (426, 700)}],
        "answer": 0,
        "margin": 250   
    },
    {
        "sound": "06ha-s.wav",
        "options": [
            {"file": "05geem.png", "size": (426, 540)},
            {"file": "06ha.png", "size": (426, 540)},
            {"file": "22kaf.png", "size": (350, 550)},
            {"file": "07ka.png", "size": (426, 700)}],
        "answer": 1,
        "margin": 250   
    },
    {
        "sound": "07ka-s.wav",
        "options": [
            {"file": "05geem.png", "size": (426, 540)},
            {"file": "20feh.png", "size": (500, 354)},
            {"file": "07ka.png", "size": (426, 700)},
            {"file": "11zay.png", "size": (300, 640)}],
        "answer": 2,
        "margin": 250   
    },
    {
        "sound": "08dal-s.wav",
        "options": [
            {"file": "09thal.png", "size": (250, 430)},
            {"file": "11zay.png", "size": (300, 640)},
            {"file": "10ra.png", "size": (300, 450)},
            {"file": "08dal.png", "size": (250, 285)}],
        "answer": 3,
        "margin": 350   
    },
    {
        "sound": "09thal-s.wav",
        "options": [
            {"file": "09thal.png", "size": (250, 430)},
            {"file": "14sad.png", "size": (500, 430)},
            {"file": "08dal.png", "size": (250, 285)},
            {"file": "28yaa.png", "size": (450, 450)}],
        "answer": 0,
        "margin": 250   
    },
    {
        "sound": "10ra-s.wav",
        "options": [
            {"file": "27waw.png", "size": (300, 450)},
            {"file": "10ra.png", "size": (300, 450)},
            {"file": "02ba.png", "size": (500, 375), "y_offset": 140},
            {"file": "11zay.png", "size": (300, 640)}],
        "answer": 1,
        "margin": 250  
    },
    {
        "sound": "11zay-s.wav",
        "options": [
            {"file": "10ra.png", "size": (300, 450)},
            {"file": "04tha.png", "size": (500, 417)},
            {"file": "11zay.png", "size": (300, 640)},
            {"file": "03ta.png", "size": (500, 354)}],
        "answer": 2,
        "margin": 250   
    },
    {
        "sound": "12sen-s.wav",
        "options": [
            {"file": "04tha.png", "size": (500, 317)},
            {"file": "13shen.png", "size": (520, 565)},
            {"file": "20feh.png", "size": (500, 354)},
            {"file": "12sen01.png", "size": (520, 390)}],
        "answer": 3,
        "margin": 200   
    },
    {
        "sound": "13shen-s.wav",
        "options": [
            {"file": "13shen.png", "size": (520, 565)},
            {"file": "24meam.png", "size": (250, 450)},
            {"file": "23lam.png", "size": (280, 610)},
            {"file": "12sen.png", "size": (520, 390)}],
        "answer": 0,
        "margin": 250   
    },
    {
        "sound": "14sad-s.wav",
        "options": [
            {"file": "15dad.png", "size": (500, 590)},
            {"file": "14sad.png", "size": (500, 430)},
            {"file": "12sen01.png", "size": (520, 390)},
            {"file": "04tha.png", "size": (500, 417)}],
        "answer": 1,
        "margin": 200   
    },
    {
        "sound": "15dad-s.wav",
        "options": [
            {"file": "14sad.png", "size": (500, 430)},
            {"file": "17zaa.png", "size": (500, 590)},
            {"file": "15dad.png", "size": (500, 590)},
            {"file": "12sen.png", "size": (520, 390)}],
        "answer": 2,
        "margin": 200   
    },
    {
        "sound": "16taa-s.wav",
        "options": [
            {"file": "17zaa.png", "size": (500, 590)},
            {"file": "03ta01.png", "size": (500, 354)},
            {"file": "10ra01.png", "size": (300, 450)},
            {"file": "16taa.png", "size": (500, 590)}],
        "answer": 3,
        "margin": 250  
    },
    {
        "sound": "17zaa-s.wav",
        "options": [
            {"file": "17zaa.png", "size": (500, 590)},
            {"file": "11zay01.png", "size": (300, 640)},
            {"file": "16taa.png", "size": (500, 590)},
            {"file": "09thal.png", "size": (250, 430)}],
        "answer": 0,
        "margin": 250   
    },
    {
        "sound": "18aen-s.wav",
        "options": [
            {"file": "27waw.png", "size": (300, 450)},
            {"file": "18aen.png", "size": (426, 540)},
            {"file": "02ba.png", "size": (500, 375), "y_offset": 140},
            {"file": "19gean.png", "size": (426, 700)}],
        "answer": 1,
        "margin": 250   
    },
    {
        "sound": "19gean-s.wav",
        "options": [
            {"file": "18aen.png", "size": (426, 540)},
            {"file": "04tha.png", "size": (500, 417)},
            {"file": "19gean.png", "size": (426, 700)},
            {"file": "03ta.png", "size": (500, 354)}],
        "answer": 2,
        "margin": 250   
    },
    {
        "sound": "20feh-s.wav",
        "options": [
            {"file": "19gean.png", "size": (426, 700)},
            {"file": "09thal.png", "size": (250, 430)},
            {"file": "25noon.png", "size": (450, 450)},
            {"file": "20feh.png", "size": (500, 354)}],
        "answer": 3,
        "margin": 250   
    },
    {
        "sound": "21kf-s.wav",
        "options": [
            {"file": "21kf.png", "size": (450, 450)},
            {"file": "03ta.png", "size": (500, 354)},
            {"file": "22kaf.png", "size": (350, 550)},
            {"file": "07ka.png", "size": (426, 700)}],
        "answer": 0,
        "margin": 250   
    },
    {
        "sound": "22kaf-s.wav",
        "options": [
            {"file": "21kf.png", "size": (450, 450)},
            {"file": "22kaf.png", "size": (350, 550)},
            {"file": "23lam.png", "size": (280, 610)},
            {"file": "01alef.png", "size": (151, 600)}],
        "answer": 1,
        "margin": 350   
    },
    {
        "sound": "23lam-s.wav",
        "options": [
            {"file": "05geem.png", "size": (426, 540)},
            {"file": "20feh.png", "size": (500, 354)},
            {"file": "23lam.png", "size": (280, 610)},
            {"file": "22kaf.png", "size": (350, 550)}],
        "answer": 2,
        "margin": 250   
    },
    {
        "sound": "24meam-s.wav",
        "options": [
            {"file": "09thal.png", "size": (250, 430)},
            {"file": "11zay.png", "size": (300, 640)},
            {"file": "10ra01.png", "size": (300, 450)},
            {"file": "24meam.png", "size": (250, 450)}],
        "answer": 3,
        "margin": 350   
    },
    {
        "sound": "25noon-s.wav",
        "options": [
            {"file": "25noon.png", "size": (450, 450)},
            {"file": "20feh.png", "size": (500, 354)},
            {"file": "19gean.png", "size": (426, 700)},
            {"file": "07ka.png", "size": (426, 700)}],
        "answer": 0,
        "margin": 250   
    },
    {
        "sound": "26heh-s.wav",
        "options": [
            {"file": "28yaa.png", "size": (450, 450)},
            {"file": "26heh.png", "size": (400, 400)},
            {"file": "22kaf.png", "size": (350, 550)},
            {"file": "07ka.png", "size": (426, 700)}],
        "answer": 1,
        "margin": 250   
    },
    {
        "sound": "27waw-s.wav",
        "options": [
            {"file": "05geem.png", "size": (426, 540)},
            {"file": "20feh.png", "size": (500, 354)},
            {"file": "27waw.png", "size": (300, 450)},
            {"file": "11zay.png", "size": (300, 640)}],
        "answer": 2,
        "margin": 250   
    },
    {
        "sound": "28yaa-s.wav",
        "options": [
            {"file": "09thal.png", "size": (250, 430)},
            {"file": "11zay.png", "size": (300, 640)},
            {"file": "10ra.png", "size": (300, 450)},
            {"file": "28yaa.png", "size": (450, 450)}],
        "answer": 3,
        "margin": 300   
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
