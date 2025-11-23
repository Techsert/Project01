# quiz_topics.py
import pygame, os, sys, arabic_reshaper
from bidi.algorithm import get_display
from screen_helpers import dynamic_font, confirm_popup
## from alphabit_name import run_alphabit_name
## from alphabit_sound import run_alphabit_sound


# ============================================================
# Generic helper for all quiz screens
# ============================================================
def draw_quiz_screen(screen, main_app, title, buttons, bg_image):
    """Draws a quiz topic screen with buttons, profile, and exit icons."""
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    running = True
    last_hovered = None

    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((0, 0, 0))
        screen.blit(bg_image, (0, 0))

        # --- Title ---
        title_font = title_font = dynamic_font(SCREEN_HEIGHT, main_app.ARABIC_FONT_PATH, main_app.ARABIC_BOLD_FONT_PATH, 0.04, bold=True)
        title_render = title_font.render(title, True, (255, 255, 255))
        screen.blit(title_render, title_render.get_rect(center=(SCREEN_WIDTH//2, int(SCREEN_HEIGHT*0.05))))

        # --- Buttons ---
        for b in buttons:
            main_app.draw_arabic_text(b["text"], 0.06, (51, 51, 51), b["rect"].center)

        # --- Hover Sound ---
        hovered = next((i for i, b in enumerate(buttons) if b["rect"].collidepoint(mouse_pos)), None)
        if hovered is not None and hovered != last_hovered:
            main_app.play_hover_sound(buttons[hovered]["hover"])
        last_hovered = hovered

        # --- Profile + Exit + Back ---
        screen.blit(main_app.profile_icon, main_app.profile_rect)
        screen.blit(main_app.exit_icon, main_app.exit_rect)

        back_font = title_font = dynamic_font(SCREEN_HEIGHT, main_app.ARABIC_FONT_PATH, main_app.ARABIC_BOLD_FONT_PATH, 0.03, bold=True)
        back_text = back_font.render("BACK", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        screen.blit(back_text, back_rect)
        if back_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 102, 0), back_rect.inflate(20, 10), 2, border_radius=8)

        # --- Events ---
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(e.pos):
                    running = False
                elif main_app.exit_rect.collidepoint(e.pos):
                    if main_app.confirm_popup("Exit the game?"):
                        pygame.quit()
                        sys.exit()
                elif main_app.profile_rect.collidepoint(e.pos):
                    main_app.open_profile_manager()
                else:
                    for b in buttons:
                        if b["rect"].collidepoint(e.pos):
                            b["action"]()

        pygame.display.flip()
        clock.tick(60)


# ============================================================
# Quiz Level 1
# ============================================================
def quiz_one(screen, main_app):
    """Quiz Topics for Level 1"""
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    bg_path = os.path.join(main_app.IMG_PATH, "quiz_bg_1.png")

    try:
        bg_image = pygame.image.load(bg_path).convert()
        bg_image = pygame.transform.smoothscale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception as e:
        print(f"⚠️ Missing {bg_path}: {e}")
        bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_image.fill((80, 30, 30))

    bg_w, bg_h = SCREEN_WIDTH, SCREEN_HEIGHT
    btn_w, btn_h = int(bg_w * 0.25), int(bg_h * 0.10)

    positions = [(0.15, 0.36), (0.50, 0.36), (0.85, 0.36),
                 (0.15, 0.89), (0.50, 0.89), (0.85, 0.89)]

    quizzes = [
        ("Quiz: الحُروف", main_app.launch_alphabit_sound, "hover_alphabetSounds.wav"),
        ("Quiz: الأعداد", main_app.launch_alphabit_sound, "hover_numbers.wav"),
        ("Quiz: الألوان", main_app.launch_alphabit_sound, "hover_colours.wav"),
        ("Quiz: الكلمات", main_app.launch_alphabit_sound, "hover_words.wav"),
        ("Quiz: أشكال", main_app.launch_alphabit_sound, "hover_alphabetShaps.wav"),
        ("Quiz: أسماء", main_app.launch_alphabit_name, "hover_alphabetNames.wav"),
    ]

    buttons = []
    for (text, action, hover), (rx, ry) in zip(quizzes, positions):
        x = int(rx * bg_w)
        y = int(ry * bg_h)
        rect = pygame.Rect(x - btn_w // 2, y - btn_h // 2, btn_w, btn_h)
        buttons.append({
            "text": text,
            "action": action,
            "hover": os.path.join(main_app.SOUND_PATH, hover),
            "rect": rect
        })

    draw_quiz_screen(screen, main_app, "Quiz Level 1", buttons, bg_image)


# ============================================================
# Quiz Level 2 (Example)
# ============================================================
def quiz_two(screen, main_app):
    """Quiz Topics for Level 2"""
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    bg_path = os.path.join(main_app.IMG_PATH, "quiz_bg_2.png")

    try:
        bg_image = pygame.image.load(bg_path).convert()
        bg_image = pygame.transform.smoothscale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception as e:
        print(f"⚠️ Missing {bg_path}: {e}")
        bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_image.fill((40, 70, 90))

    bg_w, bg_h = SCREEN_WIDTH, SCREEN_HEIGHT
    btn_w, btn_h = int(bg_w * 0.25), int(bg_h * 0.10)

    positions = [(0.33, 0.36), (0.66, 0.36), (0.33, 0.80), (0.66, 0.80)]

    quizzes = [
        ("Quiz 2: الأشكال", main_app.launch_alphabit_sound, "hover_alphabetShaps.wav"),
        ("Quiz 2: الحروف", main_app.launch_alphabit_name, "hover_alphabetNames.wav"),
        ("Quiz 2: الألوان", main_app.launch_alphabit_sound, "hover_colours.wav"),
        ("Quiz 2: الكلمات", main_app.launch_alphabit_sound, "hover_words.wav"),
    ]

    buttons = []
    for (text, action, hover), (rx, ry) in zip(quizzes, positions):
        x = int(rx * bg_w)
        y = int(ry * bg_h)
        rect = pygame.Rect(x - btn_w // 2, y - btn_h // 2, btn_w, btn_h)
        buttons.append({
            "text": text,
            "action": action,
            "hover": os.path.join(main_app.SOUND_PATH, hover),
            "rect": rect
        })

    draw_quiz_screen(screen, main_app, "Quiz Level 2", buttons, bg_image)


# ============================================================
# Dispatcher Function
# ============================================================
def run_quiz_topics(screen, main_app, level=1):
    """Automatically runs the correct quiz screen based on the level number."""
    quiz_map = {
        1: quiz_one,
        2: quiz_two,
        # Add more quiz levels here: 3: quiz_three, 4: quiz_four, etc.
    }

    func = quiz_map.get(level)
    if func:
        func(screen, main_app)
    else:
        print(f"⚠️ No quiz defined for Level {level}")
