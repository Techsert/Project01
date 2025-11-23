import os
import pygame
from alphabit_name import run_alphabit_name
from alphabit_sound import run_alphabit_sound

# ===========================
# CONFIG
# ===========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(BASE_DIR, "../assets/img/main")
SOUND_PATH = os.path.join(BASE_DIR, "../assets/sounds/main")

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen setup
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Welcome to Learning World - Level One")
clock = pygame.time.Clock()

# Load fonts
def load_font(size):
    try:
        return pygame.font.Font(None, size)  # Replace None with custom font if available
    except:
        return pygame.font.SysFont("Arial", size)

# Load images
def load_image(filename, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
    try:
        img = pygame.image.load(filename).convert_alpha()
        return pygame.transform.smoothscale(img, (width, height))
    except Exception as e:
        print(f"Image load error ({filename}):", e)
        return None

# Load sounds
def load_sound(filename):
    try:
        return pygame.mixer.Sound(filename)
    except Exception as e:
        print(f"Sound load error ({filename}):", e)
        return None

# ===========================
# Main QuizApp Class
# ===========================
class QuizApp:
    def __init__(self):
        self.running = True
        self.show_welcome = True
        self.bg_music = os.path.join(SOUND_PATH, "bg_sound.mp3")
        self.play_bg_music()
        self.buttons = []

        # Prepare welcome screen assets
        self.welcome_bg = load_image(os.path.join(IMG_PATH, "background.png"))
        self.section_bg = load_image(os.path.join(IMG_PATH, "section_bg.png"))

        # Button setup: rect, text, action, hover_sound
        self.section_buttons = [
            {"pos": (0.15, 0.36), "text": "أسماء الحُروف", "action": self.launch_alphabit_name, "hover": os.path.join(SOUND_PATH, "hover_alphabetNames.wav")},
            {"pos": (0.50, 0.36), "text": "أصوات الحُروف", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_alphabetSounds.wav")},
            {"pos": (0.85, 0.36), "text": "أشكال الحُروف", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_alphabetShaps.wav")},
            {"pos": (0.15, 0.89), "text": "الأعداد", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_numbers.wav")},
            {"pos": (0.50, 0.89), "text": "الألوان", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_colours.wav")},
            {"pos": (0.85, 0.89), "text": "الكَلِمات", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_words.wav")},
        ]

    # Background music
    def play_bg_music(self):
        try:
            pygame.mixer.music.load(self.bg_music)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Background music error:", e)

    # Play hover sound
    def play_hover_sound(self, path):
        sound = load_sound(path)
        if sound:
            sound.play()

    # Start quiz buttons
    def launch_alphabit_name(self):
        print("Launching Alphabit Name...")
        pygame.mixer.stop()
        run_alphabit_name(screen, self)

    def launch_alphabit_sound(self):
        print("Launching Alphabit Sound...")
        pygame.mixer.stop()
        run_alphabit_sound(screen, main_app=self)

    # Draw text
    def draw_text(self, text, font_size, color, center):
        font = load_font(font_size)
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(center=center)
        screen.blit(rendered, rect)

    # Draw button
    def draw_button(self, button_info):
        x = int(button_info["pos"][0] * SCREEN_WIDTH)
        y = int(button_info["pos"][1] * SCREEN_HEIGHT)
        self.draw_text(button_info["text"], 60, (51, 51, 51), (x, y))

    # Main loop
    def run(self):
        while self.running:
            screen.fill((0, 0, 0))

            if self.show_welcome:
                if self.welcome_bg:
                    screen.blit(self.welcome_bg, (0, 0))
                self.draw_text("مرحباً", 250, (51, 51, 51), (SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
                self.draw_text("هيا نبدأ", 72, (255, 102, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT*0.7))
            else:
                if self.section_bg:
                    screen.blit(self.section_bg, (0, 0))
                for btn in self.section_buttons:
                    self.draw_button(btn)

            # Event handling
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.show_welcome:
                        self.show_welcome = False
                    else:
                        # Check buttons click
                        for btn in self.section_buttons:
                            x = int(btn["pos"][0] * SCREEN_WIDTH)
                            y = int(btn["pos"][1] * SCREEN_HEIGHT)
                            rect = pygame.Rect(x-100, y-50, 200, 100)
                            if rect.collidepoint(mouse_pos):
                                btn["action"]()
                elif event.type == pygame.MOUSEMOTION:
                    # Hover sound
                    if not self.show_welcome:
                        for btn in self.section_buttons:
                            x = int(btn["pos"][0] * SCREEN_WIDTH)
                            y = int(btn["pos"][1] * SCREEN_HEIGHT)
                            rect = pygame.Rect(x-100, y-50, 200, 100)
                            if rect.collidepoint(mouse_pos):
                                self.play_hover_sound(btn["hover"])

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    app = QuizApp()
    app.run()
