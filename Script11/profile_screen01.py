import os
import pygame
import json
import arabic_reshaper
from bidi.algorithm import get_display

# ----------------------------
# Config
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../assets", "profiles", "data")
PROFILE_FILE = os.path.join(DATA_DIR, "profiles.json")
AVATAR_FOLDER = os.path.join(BASE_DIR, "../assets", "profiles", "avatars")
ARABIC_FONT_PATH = os.path.join(BASE_DIR, "../assets/fonts/NotoNaskhArabic-Regular.ttf")
ARABIC_BOLD_FONT_PATH = os.path.join(BASE_DIR, "../assets/fonts/NotoNaskhArabic-Bold.ttf")
AVAILABLE_AVATARS = ["avatar1.png","avatar2.png","avatar3.png","avatar4.png","avatar5.png"]

# ----------------------------
# Helper functions
# ----------------------------
def draw_arabic_text(surface, text, font_path, size, color, pos, bold=False, align="center"):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    font = pygame.font.Font(font_path, size)
    rendered = font.render(bidi_text, True, color)
    rect = rendered.get_rect(center=pos) if align=="center" else rendered.get_rect(topleft=pos)
    surface.blit(rendered, rect)
    return rect

def load_profiles():
    if not os.path.exists(PROFILE_FILE):
        return []  # return empty list if file doesn't exist
    with open(PROFILE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]  # wrap single dict in list
        else:
            return []


def save_profiles(profiles):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)

# ----------------------------
# Profile Screen
# ----------------------------
def run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    clock = pygame.time.Clock()
    running = True

    # Load avatars
    avatar_images = {}
    for a in AVAILABLE_AVATARS:
        path = os.path.join(AVATAR_FOLDER, a)
        if os.path.exists(path):
            avatar_images[a] = pygame.image.load(path).convert_alpha()
        else:
            print(f"Missing avatar: {path}")

    # State
    profiles = load_profiles()
    current_input = {"name": "", "age": ""}
    selected_avatar = AVAILABLE_AVATARS[0]
    mode = "select"  # "select" or "create"
    selected_profile = None

    # Rects
    name_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, 200, 300, 60)
    age_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, 300, 300, 60)
    create_button = pygame.Rect(SCREEN_WIDTH//2 - 100, 400, 200, 60)

    # Input state
    active_input = None  # "name" or "age"

    while running:
        screen.fill((180, 180, 180))
        mouse_pos = pygame.mouse.get_pos()

        # Draw title
        draw_arabic_text(screen, "إنشاء ملف جديد", ARABIC_BOLD_FONT_PATH, 48, (0,0,0), (SCREEN_WIDTH//2, 60), align="center")

        # Draw input boxes
        pygame.draw.rect(screen, (255,255,255), name_rect)
        pygame.draw.rect(screen, (0,0,0), name_rect, 2)
        draw_arabic_text(screen, f"الاسم: {current_input['name']}", ARABIC_FONT_PATH, 36, (0,0,0), name_rect.center, align="center")

        pygame.draw.rect(screen, (255,255,255), age_rect)
        pygame.draw.rect(screen, (0,0,0), age_rect, 2)
        draw_arabic_text(screen, f"العمر: {current_input['age']}", ARABIC_FONT_PATH, 36, (0,0,0), age_rect.center, align="center")

        # Draw create button
        pygame.draw.rect(screen, (255,102,0), create_button)
        draw_arabic_text(screen, "ملف جديد", ARABIC_BOLD_FONT_PATH, 36, (255,255,255), create_button.center, align="center")

        # Draw avatars
        avatar_start_x = SCREEN_WIDTH//2 - (len(AVAILABLE_AVATARS)*80)//2
        avatar_y = 500
        avatar_rects = []
        for i, a in enumerate(AVAILABLE_AVATARS):
            rect = pygame.Rect(avatar_start_x + i*80, avatar_y, 64, 64)
            avatar_rects.append((rect, a))
            screen.blit(pygame.transform.scale(avatar_images[a], (64,64)), rect.topleft)
            if a == selected_avatar:
                pygame.draw.rect(screen, (255, 102, 0), rect, 3)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if active_input and event.key == pygame.K_BACKSPACE:
                    current_input[active_input] = current_input[active_input][:-1]
                elif active_input:
                    if len(event.unicode) > 0:
                        current_input[active_input] += event.unicode
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if name_rect.collidepoint(mouse_pos):
                    active_input = "name"
                elif age_rect.collidepoint(mouse_pos):
                    active_input = "age"
                elif create_button.collidepoint(mouse_pos):
                    # Save profile
                    profile = {
                        "name": current_input["name"],
                        "age": current_input["age"],
                        "avatar": selected_avatar
                    }
                    profiles.append(profile)
                    save_profiles(profiles)
                    selected_profile = profile
                    running = False
                else:
                    active_input = None
                # Avatar click
                for rect, a in avatar_rects:
                    if rect.collidepoint(mouse_pos):
                        selected_avatar = a

        pygame.display.flip()
        clock.tick(60)

    return selected_profile

if __name__ == "__main__":
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Profile Screen Test")

    profile = run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    print("Selected profile:", profile)
    pygame.quit()

