# practice_lvl1_P1.py - Practice 1 for Level 1 (covers T1 and T2 content)
import pygame
import config
from practice_base import PracticeBase
from profile_system import mark_learning_topic_complete

# practice_lvl1_P1.py - UPDATED QUESTIONS

PRACTICE_QUESTIONS = [
    # Multiple choice questions (existing)
    {
        "type": "multiple_choice",
        "sound": "01alef-s.wav",
        "options": [
            {"file": "01alef01.png", "size": (151, 700)},
            {"file": "08dal.png", "size": (250, 285)},
            {"file": "26heh.png", "size": (400, 400)}
        ],
        "answer": 0,
        "margin": 200
    },
    
    # Drag and drop question
    {
        "type": "drag_drop",
        "sound": "02ba-s.wav",
        "items": [
            {
                "id": "ba",
                "file": "02ba.png",
                "size": (200, 150),
                "x": -250,
                "y": 150,
                "correct_zone": "zone1"
            },
            {
                "id": "ta",
                "file": "03ta.png",
                "size": (200, 176),
                "x": 250,
                "y": 150,
                "correct_zone": "zone2"
            }
        ],
        "drop_zones": [
            {
                "id": "zone1",
                "label": "ح",
                "x": -200,
                "y": 100,
                "w": 250,
                "h": 200
            },
            {
                "id": "zone2",
                "label": "ت",
                "x": 200,
                "y": 100,
                "w": 250,
                "h": 200
            }
        ]
    },
    
    # Letter tracing question
    {
        "type": "tracing",
        "sound": "01alef-s.wav",
        "letter_image": "01alef01.png",
        "letter_size": (300, 600),
        "letter_x_ratio": 0.5,  # Center horizontally (0.5 = 50% from left)
        "letter_y_ratio": 0.45,  # Slightly above center vertically
        "trace_path": [
            (300, 200), (300, 250), (300, 300), (300, 350),
            (300, 400), (300, 450), (300, 500), (300, 550),
            (300, 600), (300, 650), (300, 700)
        ]
    },
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
