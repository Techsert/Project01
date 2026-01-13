import pygame
import os
import time
from screen_helpers import confirm_popup, dynamic_font
from profile_system import load_profiles

# ============================================================
# INITIALIZATION
# ============================================================
pygame.init()
pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_DIR, "../assets/fonts/NotoNaskhArabic-Regular.ttf")
BOLD_FONT_PATH = os.path.join(BASE_DIR, "../assets/fonts/NotoNaskhArabic-Bold.ttf")
IMG_PATH = os.path.join(BASE_DIR, "../assets/img/alphabitSound")
SOUND_PATH = os.path.join(BASE_DIR, "../assets/sounds/alphabitSound")
AVATAR_PATH = os.path.join(BASE_DIR, "../assets/profiles/avatars")

# ============================================================
# SLIDES (sample shortened — keep your full 28-slide list)
# ============================================================
slides = [
    {
        "title": "حرف الألف",
        "narration": f"{SOUND_PATH}/01alef-s.wav",
        "images": [
            {"path": f"{IMG_PATH}/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": f"{IMG_PATH}/01alef.png", "delay": 0, "scale": (0.05, 0.50), "position": "center", "duration": 2000},
            {"path": f"{IMG_PATH}/01alef-f.png", "sound": f"{SOUND_PATH}/01alef-f.wav", "delay": 3000, "scale": (0.05, 0.45), "position": "center-right", "offset": {"x": -200, "y": 0}},
            {"path": f"{IMG_PATH}/01alef-k.png", "sound": f"{SOUND_PATH}/01alef-k.wav", "delay": 7000, "scale": (0.05, 0.45), "position": "center"},
            {"path": f"{IMG_PATH}/01alef-d.png", "sound": f"{SOUND_PATH}/01alef-d.wav", "delay": 10000, "scale": (0.05, 0.45), "position": "center-left", "offset": {"x": 180, "y": 0}},
        ],
    },
    {
        "title": "أحسنت",
        "images": [
            {"path": f"{IMG_PATH}/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": f"{IMG_PATH}/coach.png", "sound": f"{SOUND_PATH}/welldone.wav", "delay": 1000, "scale": (0.30, 0.40), "position": "center"},
        ],
    },
]

# ============================================================
# MAIN CLASS
# ============================================================
class AlphabitSoundScreen:
    def __init__(self, screen, main_app=None, active_profile=None):
        self.screen = screen
        self.main_app = main_app
        self.active_profile = active_profile
        self.slides = slides
        self.index = 0
        self.start_time = pygame.time.get_ticks()
        self.channel_narr = pygame.mixer.Channel(0)
        self.channel_fx = pygame.mixer.Channel(1)
        self.images = []
        self.buttons = []
        self.font_loader = lambda s, bold=False: dynamic_font(screen.get_height(), FONT_PATH, BOLD_FONT_PATH, size_ratio=s/screen.get_height(), bold=bold)

        # Load profile avatar
        self.profile_img = None
        if self.active_profile and os.path.exists(os.path.join(AVATAR_PATH, self.active_profile.get("avatar", ""))):
            avatar_path = os.path.join(AVATAR_PATH, self.active_profile["avatar"])
            try:
                img = pygame.image.load(avatar_path).convert_alpha()
                self.profile_img = pygame.transform.smoothscale(img, (80, 80))
            except Exception as e:
                print("Profile avatar error:", e)

        # Load exit icon
        self.exit_img = None
        exit_path = os.path.join(BASE_DIR, "../assets/img/main/exit_icon.png")
        if os.path.exists(exit_path):
            self.exit_img = pygame.image.load(exit_path).convert_alpha()
            self.exit_img = pygame.transform.smoothscale(self.exit_img, (70, 70))

        self.load_slide()

    # --------------------------------------------------------
    def stop_sounds(self):
        pygame.mixer.stop()

    def load_slide(self):
        self.stop_sounds()
        slide = self.slides[self.index]
        self.start_time = pygame.time.get_ticks()
        self.images.clear()

        # play narration
        narration = slide.get("narration")
        if narration and os.path.exists(narration):
            try:
                self.channel_narr.play(pygame.mixer.Sound(narration))
            except Exception as e:
                print("Narration error:", e)

        # preload images
        for img_data in slide["images"]:
            img_path = img_data["path"]
            if not os.path.exists(img_path):
                continue
            img = pygame.image.load(img_path).convert_alpha()
            w = int(self.screen.get_width() * img_data.get("scale", (0.3, 0.3))[0])
            h = int(self.screen.get_height() * img_data.get("scale", (0.3, 0.3))[1])
            img = pygame.transform.smoothscale(img, (w, h))
            rect = img.get_rect(center=self.screen.get_rect().center)
            self.images.append({"surf": img, "rect": rect, "data": img_data})

    # --------------------------------------------------------
    def draw(self):
        self.screen.fill((255, 255, 255))
        slide = self.slides[self.index]
        elapsed = pygame.time.get_ticks() - self.start_time

        # Title
        title_font = self.font_loader(int(self.screen.get_height() * 0.08), bold=True)
        title_surface = title_font.render(slide["title"], True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, int(self.screen.get_height() * 0.08)))
        self.screen.blit(title_surface, title_rect)

        # Images
        for img_obj in self.images:
            img_data = img_obj["data"]
            if elapsed >= img_data.get("delay", 0):
                self.draw_image(img_obj)

        # Profile + Exit Buttons
        self.draw_top_buttons()

        # Navigation
        self.draw_nav_buttons()

        pygame.display.flip()

    # --------------------------------------------------------
    def draw_image(self, img_obj):
        img_data = img_obj["data"]
        rect = img_obj["rect"].copy()

        offset = img_data.get("offset", {"x": 0, "y": 0})
        rect.x += offset.get("x", 0)
        rect.y += offset.get("y", 0)

        pos = img_data.get("position", "center")
        if pos == "center-right":
            rect.centerx = int(self.screen.get_width() * 0.8)
        elif pos == "center-left":
            rect.centerx = int(self.screen.get_width() * 0.2)
        elif pos == "top":
            rect.centery = int(self.screen.get_height() * 0.2)
        elif pos == "bottom":
            rect.centery = int(self.screen.get_height() * 0.8)

        self.screen.blit(img_obj["surf"], rect)

        # Play sound if defined and not overlapping
        if "sound" in img_data and not self.channel_fx.get_busy():
            sound_path = img_data["sound"]
            if os.path.exists(sound_path):
                try:
                    self.channel_fx.play(pygame.mixer.Sound(sound_path))
                except Exception as e:
                    print("Sound error:", e)

    # --------------------------------------------------------
    def draw_top_buttons(self):
        W, H = self.screen.get_size()
        margin = 20

        # Profile image
        if self.profile_img:
            profile_rect = self.profile_img.get_rect(topright=(W - margin - 80, margin))
            self.screen.blit(self.profile_img, profile_rect)
            pygame.draw.rect(self.screen, (255, 165, 0), profile_rect, 3, border_radius=12)

        # Exit icon
        if self.exit_img:
            exit_rect = self.exit_img.get_rect(topright=(W - margin, margin))
            self.screen.blit(self.exit_img, exit_rect)
            pygame.draw.rect(self.screen, (200, 0, 0), exit_rect, 2, border_radius=10)
            self.exit_rect = exit_rect
        else:
            self.exit_rect = pygame.Rect(W - 100, 20, 80, 80)

    # --------------------------------------------------------
    def draw_nav_buttons(self):
        W, H = self.screen.get_size()
        btn_font = self.font_loader(int(H * 0.05))
        btn_color = (230, 230, 230)
        text_color = (0, 0, 0)
        self.buttons = []

        def draw_button(label, center_pos, tag):
            surf = btn_font.render(label, True, text_color)
            rect = surf.get_rect(center=center_pos)
            pygame.draw.rect(self.screen, btn_color, rect.inflate(40, 20), border_radius=12)
            self.screen.blit(surf, rect)
            self.buttons.append((tag, rect))

        if self.index > 0:
            draw_button("السابق", (W * 0.15, H * 0.9), "prev")
        draw_button("العودة", (W * 0.5, H * 0.9), "back")
        if self.index < len(self.slides) - 1:
            draw_button("التالي", (W * 0.85, H * 0.9), "next")

    # --------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Exit button
            if self.exit_rect.collidepoint(event.pos):
                confirm = confirm_popup(self.screen, "هل تريد الخروج؟", self.font_loader)
                if confirm:
                    self.stop_sounds()
                    if self.main_app:
                        self.main_app.show_section_screen()
                    else:
                        pygame.quit()
                        exit()
            # Navigation
            for tag, rect in self.buttons:
                if rect.collidepoint(event.pos):
                    if tag == "next": self.next_slide()
                    elif tag == "prev": self.prev_slide()
                    elif tag == "back": self.back_to_main()

    # --------------------------------------------------------
    def next_slide(self):
        if self.index < len(self.slides) - 1:
            self.index += 1
            self.load_slide()

    def prev_slide(self):
        if self.index > 0:
            self.index -= 1
            self.load_slide()

    def back_to_main(self):
        self.stop_sounds()
        if self.main_app:
            self.main_app.show_section_screen()
        else:
            pygame.quit()
            exit()

# ============================================================
# RUN FUNCTION
# ============================================================
def run_alphabit_sound(screen=None, main_app=None, profile=None):
    if screen is None:
        info = pygame.display.Info()
        screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
        pygame.display.set_caption("Alphabit Sound Lesson")

    # Stop menu music
    pygame.mixer.music.stop()

    clock = pygame.time.Clock()
    app = AlphabitSoundScreen(screen, main_app, profile)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            else:
                app.handle_event(event)

        app.draw()
        clock.tick(30)

    if main_app:
        main_app.show_section_screen()
    else:
        pygame.quit()


if __name__ == "__main__":
    run_alphabit_sound()
