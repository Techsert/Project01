import os
import sys
import pygame
from screen_helpers import confirm_popup, load_font, load_icon
from profile_system import (
    load_profiles, save_profiles, create_profile, delete_profile,
    AVAILABLE_AVATARS, AVAILABLE_REWARDS, get_progress_summary
)

import config

pygame.init()

# ✅ FIX: Load fonts using config paths
FONT = load_font(config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, 32, default_font_name="Arial")
TITLE_FONT = load_font(config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, 48, bold=True, default_font_name="Arial")
BUTTON_FONT = load_font(config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, 32, bold=True, default_font_name="Arial")

# ✅ FIX: Use config paths
AVATAR_PATH = config.AVATAR_PROFILES_PATH
IMG_PATH = config.IMG_MAIN_PATH
EXIT_IMG = os.path.join(IMG_PATH, "exit_icon.png")

# ✅ NEW: Icon paths
ICONS_PATH = os.path.join(IMG_PATH, "icons")
LOCK_ICON_PATH = os.path.join(ICONS_PATH, "lock_icon.png")
UNLOCK_ICON_PATH = os.path.join(ICONS_PATH, "unlock_icon.png")
PARTIAL_ICON_PATH = os.path.join(ICONS_PATH, "partial_icon.png")
TROPHY_ICON_PATH = os.path.join(ICONS_PATH, "trophy_icon.png")
STAR_ICON_PATH = os.path.join(ICONS_PATH, "star_icon.png")
MEDAL_ICON_PATH = os.path.join(ICONS_PATH, "medal_icon.png")
WARNING_ICON_PATH = os.path.join(ICONS_PATH, "warning_icon.png")


# ====================== Helpers ======================
def _load_avatar_images():
    return {
        a: pygame.image.load(os.path.join(AVATAR_PATH, a)).convert_alpha()
        for a in AVAILABLE_AVATARS
    }

# ================== Profile Selection ==================
def run_profile_screen(screen, SCREEN_WIDTH_PARAM, SCREEN_HEIGHT_PARAM):
    """
    Startup selector:
      - Click profile -> returns profile dict
      - 'New Profile' -> create form
      - Delete icon per profile
      - Exit button (bottom-right)
    """
    # ✅ FIX: Get dimensions from screen, not from config
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    
    clock = pygame.time.Clock()
    avatar_images = _load_avatar_images()
    profiles = load_profiles() or []

    # State
    mode = "select"  # "select" or "create"
    current_input = {"name": "", "age": ""}
    active_input = None
    selected_avatar = AVAILABLE_AVATARS[0]
    cursor_visible, cursor_timer = True, 0

    # ✅ FIX: Now SCREEN_WIDTH/HEIGHT are defined
    create_button = pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.85, SCREEN_WIDTH * 0.2, 60)
    name_rect = pygame.Rect(SCREEN_WIDTH // 2 - 180, 220, 360, 60)
    age_rect  = pygame.Rect(SCREEN_WIDTH // 2 - 180, 300, 360, 60)

    # Exit icon - ✅ Match size with main app
    try:
        exit_icon = pygame.image.load(EXIT_IMG).convert_alpha()
        icon_width = int(SCREEN_WIDTH * config.EXIT_ICON_WIDTH_RATIO)
        icon_height = int(SCREEN_HEIGHT * config.EXIT_ICON_HEIGHT_RATIO)
        exit_icon = pygame.transform.smoothscale(exit_icon, (icon_width, icon_height))
    except Exception as e:
        print(f"Error loading exit_icon: {e}. Using placeholder.")
        icon_width = int(SCREEN_WIDTH * config.EXIT_ICON_WIDTH_RATIO)
        icon_height = int(SCREEN_HEIGHT * config.EXIT_ICON_HEIGHT_RATIO)
        exit_icon = pygame.Surface((icon_width, icon_height), pygame.SRCALPHA)
        exit_icon.fill((200,0,0,200))
    exit_rect = exit_icon.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))  # ✅ Match position too

    # ---------- draw: profiles grid ----------
    def draw_profiles():
        screen.fill((245, 245, 245))
        title = TITLE_FONT.render("Select Your Profile", True, (0, 0, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 60))

        # --- Calculate grid layout dynamically ---
        CARD_W, CARD_H = 150, 150
        MARGIN_X, MARGIN_Y = 80, 100
        cols = 4  # how many avatars per row

        if not profiles:
            info = FONT.render("No profiles found. Click 'New Profile' to create one.", True, (100,100,100))
            screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, SCREEN_HEIGHT//2))
        else:
            # === Dynamic Centered Rows ===
            rows = (len(profiles) + cols - 1) // cols
            start_y = (SCREEN_HEIGHT - (rows * (CARD_H + MARGIN_Y))) // 2 + 150

            for row in range(rows):
                start_idx = row * cols
                end_idx = min(start_idx + cols, len(profiles))
                row_profiles = profiles[start_idx:end_idx]
                row_count = len(row_profiles)

                # Center this specific row horizontally
                total_row_width = row_count * CARD_W + (row_count - 1) * MARGIN_X
                start_x = (SCREEN_WIDTH - total_row_width) // 2 + CARD_W // 2

                x = start_x
                y = start_y + row * (CARD_H + MARGIN_Y)

                for profile in row_profiles:
                    name = profile.get("name", "")
                    avatar_name = profile.get("avatar", AVAILABLE_AVATARS[0])
                    avatar = avatar_images.get(avatar_name)
                    if avatar:
                        avatar_thumb = pygame.transform.smoothscale(avatar, (CARD_W, CARD_H))
                        rect = avatar_thumb.get_rect(center=(x, y))
                        screen.blit(avatar_thumb, rect)

                        text = FONT.render(name, True, (0, 0, 0))
                        screen.blit(text, (x - text.get_width() // 2, y + CARD_H // 2 + 20))

                        pygame.draw.rect(screen, (0, 0, 0), rect, 3)
                        profile["rect"] = rect

                        # delete icon
                        del_rect = pygame.Rect(rect.right - 25, rect.top - 10, 25, 25)
                        pygame.draw.rect(screen, (255, 0, 0), del_rect)
                        pygame.draw.line(screen, (255, 255, 255), del_rect.topleft, del_rect.bottomright, 2)
                        pygame.draw.line(screen, (255, 255, 255),
                                         (del_rect.left, del_rect.bottom), (del_rect.right, del_rect.top), 2)
                        profile["delete_rect"] = del_rect

                    x += CARD_W + MARGIN_X

        # New Profile button
        pygame.draw.rect(screen, (255, 102, 0), create_button, border_radius=15)
        label = FONT.render("New Profile", True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=create_button.center))

        # Exit icon
        screen.blit(exit_icon, exit_rect)

    # ---------- draw: create form ----------
    def draw_create_form():
        screen.fill((245, 245, 245))
        t = TITLE_FONT.render("Create New Profile", True, (0, 0, 0))
        screen.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2, 60))

        # Name
        screen.blit(FONT.render("Name:", True, (0,0,0)), (name_rect.x - 110, name_rect.y + 10))
        pygame.draw.rect(screen, (255,255,255), name_rect)
        pygame.draw.rect(screen, (0,0,0), name_rect, 2)
        name_surf = FONT.render(current_input["name"], True, (0,0,0))
        name_box = name_surf.get_rect(center=name_rect.center)
        screen.blit(name_surf, name_box)

        # caret
        if active_input == "name" and cursor_visible:
            pygame.draw.line(screen, (0,0,0), (name_box.right+6, name_rect.y+8), (name_box.right+6, name_rect.bottom-8), 2)

        # Age
        screen.blit(FONT.render("Age:", True, (0,0,0)), (age_rect.x - 80, age_rect.y + 10))
        pygame.draw.rect(screen, (255,255,255), age_rect)
        pygame.draw.rect(screen, (0,0,0), age_rect, 2)
        age_surf = FONT.render(current_input["age"], True, (0,0,0))
        age_box = age_surf.get_rect(center=age_rect.center)
        screen.blit(age_surf, age_box)

        if active_input == "age" and cursor_visible:
            pygame.draw.line(screen, (0,0,0), (age_box.right+6, age_rect.y+8), (age_box.right+6, age_rect.bottom-8), 2)

        # Avatar selection (centered row)
        AVATAR_SIZE = 120
        SPACING_X = 50
        y = int(SCREEN_HEIGHT * 0.7)

        # dynamically center the row
        row_count = len(AVAILABLE_AVATARS)
        total_row_width = row_count * AVATAR_SIZE + (row_count - 1) * SPACING_X
        start_x = (SCREEN_WIDTH - total_row_width) // 2 + AVATAR_SIZE // 2

        # draw avatars centered
        x = start_x
        for a in AVAILABLE_AVATARS:
            thumb = pygame.transform.smoothscale(avatar_images[a], (AVATAR_SIZE, AVATAR_SIZE))
            r = thumb.get_rect(center=(x, y))
            screen.blit(thumb, r)
            if a == selected_avatar:
                pygame.draw.rect(screen, (255, 102, 0), r, 4, border_radius=10)
            avatar_images[a + "_rect"] = r
            x += AVATAR_SIZE + SPACING_X

        # Save button
        pygame.draw.rect(screen, (255, 102, 0), create_button, border_radius=15)
        screen.blit(FONT.render("Save", True, (255,255,255)), FONT.render("Save", True, (255,255,255)).get_rect(center=create_button.center))

        # Exit icon
        screen.blit(exit_icon, exit_rect)

    # ---------------- Main loop ----------------
    while True:
        mouse = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            elif e.type == pygame.MOUSEBUTTONDOWN:
                # Exit app
                if exit_rect.collidepoint(mouse):
                    if confirm_popup(screen, "Exit the game?", lambda size, bold=False: load_font(config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, size, bold)):
                        pygame.quit(); sys.exit()

                if mode == "select":
                    # delete or select
                    for profile in profiles[:]:
                        if "delete_rect" in profile and profile["delete_rect"].collidepoint(mouse):
                            if confirm_popup(screen, f"Delete '{profile['name']}'?", lambda size, bold=False: load_font(config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, size, bold)):
                                delete_profile(profile["name"])
                                profiles.remove(profile)
                                clean = [{k:v for k,v in p.items() if k not in ("rect","delete_rect")} for p in profiles]
                                save_profiles(clean)
                                profiles = load_profiles() or []
                            break
                        elif "rect" in profile and profile["rect"].collidepoint(mouse):
                            # select (return to main app)
                            return {k:v for k,v in profile.items() if k not in ("rect","delete_rect")}

                    # create new
                    if create_button.collidepoint(mouse):
                        mode = "create"

                elif mode == "create":
                    # focus fields
                    if name_rect.collidepoint(mouse): active_input = "name"
                    elif age_rect.collidepoint(mouse): active_input = "age"
                    else: active_input = None

                    # avatar selection
                    for a in AVAILABLE_AVATARS:
                        r = avatar_images.get(a + "_rect")
                        if r and r.collidepoint(mouse):
                            selected_avatar = a

                    # save new profile
                    if create_button.collidepoint(mouse):
                        if current_input["name"] and current_input["age"]:
                            p = create_profile(current_input["name"], current_input["age"], selected_avatar)
                            return p

            elif e.type == pygame.KEYDOWN and mode == "create" and active_input:
                if e.key == pygame.K_BACKSPACE:
                    current_input[active_input] = current_input[active_input][:-1]
                else:
                    ch = e.unicode
                    if active_input == "name" and ch.isalpha() and len(current_input["name"]) < 8:
                        current_input["name"] += ch
                    elif active_input == "age" and ch.isdigit() and len(current_input["age"]) < 2:
                        current_input["age"] += ch

        # draw
        if mode == "select":
            draw_profiles()
        else:
            draw_create_form()

        # caret blink
        cursor_timer += clock.get_time()
        if cursor_timer >= 500:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        pygame.display.flip()
        clock.tick(60)


# ================== Profile Manage (from main app) ==================
def run_profile_manage_screen(screen, SCREEN_WIDTH_PARAM, SCREEN_HEIGHT_PARAM, profile):
    """
    Manage current profile from main menu:
      - View avatar, name, age
      - Edit name/age (Edit -> Save)
      - Change avatar
      - View achievements (scrollable grid)
      - View progress (bottom section)
      - Delete profile
    """
    # ✅ FIX: Get dimensions from screen
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    
    clock = pygame.time.Clock()
    avatar_images = _load_avatar_images()

    # ✅ NEW: Load icon images once (cached)
    icon_cache = {
        "lock": load_icon(LOCK_ICON_PATH, (30, 30), (200, 0, 0)),
        "unlock": load_icon(UNLOCK_ICON_PATH, (30, 30), (0, 200, 0)),
        "partial": load_icon(PARTIAL_ICON_PATH, (30, 30), (220, 180, 0)),
        "trophy": load_icon(TROPHY_ICON_PATH, (35, 35), (255, 215, 0)),
        "star": load_icon(STAR_ICON_PATH, (35, 35), (0, 150, 200)),
        "medal": load_icon(MEDAL_ICON_PATH, (35, 35), (200, 150, 0)),
        "warning": load_icon(WARNING_ICON_PATH, (35, 35), (200, 100, 100)),
    }

    # --- State ---
    working = dict(profile)
    editing = False
    active_input = None
    cursor_visible, cursor_timer = True, 0
    zoomed_reward = None

    # --- Rewards ---
    reward_cards = []
    try:
        for r in AVAILABLE_REWARDS:
            path = os.path.join(config.REWARDS_CARDS_PATH, r)
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                reward_cards.append((r, img))
    except Exception as e:
        print("Reward load error:", e)

    # --- Scrollable grid setup ---
    scroll_offset = 0
    max_scroll = 0
    scroll_speed = 40

    # --- UI Rects ---
    back_btn = pygame.Rect(80, SCREEN_HEIGHT - 100, 180, 60)
    edit_btn = pygame.Rect(SCREEN_WIDTH //4 - 400, int(SCREEN_HEIGHT * 0.05), 160, 60)
    save_btn = pygame.Rect(SCREEN_WIDTH //4 - 400, int(SCREEN_HEIGHT * 0.10), 160, 60)
    del_btn  = pygame.Rect(SCREEN_WIDTH //4, SCREEN_HEIGHT - 100, 180, 60)

    # Name & Age input fields (resolution-scaled)
    NAME_X_RATIO = 0.05
    NAME_Y_RATIO = 0.07
    AGE_X_RATIO  = 0.05
    AGE_Y_RATIO  = 0.11
    BOX_W_RATIO  = 0.05
    BOX_H_RATIO  = 0.03

    name_rect = pygame.Rect(
        int(SCREEN_WIDTH * NAME_X_RATIO),
        int(SCREEN_HEIGHT * NAME_Y_RATIO),
        int(SCREEN_WIDTH * BOX_W_RATIO),
        int(SCREEN_HEIGHT * BOX_H_RATIO)
    )

    age_rect = pygame.Rect(
        int(SCREEN_WIDTH * AGE_X_RATIO),
        int(SCREEN_HEIGHT * AGE_Y_RATIO),
        int(SCREEN_WIDTH * BOX_W_RATIO),
        int(SCREEN_HEIGHT * BOX_H_RATIO)
    )

    def draw_progress_section():
        """Draw progress and achievements section with IMAGE ICONS"""
        # Get progress summary
        progress_summary = get_progress_summary(profile.get("name", ""))
        
        # Progress Section Title
        PROGRESS_TITLE_X_RATIO = 0.60
        PROGRESS_TITLE_Y_RATIO = 0.07
        
        progress_title = TITLE_FONT.render("Progress & Achievements", True, (0, 0, 0))
        title_x = int(SCREEN_WIDTH * PROGRESS_TITLE_X_RATIO)
        title_y = int(SCREEN_HEIGHT * PROGRESS_TITLE_Y_RATIO)
        screen.blit(progress_title, (title_x, title_y))
        
        # Learning Progress
        LEARNING_START_Y = 0.15
        TEXT_X = 0.60
        
        learning_label = FONT.render("Learning Levels:", True, (0, 100, 0))
        screen.blit(learning_label, (int(SCREEN_WIDTH * TEXT_X), int(SCREEN_HEIGHT * LEARNING_START_Y)))
        
        # Show completed learning levels
        completed_learning = progress_summary.get("learning_completed", [])
        if completed_learning:
            for i, level in enumerate(sorted(completed_learning)):
                y_pos = LEARNING_START_Y + 0.04 + (i * 0.03)
                level_text = FONT.render(f"Level {level} Complete", True, (0, 150, 0))
                
                # ✅ Calculate vertical alignment for icon and text
                text_y = int(SCREEN_HEIGHT * y_pos)
                text_height = level_text.get_height()
                icon_height = icon_cache["unlock"].get_height()
                
                # Center icon vertically with text
                icon_x = int(SCREEN_WIDTH * (TEXT_X + 0.02))
                icon_y = text_y + (text_height - icon_height) // 2
                
                screen.blit(icon_cache["unlock"], (icon_x, icon_y))
                screen.blit(level_text, (icon_x + 35, text_y))
        else:
            no_learning = FONT.render("No levels completed yet", True, (150, 150, 150))
            screen.blit(no_learning, (int(SCREEN_WIDTH * (TEXT_X + 0.02)), int(SCREEN_HEIGHT * (LEARNING_START_Y + 0.04))))
        
        # Quiz Progress
        QUIZ_START_Y = 0.32
        
        quiz_label = FONT.render("Quiz Scores:", True, (0, 100, 200))
        screen.blit(quiz_label, (int(SCREEN_WIDTH * TEXT_X), int(SCREEN_HEIGHT * QUIZ_START_Y)))
        
        # Show quiz scores with IMAGE ICONS
        quiz_scores = progress_summary.get("quiz_scores", {})
        if quiz_scores:
            for i, (level, score) in enumerate(sorted(quiz_scores.items())):
                y_pos = QUIZ_START_Y + 0.04 + (i * 0.03)
                
                # ✅ Choose icon based on score
                if score == 100:
                    color = (0, 200, 0)  # Perfect - green
                    icon_img = icon_cache["trophy"]
                elif score >= 90:
                    color = (0, 150, 200)  # Good - blue
                    icon_img = icon_cache["star"]
                elif score >= 70:
                    color = (200, 150, 0)  # OK - yellow
                    icon_img = icon_cache["medal"]
                else:
                    color = (200, 100, 100)  # Needs improvement - red
                    icon_img = icon_cache["warning"]
                
                score_text = FONT.render(f"Level {level}: {score}% (Best)", True, color)
                
                # ✅ Calculate vertical alignment for icon and text
                text_y = int(SCREEN_HEIGHT * y_pos)
                text_height = score_text.get_height()
                icon_height = icon_img.get_height()
                
                # Center icon vertically with text
                icon_x = int(SCREEN_WIDTH * (TEXT_X + 0.02))
                icon_y = text_y + (text_height - icon_height) // 2
                
                screen.blit(icon_img, (icon_x, icon_y))
                screen.blit(score_text, (icon_x + 40, text_y))
        else:
            no_quiz = FONT.render("No quizzes completed yet", True, (150, 150, 150))
            screen.blit(no_quiz, (int(SCREEN_WIDTH * (TEXT_X + 0.02)), int(SCREEN_HEIGHT * (QUIZ_START_Y + 0.04))))
        
        # Unlock Status with IMAGE ICONS
        UNLOCK_START_Y = 0.50
        
        unlock_label = FONT.render("Level Access:", True, (100, 0, 100))
        screen.blit(unlock_label, (int(SCREEN_WIDTH * TEXT_X), int(SCREEN_HEIGHT * UNLOCK_START_Y)))
        
        unlock_status = progress_summary.get("unlock_status", {})
        learning_unlocked = unlock_status.get("learning", {})
        quiz_unlocked = unlock_status.get("quiz", {})
        
        y_offset = 0.04
        for level in [1, 2, 3]:
            y_pos = UNLOCK_START_Y + y_offset
            
            # Check unlock status
            level_topics = learning_unlocked.get(level, {})
            any_topic_unlocked = any(level_topics.values()) if level_topics else False
            all_topics_unlocked = all(level_topics.values()) if level_topics else False
            
            # Learning status
            if all_topics_unlocked:
                learn_icon_img = icon_cache["unlock"]
                learn_color = (0, 150, 0)
                learn_status = "All Topics Unlocked"
            elif any_topic_unlocked:
                learn_icon_img = icon_cache["partial"]
                learn_color = (200, 150, 0)
                unlocked_count = sum(1 for unlocked in level_topics.values() if unlocked)
                total_count = len(level_topics)
                learn_status = f"{unlocked_count}/{total_count} Topics Unlocked"
            else:
                learn_icon_img = icon_cache["lock"]
                learn_color = (150, 0, 0)
                learn_status = "Locked"
            
            # Quiz status
            if quiz_unlocked.get(level, False):
                quiz_icon_img = icon_cache["unlock"]
                quiz_color = (0, 150, 0)
                quiz_status = "Unlocked"
            else:
                quiz_icon_img = icon_cache["lock"]
                quiz_color = (150, 0, 0)
                quiz_status = "Locked"
            
            # ✅ Draw learning icon and text (vertically aligned)
            learn_text = FONT.render(f"Learning {level}: {learn_status}", True, learn_color)
            text_y = int(SCREEN_HEIGHT * y_pos)
            text_height = learn_text.get_height()
            icon_height = learn_icon_img.get_height()
            
            learn_x = int(SCREEN_WIDTH * (TEXT_X + 0.02))
            learn_icon_y = text_y + (text_height - icon_height) // 2
            
            screen.blit(learn_icon_img, (learn_x, learn_icon_y))
            screen.blit(learn_text, (learn_x + 35, text_y))
            
            # ✅ Draw quiz icon and text (vertically aligned)
            quiz_text = FONT.render(f"Quiz {level}: {quiz_status}", True, quiz_color)
            quiz_x = int(SCREEN_WIDTH * (TEXT_X + 0.22))
            quiz_icon_y = text_y + (text_height - icon_height) // 2
            
            screen.blit(quiz_icon_img, (quiz_x, quiz_icon_y))
            screen.blit(quiz_text, (quiz_x + 35, text_y))
            
            y_offset += 0.04
        
        # Stats Summary
        STATS_START_Y = 0.80
        
        stats_label = FONT.render("Statistics:", True, (0, 0, 0))
        screen.blit(stats_label, (int(SCREEN_WIDTH * TEXT_X), int(SCREEN_HEIGHT * STATS_START_Y)))
        
        total_attempts = progress_summary.get("total_attempts", 0)
        total_rewards = progress_summary.get("total_rewards", 0)
        
        attempts_text = FONT.render(f"Quiz Attempts: {total_attempts}", True, (80, 80, 80))
        rewards_text = FONT.render(f"Rewards Unlocked: {total_rewards} / {len(AVAILABLE_REWARDS)}", True, (200, 100, 0))
        
        screen.blit(attempts_text, (int(SCREEN_WIDTH * (TEXT_X + 0.02)), int(SCREEN_HEIGHT * (STATS_START_Y + 0.04))))
        screen.blit(rewards_text, (int(SCREEN_WIDTH * (TEXT_X + 0.02)), int(SCREEN_HEIGHT * (STATS_START_Y + 0.07))))

    def draw():
        nonlocal reward_rects, max_scroll
        screen.fill((230, 255, 230))
        
        # Profile Settings Title
        PROFILE_TITLE_X_RATIO = 0.01
        PROFILE_TITLE_Y_RATIO = 0.02

        title = TITLE_FONT.render("Profile Settings", True, (0, 0, 0))
        TITLE_X = int(SCREEN_WIDTH * PROFILE_TITLE_X_RATIO)
        TITLE_Y = int(SCREEN_HEIGHT * PROFILE_TITLE_Y_RATIO)
        screen.blit(title, (TITLE_X, TITLE_Y))

        # Avatar Selection
        AVATAR_START_X_RATIO = 0.03
        AVATAR_START_Y_RATIO = 0.15
        AVATAR_SIZE_RATIO    = 0.05
        AVATAR_GAP_RATIO     = 0.01

        avatar_size = int(SCREEN_WIDTH * AVATAR_SIZE_RATIO)
        x = int(SCREEN_WIDTH * AVATAR_START_X_RATIO)
        y = int(SCREEN_HEIGHT * AVATAR_START_Y_RATIO)

        for a in AVAILABLE_AVATARS:
            thumb = pygame.transform.smoothscale(avatar_images[a], (avatar_size, avatar_size))
            r = thumb.get_rect(topleft=(x, y))
            screen.blit(thumb, r)

            pygame.draw.rect(
                screen,
                (255, 102, 0) if a == working["avatar"] else (0, 0, 0),
                r, 4, border_radius=10
            )

            avatar_images[a + "_rect"] = r
            x += int(SCREEN_WIDTH * (AVATAR_SIZE_RATIO + AVATAR_GAP_RATIO))

        # Name field
        label_surface = FONT.render("Name:", True, (0, 0, 0))
        label_rect = label_surface.get_rect()
        label_rect.centery = name_rect.centery
        label_rect.right = name_rect.x - int(SCREEN_WIDTH * 0.01)
        screen.blit(label_surface, label_rect)

        pygame.draw.rect(screen, (255, 255, 255), name_rect)
        pygame.draw.rect(screen, (0, 0, 0), name_rect, 2)

        name_surf = FONT.render(working["name"], True, (0, 0, 0))
        name_box = name_surf.get_rect(center=name_rect.center)
        screen.blit(name_surf, name_box)

        if editing and active_input == "name" and cursor_visible:
            pygame.draw.line(screen, (0, 0, 0), (name_box.right + 6, name_rect.y + 8), (name_box.right + 6, name_rect.bottom - 8), 2)

        # Age field
        label_surface = FONT.render("Age:", True, (0, 0, 0))
        label_rect = label_surface.get_rect()
        label_rect.centery = age_rect.centery
        label_rect.right = age_rect.x - int(SCREEN_WIDTH * 0.01)
        screen.blit(label_surface, label_rect)

        pygame.draw.rect(screen, (255, 255, 255), age_rect)
        pygame.draw.rect(screen, (0, 0, 0), age_rect, 2)

        age_surf = FONT.render(working["age"], True, (0, 0, 0))
        age_box = age_surf.get_rect(center=age_rect.center)
        screen.blit(age_surf, age_box)

        if editing and active_input == "age" and cursor_visible:
            pygame.draw.line(screen, (0, 0, 0), (age_box.right + 6, age_rect.y + 8), (age_box.right + 6, age_rect.bottom - 8), 2)

        # ✅ ADD PROGRESS SECTION HERE (before achievements)
        draw_progress_section()

        # Achievements section
        ACH_TITLE_X_RATIO = 0.01
        ACH_TITLE_Y_RATIO = 0.30

        reward_title = TITLE_FONT.render("Achievements", True, (0, 0, 0))
        title_x = int(SCREEN_WIDTH * ACH_TITLE_X_RATIO)
        title_y = int(SCREEN_HEIGHT * ACH_TITLE_Y_RATIO)
        screen.blit(reward_title, (title_x, title_y))

        # Rewards Scroll Section
        view_width  = int(SCREEN_WIDTH * 0.37)
        view_height = int(SCREEN_HEIGHT * 0.38)
        reward_surface = pygame.Surface((view_width, view_height))
        reward_surface.fill((235, 255, 235))

        cols = 7
        card_width = int(SCREEN_WIDTH * 0.05)
        card_height = int(SCREEN_HEIGHT * 0.18)
        margin_x = 10
        margin_y = 20
        reward_rects = {}

        total_rows = (len(reward_cards) + cols - 1) // cols
        max_scroll = max(0, total_rows * (card_height + margin_y) - view_height + 40)

        y_offset = -scroll_offset
        start_x = 0.0

        for i, (r, card_img) in enumerate(reward_cards):
            row, col = divmod(i, cols)
            x = start_x + col * (card_width + margin_x)
            y = row * (card_height + margin_y) + y_offset

            if y + card_height < 0 or y > view_height:
                continue

            img = pygame.transform.smoothscale(card_img, (card_width, card_height))
            if r not in working.get("rewards", []):
                arr = pygame.surfarray.array3d(img)
                avg = arr.mean(axis=2, keepdims=True)
                arr[:] = avg
                img = pygame.surfarray.make_surface(arr)
                img.set_alpha(100)
            else:
                abs_x = x + int(SCREEN_WIDTH * 0.01)
                abs_y = y + int(SCREEN_HEIGHT * 0.35)
                reward_rects[r] = pygame.Rect(abs_x, abs_y, card_width, card_height)

            reward_surface.blit(img, (x, y))

        screen.blit(reward_surface, (int(SCREEN_WIDTH * 0.01), int(SCREEN_HEIGHT * 0.35)))

        # Progress Bar
        PROG_X_RATIO = 0.01
        PROG_Y_RATIO = 0.73
        PROG_W_RATIO = 0.37
        PROG_H_RATIO = 0.035

        unlocked = len(working.get("rewards", []))
        total = len(AVAILABLE_REWARDS)
        progress_ratio = unlocked / total if total > 0 else 0

        bar_x = int(SCREEN_WIDTH * PROG_X_RATIO)
        bar_y = int(SCREEN_HEIGHT * PROG_Y_RATIO)
        bar_w = int(SCREEN_WIDTH * PROG_W_RATIO)
        bar_h = int(SCREEN_HEIGHT * PROG_H_RATIO)

        pygame.draw.rect(screen, (220, 220, 220), (bar_x, bar_y, bar_w, bar_h), border_radius=15)
        pygame.draw.rect(screen, (255, 102, 0), (bar_x, bar_y, int(bar_w * progress_ratio), bar_h), border_radius=15)

        info_text = FONT.render(f"{unlocked} / {total} unlocked", True, (0, 0, 0))
        info_rect = info_text.get_rect(midleft=(bar_x, bar_y + bar_h + int(SCREEN_HEIGHT * 0.03)))
        screen.blit(info_text, info_rect)

        # Buttons
        for rect, color, label in [
            (back_btn, (150, 0, 0), "Back"),
            (edit_btn, (255, 102, 0), "Edit"),
            (save_btn, (0, 170, 0), "Save"),
            (del_btn, (120, 120, 120), "Delete"),
        ]:
            pygame.draw.rect(screen, color, rect, border_radius=14)
            lab_surf = BUTTON_FONT.render(label, True, (255, 255, 255))
            screen.blit(lab_surf, lab_surf.get_rect(center=rect.center))

    # --- Main Loop ---
    reward_rects = {}
    while True:
        mouse = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(mouse): return working
                elif edit_btn.collidepoint(mouse): editing, active_input = True, "name"
                elif save_btn.collidepoint(mouse) and editing:
                    profiles = load_profiles() or []
                    for p in profiles:
                        if p.get("name") == profile.get("name"):
                            p.update(working)
                            break
                    save_profiles(profiles)
                    return working
                elif del_btn.collidepoint(mouse):
                    if confirm_popup(screen, "Delete this profile?", lambda size, bold=False: load_font(config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, size, bold)):
                        delete_profile(profile.get("name", ""))
                        return {"_deleted": True}

                # Avatar selection
                for a in AVAILABLE_AVATARS:
                    r = avatar_images.get(a + "_rect")
                    if r and r.collidepoint(mouse):
                        working["avatar"] = a

                # Reward zoom
                if e.button == 1:
                    if zoomed_reward:
                        zoomed_reward = None
                    else:
                        for r, rect in reward_rects.items():
                            if rect.collidepoint(mouse):
                                zoomed_reward = r
                                break

                # Input focus
                if editing:
                    if name_rect.collidepoint(mouse): active_input = "name"
                    elif age_rect.collidepoint(mouse): active_input = "age"

            elif e.type == pygame.KEYDOWN and editing and active_input:
                if e.key == pygame.K_BACKSPACE:
                    working[active_input] = working[active_input][:-1]
                else:
                    ch = e.unicode
                    if active_input == "name" and ch.isalpha() and len(working["name"]) < 8:
                        working["name"] += ch
                    elif active_input == "age" and ch.isdigit() and len(working["age"]) < 2:
                        working["age"] += ch

            elif e.type == pygame.MOUSEWHEEL:
                scroll_offset -= e.y * scroll_speed
                scroll_offset = max(0, min(scroll_offset, max_scroll))

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    scroll_offset = min(scroll_offset + scroll_speed, max_scroll)
                elif e.key == pygame.K_UP:
                    scroll_offset = max(scroll_offset - scroll_speed, 0)

        # --- Draw Everything ---
        draw()

        # Zoom overlay
        if zoomed_reward:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            for r, img in reward_cards:
                if r == zoomed_reward:
                    large_w = int(SCREEN_WIDTH * 0.20)
                    large_h = int(SCREEN_HEIGHT * 0.72)
                    large_img = pygame.transform.smoothscale(img, (large_w, large_h))
                    rect = large_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    screen.blit(large_img, rect)
                    break
            hint = FONT.render("Click anywhere to close", True, (255, 255, 255))
            screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 80))

        # Caret blink
        cursor_timer += clock.get_time()
        if cursor_timer >= 500:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        pygame.display.flip()
        clock.tick(60)


# =============== Quick standalone test ===============
if __name__ == "__main__":
    test_screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Profile Screen Test")
    selected = run_profile_screen(test_screen, 1280, 720)
    print("Selected profile:", selected)
    pygame.quit()
    sys.exit()
