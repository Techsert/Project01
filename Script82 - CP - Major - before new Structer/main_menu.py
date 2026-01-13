import os
import sys
import pygame
import arabic_reshaper
import config
from screen_helpers import confirm_popup, dynamic_font, load_font, load_image
from bidi.algorithm import get_display
from profile_screen import run_profile_screen, run_profile_manage_screen
from audio_manager import AudioManager  # ✅ IMPORT AUDIO MANAGER
from reward_popup import RewardPopup 

# -------------- Learning topics -----------------
from learning_topics import run_learning_topics
from learn_lvl1_T1 import run_learn_lvl1_T1
from learn_lvl1_T2 import run_learn_lvl1_T2
from learn_lvl1_T3 import run_learn_lvl1_T3
from learn_lvl2_T1 import run_learn_lvl2_T1
from learn_lvl2_T2 import run_learn_lvl2_T2
from learn_lvl2_T3 import run_learn_lvl2_T3
from learn_lvl2_T4 import run_learn_lvl2_T4
from learn_lvl2_T5 import run_learn_lvl2_T5
from learn_lvl2_T6 import run_learn_lvl2_T6
from learn_lvl2_T7 import run_learn_lvl2_T7

# -------------- Practices ----------------------
from practice_lvl1_P1 import run_practice_lvl1_P1
from practice_lvl2_P1 import run_practice_lvl2_P1
from practice_lvl2_P2 import run_practice_lvl2_P2

# ---------------- Quiz topics ------------------
from quiz_topics import run_quiz_topics
from quiz_lvl1 import run_quiz_lvl1
from quiz_lvl2 import run_quiz_lvl2
from quiz_lvl3 import run_quiz_lvl3

# ==========================================================
# PYGAME INITIALIZATION
# ==========================================================
pygame.init()
pygame.mixer.init()

# ✅ Get screen dimensions properly
SCREEN_WIDTH, SCREEN_HEIGHT = config.get_screen_dimensions()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Welcome to Learning World - Level One")
clock = pygame.time.Clock()

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

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
        self.audio_manager = AudioManager()
        self.audio_manager.play_bg_music()

        # ✅ NEW: Reward popup manager
        self.reward_popup = RewardPopup(screen)
        
        # === Backgrounds ===
        self.welcome_bg = load_image(
            os.path.join(config.IMG_MAIN_PATH, "background.png"),
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            keep_aspect=False
        )
        self.welcome_bg_pos = (0, 0)
        
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
    # AUDIO METHODS - USING AUDIO MANAGER
    # ==========================================================
    def play_hover_sound(self, path):
        """Play hover sound effect using AudioManager."""
        self.audio_manager.play_hover_sound(path)
    
    def open_profile_manager(self):
        """Open profile manager with proper audio state management."""
        # ✅ Push current audio context to stack
        self.audio_manager.push_audio_context()
        
        # Stop all sounds
        self.audio_manager.stop_all_sounds()
        
        # Open profile manager
        updated = run_profile_manage_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, self.selected_profile)
        
        # Handle profile changes
        if updated:
            if updated.get("_deleted"):
                self.selected_profile = run_profile_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
                self.audio_manager.play_bg_music()
            else:
                self.selected_profile.update(updated)
                avatar_path = os.path.join(config.AVATAR_PROFILES_PATH, self.selected_profile["avatar"])
                self.profile_icon = load_image(avatar_path, SCREEN_WIDTH * config.PROFILE_ICON_SIZE_RATIO, SCREEN_WIDTH * config.PROFILE_ICON_SIZE_RATIO)
                self.profile_rect = self.profile_icon.get_rect(topright=(SCREEN_WIDTH - 30, 30))
        
        # ✅ Pop and restore audio context
        self.audio_manager.pop_audio_context(restore=True)
    
    def confirm_popup(self, msg):
        """Show confirmation popup using screen_helpers."""
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
    # ✅ NEW: REWARD POPUP DISPLAY
    # ==========================================================
    def _show_reward_popup(self):
        """Display reward popup overlay - similar to quiz feedback."""
        clock = pygame.time.Clock()
        
        # Show first reward
        if not self.reward_popup.is_active() and self.reward_popup.has_pending_rewards():
            self.reward_popup.show_next_reward()
        
        # Main loop for reward display
        while self.reward_popup.is_active() or self.reward_popup.has_pending_rewards():
            # Update reward state
            self.reward_popup.update()
            
            # Redraw current screen (to keep background visible)
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.welcome_bg, self.welcome_bg_pos)
            
            # Draw reward popup on top
            self.reward_popup.draw()
            
            pygame.display.flip()
            
            # Handle events
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    # Click to advance to next reward or close
                    self.reward_popup.handle_click()
                elif e.type == pygame.KEYDOWN:
                    if e.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                        self.reward_popup.handle_click()
            
            clock.tick(60)
    
    # ==========================================================
    # ✅ UPDATED: PROFILE RELOAD WITH REWARD CHECK
    # ==========================================================
    def _reload_profile(self):
        """Reload the current profile from disk to get updated progress/rewards."""
        from profile_system import load_profiles
        
        profiles = load_profiles()
        current_name = self.selected_profile.get("name")
        
        for p in profiles:
            if p.get("name") == current_name:
                # ✅ Track old rewards BEFORE reloading
                old_rewards = set(self.selected_profile.get("rewards", []))
                
                # Update the selected profile with fresh data
                self.selected_profile.update(p)
                
                # ✅ Find NEW rewards (ones that weren't there before)
                new_rewards = set(p.get("rewards", [])) - old_rewards
                
                print(f"📄 Reloaded profile: {current_name}, Total rewards: {len(p.get('rewards', []))}, New: {len(new_rewards)}")
                
                # ✅ Only add NEW rewards to popup
                if new_rewards:
                    for reward in new_rewards:
                        self.reward_popup.add_reward(reward)
                    
                    # Show popup if there are rewards to display
                    if self.reward_popup.has_pending_rewards():
                        self._show_reward_popup()
                
                break

    
    # ==========================================================
    # LAUNCH METHODS FOR LEARNING TOPICS
    # ==========================================================
    # -------------- Learning topics -----------------
    def launch_learn_lvl1_T1(self):
        """Launch Level 1 Topic 1."""
        self.audio_manager.stop_all_sounds()
        run_learn_lvl1_T1(self.screen, self)
        self._reload_profile()
    
    def launch_learn_lvl1_T2(self):
        """Launch Level 1 Topic 2."""
        self.audio_manager.stop_all_sounds()
        run_learn_lvl1_T2(self.screen, self)
        self._reload_profile()

    def launch_learn_lvl1_T3(self):
        """Launch Level 1 Topic 3."""
        self.audio_manager.stop_all_sounds()
        run_learn_lvl1_T3(self.screen, self)
        self._reload_profile()

    def launch_learn_lvl2_T1(self):
        """Launch Level 2 Topic 1."""
        self.audio_manager.stop_all_sounds()
        run_learn_lvl2_T1(self.screen, self)
        self._reload_profile()
        
    def launch_learn_lvl2_T2(self):
        """Launch Level 2 Topic 2."""
        self.audio_manager.stop_all_sounds()
        run_learn_lvl2_T2(self.screen, self)
        self._reload_profile()

    def launch_learn_lvl2_T3(self):
        """Launch Level 2 Topic 3."""
        self.audio_manager.stop_all_sounds()
        run_learn_lvl2_T3(self.screen, self)
        self._reload_profile()
        
    def launch_learn_lvl2_T4(self):
        """Launch Level 2 Topic 4."""
        self.audio_manager.stop_all_sounds()
        run_learn_lvl2_T4(self.screen, self)
        self._reload_profile()

    def launch_learn_lvl2_T5(self):
        """Launch Level 2 Topic 5."""
        self.audio_manager.stop_all_sounds()
        run_learn_lvl2_T5(self.screen, self)
        self._reload_profile()

    def launch_learn_lvl2_T6(self):
        """Launch Level 2 Topic 6."""
        self.audio_manager.stop_all_sounds()
        run_learn_lvl2_T6(self.screen, self)
        self._reload_profile()

    def launch_learn_lvl2_T7(self):
        """Launch Level 2 Topic 7."""
        self.audio_manager.stop_all_sounds()
        run_learn_lvl2_T7(self.screen, self)
        self._reload_profile()

    # -------------- Practices ----------------------

    def launch_practice_lvl1_P1(self):
        """Launch Level 1 Practice 1."""
        self.audio_manager.stop_all_sounds()
        from practice_lvl1_P1 import run_practice_lvl1_P1
        run_practice_lvl1_P1(self.screen, self)
        self._reload_profile()

    def launch_practice_lvl2_P1(self):
        """Launch Level 2 Practice 1."""
        self.audio_manager.stop_all_sounds()
        from practice_lvl2_P1 import run_practice_lvl2_P1
        run_practice_lvl2_P1(self.screen, self)
        self._reload_profile()

    def launch_practice_lvl2_P2(self):
        """Launch Level 2 Practice 2."""
        self.audio_manager.stop_all_sounds()
        from practice_lvl2_P2 import run_practice_lvl2_P2
        run_practice_lvl2_P2(self.screen, self)
        self._reload_profile()

    # ---------------- Quiz topics ------------------

    def launch_quiz_lvl1(self):
        """Launch Level 1 Quiz."""
        self.audio_manager.stop_all_sounds()
        run_quiz_lvl1(self.screen, self)
        self._reload_profile()
        
    def launch_quiz_lvl2(self):
        """Launch Level 2 Quiz."""
        self.audio_manager.stop_all_sounds()
        run_quiz_lvl2(self.screen, self)
        self._reload_profile()
        
    def launch_quiz_lvl3(self):
        """Launch Level 3 Quiz."""
        self.audio_manager.stop_all_sounds()
        run_quiz_lvl3(self.screen, self)
        self._reload_profile()
    
    # ==========================================================
    # WELCOME SCREEN
    # ==========================================================
    def open_welcome_screen(self):
        """Main Welcome Menu."""
        extra_buttons = [
            {"label": "Level Check", "color": config.COLOR_GREEN, "x_ratio": 0.29, "y_ratio": 0.25, "w_ratio": 0.15, "h_ratio": 0.10},
            {"label": "Learning", "color": (255, 204, 0), "x_ratio": 0.39, "y_ratio": 0.45, "w_ratio": 0.15, "h_ratio": 0.10},
            {"label": "Quizzes", "color": (255, 51, 51), "x_ratio": 0.49, "y_ratio": 0.65, "w_ratio": 0.15, "h_ratio": 0.10},
        ]
        
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
            
            title_font = dynamic_font(SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, config.TITLE_SIZE_RATIO, bold=True)
            title_text = title_font.render("Learning Levels", True, config.COLOR_WHITE)
            screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.04))))
            
            screen.blit(self.profile_icon, self.profile_rect)
            if self.profile_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, config.COLOR_ORANGE, self.profile_rect, 3, border_radius=10)
            
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
            
            hint_font = dynamic_font(SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, config.SMALL_TEXT_SIZE_RATIO, bold=True)
            hint_text = hint_font.render("BACK", True, config.COLOR_WHITE)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(hint_text, hint_rect)
            if hint_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, config.COLOR_ORANGE, hint_rect.inflate(20, 10), 2, border_radius=8)
            
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
            
            title_font = dynamic_font(SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, config.TITLE_SIZE_RATIO, bold=True)
            title_text = title_font.render("Quizzes", True, config.COLOR_WHITE)
            screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.04))))
            
            screen.blit(self.profile_icon, self.profile_rect)
            if self.profile_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, config.COLOR_ORANGE, self.profile_rect, 3, border_radius=10)
            
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
            
            hint_font = dynamic_font(SCREEN_HEIGHT, config.ARABIC_FONT_REGULAR, config.ARABIC_FONT_BOLD, config.SMALL_TEXT_SIZE_RATIO, bold=True)
            hint_text = hint_font.render("BACK", True, config.COLOR_WHITE)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(hint_text, hint_rect)
            if hint_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, config.COLOR_ORANGE, hint_rect.inflate(20, 10), 2, border_radius=8)
            
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
