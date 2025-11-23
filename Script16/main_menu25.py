import os
import sys
import pygame
import arabic_reshaper
from bidi.algorithm import get_display
from profile_screen13 import run_profile_screen, run_profile_manage_screen
##from alphabit_name import run_alphabit_name
##from alphabit_sound import run_alphabit_sound

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
    except:
        return pygame.font.SysFont("Arial", size)


def dynamic_font(size_ratio=0.05, bold=False):
    """Scale font size relative to screen height."""
    return load_font(int(SCREEN_HEIGHT * size_ratio), bold=bold)


def load_image(filename, width=None, height=None):
    """Load and optionally scale an image."""
    try:
        img = pygame.image.load(filename).convert_alpha()
        if width and height:
            img = pygame.transform.smoothscale(img, (int(width), int(height)))
        return img
    except Exception as e:
        print(f"Image load error: {e}")
        return None


def load_sound(filename):
    try:
        return pygame.mixer.Sound(filename)
    except Exception as e:
        print(f"Sound load error: {e}")
        return None


def load_scaled_background(path, target_width, target_height, keep_aspect=True):
    """Load and scale a background image to the given width/height, centered on screen."""
    try:
        img = pygame.image.load(path).convert_alpha()
        img_w, img_h = img.get_size()

        if keep_aspect:
            # Scale proportionally (fit inside target)
            scale_factor = min(target_width / img_w, target_height / img_h)
            new_size = (int(img_w * scale_factor), int(img_h * scale_factor))
        else:
            # Stretch to fill exactly the target dimensions
            new_size = (int(target_width), int(target_height))

        img = pygame.transform.smoothscale(img, new_size)

        # Center on screen
        x = (SCREEN_WIDTH - new_size[0]) // 2
        y = (SCREEN_HEIGHT - new_size[1]) // 2

        return img, (x, y)

    except Exception as e:
        print(f"Error loading background: {e}")
        return None, (0, 0)





def confirm_popup(screen, msg):
    """Display Yes/No confirmation popup centered on screen."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Smaller and proportional popup box
    box_width = int(SCREEN_WIDTH * 0.3)
    box_height = int(SCREEN_HEIGHT * 0.25)
    box = pygame.Rect(0, 0, box_width, box_height)
    box.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    pygame.draw.rect(screen, (255, 255, 255), box, border_radius=20)
    pygame.draw.rect(screen, (255, 102, 0), box, 4, border_radius=20)

    # Fonts
    title_font = load_font(int(SCREEN_HEIGHT * 0.04), bold=True)
    button_font = load_font(int(SCREEN_HEIGHT * 0.03))

    # Message text
    text = title_font.render(msg, True, (0, 0, 0))
    screen.blit(text, (box.centerx - text.get_width() // 2, box.top + 25))

    # Buttons (scaled)
    btn_w, btn_h = int(box_width * 0.3), int(box_height * 0.35)
    yes = pygame.Rect(box.centerx - btn_w - 20, box.bottom - btn_h - 20, btn_w, btn_h)
    no = pygame.Rect(box.centerx + 20, box.bottom - btn_h - 20, btn_w, btn_h)

    pygame.draw.rect(screen, (0, 170, 0), yes, border_radius=10)
    pygame.draw.rect(screen, (170, 0, 0), no, border_radius=10)

    # Button text
    # Render button labels
    yes_text = button_font.render("Yes", True, (255, 255, 255))
    no_text = button_font.render("No", True, (255, 255, 255))

    # Center text in each button
    yes_text_rect = yes_text.get_rect(center=yes.center)
    no_text_rect = no_text.get_rect(center=no.center)

    screen.blit(yes_text, yes_text_rect)
    screen.blit(no_text, no_text_rect)

    pygame.display.flip()

    # Wait for input
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if yes.collidepoint(e.pos): return True
                elif no.collidepoint(e.pos): return False
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
        # === Welcome Background ===
        welcome_width = int(SCREEN_WIDTH* 1.0)   # 95% of screen width
        welcome_height = int(SCREEN_HEIGHT* 1.0) # 93% of screen height
        self.welcome_bg, self.welcome_bg_pos = load_scaled_background(
            os.path.join(IMG_PATH, "background.png"),
            welcome_width,
            welcome_height,
            keep_aspect=False
        )

        # === Section Background ===
        section_width = int(SCREEN_WIDTH * 0.9)    # 90% of screen width
        section_height = int(SCREEN_HEIGHT * 0.95) # 88% of screen height
        self.section_bg, self.section_bg_pos = load_scaled_background(
            os.path.join(IMG_PATH, "section_bg.png"),
            section_width,
            section_height,
            keep_aspect=False
        )


        # Profile icon
        avatar_name = selected_profile.get("avatar") if selected_profile else None
        avatar_path = os.path.join(AVATAR_PATH, avatar_name) if avatar_name else os.path.join(IMG_PATH, "profile_icon.png")
        self.profile_icon = load_image(avatar_path, SCREEN_WIDTH * 0.04, SCREEN_WIDTH * 0.04)
        self.profile_rect = self.profile_icon.get_rect(topright=(SCREEN_WIDTH - 30, 30))

        # Exit button
        # ============================
        # Exit Button (Bottom Right)
        # ============================
        exit_icon_path = os.path.join(IMG_PATH, "exit_icon.png")

        # You can pick either a fixed size:
        # self.exit_icon = load_image(exit_icon_path, 80, 80)

        # ✅ Or a resolution-based size (recommended)
        icon_width = int(SCREEN_WIDTH * 0.05)   # 5% of screen width
        icon_height = int(SCREEN_HEIGHT * 0.09) # 8% of screen height
        self.exit_icon = load_image(exit_icon_path, icon_width, icon_height)

        self.exit_rect = self.exit_icon.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))



        # Section buttons (positions & scaling relative to section_bg)
        bg_x, bg_y = self.section_bg_pos
        bg_w, bg_h = self.section_bg.get_size()

        self.section_buttons = [
            {"pos": (0.15, 0.36), "text": "أسماء الحُروف", "action": self.launch_alphabit_name,
             "hover": os.path.join(SOUND_PATH, "hover_alphabetNames.wav")},
            {"pos": (0.50, 0.36), "text": "أصوات الحُروف", "action": self.launch_alphabit_sound,
             "hover": os.path.join(SOUND_PATH, "hover_alphabetSounds.wav")},
            {"pos": (0.85, 0.36), "text": "أشكال الحُروف", "action": self.launch_alphabit_sound,
             "hover": os.path.join(SOUND_PATH, "hover_alphabetShaps.wav")},
            {"pos": (0.15, 0.89), "text": "الأعداد", "action": self.launch_alphabit_sound,
             "hover": os.path.join(SOUND_PATH, "hover_numbers.wav")},
            {"pos": (0.50, 0.89), "text": "الألوان", "action": self.launch_alphabit_sound,
             "hover": os.path.join(SOUND_PATH, "hover_colours.wav")},
            {"pos": (0.85, 0.89), "text": "الكَلِمات", "action": self.launch_alphabit_sound,
             "hover": os.path.join(SOUND_PATH, "hover_words.wav")},
        ]

        # Adjust button rects based on section_bg instead of full screen
        btn_w = bg_w * 0.25
        btn_h = bg_h * 0.1

        for btn in self.section_buttons:
            rel_x, rel_y = btn["pos"]
            x = bg_x + int(rel_x * bg_w)
            y = bg_y + int(rel_y * bg_h)
            btn["rect"] = pygame.Rect(x - btn_w // 2, y - btn_h // 2, btn_w, btn_h)


        # Start button
        self.start_rect = pygame.Rect(
            SCREEN_WIDTH * 0.45, SCREEN_HEIGHT * 0.65, SCREEN_WIDTH * 0.15, SCREEN_HEIGHT * 0.2
        )
        # === Additional Buttons (dynamic ratios) ===
        self.extra_buttons = [
            {"label": "Level Check", "color": (0, 204, 0), "x_ratio": 0.29, "y_ratio": 0.25, "w_ratio": 0.15, "h_ratio": 0.10},
            {"label": "Learning", "color": (255, 204, 0), "x_ratio": 0.39, "y_ratio": 0.45, "w_ratio": 0.15, "h_ratio": 0.10},
            {"label": "Quizzes", "color": (255, 51, 51), "x_ratio": 0.49, "y_ratio": 0.65, "w_ratio": 0.15, "h_ratio": 0.10},
        ]

    # ---------------- TEXT ----------------
    def draw_arabic_text(self, text, size_ratio, color, center, bold=False):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        font = dynamic_font(size_ratio, bold=bold)
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
            self.profile_icon = load_image(avatar_path, SCREEN_WIDTH * 0.05, SCREEN_WIDTH * 0.05)
            self.profile_rect = self.profile_icon.get_rect(topright=(SCREEN_WIDTH - 30, 30))
        self.play_bg_music()

        
    # ================= Learning screen =========================
    def open_learning_screen(self):
        """Open a fullscreen screen showing soccerfield.png as background (with profile icon)."""
        soccer_path = os.path.join(IMG_PATH, "soccerfield.png")

        try:
            bg_image = pygame.image.load(soccer_path).convert()
            bg_image = pygame.transform.smoothscale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Error loading soccerfield.png: {e}")
            return

        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False  # Exit this screen on ESC
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if self.profile_rect.collidepoint(e.pos):
                        # ✅ Allow opening profile manager directly from this screen
                        self.open_profile_manager()
                        # Reload background after returning
                        bg_image = pygame.image.load(soccer_path).convert()
                        bg_image = pygame.transform.smoothscale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    else:
                        # Click anywhere else to exit
                        running = False

            # Draw background
            screen.blit(bg_image, (0, 0))

            # ✅ Draw profile icon
            screen.blit(self.profile_icon, self.profile_rect)
            if self.profile_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (255, 102, 0), self.profile_rect, 3, border_radius=10)

            # Optional text hint
            hint_font = dynamic_font(0.05, bold=True)
            hint_text = hint_font.render("BACK", True, (255, 255, 255))
            screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, SCREEN_HEIGHT - 100))

            pygame.display.flip()
            clock.tick(60)


    # ---------------- MAIN LOOP ----------------
    def run(self):
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            screen.fill((255, 255, 255))
            if self.show_welcome:
                if self.welcome_bg:
                    screen.blit(self.welcome_bg, self.welcome_bg_pos)
##                self.draw_arabic_text("مرحباً", 0.12, (51, 51, 51),
##                                       (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3), bold=True)

                # === Start Button ===
##                pygame.draw.rect(screen, (255, 255, 255), self.start_rect, border_radius=30)
##                pygame.draw.rect(screen, (255, 102, 0), self.start_rect, 5, border_radius=30)
##                self.draw_arabic_text("هيا نبدأ", 0.07, (255, 102, 0), self.start_rect.center, bold=True)

                # === Extra Buttons (resolution-based positions) ===
                for btn in self.extra_buttons:
                    x = int(SCREEN_WIDTH * btn["x_ratio"])
                    y = int(SCREEN_HEIGHT * btn["y_ratio"])
                    w = int(SCREEN_WIDTH * btn["w_ratio"])
                    h = int(SCREEN_HEIGHT * btn["h_ratio"])
                    
                    # ✅ Centered placement — draw from the middle of the button
                    rect = pygame.Rect(x - w // 2, y - h // 2, w, h)
                    pygame.draw.rect(screen, btn["color"], rect, border_radius=25)
                    pygame.draw.rect(screen, (255, 255, 255), rect, 4, border_radius=25)
                    self.draw_arabic_text(btn["label"], 0.05, (255, 255, 255), rect.center, bold=True)


            else:
                if self.section_bg: screen.blit(self.section_bg, self.section_bg_pos)
                for btn in self.section_buttons:
                    self.draw_arabic_text(btn["text"], 0.06, (51, 51, 51), btn["rect"].center)

            # Profile + Exit icons
            screen.blit(self.profile_icon, self.profile_rect)
            if self.profile_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255,102,0), self.profile_rect, 3, border_radius=10)

            screen.blit(self.exit_icon, self.exit_rect)
            if self.exit_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255,102,0), self.exit_rect, 3, border_radius=10)

            # EVENTS
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    if confirm_popup(screen, "Exit the game?"): pygame.quit(); sys.exit()
                elif e.type == pygame.USEREVENT + 1:
                    self.show_welcome = False
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    if confirm_popup(screen, "Exit the game?"): pygame.quit(); sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_rect.collidepoint(mouse_pos):
                        if confirm_popup(screen, "Exit the game?"): pygame.quit(); sys.exit()
                    elif self.profile_rect.collidepoint(mouse_pos):
                        self.open_profile_manager()
                    elif self.show_welcome and self.start_rect.collidepoint(mouse_pos):
                        self.start_with_delay()

                    # === Check for clicks on new buttons ===
                    elif self.show_welcome:
                        for btn in self.extra_buttons:
                            x = int(SCREEN_WIDTH * btn["x_ratio"])
                            y = int(SCREEN_HEIGHT * btn["y_ratio"])
                            w = int(SCREEN_WIDTH * btn["w_ratio"])
                            h = int(SCREEN_HEIGHT * btn["h_ratio"])
                            
                            # ✅ Must match the drawing rect exactly
                            rect = pygame.Rect(x - w // 2, y - h // 2, w, h)
                            
                            if rect.collidepoint(mouse_pos):
                                if btn["label"] == "Level Check":
                                    print("Level Check clicked!")
                                elif btn["label"] == "Learning":
                                    self.open_learning_screen()
                                elif btn["label"] == "Quizzes":
                                    print("Quizzes clicked!")


                    elif not self.show_welcome:
                        for btn in self.section_buttons:
                            if btn["rect"].collidepoint(mouse_pos): btn["action"]()
                elif e.type == pygame.MOUSEMOTION and not self.show_welcome:
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
