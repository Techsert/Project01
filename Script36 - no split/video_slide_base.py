# video_slide_base.py - COMPLETE VERSION
# Replace your entire video_slide_base.py with this

import pygame
import sys
import time
import os
import arabic_reshaper
from bidi.algorithm import get_display
import config
from moviepy import VideoFileClip
from learning_topics import run_learning_topics

# ==========================================================
# CONSTANTS (eliminates magic numbers)
# ==========================================================
VIDEO_FPS = 30  # Video playback frame rate
FRAME_INTERVAL = 1.0 / VIDEO_FPS
CURSOR_BLINK_MS = 500
VIDEO_CACHE_CLEANUP_INTERVAL = 300  # Clean cache every 5 minutes

# ==========================================================
# GLOBAL VIDEO CACHE with cleanup
# ==========================================================
video_cache = {}
last_video_frame_cache = {}
_cache_last_cleanup = time.time()

def cleanup_video_resources():
    """Properly close and clear video resources to prevent memory leaks."""
    global video_cache, last_video_frame_cache
    
    print("🧹 Cleaning up video resources...")
    for video_path, clip in video_cache.items():
        try:
            if clip:
                clip.close()
        except Exception as e:
            print(f"Error closing video clip {video_path}: {e}")
    
    video_cache.clear()
    last_video_frame_cache.clear()
    print("✅ Video resources cleaned")

def periodic_cache_cleanup():
    """Periodically clean old cached frames to manage memory."""
    global _cache_last_cleanup
    
    current_time = time.time()
    if current_time - _cache_last_cleanup > VIDEO_CACHE_CLEANUP_INTERVAL:
        # Keep only the most recently used frames
        if len(last_video_frame_cache) > 5:
            print(f"⚠️ Frame cache size: {len(last_video_frame_cache)}, cleaning old entries")
            # Keep only the last 3 frames
            keys = list(last_video_frame_cache.keys())
            for key in keys[:-3]:
                del last_video_frame_cache[key]
        _cache_last_cleanup = current_time

# ==========================================================
# VIDEO SLIDE PLAYER BASE CLASS
# ==========================================================
class VideoSlidePlayer:
    """Base class for video slide presentations."""
    
    def __init__(self, screen, main_app, slides, level=1, has_navigation=False):
        """
        Args:
            screen: Pygame screen surface
            main_app: Reference to QuizApp instance
            slides: List of slide dictionaries
            level: Learning level number
            has_navigation: If True, shows Next/Prev buttons
        """
        self.screen = screen
        self.main_app = main_app
        self.slides = slides
        self.level = level
        self.has_navigation = has_navigation
        
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen.get_size()
        self.clock = pygame.time.Clock()
        
        # Slide state
        self.slide_index = 0
        self.start_time = 0
        
        # Video state
        self.current_video_clip = None
        self.video_start_time = 0
        self.video_finished = False
        self.last_rendered_video_frame_surface = None
        self.next_frame_time = 0  # Frame rate limiting
        
        self.running = True

        self.audio_manager = getattr(main_app, 'audio_manager', None)
        
        print(f"🎬 VideoSlidePlayer initialized (level={level}, nav={has_navigation})")
    
    def stop_sounds(self):
        """Stops all audio channels."""
        try:
            if self.audio_manager:
                self.audio_manager.stop_all_sounds()
            else:
                pygame.mixer.music.stop()
                for i in range(pygame.mixer.get_num_channels()):
                    pygame.mixer.Channel(i).stop()
        except Exception as e:
            print(f"❌ Stop sound error: {e}")
    
    def play_sound(self, path):
        """Plays audio file with error handling."""
        try:
            if not os.path.exists(path):
                print(f"⚠️ Audio file not found: {path}")
                return False
            
            if self.audio_manager:
                return self.audio_manager.play_sound(path, 'narration')
            else:
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
                return True
        except Exception as e:
            print(f"❌ Sound error playing {path}: {e}")
            return False
    
    def draw_arabic_text(self, text, size_ratio, color, center, bold=False):
        """Arabic-safe centered text rendering."""
        reshaped = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped)
        font_path = config.ARABIC_FONT_BOLD if bold else config.ARABIC_FONT_REGULAR
        
        try:
            font = pygame.font.Font(font_path, int(self.SCREEN_HEIGHT * size_ratio))
        except Exception as e:
            print(f"❌ Font load error: {e}")
            font = pygame.font.Font(None, int(self.SCREEN_HEIGHT * size_ratio))
        
        rendered = font.render(bidi_text, True, color)
        rect = rendered.get_rect(center=center)
        self.screen.blit(rendered, rect)
    
    def draw_centered_image(self, img_path, scale, position="center"):
        """Draw an image with scaling relative to screen size."""
        try:
            if not os.path.exists(img_path):
                raise FileNotFoundError(f"Image not found: {img_path}")
            
            img = pygame.image.load(img_path).convert_alpha()
            w, h = int(self.SCREEN_WIDTH * scale[0]), int(self.SCREEN_HEIGHT * scale[1])
            img = pygame.transform.smoothscale(img, (w, h))
            rect = img.get_rect()
            
            if position == "center":
                rect.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
            elif position == "top-left":
                rect.topleft = (0, 0)
            elif position == "bottom-right":
                rect.bottomright = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            
            self.screen.blit(img, rect)
            return rect
        except Exception as e:
            print(f"⚠️ Image load error: {img_path} | {e}")
            # Draw placeholder
            placeholder = pygame.Surface((100, 100))
            placeholder.fill((200, 0, 0))
            rect = placeholder.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
            self.screen.blit(placeholder, rect)
            return rect
    
    def load_video_clip(self, video_path):
        """Load video clip with error handling and caching."""
        if video_path not in video_cache:
            try:
                if not os.path.exists(video_path):
                    raise FileNotFoundError(f"Video not found: {video_path}")
                
                clip = VideoFileClip(video_path)
                video_cache[video_path] = clip
                print(f"✅ Loaded video: {os.path.basename(video_path)}")
            except Exception as e:
                print(f"❌ Error loading video {video_path}: {e}")
                return None
        return video_cache[video_path]
    
    def get_video_frame_surface(self, clip, current_time, video_data):
        """Fetches, converts, and scales a video frame with frame rate limiting."""
        try:
            # Frame rate limiting - only get new frame at VIDEO_FPS
            current_real_time = time.time()
            if current_real_time < self.next_frame_time and self.last_rendered_video_frame_surface:
                return self.last_rendered_video_frame_surface
            
            self.next_frame_time = current_real_time + FRAME_INTERVAL
            
            # Get frame from video
            frame_array = clip.get_frame(current_time)
            frame_surface = pygame.surfarray.make_surface(frame_array.swapaxes(0, 1))
            
            # Scale the frame
            scale = video_data.get("scale", (1.0, 1.0))
            w, h = int(self.SCREEN_WIDTH * scale[0]), int(self.SCREEN_HEIGHT * scale[1])
            frame_surface = pygame.transform.smoothscale(frame_surface, (w, h))
            
            return frame_surface
        except Exception as e:
            print(f"❌ Error getting video frame at {current_time:.2f}s: {e}")
            return None
    
    def render_slide(self, slide):
        """Draws content based on slide type: background, video, foreground images."""
        # 1. Draw Background Image if present
        if "background_image" in slide:
            bg_data = slide["background_image"]
            self.draw_centered_image(
                bg_data["path"],
                bg_data.get("scale", (1.0, 1.0)),
                bg_data.get("position", "top-left"),
            )
        
        # 2. Draw Video if present (on top of background)
        if "video" in slide:
            video_data = slide["video"]
            video_path = video_data["path"]
            audio_path = video_data.get("audio_path")
            
            # Initialize video only once when entering the slide
            if self.current_video_clip is None and not self.video_finished:
                self.current_video_clip = self.load_video_clip(video_path)
                if self.current_video_clip:
                    self.video_start_time = time.time()
                    self.last_rendered_video_frame_surface = None
                    self.next_frame_time = 0
                    
                    # Play external audio if provided
                    if audio_path and os.path.exists(audio_path):
                        self.play_sound(audio_path)
                    else:
                        print("⚠️ No audio file specified for video slide.")
                else:
                    self.draw_arabic_text("Video not available", 0.05, (255, 0, 0), 
                                         (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
                    self.video_finished = True
            
            # Display video frame if clip is loaded and not finished
            if self.current_video_clip and not self.video_finished:
                elapsed_video_time = (time.time() - self.video_start_time)
                
                if elapsed_video_time < self.current_video_clip.duration:
                    frame_surface = self.get_video_frame_surface(
                        self.current_video_clip, elapsed_video_time, video_data
                    )
                    if frame_surface:
                        self.last_rendered_video_frame_surface = frame_surface
                else:
                    # Video finished, cache last frame
                    if self.last_rendered_video_frame_surface is None or video_path not in last_video_frame_cache:
                        frame_surface = self.get_video_frame_surface(
                            self.current_video_clip, 
                            self.current_video_clip.duration - 0.01, 
                            video_data
                        )
                        if frame_surface:
                            self.last_rendered_video_frame_surface = frame_surface
                            last_video_frame_cache[video_path] = frame_surface
                    
                    self.video_finished = True
                    pygame.mixer.music.stop()
            
            # Draw the cached frame
            if self.last_rendered_video_frame_surface:
                rect = self.last_rendered_video_frame_surface.get_rect()
                position = video_data.get("position", "center")
                if position == "center":
                    rect.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
                elif position == "top-left":
                    rect.topleft = (0, 0)
                elif position == "bottom-right":
                    rect.bottomright = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                self.screen.blit(self.last_rendered_video_frame_surface, rect)
            elif self.video_finished and video_path in last_video_frame_cache:
                rect = last_video_frame_cache[video_path].get_rect()
                position = video_data.get("position", "center")
                if position == "center":
                    rect.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
                elif position == "top-left":
                    rect.topleft = (0, 0)
                elif position == "bottom-right":
                    rect.bottomright = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                self.screen.blit(last_video_frame_cache[video_path], rect)
        
        # 3. Draw Foreground Images if present
        if "images" in slide:
            elapsed = (time.time() - self.start_time) * 1000
            for img_data in slide["images"]:
                delay = img_data.get("delay", 0)
                duration = img_data.get("duration", None)
                
                if elapsed >= delay and (duration is None or elapsed <= delay + duration):
                    self.draw_centered_image(
                        img_data["path"],
                        img_data.get("scale", (0.3, 0.3)),
                        img_data.get("position", "center"),
                    )
                
                if not img_data.get("_played", False) and elapsed >= delay and "sound" in img_data:
                    if not pygame.mixer.music.get_busy() or "video" not in slide:
                        self.play_sound(img_data["sound"])
                        img_data["_played"] = True
    
    def reset_slide_state(self):
        """Reset state when changing slides."""
        self.stop_sounds()
        self.current_video_clip = None
        self.video_finished = False
        self.last_rendered_video_frame_surface = None
        self.start_time = time.time()
    
    def set_audio_context(self, slide):
        """Set audio context for main_app based on slide type."""
        if self.audio_manager:
            if "video" in slide:
                video_data = slide["video"]
                audio_path = video_data.get("audio_path")
                if audio_path:
                    self.audio_manager.set_context('video_audio', audio_path)
                else:
                    self.audio_manager.set_context('video_audio', None)
            elif "narration" in slide:
                self.audio_manager.set_context('narration', slide["narration"])
            else:
                self.audio_manager.set_context('bg_music', None)
        
        # Backwards compatibility
        if "video" in slide:
            video_data = slide["video"]
            self.main_app._current_audio_type = 'video_audio'
            self.main_app._current_audio_path = video_data.get("audio_path")
        elif "narration" in slide:
            self.main_app._current_audio_type = 'narration'
            self.main_app._current_audio_path = slide["narration"]
            self.play_sound(slide["narration"])
        else:
            self.main_app._current_audio_type = 'bg_music'
            self.main_app._current_audio_path = None
    
    def handle_profile_click(self):
        """Handle profile icon click with audio context management."""
        print("👤 Profile icon clicked")
        
        # ✅ Push audio context BEFORE stopping sounds
        if self.audio_manager:
            self.audio_manager.push_audio_context()
        
        # Stop sounds for profile screen
        self.stop_sounds()
        
        # Open profile manager
        self.main_app.open_profile_manager()
        
        # ✅ Audio context will be restored by open_profile_manager
        # Reset video state when returning
        current_slide_data = self.slides[self.slide_index]
        if "video" in current_slide_data:
            self.current_video_clip = None
            self.video_start_time = 0
            self.video_finished = False
            self.last_rendered_video_frame_surface = None
            print("🔄 Video state reset after profile return")
    
    def handle_back_click(self):
        """Handle back button click."""
        print("⬅️ Back button clicked")
        
        self.stop_sounds()
        self.current_video_clip = None
        self.video_finished = False
        self.last_rendered_video_frame_surface = None
        
        # ✅ Always restore background music when leaving video player
        if self.audio_manager:
            # Pop context but force BG music to play
            self.audio_manager.pop_audio_context(restore=True, force_bg_music=True)
        
        # Clear audio context
        self.main_app._current_audio_type = 'bg_music'
        self.main_app._current_audio_path = None
        
        self.running = False
        from learning_topics import run_learning_topics
        run_learning_topics(self.screen, self.main_app, level=self.level)
    
    def run(self):
        """Main loop for slide presentation."""
        print(f"▶️ Starting video slide player (slide {self.slide_index + 1}/{len(self.slides)})")
        
        # ✅ Push audio context when entering video player
        if self.audio_manager:
            self.audio_manager.push_audio_context()
        
        # Initial slide setup
        current_slide = self.slides[self.slide_index]
        self.set_audio_context(current_slide)
        self.start_time = time.time()
        
        while self.running:
            self.screen.fill((255, 255, 255))
            slide = self.slides[self.slide_index]
            
            # Determine if video is currently active and playing
            is_video_slide = "video" in slide
            is_video_playing = is_video_slide and self.current_video_clip is not None and not self.video_finished
            
            # Render slide content
            self.render_slide(slide)
            
            # Title
            self.draw_arabic_text(
                slide["title"],
                0.06,
                (0, 0, 0),
                (self.SCREEN_WIDTH // 2, int(self.SCREEN_HEIGHT * 0.07)),
                bold=True
            )
            
            # Profile + Exit icons
            self.screen.blit(self.main_app.profile_icon, self.main_app.profile_rect)
            self.screen.blit(self.main_app.exit_icon, self.main_app.exit_rect)
            
            # Navigation buttons
            self.draw_navigation_buttons(is_video_playing)
            
            pygame.display.flip()
            
            # Event handling
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    cleanup_video_resources()
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.running = False
                    pygame.event.clear()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(e.pos, is_video_playing)
            
            # Periodic cache cleanup
            periodic_cache_cleanup()
            
            self.clock.tick(60)
        
        # ✅ Cleanup on exit - restore audio context
        print("⏹️ Video slide player stopping")
        self.stop_sounds()
        cleanup_video_resources()
        
        # ✅ Pop audio context when leaving video player
        if self.audio_manager:
            self.audio_manager.pop_audio_context(restore=True)
        else:
            # Fallback: just play BG music
            if hasattr(self.main_app, 'play_bg_music'):
                self.main_app.play_bg_music()
    
    def draw_navigation_buttons(self, is_video_playing):
        """Draw navigation buttons (overridden by subclasses)."""
        # Base implementation - just back button
        btn_font = pygame.font.Font(
            config.ARABIC_FONT_REGULAR,
            int(self.SCREEN_HEIGHT * 0.035)
        )
        back_rect = pygame.Rect(
            int(self.SCREEN_WIDTH * 0.42),
            int(self.SCREEN_HEIGHT * 0.90),
            250,
            100
        )
        back_color = (200, 80, 80)
        
        pygame.draw.rect(self.screen, back_color, back_rect, border_radius=15)
        self.main_app.draw_arabic_text(
            "Back",
            0.035,
            (255, 255, 255),
            back_rect.center
        )
        
        # Store for event handling
        self.back_rect = back_rect
    
    def handle_mouse_click(self, pos, is_video_playing):
        """Handle mouse clicks (overridden by subclasses)."""
        if self.main_app.exit_rect.collidepoint(pos):
            if self.main_app.confirm_popup("Exit the game?"):
                cleanup_video_resources()
                pygame.quit()
                sys.exit()
        elif self.main_app.profile_rect.collidepoint(pos):
            self.handle_profile_click()
        elif hasattr(self, 'back_rect') and self.back_rect.collidepoint(pos):
            self.handle_back_click()


# ==========================================================
# NAVIGABLE VIDEO SLIDE PLAYER (with Next/Prev buttons)
# ✅ ADD THIS CLASS - IT WAS MISSING!
# ==========================================================
class NavigableVideoSlidePlayer(VideoSlidePlayer):
    """Extended player with Next/Prev navigation buttons - SHARED BY ALL TOPICS."""
    
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
        if self.main_app.exit_rect.collidepoint(pos):
            if self.main_app.confirm_popup("Exit the game?"):
                cleanup_video_resources()
                pygame.quit()
                import sys
                sys.exit()
        elif self.main_app.profile_rect.collidepoint(pos):
            self.handle_profile_click()
        elif self.back_rect.collidepoint(pos):
            self.handle_back_click()
        elif self.next_rect.collidepoint(pos) and not is_video_playing:
            self.navigate_to_next_slide()
        elif self.prev_rect.collidepoint(pos) and not is_video_playing:
            self.navigate_to_prev_slide()
    
    def navigate_to_next_slide(self):
        """Navigate to the next slide."""
        if self.slide_index >= len(self.slides) - 1:
            print(f"ℹ️ Already at last slide ({self.slide_index + 1}/{len(self.slides)})")
            return
        
        print(f"➡️ Moving from slide {self.slide_index + 1} to {self.slide_index + 2}")
        
        # ✅ Stop audio before changing slides
        if self.audio_manager:
            self.audio_manager.stop_all_sounds()
        
        self.reset_slide_state()
        self.slide_index += 1
        new_slide = self.slides[self.slide_index]
        
        if "images" in new_slide:
            for img_data in new_slide["images"]:
                img_data["_played"] = False
        
        # ✅ Set new audio context
        self.set_audio_context(new_slide)
    
    def navigate_to_prev_slide(self):
        """Navigate to the previous slide."""
        if self.slide_index <= 0:
            print(f"ℹ️ Already at first slide")
            return
        
        print(f"⬅️ Moving from slide {self.slide_index + 1} to {self.slide_index}")
        
        # ✅ Stop audio before changing slides
        if self.audio_manager:
            self.audio_manager.stop_all_sounds()
        
        self.reset_slide_state()
        self.slide_index -= 1
        new_slide = self.slides[self.slide_index]
        
        if "images" in new_slide:
            for img_data in new_slide["images"]:
                img_data["_played"] = False
        
        # ✅ Set new audio context
        self.set_audio_context(new_slide)
