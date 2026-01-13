# quiz_topics.py - UPDATED WITH PROGRESS TRACKING
import pygame, os, sys, arabic_reshaper
from bidi.algorithm import get_display
from screen_helpers import dynamic_font, confirm_popup
import config
from profile_system import get_unlock_status  # ✅ ADD THIS IMPORT

# ============================================================
# Generic helper for all quiz screens
# ============================================================
def draw_quiz_screen(screen, main_app, title, buttons, bg_image, bg_rect, level=1):
    """
    ✅ FIXED: Draws a quiz topic screen with proper unlock checking.
    
    The 'level' parameter indicates WHICH quiz screen we're on (1, 2, or 3).
    Each quiz screen has only ONE button for that specific quiz level.
    We use the 'level' parameter to check unlock status, NOT the button index.
    """
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    running = True
    last_hovered = None
    
    # Get unlock status for current profile
    profile_name = main_app.selected_profile.get("name") if main_app.selected_profile else None
    unlock_status = get_unlock_status(profile_name) if profile_name else {"learning": {}, "quiz": {}}

    if bg_rect is None:
        bg_rect = bg_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    def show_confirm_popup(msg):
        return main_app.confirm_popup(msg)

    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((255, 255, 255))
        screen.blit(bg_image, bg_rect)
        
        # Title
        title_font = dynamic_font(SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, 0.04, bold=True)
        title_render = title_font.render(title, True, (180, 0, 200))
        screen.blit(title_render, title_render.get_rect(center=(SCREEN_WIDTH // 2, bg_rect.top - int(SCREEN_HEIGHT * 0.05))))

        # ✅ FIXED: Check unlock status using the 'level' parameter, not button index
        # This is the correct quiz level for THIS screen
        is_unlocked = unlock_status.get("quiz", {}).get(level, False)
        
        # Draw buttons
        for i, b in enumerate(buttons):
            # Draw button image (may be grayed out if locked)
            if "image" in b and b["image"] is not None:
                button_img = b["image"].copy()
                
                # Gray out locked levels
                if not is_unlocked:
                    try:
                        arr = pygame.surfarray.array3d(button_img)
                        avg = arr.mean(axis=2, keepdims=True)
                        arr[:] = avg * 0.5
                        button_img = pygame.surfarray.make_surface(arr)
                        button_img.set_alpha(150)
                    except:
                        button_img.set_alpha(100)
                
                screen.blit(button_img, b["rect"])
                
                # Draw lock icon if locked
                if not is_unlocked:
                    lock_font = dynamic_font(SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, 0.08, bold=True)
                    lock_text = lock_font.render("🔒", True, (255, 0, 0))
                    lock_rect = lock_text.get_rect(center=b["rect"].center)
                    screen.blit(lock_text, lock_rect)
            else:
                color = (100, 100, 200) if is_unlocked else (100, 100, 100)
                pygame.draw.rect(screen, color, b["rect"])
                pygame.draw.rect(screen, (50, 50, 150), b["rect"], 3)

            # Draw text
            button_text_color = (180, 0, 200) if is_unlocked else (150, 150, 150)
            offset_x = 0
            offset_y = 120
            final_text_pos = (b["rect"].center[0] + offset_x, b["rect"].center[1] + offset_y)
            main_app.draw_arabic_text(b["text"], 0.04, button_text_color, final_text_pos)

        # Hover Sound (only for unlocked levels)
        hovered = None
        for i, b in enumerate(buttons):
            if b["rect"].collidepoint(mouse_pos):
                # ✅ FIXED: Use level parameter
                if is_unlocked:
                    hovered = i
                break
        
        if hovered is not None and hovered != last_hovered:
            main_app.play_hover_sound(buttons[hovered]["hover"])
        last_hovered = hovered

        # Profile + Exit
        if main_app.profile_icon and main_app.profile_rect:
            screen.blit(main_app.profile_icon, main_app.profile_rect)
        if main_app.exit_icon and main_app.exit_rect:
            screen.blit(main_app.exit_icon, main_app.exit_rect)
        
        # Events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if main_app.exit_rect.collidepoint(e.pos):
                    if show_confirm_popup("Exit the game?"):
                        pygame.quit(); sys.exit()
                elif main_app.profile_rect.collidepoint(e.pos):
                    main_app.open_profile_manager()
                else:
                    # ✅ FIXED: Quiz button click
                    for i, b in enumerate(buttons):
                        if b["rect"].collidepoint(e.pos):
                            # Use level parameter to check unlock status
                            if is_unlocked:
                                b["action"]()
                            else:
                                # Show unlock requirement message
                                msg = f"Complete all Learning Level {level} topics first to unlock Quiz Level {level}!"
                                show_confirm_popup(msg)
                            break

        pygame.display.flip()
        clock.tick(60)


# ============================================================
# Quiz Level 1
# ============================================================
def quiz_one(screen, main_app):
    """Quiz Topics for Level 1"""
    if not pygame.display.get_surface():
        screen = pygame.display.set_mode(screen.get_size(), pygame.FULLSCREEN)
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    bg_path = os.path.join(config.IMG_MAIN_PATH, "bg-tr.png")

    try:
        bg_image = pygame.image.load(bg_path).convert_alpha()
    except Exception as e:
        print(f"⚠️ Missing {bg_path}: {e}")
        bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_image.fill((255, 255, 255))

    # === FLEXIBLE BACKGROUND ===
    bg_w = int(SCREEN_WIDTH * 0.95)
    bg_h = int(SCREEN_HEIGHT * 0.8)
    bg_image = pygame.transform.smoothscale(bg_image, (bg_w, bg_h))
    bg_rect = bg_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # === Optional offset ===
    bg_rect.y -= -20

    # === BUTTON DIMENSIONS AND POSITIONS RELATIVE TO BACKGROUND ===
    btn_w, btn_h = int(bg_w * 0.19), int(bg_h * 0.40)

    positions = [
        (0.50, 0.50), # Mid-center
    ]

    # New structure for topics: (text, action, hover_sound, button_image_filename)
    topics_data = [
        ("Quiz LVL 1", main_app.launch_quiz_lvl1, "hover_Lvl1_Topic1_ogg.ogg", "f01.png"),
    ]

    # === Build buttons with unique images ===
    buttons = []
    for (text, action, hover, img_filename), (rx, ry) in zip(topics_data, positions):
        x = bg_rect.left + int(rx * bg_w)
        y = bg_rect.top + int(ry * bg_h)

        scaled_button_image = None
        button_img_path = os.path.join(config.IMG_MAIN_PATH, img_filename)
        try:
            button_image = pygame.image.load(button_img_path).convert_alpha()
            scaled_button_image = pygame.transform.smoothscale(button_image, (btn_w, btn_h))
        except Exception as e:
            print(f"⚠️ Missing button image {button_img_path}: {e}. Using fallback rectangle for {text}.")

        rect = pygame.Rect(x - btn_w // 2, y - btn_h // 2, btn_w, btn_h)

        buttons.append({
            "text": text,
            "action": action,
            "hover": os.path.join(config.SOUND_MAIN_PATH, hover),
            "rect": rect,
            "image": scaled_button_image
        })

    # ✅ Pass level parameter
    draw_quiz_screen(screen, main_app, "Quiz Level 1", buttons, bg_image, bg_rect, level=1)


# ============================================================
# Quiz Level 2
# ============================================================
def quiz_two(screen, main_app):
    """Quiz Topics for Level 2"""
    if not pygame.display.get_surface():
        screen = pygame.display.set_mode(screen.get_size(), pygame.FULLSCREEN)
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    bg_path = os.path.join(config.IMG_MAIN_PATH, "bg-tr.png")

    try:
        bg_image = pygame.image.load(bg_path).convert_alpha()
    except Exception as e:
        print(f"⚠️ Missing {bg_path}: {e}")
        bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_image.fill((255, 255, 255))

    # === FLEXIBLE BACKGROUND ===
    bg_w = int(SCREEN_WIDTH * 0.95)
    bg_h = int(SCREEN_HEIGHT * 0.8)
    bg_image = pygame.transform.smoothscale(bg_image, (bg_w, bg_h))
    bg_rect = bg_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # === Optional offset ===
    bg_rect.y -= -20

    # === BUTTON DIMENSIONS AND POSITIONS RELATIVE TO BACKGROUND ===
    btn_w, btn_h = int(bg_w * 0.19), int(bg_h * 0.40)

    positions = [
        (0.50, 0.50), # Mid-center
    ]

    # New structure for topics: (text, action, hover_sound, button_image_filename)
    topics_data = [
        ("Quiz LVL 2", main_app.launch_quiz_lvl2, "hover_Lvl1_Topic1_ogg.ogg", "f01.png"),
    ]

    # === Build buttons with unique images ===
    buttons = []
    for (text, action, hover, img_filename), (rx, ry) in zip(topics_data, positions):
        x = bg_rect.left + int(rx * bg_w)
        y = bg_rect.top + int(ry * bg_h)

        scaled_button_image = None
        button_img_path = os.path.join(config.IMG_MAIN_PATH, img_filename)
        try:
            button_image = pygame.image.load(button_img_path).convert_alpha()
            scaled_button_image = pygame.transform.smoothscale(button_image, (btn_w, btn_h))
        except Exception as e:
            print(f"⚠️ Missing button image {button_img_path}: {e}. Using fallback rectangle for {text}.")

        rect = pygame.Rect(x - btn_w // 2, y - btn_h // 2, btn_w, btn_h)

        buttons.append({
            "text": text,
            "action": action,
            "hover": os.path.join(config.SOUND_MAIN_PATH, hover),
            "rect": rect,
            "image": scaled_button_image
        })

    # ✅ Pass level parameter
    draw_quiz_screen(screen, main_app, "Quiz Level 2", buttons, bg_image, bg_rect, level=2)


# ============================================================
# Quiz Level 3
# ============================================================
def quiz_three(screen, main_app):
    """Quiz Topics for Level 3"""
    if not pygame.display.get_surface():
        screen = pygame.display.set_mode(screen.get_size(), pygame.FULLSCREEN)
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    bg_path = os.path.join(config.IMG_MAIN_PATH, "bg-tr.png")

    try:
        bg_image = pygame.image.load(bg_path).convert_alpha()
    except Exception as e:
        print(f"⚠️ Missing {bg_path}: {e}")
        bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_image.fill((255, 255, 255))

    # === FLEXIBLE BACKGROUND ===
    bg_w = int(SCREEN_WIDTH * 0.95)
    bg_h = int(SCREEN_HEIGHT * 0.8)
    bg_image = pygame.transform.smoothscale(bg_image, (bg_w, bg_h))
    bg_rect = bg_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # === Optional offset ===
    bg_rect.y -= -20

    # === BUTTON DIMENSIONS AND POSITIONS RELATIVE TO BACKGROUND ===
    btn_w, btn_h = int(bg_w * 0.19), int(bg_h * 0.40)

    positions = [
        (0.50, 0.50), # Mid-center
    ]

    # New structure for topics: (text, action, hover_sound, button_image_filename)
    topics_data = [
        ("Quiz LVL 3", main_app.launch_quiz_lvl3, "hover_Lvl1_Topic1_ogg.ogg", "f01.png"),
    ]

    # === Build buttons with unique images ===
    buttons = []
    for (text, action, hover, img_filename), (rx, ry) in zip(topics_data, positions):
        x = bg_rect.left + int(rx * bg_w)
        y = bg_rect.top + int(ry * bg_h)

        scaled_button_image = None
        button_img_path = os.path.join(config.IMG_MAIN_PATH, img_filename)
        try:
            button_image = pygame.image.load(button_img_path).convert_alpha()
            scaled_button_image = pygame.transform.smoothscale(button_image, (btn_w, btn_h))
        except Exception as e:
            print(f"⚠️ Missing button image {button_img_path}: {e}. Using fallback rectangle for {text}.")

        rect = pygame.Rect(x - btn_w // 2, y - btn_h // 2, btn_w, btn_h)

        buttons.append({
            "text": text,
            "action": action,
            "hover": os.path.join(config.SOUND_MAIN_PATH, hover),
            "rect": rect,
            "image": scaled_button_image
        })

    # ✅ Pass level parameter
    draw_quiz_screen(screen, main_app, "Quiz Level 3", buttons, bg_image, bg_rect, level=3)


# ============================================================
# Dispatcher Function
# ============================================================
def run_quiz_topics(screen, main_app, level=1):
    """Automatically runs the correct quiz screen based on the level number."""
    quiz_map = {
        1: quiz_one,
        2: quiz_two,
        3: quiz_three,
    }

    func = quiz_map.get(level)
    if func:
        func(screen, main_app)
    else:
        print(f"⚠️ No quiz defined for Level {level}")
