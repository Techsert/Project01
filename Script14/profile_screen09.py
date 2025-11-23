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

        x, y = 200, 200
        if not profiles:
            info = FONT.render("No profiles found. Click 'New Profile' to create one.", True, (100,100,100))
            screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, SCREEN_HEIGHT//2))
        else:
            for profile in profiles:
                name = profile.get("name", "")
                avatar_name = profile.get("avatar", AVAILABLE_AVATARS[0])
                avatar = avatar_images.get(avatar_name)
                if avatar:
                    avatar_thumb = pygame.transform.smoothscale(avatar, (150, 150))
                    rect = avatar_thumb.get_rect(center=(x, y))
                    screen.blit(avatar_thumb, rect)

                    text = FONT.render(name, True, (0, 0, 0))
                    screen.blit(text, (x - text.get_width() // 2, y + 100))

                    pygame.draw.rect(screen, (0, 0, 0), rect, 3)
                    profile["rect"] = rect

                    # simple delete box (top-right of avatar)
                    del_rect = pygame.Rect(rect.right - 25, rect.top - 10, 25, 25)
                    pygame.draw.rect(screen, (255, 0, 0), del_rect)
                    pygame.draw.line(screen, (255, 255, 255), del_rect.topleft, del_rect.bottomright, 2)
                    pygame.draw.line(screen, (255, 255, 255), (del_rect.left, del_rect.bottom), (del_rect.right, del_rect.top), 2)
                    profile["delete_rect"] = del_rect

                x += 250
                if x > SCREEN_WIDTH - 200:
                    x = 200
                    y += 250

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
        avatars_title = TITLE_FONT.render("Choose your avatar", True, (0, 0, 0))
        screen.blit(avatars_title, (SCREEN_WIDTH//2 - avatars_title.get_width()//2, 400))
        x, y = SCREEN_WIDTH//2 - 300, 480
        for a in AVAILABLE_AVATARS:
            thumb = pygame.transform.smoothscale(avatar_images[a], (120, 120))
            r = thumb.get_rect(center=(x, y))
            screen.blit(thumb, r)
            pygame.draw.rect(screen, (255,102,0) if a == selected_avatar else (0,0,0), r, 4, border_radius=10)
            avatar_images[a + "_rect"] = r
            x += 150

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
      - Click thumbs to change avatar
      - Edit name/age (Edit -> Save)
      - Delete
      - Back returns updated profile (or {'_deleted': True} if deleted)
    """
    clock = pygame.time.Clock()
    avatar_images = _load_avatar_images()

    working = dict(profile)  # local copy
    editing = False
    active_input = None
    cursor_visible, cursor_timer = True, 0

    # UI rects
    back_btn = pygame.Rect(80, SCREEN_HEIGHT - 100, 180, 60)
    edit_btn = pygame.Rect(SCREEN_WIDTH//2 - 200, int(SCREEN_HEIGHT*0.80), 160, 60)
    save_btn = pygame.Rect(SCREEN_WIDTH//2 +  40, int(SCREEN_HEIGHT*0.80), 160, 60)
    del_btn  = pygame.Rect(SCREEN_WIDTH - 260, SCREEN_HEIGHT - 100, 180, 60)
    name_rect = pygame.Rect(SCREEN_WIDTH//2 - 180, 480, 360, 50)
    age_rect  = pygame.Rect(SCREEN_WIDTH//2 - 180, 550, 360, 50)

    def draw():
        screen.fill((245,245,245))
        title = TITLE_FONT.render("Profile Settings", True, (0,0,0))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 60))

        # big avatar
        big = pygame.transform.smoothscale(avatar_images[working["avatar"]], (200,200))
        screen.blit(big, big.get_rect(center=(SCREEN_WIDTH//2, 220)))

        # avatar thumbs row
        x = SCREEN_WIDTH//2 - 300
        for a in AVAILABLE_AVATARS:
            thumb = pygame.transform.smoothscale(avatar_images[a], (100,100))
            r = thumb.get_rect(center=(x,380))
            screen.blit(thumb, r)
            pygame.draw.rect(screen, (255,102,0) if a==working["avatar"] else (0,0,0), r, 4, border_radius=10)
            avatar_images[a+"_rect"] = r
            x += 130

        # name
        screen.blit(FONT.render("Name:", True, (0,0,0)), (name_rect.x - 110, name_rect.y + 8))
        pygame.draw.rect(screen, (255,255,255), name_rect); pygame.draw.rect(screen, (0,0,0), name_rect, 2)
        name_surf = FONT.render(working["name"], True, (0,0,0))
        name_box = name_surf.get_rect(center=name_rect.center)
        screen.blit(name_surf, name_box)
        if editing and active_input == "name" and cursor_visible:
            pygame.draw.line(screen, (0,0,0), (name_box.right + 6, name_rect.y + 8), (name_box.right + 6, name_rect.bottom - 8), 2)

        # age
        screen.blit(FONT.render("Age:", True, (0,0,0)), (age_rect.x - 80, age_rect.y + 8))
        pygame.draw.rect(screen, (255,255,255), age_rect); pygame.draw.rect(screen, (0,0,0), age_rect, 2)
        age_surf = FONT.render(working["age"], True, (0,0,0))
        age_box = age_surf.get_rect(center=age_rect.center)
        screen.blit(age_surf, age_box)
        if editing and active_input == "age" and cursor_visible:
            pygame.draw.line(screen, (0,0,0), (age_box.right + 6, age_rect.y + 8), (age_box.right + 6, age_rect.bottom - 8), 2)
        # ============ Rewards Section =================
        # --- Rewards Display ---
        reward_title = TITLE_FONT.render("Achievements", True, (0, 0, 0))
        screen.blit(reward_title, (SCREEN_WIDTH//2 - reward_title.get_width()//2, 620))

        reward_x = SCREEN_WIDTH//2 - 350
        reward_y = 700
        for r, card_img in reward_cards:
            img = pygame.transform.smoothscale(card_img, (120, 120))
            if r not in working.get("rewards", []):
                # Convert to grayscale (locked)
                arr = pygame.surfarray.array3d(img)
                avg = arr.mean(axis=2, keepdims=True)
                arr[:] = avg
                img = pygame.surfarray.make_surface(arr)
            screen.blit(img, (reward_x, reward_y))
            reward_x += 140

        # ==============Rewards section End ============

        # buttons
        for rect, color, label in [
            (back_btn, (150, 0, 0), "Back"),
            (edit_btn, (255, 102, 0), "Edit"),
            (save_btn, (0, 170, 0), "Save"),
            (del_btn,  (120,120,120), "Delete"),
        ]:
            pygame.draw.rect(screen, color, rect, border_radius=14)
            lab_surf = FONT.render(label, True, (255,255,255))
            screen.blit(lab_surf, (rect.centerx - lab_surf.get_width()//2, rect.centery - 18))







    # -------- main loop --------
    while True:
        mouse = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            elif e.type == pygame.MOUSEBUTTONDOWN:
                # back
                if back_btn.collidepoint(mouse):
                    return working  # return current (even if not edited)

                # edit
                if edit_btn.collidepoint(mouse):
                    editing = True
                    active_input = "name"

                # save
                if save_btn.collidepoint(mouse) and editing:
                    # persist updates into JSON (by name match; adjust if you use IDs)
                    profiles = load_profiles() or []
                    for p in profiles:
                        if p.get("name") == profile.get("name") and p.get("avatar") == profile.get("avatar"):
                            p["name"] = working["name"]
                            p["age"] = working["age"]
                            p["avatar"] = working["avatar"]
                            break
                    save_profiles(profiles)
                    return working

                # delete
                if del_btn.collidepoint(mouse):
                    if confirm_popup(screen, "Delete this profile?"):
                        delete_profile(profile.get("name", ""))
                        return {"_deleted": True}

                # focus inputs while editing
                if editing:
                    if name_rect.collidepoint(mouse): active_input = "name"
                    elif age_rect.collidepoint(mouse): active_input = "age"

                # change avatar by clicking thumbs
                for a in AVAILABLE_AVATARS:
                    r = avatar_images.get(a + "_rect")
                    if r and r.collidepoint(mouse):
                        working["avatar"] = a

            elif e.type == pygame.KEYDOWN and editing and active_input:
                if e.key == pygame.K_BACKSPACE:
                    working[active_input] = working[active_input][:-1]
                else:
                    ch = e.unicode
                    if active_input == "name" and ch.isalpha() and len(working["name"]) < 8:
                        working["name"] += ch
                    elif active_input == "age" and ch.isdigit() and len(working["age"]) < 2:
                        working["age"] += ch

        draw()

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
