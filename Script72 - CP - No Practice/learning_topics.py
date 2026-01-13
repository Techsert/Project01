# learning_topics.py - UPDATED WITH IMAGE ICONS
import pygame, os, sys, arabic_reshaper
from bidi.algorithm import get_display
from screen_helpers import dynamic_font, confirm_popup, info_popup
from profile_system import get_unlock_status, is_topic_unlocked
import config

# ✅ NEW: Icon paths
ICONS_PATH = os.path.join(config.IMG_MAIN_PATH, "icons")
LOCK_ICON_PATH = os.path.join(ICONS_PATH, "lock_icon.png")

def load_lock_icon(size=(60, 60)):
    """Load lock icon image with fallback"""
    if os.path.exists(LOCK_ICON_PATH):
        try:
            img = pygame.image.load(LOCK_ICON_PATH).convert_alpha()
            return pygame.transform.smoothscale(img, size)
        except Exception as e:
            print(f"⚠️ Error loading lock icon: {e}")
    
    # Fallback: create red lock surface
    surf = pygame.Surface(size, pygame.SRCALPHA)
    # Draw padlock body
    lock_w, lock_h = size[0] // 2, size[1] // 2
    lock_x, lock_y = (size[0] - lock_w) // 2, size[1] // 2
    pygame.draw.rect(surf, (200, 0, 0, 220), (lock_x, lock_y, lock_w, lock_h), border_radius=5)
    # Draw padlock shackle
    shackle_rect = pygame.Rect(lock_x + lock_w//4, lock_y - lock_h//2, lock_w//2, lock_h//2)
    pygame.draw.arc(surf, (200, 0, 0, 220), shackle_rect, 0, 3.14, 5)
    return surf

# ============================================================
# Generic helper for all topic screens
# ============================================================
def draw_topic_screen(screen, main_app, title, buttons, bg_image, bg_rect, level=1):
    """Draws a full topic screen with buttons, profile, and exit icons."""
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    running = True
    last_hovered = None
    
    # ✅ Get unlock status for current profile
    profile_name = main_app.selected_profile.get("name") if main_app.selected_profile else None
    
    # ✅ Load lock icon once
    lock_icon = load_lock_icon(size=(80, 80))
    
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
            # ✅ FIXED: Check if THIS SPECIFIC TOPIC is unlocked
            topic_id = f"T{i + 1}"
            is_unlocked = is_topic_unlocked(profile_name, level, topic_id) if profile_name else (level == 1 and i == 0)
            
            # Draw button image (may be grayed out if locked)
            if "image" in b and b["image"] is not None:
                button_img = b["image"].copy()
                
                # ✅ Gray out locked topics
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
                
                # ✅ Draw lock ICON IMAGE if locked (not emoji)
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
                topic_id = f"T{i + 1}"
                is_unlocked = is_topic_unlocked(profile_name, level, topic_id) if profile_name else (level == 1 and i == 0)
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
                            topic_id = f"T{i + 1}"
                            is_unlocked = is_topic_unlocked(profile_name, level, topic_id) if profile_name else (level == 1 and i == 0)
                            
                            if is_unlocked:
                                b["action"]()
                            else:
                                # ✅ Show specific unlock requirement with OK button
                                if level == 1 and i == 0:
                                    msg = "This topic is always unlocked!"
                                elif i == 0 and level > 1:
                                    msg = f"Complete Quiz Level {level - 1}\nwith 90%+ to unlock Level {level}!"
                                else:
                                    msg = f"Complete the previous topic first!"
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
    btn_w, btn_h = int(bg_w * 0.19), int(bg_h * 0.40)
    
    positions = [
        (0.77, 0.50), # Mid-leftish
        (0.50, 0.50), # Mid-center
        (0.23, 0.50),  # Mid-rightish        
    ]

    # New structure for topics: (text, action, hover_sound, button_image_filename)
    topics_data = [
        ("", main_app.launch_learn_lvl1_T1, "hover_Lvl1_Topic1_ogg.ogg", "T_lvl1_T1.png"), # Introduction
        ("", main_app.launch_learn_lvl1_T2, "hover_Lvl1_Topic2_ogg.ogg", "T_lvl1_T2.png"), # Alphabet Names
        ("", main_app.launch_learn_lvl1_T3, "hover_Lvl1_Topic3_ogg.ogg", "T_lvl1_T3.png"), # Revision
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
        (0.81, 0.33),
        (0.62, 0.33),
        (0.38, 0.33),
        (0.19, 0.33), 
        (0.715, 0.67),
        (0.285, 0.67),
        (0.50, 0.67),
    ]


    topics_data = [
        ("", main_app.launch_learn_lvl2_T1, "hover_Lvl1_Topic1_ogg.ogg", "T_lvl2_T1.png"),  # Introduction
        ("", main_app.launch_learn_lvl2_T2, "hover_FAT-HA.ogg", "T_lvl2_T2.png"),            # FAT-HA
        ("", main_app.launch_learn_lvl2_T3, "hover_KAS-RA.ogg", "T_lvl2_T3.png"),        # KAS-RA
        ("", main_app.launch_learn_lvl2_T4, "hover_DA-MA.ogg", "T_lvl2_T4.png"),        # DA-MA
        ("", main_app.launch_learn_lvl2_T5, "hover_TAN-WEEN.ogg", "T_lvl2_T5.png"),        # TAN-WEEN
        ("", main_app.launch_learn_lvl2_T6, "hover_SO-KOON.ogg", "T_lvl2_T6.png"),        # SO-KON
        ("", main_app.launch_learn_lvl2_T7, "hover_Lvl1_Topic3_ogg.ogg", "T_lvl2_T7.png"),        # Revision
    ]

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
