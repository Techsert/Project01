import os
import sys
import pygame
from profile_system import (
    load_profiles, save_profiles, create_profile, delete_profile,
    AVAILABLE_AVATARS, AVAILABLE_REWARDS, REWARDS_PATH
)

pygame.init()
FONT = pygame.font.SysFont("Arial", 32)
TITLE_FONT = pygame.font.SysFont("Arial", 48, bold=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AVATAR_PATH = os.path.join(BASE_DIR, "../assets/profiles/avatars")
DATA_PATH = os.path.join(BASE_DIR, "../assets/profiles/data")
IMG_PATH = os.path.join(BASE_DIR, "../assets/img/main")
EXIT_IMG = os.path.join(IMG_PATH, "exit_icon.png")

os.makedirs(DATA_PATH, exist_ok=True)


# ====================== Helpers ======================
def confirm_popup(screen, msg):
    """Modal Yes/No confirmation dialog. Returns True/False."""
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    box = pygame.Rect(0, 0, 520, 240)
    box.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.draw.rect(screen, (255, 255, 255), box, border_radius=15)
    pygame.draw.rect(screen, (255, 102, 0), box, 4, border_radius=15)

    title = TITLE_FONT.render(msg, True, (0, 0, 0))
    screen.blit(title, (box.centerx - title.get_width() // 2, box.top + 40))

    yes = pygame.Rect(box.centerx - 140, box.bottom - 80, 120, 50)
    no = pygame.Rect(box.centerx + 20,  box.bottom - 80, 120, 50)
    pygame.draw.rect(screen, (0, 170, 0), yes, border_radius=10)
    pygame.draw.rect(screen, (170, 0, 0), no,  border_radius=10)
    screen.blit(FONT.render("Yes", True, (255,255,255)), (yes.centerx-28, yes.centery-18))
    screen.blit(FONT.render("No",  True, (255,255,255)), (no.centerx-22,  no.centery-18))

    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if yes.collidepoint(e.pos): return True
                if no.collidepoint(e.pos):  return False
        pygame.time.wait(10)


def _load_avatar_images():
    return {
        a: pygame.image.load(os.path.join(AVATAR_PATH, a)).convert_alpha()
        for a in AVAILABLE_AVATARS
    }


# ================== Profile Selection ==================
def run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    """
    Startup selector:
      - Click profile -> returns profile dict
      - 'New Profile' -> create form
      - Delete icon per profile
      - Exit button (bottom-right)
    """
    clock = pygame.time.Clock()
    avatar_images = _load_avatar_images()
    profiles = load_profiles() or []

    # State
    mode = "select"  # "select" or "create"
    current_input = {"name": "", "age": ""}
    active_input = None
    selected_avatar = AVAILABLE_AVATARS[0]
    cursor_visible, cursor_timer = True, 0

    # UI rects
    create_button = pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.85, SCREEN_WIDTH * 0.2, 60)
    name_rect = pygame.Rect(SCREEN_WIDTH // 2 - 180, 220, 360, 60)
    age_rect  = pygame.Rect(SCREEN_WIDTH // 2 - 180, 300, 360, 60)

    # Exit icon
    try:
        exit_icon = pygame.image.load(EXIT_IMG).convert_alpha()
        exit_icon = pygame.transform.smoothscale(exit_icon, (70, 70))
    except:
        exit_icon = pygame.Surface((70,70), pygame.SRCALPHA); exit_icon.fill((200,0,0,200))
    exit_rect = exit_icon.get_rect(bottomright=(SCREEN_WIDTH - 30, SCREEN_HEIGHT - 30))

    # ---------- draw: profiles grid ----------
    def draw_profiles():
        screen.fill((245, 245, 245))
        title = TITLE_FONT.render("Select Your Profile", True, (0, 0, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 60))

        # --- Calculate grid layout dynamically ---
        CARD_W, CARD_H = 150, 150
        MARGIN_X, MARGIN_Y = 80, 100
        cols = 4  # how many avatars per row

        rows = (len(profiles) + cols - 1) // cols
        total_grid_width = cols * CARD_W + (cols - 1) * MARGIN_X
        total_grid_height = rows * (CARD_H + 60) + (rows - 1) * MARGIN_Y  # include text spacing

        # Center starting position
        start_x = (SCREEN_WIDTH - total_grid_width) // 2 + CARD_W // 2
        start_y = (SCREEN_HEIGHT - total_grid_height) // 2 + CARD_H // 2

        x, y = start_x, start_y

        if not profiles:
            info = FONT.render("No profiles found. Click 'New Profile' to create one.", True, (100,100,100))
            screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, SCREEN_HEIGHT//2))
        else:
            # === Dynamic Centered Rows ===
            CARD_W, CARD_H = 150, 150
            MARGIN_X, MARGIN_Y = 80, 100
            cols = 4  # max avatars per row

            rows = (len(profiles) + cols - 1) // cols
            start_y = (SCREEN_HEIGHT - (rows * (CARD_H + MARGIN_Y))) // 2 + 150  # vertical center offset

            for row in range(rows):
                start_idx = row * cols
                end_idx = min(start_idx + cols, len(profiles))
                row_profiles = profiles[start_idx:end_idx]
                row_count = len(row_profiles)

                # 🔹 Center this specific row horizontally
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

        # Avatar selection (thumbnails)
        # === Avatar selection (centered row) ===
##        avatars_title = TITLE_FONT.render("Choose your avatar", True, (0, 0, 0))
##        screen.blit(avatars_title, (SCREEN_WIDTH // 2 - avatars_title.get_width() // 2, 400))

        # layout constants
        AVATAR_SIZE = 120
        SPACING_X = 50
        y = 500  # vertical position of the row

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
        screen.blit(FONT.render("Save", True, (255,255,255)), (create_button.centerx - 35, create_button.centery - 18))

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
                    if confirm_popup(screen, "Exit the game?"):
                        pygame.quit(); sys.exit()

                if mode == "select":
                    # delete or select
                    for profile in profiles[:]:
                        if "delete_rect" in profile and profile["delete_rect"].collidepoint(mouse):
                            if confirm_popup(screen, f"Delete '{profile['name']}'?"):
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
def run_profile_manage_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, profile):
    """
    Manage current profile from main menu:
      - View avatar, name, age
      - Edit name/age (Edit -> Save)
      - Change avatar
      - View achievements (scrollable grid)
      - View progress (bottom section)
      - Delete profile
    """
    clock = pygame.time.Clock()
    avatar_images = _load_avatar_images()

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
            path = os.path.join(REWARDS_PATH, r)
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
    edit_btn = pygame.Rect(SCREEN_WIDTH // 2 - 200, int(SCREEN_HEIGHT * 0.80), 160, 60)
    save_btn = pygame.Rect(SCREEN_WIDTH // 2 + 40, int(SCREEN_HEIGHT * 0.80), 160, 60)
    del_btn  = pygame.Rect(SCREEN_WIDTH - 260, SCREEN_HEIGHT - 100, 180, 60)
    # === Name & Age input fields (resolution-scaled) ===

    # Control ratios — tweak these four values for position and spacing
    NAME_X_RATIO = 0.05    # horizontal position (5% from left)
    NAME_Y_RATIO = 0.07    # vertical position (20% from top)
    AGE_X_RATIO  = 0.05    # horizontal position (same as Name to align)
    AGE_Y_RATIO  = 0.11    # vertical position (28% from top, below Name)

    # Control box sizes (relative to screen)
    BOX_W_RATIO  = 0.05    # width (25% of screen width)
    BOX_H_RATIO  = 0.03    # height (5% of screen height)

    # Create rects
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


    def draw():
        nonlocal reward_rects, max_scroll
        screen.fill((230, 255, 230))
        # === Profile Settings Title (resolution-scaled, adjustable) ===
        PROFILE_TITLE_X_RATIO = 0.01   # 5% from left side
        PROFILE_TITLE_Y_RATIO = 0.02   # 5% from top side

        title = TITLE_FONT.render("Profile Settings", True, (0, 0, 0))
        TITLE_X = int(SCREEN_WIDTH * PROFILE_TITLE_X_RATIO)
        TITLE_Y = int(SCREEN_HEIGHT * PROFILE_TITLE_Y_RATIO)
        screen.blit(title, (TITLE_X, TITLE_Y))


        # --- Profile info section ---
##        big = pygame.transform.smoothscale(avatar_images[working["avatar"]], (200, 200))
##        screen.blit(big, big.get_rect(center=(SCREEN_WIDTH // 2, 180)))

        # Avatars row
        # === Avatar Selection (resolution-scaled, adjustable) ===

        AVATAR_START_X_RATIO = 0.03    # starting position (5% from left)
        AVATAR_START_Y_RATIO = 0.15    # vertical position (38% from top, below Age field)
        AVATAR_SIZE_RATIO    = 0.05    # each avatar size (8% of screen width)
        AVATAR_GAP_RATIO     = 0.01    # gap between avatars (7% of screen width)

        # Calculate positions and sizes
        avatar_size = int(SCREEN_WIDTH * AVATAR_SIZE_RATIO)
        x = int(SCREEN_WIDTH * AVATAR_START_X_RATIO)
        y = int(SCREEN_HEIGHT * AVATAR_START_Y_RATIO)

        for a in AVAILABLE_AVATARS:
            thumb = pygame.transform.smoothscale(avatar_images[a], (avatar_size, avatar_size))
            r = thumb.get_rect(topleft=(x, y))
            screen.blit(thumb, r)

            # highlight border
            pygame.draw.rect(
                screen,
                (255, 102, 0) if a == working["avatar"] else (0, 0, 0),
                r, 4, border_radius=10
            )

            avatar_images[a + "_rect"] = r
            x += int(SCREEN_WIDTH * (AVATAR_SIZE_RATIO + AVATAR_GAP_RATIO))  # move to next slot


        # === Name / Age fields (resolution-scaled, full control) ===
        LABEL_Y_OFFSET_RATIO = -0.03  # move label up (3% of screen height)

        # --- Name field ---
        # --- Name label beside box ---
        label_surface = FONT.render("Name:", True, (0, 0, 0))
        label_rect = label_surface.get_rect()
        label_rect.centery = name_rect.centery                      # keep vertically aligned
        label_rect.right = name_rect.x - int(SCREEN_WIDTH * 0.01)   # 1% gap between label and box
        screen.blit(label_surface, label_rect)


        pygame.draw.rect(screen, (255, 255, 255), name_rect)
        pygame.draw.rect(screen, (0, 0, 0), name_rect, 2)

        name_surf = FONT.render(working["name"], True, (0, 0, 0))
        name_box = name_surf.get_rect(center=name_rect.center)
        screen.blit(name_surf, name_box)

        # Caret (typing cursor)
        if editing and active_input == "name" and cursor_visible:
            pygame.draw.line(
                screen, (0, 0, 0),
                (name_box.right + 6, name_rect.y + 8),
                (name_box.right + 6, name_rect.bottom - 8), 2
            )


        # --- Age field ---
        # --- Age label beside box ---
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

        # Caret (typing cursor)
        if editing and active_input == "age" and cursor_visible:
            pygame.draw.line(
                screen, (0, 0, 0),
                (age_box.right + 6, age_rect.y + 8),
                (age_box.right + 6, age_rect.bottom - 8), 2
            )


        # --- Achievements section ---
        # === Achievements Title (resolution-scaled) ===
        ACH_TITLE_X_RATIO = 0.01   # horizontal offset from left edge
        ACH_TITLE_Y_RATIO = 0.30   # vertical offset from top

        reward_title = TITLE_FONT.render("Achievements", True, (0, 0, 0))
        title_x = int(SCREEN_WIDTH * ACH_TITLE_X_RATIO)
        title_y = int(SCREEN_HEIGHT * ACH_TITLE_Y_RATIO)
        screen.blit(reward_title, (title_x, title_y))


        # === Rewards Scroll Section (left-aligned) ===
        # Size
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
        start_x = 0.0  # 🔹 Left-aligned under Achievements title

        for i, (r, card_img) in enumerate(reward_cards):
            row, col = divmod(i, cols)
            x = start_x + col * (card_width + margin_x)
            y = row * (card_height + margin_y) + y_offset

            if y + card_height < 0 or y > view_height:
                continue  # skip off-screen cards

            img = pygame.transform.smoothscale(card_img, (card_width, card_height))
            if r not in working.get("rewards", []):
                arr = pygame.surfarray.array3d(img)
                avg = arr.mean(axis=2, keepdims=True)
                arr[:] = avg
                img = pygame.surfarray.make_surface(arr)
                img.set_alpha(100)
            else:
                # Convert card position from surface-space to screen-space
                abs_x = x + int(SCREEN_WIDTH * 0.01)   # ← matches your screen.blit() X offset
                abs_y = y + int(SCREEN_HEIGHT * 0.35)  # ← matches your screen.blit() Y offset
                reward_rects[r] = pygame.Rect(abs_x, abs_y, card_width, card_height)


            reward_surface.blit(img, (x, y))

        screen.blit(reward_surface, (int(SCREEN_WIDTH * 0.01), int(SCREEN_HEIGHT * 0.35)))


        # --- Progress Section ---
##        progress_y = int(SCREEN_HEIGHT * 0.80)
##        progress_title = TITLE_FONT.render("Progress", True, (0, 0, 0))
##        screen.blit(progress_title, (SCREEN_WIDTH // 2 - progress_title.get_width() // 2, progress_y))

        # === Progress Bar (resolution-scaled & fully controllable) ===

        # Control ratios (you can fine-tune these)
        PROG_X_RATIO = 0.01     # horizontal position (5% from left)
        PROG_Y_RATIO = 0.73     # vertical position (distance from top)
        PROG_W_RATIO = 0.37     # width (40% of screen width)
        PROG_H_RATIO = 0.035    # height (3.5% of screen height)

        unlocked = len(working.get("rewards", []))
        total = len(AVAILABLE_REWARDS)
        progress_ratio = unlocked / total if total > 0 else 0

        # Convert ratios to absolute pixel values
        bar_x = int(SCREEN_WIDTH * PROG_X_RATIO)
        bar_y = int(SCREEN_HEIGHT * PROG_Y_RATIO)
        bar_w = int(SCREEN_WIDTH * PROG_W_RATIO)
        bar_h = int(SCREEN_HEIGHT * PROG_H_RATIO)

        # Draw progress bar background and fill
        pygame.draw.rect(screen, (220, 220, 220), (bar_x, bar_y, bar_w, bar_h), border_radius=15)
        pygame.draw.rect(screen, (255, 102, 0), (bar_x, bar_y, bar_w * progress_ratio, bar_h), border_radius=15)

        # Progress info text (aligned with bar)
        info_text = FONT.render(f"{unlocked} / {total} unlocked", True, (0, 0, 0))
        info_rect = info_text.get_rect(midleft=(bar_x, bar_y + bar_h + int(SCREEN_HEIGHT * 0.01)))
        screen.blit(info_text, info_rect)


        # --- Buttons ---
        for rect, color, label in [
            (back_btn, (150, 0, 0), "Back"),
            (edit_btn, (255, 102, 0), "Edit"),
            (save_btn, (0, 170, 0), "Save"),
            (del_btn, (120, 120, 120), "Delete"),
        ]:
            pygame.draw.rect(screen, color, rect, border_radius=14)
            lab_surf = FONT.render(label, True, (255, 255, 255))
            screen.blit(lab_surf, (rect.centerx - lab_surf.get_width() // 2, rect.centery - 18))

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
                    if confirm_popup(screen, "Delete this profile?"):
                        delete_profile(profile.get("name", ""))
                        return {"_deleted": True}

                # Avatar selection
                for a in AVAILABLE_AVATARS:
                    r = avatar_images.get(a + "_rect")
                    if r and r.collidepoint(mouse):
                        working["avatar"] = a

                # Reward zoom
                # Reward zoom — only trigger on left-click, ignore scroll
                if e.button == 1:  # left mouse button
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
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Profile Screen Test")
    selected = run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    print("Selected profile:", selected)
    pygame.quit()
    sys.exit()
