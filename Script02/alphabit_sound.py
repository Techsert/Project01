import tkinter as tk
from PIL import Image, ImageTk
import pygame
import os
#from functools import partial


# Initialize pygame mixer
pygame.mixer.init()

# Sample slide data
slides = [
        # Intro Slide
    {
        "title": "أصوات الحُروف",
        "narration": "../assets/sounds/alphabitSound/intro01.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/k8.jpg", "delay": 1500, "scale": (0.25, 0.55), "position": "center"},
        ]
    },
        # Slide 1 - Alef
    {
        "title": "حرف الألف",
        "narration": "../assets/sounds/alphabitSound/01alef-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/01alef.png", "delay": 0, "scale": (0.05, 0.50), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/01alef-f.png", "sound": "../assets/sounds/alphabitSound/01alef-f.wav", "delay": 3000, "scale": (0.05, 0.45), "position": "center-right", "offset": {"x": -200, "y": 0}},
            {"path": "../assets/img/alphabitSound/01alef-k.png", "sound": "../assets/sounds/alphabitSound/01alef-k.wav", "delay": 7000, "scale": (0.05, 0.45), "position": "center"},
            {"path": "../assets/img/alphabitSound/01alef-d.png", "sound": "../assets/sounds/alphabitSound/01alef-d.wav", "delay": 10000, "scale": (0.05, 0.45), "position": "center-left", "offset": {"x": 180, "y": 0}}
        ]
    },
        # Slide 2 - Ba
    {
       "title": "حرف الباء",
        "narration": "../assets/sounds/alphabitSound/02ba-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/02ba.png", "delay": 0, "scale": (0.20, 0.45), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/02ba-f.png", "sound": "../assets/sounds/alphabitSound/02ba-f.wav", "delay": 3000, "scale": (0.15, 0.40), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/02ba-k.png", "sound": "../assets/sounds/alphabitSound/02ba-k.wav", "delay": 7000, "scale": (0.15, 0.40), "position": "center", "offset": {"x": 0, "y": 70}},
            {"path": "../assets/img/alphabitSound/02ba-d.png", "sound": "../assets/sounds/alphabitSound/02ba-d.wav", "delay": 11000, "scale": (0.15, 0.40), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
        # Slide 3 - Ta
    {
        "title": "حرف التاء",
        "narration": "../assets/sounds/alphabitSound/03ta-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/03ta.png", "delay": 0, "scale": (0.20, 0.45), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/03ta-f.png", "sound": "../assets/sounds/alphabitSound/03ta-f.wav", "delay": 3000, "scale": (0.15, 0.40), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/03ta-k.png", "sound": "../assets/sounds/alphabitSound/03ta-k.wav", "delay": 7000, "scale": (0.15, 0.40), "position": "center", "offset": {"x": 0, "y": 70}},
            {"path": "../assets/img/alphabitSound/03ta-d.png", "sound": "../assets/sounds/alphabitSound/03ta-d.wav", "delay": 11000, "scale": (0.15, 0.40), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
        # Slide 4 - Tha
    {
        "title": "حرف الثاء",
        "narration": "../assets/sounds/alphabitSound/04tha-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/04tha.png", "delay": 0, "scale": (0.20, 0.45), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/04tha-f.png", "sound": "../assets/sounds/alphabitSound/04tha-f.wav", "delay": 3000, "scale": (0.15, 0.40), "position": "center-right", "offset": {"x": -150, "y": -10}},
            {"path": "../assets/img/alphabitSound/04tha-k.png", "sound": "../assets/sounds/alphabitSound/04tha-k.wav", "delay": 7000, "scale": (0.15, 0.40), "position": "center", "offset": {"x": 0, "y": 60}},
            {"path": "../assets/img/alphabitSound/04tha-d.png", "sound": "../assets/sounds/alphabitSound/04tha-d.wav", "delay": 10000, "scale": (0.15, 0.40), "position": "center-left", "offset": {"x": 150, "y": -30}}
        ]
    },
            # Slide 5 - Gem
    {
        "title": "حرف الجيم",
        "narration": "../assets/sounds/alphabitSound/05gem-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/05gem.png", "delay": 0, "scale": (0.20, 0.40), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/05gem-f.png", "sound": "../assets/sounds/alphabitSound/05gem-f.wav", "delay": 3000, "scale": (0.15, 0.35), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/05gem-k.png", "sound": "../assets/sounds/alphabitSound/05gem-k.wav", "delay": 7000, "scale": (0.15, 0.35), "position": "center", "offset": {"x": 0, "y": 80}},
            {"path": "../assets/img/alphabitSound/05gem-d.png", "sound": "../assets/sounds/alphabitSound/05gem-d.wav", "delay": 10000, "scale": (0.15, 0.35), "position": "center-left", "offset": {"x": 150, "y": 20}}
        ]
    },
            # Slide 6 - 7a
    {
        "title": "حرف الحاء",
        "narration": "../assets/sounds/alphabitSound/06ha-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/06ha.png", "delay": 0, "scale": (0.20, 0.40), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/06ha-f.png", "sound": "../assets/sounds/alphabitSound/06ha-f.wav", "delay": 3000, "scale": (0.15, 0.35), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/06ha-k.png", "sound": "../assets/sounds/alphabitSound/06ha-k.wav", "delay": 7000, "scale": (0.15, 0.35), "position": "center", "offset": {"x": 0, "y": 70}},
            {"path": "../assets/img/alphabitSound/06ha-d.png", "sound": "../assets/sounds/alphabitSound/06ha-d.wav", "delay": 10000, "scale": (0.15, 0.35), "position": "center-left", "offset": {"x": 150, "y": 20}} 
        ]
    },
            # Slide 7 - ka
    {
        "title": "حرف الخاء",
        "narration": "../assets/sounds/alphabitSound/07ka-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/07ka.png", "delay": 0, "scale": (0.20, 0.45), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/07ka-f.png", "sound": "../assets/sounds/alphabitSound/07ka-f.wav", "delay": 3000, "scale": (0.15, 0.40), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/07ka-k.png", "sound": "../assets/sounds/alphabitSound/07ka-k.wav", "delay": 7000, "scale": (0.15, 0.40), "position": "center", "offset": {"x": 0, "y": 0}},
            {"path": "../assets/img/alphabitSound/07ka-d.png", "sound": "../assets/sounds/alphabitSound/07ka-d.wav", "delay": 10000, "scale": (0.15, 0.40), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
            # Slide 8 - Dal
    {
        "title": "حرف الدال",
        "narration": "../assets/sounds/alphabitSound/08dal-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/08dal.png", "delay": 0, "scale": (0.10, 0.30), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/08dal-f.png", "sound": "../assets/sounds/alphabitSound/08dal-f.wav", "delay": 3000, "scale": (0.10, 0.30), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/08dal-k.png", "sound": "../assets/sounds/alphabitSound/08dal-k.wav", "delay": 7000, "scale": (0.10, 0.30), "position": "center", "offset": {"x": 0, "y": 40}},
            {"path": "../assets/img/alphabitSound/08dal-d.png", "sound": "../assets/sounds/alphabitSound/08dal-d.wav", "delay": 10000, "scale": (0.10, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
            # Slide 9 - Thal
    {
        "title": "حرف الذال",
        "narration": "../assets/sounds/alphabitSound/09thal-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/09thal.png", "delay": 0, "scale": (0.10, 0.35), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/09thal-f.png", "sound": "../assets/sounds/alphabitSound/09thal-f.wav", "delay": 3000, "scale": (0.10, 0.35), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/09thal-k.png", "sound": "../assets/sounds/alphabitSound/09thal-k.wav", "delay": 7000, "scale": (0.10, 0.35), "position": "center", "offset": {"x": 0, "y": 60}},
            {"path": "../assets/img/alphabitSound/09thal-d.png", "sound": "../assets/sounds/alphabitSound/09thal-d.wav", "delay": 10000, "scale": (0.10, 0.35), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
            # Slide 10 - Ra
    {
        "title": "حرف الراء",
        "narration": "../assets/sounds/alphabitSound/10ra-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/10ra.png", "delay": 0, "scale": (0.15, 0.35), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/10ra-f.png", "sound": "../assets/sounds/alphabitSound/10ra-f.wav", "delay": 3000, "scale": (0.10, 0.30), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/10ra-k.png", "sound": "../assets/sounds/alphabitSound/10ra-k.wav", "delay": 7000, "scale": (0.10, 0.30), "position": "center", "offset": {"x": 0, "y": 40}},
            {"path": "../assets/img/alphabitSound/10ra-d.png", "sound": "../assets/sounds/alphabitSound/10ra-d.wav", "delay": 10000, "scale": (0.10, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
            # Slide 11 - Zay
    {
        "title": "حرف الزاي",
        "narration": "../assets/sounds/alphabitSound/11zay-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/11zay.png", "delay": 0, "scale": (0.15, 0.35), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/11zay-f.png", "sound": "../assets/sounds/alphabitSound/11zay-f.wav", "delay": 3000, "scale": (0.10, 0.30), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/11zay-k.png", "sound": "../assets/sounds/alphabitSound/11zay-k.wav", "delay": 7000, "scale": (0.10, 0.30), "position": "center", "offset": {"x": 0, "y": 40}},
            {"path": "../assets/img/alphabitSound/11zay-d.png", "sound": "../assets/sounds/alphabitSound/11zay-d.wav", "delay": 10000, "scale": (0.10, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
            # Slide 12 - Sen
    {
        "title": "حرف السين",
        "narration": "../assets/sounds/alphabitSound/12sen-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/12sen.png", "delay": 0, "scale": (0.20, 0.35), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/12sen-f.png", "sound": "../assets/sounds/alphabitSound/12sen-f.wav", "delay": 3000, "scale": (0.15, 0.30), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/12sen-k.png", "sound": "../assets/sounds/alphabitSound/12sen-k.wav", "delay": 7000, "scale": (0.15, 0.30), "position": "center", "offset": {"x": 0, "y": 40}},
            {"path": "../assets/img/alphabitSound/12sen-d.png", "sound": "../assets/sounds/alphabitSound/12sen-d.wav", "delay": 10000, "scale": (0.15, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
            # Slide 13 - Shen
    {
        "title": "حرف الشين",
        "narration": "../assets/sounds/alphabitSound/13shen-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/13shen.png", "delay": 0, "scale": (0.20, 0.35), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/13shen-f.png", "sound": "../assets/sounds/alphabitSound/13shen-f.wav", "delay": 3000, "scale": (0.15, 0.30), "position": "center-right", "offset": {"x": -150, "y": 20}},
            {"path": "../assets/img/alphabitSound/13shen-k.png", "sound": "../assets/sounds/alphabitSound/13shen-k.wav", "delay": 7000, "scale": (0.15, 0.30), "position": "center", "offset": {"x": 0, "y": 60}},
            {"path": "../assets/img/alphabitSound/13shen-d.png", "sound": "../assets/sounds/alphabitSound/13shen-d.wav", "delay": 10000, "scale": (0.15, 0.30), "position": "center-left", "offset": {"x": 150, "y": 50}}
        ]
    },
            # Slide 14 - Sad
    {
        "title": "حرف الصاد",
        "narration": "../assets/sounds/alphabitSound/14sad-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/14sad.png", "delay": 0, "scale": (0.20, 0.35), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/14sad-f.png", "sound": "../assets/sounds/alphabitSound/14sad-f.wav", "delay": 3000, "scale": (0.15, 0.30), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/14sad-k.png", "sound": "../assets/sounds/alphabitSound/14sad-k.wav", "delay": 7000, "scale": (0.15, 0.30), "position": "center", "offset": {"x": 0, "y": 40}},
            {"path": "../assets/img/alphabitSound/14sad-d.png", "sound": "../assets/sounds/alphabitSound/14sad-d.wav", "delay": 10000, "scale": (0.15, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
            # Slide 15 - Dad
    {
        "title": "حرف الضاد",
        "narration": "../assets/sounds/alphabitSound/15dad-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/15dad.png", "delay": 0, "scale": (0.20, 0.40), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/15dad-f.png", "sound": "../assets/sounds/alphabitSound/15dad-f.wav", "delay": 3000, "scale": (0.15, 0.30), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/15dad-k.png", "sound": "../assets/sounds/alphabitSound/15dad-k.wav", "delay": 7000, "scale": (0.15, 0.30), "position": "center", "offset": {"x": 0, "y": 0}},
            {"path": "../assets/img/alphabitSound/15dad-d.png", "sound": "../assets/sounds/alphabitSound/15dad-d.wav", "delay": 10000, "scale": (0.15, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
            # Slide 16 - Taa
    {
        "title": "حرف الطاء",
        "narration": "../assets/sounds/alphabitSound/16-taa-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/16taa.png", "delay": 0, "scale": (0.20, 0.40), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/16taa-f.png", "sound": "../assets/sounds/alphabitSound/16-taa-f.wav", "delay": 3000, "scale": (0.10, 0.30), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/16taa-k.png", "sound": "../assets/sounds/alphabitSound/16-taa-k.wav", "delay": 7000, "scale": (0.10, 0.30), "position": "center", "offset": {"x": 0, "y": 40}},
            {"path": "../assets/img/alphabitSound/16taa-d.png", "sound": "../assets/sounds/alphabitSound/16-taa-d.wav", "delay": 10000, "scale": (0.10, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
#            # Slide 17 - Zaa
    {
        "title": "حرف الظاء",
        "narration": "../assets/sounds/alphabitSound/17zaa-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/17zaa.png", "delay": 0, "scale": (0.20, 0.40), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/17zaa-f.png", "sound": "../assets/sounds/alphabitSound/17zaa-f.wav", "delay": 3000, "scale": (0.10, 0.30), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/17zaa-k.png", "sound": "../assets/sounds/alphabitSound/17zaa-k.wav", "delay": 7000, "scale": (0.10, 0.30), "position": "center", "offset": {"x": 0, "y": 40}},
            {"path": "../assets/img/alphabitSound/17zaa-d.png", "sound": "../assets/sounds/alphabitSound/17zaa-d.wav", "delay": 10000, "scale": (0.10, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
            # Slide 18 - Aen
    {
        "title": "حرف العين",
        "narration": "../assets/sounds/alphabitSound/18aen-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/18aen.png", "delay": 0, "scale": (0.15, 0.50), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/18aen-f.png", "sound": "../assets/sounds/alphabitSound/18aen-f.wav", "delay": 3000, "scale": (0.10, 0.30), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/18aen-k.png", "sound": "../assets/sounds/alphabitSound/18aen-k.wav", "delay": 7000, "scale": (0.10, 0.30), "position": "center", "offset": {"x": 0, "y": 40}},
            {"path": "../assets/img/alphabitSound/18aen-d.png", "sound": "../assets/sounds/alphabitSound/18aen-d.wav", "delay": 10000, "scale": (0.10, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
            # Slide 19 - Gean
    {
        "title": "حرف الغين",
        "narration": "../assets/sounds/alphabitSound/19gean-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/19gean.png", "delay": 0, "scale": (0.15, 0.50), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/19gean-f.png", "sound": "../assets/sounds/alphabitSound/19gean-f.wav", "delay": 3000, "scale": (0.10, 0.30), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/19gean-k.png", "sound": "../assets/sounds/alphabitSound/19gean-k.wav", "delay": 7000, "scale": (0.10, 0.30), "position": "center", "offset": {"x": 0, "y": 20}},
            {"path": "../assets/img/alphabitSound/19gean-d.png", "sound": "../assets/sounds/alphabitSound/19gean-d.wav", "delay": 10000, "scale": (0.10, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
            # Slide 20 - Feh
    {
        "title": "حرف الفاء",
        "narration": "../assets/sounds/alphabitSound/20feh-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/20feh.png", "delay": 0, "scale": (0.20, 0.40), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/20feh-f.png", "sound": "../assets/sounds/alphabitSound/20feh-f.wav", "delay": 3000, "scale": (0.15, 0.30), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/20feh-k.png", "sound": "../assets/sounds/alphabitSound/20feh-k.wav", "delay": 7000, "scale": (0.15, 0.30), "position": "center", "offset": {"x": 0, "y": 40}},
            {"path": "../assets/img/alphabitSound/20feh-d.png", "sound": "../assets/sounds/alphabitSound/20feh-d.wav", "delay": 10000, "scale": (0.15, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
            # Slide 21 - Kf
    {
        "title": "حرف القاف",
        "narration": "../assets/sounds/alphabitSound/21kf-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/21kf.png", "delay": 0, "scale": (0.15, 0.40), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/21kf-f.png", "sound": "../assets/sounds/alphabitSound/21kf-f.wav", "delay": 3000, "scale": (0.15, 0.30), "position": "center-right", "offset": {"x": -150, "y": 40}},
            {"path": "../assets/img/alphabitSound/21kf-k.png", "sound": "../assets/sounds/alphabitSound/21kf-k.wav", "delay": 7000, "scale": (0.15, 0.30), "position": "center", "offset": {"x": 0, "y": 40}},
            {"path": "../assets/img/alphabitSound/21kf-d.png", "sound": "../assets/sounds/alphabitSound/21kf-d.wav", "delay": 10000, "scale": (0.15, 0.30), "position": "center-left", "offset": {"x": 150, "y": 20}}
        ]
    },
            # Slide 22 - Kaf
    {
        "title": "حرف الكاف",
        "narration": "../assets/sounds/alphabitSound/22kaf-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/22kaf.png", "delay": 0, "scale": (0.15, 0.40), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/22kaf-f.png", "sound": "../assets/sounds/alphabitSound/22kaf-f.wav", "delay": 3000, "scale": (0.15, 0.30), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/22kaf-k.png", "sound": "../assets/sounds/alphabitSound/22kaf-k.wav", "delay": 7000, "scale": (0.15, 0.30), "position": "center", "offset": {"x": 0, "y": 40}},
            {"path": "../assets/img/alphabitSound/22kaf-d.png", "sound": "../assets/sounds/alphabitSound/22kaf-d.wav", "delay": 10000, "scale": (0.15, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
            # Slide 23 - Lam
    {
        "title": "حرف اللام",
        "narration": "../assets/sounds/alphabitSound/23lam-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/23lam.png", "delay": 0, "scale": (0.15, 0.45), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/23lam-f.png", "sound": "../assets/sounds/alphabitSound/23lam-f.wav", "delay": 3000, "scale": (0.10, 0.30), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/23lam-k.png", "sound": "../assets/sounds/alphabitSound/23lam-k.wav", "delay": 7000, "scale": (0.10, 0.30), "position": "center", "offset": {"x": 0, "y": 40}},
            {"path": "../assets/img/alphabitSound/23lam-d.png", "sound": "../assets/sounds/alphabitSound/23lam-d.wav", "delay": 10000, "scale": (0.10, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
            # Slide 24 - Meam
    {
        "title": "حرف الميم",
        "narration": "../assets/sounds/alphabitSound/24meam-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/24meam.png", "delay": 0, "scale": (0.10, 0.40), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/24meam-f.png", "sound": "../assets/sounds/alphabitSound/24meam-f.wav", "delay": 3000, "scale": (0.10, 0.30), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/24meam-k.png", "sound": "../assets/sounds/alphabitSound/24meam-k.wav", "delay": 7000, "scale": (0.10, 0.30), "position": "center", "offset": {"x": 0, "y": 40}},
            {"path": "../assets/img/alphabitSound/24meam-d.png", "sound": "../assets/sounds/alphabitSound/24meam-d.wav", "delay": 10000, "scale": (0.10, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
            # Slide 25 - Noon
    {
        "title": "حرف النون",
        "narration": "../assets/sounds/alphabitSound/25noon-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/25noon.png", "delay": 0, "scale": (0.15, 0.40), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/25noon-f.png", "sound": "../assets/sounds/alphabitSound/25noon-f.wav", "delay": 3000, "scale": (0.10, 0.30), "position": "center-right", "offset": {"x": -150, "y": 20}},
            {"path": "../assets/img/alphabitSound/25noon-k.png", "sound": "../assets/sounds/alphabitSound/25noon-k.wav", "delay": 7000, "scale": (0.10, 0.30), "position": "center", "offset": {"x": 0, "y": 40}},
            {"path": "../assets/img/alphabitSound/25noon-d.png", "sound": "../assets/sounds/alphabitSound/25noon-d.wav", "delay": 10000, "scale": (0.10, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
            # Slide 26 - Heh
    {
        "title": "حرف الهاء",
        "narration": "../assets/sounds/alphabitSound/26heh-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/26heh.png", "delay": 0, "scale": (0.15, 0.40), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/26heh-f.png", "sound": "../assets/sounds/alphabitSound/26heh-f.wav", "delay": 3000, "scale": (0.10, 0.30), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/26heh-k.png", "sound": "../assets/sounds/alphabitSound/26heh-k.wav", "delay": 7000, "scale": (0.10, 0.30), "position": "center", "offset": {"x": 0, "y": 40}},
            {"path": "../assets/img/alphabitSound/26heh-d.png", "sound": "../assets/sounds/alphabitSound/26heh-d.wav", "delay": 10000, "scale": (0.10, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
                # Slide 27 - Waw
    {
        "title": "حرف الواو",
        "narration": "../assets/sounds/alphabitSound/27waw-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/27waw.png", "delay": 0, "scale": (0.15, 0.35), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/27waw-f.png", "sound": "../assets/sounds/alphabitSound/27waw-f.wav", "delay": 3000, "scale": (0.10, 0.30), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/27waw-k.png", "sound": "../assets/sounds/alphabitSound/27waw-k.wav", "delay": 7000, "scale": (0.10, 0.30), "position": "center", "offset": {"x": 0, "y": 40}},
            {"path": "../assets/img/alphabitSound/27waw-d.png", "sound": "../assets/sounds/alphabitSound/27waw-d.wav", "delay": 10000, "scale": (0.10, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
                # Slide 28 - Yaa
    {
        "title": "حرف الياء",
        "narration": "../assets/sounds/alphabitSound/28yaa-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/28yaa.png", "delay": 0, "scale": (0.20, 0.40), "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/28yaa-f.png", "sound": "../assets/sounds/alphabitSound/28yaa-f.wav", "delay": 3000, "scale": (0.10, 0.30), "position": "center-right", "offset": {"x": -150, "y": 0}},
            {"path": "../assets/img/alphabitSound/28yaa-k.png", "sound": "../assets/sounds/alphabitSound/28yaa-k.wav", "delay": 7000, "scale": (0.10, 0.30), "position": "center", "offset": {"x": 0, "y": 40}},
            {"path": "../assets/img/alphabitSound/28yaa-d.png", "sound": "../assets/sounds/alphabitSound/28yaa-d.wav", "delay": 10000, "scale": (0.10, 0.30), "position": "center-left", "offset": {"x": 150, "y": 0}}
        ]
    },
                # End Slid
    {
        "title": "أحسنت",
        "narration": "../assets/sounds/alphabitSound/theend.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/k2.png", "delay": 0, "scale": (0.30, 0.40), "position": "center"}
        ]
    },
    
]

class AlphabitSoundApp:
    def __init__(self, root, main_app=None):  # add main_app
        self.root = root
        self.main_app = main_app  # store reference to QuizApp
        self.root.title("Alphabit Sound App")
        self.root.attributes('-fullscreen', True)
        self.slide_index = 0
        self.image_labels = []
        self.photos = []   # 🔒 keep references to PhotoImage
        self.scheduled_tasks = []  # ✅ store after() task IDs
        self.root.configure(bg="white")

        root.bind("<Escape>", self.on_escape)
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Title
        self.title_label = tk.Label(root, text="", font=("Scheherazade", 60, "bold"), bg="#ffffff", bd=0, relief="flat")
        self.title_label.pack(pady=.05)
        self.title_label.pack(padx=0.05)

        # Image container (center)
        self.image_frame = tk.Frame(root, bg="#ffffff", height=400)
        self.image_frame.pack(fill="both", expand=True, pady=0)

        # Navigation (bottom bar)
        self.nav_frame = tk.Frame(root, bg="#ffffff", height=100)
        self.nav_frame.pack(side="bottom", fill="x")

        self.load_slide()

    def on_close(self):
        """Stop all sounds and quit the mixer before closing window."""
        self.stop_sounds()         # stop music and channels
        pygame.mixer.quit()        # fully shutdown Pygame mixer
        self.root.destroy()        # close the Tk window


    def on_escape(self, event=None):
        """Handle Escape key: stop sounds and exit fullscreen."""
        self.clear_scheduled_tasks()  # cancel all pending after() calls
        self.stop_sounds()            # stop all currently playing sounds
        self.root.attributes('-fullscreen', False)
        

    def load_slide(self):
        self.clear_scheduled_tasks()
        self.clear_images()
        
        slide = slides[self.slide_index]
        self.title_label.config(text=slide["title"])
        print("Slide title:", slide["title"])

        # Play narration
        try:
            narration = pygame.mixer.Sound(slide["narration"])
            pygame.mixer.Channel(0).play(narration)
        except Exception as e:
            print("Narration error:", e)

        # Schedule images with delay
        for img_data in slide["images"]:
            delay = img_data.get("delay", 0)
            task_id = self.root.after(delay, self.make_image_callback(img_data))
            self.scheduled_tasks.append(task_id)

        self.update_navigation_buttons()

        # Remove image
    def remove_image(self, label):
        if label in self.image_labels:
            label.destroy()
            self.image_labels.remove(label)


        #Stop sound when moving to next slid
    def stop_sounds(self):
        try:
            pygame.mixer.stop()  # stops all sounds on all channels
        except Exception as e:
            print("Stop sound error:", e)


    def make_image_callback(self, img_data):
        def callback():
            # Only show if we’re still on the same slide
            if img_data in slides[self.slide_index]["images"]:
                self.show_image(img_data)
        return callback


    def clear_scheduled_tasks(self):
        for task_id in self.scheduled_tasks:
            try:
                self.root.after_cancel(task_id)
            except Exception:
                pass
        self.scheduled_tasks.clear()

    def back_to_main(self):
        """Stop all sounds, cancel tasks, and return to main menu."""
        self.stop_sounds()
        self.clear_scheduled_tasks()

        # Clear all widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Go back to main menu if main_app provided
        if self.main_app:
            print("🔙 Returning to Main Menu")
            self.main_app.show_section_screen()
        else:
            print("⚠ No main_app reference provided, exiting.")
            self.root.destroy()


    def show_image(self, img_data):
        abs_path = os.path.abspath(img_data["path"])
        if not os.path.exists(abs_path):
            print("❌ Image not found:", abs_path)
            fallback = tk.Label(self.image_frame, text="Image failed", bg="white", font=("Arial", 12))
            fallback.place(relx=0.5, rely=0.5, anchor="center")
            return

        try:
            # Screen size
            screen_w = self.root.winfo_screenwidth()
            screen_h = self.root.winfo_screenheight()

            # Use scale if provided
            scale = img_data.get("scale", (0.2, 0.3))
            img_w = int(screen_w * scale[0])
            img_h = int(screen_h * scale[1])

            img = Image.open(abs_path).resize((img_w, img_h))
            photo = ImageTk.PhotoImage(img)

            label = tk.Label(self.image_frame, image=photo, bg=self.image_frame["bg"], bd=0)
            label.image = photo
            self.photos.append(photo)

            # --- Offset values (default 0,0) ---
            offset = img_data.get("offset", {})
            offset_x = offset.get("x", 0)
            offset_y = offset.get("y", 0)

            # --- Positioning ---
            if "x" in img_data and "y" in img_data:
                # Absolute placement
                label.place(x=img_data["x"] + offset_x, y=img_data["y"] + offset_y)
            else:
                # Keyword placement
                position_map = {
                    "center":       (0.5, 0.5, "center"),
                    "top":          (0.5, 0.0, "n"),
                    "bottom":       (0.5, 1.0, "s"),
                    "left":         (0.15, 0.5, "w"),
                    "right":        (0.85, 0.5, "e"),
                    "top-left":     (0.0, 0.0, "nw"),
                    "top-right":    (1.0, 0.0, "ne"),
                    "bottom-left":  (0.0, 1.0, "sw"),
                    "bottom-right": (1.0, 1.0, "se"),
                    "center-right": (0.9, 0.5, "e"),
                    "center-left":  (0.1, 0.5, "w"),
                }
                relx, rely, anchor = position_map.get(img_data.get("position", "center"))
                label.place(relx=relx, rely=rely, anchor=anchor, x=offset_x, y=offset_y)

            self.image_labels.append(label)

            # --- Play sound if defined ---
            sound_path = img_data.get("sound")
            if sound_path and os.path.exists(sound_path):
                try:
                    sound = pygame.mixer.Sound(sound_path)
                    pygame.mixer.Channel(1).play(sound)
                except Exception as e:
                    print("Sound play error:", e)

            # Auto-remove after duration if given
            duration = img_data.get("duration")
            if duration:
                task_id = self.root.after(duration, lambda: self.remove_image(label))
                self.scheduled_tasks.append(task_id)

        except Exception as e:
            print("❌ Image error:", e)
            fallback = tk.Label(self.image_frame, text="Image failed", bg="#ffffff", font=("Scheherazade", 12))
            fallback.place(relx=0.5, rely=0.5, anchor="center")




    def play_hover_sound(self, path):
        try:
            sound = pygame.mixer.Sound(path)
            pygame.mixer.Channel(1).play(sound)
        except Exception as e:
            print("Hover sound error:", e)

    def clear_images(self):
        for lbl in self.image_labels:
            lbl.destroy()
        self.image_labels.clear()
        self.stop_sounds()   # ✅ stop audio when slide cleared

    def next_slide(self):
        if self.slide_index < len(slides) - 1:
            self.stop_sounds()   # ✅ stop old sounds
            self.slide_index += 1
            self.load_slide()

    def prev_slide(self):
        if self.slide_index > 0:
            self.stop_sounds()   # ✅ stop old sounds
            self.slide_index -= 1
            self.load_slide()

    def update_navigation_buttons(self):
        for widget in self.nav_frame.winfo_children():
            widget.destroy()

        # Previous button
        if self.slide_index > 0:
            prev_btn = tk.Button(
                self.nav_frame, text="السابق ⏭", font=("Scheherazade", 25, "bold"),
                command=self.prev_slide, bg="#ddddff"
            )
            prev_btn.place(relx=0.95, rely=0.5, anchor="center")

        # ✅ Back button always visible
        back_btn = tk.Button(
            self.nav_frame, text="⬅ العودة", font=("Scheherazade", 25, "bold"),
            command=self.back_to_main, bg="#ffcccc"
        )
        back_btn.place(relx=0.5, rely=0.5, anchor="center")

        # Next or Exit button
        if self.slide_index < len(slides) - 1:
            next_btn = tk.Button(
                self.nav_frame, text="⏮ التالي", font=("Scheherazade", 25, "bold"),
                command=self.next_slide, bg="#ccffcc"
            )
            next_btn.place(relx=0.05, rely=0.5, anchor="center")
        else:
            exit_btn = tk.Button(
                self.nav_frame, text="الخروج x", font=("Scheherazade", 25, "bold"),
                command=self.root.destroy, bg="#ffcccc"
            )
            exit_btn.place(relx=0.05, rely=0.5, anchor="center")


def run_alphabit_sound(root=None, main_app=None):
    if root is None:
        root = tk.Tk()
        app = AlphabitSoundApp(root, main_app)
        root.mainloop()
    else:
        for widget in root.winfo_children():
            widget.destroy()
        app = AlphabitSoundApp(root, main_app)


if __name__ == "__main__":
    run_alphabit_sound()
