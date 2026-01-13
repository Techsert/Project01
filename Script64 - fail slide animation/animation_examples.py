# animation_examples.py - Examples of using animations in slides
# Copy these patterns to your learn_lvl*.py files

# ==========================================================
# EXAMPLE 1: FADE ANIMATION (DEFAULT)
# ==========================================================
FADE_EXAMPLE = {
    "title": "Fade In Animation",
    "narration": "../assets/sounds/example.wav",
    "images": [
        {
            "path": "../assets/img/alphabitSound/bg-tr.png",
            "delay": 0,
            "scale": (0.95, 0.80),
            "position": "center",
            "animation": "fade"  # ✅ Smooth fade in
        },
        {
            "path": "../assets/img/alphabitSound/Letters/01alef.png",
            "sound": "../assets/sounds/alphabitSound/01alef.wav",
            "delay": 1000,  # Appears after 1 second
            "scale": (0.04, 0.40),
            "position": "center",
            "animation": "fade"
        }
    ]
}

# ==========================================================
# EXAMPLE 2: SCALE/ZOOM ANIMATION WITH BOUNCE
# ==========================================================
SCALE_BOUNCE_EXAMPLE = {
    "title": "Scale Animation with Bounce",
    "narration": "../assets/sounds/example.wav",
    "images": [
        {
            "path": "../assets/img/alphabitSound/bg-tr.png",
            "delay": 0,
            "scale": (0.95, 0.80),
            "position": "center"
        },
        {
            "path": "../assets/img/alphabitSound/Letters/02ba.png",
            "sound": "../assets/sounds/alphabitSound/02ba.wav",
            "delay": 500,
            "scale": (0.20, 0.30),
            "position": "center",
            "animation": "scale"  # ✅ Zooms in from 0 to full size with bounce
        }
    ]
}

# ==========================================================
# EXAMPLE 3: ELASTIC BOUNCE ANIMATION
# ==========================================================
ELASTIC_BOUNCE_EXAMPLE = {
    "title": "Elastic Bounce Animation",
    "narration": "../assets/sounds/example.wav",
    "images": [
        {
            "path": "../assets/img/alphabitSound/bg-tr.png",
            "delay": 0,
            "scale": (0.95, 0.80),
            "position": "center"
        },
        {
            "path": "../assets/img/alphabitSound/Letters/03ta.png",
            "sound": "../assets/sounds/alphabitSound/03ta.wav",
            "delay": 800,
            "scale": (0.20, 0.35),
            "position": "center",
            "animation": "bounce"  # ✅ Spring-like elastic bounce effect
        }
    ]
}

# ==========================================================
# EXAMPLE 4: MULTIPLE IMAGES WITH STAGGERED ANIMATIONS
# ==========================================================
STAGGERED_ANIMATIONS = {
    "title": "Multiple Letters Appearing",
    "narration": "../assets/sounds/example.wav",
    "images": [
        {
            "path": "../assets/img/alphabitSound/bg-tr.png",
            "delay": 0,
            "scale": (0.95, 0.80),
            "position": "center"
        },
        # ✅ First letter: bounces in at 500ms
        {
            "path": "../assets/img/alphabitSound/Letters/01alef.png",
            "sound": "../assets/sounds/alphabitSound/01alef.wav",
            "delay": 500,
            "scale": (0.02, 0.15),
            "position": "right",
            "offset": {"x": -400, "y": -265},
            "animation": "bounce"
        },
        # ✅ Second letter: scales in at 1000ms
        {
            "path": "../assets/img/alphabitSound/Letters/02ba.png",
            "delay": 1000,
            "scale": (0.07, 0.07),
            "position": "right",
            "offset": {"x": -520, "y": -170},
            "animation": "scale"
        },
        # ✅ Third letter: fades in at 1500ms
        {
            "path": "../assets/img/alphabitSound/Letters/03ta.PNG",
            "delay": 1500,
            "scale": (0.07, 0.07),
            "position": "center",
            "offset": {"x": 775, "y": -205},
            "animation": "fade"
        }
    ]
}

# ==========================================================
# EXAMPLE 5: IMAGES WITH DURATION (FADE OUT)
# ==========================================================
FADE_OUT_EXAMPLE = {
    "title": "Temporary Message",
    "narration": "../assets/sounds/example.wav",
    "images": [
        {
            "path": "../assets/img/alphabitSound/bg-tr.png",
            "delay": 0,
            "scale": (0.95, 0.80),
            "position": "center"
        },
        # ✅ This image appears at 1s, stays for 3s, then fades out
        {
            "path": "../assets/img/main/Strongest01.png",
            "delay": 1000,
            "duration": 3000,  # Visible for 3 seconds
            "scale": (0.4, 0.3),
            "position": "center",
            "animation": "scale"
        },
        # ✅ Next image appears after first one fades
        {
            "path": "../assets/img/main/Qurann.png",
            "delay": 5000,  # Appears after previous fades (1s + 3s + 1s fade)
            "duration": 3000,
            "scale": (0.3, 0.5),
            "position": "center",
            "animation": "bounce"
        }
    ]
}

# ==========================================================
# EXAMPLE 6: UPDATED learn_lvl1_T3.py WITH ANIMATIONS
# ==========================================================
# This shows how to update your existing slides with animations

UPDATED_SLIDES_T3 = [
    # Slide 1 - Revision with staggered letter animations
    {
        "title": "Revision",
        "narration": "../assets/sounds/Learn_lvl1_T3/Learn_lvl1_T3-1.wav",
        "images": [
            {
                "path": "../assets/img/alphabitSound/bg-ft.png",
                "delay": 0,
                "scale": (0.95, 0.80),
                "position": "center"
            },
            {
                "path": "../assets/img/Learn_lvl1_T3/intro01.png",
                "delay": 0,
                "scale": (0.1, 0.4),
                "position": "left",
                "offset": {"x": 250, "y": 50},
                "animation": "fade"
            },
            # ✅ Messages with fade in/out
            {
                "path": "../assets/img/main/Strongest01.png",
                "delay": 7500,
                "scale": (0.4, 0.3),
                "position": "center",
                "offset": {"x": 0, "y": 0},
                "duration": 4000,
                "animation": "scale"  # Zooms in
            },
            {
                "path": "../assets/img/main/Qurann.png",
                "delay": 14000,
                "scale": (0.3, 0.5),
                "position": "center",
                "offset": {"x": 0, "y": 0},
                "duration": 4000,
                "animation": "bounce"  # Bounces in
            },
            {
                "path": "../assets/img/main/28letters.png",
                "delay": 19000,
                "scale": (0.3, 0.2),
                "position": "center",
                "offset": {"x": 0, "y": 0},
                "duration": 3000,
                "animation": "scale"
            },
            {
                "path": "../assets/img/main/arrows.png",
                "delay": 22500,
                "scale": (0.3, 0.5),
                "position": "center",
                "offset": {"x": 700, "y": 0},
                "duration": 4000,
                "animation": "fade"
            },
            
            # ✅ Second part with character
            {
                "path": "../assets/img/Learn_lvl1_T3/intro01.png",
                "delay": 30000,
                "scale": (0.1, 0.4),
                "position": "left",
                "offset": {"x": 250, "y": 50},
                "sound": "../assets/sounds/Learn_lvl1_T3/Learn_lvl1_T3-2.wav",
                "animation": "fade"
            },

            # ✅ Letters appearing with bounce animation (staggered by 500ms each)
            {
                "path": "../assets/img/alphabitSound/Letters/01alef.png",
                "delay": 39500,
                "scale": (0.02, 0.15),
                "position": "right",
                "offset": {"x": -400, "y": -265},
                "animation": "bounce"
            },
            {
                "path": "../assets/img/alphabitSound/Letters/02ba.png",
                "delay": 40000,
                "scale": (0.07, 0.07),
                "position": "right",
                "offset": {"x": -520, "y": -170},
                "animation": "bounce"
            },
            {
                "path": "../assets/img/alphabitSound/Letters/03ta.PNG",
                "delay": 40600,
                "scale": (0.07, 0.07),
                "position": "center",
                "offset": {"x": 775, "y": -205},
                "animation": "bounce"
            },
            {
                "path": "../assets/img/alphabitSound/Letters/04tha.PNG",
                "delay": 41000,
                "scale": (0.07, 0.07),
                "position": "center",
                "offset": {"x": 450, "y": -205},
                "animation": "bounce"
            },
            # ... continue for all 28 letters with bounce animation
        ]
    }
]

# ==========================================================
# CHOOSING TRANSITION TYPES
# ==========================================================
# You can change transition type by modifying the NavigableVideoSlidePlayer class:
# In navigate_to_next_slide() or navigate_to_prev_slide(), change:
#
# self.transition_type = "slide"   # ✅ Slide left/right (default)
# self.transition_type = "fade"    # ✅ Crossfade between slides
# self.transition_type = "zoom"    # ✅ Zoom out old, zoom in new
#
# Example usage in your learning module:

def custom_transition_example(screen, main_app):
    """Example with custom transition type"""
    from video_slide_base import NavigableVideoSlidePlayer
    
    player = NavigableVideoSlidePlayer(
        screen=screen,
        main_app=main_app,
        slides=UPDATED_SLIDES_T3,
        level=1,
        has_navigation=True
    )
    
    # ✅ Override transition type before running
    player.transition_type = "fade"  # or "zoom" or "slide"
    
    player.topic = "T3"
    player.run()

# ==========================================================
# ANIMATION TIMING TIPS
# ==========================================================
"""
TIMING GUIDELINES:
1. Fade animations: Best for subtle appearances (300ms duration)
2. Scale animations: Good for emphasis (400ms duration with bounce)
3. Bounce animations: Great for playful, energetic content
4. Staggered delays: Space images 300-600ms apart for smooth flow
5. Duration: Use for temporary messages (3-5 seconds typically)

DELAY PATTERNS:
- Immediate (0ms): Background images
- Quick (300-500ms): First foreground element
- Staggered (600-1000ms intervals): Sequential elements
- Delayed (2000ms+): After narration or previous animation

TRANSITION TYPES:
- "slide": Best for sequential learning content
- "fade": Best for smooth, professional transitions
- "zoom": Best for emphasis or topic changes
"""

# ==========================================================
# PERFORMANCE TIPS
# ==========================================================
"""
OPTIMIZATION:
1. Don't use too many simultaneous animations (max 3-4 at once)
2. Large images with scale animation may impact performance
3. Keep transition duration under 1 second for responsiveness
4. Use fade for complex slides with many elements
5. Cache frequently used images to reduce loading
"""
