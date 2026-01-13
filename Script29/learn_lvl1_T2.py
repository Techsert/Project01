# learn_lvl1_T1.py — Introduction to the arabic language
import pygame, os, sys, time
import arabic_reshaper
from bidi.algorithm import get_display
import config
from moviepy import VideoFileClip # Import moviepy
from learning_topics import run_learning_topics

# ==========================================================
# SLIDE DATA (updated for video)
# ==========================================================
slides = [
    # intro slide
    {
        "title": "Alphabet Names",
        "background_image": { # NEW KEY for background
            "path": "../assets/img/alphabitSound/bg-nt.png",
            "scale": (0.95, 0.78),
            "position": "center" # Usually center or top-left for backgrounds
        },
        "video": {
            "path": "../assets/videos/Lvl1_Topic1_slide2_NoSound.mp4",
            "audio_path": "../assets/sounds/Learn_lvl1_T1/lvl1_topic1_Slide2.wav",
            "scale": (0.3, 0.5), # Video will appear on top of the background
            "position": "center"
        },
         "images": [
             {"path": "../assets/img/boy01.png", "delay": 2000, "scale": (0.1, 0.1), "position": "bottom-right"},
         ]
    },
    
    # Sub intro slide 
    {
        "title": "Introduction To The Arabic Language",
        "background_image": {
            "path": "../assets/img/alphabitSound/bg-nt.png",
            "scale": (0.95, 0.78),
            "position": "center" 
        },
        "video": {
            "path": "../assets/videos/Lvl1_Topic1_slide2_NoSound.mp4",
            "audio_path": "../assets/sounds/Learn_lvl1_T1/lvl1_topic1_Slide2.wav",
            "scale": (0.3, 0.5), 
            "position": "center"
        },
         "images": [
             {"path": "../assets/img/boy01.png", "delay": 2000, "scale": (0.1, 0.1), "position": "bottom-right"},
         ]
    },
    
    # Slide 1 - 
    {
        "title": "حرف الألف",
        "narration": "",
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
# ==========================================================
# GLOBAL VIDEO CACHE (to avoid reloading for multiple slides)
# ==========================================================
video_cache = {}

# Store the last frame of a video once it's finished
last_video_frame_cache = {}

# ==========================================================
# RUN FUNCTION
# ==========================================================
def run_learn_lvl1_T2(screen, main_app):
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    slide_index = 0
    start_time = 0
    current_video_clip = None
    video_start_time = 0
    video_finished = False
    last_rendered_video_frame_surface = None

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

    def get_video_frame_surface(clip, current_time, video_data):
        """Fetches, converts, and scales a video frame."""
        try:
            frame_array = clip.get_frame(current_time)
            frame_surface = pygame.surfarray.make_surface(frame_array.swapaxes(0, 1))

            # Scale the frame
            scale = video_data.get("scale", (1.0, 1.0))
            w, h = int(SCREEN_WIDTH * scale[0]), int(SCREEN_HEIGHT * scale[1])
            frame_surface = pygame.transform.smoothscale(frame_surface, (w, h))
            return frame_surface
        except Exception as e:
            print(f"Error getting or processing video frame: {e}")
            return None


    def render_slide(slide):
        """Draws content based on slide type: background, then video, then foreground images."""
        nonlocal current_video_clip, video_start_time, video_finished, last_rendered_video_frame_surface

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

            # Initialize video only once when entering the slide or if it was reset
            if current_video_clip is None and not video_finished:
                current_video_clip = load_video_clip(video_path)
                if current_video_clip:
                    video_start_time = time.time() # Reset video start time
                    last_rendered_video_frame_surface = None # Clear previous frame cache

                    # ✅ Play external audio if provided (videos have no sound)
                    if audio_path and os.path.exists(audio_path):
                        play_sound(audio_path)
                    else:
                        print("No audio file specified for video slide.")
                else:
                    draw_arabic_text("Video not available", 0.05, (255, 0, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    video_finished = True # Mark as finished if clip can't be loaded

            # Display video frame if clip is loaded and not finished
            if current_video_clip and not video_finished:
                elapsed_video_time = (time.time() - video_start_time)

                if elapsed_video_time < current_video_clip.duration:
                    frame_surface = get_video_frame_surface(current_video_clip, elapsed_video_time, video_data)
                    if frame_surface:
                        last_rendered_video_frame_surface = frame_surface # Cache the current frame
                else:
                    # Video finished, get and cache the last frame, then set flag
                    if last_rendered_video_frame_surface is None or video_path not in last_video_frame_cache:
                        frame_surface = get_video_frame_surface(current_video_clip, current_video_clip.duration - 0.01, video_data)
                        if frame_surface:
                            last_rendered_video_frame_surface = frame_surface
                            last_video_frame_cache[video_path] = frame_surface # Store for future re-draws
                    
                    video_finished = True
                    pygame.mixer.music.stop() # Stop video audio when it finishes
            
            # Draw the cached frame if video is finished or if it's the current frame
            if last_rendered_video_frame_surface:
                rect = last_rendered_video_frame_surface.get_rect()
                position = video_data.get("position", "center")
                if position == "center":
                    rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                elif position == "top-left":
                    rect.topleft = (0, 0)
                elif position == "bottom-right":
                    rect.bottomright = (SCREEN_WIDTH, SCREEN_HEIGHT)
                screen.blit(last_rendered_video_frame_surface, rect)
            elif video_finished and video_path in last_video_frame_cache:
                # If video finished and we have a cached last frame, draw it
                rect = last_video_frame_cache[video_path].get_rect()
                position = video_data.get("position", "center")
                if position == "center":
                    rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                elif position == "top-left":
                    rect.topleft = (0, 0)
                elif position == "bottom-right":
                    rect.bottomright = (SCREEN_WIDTH, SCREEN_HEIGHT)
                screen.blit(last_video_frame_cache[video_path], rect)


        # 3. Draw Foreground Images if present (on top of video/background)
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

                if not img_data.get("_played", False) and elapsed >= delay and "sound" in img_data:
                    if not pygame.mixer.music.get_busy() or "video" not in slide:
                        play_sound(img_data["sound"])
                        img_data["_played"] = True

    # ------------------------------------------------------
    # MAIN LOOP
    # ------------------------------------------------------
    running = True

    # Initial slide setup
    current_slide = slides[slide_index]
    
    # ✅ FIX: Set audio context for main_app BEFORE playing
    if "video" in current_slide:
        video_data = current_slide["video"]
        if video_data.get("audio_path"):
            main_app._current_audio_type = 'video_audio'
            main_app._current_audio_path = video_data["audio_path"]
        else:
            main_app._current_audio_type = 'video_audio'
            main_app._current_audio_path = "temp_video_audio.wav"
    elif "narration" in current_slide:
        main_app._current_audio_type = 'narration'
        main_app._current_audio_path = current_slide["narration"]
        play_sound(current_slide["narration"])
    else:
        main_app._current_audio_type = 'bg_music'
        main_app._current_audio_path = None

    start_time = time.time()

    while running:
        screen.fill((255, 255, 255))
        slide = slides[slide_index]

        # Determine if video is currently active and playing
        is_video_slide = "video" in slide
        is_video_playing = is_video_slide and current_video_clip is not None and not video_finished

        # === Draw content ===
        render_slide(slide)

        # === Title ===
        draw_arabic_text(
            slide["title"], 
            0.06, 
            (0, 0, 0), 
            (SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.07)), 
            bold=True
        )

        # === Profile + Exit icons ===
        screen.blit(main_app.profile_icon, main_app.profile_rect)
        screen.blit(main_app.exit_icon, main_app.exit_rect)

        # === Navigation Buttons ===
        btn_font = pygame.font.Font(config.ARABIC_FONT_REGULAR, int(SCREEN_HEIGHT * 0.035))
        next_rect = pygame.Rect(int(SCREEN_WIDTH * 0.05), int(SCREEN_HEIGHT * 0.90), 250, 100)
        prev_rect = pygame.Rect(int(SCREEN_WIDTH * 0.82), int(SCREEN_HEIGHT * 0.90), 250, 100)
        back_rect = pygame.Rect(int(SCREEN_WIDTH * 0.42), int(SCREEN_HEIGHT * 0.90), 250, 100)

        # Define button colors based on state
        next_color = (60, 120, 200) if not is_video_playing else (150, 150, 150)
        prev_color = (60, 120, 200) if not is_video_playing else (150, 150, 150)
        back_color = (200, 80, 80)

        pygame.draw.rect(screen, next_color, next_rect, border_radius=15)
        pygame.draw.rect(screen, prev_color, prev_rect, border_radius=15)
        pygame.draw.rect(screen, back_color, back_rect, border_radius=15)

        main_app.draw_arabic_text("Next", 0.035, (255,255,255), next_rect.center)
        main_app.draw_arabic_text("Prev", 0.035, (255,255,255), prev_rect.center)
        main_app.draw_arabic_text("Back", 0.035, (255,255,255), back_rect.center)

        pygame.display.flip()

        # === Handle Events ===
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if main_app.exit_rect.collidepoint(e.pos):
                    if main_app.confirm_popup("Exit the game?"):
                        pygame.quit()
                        sys.exit()
                        
                elif main_app.profile_rect.collidepoint(e.pos):
                    current_slide_data = slides[slide_index]
                    
                    # Set audio context before opening profile manager
                    if "video" in current_slide_data and current_slide_data["video"].get("audio_path"):
                        main_app._current_audio_type = 'video_audio'
                        main_app._current_audio_path = current_slide_data["video"]["audio_path"]
                    elif "narration" in current_slide_data:
                        main_app._current_audio_type = 'narration'
                        main_app._current_audio_path = current_slide_data["narration"]
                    else:
                        main_app._current_audio_type = 'bg_music'
                        main_app._current_audio_path = None

                    stop_sounds()
                    main_app.open_profile_manager()

                    # Reset video state after returning from profile
                    if "video" in current_slide_data:
                        current_video_clip = None
                        video_start_time = 0
                        video_finished = False
                        last_rendered_video_frame_surface = None

                # ✅ FIXED: Next Button
                elif next_rect.collidepoint(e.pos):
                    if not is_video_playing:  # Only allow navigation when video isn't playing
                        # Stop current sounds
                        stop_sounds()
                        
                        # Clear video state
                        current_video_clip = None
                        video_finished = False
                        last_rendered_video_frame_surface = None
                        
                        # Move to next slide
                        slide_index = min(slide_index + 1, len(slides) - 1)
                        start_time = time.time()  # Reset timer for image delays
                        
                        # Get new slide
                        new_slide = slides[slide_index]
                        
                        # Reset image played flags
                        if "images" in new_slide:
                            for s_img in new_slide["images"]:
                                s_img["_played"] = False
                        
                        # ✅ FIX: Set audio context for the NEW slide
                        if "video" in new_slide:
                            video_data = new_slide["video"]
                            if video_data.get("audio_path"):
                                main_app._current_audio_type = 'video_audio'
                                main_app._current_audio_path = video_data["audio_path"]
                                # Video audio will auto-play in render_slide
                            else:
                                main_app._current_audio_type = 'video_audio'
                                main_app._current_audio_path = "temp_video_audio.wav"
                        elif "narration" in new_slide:
                            main_app._current_audio_type = 'narration'
                            main_app._current_audio_path = new_slide["narration"]
                            play_sound(new_slide["narration"])  # Play narration immediately
                        else:
                            main_app._current_audio_type = 'bg_music'
                            main_app._current_audio_path = None

                # ✅ FIXED: Previous Button
                elif prev_rect.collidepoint(e.pos):
                    if not is_video_playing:  # Only allow navigation when video isn't playing
                        # Stop current sounds
                        stop_sounds()
                        
                        # Clear video state
                        current_video_clip = None
                        video_finished = False
                        last_rendered_video_frame_surface = None
                        
                        # Move to previous slide
                        slide_index = max(slide_index - 1, 0)
                        start_time = time.time()  # Reset timer for image delays
                        
                        # Get new slide
                        new_slide = slides[slide_index]
                        
                        # Reset image played flags
                        if "images" in new_slide:
                            for s_img in new_slide["images"]:
                                s_img["_played"] = False
                        
                        # ✅ FIX: Set audio context for the NEW slide
                        if "video" in new_slide:
                            video_data = new_slide["video"]
                            if video_data.get("audio_path"):
                                main_app._current_audio_type = 'video_audio'
                                main_app._current_audio_path = video_data["audio_path"]
                                # Video audio will auto-play in render_slide
                            else:
                                main_app._current_audio_type = 'video_audio'
                                main_app._current_audio_path = "temp_video_audio.wav"
                        elif "narration" in new_slide:
                            main_app._current_audio_type = 'narration'
                            main_app._current_audio_path = new_slide["narration"]
                            play_sound(new_slide["narration"])  # Play narration immediately
                        else:
                            main_app._current_audio_type = 'bg_music'
                            main_app._current_audio_path = None

                # Back Button
                elif back_rect.collidepoint(e.pos):
                    stop_sounds()
                    current_video_clip = None
                    video_finished = False
                    last_rendered_video_frame_surface = None
                    
                    # Clear audio context
                    main_app._current_audio_type = 'bg_music'
                    main_app._current_audio_path = None
                    
                    running = False
                    run_learning_topics(screen, main_app, level=1)

        clock.tick(60)

    stop_sounds()
    
    # ✅ FIX: Final cleanup
    main_app._current_audio_type = 'bg_music'
    main_app._current_audio_path = None


















































    
