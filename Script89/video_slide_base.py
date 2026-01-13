# video_slide_base.py - FIXED TO NOT CHECK REWARDS (let main app handle it)
import pygame
import sys
import time
import os
import arabic_reshaper
from bidi.algorithm import get_display
import config
##from moviepy import VideoFileClip
##from learning_topics import run_learning_topics
from screen_helpers import confirm_popup, load_font
from profile_system import mark_learning_topic_complete
from ffpyplayer.player import MediaPlayer

# ==========================================================
# CONSTANTS
# ==========================================================
VIDEO_CACHE_CLEANUP_INTERVAL = 300

# ==========================================================
# GLOBAL VIDEO CACHE (Updated for FFPyPlayer)
# ==========================================================
video_cache = {}
last_video_frame_cache = {}
_cache_last_cleanup = time.time()

def cleanup_video_resources():
    """Properly close and clear video resources."""
    global video_cache, last_video_frame_cache
    
    print("🧹 Cleaning up video resources...")
    for video_path, player in video_cache.items():
        try:
            if player:
                player.close_player() # ✅ FFPyPlayer close method
        except Exception as e:
            print(f"Error closing video player {video_path}: {e}")
    
    video_cache.clear()
    last_video_frame_cache.clear()
    print("✅ Video resources cleaned")

def periodic_cache_cleanup():
    """Periodically clean old cached frames."""
    global _cache_last_cleanup
    current_time = time.time()
    if current_time - _cache_last_cleanup > VIDEO_CACHE_CLEANUP_INTERVAL:
        if len(last_video_frame_cache) > 5:
            keys = list(last_video_frame_cache.keys())
            for key in keys[:-3]:
                del last_video_frame_cache[key]
        _cache_last_cleanup = current_time

# ==========================================================
# VIDEO SLIDE PLAYER BASE CLASS
# ==========================================================
class VideoSlidePlayer:
    def __init__(self, screen, main_app, slides, level=1, has_navigation=False):
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
        self.current_video_player = None # ✅ Renamed from 'clip' to 'player'
        self.video_finished = False
        self.last_rendered_video_frame_surface = None
        
        self.running = True
        self._learning_recorded = False
    
    # ==========================================================
    # AUDIO METHODS - USING AUDIO MANAGER
    # ==========================================================
    def stop_sounds(self):
        """✅ Use AudioManager to stop sounds."""
        self.main_app.audio_manager.stop_all_sounds()
    
    def play_sound(self, path):
        """✅ Use AudioManager to play sound."""
        return self.main_app.audio_manager.play_sound(path, audio_type='narration')
    
    # ==========================================================
    # TEXT AND IMAGE RENDERING
    # ==========================================================
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

    # ===========================================================
    # ADD TEXT SUPPORT TO video_slide_base.py
    # ===========================================================
    def render_text_element(self, text_data, elapsed):
        """Render text element on slide with timing, positioning, and effects."""
        delay = text_data.get("delay", 0)
        duration = text_data.get("duration", None)
        
        # Check timing
        if elapsed < delay:
            return
        
        if duration is not None and elapsed > delay + duration:
            return
        
        # Flash effect
        flash_count = text_data.get("flash_count", 0)
        flash_speed = text_data.get("flash_speed", 500)
        should_draw = True
        
        if flash_count > 0:
            if "_flash_start" not in text_data:
                text_data["_flash_start"] = elapsed
                text_data["_flashes_done"] = 0
            
            flash_elapsed = elapsed - text_data["_flash_start"]
            flash_cycle = int(flash_elapsed / flash_speed)
            
            if text_data["_flashes_done"] < flash_count:
                should_draw = (flash_cycle % 2) == 0
                if flash_cycle > text_data["_flashes_done"] * 2:
                    text_data["_flashes_done"] = flash_cycle // 2
        
        if not should_draw:
            return
        
        # Get text properties
        text = text_data.get("text", "")
        size_ratio = text_data.get("size_ratio", 0.05)
        color = text_data.get("color", (0, 0, 0))
        bold = text_data.get("bold", False)
        
        # Calculate position
        position = text_data.get("position", "center")
        offset = text_data.get("offset", {"x": 0, "y": 0})
        
        # Determine center coordinates
        if isinstance(position, tuple):
            x, y = position
        elif position == "center":
            x, y = self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2
        elif position == "top":
            x, y = self.SCREEN_WIDTH // 2, int(self.SCREEN_HEIGHT * 0.1)
        elif position == "bottom":
            x, y = self.SCREEN_WIDTH // 2, int(self.SCREEN_HEIGHT * 0.9)
        elif position == "left":
            x, y = int(self.SCREEN_WIDTH * 0.1), self.SCREEN_HEIGHT // 2
        elif position == "right":
            x, y = int(self.SCREEN_WIDTH * 0.9), self.SCREEN_HEIGHT // 2
        elif position == "top-left":
            x, y = int(self.SCREEN_WIDTH * 0.1), int(self.SCREEN_HEIGHT * 0.1)
        elif position == "top-right":
            x, y = int(self.SCREEN_WIDTH * 0.9), int(self.SCREEN_HEIGHT * 0.1)
        elif position == "bottom-left":
            x, y = int(self.SCREEN_WIDTH * 0.1), int(self.SCREEN_HEIGHT * 0.9)
        elif position == "bottom-right":
            x, y = int(self.SCREEN_WIDTH * 0.9), int(self.SCREEN_HEIGHT * 0.9)
        else:
            x, y = self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2
        
        # Apply offset
        if offset:
            x += offset.get("x", 0)
            y += offset.get("y", 0)
            
        # Draw the text
        self.draw_arabic_text(text, size_ratio, color, (x, y), bold)
    
    def draw_centered_image(self, img_path, scale, position="center", offset=None):
        """Draw an image with scaling relative to screen size and optional offset."""
        try:
            if not os.path.exists(img_path):
                raise FileNotFoundError(f"Image not found: {img_path}")
            
            img = pygame.image.load(img_path).convert_alpha()
            w, h = int(self.SCREEN_WIDTH * scale[0]), int(self.SCREEN_HEIGHT * scale[1])
            img = pygame.transform.smoothscale(img, (w, h))
            rect = img.get_rect()
            
            # Set base position
            if position == "center":
                rect.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
            elif position == "top-left":
                rect.topleft = (0, 0)
            elif position == "bottom-right":
                rect.bottomright = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            elif position == "left":
                rect.midleft = (0, self.SCREEN_HEIGHT // 2)
            elif position == "right":
                rect.midright = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT // 2)
            elif position == "top":
                rect.midtop = (self.SCREEN_WIDTH // 2, 0)
            elif position == "bottom":
                rect.midbottom = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT)
            
            # ✅ Apply offset if provided
            if offset:
                rect.x += offset.get("x", 0)
                rect.y += offset.get("y", 0)
            
            self.screen.blit(img, rect)
            return rect
        except Exception as e:
            print(f"⚠️ Image load error: {img_path} | {e}")
            placeholder = pygame.Surface((100, 100))
            placeholder.fill((200, 0, 0))
            rect = placeholder.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
            self.screen.blit(placeholder, rect)
            return rect
    
    # ==========================================================
    # ✅ NEW FFPYPLAYER VIDEO METHODS
    # ==========================================================
    def load_video_player(self, video_path):
        """Load video using FFPyPlayer."""
        if video_path not in video_cache:
            try:
                if not os.path.exists(video_path):
                    print(f"❌ Video not found: {video_path}")
                    return None
                
                # Create FFPyPlayer
                player = MediaPlayer(video_path)
                video_cache[video_path] = player
                print(f"✅ Loaded video: {os.path.basename(video_path)}")
            except Exception as e:
                print(f"❌ Error loading video: {e}")
                return None
        return video_cache[video_path]

    def render_slide(self, slide):
        """Draws content: BG -> Video -> Images -> Text."""
        
        # 1. Background (Keep this!)
        if "background_image" in slide:
            bg_data = slide["background_image"]
            self.draw_centered_image(
                bg_data["path"],
                bg_data.get("scale", (1.0, 1.0)),
                bg_data.get("position", "top-left"),
            )
        
        # 2. Video (✅ UPDATED FOR FFPYPLAYER)
        if "video" in slide:
            video_data = slide["video"]
            video_path = video_data["path"]
            audio_path = video_data.get("audio_path")
            
            # Initialize Player
            if self.current_video_player is None and not self.video_finished:
                self.current_video_player = self.load_video_player(video_path)
                if audio_path:
                    delay = video_data.get("audio_delay", 0.0) # Default 0.0s delay
                    self.audio_start_trigger = time.time() + delay
                    self.pending_audio_path = audio_path
                
                if self.current_video_player:
                    # Sync external audio
                    if audio_path and os.path.exists(audio_path):
                        self.main_app.audio_manager.play_sound(audio_path, audio_type='video_audio')
                        # Mute internal video audio so they don't clash
                        self.current_video_player.set_volume(0.0)
                else:
                    self.video_finished = True

            # Get Frame from FFPyPlayer
            if self.current_video_player and not self.video_finished:
                frame, val = self.current_video_player.get_frame()
                
                if val == 'eof':
                    self.video_finished = True
                elif frame is not None:
                    # Convert to Pygame Surface
                    img, t = frame
                    w, h = img.get_size()
                    # Convert raw data to pygame surface
                    # Note: FFPyPlayer usually outputs RGB
                    video_surf = pygame.image.frombuffer(img.to_bytearray()[0], (w, h), "RGB")
                    
                    # Scale to fit screen
                    scale = video_data.get("scale", (1.0, 1.0))
                    target_w = int(self.SCREEN_WIDTH * scale[0])
                    target_h = int(self.SCREEN_HEIGHT * scale[1])
                    
                    self.last_rendered_video_frame_surface = pygame.transform.smoothscale(video_surf, (target_w, target_h))
            
            # Draw the Surface
            if self.last_rendered_video_frame_surface:
                rect = self.last_rendered_video_frame_surface.get_rect()
                position = video_data.get("position", "center")
                
                if position == "center":
                    rect.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
                elif position == "top-left":
                    rect.topleft = (0, 0)
                
                self.screen.blit(self.last_rendered_video_frame_surface, rect)

        # 3. Foreground images WITH FLASHING SUPPORT
        if "images" in slide:
            elapsed = (time.time() - self.start_time) * 1000
            
            for img_data in slide["images"]:
                delay = img_data.get("delay", 0)
                duration = img_data.get("duration", None)
                
                # Flash effect parameters
                flash_count = img_data.get("flash_count", 0)
                flash_speed = img_data.get("flash_speed", 500)
                flash_repeat = img_data.get("flash_repeat", 1)
                flash_cycle_interval = img_data.get("flash_cycle_interval", 2000)

                # Check if image should be visible based on timing
                if elapsed >= delay and (duration is None or elapsed <= delay + duration):
                    
                    # Apply flashing effect with repeat cycles
                    should_draw = True
                    if flash_count > 0:
                        # Initialize flash state if not exists
                        if "_flash_cycle_count" not in img_data:
                            img_data["_flash_cycle_count"] = 0
                            img_data["_flash_start"] = elapsed
                            img_data["_flashes_done"] = 0
                            img_data["_in_cycle_pause"] = False
                            img_data["_cycle_pause_start"] = 0
                        
                        # Check if we're in a pause between cycles
                        if img_data["_in_cycle_pause"]:
                            pause_elapsed = elapsed - img_data["_cycle_pause_start"]
                            if pause_elapsed >= flash_cycle_interval:
                                # Start next cycle
                                img_data["_in_cycle_pause"] = False
                                img_data["_flash_start"] = elapsed
                                img_data["_flashes_done"] = 0
                                img_data["_flash_cycle_count"] += 1
                            else:
                                should_draw = True
                        else:
                            # We're in an active flash cycle
                            flash_elapsed = elapsed - img_data["_flash_start"]
                            flash_cycle = int(flash_elapsed / flash_speed)
                            
                            if img_data["_flashes_done"] < flash_count:
                                should_draw = (flash_cycle % 2) == 0
                                if flash_cycle > img_data["_flashes_done"] * 2:
                                    img_data["_flashes_done"] = flash_cycle // 2
                            else:
                                # Finished this cycle
                                if img_data["_flash_cycle_count"] + 1 < flash_repeat:
                                    img_data["_in_cycle_pause"] = True
                                    img_data["_cycle_pause_start"] = elapsed
                                    should_draw = True
                                else:
                                    should_draw = True
                    
                    # Draw image
                    if should_draw:
                        self.draw_centered_image(
                            img_data["path"],
                            img_data.get("scale", (0.3, 0.3)),
                            img_data.get("position", "center"),
                            img_data.get("offset", None),
                        )               
                
                # Play sound with optional repeat
                if "sound" in img_data:
                    repeat_count = img_data.get("sound_repeat", 1)
                    repeat_interval = img_data.get("sound_interval", 1000)
                    
                    if "_sound_play_count" not in img_data:
                        img_data["_sound_play_count"] = 0
                        img_data["_last_sound_time"] = -repeat_interval                  
                    
                    if (elapsed >= delay and 
                        img_data["_sound_play_count"] < repeat_count and
                        elapsed - img_data["_last_sound_time"] >= repeat_interval):
                        
                        # Only play if main music isn't overpowering or if it's designed to overlap
                        # (Adjust this check based on your preference, currently set to play freely)
                        self.play_sound(img_data["sound"])
                        img_data["_sound_play_count"] += 1
                        img_data["_last_sound_time"] = elapsed

        # 4. Text elements (✅ KEEP THIS - Crucial for labels!)
        if "texts" in slide:
            elapsed = (time.time() - self.start_time) * 1000
            for text_data in slide["texts"]:
                # Your full render_text_element function handles this
                self.render_text_element(text_data, elapsed)

    
    
    def reset_slide_state(self):
        """Reset state when changing slides."""
        self.stop_sounds()
        # FFPyPlayer specific reset
        if self.current_video_player:
            # We don't close it if we want to cache it, but we might want to seek to 0
            # For simplicity with caching, we just set current to None and let cache handle it
            # Or seek: self.current_video_player.seek(0)
            pass
            
        self.current_video_player = None 
        self.video_finished = False
        self.last_rendered_video_frame_surface = None
        self.start_time = time.time()
        
        # Reset flash states for images
        # Reset flash states for images
        if 0 <= self.slide_index < len(self.slides):
            slide = self.slides[self.slide_index]
            if "images" in slide:
                for img_data in slide["images"]:
                    if "_flash_start" in img_data:
                        del img_data["_flash_start"]
                    if "_flashes_done" in img_data:
                        del img_data["_flashes_done"]
                    # ✅ NEW: Reset flash cycle states
                    if "_flash_cycle_count" in img_data:
                        del img_data["_flash_cycle_count"]
                    if "_in_cycle_pause" in img_data:
                        del img_data["_in_cycle_pause"]
                    if "_cycle_pause_start" in img_data:
                        del img_data["_cycle_pause_start"]
                    # Reset sound repeat states
                    if "_sound_play_count" in img_data:
                        del img_data["_sound_play_count"]
                    if "_last_sound_time" in img_data:
                        del img_data["_last_sound_time"]
            
            # ✅ NEW: Reset flash states for texts
            if "texts" in slide:
                for text_data in slide["texts"]:
                    if "_flash_start" in text_data:
                        del text_data["_flash_start"]
                    if "_flashes_done" in text_data:
                        del text_data["_flashes_done"]
    
    def set_audio_context(self, slide):
        """✅ Set audio context using AudioManager."""
        if "video" in slide:
            video_data = slide["video"]
            if video_data.get("audio_path"):
                self.main_app.audio_manager.set_context('video_audio', video_data["audio_path"])
            else:
                self.main_app.audio_manager.set_context('video_audio', "temp_video_audio.wav")
        elif "narration" in slide:
            self.main_app.audio_manager.set_context('narration', slide["narration"])
            self.play_sound(slide["narration"])
        else:
            self.main_app.audio_manager.set_context('bg_music', None)
    
    def handle_profile_click(self):
        """✅ Handle profile click with AudioManager context management."""
        current_slide_data = self.slides[self.slide_index]
        
        # Push audio context
        self.main_app.audio_manager.push_audio_context()
        
        # Stop all sounds
        self.stop_sounds()
        
        # Open profile
        self.main_app.open_profile_manager()
        
        # Reset video state when returning
        if "video" in current_slide_data:
            self.current_video_clip = None
            self.video_start_time = 0
            self.video_finished = False
            self.last_rendered_video_frame_surface = None
        
        # Restore audio context
        self.main_app.audio_manager.pop_audio_context(restore=True)
    
    def handle_back_click(self):
        """Handle back button click."""
        self.stop_sounds()
        self.current_video_clip = None
        self.video_finished = False
        self.last_rendered_video_frame_surface = None
        
        # Clear audio context
        self.main_app.audio_manager.set_context('bg_music', None)
        
        self.running = False
    
    # ==========================================================
    # MAIN LOOP
    # ==========================================================
    def run(self):
        # (Standard run loop, no changes needed except ensuring cleanup happens)
        current_slide = self.slides[self.slide_index]
        self.set_audio_context(current_slide)
        self.start_time = time.time()
        
        while self.running:
            self.screen.fill((255, 255, 255))
            slide = self.slides[self.slide_index]
            
            # Logic check for nav buttons
            is_video_slide = "video" in slide
            is_video_playing = is_video_slide and not self.video_finished
            
            self.render_slide(slide)
            
            # UI Overlays
            self.draw_arabic_text(slide["title"], 0.06, (0, 0, 0), (self.SCREEN_WIDTH // 2, int(self.SCREEN_HEIGHT * 0.07)), bold=True)
            self.screen.blit(self.main_app.profile_icon, self.main_app.profile_rect)
            self.screen.blit(self.main_app.exit_icon, self.main_app.exit_rect)
            self.draw_navigation_buttons(is_video_playing)
            
            pygame.display.flip()
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    cleanup_video_resources()
                    pygame.quit(); sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(e.pos, is_video_playing)
            
            periodic_cache_cleanup()
            self.clock.tick(60) # Higher FPS possible now!
            
        self.stop_sounds()
        cleanup_video_resources()
        self.main_app.audio_manager.set_context('bg_music', None)
    
    def draw_navigation_buttons(self, is_video_playing):
        """Draw navigation buttons (overridden by subclasses)."""
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
        
        self.back_rect = back_rect
    
    def handle_mouse_click(self, pos, is_video_playing):
        """✅ Handle mouse clicks using screen_helpers.confirm_popup."""
        if self.main_app.exit_rect.collidepoint(pos):
            # ✅ Use centralized confirm_popup from screen_helpers
            if confirm_popup(
                self.screen,
                "Exit the game?",
                lambda size, bold=False: load_font(
                    config.ARABIC_FONT_REGULAR,
                    config.ARABIC_FONT_BOLD,
                    size,
                    bold
                )
            ):
                cleanup_video_resources()
                pygame.quit()
                sys.exit()
        elif self.main_app.profile_rect.collidepoint(pos):
            self.handle_profile_click()
        elif hasattr(self, 'back_rect') and self.back_rect.collidepoint(pos):
            self.handle_back_click()


# ==========================================================
# NAVIGABLE VIDEO SLIDE PLAYER
# ==========================================================
class NavigableVideoSlidePlayer(VideoSlidePlayer):
    """✅ Extended player with Next/Prev navigation - USES AUDIO_MANAGER."""
    
    def draw_navigation_buttons(self, is_video_playing):
        """Draw Next, Prev, and Back buttons."""
        btn_font = pygame.font.Font(
            config.ARABIC_FONT_REGULAR,
            int(self.SCREEN_HEIGHT * 0.035)
        )
        
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
        
        next_color = (60, 120, 200) if not is_video_playing else (150, 150, 150)
        prev_color = (60, 120, 200) if not is_video_playing else (150, 150, 150)
        back_color = (200, 80, 80)
        
        pygame.draw.rect(self.screen, next_color, self.next_rect, border_radius=15)
        pygame.draw.rect(self.screen, prev_color, self.prev_rect, border_radius=15)
        pygame.draw.rect(self.screen, back_color, self.back_rect, border_radius=15)
        
        self.main_app.draw_arabic_text("Next", 0.035, (255, 255, 255), self.next_rect.center)
        self.main_app.draw_arabic_text("Prev", 0.035, (255, 255, 255), self.prev_rect.center)
        self.main_app.draw_arabic_text("Back", 0.035, (255, 255, 255), self.back_rect.center)
    
    def handle_mouse_click(self, pos, is_video_playing):
        """✅ Handle clicks with confirm_popup from screen_helpers."""
        if self.main_app.exit_rect.collidepoint(pos):
            if confirm_popup(
                self.screen,
                "Exit the game?",
                lambda size, bold=False: load_font(
                    config.ARABIC_FONT_REGULAR,
                    config.ARABIC_FONT_BOLD,
                    size,
                    bold
                )
            ):
                cleanup_video_resources()
                pygame.quit()
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
            # ✅ Mark completion when reaching last slide
            self.check_and_mark_completion()
            return
        
        print(f"➡️ Moving from slide {self.slide_index + 1} to {self.slide_index + 2}")
        
        self.reset_slide_state()
        self.slide_index += 1
        new_slide = self.slides[self.slide_index]
        
        if "images" in new_slide:
            for img_data in new_slide["images"]:
                img_data["_played"] = False
        
        self.set_audio_context(new_slide)
        
        # ✅ Check completion after moving to last slide
        if self.slide_index >= len(self.slides) - 1:
            self.check_and_mark_completion()
    
    def navigate_to_prev_slide(self):
        """Navigate to the previous slide."""
        if self.slide_index <= 0:
            print(f"ℹ️ Already at first slide")
            return
        
        print(f"⬅️ Moving from slide {self.slide_index + 1} to {self.slide_index}")
        
        self.reset_slide_state()
        self.slide_index -= 1
        new_slide = self.slides[self.slide_index]
        
        if "images" in new_slide:
            for img_data in new_slide["images"]:
                img_data["_played"] = False
        
        self.set_audio_context(new_slide)

    def check_and_mark_completion(self):
        """✅ FIXED: Mark topic complete WITHOUT checking rewards here"""
        if self.slide_index >= len(self.slides) - 1:  # On last slide
            profile_name = self.main_app.selected_profile.get("name") if self.main_app.selected_profile else None
            if profile_name and not hasattr(self, '_learning_recorded'):
                # ✅ Only mark completion - don't check rewards
                # Rewards will be checked in main_menu28.py after _reload_profile()
                topic = getattr(self, 'topic', 'T1')
                mark_learning_topic_complete(profile_name, self.level, topic)
                self._learning_recorded = True
                print(f"✅ {profile_name} completed Learning Level {self.level} - Topic {topic}")
