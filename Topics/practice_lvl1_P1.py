# practice_lvl1_P1.py - Practice Alphabet Names
import pygame
import config
from practice_base import PracticeBase
from profile_system import mark_learning_topic_complete

# practice_lvl1_P1.py - UPDATED QUESTIONS

PRACTICE_QUESTIONS = [
    #############################
    # Drag and drop Many to One #
    #############################
##    # Alef
##    {
##        "type": "drag_drop",
##        "sound": "01alef-s.wav",
##        "items": [            
##            {
##                "id": "ba",
##                "file": "02ba.png",
##                "size": (200, 150),
##                "x": 305,
##                "y": 150,
##            },
##
##            {
##                "id": "Alef",
##                "file": "01alef.png",
##                "size": (50, 210),
##                "x": -25,
##                "y": 40,
##                "correct_zone": "target_zone" # Correct Answer
##            },
##            
##            {
##                "id": "ta",
##                "file": "03ta.png",
##                "size": (200, 140),
##                "x": -475,
##                "y": 105,
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -300,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##
##    # Baa
##    {
##        "type": "drag_drop",
##        "sound": "02ba-s.wav",
##        "items": [            
##            {
##                "id": "ba",
##                "file": "02ba.png",
##                "size": (200, 150),
##                "x": -100,
##                "y": 150,
##                "correct_zone": "target_zone" # Correct Answer
##            },
##
##            {
##                "id": "tha",
##                "file": "04tha.png", 
##                "size": (200, 165),
##                "x": 300,               
##                "y": 80,
##            },
##            
##            {
##                "id": "ta",
##                "file": "03ta.png",
##                "size": (200, 140),
##                "x": -500,
##                "y": 105,
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # Ta
##    {
##        "type": "drag_drop",
##        "sound": "03ta-s.wav",
##        "items": [            
##            {
##                "id": "ba_wrong",
##                "file": "02ba.png",
##                "size": (200, 150),
##                "x": -100,
##                "y": 150,
##            },
##
##            {
##                "id": "tha_wrong",
##                "file": "04tha.png", 
##                "size": (200, 165),
##                "x": 300,               
##                "y": 80,
##            },
##            
##            {
##                "id": "ta_correct",
##                "file": "03ta.png",
##                "size": (200, 140),
##                "x": -500,
##                "y": 105,
##                "correct_zone": "target_zone" # Correct Answer
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # Tha
##    {
##        "type": "drag_drop",
##        "sound": "04tha-s.wav",
##        "items": [            
##            {
##                "id": "ba",
##                "file": "02ba.png",
##                "size": (200, 150),
##                "x": -100,
##                "y": 150,
##            },
##
##            {
##                "id": "tha",
##                "file": "04tha.png", 
##                "size": (200, 165),
##                "x": 300,               
##                "y": 80,
##                "correct_zone": "target_zone" # Correct Answer
##            },
##            
##            {
##                "id": "ta",
##                "file": "03ta.png",
##                "size": (200, 140),
##                "x": -500,
##                "y": 105,
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # Geam
##    {
##        "type": "drag_drop",
##        "sound": "05geem-s.wav",
##        "items": [            
##            {
##                "id": "geam",
##                "file": "05geem.PNG",
##                "size": (200, 210),
##                "x": 300,
##                "y": 40,
##                "correct_zone": "target_zone"
##            },
##            {
##                "id": "ha",
##                "file": "06ha.png",
##                "size": (200, 210),
##                "x": -100,
##                "y": 40,
##            },
##
##            {
##                "id": "Ka",
##                "file": "07ka.PNG",
##                "size": (200, 275),
##                "x": -500,
##                "y": -25,
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # حاء
##    {
##        "type": "drag_drop",
##        "sound": "06ha-s.wav",
##        "items": [            
##            {
##                "id": "geam",
##                "file": "05geem.PNG",
##                "size": (200, 210),
##                "x": 300,
##                "y": 40,
##            },
##            {
##                "id": "ha",
##                "file": "06ha.png",
##                "size": (200, 210),
##                "x": -100,
##                "y": 40,
##                "correct_zone": "target_zone"
##            },
##
##            {
##                "id": "Ka",
##                "file": "07ka.PNG",
##                "size": (200, 275),
##                "x": -500,
##                "y": -25,
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # خاء
##    {
##        "type": "drag_drop",
##        "sound": "07ka-s.wav",
##        "items": [            
##            {
##                "id": "geam",
##                "file": "05geem.PNG",
##                "size": (200, 210),
##                "x": 300,
##                "y": 40,
##            },
##            {
##                "id": "ha",
##                "file": "06ha.png",
##                "size": (200, 210),
##                "x": -100,
##                "y": 40,
##            },
##
##            {
##                "id": "Ka",
##                "file": "07ka.PNG",
##                "size": (200, 275),
##                "x": -500,
##                "y": -25,
##                "correct_zone": "target_zone"
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # دال
##    {
##        "type": "drag_drop",
##        "sound": "08dal-s.wav",
##        "items": [            
##            {
##                "id": "Dal",
##                "file": "08dal.PNG",
##                "size": (120, 140),
##                "x": 350,
##                "y": 105,
##                "correct_zone": "target_zone"
##            },
##            {
##                "id": "Thal",
##                "file": "09thal.PNG",
##                "size": (120, 210),
##                "x": -50,
##                "y": 35,
##            },
##            
##            {
##                "id": "Ra",
##                "file": "10ra.PNG",
##                "size": (170, 190),
##                "x": -500,
##                "y": 110,
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # ذال
##    {
##        "type": "drag_drop",
##        "sound": "09thal-s.wav",
##        "items": [            
##            {
##                "id": "Dal",
##                "file": "08dal.PNG",
##                "size": (120, 140),
##                "x": 350,
##                "y": 105,
##            },
##            {
##                "id": "Thal",
##                "file": "09thal.PNG",
##                "size": (120, 210),
##                "x": -50,
##                "y": 35,
##                "correct_zone": "target_zone"
##            },
##            
##            {
##                "id": "Ra",
##                "file": "10ra.PNG",
##                "size": (170, 190),
##                "x": -500,
##                "y": 110,
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # راء
##    {
##        "type": "drag_drop",
##        "sound": "10ra-s.wav",
##        "items": [            
##            {
##                "id": "Thal",
##                "file": "09thal.PNG",
##                "size": (120, 210),
##                "x": 350,
##                "y": 35,
##            },
##            
##            {
##                "id": "Ra",
##                "file": "10ra.PNG",
##                "size": (170, 190),
##                "x": -100,
##                "y": 110,
##                "correct_zone": "target_zone"
##            },
##            {
##                "id": "Zay",
##                "file": "11zay.PNG",
##                "size": (170, 270),
##                "x": -500,
##                "y": 30,
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # زاي
##    {
##        "type": "drag_drop",
##        "sound": "11zay-s.wav",
##        "items": [            
##            {
##                "id": "Thal",
##                "file": "09thal.PNG",
##                "size": (120, 210),
##                "x": 350,
##                "y": 35,
##            },
##            
##            {
##                "id": "Ra",
##                "file": "10ra.PNG",
##                "size": (170, 190),
##                "x": -100,
##                "y": 110,
##            },
##            {
##                "id": "Zay",
##                "file": "11zay.PNG",
##                "size": (170, 270),
##                "x": -500,
##                "y": 30,
##                "correct_zone": "target_zone"
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # سين
##    {
##        "type": "drag_drop",
##        "sound": "12sen-s.wav",
##        "items": [            
##            {
##                "id": "Seen",
##                "file": "12sen.PNG",
##                "size": (210, 205),
##                "x": 300,
##                "y": 130,
##                "correct_zone": "target_zone"
##            },
##            
##            {
##                "id": "Sheen",
##                "file": "13shen.PNG",
##                "size": (210, 320),
##                "x": -100,
##                "y": 15,
##            },
##            
##            {
##                "id": "Sad",
##                "file": "14sad.PNG",
##                "size": (210, 210),
##                "x": -500,
##                "y": 130,
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # شين
##    {
##        "type": "drag_drop",
##        "sound": "13shen-s.wav",
##        "items": [            
##            {
##                "id": "Seen",
##                "file": "12sen.PNG",
##                "size": (210, 205),
##                "x": 300,
##                "y": 130,
##            },
##            
##            {
##                "id": "Sheen",
##                "file": "13shen.PNG",
##                "size": (210, 320),
##                "x": -100,
##                "y": 15,
##                "correct_zone": "target_zone"
##            },
##            
##            {
##                "id": "Sad",
##                "file": "14sad.PNG",
##                "size": (210, 210),
##                "x": -500,
##                "y": 130,
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # صاد
##    {
##        "type": "drag_drop",
##        "sound": "14sad-s.wav",
##        "items": [            
##            {
##                "id": "Sheen",
##                "file": "13shen.PNG",
##                "size": (210, 320),
##                "x": 300,
##                "y": 15,
##            },
##            
##            {
##                "id": "Sad",
##                "file": "14sad.PNG",
##                "size": (210, 210),
##                "x": -100,
##                "y": 130,
##                "correct_zone": "target_zone"
##            },
##            {
##                "id": "Dad",
##                "file": "15dad.PNG",
##                "size": (210, 275),
##                "x": -500,
##                "y": 60,
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # ضاد
##    {
##        "type": "drag_drop",
##        "sound": "15dad-s.wav",
##        "items": [            
##            {
##                "id": "Sheen",
##                "file": "13shen.PNG",
##                "size": (210, 320),
##                "x": 300,
##                "y": 15,
##            },
##            
##            {
##                "id": "Sad",
##                "file": "14sad.PNG",
##                "size": (210, 210),
##                "x": -100,
##                "y": 130,
##            },
##            {
##                "id": "Dad",
##                "file": "15dad.PNG",
##                "size": (210, 275),
##                "x": -500,
##                "y": 60,
##                "correct_zone": "target_zone"
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # طاء
##    {
##        "type": "drag_drop",
##        "sound": "16-taa-s.wav",
##        "items": [
##            {
##                "id": "Dad",
##                "file": "15dad.PNG",
##                "size": (210, 275),
##                "x": 300,
##                "y": 60,
##            },
##
##            {
##                "id": "Taa",
##                "file": "16taa.PNG",
##                "size": (200, 270),
##                "x": -100,
##                "y": -25,
##                "correct_zone": "target_zone"
##            },
##            
##            {
##                "id": "Zaa",
##                "file": "17zaa.PNG",
##                "size": (200, 270),
##                "x": -500,
##                "y": -25,
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # ظاء
##    {
##        "type": "drag_drop",
##        "sound": "17zaa-s.wav",
##        "items": [            
##            {
##                "id": "Dad",
##                "file": "15dad.PNG",
##                "size": (210, 275),
##                "x": 300,
##                "y": 60,
##            },
##
##            {
##                "id": "Taa",
##                "file": "16taa.PNG",
##                "size": (200, 270),
##                "x": -100,
##                "y": -25,
##            },
##            
##            {
##                "id": "Zaa",
##                "file": "17zaa.PNG",
##                "size": (200, 270),
##                "x": -500,
##                "y": -25,
##                "correct_zone": "target_zone"
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # عين
##    {
##        "type": "drag_drop",
##        "sound": "18aen-s.wav",
##        "items": [            
##            {
##                "id": "Aen",
##                "file": "18aen.PNG",
##                "size": (200, 210),
##                "x": 300,
##                "y": 40,
##                "correct_zone": "target_zone"
##            },
##            
##            {
##                "id": "Gean",
##                "file": "19gean.PNG",
##                "size": (200, 260),
##                "x": -100,
##                "y": -15,
##            },
##            
##            {
##                "id": "Feh",
##                "file": "20feh.PNG",
##                "size": (210, 150),
##                "x": -500,
##                "y": 95,
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # غين
##    {
##        "type": "drag_drop",
##        "sound": "19gean-s.wav",
##        "items": [            
##            {
##                "id": "Aen",
##                "file": "18aen.PNG",
##                "size": (200, 210),
##                "x": 300,
##                "y": 40,
##            },
##            
##            {
##                "id": "Gean",
##                "file": "19gean.PNG",
##                "size": (200, 260),
##                "x": -100,
##                "y": -15,
##                "correct_zone": "target_zone"
##            },
##            
##            {
##                "id": "Feh",
##                "file": "20feh.PNG",
##                "size": (210, 150),
##                "x": -500,
##                "y": 95,
##            },
##
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # فاء
##    {
##        "type": "drag_drop",
##        "sound": "20feh-s.wav",
##        "items": [            
##            {
##                "id": "Gean",
##                "file": "19gean.PNG",
##                "size": (200, 260),
##                "x": 300,
##                "y": -15,
##            },
##            
##            {
##                "id": "Feh",
##                "file": "20feh.PNG",
##                "size": (210, 150),
##                "x": -100,
##                "y": 95,
##                "correct_zone": "target_zone"
##            },
##
##            {
##                "id": "Kf",
##                "file": "21kf.PNG",
##                "size": (190, 160),
##                "x": -500,
##                "y": 95,
##            },
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # قاف
##    {
##        "type": "drag_drop",
##        "sound": "21kf-s.wav",
##        "items": [            
##            {
##                "id": "Gean",
##                "file": "19gean.PNG",
##                "size": (200, 260),
##                "x": 300,
##                "y": -15,
##            },
##            
##            {
##                "id": "Feh",
##                "file": "20feh.PNG",
##                "size": (210, 150),
##                "x": -100,
##                "y": 95,
##            },
##
##            {
##                "id": "Kf",
##                "file": "21kf.PNG",
##                "size": (190, 160),
##                "x": -500,
##                "y": 95,
##                "correct_zone": "target_zone"
##            },
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # كاف
##    {
##        "type": "drag_drop",
##        "sound": "22kaf-s.wav",
##        "items": [           
##            {
##                "id": "Feh",
##                "file": "20feh.PNG",
##                "size": (210, 150),
##                "x": 300,
##                "y": 95,
##            },
##
##            {
##                "id": "Kf",
##                "file": "21kf.PNG",
##                "size": (190, 160),
##                "x": -100,
##                "y": 95,
##            },
##
##            {
##                "id": "Kaf",
##                "file": "22kaf.PNG",
##                "size": (200, 275),
##                "x": -500,
##                "y": -25,
##                "correct_zone": "target_zone"
##            },
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # لام
##    {
##        "type": "drag_drop",
##        "sound": "23lam-s.wav",
##        "items": [           
##            {
##                "id": "Lam",
##                "file": "23lam.PNG",
##                "size": (170, 275),
##                "x": 300,
##                "y": -25,
##                "correct_zone": "target_zone"
##            },
##
##            {
##                "id": "Meam",
##                "file": "24meam.PNG",
##                "size": (160, 165),
##                "x": -100,
##                "y": 85,
##            },
##            
##            {
##                "id": "Noon",
##                "file": "25noon.PNG",
##                "size": (190, 160),
##                "x": -500,
##                "y": 85,
##            },
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # ميم
##    {
##        "type": "drag_drop",
##        "sound": "24meam-s.wav",
##        "items": [           
##            {
##                "id": "Lam",
##                "file": "23lam.PNG",
##                "size": (170, 275),
##                "x": 300,
##                "y": -25,
##            },
##
##            {
##                "id": "Meam",
##                "file": "24meam.PNG",
##                "size": (160, 165),
##                "x": -100,
##                "y": 85,
##                "correct_zone": "target_zone"
##            },
##            
##            {
##                "id": "Noon",
##                "file": "25noon.PNG",
##                "size": (190, 160),
##                "x": -500,
##                "y": 85,
##            },
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # نون
##    {
##        "type": "drag_drop",
##        "sound": "25noon-s.wav",
##        "items": [           
##            {
##                "id": "Lam",
##                "file": "23lam.PNG",
##                "size": (170, 275),
##                "x": 300,
##                "y": -25,
##            },
##
##            {
##                "id": "Meam",
##                "file": "24meam.PNG",
##                "size": (160, 165),
##                "x": -100,
##                "y": 85,
##            },
##            
##            {
##                "id": "Noon",
##                "file": "25noon.PNG",
##                "size": (190, 160),
##                "x": -500,
##                "y": 85,
##                "correct_zone": "target_zone"
##            },
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # هاء
##    {
##        "type": "drag_drop",
##        "sound": "26heh-s.wav",
##        "items": [           
##            {
##                "id": "Heh",
##                "file": "26heh.PNG",
##                "size": (190, 160),
##                "x": 300,
##                "y": 95,
##                "correct_zone": "target_zone"
##            },
##            
##            {
##                "id": "Waw",
##                "file": "27waw.PNG",
##                "size": (170, 190),
##                "x": -100,
##                "y": 110,
##            },
##            
##            {
##                "id": "Yaa",
##                "file": "28yaa.PNG",
##                "size": (190, 160),
##                "x": -500,
##                "y": 125,
##            },
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # واو
##    {
##        "type": "drag_drop",
##        "sound": "27waw-s.wav",
##        "items": [           
##            {
##                "id": "Heh",
##                "file": "26heh.PNG",
##                "size": (190, 160),
##                "x": 300,
##                "y": 95,
##            },
##            
##            {
##                "id": "Waw",
##                "file": "27waw.PNG",
##                "size": (170, 190),
##                "x": -100,
##                "y": 110,
##                "correct_zone": "target_zone"
##            },
##            
##            {
##                "id": "Yaa",
##                "file": "28yaa.PNG",
##                "size": (190, 160),
##                "x": -500,
##                "y": 125,
##            },
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },
##
##    # ياء
##    {
##        "type": "drag_drop",
##        "sound": "28yaa-s.wav",
##        "items": [           
##            {
##                "id": "Heh",
##                "file": "26heh.PNG",
##                "size": (190, 160),
##                "x": 300,
##                "y": 95,
##            },
##            
##            {
##                "id": "Waw",
##                "file": "27waw.PNG",
##                "size": (170, 190),
##                "x": -100,
##                "y": 110,
##            },
##            
##            {
##                "id": "Yaa",
##                "file": "28yaa.PNG",
##                "size": (190, 160),
##                "x": -500,
##                "y": 125,
##                "correct_zone": "target_zone"
##            },
##        ],
##        "drop_zones": [
##            {
##                "id": "target_zone",
##                "label": "",
##                "x": 0,
##                "y": -250,
##                "w": 250,
##                "h": 330
##            },
##        ]
##    },

    ##############################
    # Drag and drop Many to Many #
    ##############################
    {
        "type": "drag_drop",
        "sound": "Sort_the_letters.wav",
        "items": [
            {
                "id": "Alef",
                "file": "01alef.png",
                "size": (70, 280),
                "x": -25,
                "y": 100,
                "correct_zone": "zone1"
            },

            {
                "id": "ba",
                "file": "02ba.png",
                "size": (200, 150),
                "x": -1300,
                "y": -150,
                "correct_zone": "zone2"
            },
            
            {
                "id": "ta",
                "file": "03ta.png",
                "size": (200, 140),
                "x": -1150,
                "y": 150,
                "correct_zone": "zone3"
            },

            {
                "id": "tha",
                "file": "04tha.png", 
                "size": (200, 165),
                "x": -850,               
                "y": 300,
                "correct_zone": "zone4"
            },

            {
                "id": "geam",
                "file": "05geem.PNG",
                "size": (200, 210),
                "x": 75,
                "y": -300,
                "correct_zone": "zone5"
            },
            
            {
                "id": "ha",
                "file": "06ha.png",
                "size": (200, 210),
                "x": 1000,
                "y": 250,
                "correct_zone": "zone6"
            },

            {
                "id": "Ka",
                "file": "07ka.PNG",
                "size": (200, 275),
                "x": -1000,
                "y": -250,
                "correct_zone": "zone7"
            },

            {
                "id": "Dal",
                "file": "08dal.PNG",
                "size": (120, 140),
                "x": 800,
                "y": -350,
                "correct_zone": "zone8"
            },
            
            {
                "id": "Thal",
                "file": "09thal.PNG",
                "size": (120, 210),
                "x": -1150,
                "y": -450,
                "correct_zone": "zone9"
            },
            
            {
                "id": "Ra",
                "file": "10ra.PNG",
                "size": (170, 190),
                "x": -600,
                "y": -150,
                "correct_zone": "zone10"
            },

            {
                "id": "Zay",
                "file": "11zay.PNG",
                "size": (170, 270),
                "x": 275,
                "y": 250,
                "correct_zone": "zone11"
            },

            {
                "id": "Seen",
                "file": "12sen.PNG",
                "size": (210, 205),
                "x": 750,
                "y": 270,
                "correct_zone": "zone12"
            },
            
            {
                "id": "Sheen",
                "file": "13shen.PNG",
                "size": (210, 320),
                "x": -550,
                "y": -500,
                "correct_zone": "zone13"
            },
            
            {
                "id": "Sad",
                "file": "14sad.PNG",
                "size": (210, 210),
                "x": 750,
                "y": -100,
                "correct_zone": "zone14"
            },

            {
                "id": "Dad",
                "file": "15dad.PNG",
                "size": (210, 275),
                "x": 250,
                "y": 60,
                "correct_zone": "zone15"
            },

            {
                "id": "Taa",
                "file": "16taa.PNG",
                "size": (200, 270),
                "x": -100,
                "y": -200,
                "correct_zone": "zone16"
            },
            
            {
                "id": "Zaa",
                "file": "17zaa.PNG",
                "size": (200, 270),
                "x": 1000,
                "y": -300,
                "correct_zone": "zone17"
            },

            {
                "id": "Aen",
                "file": "18aen.PNG",
                "size": (200, 210),
                "x": -1350,
                "y": 250,
                "correct_zone": "zone18"
            },
            
            {
                "id": "Gean",
                "file": "19gean.PNG",
                "size": (200, 260),
                "x": 450,
                "y": -120,
                "correct_zone": "zone19"
            },
            
            {
                "id": "Feh",
                "file": "20feh.PNG",
                "size": (210, 150),
                "x": -600,
                "y": 200,
                "correct_zone": "zone20"
            },

            {
                "id": "Kf",
                "file": "21kf.PNG",
                "size": (190, 160),
                "x": 250,
                "y": -450,
                "correct_zone": "zone21"
            },

            {
                "id": "Kaf",
                "file": "22kaf.PNG",
                "size": (200, 275),
                "x": -300,
                "y": 0,
                "correct_zone": "zone22"
            },

            {
                "id": "Lam",
                "file": "23lam.PNG",
                "size": (170, 275),
                "x": -300,
                "y": -300,
                "correct_zone": "zone23"
            },

            {
                "id": "Meam",
                "file": "24meam.PNG",
                "size": (160, 165),
                "x": -800,
                "y": -400,
                "correct_zone": "zone24"
            },
            
            {
                "id": "Noon",
                "file": "25noon.PNG",
                "size": (190, 160),
                "x": 800,
                "y": 800,
                "correct_zone": "zone25"
            },

            {
                "id": "Heh",
                "file": "26heh.PNG",
                "size": (190, 160),
                "x": 0,
                "y": 300,
                "correct_zone": "zone26"
            },
            
            {
                "id": "Waw",
                "file": "27waw.PNG",
                "size": (170, 190),
                "x": 1200,
                "y": 0,
                "correct_zone": "zone27"
            },
            
            {
                "id": "Yaa",
                "file": "28yaa.PNG",
                "size": (190, 160),
                "x": -800,
                "y": -200,
                "correct_zone": "zone28"
            },

            
        ],
        "drop_zones": [
            {
                "id": "zone1",
                "label": "",
                "x": 1300,
                "y": -350,
                "w": 250,
                "h": 330
            },
            
            {
                "id": "zone2",
                "label": "",
                "x": 1040,
                "y": -350,
                "w": 250,
                "h": 330
            },
            
            {
                "id": "zone3",
                "label": "",
                "x": 780,
                "y": -350,
                "w": 250,
                "h": 330
            },
            
            {
                "id": "zone4",
                "label": "",
                "x": 520,
                "y": -350,
                "w": 250,
                "h": 330
            },

            
            {
                "id": "zone5",
                "label": "",
                "x": 260,
                "y": -350,
                "w": 250,
                "h": 330
            },

            
            {
                "id": "zone6",
                "label": "",
                "x": 0,
                "y": -350,
                "w": 250,
                "h": 330
            },

            
            {
                "id": "zone7",
                "label": "",
                "x": -260,
                "y": -350,
                "w": 250,
                "h": 330
            },

            
            {
                "id": "zone8",
                "label": "",
                "x": -520,
                "y": -350,
                "w": 250,
                "h": 330
            },

            
            {
                "id": "zone9",
                "label": "",
                "x": -780,
                "y": -350,
                "w": 250,
                "h": 330
            },

            
            {
                "id": "zone10",
                "label": "",
                "x": -1040,
                "y": -350,
                "w": 250,
                "h": 330
            },

            
            {
                "id": "zone11",
                "label": "",
                "x": -1300,
                "y": -350,
                "w": 250,
                "h": 330
            },
            
            {
                "id": "zone12",
                "label": "",
                "x": 1300,
                "y": -10,
                "w": 250,
                "h": 330
            },
                        {
                "id": "zone13",
                "label": "",
                "x": 1040,
                "y": -10,
                "w": 250,
                "h": 330
            },
            
            {
                "id": "zone14",
                "label": "",
                "x": 780,
                "y": -10,
                "w": 250,
                "h": 330
            },
            
            {
                "id": "zone15",
                "label": "",
                "x": 520,
                "y": -10,
                "w": 250,
                "h": 330
            },

            
            {
                "id": "zone16",
                "label": "",
                "x": 260,
                "y": -10,
                "w": 250,
                "h": 330
            },

            
            {
                "id": "zone17",
                "label": "",
                "x": 0,
                "y": -10,
                "w": 250,
                "h": 330
            },

            
            {
                "id": "zone18",
                "label": "",
                "x": -260,
                "y": -10,
                "w": 250,
                "h": 330
            },

            
            {
                "id": "zone19",
                "label": "",
                "x": -520,
                "y": -10,
                "w": 250,
                "h": 330
            },

            
            {
                "id": "zone20",
                "label": "",
                "x": -780,
                "y": -10,
                "w": 250,
                "h": 330
            },

            
            {
                "id": "zone21",
                "label": "",
                "x": -1040,
                "y": -10,
                "w": 250,
                "h": 330
            },

            
            {
                "id": "zone22",
                "label": "",
                "x": -1300,
                "y": -10,
                "w": 250,
                "h": 330
            },

            {
                "id": "zone23",
                "label": "",
                "x": 1300,
                "y": 330,
                "w": 250,
                "h": 330
            },

            {
                "id": "zone24",
                "label": "",
                "x": 1040,
                "y": 330,
                "w": 250,
                "h": 330
            },

            {
                "id": "zone25",
                "label": "",
                "x": 780,
                "y": 330,
                "w": 250,
                "h": 330
            },

            {
                "id": "zone26",
                "label": "",
                "x": -780,
                "y": 330,
                "w": 250,
                "h": 330
            },

            {
                "id": "zone27",
                "label": "",
                "x": -1040,
                "y": 330,
                "w": 250,
                "h": 330
            },

            {
                "id": "zone28",
                "label": "",
                "x": -1300,
                "y": 330,
                "w": 250,
                "h": 330
            },

        ]
    },

    
##    # Letter tracing question
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

class PracticeLevel1_P1(PracticeBase):
    """Practice 1 for Level 1 - Covers T1 and T2"""
    
    def __init__(self):
        super().__init__(level=1)
        self.practice_id = "P1"
    
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
        mark_learning_topic_complete(profile_name, 1, "P1")
    
    main_app.audio_manager.play_bg_music()
