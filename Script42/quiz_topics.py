# quiz_topics.py
import pygame, os, sys, arabic_reshaper
from bidi.algorithm import get_display
from screen_helpers import dynamic_font, confirm_popup
import config

# ============================================================
# Generic helper for all quiz screens
# ============================================================
def draw_quiz_screen(screen, main_app, title, buttons, bg_image, bg_rect):
    """Draws a quiz topic screen with buttons, profile, and exit icons."""
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    running = True
    last_hovered = None

    # If no custom bg_rect passed, center by default
    if bg_rect is None:
        bg_rect = bg_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    def show_confirm_popup(msg):
        """Use main_app's confirm_popup method."""
        return main_app.confirm_popup(msg)

    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((255, 255, 255))
        
        # Centered background draw
        screen.blit(bg_image, bg_rect)
        
        # --- Title ---
        title_font = dynamic_font(SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, 0.04, bold=True)
        # Use arabic_reshaper and get_display for Arabic titles if needed, but for "Learning Level 1" it's not
        title_render = title_font.render(title, True, (180, 0, 200))
        screen.blit(title_render, title_render.get_rect(center=(SCREEN_WIDTH // 2, bg_rect.top - int(SCREEN_HEIGHT * 0.05))))

        # --- Buttons ---
        for b in buttons:
            # Check if an image is provided for the button
            if "image" in b and b["image"] is not None:
                screen.blit(b["image"], b["rect"]) # Blit the image at the button's rect
            else:
                # Fallback to drawing a simple rectangle if no image is provided
                pygame.draw.rect(screen, (100, 100, 200), b["rect"]) # Example fallback color
                pygame.draw.rect(screen, (50, 50, 150), b["rect"], 3) # Border

            # Define your desired text color
            button_text_color = (180, 0, 200) # Black

            # Define your desired text position offset from the center
            # Positive values move right/down, negative values move left/up
            offset_x = 0  # No horizontal offset
            offset_y = 120 # Move text 5 pixels up

            # Calculate the final text position
            final_text_pos = (b["rect"].center[0] + offset_x, b["rect"].center[1] + offset_y)

            # Draw text on top of the button (image or rectangle)
            main_app.draw_arabic_text(b["text"], 0.04, button_text_color, final_text_pos)


        # --- Hover Sound ---
        hovered = next((i for i, b in enumerate(buttons) if b["rect"].collidepoint(mouse_pos)), None)
        if hovered is not None and hovered != last_hovered:
            main_app.play_hover_sound(buttons[hovered]["hover"])
        last_hovered = hovered

        # --- Profile + Exit + Back ---
        # Draw profile icon
        if main_app.profile_icon and main_app.profile_rect:
            screen.blit(main_app.profile_icon, main_app.profile_rect)

        # Draw exit icon
        if main_app.exit_icon and main_app.exit_rect:
            screen.blit(main_app.exit_icon, main_app.exit_rect)
        
        # --- Events ---
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                # ✅ Exit button click
                if main_app.exit_rect.collidepoint(e.pos):
                    if show_confirm_popup("Exit the game?"):
                        pygame.quit(); sys.exit()

                # ✅ Profile button click
                elif main_app.profile_rect.collidepoint(e.pos):
                    main_app.open_profile_manager()

                # ✅ Topic buttons
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
    scale_ratio = 0.86
    bg_w = int(SCREEN_WIDTH * 0.95)  # Set width to 70% of screen width
    bg_h = int(SCREEN_HEIGHT * 0.8) # Set height to 90% of screen height (might stretch if aspect ratio isn't natural)
    bg_image = pygame.transform.smoothscale(bg_image, (bg_w, bg_h))
    bg_rect = bg_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # === Optional offset ===
    bg_rect.y -= -20  # move slightly up if needed

    # === BUTTON DIMENSIONS AND POSITIONS RELATIVE TO BACKGROUND ===
    btn_w, btn_h = int(bg_w * 0.19), int(bg_h * 0.40) # Slightly larger buttons for images

    positions = [
##        (0.23, 0.50), # Mid-leftish
        (0.50, 0.50), # Mid-center
##        (0.77, 0.50),  # Mid-rightish        
##        (0.20, 0.30), # Top-leftish
##        (0.50, 0.30), # Top-center
##        (0.80, 0.30), # Top-rightish
##        (0.20, 0.60), # Mid-leftish
##        (0.50, 0.60), # Mid-center
##        (0.80, 0.60)  # Mid-rightish
    ]

    # New structure for topics: (text, action, hover_sound, button_image_filename)
    topics_data = [
        ("Quiz LVL 1", main_app.launch_quiz_lvl1, "hover_Lvl1_Topic1_ogg.ogg", "f01.png"),
##        ("Alphabet Names", main_app.launch_learn_lvl1_T2, "hover_Lvl1_Topic2_ogg.ogg", "f02.png"),
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

        # The rect determines clickable area and position for blitting
        rect = pygame.Rect(x - btn_w // 2, y - btn_h // 2, btn_w, btn_h)

        buttons.append({
            "text": text,
            "action": action,
            "hover": os.path.join(config.SOUND_MAIN_PATH, hover),
            "rect": rect,
            "image": scaled_button_image # Add the scaled image to the button data
        })

    # Now call the draw loop
    draw_quiz_screen(screen, main_app, "Quiz Level 1", buttons, bg_image, bg_rect)


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
    scale_ratio = 0.86
    bg_w = int(SCREEN_WIDTH * 0.95)  # Set width to 70% of screen width
    bg_h = int(SCREEN_HEIGHT * 0.8) # Set height to 90% of screen height (might stretch if aspect ratio isn't natural)
    bg_image = pygame.transform.smoothscale(bg_image, (bg_w, bg_h))
    bg_rect = bg_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # === Optional offset ===
    bg_rect.y -= -20  # move slightly up if needed

    # === BUTTON DIMENSIONS AND POSITIONS RELATIVE TO BACKGROUND ===
    btn_w, btn_h = int(bg_w * 0.19), int(bg_h * 0.40) # Slightly larger buttons for images

    positions = [
##        (0.23, 0.50), # Mid-leftish
        (0.50, 0.50), # Mid-center
##        (0.77, 0.50),  # Mid-rightish        
##        (0.20, 0.30), # Top-leftish
##        (0.50, 0.30), # Top-center
##        (0.80, 0.30), # Top-rightish
##        (0.20, 0.60), # Mid-leftish
##        (0.50, 0.60), # Mid-center
##        (0.80, 0.60)  # Mid-rightish
    ]

    # New structure for topics: (text, action, hover_sound, button_image_filename)
    topics_data = [
        ("Quiz LVL 2", main_app.launch_quiz_lvl2, "hover_Lvl1_Topic1_ogg.ogg", "f01.png"),
##        ("Alphabet Names", main_app.launch_learn_lvl1_T2, "hover_Lvl1_Topic2_ogg.ogg", "f02.png"),
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

        # The rect determines clickable area and position for blitting
        rect = pygame.Rect(x - btn_w // 2, y - btn_h // 2, btn_w, btn_h)

        buttons.append({
            "text": text,
            "action": action,
            "hover": os.path.join(config.SOUND_MAIN_PATH, hover),
            "rect": rect,
            "image": scaled_button_image # Add the scaled image to the button data
        })

    # Now call the draw loop
    draw_quiz_screen(screen, main_app, "Quiz Level 2", buttons, bg_image, bg_rect)



# ============================================================
# Quiz Level 3
# ============================================================
def quiz_three(screen, main_app):
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
    scale_ratio = 0.86
    bg_w = int(SCREEN_WIDTH * 0.95)  # Set width to 70% of screen width
    bg_h = int(SCREEN_HEIGHT * 0.8) # Set height to 90% of screen height (might stretch if aspect ratio isn't natural)
    bg_image = pygame.transform.smoothscale(bg_image, (bg_w, bg_h))
    bg_rect = bg_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # === Optional offset ===
    bg_rect.y -= -20  # move slightly up if needed

    # === BUTTON DIMENSIONS AND POSITIONS RELATIVE TO BACKGROUND ===
    btn_w, btn_h = int(bg_w * 0.19), int(bg_h * 0.40) # Slightly larger buttons for images

    positions = [
##        (0.23, 0.50), # Mid-leftish
        (0.50, 0.50), # Mid-center
##        (0.77, 0.50),  # Mid-rightish        
##        (0.20, 0.30), # Top-leftish
##        (0.50, 0.30), # Top-center
##        (0.80, 0.30), # Top-rightish
##        (0.20, 0.60), # Mid-leftish
##        (0.50, 0.60), # Mid-center
##        (0.80, 0.60)  # Mid-rightish
    ]

    # New structure for topics: (text, action, hover_sound, button_image_filename)
    topics_data = [
        ("Quiz LVL 3", main_app.launch_quiz_lvl3, "hover_Lvl1_Topic1_ogg.ogg", "f01.png"),
##        ("Alphabet Names", main_app.launch_learn_lvl1_T2, "hover_Lvl1_Topic2_ogg.ogg", "f02.png"),
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

        # The rect determines clickable area and position for blitting
        rect = pygame.Rect(x - btn_w // 2, y - btn_h // 2, btn_w, btn_h)

        buttons.append({
            "text": text,
            "action": action,
            "hover": os.path.join(config.SOUND_MAIN_PATH, hover),
            "rect": rect,
            "image": scaled_button_image # Add the scaled image to the button data
        })

    # Now call the draw loop
    draw_quiz_screen(screen, main_app, "Quiz Level 3", buttons, bg_image, bg_rect)

# ============================================================
# Dispatcher Function
# ============================================================
def run_quiz_topics(screen, main_app, level=1):
    """Automatically runs the correct quiz screen based on the level number."""
    quiz_map = {
        1: quiz_one,
        2: quiz_two,
        3: quiz_three,
        # Add more quiz levels here: 3: quiz_three, 4: quiz_four, etc.
    }

    func = quiz_map.get(level)
    if func:
        func(screen, main_app)
    else:
        print(f"⚠️ No quiz defined for Level {level}")
