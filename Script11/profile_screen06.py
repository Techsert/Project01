import os
import pygame
from profile_system import load_profiles, save_profiles, create_profile, delete_profile, AVAILABLE_AVATARS

pygame.init()


def draw_text(surface, text, size, color, pos, bold=False, align="center"):
    """Draw English text using the built-in Arial font."""
    font = pygame.font.SysFont("Arial", size, bold)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=pos) if align == "center" else rendered.get_rect(topleft=pos)
    surface.blit(rendered, rect)
    return rect


def run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    clock = pygame.time.Clock()
    cursor_visible = True
    cursor_timer = 0

    # Load avatar images
    avatar_folder = os.path.join("../assets", "profiles", "avatars")
    avatar_images = {
        a: pygame.image.load(os.path.join(avatar_folder, a)).convert_alpha()
        for a in AVAILABLE_AVATARS
    }

    # Load exit button image
    exit_image_path = os.path.join("../assets", "img", "main", "exit_icon.png")
    exit_image = pygame.image.load(exit_image_path).convert_alpha()
    exit_image = pygame.transform.smoothscale(exit_image, (80, 80))
    exit_rect = exit_image.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))

    profiles = load_profiles() or []
    current_input = {"name": "", "age": ""}
    selected_avatar = AVAILABLE_AVATARS[0]
    mode = "select"  # "select" or "create"
    selected_profile = None
    show_exit_confirm = False  # confirmation state

    # Rectangles
    create_button = pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.85, SCREEN_WIDTH * 0.2, 60)
    name_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 200, 300, 60)
    age_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 60)
    active_input = None  # "name" or "age"

    # ------------------------------------------------------------------
    # Draw Profiles Screen
    # ------------------------------------------------------------------
    def draw_profiles():
        screen.fill((245, 245, 245))
        draw_text(screen, "Select Your Profile", 48, (0, 0, 0), (SCREEN_WIDTH // 2, 60), bold=True)

        x, y = 200, 200
        for profile in profiles:
            name = profile.get("name", "")
            avatar_name = profile.get("avatar", AVAILABLE_AVATARS[0])
            avatar = avatar_images.get(avatar_name)
            if avatar:
                avatar = pygame.transform.smoothscale(avatar, (150, 150))
                rect = avatar.get_rect(center=(x, y))
                screen.blit(avatar, rect)
                draw_text(screen, name, 36, (0, 0, 0), (x, y + 100))
                pygame.draw.rect(screen, (0, 0, 0), rect, 3)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, (255, 102, 0), rect, 5)
                profile["rect"] = rect
            x += 250
            if x > SCREEN_WIDTH - 200:
                x = 200
                y += 250

        # Create new profile button
        pygame.draw.rect(screen, (255, 102, 0), create_button, border_radius=15)
        draw_text(screen, "New Profile", 36, (255, 255, 255), create_button.center, bold=True)

        # Draw Exit button (bottom right)
        screen.blit(exit_image, exit_rect)

    # ------------------------------------------------------------------
    # Draw Create Profile Screen
    # ------------------------------------------------------------------
    def draw_create_form():
        screen.fill((245, 245, 245))
        draw_text(screen, "Create New Profile", 48, (0, 0, 0), (SCREEN_WIDTH // 2, 60), bold=True)

        font = pygame.font.SysFont("Arial", 36)

        # ===================== Name Field =====================
        draw_text(screen, "Name:", 36, (0, 0, 0), (name_rect.centerx - 200, name_rect.centery), bold=True)
        pygame.draw.rect(screen, (255, 255, 255), name_rect)
        pygame.draw.rect(screen, (0, 0, 0), name_rect, 2)

        # Text clipping
        name_text = current_input["name"]
        while font.size(name_text)[0] > name_rect.width - 20:
            name_text = name_text[1:]
        rendered_name = font.render(name_text, True, (0, 0, 0))
        text_rect = rendered_name.get_rect(center=name_rect.center)
        screen.blit(rendered_name, text_rect)

        # Cursor
        if active_input == "name" and cursor_visible:
            cursor_x = text_rect.right + 5
            cursor_y_top = name_rect.centery - font.get_height() // 2
            cursor_y_bottom = name_rect.centery + font.get_height() // 2
            pygame.draw.line(screen, (0, 0, 0), (cursor_x, cursor_y_top), (cursor_x, cursor_y_bottom), 2)

        # ===================== Age Field =====================
        draw_text(screen, "Age:", 36, (0, 0, 0), (age_rect.centerx - 200, age_rect.centery), bold=True)
        pygame.draw.rect(screen, (255, 255, 255), age_rect)
        pygame.draw.rect(screen, (0, 0, 0), age_rect, 2)

        age_text = current_input["age"]
        while font.size(age_text)[0] > age_rect.width - 20:
            age_text = age_text[1:]
        rendered_age = font.render(age_text, True, (0, 0, 0))
        text_rect = rendered_age.get_rect(center=age_rect.center)
        screen.blit(rendered_age, text_rect)

        if active_input == "age" and cursor_visible:
            cursor_x = text_rect.right + 5
            cursor_y_top = age_rect.centery - font.get_height() // 2
            cursor_y_bottom = age_rect.centery + font.get_height() // 2
            pygame.draw.line(screen, (0, 0, 0), (cursor_x, cursor_y_top), (cursor_x, cursor_y_bottom), 2)

        # ===================== Avatar Selection =====================
        draw_text(screen, "Choose Your Avatar", 48, (0, 0, 0), (SCREEN_WIDTH // 2, 400), bold=True)

        x, y = SCREEN_WIDTH // 2 - 300, 480
        for a in AVAILABLE_AVATARS:
            avatar = avatar_images[a]
            avatar = pygame.transform.smoothscale(avatar, (120, 120))
            rect = avatar.get_rect(center=(x, y))
            screen.blit(avatar, rect)
            if a == selected_avatar:
                pygame.draw.rect(screen, (255, 102, 0), rect, 5)
            else:
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            avatar_images[a + "_rect"] = rect
            x += 150

        # ===================== Save Button =====================
        pygame.draw.rect(screen, (255, 102, 0), create_button, border_radius=15)
        draw_text(screen, "Save", 36, (255, 255, 255), create_button.center, bold=True)

        # Draw Exit button (bottom right)
        screen.blit(exit_image, exit_rect)

    # ------------------------------------------------------------------
    # Draw Exit Confirmation Popup
    # ------------------------------------------------------------------
    def draw_exit_confirmation():
        popup_width, popup_height = 400, 200
        popup_rect = pygame.Rect(
            (SCREEN_WIDTH - popup_width) // 2,
            (SCREEN_HEIGHT - popup_height) // 2,
            popup_width,
            popup_height,
        )
        pygame.draw.rect(screen, (240, 240, 240), popup_rect, border_radius=20)
        pygame.draw.rect(screen, (0, 0, 0), popup_rect, 3)

        draw_text(screen, "Are you sure you want to exit?", 28, (0, 0, 0), popup_rect.center, bold=True)

        # Buttons
        yes_rect = pygame.Rect(popup_rect.centerx - 120, popup_rect.bottom - 70, 100, 50)
        no_rect = pygame.Rect(popup_rect.centerx + 20, popup_rect.bottom - 70, 100, 50)

        pygame.draw.rect(screen, (255, 102, 0), yes_rect, border_radius=10)
        pygame.draw.rect(screen, (180, 180, 180), no_rect, border_radius=10)

        draw_text(screen, "Yes", 28, (255, 255, 255), yes_rect.center, bold=True)
        draw_text(screen, "No", 28, (0, 0, 0), no_rect.center, bold=True)

        return yes_rect, no_rect

    # ------------------------------------------------------------------
    # Main Loop
    # ------------------------------------------------------------------
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_exit_confirm:
                    yes_rect, no_rect = draw_exit_confirmation()
                    if yes_rect.collidepoint(mouse_pos):
                        pygame.display.quit()
                        pygame.quit()
                        raise SystemExit
                    elif no_rect.collidepoint(mouse_pos):
                        show_exit_confirm = False
                    continue

                # Exit button clicked
                if exit_rect.collidepoint(mouse_pos):
                    show_exit_confirm = True
                    continue

                # ================= CREATE MODE =================
                if mode == "create":
                    if name_rect.collidepoint(mouse_pos):
                        active_input = "name"
                    elif age_rect.collidepoint(mouse_pos):
                        active_input = "age"
                    else:
                        active_input = None

                # ================= SELECT MODE =================
                if mode == "select":
                    for profile in profiles:
                        if "rect" in profile and profile["rect"].collidepoint(mouse_pos):
                            selected_profile = profile
                            return selected_profile
                    if create_button.collidepoint(mouse_pos):
                        mode = "create"

                # ================= CREATE MODE (SAVE/AVATAR) =================
                elif mode == "create":
                    for a in AVAILABLE_AVATARS:
                        rect = avatar_images.get(a + "_rect")
                        if rect and rect.collidepoint(mouse_pos):
                            selected_avatar = a
                    if create_button.collidepoint(mouse_pos):
                        if current_input["name"] and current_input["age"]:
                            try:
                                profile = create_profile(
                                    current_input["name"],
                                    current_input["age"],
                                    selected_avatar
                                )
                                return profile
                            except Exception as e:
                                print("Error creating profile:", e)

            elif event.type == pygame.KEYDOWN and mode == "create" and active_input:
                if event.key == pygame.K_BACKSPACE:
                    current_input[active_input] = current_input[active_input][:-1]
                elif event.key == pygame.K_RETURN:
                    if current_input["name"] and current_input["age"]:
                        try:
                            profile = create_profile(
                                current_input["name"],
                                current_input["age"],
                                selected_avatar
                            )
                            return profile
                        except Exception as e:
                            print("Error creating profile:", e)
                else:
                    char = event.unicode
                    # === Name Input: letters only, max 8 ===
                    if active_input == "name":
                        if char.isalpha() and len(current_input["name"]) < 8:
                            current_input["name"] += char
                    # === Age Input: digits only, max 2 ===
                    elif active_input == "age":
                        if char.isdigit() and len(current_input["age"]) < 2:
                            current_input["age"] += char

        # Draw UI
        if show_exit_confirm:
            draw_profiles() if mode == "select" else draw_create_form()
            draw_exit_confirmation()
        else:
            if mode == "select":
                draw_profiles()
            else:
                draw_create_form()

        # Cursor blink
        cursor_timer += clock.get_time()
        if cursor_timer >= 500:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Profile Screen Test")

    selected_profile = run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    print("Selected profile:", selected_profile)

    pygame.quit()
