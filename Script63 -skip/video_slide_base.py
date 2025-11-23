# video_slide_base.py - UPDATED WITH SPRITE ANIMATION SUPPORT
import pygame
import sys
import time
import os
import arabic_reshaper
from bidi.algorithm import get_display
import config
from moviepy import VideoFileClip
from learning_topics import run_learning_topics
from screen_helpers import confirm_popup, load_font
from profile_system import mark_learning_topic_complete
from sprite_animation import SpriteAnimation  # ✅ NEW IMPORT

# ==========================================================
# CONSTANTS
# ==========================================================
VIDEO_FPS = 30
FRAME_INTERVAL = 1.0 / VIDEO_FPS
VIDEO_CACHE_CLEANUP_INTERVAL = 300

# ==========================================================
# GLOBAL VIDEO CACHE (Legacy - for backwards compatibility)
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
        if len(last_video_frame_cache) > 5:
            print(f"⚠️ Frame cache size: {len(last_video_frame_cache)}, cleaning old entries")
            keys = list(last_video_frame_cache.keys())
            for key in keys[:-3]:
                del last_video_frame_cache[key]
        _cache_last_cleanup = current_time

# ==========================================================
# VIDEO SLIDE PLAYER BASE CLASS
# ==========================================================
class VideoSlidePlayer:
    """
    Base class for video/animation slide presentations.
    ✅ NOW SUPPORTS BOTH SPRITE ANIMATIONS AND VIDEOS
    """
    
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
        
        # Video state (legacy)
        self.current_video_clip = None
        self.video_start_time = 0
        self.video_finished = False
        self.last_rendered_video_frame_surface = None
        self.next_frame_time = 0
        
        # ✅ NEW: Sprite animation state
        self.current_animation = None
        self.animation_finished = False
        
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
            print(f"⌫ Font load error: {e}")
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
            placeholder = pygame.Surface((100, 100))
            placeholder.fill((200, 0, 0))
            rect = placeholder.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
            self.screen.blit(placeholder, rect)
            return rect
    
    # ==========================================================
    # ✅ NEW: SPRITE ANIMATION METHODS
    # ==========================================================
    def load_sprite_animation(self, animation_data):
        """
        Load sprite animation from slide data.
        
        Animation data format:
        {
            "type": "sprite_sheet",  # or "individual_frames"
            "path": "path/to/sprite_sheet.png",  # or list of frame paths
            "frame_width": 256,
            "frame_height": 256,
            "num_frames": 30,
            "fps": 30,
            "loop": True,
            "scale": (0.3, 0.5),  # As screen ratio
            "position": "center",
            "audio_path": "optional_audio.wav"
        }
        """
        try:
            anim_type = animation_data.get("type", "sprite_sheet")
            fps = animation_data.get("fps", 30)
            loop = animation_data.get("loop", True)
            scale_ratio = animation_data.get("scale", (1.0, 1.0))
            
            # Calculate actual pixel size from screen ratio
            scale_pixels = (
                int(self.SCREEN_WIDTH * scale_ratio[0]),
                int(self.SCREEN_HEIGHT * scale_ratio[1])
            )
            
            if anim_type == "sprite_sheet":
                # Load from sprite sheet
                animation = SpriteAnimation(
                    sprite_sheet_path=animation_data["path"],
                    frame_width=animation_data["frame_width"],
                    frame_height=animation_data["frame_height"],
                    num_frames=animation_data["num_frames"],
                    fps=fps,
                    loop=loop,
                    scale=scale_pixels
                )
            elif anim_type == "individual_frames":
                # Load from individual frame files
                frame_paths = animation_data["path"]  # List of paths
                animation = SpriteAnimation.from_individual_frames(
                    frame_paths=frame_paths,
                    fps=fps,
                    loop=loop,
                    scale=scale_pixels
                )
            else:
                print(f"⚠️ Unknown animation type: {anim_type}")
                return None
            
            # Play audio if specified
            audio_path = animation_data.get("audio_path")
            if audio_path and os.path.exists(audio_path):
                self.main_app.audio_manager.play_sound(audio_path, audio_type='video_audio')
            
            return animation
        
        except Exception as e:
            print(f"❌ Error loading sprite animation: {e}")
            return None
    
    # ==========================================================
    # VIDEO METHODS (Legacy - kept for backwards compatibility)
    # ==========================================================
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
                print(f"⌫ Error loading video {video_path}: {e}")
                return None
        return video_cache[video_path]
    
    def get_video_frame_surface(self, clip, current_time, video_data):
        """Fetches, converts, and scales a video frame with frame rate limiting."""
        try:
            current_real_time = time.time()
            if current_real_time < self.next_frame_time and self.last_rendered_video_frame_surface:
                return self.last_rendered_video_frame_surface
            
            self.next_frame_time = current_real_time + FRAME_INTERVAL
            
            frame_array = clip.get_frame(current_time)
            frame_surface = pygame.surfarray.make_surface(frame_array.swapaxes(0, 1))
            
            scale = video_data.get("scale", (1.0, 1.0))
            w, h = int(self.SCREEN_WIDTH * scale[0]), int(self.SCREEN_HEIGHT * scale[1])
            frame_surface = pygame.transform.smoothscale(frame_surface, (w, h))
            
            return frame_surface
        except Exception as e:
            print(f"⌫ Error getting video frame at {current_time:.2f}s: {e}")
            return None
    
    def render_slide(self, slide):
        """✅ UPDATED: Draws content based on slide type (supports animations + videos)."""
        # 1. Background
        if "background_image" in slide:
            bg_data = slide["background_image"]
            self.draw_centered_image(
                bg_data["path"],
                bg_data.get("scale", (1.0, 1.0)),
                bg_data.get("position", "top-left"),
            )
        
        # ✅ 2. NEW: Sprite Animation (preferred method)
        if "animation" in slide:
            animation_data = slide["animation"]
            
            # Initialize animation on first frame
            if self.current_animation is None and not self.animation_finished:
                self.current_animation = self.load_sprite_animation(animation_data)
                if self.current_animation:
                    self.current_animation.play()
                else:
                    self.animation_finished = True
            
            # Update and draw animation
            if self.current_animation and not self.animation_finished:
                # Update animation (pass delta time)
                dt = self.clock.get_time() / 1000.0  # Convert ms to seconds
                self.current_animation.update(dt)
                
                # Check if animation finished
                if self.current_animation.is_complete():
                    self.animation_finished = True
                    self.main_app.audio_manager.stop_all_sounds()
                
                # Draw animation
                position = animation_data.get("position", "center")
                if position == "center":
                    self.current_animation.draw_centered(self.screen, (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
                else:
                    # Custom positioning
                    rect = self.current_animation.get_rect()
                    if position == "top-left":
                        rect.topleft = (0, 0)
                    elif position == "bottom-right":
                        rect.bottomright = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                    self.current_animation.draw(self.screen, rect.topleft)
        
        # 3. Video (legacy support - use animations instead for better performance)
        elif "video" in slide:
            video_data = slide["video"]
            video_path = video_data["path"]
            audio_path = video_data.get("audio_path")
            
            if self.current_video_clip is None and not self.video_finished:
                self.current_video_clip = self.load_video_clip(video_path)
                if self.current_video_clip:
                    self.video_start_time = time.time()
                    self.last_rendered_video_frame_surface = None
                    self.next_frame_time = 0
                    
                    if audio_path and os.path.exists(audio_path):
                        self.main_app.audio_manager.play_sound(audio_path, audio_type='video_audio')
                else:
                    self.draw_arabic_text("Video not available", 0.05, (255, 0, 0), 
                                         (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
                    self.video_finished = True
            
            if self.current_video_clip and not self.video_finished:
                elapsed_video_time = (time.time() - self.video_start_time)
                
                if elapsed_video_time < self.current_video_clip.duration:
                    frame_surface = self.get_video_frame_surface(
                        self.current_video_clip, elapsed_video_time, video_data
                    )
                    if frame_surface:
                        self.last_rendered_video_frame_surface = frame_surface
                else:
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
                    self.main_app.audio_manager.stop_all_sounds()
            
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
        
        # 4. Foreground images (unchanged)
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
                    if not self.main_app.audio_manager.is_music_playing() or ("video" not in slide and "animation" not in slide):
                        self.play_sound(img_data["sound"])
                        img_data["_played"] = True
    
    def reset_slide_state(self):
        """✅ UPDATED: Reset state when changing slides."""
        self.stop_sounds()
        
        # Reset video state
        self.current_video_clip = None
        self.video_finished = False
        self.last_rendered_video_frame_surface = None
        
        # ✅ Reset animation state
        self.current_animation = None
        self.animation_finished = False
        
        self.start_time = time.time()
    
    def set_audio_context(self, slide):
        """✅ Set audio context using AudioManager."""
        if "animation" in slide:
            # Animation audio handled in load_sprite_animation
            pass
        elif "video" in slide:
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
        
        # Reset state when returning
        if "video" in current_slide_data:
            self.current_video_clip = None
            self.video_start_time = 0
            self.video_finished = False
            self.last_rendered_video_frame_surface = None
        
        if "animation" in current_slide_data:
            if self.current_animation:
                self.current_animation.reset()
        
        # Restore audio context
        self.main_app.audio_manager.pop_audio_context(restore=True)
    
    def handle_back_click(self):
        """Handle back button click."""
        self.stop_sounds()
        self.current_video_clip = None
        self.video_finished = False
        self.last_rendered_video_frame_surface = None
        self.current_animation = None
        self.animation_finished = False
        
        # Clear audio context
        self.main_app.audio_manager.set_context('bg_music', None)
        
        self.running = False
    
    # ==========================================================
    # MAIN LOOP
    # ==========================================================
    def run(self):
        """Main loop for slide presentation."""
        current_slide = self.slides[self.slide_index]
        self.set_audio_context(current_slide)
        self.start_time = time.time()
        
        while self.running:
            self.screen.fill((255, 255, 255))
            slide = self.slides[self.slide_index]
            
            # ✅ Check if animation or video is playing
            is_animation_slide = "animation" in slide
            is_animation_playing = is_animation_slide and self.current_animation is not None and not self.animation_finished
            
            is_video_slide = "video" in slide
            is_video_playing = is_video_slide and self.current_video_clip is not None and not self.video_finished
            
            is_media_playing = is_animation_playing or is_video_playing
            
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
            self.draw_navigation_buttons(is_media_playing)
            
            pygame.display.flip()
            
            # Event handling
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    cleanup_video_resources()
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(e.pos, is_media_playing)
            
            periodic_cache_cleanup()
            self.clock.tick(60)
        
        # Cleanup on exit
        self.stop_sounds()
        cleanup_video_resources()
        self.main_app.audio_manager.set_context('bg_music', None)
    
    def draw_navigation_buttons(self, is_media_playing):
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
    
    def handle_mouse_click(self, pos, is_media_playing):
        """✅ Handle mouse clicks using screen_helpers.confirm_popup."""
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
        elif hasattr(self, 'back_rect') and self.back_rect.collidepoint(pos):
            self.handle_back_click()


# ==========================================================
# NAVIGABLE VIDEO SLIDE PLAYER
# ==========================================================
class NavigableVideoSlidePlayer(VideoSlidePlayer):
    """✅ Extended player with Next/Prev navigation - SUPPORTS ANIMATIONS."""
    
    def draw_navigation_buttons(self, is_media_playing):
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
        
        next_color = (60, 120, 200) if not is_media_playing else (150, 150, 150)
        prev_color = (60, 120, 200) if not is_media_playing else (150, 150, 150)
        back_color = (200, 80, 80)
        
        pygame.draw.rect(self.screen, next_color, self.next_rect, border_radius=15)
        pygame.draw.rect(self.screen, prev_color, self.prev_rect, border_radius=15)
        pygame.draw.rect(self.screen, back_color, self.back_rect, border_radius=15)
        
        self.main_app.draw_arabic_text("Next", 0.035, (255, 255, 255), self.next_rect.center)
        self.main_app.draw_arabic_text("Prev", 0.035, (255, 255, 255), self.prev_rect.center)
        self.main_app.draw_arabic_text("Back", 0.035, (255, 255, 255), self.back_rect.center)
    
    def handle_mouse_click(self, pos, is_media_playing):
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
        elif self.next_rect.collidepoint(pos) and not is_media_playing:
            self.navigate_to_next_slide()
        elif self.prev_rect.collidepoint(pos) and not is_media_playing:
            self.navigate_to_prev_slide()
    
    def navigate_to_next_slide(self):
        """Navigate to the next slide."""
        if self.slide_index >= len(self.slides) - 1:
            print(f"ℹ️ Already at last slide ({self.slide_index + 1}/{len(self.slides)})")
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
        """✅ Mark topic complete WITHOUT checking rewards here"""
        if self.slide_index >= len(self.slides) - 1:
            profile_name = self.main_app.selected_profile.get("name") if self.main_app.selected_profile else None
            if profile_name and not hasattr(self, '_learning_recorded'):
                topic = getattr(self, 'topic', 'T1')
                mark_learning_topic_complete(profile_name, self.level, topic)
                self._learning_recorded = True
                print(f"✅ {profile_name} completed Learning Level {self.level} - Topic {topic}")
