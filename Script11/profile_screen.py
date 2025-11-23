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

    if align == "center":
        rect = rendered.get_rect(center=pos)
    else:
        rect = rendered.get_rect(topleft=pos)

    surface.blit(rendered, rect)
    return rect


# Screen constants will be passed from main.py
def run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
##    font = pygame.font.SysFont("Arial", 48)
##    small_font = pygame.font.SysFont("Arial", 36)
    clock = pygame.time.Clock()

    # Load avatar images
    avatar_folder = os.path.join("../assets", "profiles", "avatars")
    avatar_images = {a: pygame.image.load(os.path.join(avatar_folder, a)).convert_alpha() for a in AVAILABLE_AVATARS}

    profiles = load_profiles()
    current_input = {"name": "", "age": ""}
    selected_avatar = AVAILABLE_AVATARS[0]
    mode = "select"  # "select" or "create"
    selected_profile = None

    # Buttons
    create_button = pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.85, SCREEN_WIDTH * 0.2, 60)

##    def draw_text(text, pos, font, color=(0, 0, 0)):
##        surf = font.render(text, True, color)
##        screen.blit(surf, pos)

    def draw_profiles():
        screen.fill((245, 245, 245))
        draw_arabic_text(screen, "اختر ملفك الشخصي", ARABIC_BOLD_FONT_PATH, 48, (0,0,0), (SCREEN_WIDTH//2 - 200, 60))
        x = 200
        y = 200
        for name, profile in profiles.items():
            avatar = avatar_images.get(profile["avatar"])
            if avatar:
                avatar = pygame.transform.smoothscale(avatar, (150, 150))
                rect = avatar.get_rect(center=(x, y))
                screen.blit(avatar, rect)
                draw_arabic_text(screen, name, ARABIC_FONT_PATH, 36, (0, 0, 0), (x, y + 100))
                pygame.draw.rect(screen, (0, 0, 0), rect, 3)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, (255, 102, 0), rect, 5)
                # store clickable area
                profile["rect"] = rect
            x += 250
            if x > SCREEN_WIDTH - 200:
                x = 200
                y += 250

        # Create new profile button
        pygame.draw.rect(screen, (255, 102, 0), create_button, border_radius=15)
        draw_arabic_text(screen, "ملف جديد", ARABIC_BOLD_FONT_PATH, 36, (255, 255, 255), create_button.center, bold=True)

    def draw_create_form():
        screen.fill((245, 245, 245))
        draw_arabic_text(screen, "إنشاء ملف جديد", ARABIC_BOLD_FONT_PATH, 48, (0,0,0), (SCREEN_WIDTH//2, 60), align="center")

        # Name input
        pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH//2 - 150, 200, 300, 60))
        pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH//2 - 150, 200, 300, 60), 2)
        draw_arabic_text(screen, f"الاسم: {current_input['name']}", ARABIC_FONT_PATH, 36, (0,0,0), (SCREEN_WIDTH//2 - 140, 210))

        # Age input
        pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH//2 - 150, 300, 300, 60))
        pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH//2 - 150, 300, 300, 60), 2)
        draw_arabic_text(screen, f"العمر: {current_input['age']}", ARABIC_FONT_PATH, 36, (0,0,0), (SCREEN_WIDTH//2 - 140, 310))

        # Avatar selection
        draw_arabic_text(screen, "اختر الصورة الرمزية:", ARABIC_BOLD_FONT_PATH, 48, (0,0,0), (SCREEN_WIDTH//2 - 150, 400))
        x = SCREEN_WIDTH//2 - 300
        y = 480
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

        # Create button
        pygame.draw.rect(screen, (255, 102, 0), create_button, border_radius=15)
        draw_arabic_text(screen, "حفظ", ARABIC_BOLD_FONT_PATH, 36, (255, 255, 255), create_button.center, bold=True)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mode == "select":
                    # Existing profiles
                    for name, profile in profiles.items():
                        if "rect" in profile and profile["rect"].collidepoint(mouse_pos):
                            selected_profile = profile
                            return selected_profile
                    # New profile
                    if create_button.collidepoint(mouse_pos):
                        mode = "create"

                elif mode == "create":
                    # Avatar selection
                    for a in AVAILABLE_AVATARS:
                        rect = avatar_images.get(a + "_rect")
                        if rect and rect.collidepoint(mouse_pos):
                            selected_avatar = a
                    # Save button
                    if create_button.collidepoint(mouse_pos):
                        if current_input["name"] and current_input["age"]:
                            try:
                                profile = create_profile(current_input["name"], current_input["age"], selected_avatar)
                                return profile
                            except Exception as e:
                                print("Error creating profile:", e)

            elif event.type == pygame.KEYDOWN and mode == "create":
                if event.key == pygame.K_RETURN:
                    if current_input["name"] and current_input["age"]:
                        try:
                            profile = create_profile(current_input["name"], current_input["age"], selected_avatar)
                            return profile
                        except Exception as e:
                            print("Error creating profile:", e)
                elif event.key == pygame.K_BACKSPACE:
                    if current_input["age"]:
                        current_input["age"] = current_input["age"][:-1]
                    elif current_input["name"]:
                        current_input["name"] = current_input["name"][:-1]
                else:
                    key = event.unicode
                    if key.isdigit() and len(current_input["name"]) > 0:
                        current_input["age"] += key
                    elif key.isalpha():
                        current_input["name"] += key

        if mode == "select":
            draw_profiles()
        else:
            draw_create_form()

        pygame.display.flip()
        clock.tick(60)
    
if __name__ == "__main__":
    # Create a test window
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Profile Screen Test")

    # Run the profile screen
    selected_profile = run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

    print("Selected profile:", selected_profile)

    pygame.quit()
