# practice_lvl4_P1.py - Practice DAM-MAH

import pygame
import config
from practice_base import PracticeBase
from profile_system import mark_learning_topic_complete

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
        "sound": "02ba-s.wav",
        "letter_image": "02ba.png",
        "letter_size": (400, 300), # Adjust size to fit
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        # ✅ NEW: Defined as separate segments
        "segments": [
            # Segment 1: The main curve (Right to Left)
            [
                (364, 30), (386, 96), (384, 161), (293, 161), (200, 161), (99, 161), (19, 121), (29, 17)
            ],
            # Segment 2: The dot below
            [
                (201, 260), (201, 270) # A short stroke for the dot
            ]
        ]
    },
]

class PracticeLevel4_P1(PracticeBase):
    """Practice 1 for Level 4"""
    
    def __init__(self):
        super().__init__(level=4)
        self.practice_id = "P1"
    
    def get_questions(self):
        return PRACTICE_QUESTIONS


def run_practice_lvl4_P1(screen, main_app):
    """Launch Practice 1 for Level 4"""
    if not pygame.get_init():
        pygame.init()
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    app = PracticeLevel4_P1()
    app.screen = screen
    app.W, app.H = screen.get_size()
    app.audio_manager = main_app.audio_manager
    app.main_app = main_app
    
    app.run()
    
    from profile_system import mark_learning_topic_complete
    profile_name = main_app.selected_profile.get("name") if main_app.selected_profile else None
    if profile_name:
        mark_learning_topic_complete(profile_name, 4, "P1")
    
    main_app.audio_manager.play_bg_music()
