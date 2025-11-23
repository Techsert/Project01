# learn_lvl1_T2.py - COMPLETE REPLACEMENT
# This is the ENTIRE file - delete everything and use only this

import pygame
import config
from video_slide_base import VideoSlidePlayer

# ==========================================================
# SLIDE DATA
# ==========================================================
SLIDES_T2 = [
    # Intro slide
    {
        "title": "Alphabet Names",
        "background_image": {
            "path": "../assets/img/alphabitSound/bg-nt.png",
            "scale": (0.95, 0.78),
            "position": "center"
        },
        "video": {
            "path": "../assets/videos/Lvl1_Topic1_slide2_NoSound.mp4",
            "audio_path": "../assets/sounds/Learn_lvl1_T1/lvl1_topic1_Slide2.wav",
            "scale": (0.3, 0.5),
            "position": "center"
        },
##        "images": [
##            {"path": "../assets/img/boy01.png", "delay": 2000, "scale": (0.1, 0.1), "position": "bottom-right"},
##        ]
    },
    
    # Slide 1 - حرف الألف
    {
        "title": "حرف الألف",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/01alef.png", "sound": "../assets/sounds/alphabitSound/01alef.wav", "delay": 0, "scale": (0.04, 0.40), "position": "center"}
        ]
    },

    # Slide 2 - Ba
    {
        "title": "حرف الباء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/02ba.png", "sound": "../assets/sounds/alphabitSound/02ba.wav", "delay": 0, "scale": (0.20, 0.30), "position": "center"}
        ]
    },
        # Slide 3 - Ta
    {
        "title": "حرف التاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/03ta.png", "sound": "../assets/sounds/alphabitSound/03ta.wav", "delay": 0, "scale": (0.20, 0.35), "position": "center"}
        ]
    },
        # Slide 4 - Tha
    {
        "title": "حرف الثاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/04tha.png", "sound": "../assets/sounds/alphabitSound/04tha.wav", "delay": 0, "scale": (0.20, 0.38), "position": "center"}
        ]
    },
            # Slide 5 - Gem
    {
        "title": "حرف الجيم",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/05geem.png", "sound": "../assets/sounds/alphabitSound/05geem.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 6 - 7a
    {
        "title": "حرف الحاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/06ha.png", "sound": "../assets/sounds/alphabitSound/06-7a.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 7 - 7'a
    {
        "title": "حرف الخاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/07ka.png", "sound": "../assets/sounds/alphabitSound/07-7-a.wav", "delay": 0, "scale": (0.15, 0.45), "position": "center"}
        ]
    },
            # Slide 8 - Dal
    {
        "title": "حرف الدال",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/08dal.png", "sound": "../assets/sounds/alphabitSound/08dal.wav", "delay": 0, "scale": (0.10, 0.30), "position": "center"}
        ]
    },
            # Slide 9 - Thal
    {
        "title": "حرف الذال",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/09thal.png", "sound": "../assets/sounds/alphabitSound/09thal.wav", "delay": 0, "scale": (0.10, 0.40), "position": "center"}
        ]
    },
            # Slide 10 - Ra
    {
        "title": "حرف الراء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/10ra.png", "sound": "../assets/sounds/alphabitSound/10ra.wav", "delay": 0, "scale": (0.10, 0.35), "position": "center"}
        ]
    },
            # Slide 11 - Zay
    {
        "title": "حرف الزاي",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/11zay.png", "sound": "../assets/sounds/alphabitSound/11zay.wav", "delay": 0, "scale": (0.10, 0.40), "position": "center"}
        ]
    },
            # Slide 12 - Sen
    {
        "title": "حرف السين",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/12sen.png", "sound": "../assets/sounds/alphabitSound/12sen.wav", "delay": 0, "scale": (0.20, 0.35), "position": "center"}
        ]
    },
            # Slide 13 - Shen
    {
        "title": "حرف الشين",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/13shen.png", "sound": "../assets/sounds/alphabitSound/13shen.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },
            # Slide 14 - Sad
    {
        "title": "حرف الصاد",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/14sad.png", "sound": "../assets/sounds/alphabitSound/14sad.wav", "delay": 0, "scale": (0.20, 0.35), "position": "center"}
        ]
    },
            # Slide 15 - Dad
    {
        "title": "حرف الضاد",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/15dad.png", "sound": "../assets/sounds/alphabitSound/15dad.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },
            # Slide 16 - Taa
    {
        "title": "حرف الطاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/16taa.png", "sound": "../assets/sounds/alphabitSound/16taa.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },
            # Slide 17 - Zaa
    {
        "title": "حرف الظاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/17zaa.png", "sound": "../assets/sounds/alphabitSound/17zaa.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },
            # Slide 18 - Aen
    {
        "title": "حرف العين",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/18aen.png", "sound": "../assets/sounds/alphabitSound/18ayn.wav", "delay": 0, "scale": (0.15, 0.40), "position": "center"}
        ]
    },
            # Slide 19 - Gaen
    {
        "title": "حرف الغين",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/19gean.png", "sound": "../assets/sounds/alphabitSound/19gean.wav", "delay": 0, "scale": (0.15, 0.45), "position": "center"}
        ]
    },
            # Slide 20 - Feh
    {
        "title": "حرف الفاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/20feh.png", "sound": "../assets/sounds/alphabitSound/20feh.wav", "delay": 0, "scale": (0.20, 0.30), "position": "center"}
        ]
    },
            # Slide 21 - Kf
    {
        "title": "حرف القاف",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/21kf.png", "sound": "../assets/sounds/alphabitSound/21kf.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 22 - Kaf
    {
        "title": "حرف الكاف",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/22kaf.png", "sound": "../assets/sounds/alphabitSound/22kaf.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 23 - Lam
    {
        "title": "حرف اللام",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/23lam.png", "sound": "../assets/sounds/alphabitSound/23lam.wav", "delay": 0, "scale": (0.10, 0.35), "position": "center"}
        ]
    },
            # Slide 24 - Meam
    {
        "title": "حرف الميم",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/24meam.png", "sound": "../assets/sounds/alphabitSound/24meam.wav", "delay": 0, "scale": (0.10, 0.35), "position": "center"}
        ]
    },
            # Slide 25 - Noon
    {
        "title": "حرف النون",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/25noon.png", "sound": "../assets/sounds/alphabitSound/25noon.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 26 - Heh
    {
        "title": "حرف الهاء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/26heh.png", "sound": "../assets/sounds/alphabitSound/26heh.wav", "delay": 0, "scale": (0.15, 0.30), "position": "center"}
        ]
    },
                # Slide 27 - Waw
    {
        "title": "حرف الواو",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/27waw.png", "sound": "../assets/sounds/alphabitSound/27waw.wav", "delay": 0, "scale": (0.10, 0.35), "position": "center"}
        ]
    },
                # Slide 28 - Yaa
    {
        "title": "حرف الياء",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/28yaa.png", "sound": "../assets/sounds/alphabitSound/28yaa.wav", "delay": 0, "scale": (0.20, 0.35), "position": "center"}
        ]
    },
                # End Slid
    {
        "title": "أحسنت",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/coach.png", "sound": "../assets/sounds/alphabitSound/welldone01.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },


    
]

# ==========================================================
# NAVIGABLE VIDEO SLIDE PLAYER (with Next/Prev buttons)
# ==========================================================
class NavigableVideoSlidePlayer(VideoSlidePlayer):
    """Extended player with Next/Prev navigation buttons."""
    
    def draw_navigation_buttons(self, is_video_playing):
        """Draw Next, Prev, and Back buttons."""
        btn_font = pygame.font.Font(
            config.ARABIC_FONT_REGULAR,
            int(self.SCREEN_HEIGHT * 0.035)
        )
        
        # Define button rectangles
        self.next_rect = pygame.Rect(
            int(self.SCREEN_WIDTH * 0.05),
            int(self.SCREEN_HEIGHT * 0.90),
            250, 100
        )
        self.prev_rect = pygame.Rect(
            int(self.SCREEN_WIDTH * 0.82),
            int(self.SCREEN_HEIGHT * 0.90),
            250, 100
        )
        self.back_rect = pygame.Rect(
            int(self.SCREEN_WIDTH * 0.42),
            int(self.SCREEN_HEIGHT * 0.90),
            250, 100
        )
        
        # Button colors (grey out during video playback)
        next_color = (60, 120, 200) if not is_video_playing else (150, 150, 150)
        prev_color = (60, 120, 200) if not is_video_playing else (150, 150, 150)
        back_color = (200, 80, 80)
        
        # Draw buttons
        pygame.draw.rect(self.screen, next_color, self.next_rect, border_radius=15)
        pygame.draw.rect(self.screen, prev_color, self.prev_rect, border_radius=15)
        pygame.draw.rect(self.screen, back_color, self.back_rect, border_radius=15)
        
        # Draw text
        self.main_app.draw_arabic_text("Next", 0.035, (255, 255, 255), self.next_rect.center)
        self.main_app.draw_arabic_text("Prev", 0.035, (255, 255, 255), self.prev_rect.center)
        self.main_app.draw_arabic_text("Back", 0.035, (255, 255, 255), self.back_rect.center)
    
    def handle_mouse_click(self, pos, is_video_playing):
        """Handle mouse clicks including navigation buttons."""
        # Handle parent class buttons (exit, profile)
        if self.main_app.exit_rect.collidepoint(pos):
            if self.main_app.confirm_popup("Exit the game?"):
                pygame.quit()
                import sys
                sys.exit()
        elif self.main_app.profile_rect.collidepoint(pos):
            self.handle_profile_click()
        elif self.back_rect.collidepoint(pos):
            self.handle_back_click()
        
        # Navigation buttons (only work when video isn't playing)
        elif self.next_rect.collidepoint(pos) and not is_video_playing:
            self.navigate_to_next_slide()
        elif self.prev_rect.collidepoint(pos) and not is_video_playing:
            self.navigate_to_prev_slide()
    
    def navigate_to_next_slide(self):
        """Navigate to the next slide."""
        if self.slide_index >= len(self.slides) - 1:
            print(f"ℹ️ Already at last slide ({self.slide_index + 1}/{len(self.slides)})")
            return  # Already at last slide
        
        print(f"➡️ Moving from slide {self.slide_index + 1} to {self.slide_index + 2}")
        
        # Reset state
        self.reset_slide_state()
        
        # Move to next slide
        self.slide_index += 1
        new_slide = self.slides[self.slide_index]
        
        # Reset image played flags
        if "images" in new_slide:
            for img_data in new_slide["images"]:
                img_data["_played"] = False
        
        # Set audio context for new slide
        self.set_audio_context(new_slide)
    
    def navigate_to_prev_slide(self):
        """Navigate to the previous slide."""
        if self.slide_index <= 0:
            print(f"ℹ️ Already at first slide")
            return  # Already at first slide
        
        print(f"⬅️ Moving from slide {self.slide_index + 1} to {self.slide_index}")
        
        # Reset state
        self.reset_slide_state()
        
        # Move to previous slide
        self.slide_index -= 1
        new_slide = self.slides[self.slide_index]
        
        # Reset image played flags
        if "images" in new_slide:
            for img_data in new_slide["images"]:
                img_data["_played"] = False
        
        # Set audio context for new slide
        self.set_audio_context(new_slide)

# ==========================================================
# RUN FUNCTION
# ==========================================================
def run_learn_lvl1_T2(screen, main_app):
    """Launch Topic 2 - Alphabet Names (with navigation)."""
    player = NavigableVideoSlidePlayer(
        screen=screen,
        main_app=main_app,
        slides=SLIDES_T2,
        level=1,
        has_navigation=True  # Enable next/prev buttons
    )
    player.run()
