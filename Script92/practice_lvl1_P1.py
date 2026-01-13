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
    # Alef
    {
        "type": "drag_drop",
        "sound": "01alef-s.wav",
        "items": [            
            {
                "id": "ba",
                "file": "02ba.png",
                "size": (200, 150),
                "x": 305,
                "y": 150,
            },

            {
                "id": "Alef",
                "file": "01alef.png",
                "size": (50, 210),
                "x": -25,
                "y": 40,
                "correct_zone": "target_zone" # Correct Answer
            },
            
            {
                "id": "ta",
                "file": "03ta.png",
                "size": (200, 140),
                "x": -475,
                "y": 105,
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -300,
                "w": 250,
                "h": 330
            },
        ]
    },


    # Baa
    {
        "type": "drag_drop",
        "sound": "02ba-s.wav",
        "items": [            
            {
                "id": "ba",
                "file": "02ba.png",
                "size": (200, 150),
                "x": -100,
                "y": 150,
                "correct_zone": "target_zone" # Correct Answer
            },

            {
                "id": "tha",
                "file": "04tha.png", 
                "size": (200, 165),
                "x": 300,               
                "y": 80,
            },
            
            {
                "id": "ta",
                "file": "03ta.png",
                "size": (200, 140),
                "x": -500,
                "y": 105,
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # Ta
    {
        "type": "drag_drop",
        "sound": "03ta-s.wav",
        "items": [            
            {
                "id": "ba_wrong",
                "file": "02ba.png",
                "size": (200, 150),
                "x": -100,
                "y": 150,
            },

            {
                "id": "tha_wrong",
                "file": "04tha.png", 
                "size": (200, 165),
                "x": 300,               
                "y": 80,
            },
            
            {
                "id": "ta_correct",
                "file": "03ta.png",
                "size": (200, 140),
                "x": -500,
                "y": 105,
                "correct_zone": "target_zone" # Correct Answer
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # Tha
    {
        "type": "drag_drop",
        "sound": "04tha-s.wav",
        "items": [            
            {
                "id": "ba",
                "file": "02ba.png",
                "size": (200, 150),
                "x": -100,
                "y": 150,
            },

            {
                "id": "tha",
                "file": "04tha.png", 
                "size": (200, 165),
                "x": 300,               
                "y": 80,
                "correct_zone": "target_zone" # Correct Answer
            },
            
            {
                "id": "ta",
                "file": "03ta.png",
                "size": (200, 140),
                "x": -500,
                "y": 105,
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # Geam
    {
        "type": "drag_drop",
        "sound": "05geem-s.wav",
        "items": [            
            {
                "id": "geam",
                "file": "05geem.PNG",
                "size": (200, 210),
                "x": 300,
                "y": 40,
                "correct_zone": "target_zone"
            },
            {
                "id": "ha",
                "file": "06ha.png",
                "size": (200, 210),
                "x": -100,
                "y": 40,
            },

            {
                "id": "Ka",
                "file": "07ka.PNG",
                "size": (200, 275),
                "x": -500,
                "y": -25,
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # حاء
    {
        "type": "drag_drop",
        "sound": "06ha-s.wav",
        "items": [            
            {
                "id": "geam",
                "file": "05geem.PNG",
                "size": (200, 210),
                "x": 300,
                "y": 40,
            },
            {
                "id": "ha",
                "file": "06ha.png",
                "size": (200, 210),
                "x": -100,
                "y": 40,
                "correct_zone": "target_zone"
            },

            {
                "id": "Ka",
                "file": "07ka.PNG",
                "size": (200, 275),
                "x": -500,
                "y": -25,
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # خاء
    {
        "type": "drag_drop",
        "sound": "07ka-s.wav",
        "items": [            
            {
                "id": "geam",
                "file": "05geem.PNG",
                "size": (200, 210),
                "x": 300,
                "y": 40,
            },
            {
                "id": "ha",
                "file": "06ha.png",
                "size": (200, 210),
                "x": -100,
                "y": 40,
            },

            {
                "id": "Ka",
                "file": "07ka.PNG",
                "size": (200, 275),
                "x": -500,
                "y": -25,
                "correct_zone": "target_zone"
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # دال
    {
        "type": "drag_drop",
        "sound": "08dal-s.wav",
        "items": [            
            {
                "id": "Dal",
                "file": "08dal.PNG",
                "size": (120, 140),
                "x": 350,
                "y": 105,
                "correct_zone": "target_zone"
            },
            {
                "id": "Thal",
                "file": "09thal.PNG",
                "size": (120, 210),
                "x": -50,
                "y": 35,
            },
            
            {
                "id": "Ra",
                "file": "10ra.PNG",
                "size": (170, 190),
                "x": -500,
                "y": 110,
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # ذال
    {
        "type": "drag_drop",
        "sound": "09thal-s.wav",
        "items": [            
            {
                "id": "Dal",
                "file": "08dal.PNG",
                "size": (120, 140),
                "x": 350,
                "y": 105,
            },
            {
                "id": "Thal",
                "file": "09thal.PNG",
                "size": (120, 210),
                "x": -50,
                "y": 35,
                "correct_zone": "target_zone"
            },
            
            {
                "id": "Ra",
                "file": "10ra.PNG",
                "size": (170, 190),
                "x": -500,
                "y": 110,
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # راء
    {
        "type": "drag_drop",
        "sound": "10ra-s.wav",
        "items": [            
            {
                "id": "Thal",
                "file": "09thal.PNG",
                "size": (120, 210),
                "x": 350,
                "y": 35,
            },
            
            {
                "id": "Ra",
                "file": "10ra.PNG",
                "size": (170, 190),
                "x": -100,
                "y": 110,
                "correct_zone": "target_zone"
            },
            {
                "id": "Zay",
                "file": "11zay.PNG",
                "size": (170, 270),
                "x": -500,
                "y": 30,
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # زاي
    {
        "type": "drag_drop",
        "sound": "11zay-s.wav",
        "items": [            
            {
                "id": "Thal",
                "file": "09thal.PNG",
                "size": (120, 210),
                "x": 350,
                "y": 35,
            },
            
            {
                "id": "Ra",
                "file": "10ra.PNG",
                "size": (170, 190),
                "x": -100,
                "y": 110,
            },
            {
                "id": "Zay",
                "file": "11zay.PNG",
                "size": (170, 270),
                "x": -500,
                "y": 30,
                "correct_zone": "target_zone"
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # سين
    {
        "type": "drag_drop",
        "sound": "12sen-s.wav",
        "items": [            
            {
                "id": "Seen",
                "file": "12sen.PNG",
                "size": (210, 205),
                "x": 300,
                "y": 130,
                "correct_zone": "target_zone"
            },
            
            {
                "id": "Sheen",
                "file": "13shen.PNG",
                "size": (210, 320),
                "x": -100,
                "y": 15,
            },
            
            {
                "id": "Sad",
                "file": "14sad.PNG",
                "size": (210, 210),
                "x": -500,
                "y": 130,
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # شين
    {
        "type": "drag_drop",
        "sound": "13shen-s.wav",
        "items": [            
            {
                "id": "Seen",
                "file": "12sen.PNG",
                "size": (210, 205),
                "x": 300,
                "y": 130,
            },
            
            {
                "id": "Sheen",
                "file": "13shen.PNG",
                "size": (210, 320),
                "x": -100,
                "y": 15,
                "correct_zone": "target_zone"
            },
            
            {
                "id": "Sad",
                "file": "14sad.PNG",
                "size": (210, 210),
                "x": -500,
                "y": 130,
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # صاد
    {
        "type": "drag_drop",
        "sound": "14sad-s.wav",
        "items": [            
            {
                "id": "Sheen",
                "file": "13shen.PNG",
                "size": (210, 320),
                "x": 300,
                "y": 15,
            },
            
            {
                "id": "Sad",
                "file": "14sad.PNG",
                "size": (210, 210),
                "x": -100,
                "y": 130,
                "correct_zone": "target_zone"
            },
            {
                "id": "Dad",
                "file": "15dad.PNG",
                "size": (210, 275),
                "x": -500,
                "y": 60,
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # ضاد
    {
        "type": "drag_drop",
        "sound": "15dad-s.wav",
        "items": [            
            {
                "id": "Sheen",
                "file": "13shen.PNG",
                "size": (210, 320),
                "x": 300,
                "y": 15,
            },
            
            {
                "id": "Sad",
                "file": "14sad.PNG",
                "size": (210, 210),
                "x": -100,
                "y": 130,
            },
            {
                "id": "Dad",
                "file": "15dad.PNG",
                "size": (210, 275),
                "x": -500,
                "y": 60,
                "correct_zone": "target_zone"
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # طاء
    {
        "type": "drag_drop",
        "sound": "16taa-s.wav",
        "items": [
            {
                "id": "Dad",
                "file": "15dad.PNG",
                "size": (210, 275),
                "x": 300,
                "y": 60,
            },

            {
                "id": "Taa",
                "file": "16taa.PNG",
                "size": (200, 270),
                "x": -100,
                "y": -25,
                "correct_zone": "target_zone"
            },
            
            {
                "id": "Zaa",
                "file": "17zaa.PNG",
                "size": (200, 270),
                "x": -500,
                "y": -25,
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # ظاء
    {
        "type": "drag_drop",
        "sound": "17zaa-s.wav",
        "items": [            
            {
                "id": "Dad",
                "file": "15dad.PNG",
                "size": (210, 275),
                "x": 300,
                "y": 60,
            },

            {
                "id": "Taa",
                "file": "16taa.PNG",
                "size": (200, 270),
                "x": -100,
                "y": -25,
            },
            
            {
                "id": "Zaa",
                "file": "17zaa.PNG",
                "size": (200, 270),
                "x": -500,
                "y": -25,
                "correct_zone": "target_zone"
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # عين
    {
        "type": "drag_drop",
        "sound": "18aen-s.wav",
        "items": [            
            {
                "id": "Aen",
                "file": "18aen.PNG",
                "size": (200, 210),
                "x": 300,
                "y": 40,
                "correct_zone": "target_zone"
            },
            
            {
                "id": "Gean",
                "file": "19gean.PNG",
                "size": (200, 260),
                "x": -100,
                "y": -15,
            },
            
            {
                "id": "Feh",
                "file": "20feh.PNG",
                "size": (210, 150),
                "x": -500,
                "y": 95,
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # غين
    {
        "type": "drag_drop",
        "sound": "19gean-s.wav",
        "items": [            
            {
                "id": "Aen",
                "file": "18aen.PNG",
                "size": (200, 210),
                "x": 300,
                "y": 40,
            },
            
            {
                "id": "Gean",
                "file": "19gean.PNG",
                "size": (200, 260),
                "x": -100,
                "y": -15,
                "correct_zone": "target_zone"
            },
            
            {
                "id": "Feh",
                "file": "20feh.PNG",
                "size": (210, 150),
                "x": -500,
                "y": 95,
            },

        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # فاء
    {
        "type": "drag_drop",
        "sound": "20feh-s.wav",
        "items": [            
            {
                "id": "Gean",
                "file": "19gean.PNG",
                "size": (200, 260),
                "x": 300,
                "y": -15,
            },
            
            {
                "id": "Feh",
                "file": "20feh.PNG",
                "size": (210, 150),
                "x": -100,
                "y": 95,
                "correct_zone": "target_zone"
            },

            {
                "id": "Kf",
                "file": "21kf.PNG",
                "size": (190, 160),
                "x": -500,
                "y": 95,
            },
        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # قاف
    {
        "type": "drag_drop",
        "sound": "21kf-s.wav",
        "items": [            
            {
                "id": "Gean",
                "file": "19gean.PNG",
                "size": (200, 260),
                "x": 300,
                "y": -15,
            },
            
            {
                "id": "Feh",
                "file": "20feh.PNG",
                "size": (210, 150),
                "x": -100,
                "y": 95,
            },

            {
                "id": "Kf",
                "file": "21kf.PNG",
                "size": (190, 160),
                "x": -500,
                "y": 95,
                "correct_zone": "target_zone"
            },
        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # كاف
    {
        "type": "drag_drop",
        "sound": "22kaf-s.wav",
        "items": [           
            {
                "id": "Feh",
                "file": "20feh.PNG",
                "size": (210, 150),
                "x": 300,
                "y": 95,
            },

            {
                "id": "Kf",
                "file": "21kf.PNG",
                "size": (190, 160),
                "x": -100,
                "y": 95,
            },

            {
                "id": "Kaf",
                "file": "22kaf.PNG",
                "size": (200, 275),
                "x": -500,
                "y": -25,
                "correct_zone": "target_zone"
            },
        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # لام
    {
        "type": "drag_drop",
        "sound": "23lam-s.wav",
        "items": [           
            {
                "id": "Lam",
                "file": "23lam.PNG",
                "size": (170, 275),
                "x": 300,
                "y": -25,
                "correct_zone": "target_zone"
            },

            {
                "id": "Meam",
                "file": "24meam.PNG",
                "size": (160, 165),
                "x": -100,
                "y": 85,
            },
            
            {
                "id": "Noon",
                "file": "25noon.PNG",
                "size": (190, 160),
                "x": -500,
                "y": 85,
            },
        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # ميم
    {
        "type": "drag_drop",
        "sound": "24meam-s.wav",
        "items": [           
            {
                "id": "Lam",
                "file": "23lam.PNG",
                "size": (170, 275),
                "x": 300,
                "y": -25,
            },

            {
                "id": "Meam",
                "file": "24meam.PNG",
                "size": (160, 165),
                "x": -100,
                "y": 85,
                "correct_zone": "target_zone"
            },
            
            {
                "id": "Noon",
                "file": "25noon.PNG",
                "size": (190, 160),
                "x": -500,
                "y": 85,
            },
        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # نون
    {
        "type": "drag_drop",
        "sound": "25noon-s.wav",
        "items": [           
            {
                "id": "Lam",
                "file": "23lam.PNG",
                "size": (170, 275),
                "x": 300,
                "y": -25,
            },

            {
                "id": "Meam",
                "file": "24meam.PNG",
                "size": (160, 165),
                "x": -100,
                "y": 85,
            },
            
            {
                "id": "Noon",
                "file": "25noon.PNG",
                "size": (190, 160),
                "x": -500,
                "y": 85,
                "correct_zone": "target_zone"
            },
        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # هاء
    {
        "type": "drag_drop",
        "sound": "26heh-s.wav",
        "items": [           
            {
                "id": "Heh",
                "file": "26heh.PNG",
                "size": (190, 160),
                "x": 300,
                "y": 95,
                "correct_zone": "target_zone"
            },
            
            {
                "id": "Waw",
                "file": "27waw.PNG",
                "size": (170, 190),
                "x": -100,
                "y": 110,
            },
            
            {
                "id": "Yaa",
                "file": "28yaa.PNG",
                "size": (190, 160),
                "x": -500,
                "y": 125,
            },
        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # واو
    {
        "type": "drag_drop",
        "sound": "27waw-s.wav",
        "items": [           
            {
                "id": "Heh",
                "file": "26heh.PNG",
                "size": (190, 160),
                "x": 300,
                "y": 95,
            },
            
            {
                "id": "Waw",
                "file": "27waw.PNG",
                "size": (170, 190),
                "x": -100,
                "y": 110,
                "correct_zone": "target_zone"
            },
            
            {
                "id": "Yaa",
                "file": "28yaa.PNG",
                "size": (190, 160),
                "x": -500,
                "y": 125,
            },
        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

    # ياء
    {
        "type": "drag_drop",
        "sound": "28yaa-s.wav",
        "items": [           
            {
                "id": "Heh",
                "file": "26heh.PNG",
                "size": (190, 160),
                "x": 300,
                "y": 95,
            },
            
            {
                "id": "Waw",
                "file": "27waw.PNG",
                "size": (170, 190),
                "x": -100,
                "y": 110,
            },
            
            {
                "id": "Yaa",
                "file": "28yaa.PNG",
                "size": (190, 160),
                "x": -500,
                "y": 125,
                "correct_zone": "target_zone"
            },
        ],
        "drop_zones": [
            {
                "id": "target_zone",
                "label": "",
                "x": 0,
                "y": -250,
                "w": 250,
                "h": 330
            },
        ]
    },

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

      ###########################
      # Letter tracing question #
      ###########################
    
    {
        "type": "tracing",
        "sound": "01alef-s.wav",
        "letter_image": "01alef.png",
        "letter_size": (160, 550), # Adjust size to fit
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        # ✅ NEW: Defined as separate segments
        "segments": [
            # Segment 1: The main curve (Right to Left)
            [
                (81, 171), (88, 248), (98, 343), (104, 427), (104, 500)
            ],
            # Segment 2: The dot below
            [
                (120, 18), (77, 18), (34, 50), (70, 81), (132, 79), (22, 112) # A short stroke for the dot
            ]
        ]
    },
    
    {
        "type": "tracing",
        "sound": "02ba-s.wav",
        "letter_image": "02ba.png",
        "letter_size": (450, 337), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (414, 28), (434, 94), (434, 176), (369, 176), (283, 176), (185, 176), (83, 176), (19, 121), (33, 23)
            ],
    
            [
                (220, 295), (230, 295) 
            ]
        ]
    },
    
    {
        "type": "tracing",
        "sound": "03ta-s.wav",
        "letter_image": "03ta.png",
        "letter_size": (450, 337), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (411, 131), (426, 182), (436, 245), (434, 301), (367, 301), (281, 301), (185, 301), (81, 301), (26, 245), (16, 182), (35, 131)
            ],
    
            [
                (270, 35), (260, 35) 
            ],

            [
                (193, 64), (183, 64) 
            ]
        ]
    },
    
    {
        "type": "tracing",
        "sound": "04tha-s.wav",
        "letter_image": "04tha.png",
        "letter_size": (450, 360), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (411, 179), (433, 267), (434, 332), (367, 332), (281, 332), (185, 332), (81, 332), (12, 267), (35, 179)
            ],
    
            [
                (265, 85), (255, 85) 
            ],

            [
                (192, 112), (182, 112) 
            ],
            [
                (205, 31), (195, 31) 
            ]
        ]
    },

    {
        "type": "tracing",
        "sound": "05geem-s.wav",
        "letter_image": "05geem.png",
        "letter_size": (450, 550), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (382,45), (335, 45), (280, 45), (225, 45), (170, 45), (115, 45), (60, 45)
            ],
    
            [
                (280, 45), (189, 100), (103, 155), (47, 210), (22, 265), (17, 320), (24, 375), (55, 430), (140, 485), (235, 509), (364, 509) 
            ],

            [
                (250, 285), (240, 285) 
            ],
        ]
    },
    
    {
        "type": "tracing",
        "sound": "06ha-s.wav",
        "letter_image": "06ha.png",
        "letter_size": (450, 550), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (382,45), (335, 45), (280, 45), (225, 45), (170, 45), (115, 45), (60, 45)
            ],
    
            [
                (280, 45), (189, 100), (103, 155), (47, 210), (22, 265), (17, 320), (24, 375), (55, 430), (140, 485), (235, 509), (364, 509) 
            ],
        ]
    },
    
    {
        "type": "tracing",
        "sound": "07ka-s.wav",
        "letter_image": "07ka.png",
        "letter_size": (450, 750), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (382,229), (335, 229), (280, 229), (225, 229), (170, 229), (115, 229), (60, 229)
            ],
    
            [
                (280, 229), (189, 287), (103, 342), (47, 397), (22, 452), (17, 507), (24, 562), (55, 617), (140, 672), (235, 696), (364, 696) 
            ],

            [
                (220, 46), (210, 46) 
            ],
        ]
    },

    {
        "type": "tracing",
        "sound": "08dal-s.wav",
        "letter_image": "08dal.png",
        "letter_size": (300, 400), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (162, 53), (209, 92), (244, 132),(265, 180), (278, 230), (282, 280), (279, 349), (225, 349), (170, 349), (105, 349), (50, 349), (16, 305)
            ],
        ]
    },

    {
        "type": "tracing",
        "sound": "09thal-s.wav",
        "letter_image": "09thal.png",
        "letter_size": (300, 450), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (160, 189), (214, 219), (247, 249), (267, 289), (275, 320), (280, 360), (279, 415), (225, 415), (170, 415), (115, 415), (55, 415), (18, 380)
            ],
    
            [
                (108, 38), (98, 38)
            ],

        ]
    },

    {
        "type": "tracing",
        "sound": "10ra-s.wav",
        "letter_image": "10ra.png",
        "letter_size": (300, 400), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (253, 40), (278, 100), (288, 160), (285, 220), (255, 280), (211, 330), (140, 370), (84, 370), (23, 351)
            ],
        ]
    },

    {
        "type": "tracing",
        "sound": "11zay-s.wav",
        "letter_image": "11zay.png",
        "letter_size": (300, 450), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (251, 161), (282, 220), (286, 280), (267, 340), (211, 390), (156, 425), (92, 425), (31, 412)
            ],
    
            [
                (219, 34), (209, 34)
            ],

        ]
    },

    {
        "type": "tracing",
        "sound": "12sen-s.wav",
        "letter_image": "12sen.png",
        "letter_size": (550, 400), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (522, 45), (537, 182), (460, 159), (456, 60), (425, 157), (333, 186), (310, 51), (333, 186), (309, 284), (238, 342), (154, 358), (76, 347), (27, 303), (18, 208), (52, 91) 
            ],
        ]
    },

    {
        "type": "tracing",
        "sound": "13shen-s.wav",
        "letter_image": "13shen.png",
        "letter_size": (550, 460), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (522, 206), (538, 303), (455, 284), (455, 223), (430, 284), (336, 305), (311, 205), (327, 247), (327, 347), (272, 403), (184, 430), (102, 430), (29, 397), (18, 321), (50, 238) 
            ],
    
            [
                (476, 96), (466, 96) 
            ],
            [
                (405, 105), (395, 105) 
            ],
            [
                (423, 32), (413, 32) 
            ],           
        ]
    },

    {
        "type": "tracing",
        "sound": "14sad-s.wav",
        "letter_image": "14sad.png",
        "letter_size": (550, 400), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (286, 175), (350, 121), (417, 65), (484, 41), (528, 104), (528, 175), (460, 175), (390, 175), (320, 175), (250, 175), (230, 40), (243, 147), (243, 230), (212, 309), (150, 349), (74, 352), (20, 302), (14, 209), (36, 97) 
            ],
        ]
    },

    {
        "type": "tracing",
        "sound": "15dad-s.wav",
        "letter_image": "15dad.png",
        "letter_size": (550, 460), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (299, 275), (351, 226), (408, 183), (465, 160), (527, 205), (525, 275), (445, 275), (355, 275), (252, 275), (232, 158), (241, 239), (240, 333), (176, 413), (92, 424), (29, 397), (12, 321), (34, 212) 
            ],
    
            [
                (356, 39), (346, 39) 
            ],

        ]
    },

    {
        "type": "tracing",
        "sound": "16taa-s.wav",
        "letter_image": "16taa.png",
        "letter_size": (550, 550), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (169, 510), (249, 435), (347, 386), (449, 363), (510, 413), (513, 510), (449, 510), (347, 510), (249, 510), (169, 510), (70, 510) 
            ],

            [
                (208, 43), (229, 140), (251, 240), (256, 340),(246, 438) 
            ],
        ]
    },

    {
        "type": "tracing",
        "sound": "17zaa-s.wav",
        "letter_image": "17zaa.png",
        "letter_size": (550, 550), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (169, 510), (249, 435), (347, 386), (449, 363), (510, 413), (513, 510), (449, 510), (347, 510), (249, 510), (169, 510), (70, 510) 
            ],
    
            [
                (208, 43), (229, 140), (251, 240), (256, 340),(246, 438)  
            ],

            [
                (404, 180), (394, 180)
            ],
        ]
    },

    {
        "type": "tracing",
        "sound": "18aen-s.wav",
        "letter_image": "18aen.png",
        "letter_size": (400, 600), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (192, 32), (128, 22), (46, 64), (27, 133), (68, 182), (133, 216), (192, 187), (283, 153), (235, 169), (133, 216), (62, 287), (25, 361), (25, 461), (113, 534), (234, 561), (346, 550)  
            ],
        ]
    },

    {
        "type": "tracing",
        "sound": "19gean-s.wav",
        "letter_image": "19gean.png",
        "letter_size": (400, 750), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (192, 183), (128, 173), (46, 215), (27, 284), (68, 333), (133, 367), (192, 338), (283, 304), (235, 320), (133, 367), (62, 438), (25, 512), (25, 612), (113, 685), (234, 712), (346, 701)
            ],
    
            [
                (138, 38), (128, 38) 
            ],
        ]
    },

    {
        "type": "tracing",
        "sound": "20feh-s.wav",
        "letter_image": "20feh.png",
        "letter_size": (450, 337), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (428,251), (360, 227), (361, 172), (395, 147), (428, 199), (428, 309), (367, 309), (281, 309), (185, 309), (81, 291), (16, 245), (30, 149)
            ],
    
            [
                (364, 31), (354, 31) 
            ],
        ]
    },
    
    {
        "type": "tracing",
        "sound": "21kf-s.wav",
        "letter_image": "21kf.png",
        "letter_size": (450, 410), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (422, 219), (348, 232), (292, 221), (292, 168), (348, 138), (400,168), (433, 290), (367, 360), (281, 381), (185, 387), (81, 369), (18, 299), (51, 204)
            ],
    
            [
                (357, 30), (347, 30) 
            ],

            [
                (272, 34), (262, 34) 
            ],
        ]
    },

    {
        "type": "tracing",
        "sound": "22kaf-s.wav",
        "letter_image": "22kaf.png",
        "letter_size": (400, 750), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (327, 56), (344, 176), (352, 290), (361, 410), (372, 530), (377, 600), (379, 690), (290, 690), (200, 690), (110, 690), (37, 641), (15, 560), (35, 437)
            ],
    
            [
                (237, 218), (191, 293), (187, 339), (252, 384), (243, 478), (119, 497)
            ],
        ]
    },

    {
        "type": "tracing",
        "sound": "23lam-s.wav",
        "letter_image": "23lam.png",
        "letter_size": (300, 700), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (240, 41), (253, 140), (264, 240), (274, 340), (283, 440), (286, 540), (227, 630), (140, 666), (52, 632), (16, 558), (21, 464), (52, 357)
            ],
        ]
    },

    {
        "type": "tracing",
        "sound": "24meam-s.wav",
        "letter_image": "24meam.png",
        "letter_size": (450, 337), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (214, 104), (254, 158), (340, 191), (405, 150), (416, 97), (355, 39), (271, 39), (180, 161), (147, 216), (97, 264), (24, 297)
            ],
    
        ]
    },

    {
        "type": "tracing",
        "sound": "25noon-s.wav",
        "letter_image": "25noon.png",
        "letter_size": (450, 410), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (405, 137), (432, 223), (430, 288), (364, 349), (278, 374), (184, 385), (80, 367), (23, 297), (35, 232), (66, 170)
            ],
    
            [
                (247, 35), (237, 35) 
            ],
        ]
    },

    {
        "type": "tracing",
        "sound": "26heh-s.wav",
        "letter_image": "26heh.png",
        "letter_size": (450, 410), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (258, 55), (334, 141), (390, 208), (430, 309), (399, 365), (327, 326), (252, 293), (198, 241), (202, 187), (263, 135), (334, 141), (330, 229), (252, 293), (183, 336), (102, 377)
            ],
        ]
    },

    {
        "type": "tracing",
        "sound": "27waw-s.wav",
        "letter_image": "27waw.png",
        "letter_size": (350, 500), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (332, 205), (243, 205), (221, 146), (231, 85), (275, 36), (315, 85), (331, 146), (329, 272), (307, 335), (265, 402), (200, 452), (109, 463), (23, 434)
            ],

        ]
    },

    {
        "type": "tracing",
        "sound": "28yaa-s.wav",
        "letter_image": "28yaa.png",
        "letter_size": (450, 500), 
        "letter_x_ratio": 0.5,
        "letter_y_ratio": 0.5,
        
        "segments": [
            [
                (434, 51), (377, 24), (298, 79), (258, 137), (252, 190), (335, 199), (405, 212), (377, 284), (303, 328), (199, 357), (111, 354), (36, 316), (16, 255), (30, 178), (64, 102)
            ],
    
            [
                (272, 452), (262, 452) 
            ],

            [
                (192, 452), (182, 452) 
            ],
        ]
    },


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
