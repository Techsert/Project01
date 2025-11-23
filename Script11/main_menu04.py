import os
import pygame
import arabic_reshaper
from bidi.algorithm import get_display
from alphabit_name import run_alphabit_name
from alphabit_sound import run_alphabit_sound

# ===========================
# CONFIG
# ===========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(BASE_DIR, "../assets/img/main")
SOUND_PATH = os.path.join(BASE_DIR, "../assets/sounds/main")
ARABIC_FONT_PATH = os.path.join(BASE_DIR, "../assets/fonts/NotoNaskhArabic-Regular.ttf")

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
        return pygame.font.Font(ARABIC_FONT_PATH, size)
    except Exception as e:
        print("Font load error:", e)
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
        self.hovered_button = None
        self.hover_channel = pygame.mixer.Channel(5)  # Dedicated channel for hover sounds
        self.start_sound_path = os.path.join(SOUND_PATH, "lets_start.mp3")

        # Background music
        self.bg_music = os.path.join(SOUND_PATH, "bg_sound.mp3")
        self.play_bg_music()

        # Load images
        self.welcome_bg = load_image(os.path.join(IMG_PATH, "background.png"))
        self.section_bg = load_image(os.path.join(IMG_PATH, "section_bg.png"))

        # Define section buttons
        self.section_buttons = [
            {"pos": (0.15, 0.36), "text": "أسماء الحُروف", "action": self.launch_alphabit_name, "hover": os.path.join(SOUND_PATH, "hover_alphabetNames.wav")},
            {"pos": (0.50, 0.36), "text": "أصوات الحُروف", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_alphabetSounds.wav")},
            {"pos": (0.85, 0.36), "text": "أشكال الحُروف", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_alphabetShaps.wav")},
            {"pos": (0.15, 0.89), "text": "الأعداد", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_numbers.wav")},
            {"pos": (0.50, 0.89), "text": "الألوان", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_colours.wav")},
            {"pos": (0.85, 0.89), "text": "الكَلِمات", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_words.wav")},
        ]

    def draw_arabic_text(self, text, size, color, center, bold=False):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        font_name = "NotoNaskhArabic-Bold.ttf" if bold else "NotoNaskhArabic-Regular.ttf"
        font_path = os.path.join(BASE_DIR, "../assets/fonts", font_name)
        font = pygame.font.Font(font_path, size)
        rendered = font.render(bidi_text, True, color)
        rect = rendered.get_rect(center=center)
        screen.blit(rendered, rect)  # ✅ use global screen, not self.screen



    # Delay moving to section slide  
    def start_with_delay(self):
        # Play the start sound
        sound = load_sound(self.start_sound_path)
        if sound:
            sound.play()
            # Schedule the transition after the sound length
            delay_ms = int(sound.get_length() * 1000)
            pygame.time.set_timer(pygame.USEREVENT + 1, delay_ms)


    # Background music
    def play_bg_music(self):
        try:
            pygame.mixer.music.load(self.bg_music)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Background music error:", e)

    def play_start_sound(self):
        sound = load_sound(self.start_sound_path)
        if sound:
            sound.play()


    # Play hover sound once per hover
    def play_hover_sound(self, path):
        sound = load_sound(path)
        if sound:
            if self.hover_channel.get_busy():
                self.hover_channel.stop()
            self.hover_channel.play(sound)

    # Quiz launches
    def launch_alphabit_name(self):
        print("Launching Alphabit Name...")
        pygame.mixer.stop()
        run_alphabit_name(screen, self)

    def launch_alphabit_sound(self):
        print("Launching Alphabit Sound...")
        pygame.mixer.stop()
        run_alphabit_sound(screen, main_app=self)

    # Draw text helper
    def draw_text(self, text, font_size, color, center):
        font = load_font(font_size)
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(center=center)
        screen.blit(rendered, rect)

    # Draw button text
    def draw_button(self, button_info):
        x = int(button_info["pos"][0] * SCREEN_WIDTH)
        y = int(button_info["pos"][1] * SCREEN_HEIGHT)
        self.draw_arabic_text(button_info["text"], 150, (51, 51, 51), (x, y))

    # Main loop
    def run(self):
        while self.running:
            screen.fill((255, 255, 255))

            mouse_pos = pygame.mouse.get_pos()

            # Draw current screen
            if self.show_welcome:
                if self.welcome_bg:
                    screen.blit(self.welcome_bg, (0, 0))
                self.draw_arabic_text("مرحباً", 250, (51, 51, 51), (SCREEN_WIDTH//2, SCREEN_HEIGHT//3), bold=True)
                # === Draw "هيا نبدأ" button with frame ===
                text = "هيا نبدأ"
                font_size = 150
                color = (255, 102, 0)
                center_x, center_y = int(SCREEN_WIDTH * 0.45), int(SCREEN_HEIGHT * 0.65)


                # Define clickable rect
                rect_width = SCREEN_WIDTH * 0.15   # adjust width
                rect_height = SCREEN_HEIGHT * 0.20   # adjust height
                start_rect = pygame.Rect(center_x - rect_width // 2,
                                         center_y - rect_height // 2,
                                         rect_width, rect_height)

                # Draw frame (background + border)
                pygame.draw.rect(screen, (255, 255, 255), start_rect, border_radius=30)  # background
                pygame.draw.rect(screen, (255, 102, 0), start_rect, 5, border_radius=30)  # border outline

                # Render Arabic text centered in the frame
                reshaped_text = arabic_reshaper.reshape(text)
                bidi_text = get_display(reshaped_text)
                font_path = os.path.join(BASE_DIR, "../assets/fonts/NotoNaskhArabic-Bold.ttf")  # bold font hardcoded
                font = pygame.font.Font(font_path, font_size)
                rendered = font.render(bidi_text, True, color)
                text_rect = rendered.get_rect(center=start_rect.center)
                screen.blit(rendered, text_rect)


            else:
                if self.section_bg:
                    screen.blit(self.section_bg, (0, 0))
                for btn in self.section_buttons:
                    self.draw_button(btn)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.USEREVENT + 1:
                    self.show_welcome = False
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Stop the timer
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.show_welcome:
                        # Define the start button clickable rect
                        rect_width = SCREEN_WIDTH * 0.15
                        rect_height = SCREEN_HEIGHT * 0.20
                        center_x, center_y = int(SCREEN_WIDTH * 0.45), int(SCREEN_HEIGHT * 0.65)
                        start_rect = pygame.Rect(center_x - rect_width // 2,
                                                 center_y - rect_height // 2,
                                                 rect_width, rect_height)

                        # Only go to next screen if click is inside the button
                        if start_rect.collidepoint(mouse_pos):
                            self.start_with_delay()  # Play sound + delay transition

                elif event.type == pygame.MOUSEMOTION and not self.show_welcome: # control the buttons of selections
                    # Track hover
                    hovered = None
                    for btn in self.section_buttons:
                        x = int(btn["pos"][0] * SCREEN_WIDTH)
                        y = int(btn["pos"][1] * SCREEN_HEIGHT)
                        rect_width = SCREEN_WIDTH * 0.25   # 25% of screen width
                        rect_height = SCREEN_HEIGHT * 0.2  # 20% of screen height
                        rect = pygame.Rect(x - rect_width // 2, y - rect_height // 2, rect_width, rect_height)

                        if rect.collidepoint(mouse_pos):
                            hovered = btn
                            break
                    if hovered != self.hovered_button:
                        self.hovered_button = hovered
                        if hovered is not None:
                            self.play_hover_sound(hovered["hover"])

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    app = QuizApp()
    app.run()
