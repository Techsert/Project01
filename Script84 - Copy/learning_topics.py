# learning_topics.py - UPDATED WITH IMAGE ICONS
import pygame, os, sys, arabic_reshaper
from bidi.algorithm import get_display
from screen_helpers import dynamic_font, confirm_popup, info_popup, load_lock_icon
from profile_system import get_unlock_status, is_item_unlocked
import config

# ✅ NEW: Icon paths
ICONS_PATH = os.path.join(config.IMG_MAIN_PATH, "icons")
LOCK_ICON_PATH = os.path.join(ICONS_PATH, "lock_icon.png")

# ============================================================
# Generic helper for all topic screens
# ============================================================
def draw_topic_screen(screen, main_app, title, buttons, bg_image, bg_rect, level=1):
    """Draws a full topic screen with buttons, profile, and exit icons."""
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    running = True
    last_hovered = None

    # Get profile name
    profile_name = main_app.selected_profile.get("name") if main_app.selected_profile else None
    
    # ✅ Load lock icon once
    lock_icon = load_lock_icon(LOCK_ICON_PATH, size=(80, 80))
    
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

        # Buttons
        for i, b in enumerate(buttons):
            # ✅ NEW: Determine unlock status based on explicit ID in button data
            item_id = b.get("id", f"T{i+1}") # Fallback to T1, T2 if no ID provided
            # Use the new unified check from profile_system
            is_unlocked = is_item_unlocked(profile_name, level, item_id) if profile_name else (level == 1 and item_id == "T1")
            
            # Draw button image (may be grayed out if locked)
            if "image" in b and b["image"] is not None:
                button_img = b["image"].copy()                
                screen.blit(button_img, b["rect"])
                
                # Draw lock ICON if locked
                if not is_unlocked:
                    lock_rect = lock_icon.get_rect(center=b["rect"].center)
                    screen.blit(lock_icon, lock_rect)
            else:
                color = (100, 100, 200) if is_unlocked else (100, 100, 100)
                pygame.draw.rect(screen, color, b["rect"])
                pygame.draw.rect(screen, (50, 50, 150), b["rect"], 3)
                
                # Draw lock icon on fallback rect too
                if not is_unlocked:
                    lock_rect = lock_icon.get_rect(center=b["rect"].center)
                    screen.blit(lock_icon, lock_rect)

            # Draw text
            button_text_color = (180, 0, 200) if is_unlocked else (150, 150, 150)
            offset_x = 0
            offset_y = 120
            final_text_pos = (b["rect"].center[0] + offset_x, b["rect"].center[1] + offset_y)
            main_app.draw_arabic_text(b["text"], 0.04, button_text_color, final_text_pos)

        # Hover Sound (only for unlocked topics)
        hovered = None
        for i, b in enumerate(buttons):
            if b["rect"].collidepoint(mouse_pos):
                # ✅ Check unlock using ID
                item_id = b.get("id", f"T{i+1}")
                is_unlocked = is_item_unlocked(profile_name, level, item_id) if profile_name else (level == 1 and item_id == "T1")
                
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
                    # Check button clicks
                    for i, b in enumerate(buttons):
                        if b["rect"].collidepoint(e.pos):
                            item_id = b.get("id", f"T{i+1}")
                            is_unlocked = is_item_unlocked(profile_name, level, item_id) if profile_name else (level == 1 and item_id == "T1")
                            
                            if is_unlocked:
                                b["action"]()
                            else:
                                # ✅ Custom locked messages based on ID type
                                if item_id.startswith("Q"):
                                    msg = "Complete all topics and practices\nto unlock the Quiz!"
                                elif item_id.startswith("P"):
                                    msg = "Complete the previous topics first!"
                                elif item_id == "T1" and level > 1:
                                    msg = f"Pass Quiz Level {level-1} with 90%+\nto unlock Level {level}!"
                                else:
                                    msg = "Complete the previous topic first!"
                                
                                info_popup(screen, msg, lambda size, bold=False: dynamic_font(SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, size / SCREEN_HEIGHT, bold))
                            break
                    

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
    bg_w = int(SCREEN_WIDTH * 0.95)
    bg_h = int(SCREEN_HEIGHT * 0.8)
    bg_image = pygame.transform.smoothscale(bg_image, (bg_w, bg_h))
    bg_rect = bg_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    bg_rect.y -= 0

    # === BUTTON DIMENSIONS AND POSITIONS RELATIVE TO BACKGROUND ===
    btn_w, btn_h = int(bg_w * 0.14), int(bg_h * 0.30)
    
    positions = [
        (0.82, 0.33), # Introduction
        (0.66, 0.63), # Alphabet Names
        (0.50, 0.33),  # Revision
        (0.34, 0.63),  # P1
        (0.18, 0.33),  # Quiz One
    ]

    # New structure for topics: (text, action, hover_sound, button_image_filename)
    topics_data = [
        ("", main_app.launch_learn_lvl1_T1, "hover_Lvl1_Topic1_ogg.ogg", "T_lvl1_T1.png", "T1"), # Introduction
        ("", main_app.launch_learn_lvl1_T2, "hover_Lvl1_Topic2_ogg.ogg", "T_lvl1_T2.png", "T2"), # Alphabet Names
        ("", main_app.launch_learn_lvl1_T3, "hover_Lvl1_Topic3_ogg.ogg", "T_lvl1_T3.png", "T3"), # Revision
        ("", main_app.launch_practice_lvl1_P1, "hover_practice.ogg", "T_lvl1_T4.png", "P1"),  # ✅ Practice 1
        ("", main_app.launch_quiz_lvl1, "hover_quiz_lvl_1.ogg", "Q_lvl1.png", "Q1"),
    ]

    # === Build buttons with unique images ===
    buttons = []
    for (text, action, hover, img_filename, item_id), (rx, ry) in zip(topics_data, positions):
        x = bg_rect.left + int(rx * bg_w)
        y = bg_rect.top + int(ry * bg_h)

        # Image loading logic...
        scaled_button_image = None
        button_img_path = os.path.join(config.IMG_MAIN_PATH, img_filename)
        try:
            button_image = pygame.image.load(button_img_path).convert_alpha()
            scaled_button_image = pygame.transform.smoothscale(button_image, (btn_w, btn_h))
        except: pass

        rect = pygame.Rect(x - btn_w // 2, y - btn_h // 2, btn_w, btn_h)

        buttons.append({
            "text": text,
            "action": action,
            "hover": os.path.join(config.SOUND_MAIN_PATH, hover),
            "rect": rect,
            "image": scaled_button_image,
            "id": item_id # ✅ Pass explicit ID
        })

    draw_topic_screen(screen, main_app, "Learning Level 1", buttons, bg_image, bg_rect, level=1)


# ============================================================
# Learning Level 2 - Topics Selection Screen
# ============================================================
def topic_two(screen, main_app):
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
    bg_rect.y -= 0

    # === BUTTON DIMENSIONS AND POSITIONS RELATIVE TO BACKGROUND ===
    btn_w, btn_h = int(bg_w * 0.14), int(bg_h * 0.30)

    positions = [
        (0.82, 0.33), # Introduction
        (0.66, 0.63), # FAT-HAH
        (0.50, 0.33),  # Revision
        (0.34, 0.63),  # P2
        (0.18, 0.33),  # Quiz Two
    ]


    topics_data = [
        ("", main_app.launch_learn_lvl2_T1, "hover_Lvl1_Topic1_ogg.ogg", "T_lvl2_T1.png", "T1"),        # Introduction
        ("", main_app.launch_learn_lvl2_T2, "hover_FAT-HA.ogg", "T_lvl2_T2.png", "T2"),                 # FAT-HAH
##        ("", main_app.launch_learn_lvl2_T3, "hover_KAS-RA.ogg", "T_lvl2_T3.png"),        # KAS-RA
##        ("", main_app.launch_learn_lvl2_T4, "hover_DA-MA.ogg", "T_lvl2_T4.png"),        # DA-MA
##        ("", main_app.launch_learn_lvl2_T5, "hover_TAN-WEEN.ogg", "T_lvl2_T5.png"),        # TAN-WEEN
##        ("", main_app.launch_learn_lvl2_T6, "hover_SO-KOON.ogg", "T_lvl2_T6.png"),        # SO-KON
        ("", main_app.launch_learn_lvl2_T7, "hover_Lvl1_Topic3_ogg.ogg", "T_lvl2_T7.png", "T3"),        # Revision
        ("", main_app.launch_practice_lvl2_P1, "hover_practice.ogg", "T_lvl1_T4.png", "P1"),            # Practice
        ("", main_app.launch_quiz_lvl2, "hover_Lvl1_Topic1_ogg.ogg", "Q_lvl2.png", "Q2"),               # Quiz
##        ("L2P2", main_app.launch_practice_lvl2_P2, "hover_Lvl1_Topic3_ogg.ogg", "T_lvl2_T7.png"),  
    ]

    buttons = []
    for (text, action, hover, img_filename, item_id), (rx, ry) in zip(topics_data, positions):
        x = bg_rect.left + int(rx * bg_w)
        y = bg_rect.top + int(ry * bg_h)

        # Image loading logic...
        scaled_button_image = None
        button_img_path = os.path.join(config.IMG_MAIN_PATH, img_filename)
        try:
            button_image = pygame.image.load(button_img_path).convert_alpha()
            scaled_button_image = pygame.transform.smoothscale(button_image, (btn_w, btn_h))
        except: pass

        rect = pygame.Rect(x - btn_w // 2, y - btn_h // 2, btn_w, btn_h)

        buttons.append({
            "text": text,
            "action": action,
            "hover": os.path.join(config.SOUND_MAIN_PATH, hover),
            "rect": rect,
            "image": scaled_button_image,
            "id": item_id # ✅ Pass explicit ID
        })

    draw_topic_screen(screen, main_app, "Learning Level 2", buttons, bg_image, bg_rect, level=2)


# ============================================================
# Dispatcher Function
# ============================================================
def run_learning_topics(screen, main_app, level=1):
    """Automatically runs the correct topic screen based on the level number."""
    topic_map = {
        1: topic_one,
        2: topic_two,
    }

    func = topic_map.get(level)
    if func:
        func(screen, main_app)
    else:
        print(f"⚠️ No topic defined for Level {level}")
