# learn_lvl1_T1.py — Full Pygame version (Arabic-friendly, with profile integration)
import pygame, os, sys, time
import arabic_reshaper
from bidi.algorithm import get_display
import config

# ==========================================================
# SLIDE DATA (same structure)
# ==========================================================
slides = [
        # Intro Slide
    {
        "title": "Introduction to the Arabic Language",
        "narration": "../assets/sounds/Learn_lvl1_T1/intro01.wav",
        "images": [
            {"path": "../assets/img/Learn_lvl1_T1/intro01.png", "delay": 0, "duration": 1000, "scale": (0.20, 0.50), "position": "center"},
            {"path": "../assets/img/Learn_lvl1_T1/intro02.png", "sound": "../assets/sounds/Learn_lvl1_T1/intro02.wav", "delay": 1000, "scale": (0.20, 0.50), "position": "center"},
        ]
    },
        # Slide 1 - Alef
    {
        "title": "حرف الألف",
        "narration": "../assets/sounds/alphabitSound/01alef.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/01alef.png", "sound": "../assets/sounds/alphabitSound/01alef.wav", "delay": 0, "scale": (0.04, 0.40), "position": "center"}
        ]
    },
         # End Slid
    {
        "title": "أحسنت",
        "narration": "../assets/sounds/alphabitSound/welldone01.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/coach.png", "sound": "../assets/sounds/alphabitSound/welldone01.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },
    
]

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

    def render_slide(slide):
        """Draws images that are within their delay–duration window."""
        elapsed = (time.time() - start_time) * 1000
        for img_data in slide["images"]:
            delay = img_data.get("delay", 0)
            duration = img_data.get("duration", None)  # duration in ms, optional

            # Show only between delay and delay + duration (if duration exists)
            if elapsed >= delay and (duration is None or elapsed <= delay + duration):
                draw_centered_image(
                    img_data["path"],
                    img_data.get("scale", (0.3, 0.3)),
                    img_data.get("position", "center"),
                )

            # Play sound once when its delay hits
            if not img_data.get("_played", False) and elapsed >= delay and "sound" in img_data:
                play_sound(img_data["sound"])
                img_data["_played"] = True


    # ------------------------------------------------------
    # MAIN LOOP
    # ------------------------------------------------------
    running = True
    play_sound(slides[slide_index]["narration"])
    start_time = time.time()

    while running:
        screen.fill((255, 255, 255))
        slide = slides[slide_index]

        # === Draw images after delay ===
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


##        screen.blit(next_text, next_rect.move(20, 15))
##        screen.blit(prev_text, prev_rect.move(20, 15))
##        screen.blit(back_text, back_rect.move(35, 15))

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
                    slide_index = min(slide_index + 1, len(slides) - 1)
                    start_time = time.time()
                    for s in slides[slide_index]["images"]:
                        s["_played"] = False
                    play_sound(slides[slide_index]["narration"])
                elif prev_rect.collidepoint(e.pos):
                    stop_sounds()
                    slide_index = max(slide_index - 1, 0)
                    start_time = time.time()
                    for s in slides[slide_index]["images"]:
                        s["_played"] = False
                    play_sound(slides[slide_index]["narration"])
                elif back_rect.collidepoint(e.pos):
                    stop_sounds()
                    running = False
                    main_app.open_learning_screen()

        clock.tick(30)

    stop_sounds()
    main_app.play_bg_music()
