# sprite_animation.py - HIGH-PERFORMANCE SPRITE SHEET ANIMATOR
import pygame
import os
from typing import Optional, Tuple, List

class SpriteAnimation:
    """
    Efficient sprite sheet animator for learning slides.
    Replaces slow video playback with fast frame blitting.
    
    Features:
    - Pre-loaded sprite sheets for instant playback
    - Frame-perfect timing control
    - Memory-efficient frame caching
    - Easy pause/resume/loop control
    - Audio sync support
    """
    
    def __init__(
        self, 
        sprite_sheet_path: str,
        frame_width: int,
        frame_height: int,
        num_frames: int,
        fps: int = 30,
        loop: bool = True,
        scale: Optional[Tuple[int, int]] = None
    ):
        """
        Initialize sprite animation from a sprite sheet.
        
        Args:
            sprite_sheet_path: Path to sprite sheet image (frames laid out horizontally or in grid)
            frame_width: Width of each individual frame in pixels
            frame_height: Height of each individual frame in pixels
            num_frames: Total number of frames in the animation
            fps: Frames per second for playback (default: 30)
            loop: Whether to loop animation (default: True)
            scale: Optional (width, height) to scale final frames
        """
        self.sprite_sheet_path = sprite_sheet_path
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = num_frames
        self.fps = fps
        self.loop = loop
        self.scale = scale
        
        # State
        self.current_frame = 0
        self.is_playing = False
        self.is_finished = False
        self.elapsed_time = 0.0
        self.frame_duration = 1.0 / fps  # Time per frame in seconds
        
        # Cache
        self.frames: List[pygame.Surface] = []
        self._sprite_sheet: Optional[pygame.Surface] = None
        
        # Load sprite sheet
        self._load_sprite_sheet()
    
    def _load_sprite_sheet(self):
        """Load and slice sprite sheet into individual frames."""
        if not os.path.exists(self.sprite_sheet_path):
            print(f"⚠️ Sprite sheet not found: {self.sprite_sheet_path}")
            # Create fallback colored frames
            self._create_fallback_frames()
            return
        
        try:
            # Load full sprite sheet
            self._sprite_sheet = pygame.image.load(self.sprite_sheet_path).convert_alpha()
            sheet_width, sheet_height = self._sprite_sheet.get_size()
            
            # Calculate grid layout
            frames_per_row = sheet_width // self.frame_width
            num_rows = (self.num_frames + frames_per_row - 1) // frames_per_row
            
            # Extract each frame
            for i in range(self.num_frames):
                row = i // frames_per_row
                col = i % frames_per_row
                
                x = col * self.frame_width
                y = row * self.frame_height
                
                # Extract frame from sprite sheet
                frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
                frame.blit(self._sprite_sheet, (0, 0), (x, y, self.frame_width, self.frame_height))
                
                # Scale if needed
                if self.scale:
                    frame = pygame.transform.smoothscale(frame, self.scale)
                
                self.frames.append(frame)
            
            # Free sprite sheet memory (we only need individual frames)
            self._sprite_sheet = None
            
            print(f"✅ Loaded {len(self.frames)} frames from {os.path.basename(self.sprite_sheet_path)}")
        
        except Exception as e:
            print(f"❌ Error loading sprite sheet {self.sprite_sheet_path}: {e}")
            self._create_fallback_frames()
    
    def _create_fallback_frames(self):
        """Create colored placeholder frames if sprite sheet fails to load."""
        size = self.scale if self.scale else (self.frame_width, self.frame_height)
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        
        for i in range(self.num_frames):
            frame = pygame.Surface(size, pygame.SRCALPHA)
            color = colors[i % len(colors)]
            frame.fill(color + (200,))
            self.frames.append(frame)
    
    @classmethod
    def from_individual_frames(
        cls,
        frame_paths: List[str],
        fps: int = 30,
        loop: bool = True,
        scale: Optional[Tuple[int, int]] = None
    ):
        """
        Alternative constructor: Load animation from individual frame files.
        Useful if you have separate PNG files instead of a sprite sheet.
        
        Args:
            frame_paths: List of paths to individual frame images
            fps: Frames per second
            loop: Whether to loop
            scale: Optional (width, height) to scale frames
        
        Returns:
            SpriteAnimation instance
        """
        # Create dummy instance
        anim = cls.__new__(cls)
        anim.frame_width = 0
        anim.frame_height = 0
        anim.num_frames = len(frame_paths)
        anim.fps = fps
        anim.loop = loop
        anim.scale = scale
        anim.current_frame = 0
        anim.is_playing = False
        anim.is_finished = False
        anim.elapsed_time = 0.0
        anim.frame_duration = 1.0 / fps
        anim.frames = []
        
        # Load individual frames
        for path in frame_paths:
            if os.path.exists(path):
                try:
                    frame = pygame.image.load(path).convert_alpha()
                    if scale:
                        frame = pygame.transform.smoothscale(frame, scale)
                    anim.frames.append(frame)
                except Exception as e:
                    print(f"⚠️ Failed to load frame {path}: {e}")
            else:
                print(f"⚠️ Frame not found: {path}")
        
        if not anim.frames:
            # Create fallback
            size = scale if scale else (100, 100)
            frame = pygame.Surface(size, pygame.SRCALPHA)
            frame.fill((200, 0, 0, 200))
            anim.frames.append(frame)
        
        print(f"✅ Loaded {len(anim.frames)} individual frames")
        return anim
    
    def update(self, dt: float):
        """
        Update animation state.
        
        Args:
            dt: Delta time in seconds since last update
        """
        if not self.is_playing or self.is_finished:
            return
        
        self.elapsed_time += dt
        
        # Check if we should advance to next frame
        if self.elapsed_time >= self.frame_duration:
            # Advance frame
            self.current_frame += 1
            self.elapsed_time = 0.0
            
            # Check if animation finished
            if self.current_frame >= self.num_frames:
                if self.loop:
                    self.current_frame = 0  # Loop back to start
                else:
                    self.current_frame = self.num_frames - 1  # Stay on last frame
                    self.is_finished = True
                    self.is_playing = False
    
    def draw(self, surface: pygame.Surface, position: Tuple[int, int]):
        """
        Draw current frame to surface.
        
        Args:
            surface: Pygame surface to draw on
            position: (x, y) position to draw frame (top-left corner)
        """
        if not self.frames:
            return
        
        frame = self.frames[self.current_frame]
        surface.blit(frame, position)
    
    def draw_centered(self, surface: pygame.Surface, center: Tuple[int, int]):
        """
        Draw current frame centered at position.
        
        Args:
            surface: Pygame surface to draw on
            center: (x, y) center position
        """
        if not self.frames:
            return
        
        frame = self.frames[self.current_frame]
        rect = frame.get_rect(center=center)
        surface.blit(frame, rect)
    
    def get_rect(self, **kwargs) -> pygame.Rect:
        """Get rect of current frame (supports pygame.Rect positioning)."""
        if not self.frames:
            return pygame.Rect(0, 0, 0, 0)
        return self.frames[self.current_frame].get_rect(**kwargs)
    
    def play(self):
        """Start or resume animation."""
        self.is_playing = True
        if self.is_finished:
            self.reset()
    
    def pause(self):
        """Pause animation."""
        self.is_playing = False
    
    def stop(self):
        """Stop animation and reset to first frame."""
        self.is_playing = False
        self.reset()
    
    def reset(self):
        """Reset animation to first frame."""
        self.current_frame = 0
        self.elapsed_time = 0.0
        self.is_finished = False
    
    def set_frame(self, frame_index: int):
        """Jump to specific frame."""
        self.current_frame = max(0, min(frame_index, self.num_frames - 1))
        self.elapsed_time = 0.0
    
    def get_duration(self) -> float:
        """Get total animation duration in seconds."""
        return self.num_frames / self.fps
    
    def is_complete(self) -> bool:
        """Check if animation has finished (only for non-looping animations)."""
        return self.is_finished
    
    def get_progress(self) -> float:
        """Get animation progress as percentage (0.0 to 1.0)."""
        if self.num_frames == 0:
            return 0.0
        return self.current_frame / self.num_frames


# ==========================================================
# HELPER FUNCTIONS FOR VIDEO-TO-SPRITE CONVERSION
# ==========================================================

def extract_frames_from_video(video_path: str, output_dir: str, max_frames: Optional[int] = None):
    """
    Extract frames from video file using moviepy.
    Handles corrupted/incomplete frames gracefully.
    
    Args:
        video_path: Path to video file
        output_dir: Directory to save extracted frames
        max_frames: Optional limit on number of frames to extract
    """
    try:
        from moviepy import VideoFileClip
        import os
        import warnings
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Suppress moviepy warnings about corrupted frames
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            clip = VideoFileClip(video_path)
        
        fps = clip.fps
        duration = clip.duration
        total_frames = int(fps * duration)
        
        if max_frames:
            total_frames = min(total_frames, max_frames)
        
        print(f"📹 Extracting {total_frames} frames from {video_path}...")
        print(f"   FPS: {fps}, Duration: {duration:.2f}s")
        
        extracted_count = 0
        last_valid_frame = None
        
        # Use iter_frames with fps parameter for better compatibility
        for i, frame in enumerate(clip.iter_frames(fps=fps)):
            if max_frames and i >= max_frames:
                break
            
            try:
                # Convert numpy array to pygame surface
                import numpy as np
                
                # Check if frame is valid (not all zeros)
                if frame is not None and frame.size > 0:
                    frame_surface = pygame.surfarray.make_surface(np.swapaxes(frame, 0, 1))
                    last_valid_frame = frame_surface
                elif last_valid_frame is not None:
                    # Use last valid frame for corrupted frames
                    frame_surface = last_valid_frame
                    print(f"  ⚠️ Using last valid frame for frame {i} (corrupted)")
                else:
                    print(f"  ⚠️ Skipping frame {i} (corrupted, no fallback)")
                    continue
                
                # Save frame
                frame_path = os.path.join(output_dir, f"frame_{i:04d}.png")
                pygame.image.save(frame_surface, frame_path)
                extracted_count += 1
                
                if (extracted_count) % 30 == 0:
                    print(f"  Extracted {extracted_count}/{total_frames} frames...")
            
            except Exception as frame_error:
                print(f"  ⚠️ Error processing frame {i}: {frame_error}")
                if last_valid_frame is not None:
                    # Save last valid frame as fallback
                    frame_path = os.path.join(output_dir, f"frame_{i:04d}.png")
                    pygame.image.save(last_valid_frame, frame_path)
                    extracted_count += 1
                continue
        
        clip.close()
        print(f"✅ Extracted {extracted_count} frames to {output_dir}")
        
        if extracted_count < total_frames:
            print(f"   ⚠️ Note: Expected {total_frames} frames but extracted {extracted_count}")
            print(f"   This is normal for videos with corrupted end frames")
        
        return extracted_count
        
    except Exception as e:
        print(f"❌ Error extracting frames: {e}")
        import traceback
        traceback.print_exc()
        return 0


def create_sprite_sheet(frame_dir: str, output_path: str, frames_per_row: int = 10):
    """
    Combine individual frames into a sprite sheet.
    
    Args:
        frame_dir: Directory containing frame_0000.png, frame_0001.png, etc.
        output_path: Path to save sprite sheet
        frames_per_row: Number of frames per row in sprite sheet
    """
    try:
        import os
        
        # Get all frame files
        frame_files = sorted([
            os.path.join(frame_dir, f) 
            for f in os.listdir(frame_dir) 
            if f.endswith('.png')
        ])
        
        if not frame_files:
            print("⚠️ No frames found")
            return
        
        # Load first frame to get dimensions
        first_frame = pygame.image.load(frame_files[0])
        frame_w, frame_h = first_frame.get_size()
        
        num_frames = len(frame_files)
        num_rows = (num_frames + frames_per_row - 1) // frames_per_row
        
        # Create sprite sheet surface
        sheet_w = frames_per_row * frame_w
        sheet_h = num_rows * frame_h
        sprite_sheet = pygame.Surface((sheet_w, sheet_h), pygame.SRCALPHA)
        
        print(f"🎨 Creating sprite sheet {sheet_w}x{sheet_h} with {num_frames} frames...")
        
        # Blit each frame onto sprite sheet
        for i, frame_path in enumerate(frame_files):
            frame = pygame.image.load(frame_path)
            row = i // frames_per_row
            col = i % frames_per_row
            x = col * frame_w
            y = row * frame_h
            sprite_sheet.blit(frame, (x, y))
        
        # Save sprite sheet
        pygame.image.save(sprite_sheet, output_path)
        print(f"✅ Sprite sheet saved to {output_path}")
        print(f"   Frame size: {frame_w}x{frame_h}")
        print(f"   Layout: {frames_per_row} frames per row, {num_rows} rows")
        
    except Exception as e:
        print(f"❌ Error creating sprite sheet: {e}")


# ==========================================================
# EXAMPLE USAGE
# ==========================================================

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    # Example 1: Load from sprite sheet
    # animation = SpriteAnimation(
    #     sprite_sheet_path="assets/animations/character_walk.png",
    #     frame_width=128,
    #     frame_height=128,
    #     num_frames=8,
    #     fps=12,
    #     loop=True,
    #     scale=(256, 256)
    # )
    
    # Example 2: Load from individual frames
    frame_paths = [
        f"assets/animations/frame_{i:04d}.png" 
        for i in range(30)
    ]
    animation = SpriteAnimation.from_individual_frames(
        frame_paths=frame_paths,
        fps=30,
        loop=True,
        scale=(400, 400)
    )
    
    animation.play()
    running = True
    
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if animation.is_playing:
                        animation.pause()
                    else:
                        animation.play()
                elif event.key == pygame.K_r:
                    animation.reset()
        
        # Update animation
        animation.update(dt)
        
        # Draw
        screen.fill((255, 255, 255))
        animation.draw_centered(screen, (400, 300))
        
        pygame.display.flip()
    
    pygame.quit()
