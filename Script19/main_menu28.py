import os
import sys
import pygame
import arabic_reshaper
from screen_helpers import confirm_popup, dynamic_font
from bidi.algorithm import get_display
from profile_screen import run_profile_screen, run_profile_manage_screen
from learning_topics import run_learning_topics
from quiz_topics import run_quiz_topics
from learn_lvl1_T1 import run_learn_lvl1_T1
from learn_lvl1_T2 import run_learn_lvl1_T2
from alphabit_sound import run_alphabit_sound

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
# HELPERS
# ===========================
def load_font(size, bold=False):
    try:
        path = ARABIC_BOLD_FONT_PATH if bold else ARABIC_FONT_PATH
        return pygame.font.Font(path, size)
    except:
        return pygame.font.SysFont("Arial", size)

##def dynamic_font(size_ratio=0.05, bold=False):
##    return load_font(int(SCREEN_HEIGHT * size_ratio), bold=bold)

def load_image(filename, width=None, height=None):
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
    try:
        img = pygame.image.load(path).convert_alpha()
        img_w, img_h = img.get_size()
        if keep_aspect:
            scale_factor = min(target_width / img_w, target_height / img_h)
            new_size = (int(img_w * scale_factor), int(img_h * scale_factor))
        else:
            new_size = (int(target_width), int(target_height))
        img = pygame.transform.smoothscale(img, new_size)
        x = (SCREEN_WIDTH - new_size[0]) // 2
        y = (SCREEN_HEIGHT - new_size[1]) // 2
        return img, (x, y)
    except Exception as e:
        print(f"Error loading background: {e}")
        return None, (0, 0)

##def confirm_popup(screen, msg):
##    """Modal Yes/No confirmation dialog."""
##    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
##    overlay.set_alpha(180)
##    overlay.fill((0, 0, 0))
##    screen.blit(overlay, (0, 0))
##
##    box_width = int(SCREEN_WIDTH * 0.3)
##    box_height = int(SCREEN_HEIGHT * 0.25)
##    box = pygame.Rect(0, 0, box_width, box_height)
##    box.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
##
##    pygame.draw.rect(screen, (255, 255, 255), box, border_radius=20)
##    pygame.draw.rect(screen, (255, 102, 0), box, 4, border_radius=20)
##
##    title_font = load_font(int(SCREEN_HEIGHT * 0.04), bold=True)
##    button_font = load_font(int(SCREEN_HEIGHT * 0.03))
##
##    text = title_font.render(msg, True, (0, 0, 0))
##    screen.blit(text, (box.centerx - text.get_width() // 2, box.top + 25))
##
##    btn_w, btn_h = int(box_width * 0.3), int(box_height * 0.35)
##    yes = pygame.Rect(box.centerx - btn_w - 20, box.bottom - btn_h - 20, btn_w, btn_h)
##    no = pygame.Rect(box.centerx + 20, box.bottom - btn_h - 20, btn_w, btn_h)
##
##    pygame.draw.rect(screen, (0, 170, 0), yes, border_radius=10)
##    pygame.draw.rect(screen, (170, 0, 0), no, border_radius=10)
##
##    yes_text = button_font.render("Yes", True, (255, 255, 255))
##    no_text = button_font.render("No", True, (255, 255, 255))
##    screen.blit(yes_text, yes_text.get_rect(center=yes.center))
##    screen.blit(no_text, no_text.get_rect(center=no.center))
##
##    pygame.display.flip()
##
##    while True:
##        for e in pygame.event.get():
##            if e.type == pygame.QUIT:
##                pygame.quit(); sys.exit()
##            if e.type == pygame.MOUSEBUTTONDOWN:
##                if yes.collidepoint(e.pos): return True
##                elif no.collidepoint(e.pos): return False
##        pygame.time.wait(10)


# ===========================
# MAIN CLASS
# ===========================
class QuizApp:
    def __init__(self, selected_profile):
        """Initialize persistent assets (music, backgrounds, icons)."""
        self.screen = screen
        self.selected_profile = selected_profile
        self.running = True
        self.hover_channel = pygame.mixer.Channel(5)
        self.start_sound_path = os.path.join(SOUND_PATH, "lets_start.mp3")
        self.screen_height = SCREEN_HEIGHT
        self.screen_width = SCREEN_WIDTH
        self.ARABIC_FONT_PATH = ARABIC_FONT_PATH
        self.ARABIC_BOLD_FONT_PATH = ARABIC_BOLD_FONT_PATH
        self.IMG_PATH = IMG_PATH
        self.SOUND_PATH = SOUND_PATH




        # === Music ===
        self.bg_music = os.path.join(SOUND_PATH, "bg_sound.mp3")
        self.play_bg_music()

        # === Backgrounds ===
        self.welcome_bg, self.welcome_bg_pos = load_scaled_background(
            os.path.join(IMG_PATH, "background.png"), SCREEN_WIDTH, SCREEN_HEIGHT, keep_aspect=False
        )
##        self.section_bg, self.section_bg_pos = load_scaled_background(
##            os.path.join(IMG_PATH, "section_bg.png"), SCREEN_WIDTH * 0.9, SCREEN_HEIGHT * 0.95, keep_aspect=False
##        )

        # === Profile Icon ===
        avatar_name = selected_profile.get("avatar") if selected_profile else None
        avatar_path = os.path.join(AVATAR_PATH, avatar_name) if avatar_name else os.path.join(IMG_PATH, "profile_icon.png")
        self.profile_icon = load_image(avatar_path, SCREEN_WIDTH * 0.04, SCREEN_WIDTH * 0.04)
        self.profile_rect = self.profile_icon.get_rect(topright=(SCREEN_WIDTH - 30, 30))

        # === Exit Icon ===
        exit_icon_path = os.path.join(IMG_PATH, "exit_icon.png")
        self.exit_icon = load_image(exit_icon_path, SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.09)
        self.exit_rect = self.exit_icon.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))

        # State used by hover sound in section screen
        self._last_hovered_btn_id = None

    # ---------------- TEXT ----------------
    def draw_arabic_text(self, text, size_ratio, color, center, bold=False):
        reshaped = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped)

        # ✅ pass the required arguments from your main app
        font = dynamic_font(
            SCREEN_HEIGHT,                 # screen height for scaling
            ARABIC_FONT_PATH,              # regular font path
            ARABIC_BOLD_FONT_PATH,         # bold font path
            size_ratio=size_ratio,
            bold=bold
        )

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

    # ---------------- PROFILE ----------------
    def open_profile_manager(self):
        pygame.mixer.music.stop()
        updated = run_profile_manage_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, self.selected_profile)
        if updated:
            if updated.get("_deleted"):
                self.selected_profile = run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
            else:
                self.selected_profile.update(updated)
            avatar_path = os.path.join(AVATAR_PATH, self.selected_profile["avatar"])
            self.profile_icon = load_image(avatar_path, SCREEN_WIDTH * 0.04, SCREEN_WIDTH * 0.04)
            self.profile_rect = self.profile_icon.get_rect(topright=(SCREEN_WIDTH - 30, 30))
        self.play_bg_music()

    # ---------------- confirm Exit ----------------
    def confirm_popup(self, msg):
        """Shortcut wrapper for global confirm_popup with app's font loader."""
        return confirm_popup(self.screen, msg, load_font)

    # ---------------- launch LVL One topics ------------
    def launch_learn_lvl1_T1(self):
        pygame.mixer.stop()
        run_learn_lvl1_T1(self.screen, self)
        
    def launch_learn_lvl1_T2(self):
        pygame.mixer.stop()
        run_learn_lvl1_T2(self.screen, self)

    def launch_alphabit_sound(self):
        pygame.mixer.stop()
        run_alphabit_sound(self.screen, main_app=self)


    # ================= SCREENS =================
    def open_welcome_screen(self):
        """Main Welcome Menu (defines its own buttons)."""
        # --- Define Welcome buttons locally (self-contained) ---
        extra_buttons = [
            {"label": "Level Check", "color": (0, 204, 0), "x_ratio": 0.29, "y_ratio": 0.25, "w_ratio": 0.15, "h_ratio": 0.10},
            {"label": "Learning",    "color": (255, 204, 0), "x_ratio": 0.39, "y_ratio": 0.45, "w_ratio": 0.15, "h_ratio": 0.10},
            {"label": "Quizzes",     "color": (255,  51, 51), "x_ratio": 0.49, "y_ratio": 0.65, "w_ratio": 0.15, "h_ratio": 0.10},
        ]
        # Precompute rects once
        for b in extra_buttons:
            x = int(SCREEN_WIDTH * b["x_ratio"])
            y = int(SCREEN_HEIGHT * b["y_ratio"])
            w = int(SCREEN_WIDTH  * b["w_ratio"])
            h = int(SCREEN_HEIGHT * b["h_ratio"])
            b["rect"] = pygame.Rect(x - w // 2, y - h // 2, w, h)

        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            # 🧼 Clear old frame
            screen.fill((255, 255, 255))

            screen.blit(self.welcome_bg, self.welcome_bg_pos)

            # Draw buttons
            for b in extra_buttons:
                pygame.draw.rect(screen, b["color"], b["rect"], border_radius=25)
                pygame.draw.rect(screen, (255, 255, 255), b["rect"], 4, border_radius=25)
                self.draw_arabic_text(b["label"], 0.05, (255, 255, 255), b["rect"].center, bold=True)

            # Profile + Exit
            screen.blit(self.profile_icon, self.profile_rect)
            if self.profile_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 102, 0), self.profile_rect, 3, border_radius=10)

            screen.blit(self.exit_icon, self.exit_rect)
            if self.exit_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 102, 0), self.exit_rect, 3, border_radius=10)

            # Events
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    if self.confirm_popup("Exit the game?"): pygame.quit(); sys.exit()
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    if self.confirm_popup("Exit the game?"): pygame.quit(); sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_rect.collidepoint(mouse_pos):
                        if self.confirm_popup("Exit the game?"): pygame.quit(); sys.exit()
                    elif self.profile_rect.collidepoint(mouse_pos):
                        self.open_profile_manager()
                    else:
                        for b in extra_buttons:
                            if b["rect"].collidepoint(mouse_pos):
                                if b["label"] == "Level Check":
                                    print("Level Check clicked!")
                                elif b["label"] == "Learning":
                                    self.open_learning_screen()
                                elif b["label"] == "Quizzes":
                                    self.open_quiz_screen()

            pygame.display.flip()
            clock.tick(60)

    # ==================================== Learning Screen ====================================

    def open_learning_screen(self):
        """Learning screen: soccer field with scattered LVL 1–9 buttons."""
        soccer_path = os.path.join(IMG_PATH, "soccerfield.png")
        try:
            bg_image = pygame.image.load(soccer_path).convert()
            bg_image = pygame.transform.smoothscale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Error loading soccerfield.png: {e}")
            return

        # Prepare LVL buttons
        lvl_buttons = []
        for i in range(1, 10):
            img_path = os.path.join(IMG_PATH, f"LVL {i}.png")
            try:
                img = pygame.image.load(img_path).convert_alpha()
            except Exception as e:
                print(f"⚠️ Missing image for LVL {i}: {e}")
                img = pygame.Surface((100, 100), pygame.SRCALPHA)
                pygame.draw.rect(img, (200, 0, 0), img.get_rect(), 4)
            lvl_buttons.append({"image": img, "label": f"LVL {i}", "rect": None})

        scatter_positions = [
            (0.10, 0.40), (0.19, 0.85), (0.29, 0.15),
            (0.39, 0.67), (0.49, 0.50), (0.59, 0.67),
            (0.69, 0.15), (0.79, 0.38), (0.89, 0.50),
        ]
        IMG_W_RATIO, IMG_H_RATIO = 0.055, 0.09

        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            # 🧼 Clear old frame
            screen.fill((255, 255, 255))

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    # BACK
                    if hint_rect.collidepoint(e.pos):
                        running = False
                        continue
                    # Profile
                    if self.profile_rect.collidepoint(e.pos):
                        self.open_profile_manager()
                        # reload bg in case display changed (keeps your original behavior)
                        bg_image = pygame.image.load(soccer_path).convert()
                        bg_image = pygame.transform.smoothscale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    else:
                        for b in lvl_buttons:
                            if b["rect"] and b["rect"].collidepoint(e.pos):
                                print(f"Clicked {b['label']}!")  # keep existing behavior
                                if b["label"] == "LVL 1":
                                    run_learning_topics(screen, self, level=1)
                                elif b["label"] == "LVL 2":
                                    run_learning_topics(screen, self, level=2)
##                                # Per your new hierarchy, open the section screen after choosing a level
##                                self.open_section_screen()
##                                break

            # Draw
            screen.blit(bg_image, (0, 0))

            # Title
            title_font = dynamic_font(SCREEN_HEIGHT, ARABIC_FONT_PATH, ARABIC_BOLD_FONT_PATH, size_ratio=0.04, bold=True)
            title_text = title_font.render("Learning Levels", True, (255, 255, 255))
            screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.04))))

            # Profile icon
            screen.blit(self.profile_icon, self.profile_rect)
            if self.profile_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 102, 0), self.profile_rect, 3, border_radius=10)

            # LVL buttons + labels
            img_w, img_h = int(SCREEN_WIDTH * IMG_W_RATIO), int(SCREEN_HEIGHT * IMG_H_RATIO)
            font = dynamic_font(SCREEN_HEIGHT, ARABIC_FONT_PATH, ARABIC_BOLD_FONT_PATH, size_ratio=0.02, bold=True)
            for (x_ratio, y_ratio), btn in zip(scatter_positions, lvl_buttons):
                x = int(SCREEN_WIDTH * x_ratio)
                y = int(SCREEN_HEIGHT * y_ratio)
                scaled_img = pygame.transform.smoothscale(btn["image"], (img_w, img_h))
                rect = scaled_img.get_rect(center=(x, y))
                btn["rect"] = rect
                screen.blit(scaled_img, rect)
                label = font.render(btn["label"], True, (255, 51, 51))
                screen.blit(label, label.get_rect(center=(x, y + img_h // 2 + 30)))

            # BACK button (hint)
            hint_font = dynamic_font(SCREEN_HEIGHT, ARABIC_FONT_PATH, ARABIC_BOLD_FONT_PATH, size_ratio=0.03, bold=True)
            hint_text = hint_font.render("BACK", True, (255, 255, 255))
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(hint_text, hint_rect)
            if hint_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 102, 0), hint_rect.inflate(20, 10), 2, border_radius=8)

            pygame.display.flip()
            clock.tick(60)

    # ============================== LVL One Learning Screen ===============================
##    def open_section_screen(self):
##        """Arabic categories screen (defines its own buttons + hover sounds)."""
##        # Build buttons relative to section_bg
##        bg_x, bg_y = self.section_bg_pos
##        bg_w, bg_h = self.section_bg.get_size()
##        btn_w, btn_h = int(bg_w * 0.25), int(bg_h * 0.10)
##
##        items = [
##            {"text": "أسماء الحُروف", "action": self.launch_alphabit_name,  "hover": os.path.join(SOUND_PATH, "hover_alphabetNames.wav"),   "pos": (0.15, 0.36)},
##            {"text": "أصوات الحُروف", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_alphabetSounds.wav"), "pos": (0.50, 0.36)},
##            {"text": "أشكال الحُروف", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_alphabetShaps.wav"),  "pos": (0.85, 0.36)},
##            {"text": "الأعداد",        "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_numbers.wav"),        "pos": (0.15, 0.89)},
##            {"text": "الألوان",        "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_colours.wav"),        "pos": (0.50, 0.89)},
##            {"text": "الكَلِمات",      "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_words.wav"),          "pos": (0.85, 0.89)},
##        ]
##        # Compute rects
##        for it in items:
##            rx, ry = it["pos"]
##            x = bg_x + int(rx * bg_w)
##            y = bg_y + int(ry * bg_h)
##            it["rect"] = pygame.Rect(x - btn_w // 2, y - btn_h // 2, btn_w, btn_h)
##
##        running = True
##        self._last_hovered_btn_id = None  # reset hover state
##        while running:
##            mouse_pos = pygame.mouse.get_pos()
##            # 🧼 Clear old frame
##            screen.fill((255, 255, 255))
##            
##            screen.blit(self.section_bg, self.section_bg_pos)
##
##            # Draw buttons (text only per your original)
##            for it in items:
##                self.draw_arabic_text(it["text"], 0.06, (51, 51, 51), it["rect"].center)
##
##            # Profile + Exit
##            screen.blit(self.profile_icon, self.profile_rect)
##            if self.profile_rect.collidepoint(mouse_pos):
##                pygame.draw.rect(screen, (255, 102, 0), self.profile_rect, 3, border_radius=10)
##
##            screen.blit(self.exit_icon, self.exit_rect)
##            if self.exit_rect.collidepoint(mouse_pos):
##                pygame.draw.rect(screen, (255, 102, 0), self.exit_rect, 3, border_radius=10)
##
##            # Hover sound (only when entering a new button)
##            hovered_id = None
##            for idx, it in enumerate(items):
##                if it["rect"].collidepoint(mouse_pos):
##                    hovered_id = idx
##                    break
##            if hovered_id is not None and hovered_id != self._last_hovered_btn_id:
##                self.play_hover_sound(items[hovered_id]["hover"])
##            self._last_hovered_btn_id = hovered_id
##
##            # Events
##            for e in pygame.event.get():
##                if e.type == pygame.QUIT:
##                    if confirm_popup(screen, "Exit the game?"): pygame.quit(); sys.exit()
##                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
##                    running = False
##                elif e.type == pygame.MOUSEBUTTONDOWN:
##                    if self.exit_rect.collidepoint(mouse_pos):
##                        if confirm_popup(screen, "Exit the game?"): pygame.quit(); sys.exit()
##                    elif self.profile_rect.collidepoint(mouse_pos):
##                        self.open_profile_manager()
##                    else:
##                        for it in items:
##                            if it["rect"].collidepoint(mouse_pos):
##                                it["action"]()
##
##            pygame.display.flip()
##            clock.tick(60)

    # ============================== Quizzes Screen ====================================
    def open_quiz_screen(self):
        """Quiz screen: soccer field layout reused with 'Quizzes' title."""
        soccer_path = os.path.join(IMG_PATH, "soccerfield.png")
        try:
            bg_image = pygame.image.load(soccer_path).convert()
            bg_image = pygame.transform.smoothscale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Error loading soccerfield.png: {e}")
            return

        # Prepare LVL buttons
        lvl_buttons = []
        for i in range(1, 10):
            img_path = os.path.join(IMG_PATH, f"LVL {i}.png")
            try:
                img = pygame.image.load(img_path).convert_alpha()
            except Exception as e:
                print(f"⚠️ Missing image for LVL {i}: {e}")
                img = pygame.Surface((100, 100), pygame.SRCALPHA)
                pygame.draw.rect(img, (200, 0, 0), img.get_rect(), 4)
            lvl_buttons.append({"image": img, "label": f"LVL {i}", "rect": None})

        scatter_positions = [
            (0.10, 0.40), (0.19, 0.85), (0.29, 0.15),
            (0.39, 0.67), (0.49, 0.50), (0.59, 0.67),
            (0.69, 0.15), (0.79, 0.38), (0.89, 0.50),
        ]
        IMG_W_RATIO, IMG_H_RATIO = 0.055, 0.09

        running = True
        while running:
            # 🧼 Clear old frame
            screen.fill((255, 255, 255))
            mouse_pos = pygame.mouse.get_pos()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    # BACK
                    if hint_rect.collidepoint(e.pos):
                        running = False
                        continue
                    # Profile
                    if self.profile_rect.collidepoint(e.pos):
                        self.open_profile_manager()
                        bg_image = pygame.image.load(soccer_path).convert()
                        bg_image = pygame.transform.smoothscale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    else:
                        for b in lvl_buttons:
                            if b["rect"] and b["rect"].collidepoint(e.pos):
                                print(f"Clicked {b['label']}!")  # placeholder for next action
                                if b["label"] == "LVL 1":
                                    run_quiz_topics(screen, self, level=1)
                                elif b["label"] == "LVL 2":
                                    run_quiz_topics(screen, self, level=2)
                                

            # Draw
            screen.blit(bg_image, (0, 0))

            # Title
            title_font = title_font = dynamic_font(SCREEN_HEIGHT, self.ARABIC_FONT_PATH, self.ARABIC_BOLD_FONT_PATH, 0.04, bold=True)
            title_text = title_font.render("Quizzes", True, (255, 255, 255))
            screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.04))))

            # Profile icon
            screen.blit(self.profile_icon, self.profile_rect)
            if self.profile_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 102, 0), self.profile_rect, 3, border_radius=10)

            # LVL buttons + labels
            img_w, img_h = int(SCREEN_WIDTH * IMG_W_RATIO), int(SCREEN_HEIGHT * IMG_H_RATIO)
            font = title_font = dynamic_font(SCREEN_HEIGHT, self.ARABIC_FONT_PATH, self.ARABIC_BOLD_FONT_PATH, 0.02, bold=True)
            for (x_ratio, y_ratio), btn in zip(scatter_positions, lvl_buttons):
                x = int(SCREEN_WIDTH * x_ratio)
                y = int(SCREEN_HEIGHT * y_ratio)
                scaled_img = pygame.transform.smoothscale(btn["image"], (img_w, img_h))
                rect = scaled_img.get_rect(center=(x, y))
                btn["rect"] = rect
                screen.blit(scaled_img, rect)
                label = font.render(btn["label"], True, (255, 51, 51))
                screen.blit(label, label.get_rect(center=(x, y + img_h // 2 + 30)))

            # BACK button (hint)
            hint_font = title_font = dynamic_font(SCREEN_HEIGHT, self.ARABIC_FONT_PATH, self.ARABIC_BOLD_FONT_PATH, 0.03, bold=True)
            hint_text = hint_font.render("BACK", True, (255, 255, 255))
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(hint_text, hint_rect)
            if hint_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 102, 0), hint_rect.inflate(20, 10), 2, border_radius=8)

            pygame.display.flip()
            clock.tick(60)

    # ---------------- MAIN LOOP ----------------
    def run(self):
        self.open_welcome_screen()


# ===========================
# ENTRY POINT
# ===========================
if __name__ == "__main__":
    selected_profile = run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    app = QuizApp(selected_profile)
    app.run()
