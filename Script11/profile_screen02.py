import os
import pygame
import arabic_reshaper
from bidi.algorithm import get_display
from profile_system import load_profiles, save_profiles, create_profile, delete_profile, AVAILABLE_AVATARS

pygame.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARABIC_FONT_PATH = os.path.join(BASE_DIR, "../assets/fonts/NotoNaskhArabic-Regular.ttf")
ARABIC_BOLD_FONT_PATH = os.path.join(BASE_DIR, "../assets/fonts/NotoNaskhArabic-Bold.ttf")


def draw_arabic_text(surface, text, font_path, size, color, pos, bold=False, align="center"):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    font = pygame.font.Font(font_path, size)
    rendered = font.render(bidi_text, True, color)
    rect = rendered.get_rect(center=pos) if align == "center" else rendered.get_rect(topleft=pos)
    surface.blit(rendered, rect)
    return rect


def run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    clock = pygame.time.Clock()

    # Load avatar images
    avatar_folder = os.path.join("../assets", "profiles", "avatars")
    avatar_images = {
        a: pygame.image.load(os.path.join(avatar_folder, a)).convert_alpha()
        for a in AVAILABLE_AVATARS
    }

    profiles = load_profiles() or []
    current_input = {"name": "", "age": ""}
    selected_avatar = AVAILABLE_AVATARS[0]
    mode = "select"  # "select" or "create"
    selected_profile = None

    # Rects
    create_button = pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.85, SCREEN_WIDTH * 0.2, 60)
    name_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 200, 300, 60)
    age_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 60)

    # Track which input box is active
    active_input = None  # "name" or "age"

    def draw_profiles():
        screen.fill((245, 245, 245))
        draw_arabic_text(screen, "اختر ملفك الشخصي", ARABIC_BOLD_FONT_PATH, 48, (0, 0, 0),
                         (SCREEN_WIDTH // 2, 60), align="center")

        x, y = 200, 200
        for profile in profiles:  # ✅ LIST iteration
            name = profile.get("name", "")
            avatar_name = profile.get("avatar", AVAILABLE_AVATARS[0])
            avatar = avatar_images.get(avatar_name)
            if avatar:
                avatar = pygame.transform.smoothscale(avatar, (150, 150))
                rect = avatar.get_rect(center=(x, y))
                screen.blit(avatar, rect)
                draw_arabic_text(screen, name, ARABIC_FONT_PATH, 36, (0, 0, 0), (x, y + 100))
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
        draw_arabic_text(screen, "ملف جديد", ARABIC_BOLD_FONT_PATH, 36, (255, 255, 255),
                         create_button.center, bold=True)

    def draw_create_form():
        screen.fill((245, 245, 245))
        draw_arabic_text(screen, "إنشاء ملف جديد", ARABIC_BOLD_FONT_PATH, 48, (0, 0, 0),
                         (SCREEN_WIDTH // 2, 60), align="center")

        # Name input
        pygame.draw.rect(screen, (255, 255, 255), name_rect)
        pygame.draw.rect(screen, (0, 0, 0), name_rect, 2)
        draw_arabic_text(screen, f"الاسم: {current_input['name']}", ARABIC_FONT_PATH, 36,
                         (0, 0, 0), name_rect.center, align="center")

        # Age input
        pygame.draw.rect(screen, (255, 255, 255), age_rect)
        pygame.draw.rect(screen, (0, 0, 0), age_rect, 2)
        draw_arabic_text(screen, f"العمر: {current_input['age']}", ARABIC_FONT_PATH, 36,
                         (0, 0, 0), age_rect.center, align="center")

        # Avatar selection
        draw_arabic_text(screen, "اختر الصورة الرمزية:", ARABIC_BOLD_FONT_PATH, 48, (0, 0, 0),
                         (SCREEN_WIDTH // 2, 400), align="center")
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

        # Save button
        pygame.draw.rect(screen, (255, 102, 0), create_button, border_radius=15)
        draw_arabic_text(screen, "حفظ", ARABIC_BOLD_FONT_PATH, 36, (255, 255, 255),
                         create_button.center, bold=True)

    # ========================= MAIN LOOP =========================
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mode == "create":
                    if name_rect.collidepoint(mouse_pos):
                        active_input = "name"
                    elif age_rect.collidepoint(mouse_pos):
                        active_input = "age"
                    else:
                        active_input = None

                if mode == "select":
                    # ✅ handle list structure
                    for profile in profiles:
                        if "rect" in profile and profile["rect"].collidepoint(mouse_pos):
                            selected_profile = profile
                            return selected_profile
                    if create_button.collidepoint(mouse_pos):
                        mode = "create"

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
                    current_input[active_input] += event.unicode

        if mode == "select":
            draw_profiles()
        else:
            draw_create_form()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Profile Screen Test")

    selected_profile = run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    print("Selected profile:", selected_profile)

    pygame.quit()
