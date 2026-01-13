import os
import sys
import pygame
from profile_system import load_profiles, save_profiles, create_profile, delete_profile, AVAILABLE_AVATARS

pygame.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../assets/profiles/data")
AVATAR_DIR = os.path.join(BASE_DIR, "../assets/profiles/avatars")
IMG_DIR = os.path.join(BASE_DIR, "../assets/img/main")

os.makedirs(DATA_DIR, exist_ok=True)

FONT = pygame.font.SysFont("Arial", 36)
TITLE_FONT = pygame.font.SysFont("Arial", 48, bold=True)


def run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    clock = pygame.time.Clock()
    cursor_visible = True
    cursor_timer = 0

    # Load images
    avatar_images = {
        a: pygame.image.load(os.path.join(AVATAR_DIR, a)).convert_alpha()
        for a in AVAILABLE_AVATARS
    }
    exit_icon = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(IMG_DIR, "exit_icon.png")).convert_alpha(), (80, 80)
    )
    exit_rect = exit_icon.get_rect(bottomright=(SCREEN_WIDTH - 30, SCREEN_HEIGHT - 30))

    delete_icon = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(IMG_DIR, "delete_icon.png")).convert_alpha(), (40, 40)
    )

    # Load data
    profiles = load_profiles() or []
    current_input = {"name": "", "age": ""}
    selected_avatar = AVAILABLE_AVATARS[0]
    active_input = None
    mode = "select"
    selected_profile = None

    create_button = pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.85, SCREEN_WIDTH * 0.2, 60)
    name_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 200, 300, 60)
    age_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 60)

    # ====== POPUP CONFIRMATION ======
    def confirm_popup(message):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        box_width, box_height = 500, 250
        box_rect = pygame.Rect((SCREEN_WIDTH - box_width)//2, (SCREEN_HEIGHT - box_height)//2, box_width, box_height)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, border_radius=15)
        pygame.draw.rect(screen, (255, 102, 0), box_rect, 4, border_radius=15)

        text = TITLE_FONT.render(message, True, (0, 0, 0))
        screen.blit(text, (box_rect.centerx - text.get_width()//2, box_rect.y + 60))

        yes_rect = pygame.Rect(box_rect.centerx - 120, box_rect.y + 150, 100, 50)
        no_rect = pygame.Rect(box_rect.centerx + 20, box_rect.y + 150, 100, 50)
        pygame.draw.rect(screen, (0, 200, 0), yes_rect, border_radius=10)
        pygame.draw.rect(screen, (200, 0, 0), no_rect, border_radius=10)

        yes_text = FONT.render("Yes", True, (255, 255, 255))
        no_text = FONT.render("No", True, (255, 255, 255))
        screen.blit(yes_text, yes_rect.move((yes_rect.width - yes_text.get_width())//2, 8))
        screen.blit(no_text, no_rect.move((no_rect.width - no_text.get_width())//2, 8))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_rect.collidepoint(event.pos):
                        return True
                    elif no_rect.collidepoint(event.pos):
                        return False
            pygame.time.wait(10)

    # ====== DRAW PROFILES ======
    def draw_profiles():
        screen.fill((245, 245, 245))
        title_surface = TITLE_FONT.render("Select Your Profile", True, (0, 0, 0))
        screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 60))

        x, y = 200, 200
        if not profiles:
            no_text = FONT.render("No profiles found. Click 'New Profile' to create one.", True, (100, 100, 100))
            screen.blit(no_text, (SCREEN_WIDTH // 2 - no_text.get_width() // 2, SCREEN_HEIGHT // 2))
        else:
            for profile in profiles:
                name = profile.get("name", "")
                avatar_name = profile.get("avatar", AVAILABLE_AVATARS[0])
                avatar = avatar_images.get(avatar_name)
                if avatar:
                    avatar = pygame.transform.smoothscale(avatar, (150, 150))
                    rect = avatar.get_rect(center=(x, y))
                    screen.blit(avatar, rect)

                    name_text = FONT.render(name, True, (0, 0, 0))
                    screen.blit(name_text, (x - name_text.get_width() // 2, y + 100))

                    pygame.draw.rect(screen, (0, 0, 0), rect, 3)
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(screen, (255, 102, 0), rect, 5)

                    delete_rect = delete_icon.get_rect(center=(x, y + 170))
                    screen.blit(delete_icon, delete_rect)

                    profile["rect"] = rect
                    profile["delete_rect"] = delete_rect

                x += 250
                if x > SCREEN_WIDTH - 200:
                    x = 200
                    y += 250

        pygame.draw.rect(screen, (255, 102, 0), create_button, border_radius=15)
        label = FONT.render("New Profile", True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=create_button.center))
        screen.blit(exit_icon, exit_rect)

    # ====== DRAW CREATE FORM ======
    def draw_create_form():
        screen.fill((245, 245, 245))
        title_surface = TITLE_FONT.render("Create New Profile", True, (0, 0, 0))
        screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 60))

        font = pygame.font.SysFont("Arial", 36)
        # Name input
        name_label = font.render("Name:", True, (0, 0, 0))
        screen.blit(name_label, (name_rect.x - 140, name_rect.y + 10))
        pygame.draw.rect(screen, (255, 255, 255), name_rect)
        pygame.draw.rect(screen, (0, 0, 0), name_rect, 2)

        name_text = current_input["name"]
        rendered_name = font.render(name_text, True, (0, 0, 0))
        text_rect = rendered_name.get_rect(center=name_rect.center)
        screen.blit(rendered_name, text_rect)
        if active_input == "name" and cursor_visible:
            pygame.draw.line(screen, (0, 0, 0),
                             (text_rect.right + 5, name_rect.y + 10),
                             (text_rect.right + 5, name_rect.y + name_rect.height - 10), 2)

        # Age input
        age_label = font.render("Age:", True, (0, 0, 0))
        screen.blit(age_label, (age_rect.x - 100, age_rect.y + 10))
        pygame.draw.rect(screen, (255, 255, 255), age_rect)
        pygame.draw.rect(screen, (0, 0, 0), age_rect, 2)

        age_text = current_input["age"]
        rendered_age = font.render(age_text, True, (0, 0, 0))
        text_rect = rendered_age.get_rect(center=age_rect.center)
        screen.blit(rendered_age, text_rect)
        if active_input == "age" and cursor_visible:
            pygame.draw.line(screen, (0, 0, 0),
                             (text_rect.right + 5, age_rect.y + 10),
                             (text_rect.right + 5, age_rect.y + age_rect.height - 10), 2)

        # Avatar selection
        avatar_label = TITLE_FONT.render("Choose your avatar", True, (0, 0, 0))
        screen.blit(avatar_label, (SCREEN_WIDTH // 2 - avatar_label.get_width() // 2, 400))
        x, y = SCREEN_WIDTH // 2 - 300, 480
        for a in AVAILABLE_AVATARS:
            avatar = pygame.transform.smoothscale(avatar_images[a], (120, 120))
            rect = avatar.get_rect(center=(x, y))
            screen.blit(avatar, rect)
            if a == selected_avatar:
                pygame.draw.rect(screen, (255, 102, 0), rect, 5)
            else:
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            avatar_images[a + "_rect"] = rect
            x += 150

        pygame.draw.rect(screen, (255, 102, 0), create_button, border_radius=15)
        label = FONT.render("Save", True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=create_button.center))
        screen.blit(exit_icon, exit_rect)

    # ====== MAIN LOOP ======
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_rect.collidepoint(mouse_pos):
                    if confirm_popup("Exit the game?"):
                        pygame.quit()
                        sys.exit()

                if mode == "create":
                    if name_rect.collidepoint(mouse_pos):
                        active_input = "name"
                    elif age_rect.collidepoint(mouse_pos):
                        active_input = "age"
                    else:
                        active_input = None

                if mode == "select":
                    for profile in profiles[:]:
                        if "delete_rect" in profile and profile["delete_rect"].collidepoint(mouse_pos):
                            if confirm_popup(f"Delete '{profile['name']}'?"):
                                delete_profile(profile["name"])
                                profiles.remove(profile)
                                clean_profiles = [
                                    {k: v for k, v in p.items() if k not in ("rect", "delete_rect")}
                                    for p in profiles
                                ]
                                save_profiles(clean_profiles)
                                profiles = load_profiles() or []
                            break
                        elif "rect" in profile and profile["rect"].collidepoint(mouse_pos):
                            return profile
                    if create_button.collidepoint(mouse_pos):
                        mode = "create"

                elif mode == "create":
                    for a in AVAILABLE_AVATARS:
                        rect = avatar_images.get(a + "_rect")
                        if rect and rect.collidepoint(mouse_pos):
                            selected_avatar = a
                    if create_button.collidepoint(mouse_pos):
                        if current_input["name"] and current_input["age"]:
                            profile = create_profile(
                                current_input["name"], current_input["age"], selected_avatar
                            )
                            return profile

            elif event.type == pygame.KEYDOWN and mode == "create" and active_input:
                if event.key == pygame.K_BACKSPACE:
                    current_input[active_input] = current_input[active_input][:-1]
                else:
                    char = event.unicode
                    if active_input == "name" and char.isalpha() and len(current_input["name"]) < 8:
                        current_input["name"] += char
                    elif active_input == "age" and char.isdigit() and len(current_input["age"]) < 2:
                        current_input["age"] += char

        if mode == "select":
            draw_profiles()
        else:
            draw_create_form()

        cursor_timer += clock.get_time()
        if cursor_timer >= 500:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        pygame.display.flip()
        clock.tick(60)


# ====== TEST RUN ======
if __name__ == "__main__":
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Profile Screen Test")
    selected_profile = run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    print("Selected profile:", selected_profile)
    pygame.quit()
    sys.exit()
