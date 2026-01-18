# practice_lvl2_P1.py - Practice FAT-HAH

import pygame
import config
from practice_base import PracticeBase
from profile_system import mark_learning_topic_complete

PRACTICE_QUESTIONS = [
##    #############################
##    # Multiple choice questions #
##    #############################
##    # Alef
##    {
##        "type": "multiple_choice",
##        "sound": "01alef-s.wav",
##        "options": [
##            {"file": "01alef01.png", "size": (151, 700)},
##            {"file": "08dal.png", "size": (250, 285)},
##            {"file": "26heh.png", "size": (400, 400)}
##        ],
##        "answer": 0,
##        "margin": 200
##    },
    
    ##############################
    # Drag and drop Many to Many #
    ##############################
    # Alef
    
    {
        "type": "drag_drop",
        "sound": "01alef-f.wav",
        "items": [
            {
                "id": "Alif",
                "file": "30-3.png",
                "size": (100, 450),
                "x": -1450,
                "y": -500,
                "correct_zone": "zone1"
            },
            {
                "id": "lam",
                "file": "30-22.png",
                "size": (250, 450),
                "x": -1300,
                "y": -500,
                "correct_zone": "zone1"
            },

            {
                "id": "7a",
                "file": "30-10.png",
                "size": (275, 450),
                "x": -950,
                "y": -500,
                "correct_zone": "zone1"
            },
            {
                "id": "RAA",
                "file": "30-14.png",
                "size": (220, 250),
                "x": -600,
                "y": -500,
                "correct_zone": "zone3"
            },
            
            {
                "id": "2dots",
                "file": "30-11.png",
                "size": (200, 90),
                "x": -600,
                "y": -140,
                "correct_zone": "zone3"
            },
            {
                "id": "kaf",
                "file": "30-21.png",
                "size": (325, 450),
                "x": -1450,
                "y": 0,
                "correct_zone": "zone1"
            },
            {
                "id": "Ayn",
                "file": "30-18.png",
                "size": (275, 450),
                "x": -1050,
                "y": 0,
                "correct_zone": "zone1"
            },
            {
                "id": "Dal",
                "file": "30-13.png",
                "size": (175, 220),
                "x": -600,
                "y": 0,
                "correct_zone": "zone3"
            },
            {
                "id": "3dots",
                "file": "30-12.png",
                "size": (150, 150),
                "x": -600,
                "y": 300,
                "correct_zone": "zone3"
            },
            ###################################
{
                "id": "Sean",
                "file": "30-15.png",
                "size": (325, 200),
                "x": 370,
                "y": -500,
                "correct_zone": "zone3"
            },
            {
                "id": "Sad",
                "file": "30-16.png",
                "size": (325, 200),
                "x": 730,
                "y": -500,
                "correct_zone": "zone3"
            },
            {
                "id": "Noon",
                "file": "30-24.png",
                "size": (175, 200),
                "x": 1100,
                "y": -500,
                "correct_zone": "zone3"
            },            
            {
                "id": "Waw",
                "file": "30-26.png",
                "size": (175, 220),
                "x": 1310,
                "y": -500,
                "correct_zone": "zone3"
            },
            ###########################################
            {
                "id": "Haa",
                "file": "30-25.png",
                "size": (220, 250),
                "x": 370,
                "y": -260,
                "correct_zone": "zone3"
            },           
            
            {
                "id": "Ba",
                "file": "30-5.png",
                "size": (300, 150),
                "x": 860,
                "y": -160,
                "correct_zone": "zone3"
            },
            {
                "id": "Faa",
                "file": "30-19.png",
                "size": (300, 150),
                "x": 1190,
                "y": -160,
                "correct_zone": "zone3"
            },
            {
                "id": "Hamza",
                "file": "30-2.png",
                "size": (150, 120),
                "x": 630,
                "y": -130,
                "correct_zone": "zone2"
            }, 
            ###############################
            {
                "id": "Qaf",
                "file": "30-20.png",
                "size": (230, 220),
                "x": 450,
                "y": 150,
                "correct_zone": "zone3"
            },
            {
                "id": "Meam",
                "file": "30-23.png",
                "size": (220, 220),
                "x": 710,
                "y": 135,
                "correct_zone": "zone3"
            },
            {
                "id": "Yaa",
                "file": "30-27.png",
                "size": (220, 220),
                "x": 1260,
                "y": 130,
                "correct_zone": "zone3"
            },            
            {
                "id": "TAA",
                "file": "30-17.png",
                "size": (225, 300),
                "x": 1000,
                "y": 50,
                "correct_zone": "zone3"
            },
                           
            #####################################
            {
                "id": "dot",
                "file": "30-9.png",
                "size": (100, 90),
                "x": 600,
                "y": 430,
                "correct_zone": "zone3"
            },
            
            {
                "id": "Fathah",
                "file": "30-1.png",
                "size": (200, 90),
                "x": 800,
                "y": 430,
                "correct_zone": "zone3"
            },
            #####################################
            
            
            






            
            
        ],
        "drop_zones": [
            
            {
                "id": "zone1",
                "label": "",
                "x": 0,
                "y": 150,
                "w": 110,
                "h": 460
            },
            {
                "id": "zone2",
                "label": "",
                "x": 0,
                "y": -145,
                "w": 160,
                "h": 130
            },
            {
                "id": "zone3",
                "label": "",
                "x": 0,
                "y": -260,
                "w": 210,
                "h": 100
            },
        ]
    },
      
##    ###########################
##    # Letter tracing question #
##    ###########################
##    
##    # Alef
##    {
##        "type": "tracing",
##        "sound": "01alef-s.wav",
##        "letter_image": "01alef01.png",
##        "letter_size": (300, 600),
##        "letter_x_ratio": 0.5,  # Center horizontally (0.5 = 50% from left)
##        "letter_y_ratio": 0.45,  # Slightly above center vertically
##        "trace_path": [
##            (300, 200), (300, 250), (300, 300), (300, 350),
##            (300, 400), (300, 450), (300, 500), (300, 550),
##            (300, 600), (300, 650), (300, 700)
##        ]
##    },
]

class PracticeLevel2_P1(PracticeBase):
    """Practice 1 for Level 2"""
    
    def __init__(self):
        super().__init__(level=2)
        self.practice_id = "P1"
    
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
        mark_learning_topic_complete(profile_name, 2, "P1")
    
    main_app.audio_manager.play_bg_music()
