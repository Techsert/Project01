#!/usr/bin/env python3
# smart_convert_video.py - Memory-optimized video to sprite sheet converter
"""
This script handles large videos efficiently by scaling frames during extraction.

Usage:
    python smart_convert_video.py <video_path> [--scale 0.5]

Example:
    python smart_convert_video.py ../assets/testvideo/Lvl1_Topic1_slide1.mp4 --scale 0.5
"""

import os
import sys
import pygame
import warnings
from pathlib import Path

def extract_frames_smart(video_path, output_dir, scale_factor=0.5, max_frames=None):
    """
    Smart frame extraction with automatic scaling to prevent memory issues.
    
    Args:
        video_path: Path to video
        output_dir: Where to save frames
        scale_factor: Scale frames (0.5 = 50% size, saves memory)
        max_frames: Optional frame limit
    
    Returns:
        (extracted_count, frame_width, frame_height, fps)
    """
    try:
        from moviepy import VideoFileClip
        import numpy as np
        
        os.makedirs(output_dir, exist_ok=True)
        pygame.init()
        
        print(f"\n📹 Loading video: {video_path}")
        
        # Suppress warnings
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            clip = VideoFileClip(video_path)
        
        fps = clip.fps
        duration = clip.duration
        original_size = clip.size
        total_expected = int(fps * duration)
        
        if max_frames:
            total_expected = min(total_expected, max_frames)
        
        # Calculate scaled size
        scaled_w = int(original_size[0] * scale_factor)
        scaled_h = int(original_size[1] * scale_factor)
        
        print(f"   Original size:   {original_size[0]}x{original_size[1]}")
        print(f"   Scaled size:     {scaled_w}x{scaled_h} ({scale_factor*100:.0f}%)")
        print(f"   FPS:             {fps}")
        print(f"   Duration:        {duration:.2f} seconds")
        print(f"   Expected frames: {total_expected}")
        
        # Estimate memory usage
        frames_per_row = 10
        num_rows = (total_expected + frames_per_row - 1) // frames_per_row
        sheet_w = frames_per_row * scaled_w
        sheet_h = num_rows * scaled_h
        memory_mb = (sheet_w * sheet_h * 4) / (1024 * 1024)
        
        print(f"\n📊 Sprite sheet estimate:")
        print(f"   Size:            {sheet_w}x{sheet_h}")
        print(f"   Memory needed:   ~{memory_mb:.0f} MB")
        
        if memory_mb > 500:
            print(f"   ⚠️ WARNING: Large sprite sheet! Consider using --scale 0.3 or 0.4")
        
        print(f"\n🔄 Extracting and scaling frames...")
        
        extracted_count = 0
        skipped_count = 0
        last_valid_frame_surface = None
        
        frame_index = 0
        for frame in clip.iter_frames(fps=fps):
            if max_frames and frame_index >= max_frames:
                break
            
            try:
                # Validate frame
                if frame is None or frame.size == 0:
                    if last_valid_frame_surface:
                        frame_surface = last_valid_frame_surface
                    else:
                        skipped_count += 1
                        frame_index += 1
                        continue
                else:
                    # Convert to pygame surface
                    frame_surface = pygame.surfarray.make_surface(np.swapaxes(frame, 0, 1))
                    
                    # Scale down to save memory
                    if scale_factor != 1.0:
                        frame_surface = pygame.transform.smoothscale(frame_surface, (scaled_w, scaled_h))
                    
                    last_valid_frame_surface = frame_surface
                
                # Save frame
                frame_path = os.path.join(output_dir, f"frame_{frame_index:04d}.png")
                pygame.image.save(frame_surface, frame_path)
                extracted_count += 1
                
                # Progress update
                if extracted_count % 50 == 0:
                    progress = (extracted_count / total_expected) * 100
                    print(f"   Progress: {extracted_count}/{total_expected} ({progress:.1f}%)")
            
            except Exception as e:
                print(f"   ⚠️ Frame {frame_index}: Error - {e}")
                if last_valid_frame_surface:
                    try:
                        frame_path = os.path.join(output_dir, f"frame_{frame_index:04d}.png")
                        pygame.image.save(last_valid_frame_surface, frame_path)
                        extracted_count += 1
                    except:
                        skipped_count += 1
                else:
                    skipped_count += 1
            
            frame_index += 1
        
        clip.close()
        
        print(f"\n✅ Frame extraction complete:")
        print(f"   Extracted:       {extracted_count} frames")
        print(f"   Skipped/Failed:  {skipped_count} frames")
        print(f"   Success rate:    {(extracted_count/total_expected)*100:.1f}%")
        
        return extracted_count, scaled_w, scaled_h, fps
    
    except Exception as e:
        print(f"\n❌ Fatal error during extraction: {e}")
        import traceback
        traceback.print_exc()
        return 0, 0, 0, 0


def create_sprite_sheet_chunked(frames_dir, output_path, frames_per_row=10):
    """
    Create sprite sheet with chunked processing to avoid memory issues.
    """
    try:
        # Get all frame files
        frame_files = sorted([
            os.path.join(frames_dir, f) 
            for f in os.listdir(frames_dir) 
            if f.endswith('.png') and f.startswith('frame_')
        ])
        
        if not frame_files:
            print("❌ No valid frame files found")
            return False, 0, 0
        
        print(f"\n🎨 Creating sprite sheet from {len(frame_files)} frames...")
        
        # Load first frame to get dimensions
        first_frame = pygame.image.load(frame_files[0])
        frame_w, frame_h = first_frame.get_size()
        print(f"   Frame size:      {frame_w}x{frame_h}")
        
        num_frames = len(frame_files)
        num_rows = (num_frames + frames_per_row - 1) // frames_per_row
        
        # Create sprite sheet surface
        sheet_w = frames_per_row * frame_w
        sheet_h = num_rows * frame_h
        
        # Check if size is reasonable
        memory_needed = (sheet_w * sheet_h * 4) / (1024 * 1024)
        print(f"   Sheet size:      {sheet_w}x{sheet_h}")
        print(f"   Layout:          {frames_per_row} frames/row × {num_rows} rows")
        print(f"   Memory needed:   ~{memory_needed:.0f} MB")
        
        if memory_needed > 1000:
            print(f"\n❌ ERROR: Sprite sheet too large ({memory_needed:.0f} MB)")
            print(f"   Try using a smaller --scale value (e.g., 0.3 or 0.4)")
            return False, frame_w, frame_h
        
        sprite_sheet = pygame.Surface((sheet_w, sheet_h), pygame.SRCALPHA)
        
        print(f"\n   Building sprite sheet...")
        
        # Blit frames in chunks to show progress
        for i, frame_path in enumerate(frame_files):
            try:
                frame = pygame.image.load(frame_path)
                row = i // frames_per_row
                col = i % frames_per_row
                x = col * frame_w
                y = row * frame_h
                sprite_sheet.blit(frame, (x, y))
                
                if (i + 1) % 100 == 0:
                    progress = ((i + 1) / num_frames) * 100
                    print(f"   Progress: {i+1}/{num_frames} ({progress:.1f}%)")
            except Exception as e:
                print(f"   ⚠️ Error loading frame {i}: {e}")
                continue
        
        # Save sprite sheet
        print(f"\n   Saving sprite sheet (this may take a moment)...")
        pygame.image.save(sprite_sheet, output_path)
        file_size = os.path.getsize(output_path) / (1024 * 1024)
        
        print(f"\n✅ Sprite sheet saved:")
        print(f"   Path:            {output_path}")
        print(f"   File size:       {file_size:.2f} MB")
        
        return True, frame_w, frame_h
    
    except Exception as e:
        print(f"\n❌ Error creating sprite sheet: {e}")
        import traceback
        traceback.print_exc()
        return False, 0, 0


def main():
    """Main conversion function with smart scaling."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert video to sprite sheet (memory optimized)')
    parser.add_argument('video_path', help='Path to video file')
    parser.add_argument('--scale', type=float, default=0.5, help='Scale factor (default: 0.5 = 50%%)')
    parser.add_argument('--max-frames', type=int, default=None, help='Limit number of frames')
    parser.add_argument('--frames-per-row', type=int, default=10, help='Frames per row in sprite sheet')
    
    args = parser.parse_args()
    
    video_path = args.video_path
    scale_factor = args.scale
    
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        sys.exit(1)
    
    # Setup paths
    video_name = Path(video_path).stem
    output_dir = Path("../assets/animations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    frames_dir = output_dir / f"{video_name}_frames"
    sprite_sheet_path = output_dir / f"{video_name}.png"
    
    print("="*70)
    print("SMART VIDEO TO SPRITE SHEET CONVERTER")
    print("="*70)
    print(f"\nInput video:     {video_path}")
    print(f"Output location: {sprite_sheet_path}")
    print(f"Scale factor:    {scale_factor} ({scale_factor*100:.0f}%)")
    
    # Step 1: Extract frames with scaling
    print("\n" + "="*70)
    print("STEP 1: EXTRACT AND SCALE FRAMES")
    print("="*70)
    
    num_frames, frame_w, frame_h, fps = extract_frames_smart(
        video_path, 
        str(frames_dir), 
        scale_factor=scale_factor,
        max_frames=args.max_frames
    )
    
    if num_frames == 0:
        print("\n❌ Frame extraction failed.")
        sys.exit(1)
    
    # Step 2: Create sprite sheet
    print("\n" + "="*70)
    print("STEP 2: CREATE SPRITE SHEET")
    print("="*70)
    
    success, final_w, final_h = create_sprite_sheet_chunked(
        str(frames_dir), 
        str(sprite_sheet_path),
        frames_per_row=args.frames_per_row
    )
    
    if not success:
        print("\n❌ Sprite sheet creation failed.")
        sys.exit(1)
    
    # Step 3: Cleanup
    print("\n" + "="*70)
    print("STEP 3: CLEANUP")
    print("="*70)
    
    response = input(f"\nDelete temporary frames? (y/n): ").strip().lower()
    if response == 'y':
        import shutil
        try:
            shutil.rmtree(frames_dir)
            print("✅ Temporary frames deleted")
        except Exception as e:
            print(f"⚠️ Could not delete frames: {e}")
    else:
        print("ℹ️ Temporary frames kept at:", frames_dir)
    
    # Step 4: Show usage
    print("\n" + "="*70)
    print("CONVERSION COMPLETE!")
    print("="*70)
    print(f"\n✅ Sprite sheet saved to: {sprite_sheet_path}")
    print(f"\n📋 Use this in your slide data:")
    print(f"""
"animation": {{
    "type": "sprite_sheet",
    "path": "{sprite_sheet_path.as_posix()}",
    "frame_width": {final_w},
    "frame_height": {final_h},
    "num_frames": {num_frames},
    "fps": {int(fps)},
    "loop": False,
    "scale": (0.3, 0.5),  # Adjust to fit your screen
    "position": "center",
    "audio_path": "../assets/sounds/Learn_lvl1_T1/lvl1_topic1_Slide1.wav"
}}
    """)
    print("="*70)


if __name__ == "__main__":
    main()
