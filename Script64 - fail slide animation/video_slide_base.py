# video_slide_base.py - ENHANCED WITH SLIDE TRANSITIONS AND IMAGE ANIMATIONS
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

# ==========================================================
# CONSTANTS
# ==========================================================
VIDEO_FPS = 30
FRAME_INTERVAL = 1.0 / VIDEO_FPS
VIDEO_CACHE_CLEANUP_INTERVAL = 300

# ✅ NEW: Animation constants
SLIDE_TRANSITION_DURATION = 300  # milliseconds
IMAGE_FADE_DURATION = 300  # milliseconds for fade in/out
IMAGE_SCALE_DURATION = 100  # milliseconds for scale animation

# ==========================================================
# GLOBAL VIDEO CACHE
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
# ✅ NEW: ANIMATION HELPER FUNCTIONS
# ==========================================================
def ease_in_out_cubic(t):
    """Smooth cubic easing function (0 to 1)"""
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - pow(-2 * t + 2, 3) / 2

def ease_out_bounce(t):
    """Bounce easing for playful animations"""
    n1 = 7.5625
    d1 = 2.75
    
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375

def ease_out_elastic(t):
    """Elastic easing for spring-like effect"""
    if t == 0 or t == 1:
        return t
    
    c4 = (2 * 3.14159) / 3
    return pow(2, -10 * t) * (2.71828 ** (10 * t - 10.75) * 
           (10.75 * c4 - 6.28318)) / c4 + 1

# ==========================================================
# VIDEO SLIDE PLAYER BASE CLASS
# ==========================================================
class VideoSlidePlayer:
    """
    Base class for video slide presentations with transitions and animations.
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
        
        # Video state
        self.current_video_clip = None
        self.video_start_time = 0
        self.video_finished = False
        self.last_rendered_video_frame_surface = None
        self.next_frame_time = 0
        
        # ✅ NEW: Transition state
        self.transitioning = False
        self.transition_start_time = 0
        self.transition_direction = 1  # 1 for forward, -1 for backward
        self.previous_slide_surface = None
        self.transition_type = "slide"  # "slide", "fade", "zoom"
        
        # ✅ NEW: Image animation state
        self.image_animations = {}  # Track animation state for each image
        
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
    
    def draw_centered_image(self, img_path, scale, position="center", offset=None, 
                          alpha=255, scale_factor=1.0):
        """
        ✅ ENHANCED: Draw an image with animations support
        
        Args:
            alpha: Transparency (0-255) for fade effects
            scale_factor: Additional scaling for zoom/bounce effects
        """
        try:
            if not os.path.exists(img_path):
                raise FileNotFoundError(f"Image not found: {img_path}")
            
            img = pygame.image.load(img_path).convert_alpha()
            
            # Apply base scale
            w, h = int(self.SCREEN_WIDTH * scale[0]), int(self.SCREEN_HEIGHT * scale[1])
            
            # Apply animation scale factor
            w = int(w * scale_factor)
            h = int(h * scale_factor)
            
            img = pygame.transform.smoothscale(img, (w, h))
            
            # Apply alpha
            if alpha < 255:
                img.set_alpha(alpha)
            
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
            
            # Apply offset if provided
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
    # ✅ NEW: ANIMATION CALCULATION METHODS
    # ==========================================================
    def get_image_animation_state(self, img_data, elapsed):
        """
        Calculate animation state for an image based on elapsed time.
        
        Returns: dict with alpha, scale_factor, and visibility
        """
        delay = img_data.get("delay", 0)
        duration = img_data.get("duration", None)
        animation = img_data.get("animation", "fade")  # "fade", "scale", "bounce", "slide"
        
        # Check if image should be visible
        if elapsed < delay:
            return {"visible": False, "alpha": 0, "scale_factor": 0.0}
        
        if duration is not None and elapsed > delay + duration:
            # Fade out animation
            fade_out_progress = min(1.0, (elapsed - (delay + duration)) / IMAGE_FADE_DURATION)
            alpha = int(255 * (1 - ease_in_out_cubic(fade_out_progress)))
            
            if alpha <= 0:
                return {"visible": False, "alpha": 0, "scale_factor": 1.0}
            
            return {"visible": True, "alpha": alpha, "scale_factor": 1.0}
        
        # Fade in animation
        time_since_appear = elapsed - delay
        
        if animation == "fade":
            # Simple fade in
            fade_progress = min(1.0, time_since_appear / IMAGE_FADE_DURATION)
            alpha = int(255 * ease_in_out_cubic(fade_progress))
            return {"visible": True, "alpha": alpha, "scale_factor": 1.0}
        
        elif animation == "scale":
            # Scale up from 0 to 1
            scale_progress = min(1.0, time_since_appear / IMAGE_SCALE_DURATION)
            scale_factor = ease_out_bounce(scale_progress)
            alpha = 255
            return {"visible": True, "alpha": alpha, "scale_factor": scale_factor}
        
        elif animation == "bounce":
            # Bounce in with elastic effect
            bounce_progress = min(1.0, time_since_appear / IMAGE_SCALE_DURATION)
            scale_factor = ease_out_elastic(bounce_progress)
            alpha = int(255 * min(1.0, bounce_progress * 2))  # Fade in quickly
            return {"visible": True, "alpha": alpha, "scale_factor": scale_factor}
        
        elif animation == "slide":
            # Slide in from side
            slide_progress = min(1.0, time_since_appear / IMAGE_SCALE_DURATION)
            alpha = int(255 * ease_in_out_cubic(slide_progress))
            return {"visible": True, "alpha": alpha, "scale_factor": 1.0}
        
        # Default: fully visible
        return {"visible": True, "alpha": 255, "scale_factor": 1.0}
    
    # ==========================================================
    # ✅ NEW: SLIDE TRANSITION METHODS
    # ==========================================================
    def capture_current_slide(self):
        """Capture current slide as a surface for transition"""
        # Create a new surface and render the current slide to it
        surf = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        # Render the current slide to the surface
        old_screen = self.screen
        self.screen = surf
        
        # Fill with white background first
        self.screen.fill((255, 255, 255))
        
        # Render current slide content
        slide = self.slides[self.slide_index]
        self.render_slide(slide)
        
        # Draw title
        self.draw_arabic_text(
            slide["title"],
            0.06,
            (0, 0, 0),
            (self.SCREEN_WIDTH // 2, int(self.SCREEN_HEIGHT * 0.07)),
            bold=True
        )
        
        # Restore original screen
        self.screen = old_screen
        
        return surf
    
    def draw_slide_transition(self, progress):
        """
        Draw transition between slides
        
        Args:
            progress: 0.0 to 1.0, how far along the transition
        """
        # Apply easing
        eased_progress = ease_in_out_cubic(progress)
        
        if self.transition_type == "slide":
            # Slide transition - old slide moves out, new slide moves in
            offset = int(self.SCREEN_WIDTH * eased_progress * self.transition_direction)
            
            # Fill background with white first
            self.screen.fill((255, 255, 255))
            
            # Draw old slide moving out
            if self.previous_slide_surface:
                if self.transition_direction == 1:
                    # Moving forward: old slide moves left
                    self.screen.blit(self.previous_slide_surface, (-offset, 0))
                else:
                    # Moving backward: old slide moves right
                    self.screen.blit(self.previous_slide_surface, (offset, 0))
            
            # Render new slide to temp surface
            temp_surf = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            temp_surf.fill((255, 255, 255))
            old_screen = self.screen
            self.screen = temp_surf
            
            slide = self.slides[self.slide_index]
            self.render_slide(slide)
            
            # Draw title on new slide
            self.draw_arabic_text(
                slide["title"],
                0.06,
                (0, 0, 0),
                (self.SCREEN_WIDTH // 2, int(self.SCREEN_HEIGHT * 0.07)),
                bold=True
            )
            
            self.screen = old_screen
            
            # Draw new slide moving in
            if self.transition_direction == 1:
                # Moving forward: new slide comes from right
                self.screen.blit(temp_surf, (self.SCREEN_WIDTH - offset, 0))
            else:
                # Moving backward: new slide comes from left
                self.screen.blit(temp_surf, (-self.SCREEN_WIDTH + offset, 0))
        
        elif self.transition_type == "fade":
            # Fade transition
            self.screen.fill((255, 255, 255))
            
            if self.previous_slide_surface:
                # Draw old slide with fading alpha
                old_alpha = int(255 * (1 - eased_progress))
                old_surf = self.previous_slide_surface.copy()
                old_surf.set_alpha(old_alpha)
                self.screen.blit(old_surf, (0, 0))
            
            # Render new slide with increasing alpha
            temp_surf = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            temp_surf.fill((255, 255, 255))
            old_screen = self.screen
            self.screen = temp_surf
            
            slide = self.slides[self.slide_index]
            self.render_slide(slide)
            
            # Draw title on new slide
            self.draw_arabic_text(
                slide["title"],
                0.06,
                (0, 0, 0),
                (self.SCREEN_WIDTH // 2, int(self.SCREEN_HEIGHT * 0.07)),
                bold=True
            )
            
            self.screen = old_screen
            
            # Blend new slide on top with alpha
            new_alpha = int(255 * eased_progress)
            temp_surf.set_alpha(new_alpha)
            self.screen.blit(temp_surf, (0, 0))
        
        elif self.transition_type == "zoom":
            # Zoom transition - old zooms out, new zooms in
            self.screen.fill((255, 255, 255))
            
            if self.previous_slide_surface:
                # Old slide zooms out and fades
                old_scale = 1.0 + (eased_progress * 0.5)
                old_alpha = int(255 * (1 - eased_progress))
                
                old_w = int(self.SCREEN_WIDTH * old_scale)
                old_h = int(self.SCREEN_HEIGHT * old_scale)
                
                try:
                    scaled_old = pygame.transform.smoothscale(self.previous_slide_surface, (old_w, old_h))
                    scaled_old.set_alpha(old_alpha)
                    
                    offset_x = (self.SCREEN_WIDTH - old_w) // 2
                    offset_y = (self.SCREEN_HEIGHT - old_h) // 2
                    self.screen.blit(scaled_old, (offset_x, offset_y))
                except:
                    pass
            
            # Render new slide
            temp_surf = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            temp_surf.fill((255, 255, 255))
            old_screen = self.screen
            self.screen = temp_surf
            
            slide = self.slides[self.slide_index]
            self.render_slide(slide)
            
            # Draw title on new slide
            self.draw_arabic_text(
                slide["title"],
                0.06,
                (0, 0, 0),
                (self.SCREEN_WIDTH // 2, int(self.SCREEN_HEIGHT * 0.07)),
                bold=True
            )
            
            self.screen = old_screen
            
            # New slide zooms in
            new_scale = 0.5 + (eased_progress * 0.5)
            new_alpha = int(255 * eased_progress)
            
            new_w = int(self.SCREEN_WIDTH * new_scale)
            new_h = int(self.SCREEN_HEIGHT * new_scale)
            
            try:
                scaled_new = pygame.transform.smoothscale(temp_surf, (new_w, new_h))
                scaled_new.set_alpha(new_alpha)
                
                offset_x = (self.SCREEN_WIDTH - new_w) // 2
                offset_y = (self.SCREEN_HEIGHT - new_h) // 2
                self.screen.blit(scaled_new, (offset_x, offset_y))
            except:
                pass
    
    # ==========================================================
    # VIDEO METHODS
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
                print(f"❌ Error loading video {video_path}: {e}")
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
            print(f"❌ Error getting video frame at {current_time:.2f}s: {e}")
            return None
    
    def render_slide(self, slide):
        """✅ ENHANCED: Draws content with animations"""
        # 1. Background
        if "background_image" in slide:
            bg_data = slide["background_image"]
            self.draw_centered_image(
                bg_data["path"],
                bg_data.get("scale", (1.0, 1.0)),
                bg_data.get("position", "top-left"),
            )
        
        # 2. Video (no animation for video)
        if "video" in slide:
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
                        print("⚠️ No audio file specified for video slide.")
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
        
        # ✅ 3. Foreground images with ANIMATIONS
        if "images" in slide:
            elapsed = (time.time() - self.start_time) * 1000
            
            for img_data in slide["images"]:
                # Get animation state
                anim_state = self.get_image_animation_state(img_data, elapsed)
                
                if not anim_state["visible"]:
                    continue
                
                # Draw image with animation properties
                self.draw_centered_image(
                    img_data["path"],
                    img_data.get("scale", (0.3, 0.3)),
                    img_data.get("position", "center"),
                    img_data.get("offset", None),
                    alpha=anim_state["alpha"],
                    scale_factor=anim_state["scale_factor"]
                )
                
                # Play sound on first appearance
                delay = img_data.get("delay", 0)
                if not img_data.get("_played", False) and elapsed >= delay and "sound" in img_data:
                    if not self.main_app.audio_manager.is_music_playing() or "video" not in slide:
                        self.play_sound(img_data["sound"])
                        img_data["_played"] = True
    
    def reset_slide_state(self):
        """Reset state when changing slides."""
        self.stop_sounds()
        self.current_video_clip = None
        self.video_finished = False
        self.last_rendered_video_frame_surface = None
        self.start_time = time.time()
        self.image_animations = {}
    
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
        
        self.main_app.audio_manager.push_audio_context()
        self.stop_sounds()
        self.main_app.open_profile_manager()
        
        if "video" in current_slide_data:
            self.current_video_clip = None
            self.video_start_time = 0
            self.video_finished = False
            self.last_rendered_video_frame_surface = None
        
        self.main_app.audio_manager.pop_audio_context(restore=True)
    
    def handle_back_click(self):
        """Handle back button click."""
        self.stop_sounds()
        self.current_video_clip = None
        self.video_finished = False
        self.last_rendered_video_frame_surface = None
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
            
            is_video_slide = "video" in slide
            is_video_playing = is_video_slide and self.current_video_clip is not None and not self.video_finished
            
            # ✅ Handle transition rendering
            if self.transitioning:
                transition_elapsed = pygame.time.get_ticks() - self.transition_start_time
                progress = min(1.0, transition_elapsed / SLIDE_TRANSITION_DURATION)
                
                self.draw_slide_transition(progress)
                
                if progress >= 1.0:
                    self.transitioning = False
                    self.previous_slide_surface = None
            else:
                # Normal slide rendering
                self.render_slide(slide)
            
            # Title (always on top)
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
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(e.pos, is_video_playing)
            
            periodic_cache_cleanup()
            self.clock.tick(60)
        
        # Cleanup on exit
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
    """✅ Extended player with Next/Prev navigation and transitions."""
    
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
        """✅ Navigate to the next slide with transition."""
        if self.slide_index >= len(self.slides) - 1:
            print(f"ℹ️ Already at last slide ({self.slide_index + 1}/{len(self.slides)})")
            self.check_and_mark_completion()
            return
        
        print(f"➡️ Moving from slide {self.slide_index + 1} to {self.slide_index + 2}")
        
        # ✅ Start transition
        self.previous_slide_surface = self.capture_current_slide()
        self.transitioning = True
        self.transition_start_time = pygame.time.get_ticks()
        self.transition_direction = 1
        self.transition_type = "slide"  # Can be "slide", "fade", or "zoom"
        
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
        """✅ Navigate to the previous slide with transition."""
        if self.slide_index <= 0:
            print(f"ℹ️ Already at first slide")
            return
        
        print(f"⬅️ Moving from slide {self.slide_index + 1} to {self.slide_index}")
        
        # ✅ Start transition
        self.previous_slide_surface = self.capture_current_slide()
        self.transitioning = True
        self.transition_start_time = pygame.time.get_ticks()
        self.transition_direction = -1
        self.transition_type = "slide"  # Can be "slide", "fade", or "zoom"
        
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
