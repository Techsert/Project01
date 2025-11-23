import os
import sys
import pygame
import arabic_reshaper
import config
from screen_helpers import confirm_popup, dynamic_font, load_font
from bidi.algorithm import get_display
from profile_screen import run_profile_screen, run_profile_manage_screen
from learning_topics import run_learning_topics
from learn_lvl1_T1 import run_learn_lvl1_T1
from learn_lvl1_T2 import run_learn_lvl1_T2
from learn_lvl1_T3 import run_learn_lvl1_T3
from learn_lvl2_T1 import run_learn_lvl2_T1
from learn_lvl2_T2 import run_learn_lvl2_T2
from learn_lvl2_T3 import run_learn_lvl2_T3
from quiz_topics import run_quiz_topics
from quiz_lvl1_3 import run_AlphabitQuiz
from quiz_lvl14_test import run_LVL4
##from alphabit_sound import run_alphabit_sound


# ==========================================================
# PYGAME INITIALIZATION
# ==========================================================
pygame.init()
pygame.mixer.init()

# ✅ FIX: Get screen dimensions properly
SCREEN_WIDTH, SCREEN_HEIGHT = config.get_screen_dimensions()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Welcome to Learning World - Level One")
clock = pygame.time.Clock()

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================
def load_image(filename, width=None, height=None):
    """Load image with error handling."""
    try:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Image not found: {filename}")
        
        img = pygame.image.load(filename).convert_alpha()
        if width and height:
            img = pygame.transform.smoothscale(img, (int(width), int(height)))
        return img
    except Exception as e:
        print(f"❌ Image load error: {e}")
        # Return placeholder
        placeholder = pygame.Surface((width or 100, height or 100))
        placeholder.fill((200, 0, 0))
        return placeholder

def load_sound(filename):
    """Load sound with error handling."""
    try:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Sound not found: {filename}")
        return pygame.mixer.Sound(filename)
    except Exception as e:
        print(f"❌ Sound load error: {e}")
        return None

def load_scaled_background(path, target_width, target_height, keep_aspect=True):
    """Load and scale background image."""
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Background not found: {path}")
        
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
        print(f"❌ Error loading background at {path}: {e}")
        # Return placeholder
        placeholder = pygame.Surface((target_width, target_height))
        placeholder.fill((50, 50, 50))
        return placeholder, (0, 0)

# ==========================================================
# MAIN APPLICATION CLASS
# ==========================================================
class QuizApp:
    def __init__(self, selected_profile):
        """Initialize persistent assets and managers."""
        self.screen = screen
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.selected_profile = selected_profile
        self.running = True
        
        # ✅ NEW: Use AudioManager for centralized audio control
        self.bg_music = os.path.join(config.SOUND_MAIN_PATH, "bg_sound.mp3")
        self.play_bg_music()
        self.hover_channel = pygame.mixer.Channel(config.HOVER_CHANNEL_ID)
        
        # Backwards compatibility - keep these for old code
        self._current_audio_type = 'bg_music'
        self._current_audio_path = None
        
        # === Backgrounds ===
        self.welcome_bg, self.welcome_bg_pos = load_scaled_background(
            os.path.join(config.IMG_MAIN_PATH, "background.png"),
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            keep_aspect=False
        )
        
        # === Profile Icon ===
        avatar_name = selected_profile.get("avatar") if selected_profile else None
        avatar_path = os.path.join(config.AVATAR_PROFILES_PATH, avatar_name) if avatar_name else os.path.join(config.IMG_MAIN_PATH, "profile_icon.png")
        self.profile_icon = load_image(
            avatar_path,
            SCREEN_WIDTH * config.PROFILE_ICON_SIZE_RATIO,
            SCREEN_WIDTH * config.PROFILE_ICON_SIZE_RATIO
        )
        self.profile_rect = self.profile_icon.get_rect(topright=(SCREEN_WIDTH - 30, 30))
        
        # === Exit Icon ===
        exit_icon_path = os.path.join(config.IMG_MAIN_PATH, "exit_icon.png")
        self.exit_icon = load_image(
            exit_icon_path,
            SCREEN_WIDTH * config.EXIT_ICON_WIDTH_RATIO,
            SCREEN_HEIGHT * config.EXIT_ICON_HEIGHT_RATIO
        )
        self.exit_rect = self.exit_icon.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))
        
        # State for hover sounds
        self._last_hovered_btn_id = None
    
    # ==========================================================
    # TEXT RENDERING
    # ==========================================================
    def draw_arabic_text(self, text, size_ratio, color, center, bold=False):
        """Render Arabic text with proper shaping."""
        reshaped = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped)
        
        font = dynamic_font(
            SCREEN_HEIGHT,
            config.ARABIC_FONT_REGULAR,
            config.ARABIC_FONT_BOLD,
            size_ratio=size_ratio,
            bold=bold
        )
        
        rendered = font.render(bidi_text, True, color)
        rect = rendered.get_rect(center=center)
        screen.blit(rendered, rect)
    
    # ==========================================================
    # AUDIO METHODS
    # ==========================================================
    def play_hover_sound(self, path):
        """Play hover sound effect."""
        sound = load_sound(path)
        if sound:
            if self.hover_channel.get_busy():
                self.hover_channel.stop()
            self.hover_channel.play(sound)
    
    def play_bg_music(self):
        """Play background music."""
        try:
            pygame.mixer.music.load(self.bg_music)
            pygame.mixer.music.set_volume(config.BG_MUSIC_VOLUME)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Music error:", e)
    
    def open_profile_manager(self):
        """Open profile manager with proper audio state management."""
        # Save current state
        was_playing = pygame.mixer.music.get_busy()
        
        # Stop all sounds
        pygame.mixer.music.stop()
        for i in range(pygame.mixer.get_num_channels()):
            pygame.mixer.Channel(i).stop()
        
        # Open profile manager
        updated = run_profile_manage_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, self.selected_profile)
        
        # Handle profile changes
        if updated:
            if updated.get("_deleted"):
                self.selected_profile = run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
                self.play_bg_music()
            else:
                self.selected_profile.update(updated)
                avatar_path = os.path.join(config.AVATAR_PROFILES_PATH, self.selected_profile["avatar"])
                self.profile_icon = load_image(avatar_path, SCREEN_WIDTH * config.PROFILE_ICON_SIZE_RATIO, SCREEN_WIDTH * config.PROFILE_ICON_SIZE_RATIO)
                self.profile_rect = self.profile_icon.get_rect(topright=(SCREEN_WIDTH - 30, 30))
                
                # Restore music if it was playing
                if was_playing:
                    self.play_bg_music()
                
    
    def confirm_popup(self, msg):
        """Show confirmation popup."""
        return confirm_popup(
            self.screen,
            msg,
            lambda size, bold=False: load_font(
                config.ARABIC_FONT_REGULAR,
                config.ARABIC_FONT_BOLD,
                size,
                bold
            )
        )
    
    # ==========================================================
    # LAUNCH METHODS FOR LEARNING TOPICS
    # ==========================================================
    def launch_learn_lvl1_T1(self):
        """Launch Level 1 Topic 1."""
        pygame.mixer.stop()
        run_learn_lvl1_T1(self.screen, self)
    
    def launch_learn_lvl1_T2(self):
        """Launch Level 1 Topic 2."""
        pygame.mixer.stop()
        run_learn_lvl1_T2(self.screen, self)

    def launch_learn_lvl1_T3(self):
        """Launch Level 1 Topic 3."""
        pygame.mixer.stop()
        run_learn_lvl1_T3(self.screen, self)

    def launch_learn_lvl2_T1(self):
        """Launch Level 2 Topic 3."""
        pygame.mixer.stop()
        run_learn_lvl2_T1(self.screen, self)
        
    def launch_learn_lvl2_T2(self):
        """Launch Level 2 Topic 3."""
        pygame.mixer.stop()
        run_learn_lvl2_T2(self.screen, self)

    def launch_learn_lvl2_T3(self):
        """Launch Level 2 Topic 3."""
        pygame.mixer.stop()
        run_learn_lvl2_T3(self.screen, self)

    def launch_quiz_lvl1_3(self):
        """Launch Level 2 Topic 3."""
        pygame.mixer.stop()
        run_AlphabitQuiz(self.screen, self)

    def launch_quiz_lvl4(self):
        """Launch Level 2 Topic 3."""
        pygame.mixer.stop()
        run_LVL4(self.screen, self)
    
##    def launch_alphabit_sound(self):
##        """Launch alphabet sound screen."""
##        pygame.mixer.stop()
##        run_alphabit_sound(self.screen, main_app=self)
##    
##    def launch_alphabit_name(self):
##        """Launch alphabet name screen."""
##        pygame.mixer.stop()
##        print("⚠️ Alphabit Names Screen not yet implemented")
    
    # ==========================================================
    # WELCOME SCREEN
    # ==========================================================
    def open_welcome_screen(self):
        """Main Welcome Menu."""
        # Define welcome buttons
        extra_buttons = [
            {"label": "Level Check", "color": config.COLOR_GREEN, "x_ratio": 0.29, "y_ratio": 0.25, "w_ratio": 0.15, "h_ratio": 0.10},
            {"label": "Learning", "color": (255, 204, 0), "x_ratio": 0.39, "y_ratio": 0.45, "w_ratio": 0.15, "h_ratio": 0.10},
            {"label": "Quizzes", "color": (255, 51, 51), "x_ratio": 0.49, "y_ratio": 0.65, "w_ratio": 0.15, "h_ratio": 0.10},
        ]
        
        # Precompute rects
        for b in extra_buttons:
            x = int(SCREEN_WIDTH * b["x_ratio"])
            y = int(SCREEN_HEIGHT * b["y_ratio"])
            w = int(SCREEN_WIDTH * b["w_ratio"])
            h = int(SCREEN_HEIGHT * b["h_ratio"])
            b["rect"] = pygame.Rect(x - w // 2, y - h // 2, w, h)
        
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            screen.fill(config.COLOR_WHITE)
            screen.blit(self.welcome_bg, self.welcome_bg_pos)
            
            # Draw buttons
            for b in extra_buttons:
                pygame.draw.rect(screen, b["color"], b["rect"], border_radius=config.BUTTON_BORDER_RADIUS)
                pygame.draw.rect(screen, config.COLOR_WHITE, b["rect"], 4, border_radius=config.BUTTON_BORDER_RADIUS)
                self.draw_arabic_text(b["label"], 0.05, config.COLOR_WHITE, b["rect"].center, bold=True)
            
            # Profile + Exit
            screen.blit(self.profile_icon, self.profile_rect)
            if self.profile_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, config.COLOR_ORANGE, self.profile_rect, 3, border_radius=10)
            
            screen.blit(self.exit_icon, self.exit_rect)
            if self.exit_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, config.COLOR_ORANGE, self.exit_rect, 3, border_radius=10)
            
            # Events
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    if self.confirm_popup("Exit the game?"):
                        pygame.quit()
                        sys.exit()
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    if self.confirm_popup("Exit the game?"):
                        pygame.quit()
                        sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_rect.collidepoint(mouse_pos):
                        if self.confirm_popup("Exit the game?"):
                            pygame.quit()
                            sys.exit()
                    elif self.profile_rect.collidepoint(mouse_pos):
                        self.open_profile_manager()
                    else:
                        for b in extra_buttons:
                            if b["rect"].collidepoint(mouse_pos):
                                if b["label"] == "Level Check":
                                    print("⚠️ Level Check not yet implemented")
                                elif b["label"] == "Learning":
                                    self.open_learning_screen()
                                elif b["label"] == "Quizzes":
                                    self.open_quiz_screen()
            
            pygame.display.flip()
            clock.tick(60)
    
    # ==========================================================
    # LEARNING SCREEN
    # ==========================================================
    def open_learning_screen(self):
        """Learning screen with level selection."""
        soccer_path = os.path.join(config.IMG_MAIN_PATH, "soccerfield.png")
        
        try:
            if not os.path.exists(soccer_path):
                raise FileNotFoundError(f"Soccer field background not found: {soccer_path}")
            bg_image = pygame.image.load(soccer_path).convert()
            bg_image = pygame.transform.smoothscale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"❌ Error loading soccerfield.png: {e}")
            bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            bg_image.fill((50, 100, 50))
        
        # Prepare level buttons
        lvl_buttons = []
        for i in range(1, 10):
            img_path = os.path.join(config.IMG_MAIN_PATH, f"LVL {i}.png")
            try:
                img = pygame.image.load(img_path).convert_alpha()
            except Exception as e:
                print(f"⚠️ Missing image for LVL {i}: {e}")
                img = pygame.Surface((100, 100), pygame.SRCALPHA)
                pygame.draw.rect(img, config.COLOR_RED, img.get_rect(), 4)
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
            screen.fill(config.COLOR_WHITE)
            screen.blit(bg_image, (0, 0))
            
            # Title
            title_font = dynamic_font(SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, config.TITLE_SIZE_RATIO, bold=True)
            title_text = title_font.render("Learning Levels", True, config.COLOR_WHITE)
            screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.04))))
            
            # Profile icon
            screen.blit(self.profile_icon, self.profile_rect)
            if self.profile_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, config.COLOR_ORANGE, self.profile_rect, 3, border_radius=10)
            
            # Level buttons
            img_w, img_h = int(SCREEN_WIDTH * IMG_W_RATIO), int(SCREEN_HEIGHT * IMG_H_RATIO)
            font = dynamic_font(SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, 0.02, bold=True)
            for (x_ratio, y_ratio), btn in zip(scatter_positions, lvl_buttons):
                x = int(SCREEN_WIDTH * x_ratio)
                y = int(SCREEN_HEIGHT * y_ratio)
                scaled_img = pygame.transform.smoothscale(btn["image"], (img_w, img_h))
                rect = scaled_img.get_rect(center=(x, y))
                btn["rect"] = rect
                screen.blit(scaled_img, rect)
                label = font.render(btn["label"], True, (255, 51, 51))
                screen.blit(label, label.get_rect(center=(x, y + img_h // 2 + 30)))
            
            # Back button
            hint_font = dynamic_font(SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, config.SMALL_TEXT_SIZE_RATIO, bold=True)
            hint_text = hint_font.render("BACK", True, config.COLOR_WHITE)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(hint_text, hint_rect)
            if hint_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, config.COLOR_ORANGE, hint_rect.inflate(20, 10), 2, border_radius=8)
            
            # Events
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if hint_rect.collidepoint(e.pos):
                        running = False
                    elif self.profile_rect.collidepoint(e.pos):
                        self.open_profile_manager()
                    else:
                        for b in lvl_buttons:
                            if b["rect"] and b["rect"].collidepoint(e.pos):
                                level = int(b["label"].split()[1])
                                run_learning_topics(screen, self, level=level)
            
            pygame.display.flip()
            clock.tick(60)
    
    # ==========================================================
    # QUIZ SCREEN
    # ==========================================================
    def open_quiz_screen(self):
        """Quiz screen with level selection."""
        soccer_path = os.path.join(config.IMG_MAIN_PATH, "soccerfield.png")
        
        try:
            if not os.path.exists(soccer_path):
                raise FileNotFoundError(f"Soccer field background not found: {soccer_path}")
            bg_image = pygame.image.load(soccer_path).convert()
            bg_image = pygame.transform.smoothscale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"❌ Error loading soccerfield.png: {e}")
            bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            bg_image.fill((30, 30, 80))
        
        # Prepare level buttons (same as learning screen)
        lvl_buttons = []
        for i in range(1, 10):
            img_path = os.path.join(config.IMG_MAIN_PATH, f"LVL {i}.png")
            try:
                img = pygame.image.load(img_path).convert_alpha()
            except Exception as e:
                print(f"⚠️ Missing image for LVL {i}: {e}")
                img = pygame.Surface((100, 100), pygame.SRCALPHA)
                pygame.draw.rect(img, config.COLOR_RED, img.get_rect(), 4)
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
            screen.fill(config.COLOR_WHITE)
            screen.blit(bg_image, (0, 0))
            
            # Title
            title_font = dynamic_font(SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, config.TITLE_SIZE_RATIO, bold=True)
            title_text = title_font.render("Quizzes", True, config.COLOR_WHITE)
            screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.04))))
            
            # Profile icon
            screen.blit(self.profile_icon, self.profile_rect)
            if self.profile_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, config.COLOR_ORANGE, self.profile_rect, 3, border_radius=10)
            
            # Level buttons
            img_w, img_h = int(SCREEN_WIDTH * IMG_W_RATIO), int(SCREEN_HEIGHT * IMG_H_RATIO)
            font = dynamic_font(SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, 0.02, bold=True)
            for (x_ratio, y_ratio), btn in zip(scatter_positions, lvl_buttons):
                x = int(SCREEN_WIDTH * x_ratio)
                y = int(SCREEN_HEIGHT * y_ratio)
                scaled_img = pygame.transform.smoothscale(btn["image"], (img_w, img_h))
                rect = scaled_img.get_rect(center=(x, y))
                btn["rect"] = rect
                screen.blit(scaled_img, rect)
                label = font.render(btn["label"], True, (255, 51, 51))
                screen.blit(label, label.get_rect(center=(x, y + img_h // 2 + 30)))
            
            # Back button
            hint_font = dynamic_font(SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, config.SMALL_TEXT_SIZE_RATIO, bold=True)
            hint_text = hint_font.render("BACK", True, config.COLOR_WHITE)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(hint_text, hint_rect)
            if hint_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, config.COLOR_ORANGE, hint_rect.inflate(20, 10), 2, border_radius=8)
            
            # Events
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if hint_rect.collidepoint(e.pos):
                        running = False
                    elif self.profile_rect.collidepoint(e.pos):
                        self.open_profile_manager()
                    else:
                        for b in lvl_buttons:
                            if b["rect"] and b["rect"].collidepoint(e.pos):
                                level = int(b["label"].split()[1])
                                run_quiz_topics(screen, self, level=level)
            
            pygame.display.flip()
            clock.tick(60)
    
    # ==========================================================
    # MAIN LOOP
    # ==========================================================
    def run(self):
        """Start the application."""
        self.open_welcome_screen()

# ==========================================================
# ENTRY POINT
# ==========================================================
if __name__ == "__main__":
    selected_profile = run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    app = QuizApp(selected_profile)
    app.run()
