# quiz_base.py - Base class for all quizzes
import pygame
import sys
import os
import random
import time
from PIL import Image, ImageFont, ImageDraw
import config

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_BIDI = True
except Exception:
    HAS_BIDI = False
    print("⚠️ Missing 'arabic_reshaper' and/or 'python-bidi'")

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================
def load_image(path, alpha=True):
    """Load image with error handling."""
    if not os.path.exists(path):
        print(f"⚠️ Missing image: {path}")
        return None
    try:
        return pygame.image.load(path).convert_alpha()
    except Exception as e:
        print(f"⚠️ Failed to load image {path}: {e}")
        return None

def load_sound(path):
    """Load sound with error handling."""
    if not os.path.exists(path):
        print(f"⚠️ Missing sound: {path}")
        return None
    try:
        return pygame.mixer.Sound(path)
    except Exception as e:
        print(f"⚠️ Failed to load sound {path}: {e}")
        return None

def render_arabic_to_surface(text, font_path, size, color=(255,255,255), bold=False):
    """Render Arabic text to a surface."""
    if HAS_BIDI and font_path and os.path.exists(font_path):
        try:
            reshaped = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped)
            pil_font = ImageFont.truetype(font_path, size)
            dummy = Image.new("RGBA", (10,10), (0,0,0,0))
            draw = ImageDraw.Draw(dummy)
            bbox = draw.textbbox((0,0), bidi_text, font=pil_font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            img = Image.new("RGBA", (w, h), (0,0,0,0))
            draw = ImageDraw.Draw(img)
            draw.text((-bbox[0], -bbox[1]), bidi_text, font=pil_font, fill=color)
            mode = img.mode
            data = img.tobytes()
            surf = pygame.image.fromstring(data, (w, h), mode).convert_alpha()
            return surf
        except Exception as e:
            print("⚠️ Arabic PIL rendering failed:", e)
    
    # Fallback
    try:
        if font_path and os.path.exists(font_path):
            f = pygame.font.Font(font_path, size)
        else:
            f = pygame.font.SysFont("arial", size)
        f.set_bold(bold)
        surf = f.render(text, True, color)
        return surf.convert_alpha()
    except Exception as e:
        print("⚠️ Fallback rendering failed:", e)
        return pygame.Surface((1,1), pygame.SRCALPHA)

# ==========================================================
# BASE QUIZ PLAYER CLASS
# ==========================================================
class QuizPlayer:
    """
    Base class for quiz presentations.
    Handles common quiz functionality like difficulty selection,
    question display, scoring, and navigation.
    """
    
    def __init__(self, screen, main_app, questions, level=1, 
                 img_path=None, sound_path=None, fonts_path=None, auto_difficulty=None):
        """
        Args:
            screen: Pygame screen surface
            main_app: Reference to QuizApp instance
            questions: List of question dictionaries
            level: Quiz level number
            img_path: Path to images folder
            sound_path: Path to sounds folder
            fonts_path: Path to fonts folder
            auto_difficulty: If set, auto-select this difficulty ("easy", "medium", "hard")
        """
        self.screen = screen
        self.main_app = main_app
        self.all_questions = questions
        self.level = level
        self.auto_difficulty = auto_difficulty  # Store auto-difficulty setting
        
        # Paths
        self.IMG_PATH = img_path or os.path.join(config.ASSETS_PATH, "img/alphabitSound/letters")
        self.SOUND_PATH = sound_path or os.path.join(config.ASSETS_PATH, "sounds/alphabitSound")
        self.FONTS_PATH = fonts_path or os.path.join(config.ASSETS_PATH, "fonts")
        
        # Screen setup
        self.W, self.H = screen.get_size()
        self.clock = pygame.time.Clock()
        
        # Find Arabic font
        self.ARABIC_FONT_PATH = self.find_arabic_font()
        
        # Audio volumes
        self.volume_hover = 0.8
        self.volume_questions = 1.0
        self.volume_feedback = 1.0
        
        # Load hover sounds
        self.hover_sounds = {}
        for level_name in ("easy", "medium", "hard"):
            path = os.path.join(self.SOUND_PATH, f"hover_{level_name}.wav")
            if os.path.exists(path):
                try:
                    snd = pygame.mixer.Sound(path)
                    snd.set_volume(self.volume_hover)
                    self.hover_sounds[level_name] = snd
                except Exception as e:
                    print(f"⚠️ Failed to load hover sound {level_name}: {e}")
        
        # Game state
        self.state = "menu" if not auto_difficulty else "playing"  # Skip menu if auto-difficulty set
        self.selected_difficulty = auto_difficulty  # Pre-set difficulty
        self.questions = []
        self.current_idx = 0
        self.selected_options = set()
        self.score = 0
        self.feedback_until = 0
        self.feedback_correct = False
        self.current_feedback_sound = None
        self.menu_rects = {}
        self.results_buttons = {}
        
        # Sound management
        self.loaded_sounds = {}
        self.current_question_sound = None
        self.question_replay_count = 5
        self.question_replay_interval = 10000
        self.current_replay = 0
        
        # Load backgrounds
        self.bg = load_image(os.path.join(self.IMG_PATH, "soccerfield.png"), alpha=False)
        if self.bg:
            self.bg = pygame.transform.smoothscale(self.bg, (self.W, self.H))
        
        self.question_bg = load_image(os.path.join(self.IMG_PATH, "quiz_bg.png"), alpha=False)
        if self.question_bg:
            self.question_bg = pygame.transform.smoothscale(self.question_bg, (self.W, self.H))
        
        # Feedback icons
        self.goal_icon = load_image(os.path.join(self.IMG_PATH, "football_goal.png"))
        if self.goal_icon:
            self.goal_icon = pygame.transform.smoothscale(self.goal_icon, (60, 60))
        
        self.miss_icon = load_image(os.path.join(self.IMG_PATH, "football_miss.png"))
        if self.miss_icon:
            self.miss_icon = pygame.transform.smoothscale(self.miss_icon, (60, 60))
        
        # Load feedback images and sounds
        self.load_feedback_assets()
        
        # Difficulty icons
        self.load_difficulty_icons()
        
        # Exit button
        self.setup_exit_button()
        
        self.running = True
    
    def find_arabic_font(self):
        """Find available Arabic font."""
        preferred = [
            os.path.join(self.FONTS_PATH, "NotoNaskhArabic-Regular.ttf"),
            os.path.join(self.FONTS_PATH, "arabic.ttf"),
            os.path.join(self.FONTS_PATH, "NotoSansArabic-Regular.ttf"),
        ]
        for p in preferred:
            if os.path.exists(p):
                return p
        try:
            return pygame.font.match_font("arial")
        except Exception:
            return None
    
    def load_feedback_assets(self):
        """Load feedback images and sounds."""
        self.correct_feedback_imgs = []
        self.wrong_feedback_imgs = []
        
        for i in range(7):
            suffix = "" if i == 0 else str(i)
            correct_img = load_image(os.path.join(self.IMG_PATH, f"thumbsup{suffix}.png"))
            wrong_img = load_image(os.path.join(self.IMG_PATH, f"thumbsdown{suffix}.png"))
            if correct_img:
                self.correct_feedback_imgs.append(correct_img)
            if wrong_img:
                self.wrong_feedback_imgs.append(wrong_img)
        
        self.correct_feedback_sounds = []
        self.wrong_feedback_sounds = []
        
        for i in range(6):
            suffix = "" if i == 0 else str(i)
            correct_snd = load_sound(os.path.join(self.SOUND_PATH, f"correct{suffix}.wav"))
            wrong_snd = load_sound(os.path.join(self.SOUND_PATH, f"wrong{suffix}.wav"))
            if correct_snd:
                self.correct_feedback_sounds.append(correct_snd)
            if wrong_snd:
                self.wrong_feedback_sounds.append(wrong_snd)
    
    def load_difficulty_icons(self):
        """Load difficulty selection icons."""
        self.diff_orig = {}
        self.diff_state = {}
        
        for d in ("easy", "medium", "hard"):
            p = os.path.join(self.IMG_PATH, f"{d}.png")
            img = load_image(p, alpha=True)
            if img:
                max_h = int(self.H * 0.6)
                scale = max_h / img.get_height()
                w = int(img.get_width() * scale * 0.8)
                h = int(max_h * 0.9)
                img = pygame.transform.smoothscale(img, (w, h))
            else:
                img = pygame.Surface((int(self.W*0.15), int(self.H*0.5)), pygame.SRCALPHA)
                img.fill((200, 200, 200, 255))
            
            self.diff_orig[d] = img
            self.diff_state[d] = {'orig': img, 'scale': 1.0, 'target': 1.0}
        
        self.diff_centers = [
            (int(self.W*0.25), int(self.H*0.55)),
            (int(self.W*0.5), int(self.H*0.55)),
            (int(self.W*0.75), int(self.H*0.55))
        ]
        
        self.last_hovered = None
    
    def setup_exit_button(self):
        """Setup exit button."""
        exit_img_path = os.path.join(self.IMG_PATH, "exitball.png")
        self.exit_img = load_image(exit_img_path, alpha=True)
        if self.exit_img:
            size = int(self.W * 0.07)
            try:
                self.exit_img = pygame.transform.smoothscale(self.exit_img, (size, size))
            except Exception:
                pass
            self.exit_rect = self.exit_img.get_rect(center=(self.W // 2, self.H - 80))
        else:
            # Fallback
            size = int(self.W * 0.07)
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(surf, (200, 0, 0, 220), (size//2, size//2), size//2)
            self.exit_img = surf
            self.exit_rect = self.exit_img.get_rect(topleft=(20, 20))
        
        self.exit_hover_sound = load_sound(os.path.join(self.SOUND_PATH, "hover_exit.wav"))
        if self.exit_hover_sound:
            self.exit_hover_sound.set_volume(1.0)
        self.exit_hovered_last = False
        
        self.show_exit_confirm = False
        self.exit_confirm_rects = {}
    
    def stop_all_sounds(self):
        """Stop all sounds."""
        try:
            pygame.mixer.music.stop()
            for s in self.loaded_sounds.values():
                s.stop()
            for s in self.hover_sounds.values():
                s.stop()
            if self.exit_hover_sound:
                self.exit_hover_sound.stop()
        except Exception as e:
            print(f"❌ Error stopping sounds: {e}")
    
    def stop_hover_only(self):
        """Stop only hover sounds."""
        try:
            for s in self.hover_sounds.values():
                s.stop()
            if self.exit_hover_sound:
                self.exit_hover_sound.stop()
        except Exception:
            pass
    
    def play_sfx(self, name):
        """Play sound effect."""
        if name not in self.loaded_sounds:
            sound_path = os.path.join(self.SOUND_PATH, name)
            if os.path.exists(sound_path):
                try:
                    snd = pygame.mixer.Sound(sound_path)
                    snd.set_volume(self.volume_questions)
                    self.loaded_sounds[name] = snd
                except Exception as e:
                    print(f"⚠️ Failed to load sound {name}: {e}")
                    return
            else:
                print(f"⚠️ Missing sound: {name}")
                return
        
        s = self.loaded_sounds.get(name)
        if s:
            s.play()
    
    def build_question_list(self, difficulty):
        """Build filtered question list based on difficulty."""
        difficulty_map = {
            "easy": ["easy"],
            "medium": ["medium"],
            "hard": ["hard", "medium"]
        }
        
        include = difficulty_map.get(difficulty, [difficulty])
        filtered = [q.copy() for q in self.all_questions if q.get("difficulty") in include]
        random.shuffle(filtered)
        return filtered
    
    def select_difficulty(self, level):
        """Handle difficulty selection."""
        self.stop_all_sounds()
        self.selected_difficulty = level
        qs = self.build_question_list(level)
        
        if not qs:
            print(f"⚠️ No questions for: {level}")
            return
        
        self.questions = qs
        self.current_idx = 0
        self.selected_options = set()
        self.score = 0
        self.state = "playing"
        
        pygame.time.set_timer(pygame.USEREVENT+3, 300, True)
        self.play_current_question_sound()
    
    def play_current_question_sound(self, first_play=True):
        """Play current question's sound."""
        if not (0 <= self.current_idx < len(self.questions)):
            return
        
        # Stop previous question sound
        if self.current_question_sound:
            self.current_question_sound.stop()
            self.current_question_sound = None
        
        # Get sound for this question
        s = self.questions[self.current_idx].get("sound")
        if not s:
            return
        
        # Stop hover sounds
        for snd in self.hover_sounds.values():
            snd.stop()
        
        sound_path = os.path.join(self.SOUND_PATH, s)
        if not os.path.exists(sound_path):
            print(f"⚠️ Missing question sound: {sound_path}")
            return
        
        try:
            self.current_question_sound = pygame.mixer.Sound(sound_path)
            self.current_question_sound.play()
        except Exception as e:
            print(f"⚠️ Failed to play question sound: {e}")
            self.current_question_sound = None
            return
        
        # Start replay timer
        if first_play:
            self.current_replay = 1
            pygame.time.set_timer(pygame.USEREVENT + 4, self.question_replay_interval)
    
    def unload_current_question_assets(self):
        """Free memory for previous question."""
        if hasattr(self, "current_question_sound") and self.current_question_sound:
            self.current_question_sound.stop()
            del self.current_question_sound
            self.current_question_sound = None
        
        if hasattr(self, "option_rects"):
            del self.option_rects
        if hasattr(self, "option_images"):
            for img in self.option_images:
                del img
            self.option_images = []
    
    def check_answer(self, idx):
        """Check if answer is correct."""
        if not (0 <= self.current_idx < len(self.questions)):
            return
        
        q = self.questions[self.current_idx]
        correct_field = q.get("answer", 0)
        
        # Multi-answer
        if isinstance(correct_field, (list, tuple)):
            correct_set = set(correct_field)
            
            # Toggle selection
            if idx in self.selected_options:
                self.selected_options.remove(idx)
            else:
                self.selected_options.add(idx)
            
            # Wrong answer clicked
            if idx not in correct_set:
                self.stop_all_sounds()
                if self.current_question_sound:
                    self.current_question_sound.stop()
                    self.current_question_sound = None
                
                self.feedback_correct = False
                self.current_feedback_img = random.choice(self.wrong_feedback_imgs)
                snd = random.choice(self.wrong_feedback_sounds) if self.wrong_feedback_sounds else None
                self.current_feedback_sound = snd
                if snd:
                    snd.stop()
                    snd.play()
                self.feedback_until = pygame.time.get_ticks() + 4000
                self.state = "feedback"
                return
            
            # All correct selected
            if self.selected_options >= correct_set and set(correct_set) <= self.selected_options:
                self.stop_all_sounds()
                if self.current_question_sound:
                    self.current_question_sound.stop()
                    self.current_question_sound = None
                
                self.feedback_correct = True
                self.score += 1
                self.current_feedback_img = random.choice(self.correct_feedback_imgs)
                snd = random.choice(self.correct_feedback_sounds) if self.correct_feedback_sounds else None
                self.current_feedback_sound = snd
                if snd:
                    snd.stop()
                    snd.play()
                self.feedback_until = pygame.time.get_ticks() + 4000
                self.state = "feedback"
                return
            
            return
        
        # Single answer
        else:
            self.stop_all_sounds()
            if self.current_question_sound:
                self.current_question_sound.stop()
                self.current_question_sound = None
            
            self.feedback_correct = (idx == correct_field)
            if self.feedback_correct:
                self.score += 1
                self.current_feedback_img = random.choice(self.correct_feedback_imgs)
                snd = random.choice(self.correct_feedback_sounds) if self.correct_feedback_sounds else None
            else:
                self.current_feedback_img = random.choice(self.wrong_feedback_imgs)
                snd = random.choice(self.wrong_feedback_sounds) if self.wrong_feedback_sounds else None
            
            self.current_feedback_sound = snd
            if snd:
                snd.stop()
                snd.play()
            
            self.feedback_until = pygame.time.get_ticks() + 4000
            self.state = "feedback"
    
    def update_menu_hover(self):
        """Update menu hover effects."""
        mouse_pos = pygame.mouse.get_pos()
        hovered_any = False
        
        for idx, key in enumerate(("easy", "medium", "hard")):
            st = self.diff_state[key]
            orig = st['orig']
            scale = st['scale']
            ow, oh = orig.get_size()
            scaled_w = int(ow*scale)
            scaled_h = int(oh*scale)
            cx, cy = self.diff_centers[idx]
            rect = pygame.Rect(int(cx-scaled_w//2), int(cy-scaled_h//2), scaled_w, scaled_h)
            self.menu_rects[key] = rect
            
            if rect.collidepoint(mouse_pos):
                st['target'] = 1.08
                hovered_any = True
                if self.last_hovered != key:
                    self.stop_hover_only()
                    snd = self.hover_sounds.get(key)
                    if snd:
                        snd.play()
                    self.last_hovered = key
                try:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                except:
                    pass
            else:
                st['target'] = 1.0
        
        if not hovered_any:
            self.last_hovered = None
            try:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            except:
                pass
        
        for st in self.diff_state.values():
            st['scale'] += (st['target'] - st['scale']) * 0.18
    
    def draw_menu(self):
        """Draw difficulty selection menu."""
        bold_font_path = os.path.join(self.FONTS_PATH, "NotoNaskhArabic-Bold.ttf")
        title_surf = render_arabic_to_surface("إختر المستوى", bold_font_path, 80, color=(0, 0, 0), bold=True)
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.W//2, int(self.H*0.03))))
        
        for idx, key in enumerate(("easy", "medium", "hard")):
            st = self.diff_state[key]
            orig = st['orig']
            scale = st['scale']
            ow, oh = orig.get_size()
            sw = int(ow*scale)
            sh = int(oh*scale)
            cx, cy = self.diff_centers[idx]
            surf = pygame.transform.smoothscale(orig, (sw, sh))
            lift = int((scale-1.0)*20)
            pos = (int(cx-sw//2), int(cy-sh//2)-lift)
            self.screen.blit(surf, pos)
            self.menu_rects[key] = pygame.Rect(pos[0], pos[1], sw, sh)
    
    def draw_playing(self):
        """Draw the current question."""
        # To be implemented by subclass
        pass
    
    def draw_feedback(self):
        """Draw feedback overlay."""
        dark = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        dark.fill((0, 0, 0, 120))
        self.screen.blit(dark, (0, 0))
        
        img = getattr(self, "current_feedback_img", None)
        if img:
            rect = img.get_rect(center=(self.W//2, self.H//2))
            self.screen.blit(img, rect.topleft)
    
    def draw_results(self):
        """Draw results screen."""
        # Dim background
        dark = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        dark.fill((0, 0, 0, 160))
        self.screen.blit(dark, (0, 0))
        
        correct = self.score
        wrong = len(self.questions) - self.score
        
        # Title
        title = render_arabic_to_surface("نتيجة المباراة", self.ARABIC_FONT_PATH, 64, color=(255, 255, 255), bold=True)
        self.screen.blit(title, title.get_rect(center=(self.W // 2, int(self.H * 0.15))))
        
        # Layout icons
        icon_size = 80
        spacing = 15
        column_height = self.H * 0.55
        icons_per_column = max(1, int(column_height // (icon_size + spacing)))
        
        x_goal_start = int(self.W * 0.02)
        x_miss_start = int(self.W * 0.95)
        
        # Correct answers
        for i in range(correct):
            col = i // icons_per_column
            row = i % icons_per_column
            x = x_goal_start + col * (icon_size + spacing)
            y = int(self.H * 0.25) + row * (icon_size + spacing)
            if self.goal_icon:
                self.screen.blit(self.goal_icon, (x, y))
        
        # Wrong answers
        for i in range(wrong):
            col = i // icons_per_column
            row = i % icons_per_column
            x = x_miss_start - col * (icon_size + spacing)
            y = int(self.H * 0.25) + row * (icon_size + spacing)
            if self.miss_icon:
                self.screen.blit(self.miss_icon, (x, y))
        
        # Numeric results
        txt_correct = render_arabic_to_surface(str(correct), "arial", 500, color=(0, 255, 0))
        txt_wrong = render_arabic_to_surface(str(wrong), "arial", 500, color=(255, 0, 0))
        
        x_center = self.W // 2
        y_numeric = int(self.H * 0.20)
        
        self.screen.blit(txt_correct, txt_correct.get_rect(center=(x_center - int(self.W * 0.1), y_numeric)))
        self.screen.blit(txt_wrong, txt_wrong.get_rect(center=(x_center + int(self.W * 0.1), y_numeric)))
        
        # Play Again button
        button_w, button_h = 300, 80
        x_button = self.W // 2 - button_w // 2
        y_button = int(self.H * 0.8)
        pygame.draw.rect(self.screen, (255, 215, 0), (x_button, y_button, button_w, button_h), border_radius=20)
        txt_play = render_arabic_to_surface("العب مرة أخرى", self.ARABIC_FONT_PATH, 40, color=(0, 0, 0), bold=True)
        self.screen.blit(txt_play, txt_play.get_rect(center=(x_button + button_w // 2, y_button + button_h // 2)))
        
        self.results_buttons["play_again"] = pygame.Rect(x_button, y_button, button_w, button_h)
    
    def draw_exit_confirm(self):
        """Draw exit confirmation popup."""
        overlay = pygame.Surface((self.W, self.H))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        box_w, box_h = 600, 300
        box_rect = pygame.Rect((self.W - box_w)//2, (self.H - box_h)//2, box_w, box_h)
        pygame.draw.rect(self.screen, (255, 255, 255), box_rect, border_radius=20)
        pygame.draw.rect(self.screen, (0, 0, 0), box_rect, 4, border_radius=20)
        
        msg_surf = render_arabic_to_surface("هل تريد الخروج من اللعبة؟", self.ARABIC_FONT_PATH, 60, color=(0, 0, 0))
        msg_rect = msg_surf.get_rect(center=(self.W//2, self.H//2 - 50))
        self.screen.blit(msg_surf, msg_rect)
        
        btn_w, btn_h = 200, 80
        yes_rect = pygame.Rect(self.W//2 - 220, self.H//2 + 40, btn_w, btn_h)
        no_rect = pygame.Rect(self.W//2 + 20, self.H//2 + 40, btn_w, btn_h)
        
        pygame.draw.rect(self.screen, (200, 50, 50), yes_rect, border_radius=15)
        pygame.draw.rect(self.screen, (50, 150, 50), no_rect, border_radius=15)
        
        yes_text = render_arabic_to_surface("نعم", self.ARABIC_FONT_PATH, 50, color=(255, 255, 255))
        no_text = render_arabic_to_surface("لا", self.ARABIC_FONT_PATH, 50, color=(255, 255, 255))
        
        self.screen.blit(yes_text, yes_text.get_rect(center=yes_rect.center))
        self.screen.blit(no_text, no_text.get_rect(center=no_rect.center))
        
        self.exit_confirm_rects = {"yes": yes_rect, "no": no_rect}
    
    def draw(self):
        """Main draw method."""
        # Background
        if self.state == "playing":
            self.screen.fill((255, 255, 255))
            if self.question_bg:
                self.screen.blit(self.question_bg, (0, 0))
        else:
            if self.bg:
                self.screen.blit(self.bg, (0, 0))
        
        # Draw based on state
        if self.state == "menu":
            self.update_menu_hover()
            self.draw_menu()
        elif self.state == "playing":
            self.draw_playing()
        elif self.state == "feedback":
            self.draw_feedback()
        elif self.state == "results":
            self.draw_results()
        
        # Exit button
        if self.exit_img:
            self.screen.blit(self.exit_img, self.exit_rect.topleft)
        
        # Exit confirmation
        if self.show_exit_confirm:
            self.draw_exit_confirm()
        
        pygame.display.flip()
    
    def handle_events(self):
        """Handle pygame events."""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_exit_confirm:
                    if self.exit_confirm_rects.get("yes", pygame.Rect(0,0,0,0)).collidepoint(event.pos):
                        self.running = False
                        return
                    elif self.exit_confirm_rects.get("no", pygame.Rect(0,0,0,0)).collidepoint(event.pos):
                        self.show_exit_confirm = False
                
                elif self.exit_rect and self.exit_rect.collidepoint(event.pos):
                    self.show_exit_confirm = True
                
                elif self.state == "menu":
                    for key, rect in self.menu_rects.items():
                        if rect.collidepoint(event.pos):
                            self.select_difficulty(key)
                
                elif self.state == "playing":
                    for i, rect in enumerate(getattr(self, "option_rects", [])):
                        if rect.collidepoint(event.pos):
                            self.check_answer(i)
                            break
                
                elif self.state == "feedback":
                    if self.current_feedback_sound:
                        self.current_feedback_sound.stop()
                        self.current_feedback_sound = None
                    
                    self.feedback_until = 0
                    self.current_idx += 1
                    self.unload_current_question_assets()
                    self.selected_options = set()
                    
                    if self.current_idx >= len(self.questions):
                        self.state = "results"
                    else:
                        self.state = "playing"
                        self.play_current_question_sound()
                    
                    self.feedback_correct = False
                    self.current_feedback_img = None
                
                elif self.state == "results":
                    if "play_again" in self.results_buttons and self.results_buttons["play_again"].collidepoint(event.pos):
                        self.stop_all_sounds()
                        self.score = 0
                        self.current_idx = 0
                        self.feedback_correct = False
                        self.current_feedback_img = None
                        self.feedback_until = 0
                        self.current_feedback_sound = None
                        self.selected_difficulty = None
                        self.state = "menu"
            
            elif event.type == pygame.USEREVENT + 4:
                if self.state == "playing" and self.current_replay < self.question_replay_count:
                    self.play_current_question_sound(first_play=False)
                    self.current_replay += 1
                else:
                    pygame.time.set_timer(pygame.USEREVENT + 4, 0)
        
        # Exit button hover
        exit_hovered = self.exit_rect.collidepoint(mouse_pos)
        if exit_hovered and not self.exit_hovered_last:
            self.stop_hover_only()
            if self.exit_hover_sound:
                self.exit_hover_sound.play()
        self.exit_hovered_last = exit_hovered
        
        # Feedback timer
        if self.state == "feedback" and self.feedback_until > 0:
            if pygame.time.get_ticks() >= self.feedback_until:
                if self.current_feedback_sound:
                    self.current_feedback_sound.stop()
                    self.current_feedback_sound = None
                
                self.current_idx += 1
                self.unload_current_question_assets()
                self.selected_options = set()
                
                if self.current_idx >= len(self.questions):
                    self.state = "results"
                else:
                    self.state = "playing"
                    self.play_current_question_sound()
                
                self.feedback_until = 0
                self.feedback_correct = False
                self.current_feedback_img = None
    
    def run(self):
        """Main game loop."""
        # Auto-select difficulty if specified
        if self.auto_difficulty:
            # Build question list for the auto-selected difficulty
            qs = self.build_question_list(self.auto_difficulty)
            if qs:
                self.questions = qs
                self.current_idx = 0
                self.selected_options = set()
                self.score = 0
                # Play first question sound after a short delay
                pygame.time.set_timer(pygame.USEREVENT+3, 300, True)
                self.play_current_question_sound()
            else:
                print(f"⚠️ No questions for auto-difficulty: {self.auto_difficulty}")
                self.state = "menu"  # Fall back to menu if no questions
        
        while self.running:
            self.draw()
            self.handle_events()
            self.clock.tick(60)
        
        # Cleanup
        self.stop_all_sounds()
        
        # Return to quiz topics (not learning topics when coming from quiz menu)
        from quiz_topics import run_quiz_topics
        run_quiz_topics(self.screen, self.main_app, level=self.level)
