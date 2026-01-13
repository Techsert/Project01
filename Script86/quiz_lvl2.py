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
        "sound": "28yaa-d.wav",
        "options": [
            {"file": "28yaa.png", "size": (450, 450)}, 
            {"file": "28yaa-k.png", "size": (450, 540), "y_offset": 90}, 
            {"file": "28yaa-d.png", "size": (450, 600)}, 
            {"file": "28yaa-f.png", "size": (450, 530)}
        ],
        "answer": 2,
        "margin": 250
    },
    {
        "sound": "01alef-f.wav",
        "options": [{"file": "01alef-f.png", "size": (180, 680)}, {"file": "01alef.png", "size": (151, 600)}, {"file": "01alef-k.png", "size": (151, 650), "y_offset": 175}, {"file": "01alef-d.png", "size": (181, 770)}],
        "answer": 0,
        "difficulty": "medium",
        "margin": 450   # custom spacing for this question
    },
    {
        "sound": "02ba-f.wav",
        "options": [{"file": "02ba-d.png", "size": (500, 590)}, {"file": "02ba-f.png", "size": (500, 520)}, {"file": "02ba.png", "size": (500, 375)}, {"file": "02ba-k.png", "size": (500, 430), "y_offset": 50},],
        "answer": 1,
        "difficulty": "medium",
        "margin": 200   # custom spacing for this question
    },
##    {
##        "sound": "03ta-f.wav",
##        "options": [{"file": "03ta-k.png", "size": (500, 490), "y_offset": 130}, {"file": "03ta-d.png", "size": (500, 510)}, {"file": "03ta-f.png", "size": (500, 440)}, {"file": "03ta.png", "size": (500, 354)}],
##        "answer": 2,
##        "difficulty": "medium",
##        "margin": 200   # custom spacing for this question
##    },
##    {
##        "sound": "04tha-f.wav",
##        "options": [{"file": "04tha.png", "size": (500, 417)}, {"file": "04tha-d.png", "size": (500, 570)}, {"file": "04tha-k.png", "size": (500, 550), "y_offset": 135}, {"file": "04tha-f.png", "size": (500, 500)}],
##        "answer": 3,
##        "difficulty": "medium",
##        "margin": 200   # custom spacing for this question
##    },
##    {
##        "sound": "05gem-f.wav",
##        "options": [{"file": "05geam-f.png", "size": (426, 720)}, {"file": "05geam-k.png", "size": (426, 665), "y_offset": 130}, {"file": "05geam-d.png", "size": (426, 820)}, {"file": "05geam.png", "size": (426, 540)}],
##        "answer": 0,
##        "difficulty": "medium",
##        "margin": 300   # custom spacing for this question
##    },
##    {
##        "sound": "06ha-f.wav",
##        "options": [{"file": "06ha-d.png", "size": (426, 820)}, {"file": "06ha.png", "size": (426, 540)}, {"file": "06ha-f.png", "size": (426, 720)}, {"file": "06ha-k.png", "size": (426, 665), "y_offset": 130}],
##        "answer": 2,
##        "difficulty": "medium",
##        "margin": 300   # custom spacing for this question
##    },
##    {
##        "sound": "07ka-f.wav",
##        "options": [{"file": "07ka-k.png", "size": (426, 830), "y_offset": 140}, {"file": "07ka-d.png", "size": (426, 910), "y_offset": 30}, {"file": "07ka-f.png", "size": (426, 810), "y_offset": 30}, {"file": "07ka.png", "size": (426, 700), "y_offset": 30}],
##        "answer": 2,
##        "difficulty": "medium",
##        "margin": 300   # custom spacing for this question
##    },
##    {
##        "sound": "08dal-f.wav",
##        "options": [{"file": "08dal.png", "size": (250, 285)}, {"file": "08dal-k.png", "size": (250, 430), "y_offset": 140}, {"file": "08dal-d.png", "size": (250, 495)}, {"file": "08dal-f.png", "size": (250, 420)}],
##        "answer": 3,
##        "difficulty": "medium",
##        "margin": 350   # custom spacing for this question
##    },
##    {
##        "sound": "09thal-f.wav",
##        "options": [{"file": "09thal-f.png", "size": (250, 530)}, {"file": "09thal.png", "size": (250, 430)}, {"file": "09thal-d.png", "size": (250, 610)}, {"file": "09thal-k.png", "size": (250, 580), "y_offset": 150}],
##        "answer": 0,
##        "difficulty": "medium",
##        "margin": 350   # custom spacing for this question
##    },
##    {
##        "sound": "10ra-f.wav",
##        "options": [{"file": "10ra-d.png", "size": (300, 740)}, {"file": "10ra-f.png", "size": (300, 640)}, {"file": "10ra-k.png", "size": (300, 600), "y_offset": 150}, {"file": "10ra.png", "size": (300, 450)}],
##        "answer": 1,
##        "difficulty": "medium",
##        "margin": 350   # custom spacing for this question
##    },
##    {
##        "sound": "11zay-f.wav",
##        "options": [{"file": "11zay.png", "size": (300, 640)}, {"file": "11zay-k.png", "size": (300, 790), "y_offset": 150}, {"file": "11zay-f.png", "size": (300, 760)}, {"file": "11zay-d.png", "size": (300, 860)}],
##        "answer": 2,
##        "difficulty": "medium",
##        "margin": 350   # custom spacing for this question
##    },
##    {
##        "sound": "12sen-f.wav",
##        "options": [{"file": "12sen-d.png", "size": (520, 750)}, {"file": "12sen.png", "size": (520, 440)}, {"file": "12sen-k.png", "size": (520, 600), "y_offset": 160}, {"file": "12sen-f.png", "size": (520, 645)}],
##        "answer": 3,
##        "difficulty": "medium",
##        "margin": 180   # custom spacing for this question
##    },
##    {
##        "sound": "13shen-f.wav",
##        "options": [{"file": "13shen-f.png", "size": (520, 770)}, {"file": "13shen-k.png", "size": (520, 875), "y_offset": 160}, {"file": "13shen.png", "size": (520, 715)}, {"file": "13shen-d.png", "size": (520, 880)}],
##        "answer": 0,
##        "difficulty": "medium",
##        "margin": 180   # custom spacing for this question
##    },
##    {
##        "sound": "14sad-f.wav",
##        "options": [{"file": "14sad-d.png", "size": (500, 740)}, {"file": "14sad-f.png", "size": (500, 640)}, {"file": "14sad-k.png", "size": (500, 590), "y_offset": 160}, {"file": "14sad.png", "size": (500, 430)}],
##        "answer": 1,
##        "difficulty": "medium",
##        "margin": 180   # custom spacing for this question
##    },
##    {
##        "sound": "15dad-f.wav",
##        "options": [{"file": "15dad-d.png", "size": (450, 790)}, {"file": "15dad.png", "size": (500, 590)}, {"file": "15dad-f.png", "size": (450, 700)}, {"file": "15dad-k.png", "size": (450, 740), "y_offset": 140}],
##        "answer": 2,
##        "difficulty": "medium",
##        "margin": 180   # custom spacing for this question
##    },
##    {
##        "sound": "16-taa-f.wav",
##        "options": [{"file": "16taa.png", "size": (500, 590)}, {"file": "16taa-k.png", "size": (500, 770), "y_offset": 190}, {"file": "16taa-d.png", "size": (500, 800)}, {"file": "16taa-f.png", "size": (500, 710)}],
##        "answer": 3,
##        "difficulty": "medium",
##        "margin": 180  # custom spacing for this question
##    },
##    {
##        "sound": "17zaa-f.wav",
##        "options": [{"file": "17zaa-f.png", "size": (500, 710)}, {"file": "17zaa.png", "size": (500, 590)}, {"file": "17zaa-k.png", "size": (500, 770), "y_offset": 190}, {"file": "17zaa-d.png", "size": (500, 800)}],
##        "answer": 0,
##        "difficulty": "medium",
##        "margin": 180   # custom spacing for this question
##    },
##    {
##        "sound": "18aen-f.wav",
##        "options": [{"file": "18aen-k.png", "size": (426, 645), "y_offset": 100}, {"file": "18aen-f.png", "size": (426, 680)}, {"file": "18aen.png", "size": (426, 540)}, {"file": "18aen-d.png", "size": (426, 760)}],
##        "answer": 1,
##        "difficulty": "medium",
##        "margin": 250   # custom spacing for this question
##    },
##    {
##        "sound": "19gean-f.wav",
##        "options": [{"file": "19gean-d.png", "size": (426, 830)}, {"file": "19gean-k.png", "size": (426, 770), "y_offset": 100}, {"file": "19gean-f.png", "size": (426, 760)}, {"file": "19gean.png", "size": (426, 700)}],
##        "answer": 2,
##        "difficulty": "medium",
##        "margin": 250   # custom spacing for this question
##    },
##    {
##        "sound": "20feh-f.wav",
##        "options": [{"file": "20feh.png", "size": (500, 354)}, {"file": "20feh-k.png", "size": (500, 510), "y_offset": 150}, {"file": "20feh-d.png", "size": (500, 440)}, {"file": "20feh-f.png", "size": (500, 360)}],
##        "answer": 3,
##        "difficulty": "medium",
##        "margin": 180   # custom spacing for this question
##    },
##    {
##        "sound": "21kf-f.wav",
##        "options": [{"file": "21kf-f.png", "size": (450, 490)}, {"file": "21kf.png", "size": (450, 450)}, {"file": "21kf-d.png", "size": (450, 550)}, {"file": "21kf-k.png", "size": (450, 560), "y_offset": 100}],
##        "answer": 0,
##        "difficulty": "medium",
##        "margin": 300   # custom spacing for this question
##    },
##    {
##        "sound": "22kaf-f.wav",
##        "options": [{"file": "22kaf-k.png", "size": (350, 760), "y_offset": 160}, {"file": "22kaf-f.png", "size": (350, 550), "y_offset": -50}, {"file": "22kaf.png", "size": (350, 550), "y_offset": -50}, {"file": "22kaf-d.png", "size": (350, 590), "y_offset": -50}],
##        "answer": 1,
##        "difficulty": "medium",
##        "margin": 340   # custom spacing for this question
##    },
##    {
##        "sound": "23lam-f.wav",
##        "options": [{"file": "23lam-d.png", "size": (280, 610)}, {"file": "23lam-k.png", "size": (280, 740), "y_offset": 130}, {"file": "23lam-f.png", "size": (280, 610)}, {"file": "23lam.png", "size": (280, 610)}],
##        "answer": 2,
##        "difficulty": "medium",
##        "margin": 380   # custom spacing for this question
##    },
##    {
##        "sound": "24meam-f.wav",
##        "options": [{"file": "24meam.png", "size": (250, 450)}, {"file": "24meam-k.png", "size": (250, 550), "y_offset": 100}, {"file": "24meam-d.png", "size": (250, 710)}, {"file": "24meam-f.png", "size": (250, 620)}],
##        "answer": 3,
##        "difficulty": "medium",
##        "margin": 450   # custom spacing for this question
##    },
##    {
##        "sound": "25noon-f.wav",
##        "options": [{"file": "25noon-f.png", "size": (450, 560)}, {"file": "25noon-k.png", "size": (450, 580), "y_offset": 130}, {"file": "25noon.png", "size": (450, 450)}, {"file": "25noon-d.png", "size": (450, 640)}],
##        "answer": 0,
##        "difficulty": "medium",
##        "margin": 250   # custom spacing for this question
##    },
##    {
##        "sound": "26heh-f.wav",
##        "options": [{"file": "26heh-d.png", "size": (400, 580)}, {"file": "26heh-f.png", "size": (400, 480)}, {"file": "26heh.png", "size": (400, 400)}, {"file": "26heh-k.png", "size": (400, 560), "y_offset": 150}],
##        "answer": 1,
##        "difficulty": "medium",
##        "margin": 250   # custom spacing for this question
##    },
##    {
##        "sound": "27waw-f.wav",
##        "options": [{"file": "27waw-k.png", "size": (300, 590), "y_offset": 130}, {"file": "27waw.png", "size": (300, 450)}, {"file": "27waw-f.png", "size": (300, 640)}, {"file": "27waw-d.png", "size": (300, 740)}],
##        "answer": 2,
##        "difficulty": "medium",
##        "margin": 350   # custom spacing for this question
##    },
##    {
##        "sound": "28yaa-f.wav",
##        "options": [{"file": "28yaa.png", "size": (450, 450)}, {"file": "28yaa-k.png", "size": (450, 540), "y_offset": 90}, {"file": "28yaa-d.png", "size": (450, 600)}, {"file": "28yaa-f.png", "size": (450, 530)}],
##        "answer": 3,
##        "difficulty": "medium",
##        "margin": 250   # custom spacing for this question
##    },    
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
