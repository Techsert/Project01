# learn_lvl2_T4.py

import pygame
import config
from video_slide_base import NavigableVideoSlidePlayer
from profile_system import mark_learning_topic_complete


# ==========================================================
# SLIDE DATA
# ==========================================================
SLIDES_T4 = [
    # Intro slide
    {
        "title": "DAM-MAH",
        "narration": "../assets/sounds/learn_lvl2/learn_lvl2_T4.wav",
        "images": [
            # BASE
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/Learn_lvl1_T3/intro09.png", "scale": (0.3, 0.6)},
            
            # SEC 02
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 7000, "scale": (0.05, 0.11), "offset": {"x": -750, "y": 0}},

            {"path": "../assets/img/learn_lvl2/10ra.png", "delay": 9000, "scale": (0.05, 0.18), "offset": {"x": 1000, "y": 0}, "duration": 11500},
            {"path": "../assets/img/learn_lvl2/11zay01.png", "delay": 9000, "scale": (0.05, 0.18), "offset": {"x": 830, "y": 0}, "duration": 11500},
            {"path": "../assets/img/learn_lvl2/21kf.PNG", "delay": 9000, "scale": (0.1, 0.16), "offset": {"x": 600, "y": 0}, "duration": 11500},

            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 9000, "scale": (0.02, 0.05), "offset": {"x": 1050, "y": -170}, "duration": 11500, "flash_count": 3, "flash_speed": 400},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 9000, "scale": (0.02, 0.05), "offset": {"x": 855, "y": -170}, "duration": 11500, "flash_count": 3, "flash_speed": 400},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 9000, "scale": (0.02, 0.05), "offset": {"x": 600, "y": -170}, "duration": 11500, "flash_count": 3, "flash_speed": 400},

            {"path": "../assets/img/alphabitSound/Letters/02ba02.png", "delay": 21000, "scale": (0.09, 0.15), "offset": {"x": 1100, "y": -160}, "duration": None},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 21000, "scale": (0.02, 0.05), "offset": {"x": 1050, "y": -310}, "flash_count": 4, "flash_speed": 400, "duration": None},

            {"path": "../assets/img/alphabitSound/Letters/04tha.PNG", "delay": 30000, "scale": (0.09, 0.15), "offset": {"x": 1100, "y": 200}},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 30000, "scale": (0.02, 0.05), "offset": {"x": 1050, "y": 60}, "flash_count": 4, "flash_speed": 400},       
            
        ],
        "texts": [
            # SEC 01
            {
                "text": "DAM-MAH",
                "delay": 3600,
                "position": "center",
                "offset": {"x": -700, "y": -200},
                "size_ratio": 0.13,
                "color": (0, 100, 200),
                "bold": True,
                "flash_count": 0,
                "flash_speed": 0,
                "duration": None
            },
            # SEC 03
            {
                "text": "'O'",
                "delay": 14000,
                "position": "center",
                "offset": {"x": -750, "y": 300},
                "size_ratio": 0.19,
                "color": (0, 100, 200),
                "bold": True,
                "flash_count": 0,
                "flash_speed": 0,
                "duration": None
            },
            {
                "text": "BO",
                "delay": 25000,
                "position": "center",
                "offset": {"x": 600, "y": -190},
                "size_ratio": 0.19,
                "color": (236, 28, 36),
                "bold": False,
                "flash_count": 0,
                "flash_speed": 0,
                "duration": None
            },
            {
                "text": "THO",
                "delay": 32000,
                "position": "center",
                "offset": {"x": 600, "y": 250},
                "size_ratio": 0.19,
                "color": (236, 28, 36),
                "bold": False,
                "flash_count": 0,
                "flash_speed": 0,
                "duration": None
            },
            
        ]  
    },
    # Slide 1 - Alef
    {
        "title": "أ",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/01alef.PNG", "scale": (0.04, 0.4),
             "sound": "../assets/sounds/Learn_lvl2/01Alef-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1500, "scale": (0.05, 0.05), "offset": {"x": 0, "y": -325},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7500},
        ]
    },
    # Slide 2 - Ba
    {
       "title": "ب",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/02ba02.png", "scale": (0.20, 0.22), "offset": {"x": 0, "y": 90},
             "sound": "../assets/sounds/Learn_lvl2/02Baa-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1000, "scale": (0.07, 0.07), "offset": {"x": -100, "y": -175},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
    # Slide 3 Ta
    {
        "title": "ت",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/03ta.png", "scale": (0.20, 0.20), "offset": {"x": 0, "y": -15},
             "sound": "../assets/sounds/Learn_lvl2/03Ta-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1100, "scale": (0.07, 0.07), "offset": {"x": -100, "y": -275},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
        # Slide 4 - Tha
    {
        "title": "ث",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/04tha.png", "scale": (0.20, 0.24), "offset": {"x": 0, "y": -45},
             "sound": "../assets/sounds/Learn_lvl2/04Tha-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1100, "scale": (0.07, 0.07), "offset": {"x": -100, "y": -275},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
            # Slide 5 - Gem
    {
        "title": "ج",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/05geem.png", "scale": (0.15, 0.35), "offset": {"x": 0, "y": 100},
             "sound": "../assets/sounds/Learn_lvl2/05-Geam-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1100, "scale": (0.07, 0.07), "offset": {"x": -100, "y": -240},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
            # Slide 6 - 7a
    {
        "title": "حرف الحاء",
        "narration": "ح",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/06ha.png", "scale": (0.15, 0.35), "offset": {"x": 0, "y": 100},
             "sound": "../assets/sounds/Learn_lvl2/06-7a-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1000, "scale": (0.07, 0.07), "offset": {"x": -100, "y": -240},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
            # Slide 7 - 7'a
    {
        "title": "خ",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/07ka.png", "scale": (0.15, 0.46), "offset": {"x": 0, "y": 22},
             "sound": "../assets/sounds/Learn_lvl2/077'a-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1000, "scale": (0.07, 0.07), "offset": {"x": -100, "y": -340},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
            # Slide 8 - Dal
    {
        "title": "د",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/08dal.png", "scale": (0.08, 0.20), "offset": {"x": 0, "y": -12},
             "sound": "../assets/sounds/Learn_lvl2/08Dal-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1000, "scale": (0.06, 0.06), "offset": {"x": -50, "y": -230},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
            # Slide 9 - Thal
    {
        "title": "ذ",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/09thal01.png", "scale": (0.08, 0.30), "offset": {"x": 0, "y": -85},
             "sound": "../assets/sounds/Learn_lvl2/09Thal-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1000, "scale": (0.06, 0.06), "offset": {"x": -100, "y": -320},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
            # Slide 10 - Ra
    {
        "title": "ر",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/10ra.png", "scale": (0.08, 0.25), "offset": {"x": 0, "y": 75},
             "sound": "../assets/sounds/Learn_lvl2/10Ra-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1000, "scale": (0.06, 0.06), "offset": {"x": 25, "y": -150},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
            # Slide 11 - Zay
    {
        "title": "ز",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/11zay.png", "scale": (0.08, 0.35), "offset": {"x": 0, "y": 3},
             "sound": "../assets/sounds/Learn_lvl2/11Zay-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1200, "scale": (0.06, 0.06), "offset": {"x": 0, "y": -280},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
            # Slide 12 - Sen
    {
        "title": "س",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/12sen.png", "scale": (0.18, 0.20), "offset": {"x": 0, "y": 110},
             "sound": "../assets/sounds/Learn_lvl2/12Seen-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1000, "scale": (0.07, 0.07), "offset": {"x": -100, "y": -150},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
            # Slide 13 - Shen
    {
        "title": "ش",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/13shen.png", "scale": (0.18, 0.32), "offset": {"x": 0, "y": 25},
             "sound": "../assets/sounds/Learn_lvl2/13Sheen-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1200, "scale": (0.07, 0.07), "offset": {"x": -100, "y": -150},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
            # Slide 14 - Sad
    {
        "title": "ص",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/14sad.png", "scale": (0.18, 0.20), "offset": {"x": 0, "y": 110},
             "sound": "../assets/sounds/Learn_lvl2/14Sad-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1200, "scale": (0.07, 0.07), "offset": {"x": -100, "y": -150},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
            # Slide 15 - Dad
    {
        "title": "ض",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/15dad01.png", "scale": (0.18, 0.27), "offset": {"x": 0, "y": 58},
             "sound": "../assets/sounds/Learn_lvl2/15Dad-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1200, "scale": (0.07, 0.07), "offset": {"x": -100, "y": -150},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
            # Slide 16 - Taa
    {
        "title": "ط",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/16taa.png", "scale": (0.13, 0.27), "offset": {"x": 0, "y": -68},
             "sound": "../assets/sounds/Learn_lvl2/16Taa-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1000, "scale": (0.06, 0.06), "offset": {"x": -50, "y": -310},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
            # Slide 17 - Zaa
    {
        "title": "ظ",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/17zaa.png", "scale": (0.13, 0.27), "offset": {"x": 0, "y": -68},
             "sound": "../assets/sounds/Learn_lvl2/17Thaa-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1200, "scale": (0.06, 0.06), "offset": {"x": -50, "y": -310},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
            # Slide 18 - Aen
    {
        "title": "ع",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/18aen.png", "scale": (0.10, 0.275), "offset": {"x": 0, "y": 53},
             "sound": "../assets/sounds/Learn_lvl2/18Ayn-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1000, "scale": (0.06, 0.06), "offset": {"x": -50, "y": -225},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
            # Slide 19 - Gaen
    {
        "title": "غ",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/19gean.png", "scale": (0.10, 0.35),
             "sound": "../assets/sounds/Learn_lvl2/19Gean-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1200, "scale": (0.06, 0.06), "offset": {"x": -50, "y": -325},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
            # Slide 20 - Feh
    {
        "title": "ف",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/20feh.png", "scale": (0.18, 0.22), "offset": {"x": 0, "y": -30},
             "sound": "../assets/sounds/Learn_lvl2/20Faa-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1100, "scale": (0.07, 0.07), "offset": {"x": -50, "y": -200},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700},
        ]
    },
            # Slide 21 - Kf
    {
        "title": "ق",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/21kf.png", "scale": (0.13, 0.28),
             "sound": "../assets/sounds/Learn_lvl2/21Qaf-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1200, "scale": (0.07, 0.07), "offset": {"x": -50, "y": -225},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700}
        ]
    },
            # Slide 22 - Kaf
    {
        "title": "ك",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},            
            {"path": "../assets/img/alphabitSound/Letters/22kaf.png", "scale": (0.13, 0.35),
             "sound": "../assets/sounds/Learn_lvl2/22Kaf-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1200, "scale": (0.07, 0.07), "offset": {"x": -25, "y": -250},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700}
        ]
    },
            # Slide 23 - Lam
    {
        "title": "ل",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/23lam01.png", "scale": (0.08, 0.39), "offset": {"x": 0, "y": 25},
             "sound": "../assets/sounds/Learn_lvl2/23Lam-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1200, "scale": (0.06, 0.06), "offset": {"x": -25, "y": -275},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700}
        ]
    },
            # Slide 24 - Meam
    {
        "title": "م",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/24meam.png", "scale": (0.08, 0.30),
             "sound": "../assets/sounds/Learn_lvl2/24Meam-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1000, "scale": (0.06, 0.06), "offset": {"x": -25, "y": -275},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700}
            
        ]
    },
            # Slide 25 - Noon
    {
        "title": "ن",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/25noon.png", "scale": (0.15, 0.25),
             "sound": "../assets/sounds/Learn_lvl2/25Noon-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1000, "scale": (0.06, 0.06), "offset": {"x": -25, "y": -275},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700}
        ]
    },
            # Slide 26 - Heh
    {
        "title": "هـ",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/26heh.png", "scale": (0.13, 0.20), "offset": {"x": 0, "y": -10},
             "sound": "../assets/sounds/Learn_lvl2/26Haa-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1200, "scale": (0.06, 0.06), "offset": {"x": -25, "y": -250},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700}
        ]
    },
                # Slide 27 - Waw
    {
        "title": "و",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/27waw.png", "scale": (0.08, 0.25), "offset": {"x": 0, "y": 75},
             "sound": "../assets/sounds/Learn_lvl2/27Waw-F.wav.", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1200, "scale": (0.06, 0.06), "offset": {"x": -25, "y": -150},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700}
        ]
    },
                # Slide 28 - Yaa
    {
        "title": "ي",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/grid01.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/Letters/28yaa.png", "scale": (0.15, 0.21), "offset": {"x": 0, "y": 40},
             "sound": "../assets/sounds/Learn_lvl2/28Yaa-F.wav", "sound_repeat": 3,  "sound_interval": 10000},
            {"path": "../assets/img/learn_lvl2/dama-R.png", "delay": 1000, "scale": (0.06, 0.06), "offset": {"x": -25, "y": -175},
             "flash_count": 2, "flash_speed": 400, "flash_repeat": 3, "flash_cycle_interval": 7700}
        ]
    },
                # End Slid
    {
        "title": "Well Done",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-tr.png", "scale": (0.95, 0.80)},
            {"path": "../assets/img/alphabitSound/coach.png", "scale": (0.20, 0.40),
             "sound": "../assets/sounds/alphabitSound/welldone01.wav",}
        ]
    },
]
# ==========================================================
# RUN FUNCTION
# ==========================================================
def run_learn_lvl2_T4(screen, main_app):
    """Launch Topic 4."""
    player = NavigableVideoSlidePlayer(
        screen=screen,
        main_app=main_app,
        slides=SLIDES_T4,
        level=2,
        has_navigation=True
    )
    player.topic = "T4"  # ✅ SET TOPIC IDENTIFIER
    player.run()# profile_system.py - FIXED WITH CORRECT UNLOCKING LOGIC

    # ✅ Mark completion after player exits
    profile_name = main_app.selected_profile.get("name") if main_app.selected_profile else None
    if profile_name:
        mark_learning_topic_complete(profile_name, 2, "T4")
        print(f"✅ Completed Learning Level 2 - Topic T4")
