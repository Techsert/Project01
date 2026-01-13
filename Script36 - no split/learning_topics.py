# learning_topics.py
import pygame, os, sys, arabic_reshaper
from bidi.algorithm import get_display
from screen_helpers import dynamic_font, confirm_popup
import config

# ============================================================
# Generic helper for all topic screens
# ============================================================
# In learning_topics.py, update draw_topic_screen function:

def draw_topic_screen(screen, main_app, title, buttons, bg_image, bg_rect):
    """Draws a full topic screen with buttons, profile, and exit icons."""
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    running = True
    last_hovered = None

    if bg_rect is None:
        bg_rect = bg_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((255, 255, 255))
        screen.blit(bg_image, bg_rect)

        # --- Title ---
        title_font = dynamic_font(SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, 
                                  config.ARABIC_FONT_BOLD, 0.04, bold=True)
        title_render = title_font.render(title, True, (180, 0, 200))
        screen.blit(title_render, title_render.get_rect(
            center=(SCREEN_WIDTH // 2, bg_rect.top - int(SCREEN_HEIGHT * 0.05))))

        # --- Buttons ---
        for b in buttons:
            if "image" in b and b["image"] is not None:
                screen.blit(b["image"], b["rect"])
            else:
                pygame.draw.rect(screen, (100, 100, 200), b["rect"])
                pygame.draw.rect(screen, (50, 50, 150), b["rect"], 3)

            button_text_color = (180, 0, 200)
            offset_x = 0
            offset_y = 120
            final_text_pos = (b["rect"].center[0] + offset_x, 
                            b["rect"].center[1] + offset_y)
            main_app.draw_arabic_text(b["text"], 0.04, button_text_color, final_text_pos)

        # --- Hover Sound ---
        hovered = next((i for i, b in enumerate(buttons) 
                       if b["rect"].collidepoint(mouse_pos)), None)
        if hovered is not None and hovered != last_hovered:
            # ✅ Use AudioManager through main_app
            main_app.play_hover_sound(buttons[hovered]["hover"])
        last_hovered = hovered

        # --- Profile + Exit ---
        if main_app.profile_icon and main_app.profile_rect:
            screen.blit(main_app.profile_icon, main_app.profile_rect)

        if main_app.exit_icon and main_app.exit_rect:
            screen.blit(main_app.exit_icon, main_app.exit_rect)

        # --- Events ---
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
                pygame.event.clear()
                return  # Exit immediatel
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if main_app.exit_rect.collidepoint(e.pos):
                    if main_app.confirm_popup("Exit the game?"):
                        pygame.quit()
                        sys.exit()
                elif main_app.profile_rect.collidepoint(e.pos):
                    # ✅ Audio context is now managed by AudioManager
                    main_app.open_profile_manager()
                else:
                    for b in buttons:
                        if b["rect"].collidepoint(e.pos):
                            # ✅ Push audio context before launching topic
                            if hasattr(main_app, 'audio_manager'):
                                main_app.audio_manager.push_audio_context()
                            b["action"]()
                            # Audio will be restored by video_slide_base when returning

        pygame.display.flip()
        clock.tick(60)



# ============================================================
# Learning Level 1 - Topics Selection Screen
# ============================================================
def topic_one(screen, main_app):
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
        (0.23, 0.50), # Mid-leftish
        (0.50, 0.50), # Mid-center
        (0.77, 0.50),  # Mid-rightish        
##        (0.20, 0.30), # Top-leftish
##        (0.50, 0.30), # Top-center
##        (0.80, 0.30), # Top-rightish
##        (0.20, 0.60), # Mid-leftish
##        (0.50, 0.60), # Mid-center
##        (0.80, 0.60)  # Mid-rightish
    ]

    # New structure for topics: (text, action, hover_sound, button_image_filename)
    topics_data = [
        ("Introduction", main_app.launch_learn_lvl1_T1, "hover_Lvl1_Topic1_ogg.ogg", "f01.png"),
        ("Alphabet Names", main_app.launch_learn_lvl1_T2, "hover_Lvl1_Topic2_ogg.ogg", "f02.png"),
        ("Revision", main_app.launch_learn_lvl1_T3, "hover_Lvl1_Topic3_ogg.ogg", "f03.png"),
##        ("الأعداد", main_app.launch_alphabit_sound, "hover_numbers.wav", "b4.png"),
##        ("الألوان", main_app.launch_alphabit_sound, "hover_colours.wav", "b5.png"),
##        ("الكَلِمات", main_app.launch_alphabit_sound, "hover_words.wav", "b6.png"),
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
    draw_topic_screen(screen, main_app, "Learning Level 1", buttons, bg_image, bg_rect)


# ============================================================
# Learning Level 2 - Topics Selection Screen
# ============================================================
def topic_two(screen, main_app):
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()  # Get from existing screen
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
        (0.23, 0.50), # Mid-leftish
        (0.50, 0.50), # Mid-center
        (0.77, 0.50),  # Mid-rightish        
##        (0.20, 0.30), # Top-leftish
##        (0.50, 0.30), # Top-center
##        (0.80, 0.30), # Top-rightish
##        (0.20, 0.60), # Mid-leftish
##        (0.50, 0.60), # Mid-center
##        (0.80, 0.60)  # Mid-rightish
    ]

    # New structure for topics: (text, action, hover_sound, button_image_filename)
    topics_data = [
        ("Introduction LVL2", main_app.launch_learn_lvl2_T1, "hover_Lvl1_Topic1_ogg.ogg", "f04.png"),
        ("Alphabet Sounds", main_app.launch_learn_lvl2_T2, "hover_Lvl1_Topic2_ogg.ogg", "f05.png"),
        ("LVL 2\n Revision", main_app.launch_learn_lvl2_T3, "hover_Lvl1_Topic3_ogg.ogg", "f06.png"),
##        ("الأعداد", main_app.launch_alphabit_sound, "hover_numbers.wav", "b4.png"),
##        ("الألوان", main_app.launch_alphabit_sound, "hover_colours.wav", "b5.png"),
##        ("الكَلِمات", main_app.launch_alphabit_sound, "hover_words.wav", "b6.png"),
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
