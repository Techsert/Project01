# learning_topics.py
# This is for the screen to choose a topic after you selected the LVL from the learning LVL screen 
import pygame, os, sys, arabic_reshaper
from bidi.algorithm import get_display
from screen_helpers import dynamic_font, confirm_popup
import config

## from alphabit_name import run_alphabit_name
## from alphabit_sound import run_alphabit_sound

# ============================================================
# Generic helper for all topic screens
# ============================================================
def draw_topic_screen(screen, main_app, title, buttons, bg_image, bg_rect):
    """Draws a full topic screen with buttons, profile, and exit icons."""
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    running = True
    last_hovered = None

    # If no custom bg_rect passed, center by default
    if bg_rect is None:
        bg_rect = bg_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((255, 255, 255))

        # ✅ Centered background draw
        screen.blit(bg_image, bg_rect)

        # --- Title ---
        title_font = dynamic_font(config.SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, 0.04, bold=True)
        title_render = title_font.render(title, True, (180, 0, 200))
        screen.blit(title_render, title_render.get_rect(center=(SCREEN_WIDTH // 2, bg_rect.top - int(SCREEN_HEIGHT * 0.05))))


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

        back_font = dynamic_font(config.SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, 0.03, bold=True)
        back_text = back_font.render("BACK", True, (180, 0, 200))
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
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
                        pygame.quit(); sys.exit()
                elif main_app.profile_rect.collidepoint(e.pos):
                    main_app.open_profile_manager()
                else:
                    for b in buttons:
                        if b["rect"].collidepoint(e.pos):
                            b["action"]()

        pygame.display.flip()
        clock.tick(60)



# ============================================================
# Topic 1 Screen (Learning Level 1)
# ============================================================
def topic_one(screen, main_app):
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    bg_path = os.path.join(config.IMG_MAIN_PATH, "Learning_bg_L1.png")

    try:
        bg_image = pygame.image.load(bg_path).convert_alpha()
    except Exception as e:
        print(f"⚠️ Missing {bg_path}: {e}")
        bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_image.fill((255, 255, 255))

    # === FLEXIBLE BACKGROUND ===
    scale_ratio = 0.8
    bg_w = int(SCREEN_WIDTH * scale_ratio)
    bg_h = int(SCREEN_HEIGHT * scale_ratio)
    bg_image = pygame.transform.smoothscale(bg_image, (bg_w, bg_h))
    bg_rect = bg_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # === Optional offset ===
    bg_rect.y -= -20  # move slightly up if needed

    # === BUTTON POSITIONS RELATIVE TO BACKGROUND ===
    btn_w, btn_h = int(bg_w * 0.25), int(bg_h * 0.10)
    positions = [
        (0.15, 0.76),
        (0.50, 0.76),
        (0.87, 0.76),
##        (0.15, 0.89),
##        (0.50, 0.89),
##        (0.85, 0.89)
    ]

    topics = [
        ("Intro to Arabic", main_app.launch_learn_lvl1_T1, "hover_alphabetNames.wav"),
        ("Alphabet Names", main_app.launch_learn_lvl1_T2, "hover_alphabetSounds.wav"),
        ("Revision", main_app.launch_learn_lvl1_T2, "hover_alphabetShaps.wav"),
##        ("الأعداد", main_app.launch_alphabit_sound, "hover_numbers.wav"),
##        ("الألوان", main_app.launch_alphabit_sound, "hover_colours.wav"),
##        ("الكَلِمات", main_app.launch_alphabit_sound, "hover_words.wav"),
    ]

    # === Build buttons only ===
    buttons = []
    for (text, action, hover), (rx, ry) in zip(topics, positions):
        x = bg_rect.left + int(rx * bg_w)
        y = bg_rect.top + int(ry * bg_h)
        rect = pygame.Rect(x - btn_w // 2, y - btn_h // 2, btn_w, btn_h)
        buttons.append({
            "text": text,
            "action": action,
            "hover": os.path.join(config.SOUND_MAIN_PATH, hover),
            "rect": rect
        })

    # ✅ Now call the draw loop
    draw_topic_screen(screen, main_app, "Learning Level 1", buttons, bg_image, bg_rect)





# ============================================================
# Topic 2 Screen (Learning Level 2)
# ============================================================
def topic_two(screen, main_app):
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    bg_path = os.path.join(config.IMG_MAIN_PATH, "learning_bg_2.png")

    try:
        bg_image = pygame.image.load(bg_path).convert_alpha()
    except Exception as e:
        print(f"⚠️ Missing {bg_path}: {e}")
        bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_image.fill((0, 255, 155))

    # === FLEXIBLE BACKGROUND ===
    scale_ratio = 0.75
    bg_w = int(SCREEN_WIDTH * scale_ratio)
    bg_h = int(SCREEN_HEIGHT * scale_ratio)
    bg_image = pygame.transform.smoothscale(bg_image, (bg_w, bg_h))
    bg_rect = bg_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # 🔧 Optional: move slightly up/down or sideways
    bg_rect.y -= 30  # move up a bit
    # bg_rect.x += 10  # example: shift right slightly if needed

    # === BUTTON POSITIONS RELATIVE TO BACKGROUND ===
    btn_w, btn_h = int(bg_w * 0.25), int(bg_h * 0.10)
    positions = [
        (0.33, 0.36),
        (0.66, 0.36),
        (0.33, 0.80),
        (0.66, 0.80)
    ]

    topics = [
        ("Level 2: كلمات جديدة", main_app.launch_alphabit_sound, "hover_words.wav"),
        ("Level 2: ألوان إضافية", main_app.launch_alphabit_sound, "hover_colours.wav"),
        ("Level 2: أشكال", main_app.launch_alphabit_sound, "hover_alphabetShaps.wav"),
        ("Level 2: الأعداد", main_app.launch_alphabit_sound, "hover_numbers.wav"),
    ]

    buttons = []
    for (text, action, hover), (rx, ry) in zip(topics, positions):
        x = bg_rect.left + int(rx * bg_w)
        y = bg_rect.top + int(ry * bg_h)
        rect = pygame.Rect(x - btn_w // 2, y - btn_h // 2, btn_w, btn_h)
        buttons.append({
            "text": text,
            "action": action,
            "hover": os.path.join(config.SOUND_MAIN_PATH, hover), # Use config
            "rect": rect
        })

    # ✅ pass both bg_image and bg_rect
    draw_topic_screen(screen, main_app, "Learning Level 2", buttons, bg_image, bg_rect)




# ============================================================
# Dispatcher Function
# ============================================================
def run_learning_topics(screen, main_app, level=1):
    """Automatically runs the correct topic screen based on the level number."""
    topic_map = {
        1: topic_one,
        2: topic_two,
        # add more topics here: 3: topic_three, 4: topic_four, etc.
    }

    func = topic_map.get(level)
    if func:
        func(screen, main_app)
    else:
        print(f"⚠️ No topic defined for Level {level}")
