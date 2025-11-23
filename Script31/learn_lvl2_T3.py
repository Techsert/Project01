# learn_lvl2_T3.py - COMPLETE REPLACEMENT
# This is the ENTIRE file - delete everything and use only this

import pygame
import config
from video_slide_base import VideoSlidePlayer

# ==========================================================
# SLIDE DATA
# ==========================================================
SLIDES_T3 = [
    # Intro slide
##    {
##        "title": "Revision",
##        "background_image": {
##            "path": "../assets/img/alphabitSound/bg-nt.png",
##            "scale": (0.95, 0.78),
##            "position": "center"
##        },
##        "video": {
##            "path": "../assets/videos/Lvl1_Topic1_slide2_NoSound.mp4",
##            "audio_path": "../assets/sounds/Learn_lvl1_T1/lvl1_topic1_Slide2.wav",
##            "scale": (0.3, 0.5),
##            "position": "center"
##        },
##        "images": [
##            {"path": "../assets/img/boy01.png", "delay": 2000, "scale": (0.1, 0.1), "position": "bottom-right"},
##        ]
##    },
    
    # Slide 1 - حرف الألف
    {
        "title": "Revision LVL 2",
        "narration": "",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/main/NotReady.png", "sound": "", "delay": 0, "scale": (0.65, 0.45), "position": "center"}
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
def run_learn_lvl2_T3(screen, main_app):
    """Launch Topic 3"""
    player = NavigableVideoSlidePlayer(
        screen=screen,
        main_app=main_app,
        slides=SLIDES_T3,
        level=2,
        has_navigation=True  # Enable next/prev buttons
    )
    player.run()
