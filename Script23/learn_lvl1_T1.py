# learn_lvl1_T1.py — Introduction to the arabic language
import pygame, os, sys, time
import arabic_reshaper
from bidi.algorithm import get_display
import config
from moviepy import VideoFileClip # Import moviepy

# Initialize moviepy (this is crucial for handling video objects)
# Note: moviepy uses ffmpeg, ensure it's installed and accessible in your PATH
# If you get errors, you might need to specify the ffmpeg path:
# from moviepy.config import change_settings
# change_settings({"FFMPEG_BINARY": "/path/to/your/ffmpeg"})


# ==========================================================
# SLIDE DATA (updated for video)
# ==========================================================
slides = [
    # ... other slides ...

    # Slide with a Background Image AND a Video
    {
        "title": "Video with Background",
        "background_image": { # NEW KEY for background
            "path": "../assets/img/alphabitSound/bg-nt.png",
            "scale": (0.95, 0.78),
            "position": "center" # Usually center or top-left for backgrounds
        },
        "video": {
            "path": "../assets/videos/intro.mp4",
            "audio_path": "../assets/sounds/Learn_lvl1_T1/intro.wav",
            "scale": (0.3, 0.5), # Video will appear on top of the background
            "position": "center"
        },
        # You can optionally still have "images" for foreground elements
        # that appear on top of the video and background.
        # "images": [
        #     {"path": "../assets/img/some_foreground_element.png", "delay": 2000, "scale": (0.1, 0.1), "position": "bottom-right"},
        # ]
    },
    # Slide 1 - Alef (using images)
    {
        "title": "حرف الألف",
        "narration": "../assets/sounds/alphabitSound/01alef.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/01alef.png", "sound": "../assets/sounds/alphabitSound/01alef.wav", "delay": 0, "scale": (0.04, 0.40), "position": "center"}
        ]
    },
##    # End Slide
##    {
##        "title": "أحسنت", # "Well Done"
##        "narration": "../assets/sounds/alphabitSound/welldone01.wav",
##        "images": [
##            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
##            {"path": "../assets/img/alphabitSound/coach.png", "sound": "../assets/sounds/alphabitSound/welldone01.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
##        ]
##    },
]

# ==========================================================
# GLOBAL VIDEO CACHE (to avoid reloading for multiple slides)
# ==========================================================
video_cache = {}

# ==========================================================
# RUN FUNCTION
# ==========================================================
def run_learn_lvl1_T1(screen, main_app):
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    slide_index = 0
    start_time = 0
    current_images = []
    playing_sound = False
    current_video_clip = None # Stores the moviepy VideoFileClip object
    video_frames_iterator = None # Iterator for video frames
    video_start_time = 0 # Time when video playback started

    def stop_sounds():
        """Stops narration and all channels."""
        try:
            pygame.mixer.music.stop()
            for i in range(pygame.mixer.get_num_channels()):
                pygame.mixer.Channel(i).stop()
        except Exception as e:
            print("Stop sound error:", e)

    def play_sound(path):
        """Plays narration or per-image sound."""
        try:
            if os.path.exists(path):
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
        except Exception as e:
            print("Sound error:", e)

    def draw_arabic_text(text, size_ratio, color, center, bold=False):
        """Arabic-safe centered text rendering."""
        reshaped = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped)
        font_path = config.ARABIC_FONT_BOLD if bold else config.ARABIC_FONT_REGULAR
        font = pygame.font.Font(font_path, int(SCREEN_HEIGHT * size_ratio))
        rendered = font.render(bidi_text, True, color)
        rect = rendered.get_rect(center=center)
        screen.blit(rendered, rect)

    def draw_centered_image(img_path, scale, position="center"):
        """Draw an image with scaling relative to screen size."""
        try:
            img = pygame.image.load(img_path).convert_alpha()
            w, h = int(SCREEN_WIDTH * scale[0]), int(SCREEN_HEIGHT * scale[1])
            img = pygame.transform.smoothscale(img, (w, h))
            rect = img.get_rect()
            if position == "center":
                rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            elif position == "top-left":
                rect.topleft = (0, 0)
            elif position == "bottom-right":
                rect.bottomright = (SCREEN_WIDTH, SCREEN_HEIGHT)
            screen.blit(img, rect)
            return rect
        except Exception as e:
            print(f"⚠️ Image load error: {img_path} | {e}")
            return None # Return None if image loading fails

    def load_video_clip(video_path):
        if video_path not in video_cache:
            try:
                clip = VideoFileClip(video_path)
                video_cache[video_path] = clip
            except Exception as e:
                print(f"Error loading video with moviepy: {video_path} | {e}")
                return None
        return video_cache[video_path]

    def render_slide(slide):
        """Draws content based on slide type: background, then video, then foreground images."""
        nonlocal current_video_clip, video_frames_iterator, video_start_time

        # 1. Draw Background Image if present
        if "background_image" in slide:
            bg_data = slide["background_image"]
            draw_centered_image(
                bg_data["path"],
                bg_data.get("scale", (1.0, 1.0)), # Default to full screen if no scale
                bg_data.get("position", "top-left"), # Backgrounds often start top-left
            )


        # 2. Draw Video if present (on top of background)
        if "video" in slide:
            video_data = slide["video"]
            video_path = video_data["path"]
            audio_path = video_data.get("audio_path")

            if current_video_clip is None: # First time entering this video slide
                current_video_clip = load_video_clip(video_path)
                if current_video_clip:
                    video_frames_iterator = current_video_clip.iter_frames(fps=current_video_clip.fps, dtype='uint8')
                    video_start_time = time.time() # Reset video start time

                    # Play audio (either from video or separate file)
                    if audio_path and os.path.exists(audio_path):
                        play_sound(audio_path)
                    elif current_video_clip.audio:
                        # moviepy can write the video's audio to a temporary file
                        temp_audio_file = "temp_video_audio.wav"
                        try:
                            # Ensure the temp file exists, and its creation doesn't error on subsequent plays
                            if not os.path.exists(temp_audio_file) or video_path not in video_cache:
                                current_video_clip.audio.write_audiofile(temp_audio_file)
                            play_sound(temp_audio_file)
                        except Exception as e:
                            print(f"Error extracting and playing video audio: {e}")
                    else:
                        print("No audio specified or found for video slide.")
                else:
                    draw_arabic_text("Video not available", 0.05, (255, 0, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    # Don't return here, as we might still want to draw foreground images
            
            # Display video frame if clip is loaded
            if current_video_clip:
                elapsed_video_time = (time.time() - video_start_time)

                try:
                    if elapsed_video_time < current_video_clip.duration:
                        frame_array = current_video_clip.get_frame(elapsed_video_time)
                        frame_surface = pygame.surfarray.make_surface(frame_array.swapaxes(0, 1))
                        # Applying vertical flip to fix potential upside-down issue.
                        # If your video is still upside down, try changing (False, True) to (False, False)
                        # Or if it's already fixed, ensure this line is present.
##                        frame_surface = pygame.transform.flip(frame_surface, False, True)

                        # Scale the frame
                        scale = video_data.get("scale", (1.0, 1.0))
                        w, h = int(SCREEN_WIDTH * scale[0]), int(SCREEN_HEIGHT * scale[1])
                        frame_surface = pygame.transform.smoothscale(frame_surface, (w, h))

                        # Position the frame
                        rect = frame_surface.get_rect()
                        position = video_data.get("position", "center")
                        if position == "center":
                            rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                        elif position == "top-left":
                            rect.topleft = (0, 0)
                        elif position == "bottom-right":
                            rect.bottomright = (SCREEN_WIDTH, SCREEN_HEIGHT)

                        screen.blit(frame_surface, rect)
                    else:
                        # Video finished
                        current_video_clip = None
                        video_frames_iterator = None
                        pygame.mixer.music.stop() # Stop video audio
                except Exception as e:
                    print(f"Error displaying video frame: {e}")
                    current_video_clip = None
                    video_frames_iterator = None
                    pygame.mixer.music.stop()


        # 3. Draw Foreground Images if present (on top of video/background)
        # These are your existing 'images' that appear based on delay/duration
        if "images" in slide:
            elapsed = (time.time() - start_time) * 1000
            for img_data in slide["images"]:
                delay = img_data.get("delay", 0)
                duration = img_data.get("duration", None)

                if elapsed >= delay and (duration is None or elapsed <= delay + duration):
                    draw_centered_image(
                        img_data["path"],
                        img_data.get("scale", (0.3, 0.3)),
                        img_data.get("position", "center"),
                    )

                # Narration for foreground images.
                # Note: If a video is playing, its audio will take precedence for pygame.mixer.music.
                # You might need to manage channels for multiple concurrent sounds.
                if not img_data.get("_played", False) and elapsed >= delay and "sound" in img_data:
                    # Only play image sound if no video audio is currently playing, or if it's on a different channel
                    if not pygame.mixer.music.get_busy() or "video" not in slide:
                        play_sound(img_data["sound"])
                        img_data["_played"] = True

    # ------------------------------------------------------
    # MAIN LOOP
    # ------------------------------------------------------
    running = True

    # Initial slide setup
    current_slide = slides[slide_index]
    if "narration" in current_slide:
        play_sound(current_slide["narration"])
    elif "video" in current_slide:
        # Video will be initialized and audio played in render_slide
        pass # Audio will be handled by render_slide for videos

    start_time = time.time() # This start_time is for image delays

    while running:
        screen.fill((255, 255, 255))
        slide = slides[slide_index]

        # === Draw content ===
        render_slide(slide)

        # === Title ===
        draw_arabic_text(slide["title"], 0.06, (0, 0, 0), (SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.07)), bold=True)

        # === Profile + Exit icons ===
        screen.blit(main_app.profile_icon, main_app.profile_rect)
        screen.blit(main_app.exit_icon, main_app.exit_rect)

        # === Navigation Buttons ===
        btn_font = pygame.font.Font(config.ARABIC_FONT_REGULAR, int(SCREEN_HEIGHT * 0.035))
        next_rect = pygame.Rect(int(SCREEN_WIDTH * 0.05), int(SCREEN_HEIGHT * 0.90), 250, 100)
        prev_rect = pygame.Rect(int(SCREEN_WIDTH * 0.82), int(SCREEN_HEIGHT * 0.90), 250, 100)
        back_rect = pygame.Rect(int(SCREEN_WIDTH * 0.42), int(SCREEN_HEIGHT * 0.90), 250, 100)

        pygame.draw.rect(screen, (60, 120, 200), next_rect, border_radius=15)
        pygame.draw.rect(screen, (60, 120, 200), prev_rect, border_radius=15)
        pygame.draw.rect(screen, (200, 80, 80), back_rect, border_radius=15)

        main_app.draw_arabic_text("Next", 0.035, (255,255,255), next_rect.center)
        main_app.draw_arabic_text("Prev", 0.035, (255,255,255), prev_rect.center)
        main_app.draw_arabic_text("Back", 0.035, (255,255,255), back_rect.center)

        pygame.display.flip()

        # === Handle Events ===
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if main_app.exit_rect.collidepoint(e.pos):
                    if main_app.confirm_popup("Exit the game?"):
                        pygame.quit(); sys.exit()
                elif main_app.profile_rect.collidepoint(e.pos):
                    main_app.open_profile_manager()
                elif next_rect.collidepoint(e.pos):
                    stop_sounds()
                    current_video_clip = None # Reset video for next slide
                    video_frames_iterator = None
                    slide_index = min(slide_index + 1, len(slides) - 1)
                    start_time = time.time()
                    # Reinitialize for new slide
                    new_slide = slides[slide_index]
                    if "images" in new_slide:
                        for s_img in new_slide["images"]:
                            s_img["_played"] = False
                        play_sound(new_slide["narration"])
                    elif "video" in new_slide:
                        # Video will be initialized in render_slide
                        pass # Audio will be handled by render_slide for videos

                elif prev_rect.collidepoint(e.pos):
                    stop_sounds()
                    current_video_clip = None # Reset video for previous slide
                    video_frames_iterator = None
                    slide_index = max(slide_index - 1, 0)
                    start_time = time.time()
                    # Reinitialize for new slide
                    new_slide = slides[slide_index]
                    if "images" in new_slide:
                        for s_img in new_slide["images"]:
                            s_img["_played"] = False
                        play_sound(new_slide["narration"])
                    elif "video" in new_slide:
                        # Video will be initialized in render_slide
                        pass # Audio will be handled by render_slide for videos
                elif back_rect.collidepoint(e.pos):
                    stop_sounds()
                    current_video_clip = None
                    video_frames_iterator = None
                    running = False
                    main_app.open_learning_screen()

        # Check if current video has finished playing
        if current_video_clip and not pygame.mixer.music.get_busy() and (time.time() - video_start_time) >= current_video_clip.duration - 0.1: # Small buffer
            print("Video finished playing, advancing slide.")
            # Automatically advance to next slide if video finishes
            stop_sounds()
            current_video_clip = None
            video_frames_iterator = None
            slide_index = min(slide_index + 1, len(slides) - 1)
            start_time = time.time()
            new_slide = slides[slide_index]
            if "images" in new_slide:
                for s_img in new_slide["images"]:
                    s_img["_played"] = False
                play_sound(new_slide["narration"])
            elif "video" in new_slide:
                pass # Video will be initialized in render_slide


        clock.tick(30) # Keep a consistent frame rate

    stop_sounds()
    # Clear video cache on exit if desired, or keep for potential reuse
    # video_cache.clear()
    main_app.play_bg_music()
