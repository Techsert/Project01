#!/usr/bin/env python3
# convert_videos_to_sprites.py - Batch convert all videos to sprite sheets
"""
This script converts all your video files to sprite sheets for faster playback.

Usage:
    python convert_videos_to_sprites.py

What it does:
    1. Scans ../assets/videos/ for all .mp4 files
    2. Extracts frames from each video
    3. Creates optimized sprite sheets
    4. Saves to ../assets/animations/
"""

import os
import pygame
from sprite_animation import extract_frames_from_video, create_sprite_sheet
from pathlib import Path

# ==========================================================
# CONFIGURATION
# ==========================================================
VIDEO_DIR = "../assets/testvideo"
OUTPUT_DIR = "../assets/animations"
FRAMES_PER_ROW = 10  # How many frames per row in sprite sheet
MAX_FRAMES = None  # Set to a number to limit frames (e.g., 60 for 2 seconds at 30fps)

# ==========================================================
# CONVERSION FUNCTION
# ==========================================================
def convert_all_videos():
    """Convert all videos in VIDEO_DIR to sprite sheets."""
    pygame.init()
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Find all video files
    video_files = []
    for ext in ['*.mp4', '*.avi', '*.mov', '*.mkv']:
        video_files.extend(Path(VIDEO_DIR).glob(ext))
    
    if not video_files:
        print(f"⚠️ No video files found in {VIDEO_DIR}")
        return
    
    print(f"📹 Found {len(video_files)} video(s) to convert\n")
    
    # Convert each video
    for i, video_path in enumerate(video_files, 1):
        video_name = video_path.stem  # Filename without extension
        print(f"\n{'='*60}")
        print(f"[{i}/{len(video_files)}] Converting: {video_name}")
        print(f"{'='*60}")
        
        try:
            # Create temp directory for frames
            frames_dir = os.path.join(OUTPUT_DIR, f"{video_name}_frames")
            os.makedirs(frames_dir, exist_ok=True)
            
            # Extract frames
            print(f"\n1️⃣ Extracting frames from {video_path.name}...")
            num_frames = extract_frames_from_video(str(video_path), frames_dir, max_frames=MAX_FRAMES)
            
            if num_frames == 0:
                print(f"   ❌ No frames extracted, skipping sprite sheet creation")
                continue
            
            # Create sprite sheet
            sprite_sheet_path = os.path.join(OUTPUT_DIR, f"{video_name}.png")
            print(f"\n2️⃣ Creating sprite sheet from {num_frames} frames...")
            create_sprite_sheet(frames_dir, sprite_sheet_path, frames_per_row=FRAMES_PER_ROW)
            
            # Optional: Delete frames folder to save space
            print(f"\n3️⃣ Cleaning up temporary frames...")
            import shutil
            try:
                shutil.rmtree(frames_dir)
                print(f"   ✅ Deleted temporary frames")
            except Exception as e:
                print(f"   ⚠️ Could not delete frames: {e}")
            
            print(f"\n✅ SUCCESS: {video_name}.png created")
            
        except Exception as e:
            print(f"\n❌ ERROR converting {video_name}: {e}")
            continue
    
    print(f"\n{'='*60}")
    print(f"🎉 Conversion complete!")
    print(f"{'='*60}")
    print(f"\nSprite sheets saved to: {OUTPUT_DIR}")
    print(f"\nNext steps:")
    print(f"  1. Update your slide data to use 'animation' instead of 'video'")
    print(f"  2. Test the new sprite animations")
    print(f"  3. Delete old video files to save space (optional)")


# ==========================================================
# ANALYZE VIDEO FUNCTION
# ==========================================================
def analyze_video(video_path):
    """Analyze a video file and print its properties."""
    try:
        from moviepy import VideoFileClip
        
        print(f"\n📊 Analyzing: {video_path}")
        print(f"{'='*60}")
        
        clip = VideoFileClip(video_path)
        
        print(f"Duration:     {clip.duration:.2f} seconds")
        print(f"FPS:          {clip.fps}")
        print(f"Resolution:   {clip.size[0]} x {clip.size[1]}")
        print(f"Total frames: {int(clip.fps * clip.duration)}")
        print(f"Has audio:    {clip.audio is not None}")
        
        # Estimate sprite sheet size
        num_frames = int(clip.fps * clip.duration)
        frame_w, frame_h = clip.size
        rows = (num_frames + FRAMES_PER_ROW - 1) // FRAMES_PER_ROW
        sheet_w = FRAMES_PER_ROW * frame_w
        sheet_h = rows * frame_h
        
        print(f"\nSprite sheet estimate:")
        print(f"  Size:       {sheet_w} x {sheet_h} pixels")
        print(f"  Layout:     {FRAMES_PER_ROW} frames/row, {rows} rows")
        print(f"  File size:  ~{(sheet_w * sheet_h * 4) / (1024*1024):.1f} MB (uncompressed)")
        
        clip.close()
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"❌ Error analyzing video: {e}")


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    import sys
    
    print("="*60)
    print("VIDEO TO SPRITE SHEET CONVERTER")
    print("="*60)
    
    # Check if specific video analysis requested
    if len(sys.argv) > 1:
        if sys.argv[1] == "--analyze":
            # Analyze all videos
            video_files = list(Path(VIDEO_DIR).glob("*.mp4"))
            for video in video_files:
                analyze_video(str(video))
        else:
            # Analyze specific video
            analyze_video(sys.argv[1])
    else:
        # Convert all videos
        print(f"\nInput directory:  {VIDEO_DIR}")
        print(f"Output directory: {OUTPUT_DIR}")
        print(f"\nThis will convert all .mp4 files to sprite sheets.")
        
        response = input("\nContinue? (y/n): ").strip().lower()
        if response == 'y':
            convert_all_videos()
        else:
            print("❌ Cancelled")


# ==========================================================
# USAGE EXAMPLES
# ==========================================================
"""
# Convert all videos in default directory
python convert_videos_to_sprites.py

# Analyze video properties before converting
python convert_videos_to_sprites.py --analyze

# Analyze specific video
python convert_videos_to_sprites.py ../assets/videos/Lvl1_Topic1_slide1_NoSound.mp4

# Convert and limit to 60 frames (set MAX_FRAMES = 60 at top)
python convert_videos_to_sprites.py
"""
