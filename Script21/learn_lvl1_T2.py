# alphabit_name.py — Full Pygame version (Arabic-friendly, with profile integration)
import pygame, os, sys, time
import arabic_reshaper
from bidi.algorithm import get_display

# ==========================================================
# SLIDE DATA (same structure)
# ==========================================================
slides = [
        # Intro Slide
    {
        "title": "الحُروف العَرَبية",
        "narration": "../assets/sounds/alphabitSound/intro.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/hard.png", "sound": "../assets/sounds/alphabitSound/areyouready.wav", "delay": 4000, "scale": (0.25, 0.50), "position": "center"},
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
        # Slide 2 - Ba
    {
        "title": "حرف الباء",
        "narration": "../assets/sounds/alphabitSound/02ba.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/02ba.png", "sound": "../assets/sounds/alphabitSound/02ba.wav", "delay": 0, "scale": (0.20, 0.30), "position": "center"}
        ]
    },
        # Slide 3 - Ta
    {
        "title": "حرف التاء",
        "narration": "../assets/sounds/alphabitSound/03ta.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/03ta.png", "sound": "../assets/sounds/alphabitSound/03ta.wav", "delay": 0, "scale": (0.20, 0.35), "position": "center"}
        ]
    },
        # Slide 4 - Tha
    {
        "title": "حرف الثاء",
        "narration": "../assets/sounds/alphabitSound/04tha.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/04tha.png", "sound": "../assets/sounds/alphabitSound/04tha.wav", "delay": 0, "scale": (0.20, 0.38), "position": "center"}
        ]
    },
            # Slide 5 - Gem
    {
        "title": "حرف الجيم",
        "narration": "../assets/sounds/alphabitSound/05gem.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/05geam.png", "sound": "../assets/sounds/alphabitSound/05geam.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 6 - 7a
    {
        "title": "حرف الحاء",
        "narration": "../assets/sounds/alphabitSound/06-7a.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/06ha.png", "sound": "../assets/sounds/alphabitSound/06-7a.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 7 - 7'a
    {
        "title": "حرف الخاء",
        "narration": "../assets/sounds/alphabitSound/07-7-a.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/07ka.png", "sound": "../assets/sounds/alphabitSound/07-7-a.wav", "delay": 0, "scale": (0.15, 0.45), "position": "center"}
        ]
    },
            # Slide 8 - Dal
    {
        "title": "حرف الدال",
        "narration": "../assets/sounds/alphabitSound/08dal.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/08dal.png", "sound": "../assets/sounds/alphabitSound/08dal.wav", "delay": 0, "scale": (0.10, 0.30), "position": "center"}
        ]
    },
            # Slide 9 - Thal
    {
        "title": "حرف الذال",
        "narration": "../assets/sounds/alphabitSound/09thal.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/09thal.png", "sound": "../assets/sounds/alphabitSound/09thal.wav", "delay": 0, "scale": (0.10, 0.40), "position": "center"}
        ]
    },
            # Slide 10 - Ra
    {
        "title": "حرف الراء",
        "narration": "../assets/sounds/alphabitSound/10ra.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/10ra.png", "sound": "../assets/sounds/alphabitSound/10ra.wav", "delay": 0, "scale": (0.10, 0.35), "position": "center"}
        ]
    },
            # Slide 11 - Zay
    {
        "title": "حرف الزاي",
        "narration": "../assets/sounds/alphabitSound/11zay.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/11zay.png", "sound": "../assets/sounds/alphabitSound/11zay.wav", "delay": 0, "scale": (0.10, 0.40), "position": "center"}
        ]
    },
            # Slide 12 - Sen
    {
        "title": "حرف السين",
        "narration": "../assets/sounds/alphabitSound/12sen.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/12sen.png", "sound": "../assets/sounds/alphabitSound/12sen.wav", "delay": 0, "scale": (0.20, 0.35), "position": "center"}
        ]
    },
            # Slide 13 - Shen
    {
        "title": "حرف الشين",
        "narration": "../assets/sounds/alphabitSound/13shen.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/13shen.png", "sound": "../assets/sounds/alphabitSound/13shen.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },
            # Slide 14 - Sad
    {
        "title": "حرف الصاد",
        "narration": "../assets/sounds/alphabitSound/14sad.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/14sad.png", "sound": "../assets/sounds/alphabitSound/14sad.wav", "delay": 0, "scale": (0.20, 0.35), "position": "center"}
        ]
    },
            # Slide 15 - Dad
    {
        "title": "حرف الضاد",
        "narration": "../assets/sounds/alphabitSound/15dad.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/15dad.png", "sound": "../assets/sounds/alphabitSound/15dad.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },
            # Slide 16 - Taa
    {
        "title": "حرف الطاء",
        "narration": "../assets/sounds/alphabitSound/16taa.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/16taa.png", "sound": "../assets/sounds/alphabitSound/16taa.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },
            # Slide 17 - Zaa
    {
        "title": "حرف الظاء",
        "narration": "../assets/sounds/alphabitSound/17zaa.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/17zaa.png", "sound": "../assets/sounds/alphabitSound/17zaa.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },
            # Slide 18 - Aen
    {
        "title": "حرف العين",
        "narration": "../assets/sounds/alphabitSound/18ayn.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/18aen.png", "sound": "../assets/sounds/alphabitSound/18ayn.wav", "delay": 0, "scale": (0.15, 0.40), "position": "center"}
        ]
    },
            # Slide 19 - Gaen
    {
        "title": "حرف الغين",
        "narration": "../assets/sounds/alphabitSound/19gean.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/19gean.png", "sound": "../assets/sounds/alphabitSound/19gean.wav", "delay": 0, "scale": (0.15, 0.45), "position": "center"}
        ]
    },
            # Slide 20 - Feh
    {
        "title": "حرف الفاء",
        "narration": "../assets/sounds/alphabitSound/20feh.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/20feh.png", "sound": "../assets/sounds/alphabitSound/20feh.wav", "delay": 0, "scale": (0.20, 0.30), "position": "center"}
        ]
    },
            # Slide 21 - Kf
    {
        "title": "حرف القاف",
        "narration": "../assets/sounds/alphabitSound/21kf.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/21kf.png", "sound": "../assets/sounds/alphabitSound/21kf.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 22 - Kaf
    {
        "title": "حرف الكاف",
        "narration": "../assets/sounds/alphabitSound/22kaf.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/22kaf.png", "sound": "../assets/sounds/alphabitSound/22kaf.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 23 - Lam
    {
        "title": "حرف اللام",
        "narration": "../assets/sounds/alphabitSound/23lam.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/23lam.png", "sound": "../assets/sounds/alphabitSound/23lam.wav", "delay": 0, "scale": (0.10, 0.35), "position": "center"}
        ]
    },
            # Slide 24 - Meam
    {
        "title": "حرف الميم",
        "narration": "../assets/sounds/alphabitSound/24meam.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/24meam.png", "sound": "../assets/sounds/alphabitSound/24meam.wav", "delay": 0, "scale": (0.10, 0.35), "position": "center"}
        ]
    },
            # Slide 25 - Noon
    {
        "title": "حرف النون",
        "narration": "../assets/sounds/alphabitSound/25noon.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/25noon.png", "sound": "../assets/sounds/alphabitSound/25noon.wav", "delay": 0, "scale": (0.15, 0.35), "position": "center"}
        ]
    },
            # Slide 26 - Heh
    {
        "title": "حرف الهاء",
        "narration": "../assets/sounds/alphabitSound/26heh.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/26heh.png", "sound": "../assets/sounds/alphabitSound/26heh.wav", "delay": 0, "scale": (0.15, 0.30), "position": "center"}
        ]
    },
                # Slide 27 - Waw
    {
        "title": "حرف الواو",
        "narration": "../assets/sounds/alphabitSound/27waw.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/27waw.png", "sound": "../assets/sounds/alphabitSound/27waw.wav", "delay": 0, "scale": (0.10, 0.35), "position": "center"}
        ]
    },
                # Slide 28 - Yaa
    {
        "title": "حرف الياء",
        "narration": "../assets/sounds/alphabitSound/28yaa.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.78), "position": "center"},
            {"path": "../assets/img/alphabitSound/Letters/28yaa.png", "sound": "../assets/sounds/alphabitSound/28yaa.wav", "delay": 0, "scale": (0.20, 0.35), "position": "center"}
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
def run_learn_lvl1_T2(screen, main_app):
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
        font_path = main_app.ARABIC_BOLD_FONT_PATH if bold else main_app.ARABIC_FONT_PATH
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
        """Draws all images in the current slide (after their delay)."""
        elapsed = (time.time() - start_time) * 1000
        for img_data in slide["images"]:
            if elapsed >= img_data.get("delay", 0):
                draw_centered_image(
                    img_data["path"],
                    img_data.get("scale", (0.3, 0.3)),
                    img_data.get("position", "center"),
                )
                if not img_data.get("_played", False) and "sound" in img_data:
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
        btn_font = pygame.font.Font(main_app.ARABIC_FONT_PATH, int(SCREEN_HEIGHT * 0.035))
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
