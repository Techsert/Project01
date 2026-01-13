import os
import pygame
import arabic_reshaper
from bidi.algorithm import get_display
from profile_screen09 import run_profile_screen, run_profile_manage_screen
from alphabit_name import run_alphabit_name
from alphabit_sound import run_alphabit_sound
import sys

# ===========================
# CONFIG
# ===========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(BASE_DIR, "../assets/img/main")
SOUND_PATH = os.path.join(BASE_DIR, "../assets/sounds/main")
AVATAR_PATH = os.path.join(BASE_DIR, "../assets/profiles/avatars")
ARABIC_FONT_PATH = os.path.join(BASE_DIR, "../assets/fonts/NotoNaskhArabic-Regular.ttf")
ARABIC_BOLD_FONT_PATH = os.path.join(BASE_DIR, "../assets/fonts/NotoNaskhArabic-Bold.ttf")

pygame.init()
pygame.mixer.init()

info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Welcome to Learning World - Level One")
clock = pygame.time.Clock()


# ===========================
# HELPER FUNCTIONS
# ===========================
def load_font(size, bold=False):
    try:
        font_path = ARABIC_BOLD_FONT_PATH if bold else ARABIC_FONT_PATH
        return pygame.font.Font(font_path, size)
    except Exception:
        return pygame.font.SysFont("Arial", size)


def load_image(filename, width=None, height=None):
    try:
        img = pygame.image.load(filename).convert_alpha()
        if width and height:
            img = pygame.transform.smoothscale(img, (width, height))
        return img
    except:
        return None


def load_sound(filename):
    try:
        return pygame.mixer.Sound(filename)
    except:
        return None


# ===========================
# CONFIRM POPUP
# ===========================
def confirm_popup(screen, msg):
    """Display Yes/No confirmation popup."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    FONT = pygame.font.SysFont("Arial", 36)
    TITLE = pygame.font.SysFont("Arial", 52, bold=True)

    box = pygame.Rect(0, 0, 500, 240)
    box.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.draw.rect(screen, (255, 255, 255), box, border_radius=20)
    pygame.draw.rect(screen, (255, 102, 0), box, 4, border_radius=20)

    text = TITLE.render(msg, True, (0, 0, 0))
    screen.blit(text, (box.centerx - text.get_width() // 2, box.top + 40))

    yes = pygame.Rect(box.centerx - 140, box.bottom - 80, 120, 50)
    no = pygame.Rect(box.centerx + 20, box.bottom - 80, 120, 50)
    pygame.draw.rect(screen, (0, 170, 0), yes, border_radius=10)
    pygame.draw.rect(screen, (170, 0, 0), no, border_radius=10)
    screen.blit(FONT.render("Yes", True, (255, 255, 255)), (yes.centerx - 30, yes.centery - 18))
    screen.blit(FONT.render("No", True, (255, 255, 255)), (no.centerx - 25, no.centery - 18))

    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if yes.collidepoint(e.pos):
                    return True
                elif no.collidepoint(e.pos):
                    return False
        pygame.time.wait(10)


# ===========================
# MAIN CLASS
# ===========================
class QuizApp:
    def __init__(self, selected_profile):
        self.selected_profile = selected_profile
        self.running = True
        self.show_welcome = True
        self.hovered_button = None
        self.hover_channel = pygame.mixer.Channel(5)
        self.start_sound_path = os.path.join(SOUND_PATH, "lets_start.mp3")

        # Music
        self.bg_music = os.path.join(SOUND_PATH, "bg_sound.mp3")
        self.play_bg_music()

        # Backgrounds
        self.welcome_bg = load_image(os.path.join(IMG_PATH, "background.png"), SCREEN_WIDTH, SCREEN_HEIGHT)
        self.section_bg = load_image(os.path.join(IMG_PATH, "section_bg.png"), SCREEN_WIDTH, SCREEN_HEIGHT)

        # Profile icon
        avatar_name = selected_profile.get("avatar") if selected_profile else None
        avatar_path = os.path.join(AVATAR_PATH, avatar_name) if avatar_name else os.path.join(IMG_PATH, "profile_icon.png")
        self.profile_icon = load_image(avatar_path, 100, 100)
        self.profile_rect = self.profile_icon.get_rect(topright=(SCREEN_WIDTH - 20, 20))

        # Exit button
        self.exit_icon = load_image(os.path.join(IMG_PATH, "exit_icon.png"), 90, 90)
        self.exit_rect = self.exit_icon.get_rect(bottomright=(SCREEN_WIDTH - 30, SCREEN_HEIGHT - 30))

        # Section buttons
        self.section_buttons = [
            {"pos": (0.15, 0.36), "text": "أسماء الحُروف", "action": self.launch_alphabit_name, "hover": os.path.join(SOUND_PATH, "hover_alphabetNames.wav")},
            {"pos": (0.50, 0.36), "text": "أصوات الحُروف", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_alphabetSounds.wav")},
            {"pos": (0.85, 0.36), "text": "أشكال الحُروف", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_alphabetShaps.wav")},
            {"pos": (0.15, 0.89), "text": "الأعداد", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_numbers.wav")},
            {"pos": (0.50, 0.89), "text": "الألوان", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_colours.wav")},
            {"pos": (0.85, 0.89), "text": "الكَلِمات", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_words.wav")},
        ]
        for btn in self.section_buttons:
            x = int(btn["pos"][0] * SCREEN_WIDTH)
            y = int(btn["pos"][1] * SCREEN_HEIGHT)
            w = SCREEN_WIDTH * 0.25
            h = SCREEN_HEIGHT * 0.1
            btn["rect"] = pygame.Rect(x - w // 2, y - h // 2, w, h)

        self.start_rect = pygame.Rect(SCREEN_WIDTH * 0.425, SCREEN_HEIGHT * 0.55, SCREEN_WIDTH * 0.15, SCREEN_HEIGHT * 0.2)

    # ---------------- TEXT ----------------
    def draw_arabic_text(self, text, size, color, center, bold=False):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        font = load_font(size, bold=bold)
        rendered = font.render(bidi_text, True, color)
        rect = rendered.get_rect(center=center)
        screen.blit(rendered, rect)

    # ---------------- SOUND ----------------
    def play_hover_sound(self, path):
        sound = load_sound(path)
        if sound:
            if self.hover_channel.get_busy():
                self.hover_channel.stop()
            self.hover_channel.play(sound)

    def play_bg_music(self):
        try:
            pygame.mixer.music.load(self.bg_music)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Music error:", e)

    # ---------------- ACTIONS ----------------
    def start_with_delay(self):
        sound = load_sound(self.start_sound_path)
        if sound:
            sound.play()
            delay = int(sound.get_length() * 1000)
            pygame.time.set_timer(pygame.USEREVENT + 1, delay)

    def launch_alphabit_name(self):
        pygame.mixer.stop()
        run_alphabit_name(screen, self)

    def launch_alphabit_sound(self):
        pygame.mixer.stop()
        run_alphabit_sound(screen, main_app=self)

    def open_profile_manager(self):
        pygame.mixer.music.stop()
        updated = run_profile_manage_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, self.selected_profile)
        if updated:
            if updated.get("_deleted"):
                self.selected_profile = run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
            else:
                self.selected_profile.update(updated)
            avatar_path = os.path.join(AVATAR_PATH, self.selected_profile["avatar"])
            self.profile_icon = load_image(avatar_path, 100, 100)
            self.profile_rect = self.profile_icon.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        self.play_bg_music()

    # ---------------- DRAWING ----------------
    def draw_button(self, btn):
        self.draw_arabic_text(btn["text"], 150, (51, 51, 51), btn["rect"].center)

    # ---------------- MAIN LOOP ----------------
    def run(self):
        while self.running:
            screen.fill((255, 255, 255))
            mouse_pos = pygame.mouse.get_pos()

            # Background
            if self.show_welcome:
                if self.welcome_bg: screen.blit(self.welcome_bg, (0, 0))
                self.draw_arabic_text("مرحباً", 250, (51,51,51), (SCREEN_WIDTH//2, SCREEN_HEIGHT//3), bold=True)
                pygame.draw.rect(screen, (255,255,255), self.start_rect, border_radius=30)
                pygame.draw.rect(screen, (255,102,0), self.start_rect, 5, border_radius=30)
                self.draw_arabic_text("هيا نبدأ", 150, (255,102,0), self.start_rect.center, bold=True)
            else:
                if self.section_bg: screen.blit(self.section_bg, (0, 0))
                for btn in self.section_buttons:
                    self.draw_button(btn)

            # Profile Icon
            screen.blit(self.profile_icon, self.profile_rect)
            if self.profile_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255,102,0), self.profile_rect, 3, border_radius=10)

            # Exit Button
            if self.exit_icon:
                screen.blit(self.exit_icon, self.exit_rect)
                if self.exit_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (255, 102, 0), self.exit_rect, 3, border_radius=10)

            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if confirm_popup(screen, "Exit the game?"):
                        pygame.quit(); sys.exit()
                elif event.type == pygame.USEREVENT + 1:
                    self.show_welcome = False
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if confirm_popup(screen, "Exit the game?"):
                        pygame.quit(); sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_rect.collidepoint(mouse_pos):
                        if confirm_popup(screen, "Exit the game?"):
                            pygame.quit(); sys.exit()
                    elif self.profile_rect.collidepoint(mouse_pos):
                        self.open_profile_manager()
                        continue
                    elif self.show_welcome and self.start_rect.collidepoint(mouse_pos):
                        self.start_with_delay()
                    elif not self.show_welcome:
                        for btn in self.section_buttons:
                            if btn["rect"].collidepoint(mouse_pos):
                                btn["action"]()
                elif event.type == pygame.MOUSEMOTION and not self.show_welcome:
                    hovered = None
                    for btn in self.section_buttons:
                        if btn["rect"].collidepoint(mouse_pos):
                            hovered = btn
                            break
                    if hovered != self.hovered_button:
                        self.hovered_button = hovered
                        if hovered is not None:
                            self.play_hover_sound(hovered["hover"])

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


# ===========================
# ENTRY POINT
# ===========================
if __name__ == "__main__":
    selected_profile = run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    app = QuizApp(selected_profile)
    app.run()
