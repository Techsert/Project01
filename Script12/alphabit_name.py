import os
import pygame
from PIL import Image

# ========================
# CONFIG
# ========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(BASE_DIR, "../assets/img/alphabitSound")
SOUND_PATH = os.path.join(BASE_DIR, "../assets/sounds/alphabitSound")
FONT_PATH = os.path.join(BASE_DIR, "../assets/fonts/NotoNaskhArabic-Regular.ttf")

# ========================
# SLIDE DATA
# ========================
slides = [
    {
        "title": "الحُروف العَرَبية",
        "narration": os.path.join(SOUND_PATH, "intro.wav"),
        "images": [
            {
                "path": os.path.join(IMG_PATH, "bg-nt.png"),
                "delay": 0,
                "scale": (0.95, 0.82),
                "position": "center"
            },
            {
                "path": os.path.join(IMG_PATH, "hard.png"),
                "sound": os.path.join(SOUND_PATH, "areyouready.wav"),
                "delay": 4000,
                "scale": (0.25, 0.55),
                "position": "center"
            },
        ]
    },
]

# ========================
# MAIN FUNCTION
# ========================
def run_alphabit_name(screen, main_app=None):
    clock = pygame.time.Clock()
    running = True
    slide_index = 0
    current_slide = slides[slide_index]
    active_images = []
    next_image_time = []
    font = pygame.font.Font(FONT_PATH, 100)

    # stop any previous music
    pygame.mixer.music.stop()

    # --- Play narration ---
    narration = current_slide.get("narration")
    if narration and os.path.exists(narration):
        pygame.mixer.music.load(narration)
        pygame.mixer.music.play()

    played_sounds = set()
    # --- Load images with timing ---
    start_time = pygame.time.get_ticks()
    for img_info in current_slide["images"]:
        img_path = img_info["path"]
        delay = img_info.get("delay", 0)
        if os.path.exists(img_path):
            image = pygame.image.load(img_path).convert_alpha()
            active_images.append((image, img_info))
            next_image_time.append(delay)
        else:
            print("Missing image:", img_path)


    while running:
        screen.fill((255, 255, 255))

        # Get current time
        elapsed = pygame.time.get_ticks() - start_time

        # --- Draw visible images ---
        for i, (img, info) in enumerate(active_images):
            if elapsed >= next_image_time[i]:
                img_w, img_h = img.get_size()
                scale_w = int(screen.get_width() * info.get("scale", (1, 1))[0])
                scale_h = int(screen.get_height() * info.get("scale", (1, 1))[1])
                img_scaled = pygame.transform.smoothscale(img, (scale_w, scale_h))

                # position
                pos = info.get("position", "center")
                rect = img_scaled.get_rect()
                if pos == "center":
                    rect.center = (screen.get_width() // 2, screen.get_height() // 2)
                elif pos == "bottom-right":
                    rect.bottomright = (screen.get_width() - 20, screen.get_height() - 20)
                elif pos == "top-right":
                    rect.topright = (screen.get_width() - 20, 20)
                elif pos == "bottom-left":
                    rect.bottomleft = (20, screen.get_height() - 20)
                elif pos == "top-left":
                    rect.topleft = (20, 20)
                screen.blit(img_scaled, rect)
                # Get the sound path for this image
                sound_path = info.get("sound")
                # Play sound if image has sound and its time has just come
                if sound_path and sound_path != current_slide.get("narration") and i not in played_sounds:
                    snd = pygame.mixer.Sound(sound_path)
                    snd.play()
                    played_sounds.add(i)


        # --- Draw title ---
        title_text = current_slide.get("title", "")
        title_surface = font.render(title_text, True, (51, 51, 51))
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() * 0.1))
        screen.blit(title_surface, title_rect)

        # --- Back Button ---
        back_text = "⬅ العودة"
        back_font = pygame.font.Font(FONT_PATH, 60)
        back_surface = back_font.render(back_text, True, (255, 255, 255))
        back_rect = back_surface.get_rect(center=(screen.get_width() * 0.1, screen.get_height() * 0.9))
        pygame.draw.rect(screen, (255, 102, 102), back_rect.inflate(40, 20), border_radius=25)
        screen.blit(back_surface, back_rect)

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    running = False  # just exit this screen


        pygame.display.flip()
        clock.tick(60)

    # Cleanup and return
    pygame.mixer.music.stop()
    if main_app:
        main_app.show_intro_screen()
# ========================
# Standalone Run Support
# ========================
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))  # or use fullscreen if you prefer
##    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("أسماء الحروف")
    run_alphabit_name(screen)
    pygame.quit()
