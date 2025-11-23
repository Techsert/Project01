import os
import sys
import pygame
import arabic_reshaper
from screen_helpers import confirm_popup, dynamic_font, load_font
from bidi.algorithm import get_display
from profile_screen import run_profile_screen, run_profile_manage_screen
from learning_topics import run_learning_topics
from quiz_topics import run_quiz_topics
from learn_lvl1_T1 import run_learn_lvl1_T1
from learn_lvl1_T2 import run_learn_lvl1_T2
from alphabit_sound import run_alphabit_sound
import config # NEW: Import your centralized config

# ===========================
# CONFIG
# ===========================
pygame.init()
pygame.mixer.init()

info = pygame.display.Info()
config.SCREEN_WIDTH, config.SCREEN_HEIGHT = info.current_w, info.current_h # NEW: Update config
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.FULLSCREEN) # Use config
pygame.display.set_caption("Welcome to Learning World - Level One")
clock = pygame.time.Clock()


# ===========================
# HELPERS
# ===========================
##def load_font(size, bold=False):
##    try:
##        path = ARABIC_BOLD_FONT_PATH if bold else ARABIC_FONT_PATH
##        return pygame.font.Font(path, size)
##    except:
##        return pygame.font.SysFont("Arial", size)


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
        # --- FIX STARTS HERE ---
        # Use config.SCREEN_WIDTH and config.SCREEN_HEIGHT
        x = (config.SCREEN_WIDTH - new_size[0]) // 2
        y = (config.SCREEN_HEIGHT - new_size[1]) // 2
        # --- FIX ENDS HERE ---
        return img, (x, y)
    except Exception as e:
        print(f"Error loading background at {path}: {e}") # Added path to error for better debugging
        return None, (0, 0)


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
        self.start_sound_path = os.path.join(config.SOUND_MAIN_PATH, "lets_start.mp3")
        self.hover_channel = pygame.mixer.Channel(config.HOVER_CHANNEL_ID) # Use config for channel ID
        self.start_sound_path = os.path.join(config.SOUND_MAIN_PATH, "lets_start.mp3") # Use config

        # === Music ===
        self.bg_music = os.path.join(config.SOUND_MAIN_PATH, "bg_sound.mp3") # Use config
        self.play_bg_music()

        # === Backgrounds ===
        self.welcome_bg, self.welcome_bg_pos = load_scaled_background(
            os.path.join(config.IMG_MAIN_PATH, "background.png"), config.SCREEN_WIDTH, config.SCREEN_HEIGHT, keep_aspect=False # Use config
        )

        # === Profile Icon ===
        avatar_name = selected_profile.get("avatar") if selected_profile else None
        avatar_path = os.path.join(config.AVATAR_PROFILES_PATH, avatar_name) if avatar_name else os.path.join(config.IMG_MAIN_PATH, "profile_icon.png") # Use config
        self.profile_icon = load_image(avatar_path, config.SCREEN_WIDTH * 0.04, config.SCREEN_WIDTH * 0.04) # Use config
        self.profile_rect = self.profile_icon.get_rect(topright=(config.SCREEN_WIDTH - 30, 30)) # Use config

        # === Exit Icon ===
        exit_icon_path = os.path.join(config.IMG_MAIN_PATH, "exit_icon.png") # Use config
        self.exit_icon = load_image(exit_icon_path, config.SCREEN_WIDTH * 0.05, config.SCREEN_HEIGHT * 0.09) # Use config
        self.exit_rect = self.exit_icon.get_rect(bottomright=(config.SCREEN_WIDTH - 20, config.SCREEN_HEIGHT - 20)) # Use config

        # State used by hover sound in section screen
        self._last_hovered_btn_id = None

    # ---------------- TEXT ----------------
    def draw_arabic_text(self, text, size_ratio, color, center, bold=False):
        reshaped = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped)

        # ✅ pass the required arguments from your main app
        font = dynamic_font(
            config.SCREEN_HEIGHT,          # Use config.SCREEN_HEIGHT
            config.ARABIC_FONT_REGULAR,    # Use config.ARABIC_FONT_REGULAR
            config.ARABIC_FONT_BOLD,       # Use config.ARABIC_FONT_BOLD
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
            pygame.mixer.music.set_volume(config.BG_MUSIC_VOLUME) # Use config)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Music error:", e)

    # ---------------- PROFILE ----------------
    def open_profile_manager(self):
        pygame.mixer.music.stop()
        updated = run_profile_manage_screen(screen, config.SCREEN_WIDTH, config.SCREEN_HEIGHT, self.selected_profile)
        if updated:
            if updated.get("_deleted"):
                self.selected_profile = run_profile_screen(screen, config.SCREEN_WIDTH, SCREEN_HEIGHT)
            else:
                self.selected_profile.update(updated)
            avatar_path = os.path.join(config.AVATAR_PROFILES_PATH, self.selected_profile["avatar"]) # Use config
            self.profile_icon = load_image(avatar_path, config.SCREEN_WIDTH * 0.04, config.SCREEN_WIDTH * 0.04) # Use config
            self.profile_rect = self.profile_icon.get_rect(topright=(config.SCREEN_WIDTH - 30, 30)) # Use config
        self.play_bg_music()

    # ---------------- confirm Exit ----------------
    def confirm_popup(self, msg):
        """Shortcut wrapper for global confirm_popup with app's font loader."""
        # Pass screen_helpers.load_font explicitly
        return confirm_popup(self.screen, msg, lambda size, bold=False: load_font(config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, size, bold)) # Use config

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

    def launch_alphabit_name(self):
        pygame.mixer.stop()
        # Placeholder: You'll need to create an `alphabit_name.py` and import `run_alphabit_name`
        # from alphabit_name import run_alphabit_name
        # run_alphabit_name(self.screen, main_app=self)
        print("Action: Launch Alphabit Names Screen (Implement alphabit_name.py)")


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
            x = int(config.SCREEN_WIDTH * b["x_ratio"]) # Use config
            y = int(config.SCREEN_HEIGHT * b["y_ratio"]) # Use config
            w = int(config.SCREEN_WIDTH  * b["w_ratio"]) # Use config
            h = int(config.SCREEN_HEIGHT * b["h_ratio"]) # Use config
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
        soccer_path = os.path.join(config.IMG_MAIN_PATH, "soccerfield.png")
        bg_image = None # Initialize to None
        try:
            bg_image = pygame.image.load(soccer_path).convert()
            bg_image = pygame.transform.smoothscale(bg_image, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        except Exception as e:
            print(f"Error loading soccerfield.png: {e}")
            return

        # Prepare LVL buttons
        lvl_buttons = []
        for i in range(1, 10):
            img_path = os.path.join(config.IMG_MAIN_PATH, f"LVL {i}.png") # Use config.IMG_MAIN_PATH
            try:
                img = pygame.image.load(img_path).convert_alpha()
            except Exception as e:
                print(f"⚠️ Missing image for LVL {i}: {e}")
                img = pygame.Surface((100, 100), pygame.SRCALPHA)
                pygame.draw.rect(img, (200, 0, 0), img.get_rect(), 4)
            lvl_buttons.append({"image": img, "label": f"LVL {i}", "rect": None})


        # Initialize title font and text here, always, if the screen is meant to be displayed
        title_font = dynamic_font(config.SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, size_ratio=0.04, bold=True)
        title_text = title_font.render("Learning Levels", True, (255, 255, 255)) # Assignment here

        # ... rest of the code ...
        # Inside the while running loop:
        # Draw
        if bg_image: # Only blit if the background image loaded successfully
            screen.blit(bg_image, (0, 0))
        else: # Fallback if image failed to load
            screen.fill((50, 50, 50)) # Or some other neutral color
            # Optionally, draw an error message if background failed
            error_font = dynamic_font(config.SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, size_ratio=0.03, bold=True)
            error_msg = error_font.render("Background failed to load!", True, (255, 0, 0))
            screen.blit(error_msg, error_msg.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)))

        # Title (this should now always be defined)
        screen.blit(title_text, title_text.get_rect(center=(config.SCREEN_WIDTH // 2, int(config.SCREEN_HEIGHT * 0.04))))        

        scatter_positions = [
            (0.10, 0.40), (0.19, 0.85), (0.29, 0.15),
            (0.39, 0.67), (0.49, 0.50), (0.59, 0.67),
            (0.69, 0.15), (0.79, 0.38), (0.89, 0.50),
        ]
        IMG_W_RATIO, IMG_H_RATIO = 0.055, 0.09

        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
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
                        bg_image = pygame.image.load(soccer_path).convert()
                        bg_image = pygame.transform.smoothscale(bg_image, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
                    else:
                        for b in lvl_buttons:
                            if b["rect"] and b["rect"].collidepoint(e.pos):
                                print(f"Clicked {b['label']}!")  # keep existing behavior
                                if b["label"] == "LVL 1":
                                    run_learning_topics(screen, self, level=1)
                                elif b["label"] == "LVL 2":
                                    run_learning_topics(screen, self, level=2)


            # Draw
            screen.blit(bg_image, (0, 0))

            # Title
            title_font = dynamic_font(config.SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, size_ratio=0.04, bold=True)
            title_text = title_font.render("Learning Levels", True, (255, 255, 255))
            screen.blit(title_text, title_text.get_rect(center=(config.SCREEN_WIDTH // 2, int(config.SCREEN_HEIGHT * 0.04))))

            # Profile icon
            screen.blit(self.profile_icon, self.profile_rect)
            if self.profile_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 102, 0), self.profile_rect, 3, border_radius=10)

            # LVL buttons + labels
            img_w, img_h = int(config.SCREEN_WIDTH * IMG_W_RATIO), int(config.SCREEN_HEIGHT * IMG_H_RATIO)
            font = dynamic_font(config.SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, size_ratio=0.02, bold=True)
            for (x_ratio, y_ratio), btn in zip(scatter_positions, lvl_buttons):
                x = int(config.SCREEN_WIDTH * x_ratio)
                y = int(config.SCREEN_HEIGHT * y_ratio)
                scaled_img = pygame.transform.smoothscale(btn["image"], (img_w, img_h))
                rect = scaled_img.get_rect(center=(x, y))
                btn["rect"] = rect
                screen.blit(scaled_img, rect)
                label = font.render(btn["label"], True, (255, 51, 51))
                screen.blit(label, label.get_rect(center=(x, y + img_h // 2 + 30)))

            # BACK button (hint)
            hint_font = dynamic_font(config.SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, size_ratio=0.03, bold=True)
            hint_text = hint_font.render("BACK", True, (255, 255, 255))
            hint_rect = hint_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 50))
            screen.blit(hint_text, hint_rect)
            if hint_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 102, 0), hint_rect.inflate(20, 10), 2, border_radius=8)

            pygame.display.flip()
            clock.tick(60)


    # ============================== Quizzes Screen ====================================
    def open_quiz_screen(self):
        """Quiz screen: soccer field layout reused with 'Quizzes' title."""
        soccer_path = os.path.join(config.IMG_MAIN_PATH, "soccerfield.png")
        bg_image = None # Initialize to None
        try:
            bg_image = pygame.image.load(soccer_path).convert()
            bg_image = pygame.transform.smoothscale(bg_image, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        except Exception as e:
            print(f"Error loading soccerfield.png: {e}")
            return

        # Prepare LVL buttons
        lvl_buttons = []
        for i in range(1, 10):
            img_path = os.path.join(config.IMG_MAIN_PATH, f"LVL {i}.png") # Use config.IMG_MAIN_PATH
            try:
                img = pygame.image.load(img_path).convert_alpha()
            except Exception as e:
                print(f"⚠️ Missing image for LVL {i}: {e}")
                img = pygame.Surface((100, 100), pygame.SRCALPHA)
                pygame.draw.rect(img, (200, 0, 0), img.get_rect(), 4)
            lvl_buttons.append({"image": img, "label": f"LVL {i}", "rect": None})


        # Initialize title font and text here, always, if the screen is meant to be displayed
        title_font = dynamic_font(config.SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, size_ratio=0.04, bold=True)
        title_text = title_font.render("Learning Levels", True, (255, 255, 255)) # Assignment here

        # ... rest of the code ...
        # Inside the while running loop:
        # Draw
        if bg_image: # Only blit if the background image loaded successfully
            screen.blit(bg_image, (0, 0))
        else: # Fallback if image failed to load
            screen.fill((50, 50, 50)) # Or some other neutral color
            # Optionally, draw an error message if background failed
            error_font = dynamic_font(config.SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, size_ratio=0.03, bold=True)
            error_msg = error_font.render("Background failed to load!", True, (255, 0, 0))
            screen.blit(error_msg, error_msg.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)))

        # Title (this should now always be defined)
        screen.blit(title_text, title_text.get_rect(center=(config.SCREEN_WIDTH // 2, int(config.SCREEN_HEIGHT * 0.04))))

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
                        bg_image = pygame.transform.smoothscale(bg_image, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
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
            title_font = dynamic_font(config.SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, size_ratio=0.04, bold=True)
##            title_font = dynamic_font(SCREEN_HEIGHT, self.ARABIC_FONT_PATH, self.ARABIC_BOLD_FONT_PATH, 0.04, bold=True)
            title_text = title_font.render("Quizzes", True, (255, 255, 255))
            screen.blit(title_text, title_text.get_rect(center=(config.SCREEN_WIDTH // 2, int(config.SCREEN_HEIGHT * 0.04))))

            # Profile icon
            screen.blit(self.profile_icon, self.profile_rect)
            if self.profile_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 102, 0), self.profile_rect, 3, border_radius=10)

            # LVL buttons + labels
            img_w, img_h = int(config.SCREEN_WIDTH * IMG_W_RATIO), int(config.SCREEN_HEIGHT * IMG_H_RATIO)
            font = dynamic_font(config.SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, size_ratio=0.02, bold=True)
            for (x_ratio, y_ratio), btn in zip(scatter_positions, lvl_buttons):
                x = int(config.SCREEN_WIDTH * x_ratio)
                y = int(config.SCREEN_HEIGHT * y_ratio)
                scaled_img = pygame.transform.smoothscale(btn["image"], (img_w, img_h))
                rect = scaled_img.get_rect(center=(x, y))
                btn["rect"] = rect
                screen.blit(scaled_img, rect)
                label = font.render(btn["label"], True, (255, 51, 51))
                screen.blit(label, label.get_rect(center=(x, y + img_h // 2 + 30)))

            # BACK button (hint)
            hint_font = dynamic_font(config.SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, size_ratio=0.03, bold=True) 
            hint_text = hint_font.render("BACK", True, (255, 255, 255))
            hint_rect = hint_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 50))
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
    selected_profile = run_profile_screen(screen, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
    app = QuizApp(selected_profile)
    app.run()
