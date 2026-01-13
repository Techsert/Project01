#!/usr/bin/env python3
# test_sprite_animation.py - Test if sprite animation works correctly
"""
This script tests if your sprite sheet animates properly.
Run this BEFORE using it in your main app.

Usage:
    python test_sprite_animation.py
"""

import pygame
import sys
from sprite_animation import SpriteAnimation

def test_sprite_animation():
    """Test sprite animation playback."""
    pygame.init()
    
    # Create test window
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Sprite Animation Test")
    clock = pygame.time.Clock()
    
    print("="*70)
    print("SPRITE ANIMATION TEST")
    print("="*70)
    
    # Get sprite sheet info from user
    sprite_path = input("\nEnter sprite sheet path: ").strip()
    if not sprite_path:
        sprite_path = "../assets/animations/Lvl1_Topic1_slide1.png"
        print(f"Using default: {sprite_path}")
    
    frame_width = int(input("Enter frame width (e.g., 550): ").strip() or "550")
    frame_height = int(input("Enter frame height (e.g., 700): ").strip() or "700")
    num_frames = int(input("Enter number of frames (e.g., 1304): ").strip() or "1304")
    fps = int(input("Enter FPS (e.g., 30): ").strip() or "30")
    
    print(f"\n📋 Configuration:")
    print(f"   Path:        {sprite_path}")
    print(f"   Frame size:  {frame_width}x{frame_height}")
    print(f"   Frames:      {num_frames}")
    print(f"   FPS:         {fps}")
    print(f"\n🔄 Loading sprite animation...")
    
    try:
        # Create animation
        animation = SpriteAnimation(
            sprite_sheet_path=sprite_path,
            frame_width=frame_width,
            frame_height=frame_height,
            num_frames=num_frames,
            fps=fps,
            loop=True,
            scale=(400, 500)  # Scale to fit screen
        )
        
        print(f"✅ Animation loaded successfully!")
        print(f"   Total frames: {len(animation.frames)}")
        print(f"   Duration: {animation.get_duration():.2f} seconds")
        
        # Start animation
        animation.play()
        
        print(f"\n🎬 Playing animation...")
        print(f"   Press SPACE to pause/resume")
        print(f"   Press R to restart")
        print(f"   Press ESC to quit")
        
        running = True
        paused = False
        
        while running:
            dt = clock.tick(60) / 1000.0  # Delta time in seconds
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        if animation.is_playing:
                            animation.pause()
                            paused = True
                            print("⏸️  Paused")
                        else:
                            animation.play()
                            paused = False
                            print("▶️  Playing")
                    elif event.key == pygame.K_r:
                        animation.reset()
                        animation.play()
                        paused = False
                        print("🔄 Restarted")
            
            # Update animation
            animation.update(dt)
            
            # Draw
            screen.fill((50, 50, 50))
            
            # Draw animation centered
            animation.draw_centered(screen, (400, 300))
            
            # Draw info
            font = pygame.font.Font(None, 30)
            
            # Current frame info
            info_text = f"Frame: {animation.current_frame + 1}/{animation.num_frames}"
            text_surf = font.render(info_text, True, (255, 255, 255))
            screen.blit(text_surf, (10, 10))
            
            # Progress bar
            progress = animation.get_progress()
            bar_width = 300
            bar_height = 20
            bar_x = 10
            bar_y = 50
            
            # Background
            pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
            # Progress
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(bar_width * progress), bar_height))
            
            # Status
            status = "PAUSED" if paused else "PLAYING"
            status_color = (255, 255, 0) if paused else (0, 255, 0)
            status_surf = font.render(status, True, status_color)
            screen.blit(status_surf, (10, 80))
            
            pygame.display.flip()
        
        print(f"\n✅ Test complete!")
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: Sprite sheet not found!")
        print(f"   {e}")
        print(f"\nMake sure you've converted the video first:")
        print(f"   python smart_convert_video.py ../assets/testvideo/Lvl1_Topic1_slide1.mp4 --scale 0.5")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    pygame.quit()


if __name__ == "__main__":
    test_sprite_animation()
