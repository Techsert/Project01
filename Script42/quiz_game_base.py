# quiz_game_base.py - BASE CLASS FOR ALL QUIZ GAMES
# Eliminates code duplication between quiz_lvl1, quiz_lvl2, quiz_lvl3

import os
import random
import pygame
from audio_manager import AudioManager
from PIL import Image, ImageFont, ImageDraw

# Optional Arabic shaping libraries
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_BIDI = True
except Exception:
    HAS_BIDI = False
    print("⚠️ Missing 'arabic_reshaper' and/or 'python-bidi'. Arabic shaping may be incorrect.")

# ==========================================================
# PATHS (relative to quiz_game_base.py location)
# ==========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "../assets")
IMG_PATH = os.path.join(ASSET_PATH, "img/alphabitSound/letters")
SOUND_PATH = os.path.join(ASSET_PATH, "sounds/alphabitSound")
FONTS_PATH = os.path.join(ASSET_PATH, "fonts")

PREFERRED_ARABIC_FONTS = [
    os.path.join(FONTS_PATH, "NotoNaskhArabic-Regular.ttf"),
    os.path.join(FONTS_PATH, "arabic.ttf"),
    os.path.join(FONTS_PATH, "NotoSansArabic-Regular.ttf"),
]

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================
def find_arabic_font():
    """Find available Arabic font"""
    for p in PREFERRED_ARABIC_FONTS:
        if os.path.exists(p):
            return p
    try:
        candidate = pygame.font.match_font("arial")
        if candidate:
            return candidate
    except Exception:
        pass
    return None

ARABIC_FONT_PATH = None  # Will be set after pygame.init()

def load_image(path, alpha=True):
    """Load image with error handling"""
    if not os.path.exists(path):
        print(f"⚠️ Missing image: {path}")
        return None
    try:
        surf = pygame.image.load(path).convert_alpha()
        return surf
    except Exception as e:
        print(f"⚠️ Failed to load image {path}: {e}")
        return None

def load_sound(path):
    """Load sound with error handling"""
    if not os.path.exists(path):
        print(f"⚠️ Missing sound: {path}")
        return None
    try:
        return pygame.mixer.Sound(path)
    except Exception as e:
        print(f"⚠️ Failed to load sound {path}: {e}")
        return None

def render_arabic_to_surface(text, font_path, size, color=(255,255,255), bold=False, italic=False):
    """Render Arabic text properly shaped"""
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
        f.set_italic(italic)
        surf = f.render(text, True, color)
        return surf.convert_alpha()
    except Exception as e:
        print("⚠️ Fallback rendering failed:", e)
        return pygame.Surface((1,1), pygame.SRCALPHA)

# ==========================================================
# BASE QUIZ GAME CLASS
# ==========================================================
class QuizGameBase:
    """
    Base class for all quiz games.
    Eliminates duplication between quiz_lvl1, quiz_lvl2, quiz_lvl3.
    """
    
    def __init__(self, level=1, difficulty="easy"):
        """Initialize quiz game."""
        import time
        start = time.time()
        # Don't initialize pygame here - already done in main
        
        self.level = level
        self.difficulty = difficulty
        
        # ✅ Use AudioManager
        self.audio_manager = None  # Will be set by run_quiz_lvl* functions
        
        # Game state
        self.state = "intro"
        self.intro_sound_playing = False
        self.intro_delay = 8000
        self.last_hovered = None
        self.questions = []
        self.current_idx = 0
        self.selected_options = set()
        self.score = 0
        self.feedback_until = 0
        self.feedback_correct = False
        self.current_feedback_sound = None
        self.start_button_rect = None
        self.results_buttons = {}
        self.last_hover_id = None
        
        # Profile (will be set by wrapper function)
        self.current_profile = None
        self.profiles = {}
        
        # Sound replay
        self.question_replay_count = 5
        self.question_replay_interval = 10000
        self.current_replay = 0
        
        # Screen setup
        self.screen = None
        self.W = 0
        self.H = 0
        
        # ✅ Fonts - find once
        global ARABIC_FONT_PATH
        if ARABIC_FONT_PATH is None:
            ARABIC_FONT_PATH = find_arabic_font()
        
        # ✅ Progress text caching
        self._cached_progress_text = None
        self._last_progress_idx = -1
        
        # Load assets
        self._load_sounds()
        self._load_backgrounds()
        self._load_start_button()
        self._load_feedback_assets()
        self._load_exit_button()
        
        self.clock = pygame.time.Clock()
        self.loaded_sounds = {}
        
        # Exit confirmation
        self.show_exit_confirm = False
        self.exit_confirm_rects = {}

        print(f"⏱️ Quiz init took {time.time() - start:.2f}s")
    
    def _load_sounds(self):
        """Load intro sound and hover sound - using AudioManager"""
        # Store paths instead of loading directly
        self.intro_sound_path = os.path.join(SOUND_PATH, "WelcIntro.wav")
        self.hover_sound_path = os.path.join(SOUND_PATH, "hover_easy.wav")
        self.exit_hover_sound_path = os.path.join(SOUND_PATH, "hover_exit.wav")
        self.exit_hovered_last = False
        
        # Background music path
        self.bg_music_path = os.path.join(SOUND_PATH, "bg_music.mp3")
        if not os.path.exists(self.bg_music_path):
            self.bg_music_path = None
        self.intro_music_playing = False
    
    def _load_backgrounds(self):
        """Load background images - optimized for faster startup"""
        # Main background (needed immediately for intro)
        bg_path = os.path.join(IMG_PATH, "soccerfield.png")
        self.bg = load_image(bg_path, alpha=False)
        if self.bg:
            self.bg = pygame.transform.smoothscale(self.bg, (self.W, self.H))
        else:
            self.bg_color = (20,120,20)
        
        # Store paths for lazy loading
        self.question_bg_path = os.path.join(IMG_PATH, "quiz_bg.png")
        self.goal_icon_path = os.path.join(IMG_PATH, "football_goal.png")
        self.miss_icon_path = os.path.join(IMG_PATH, "football_miss.png")
        
        # Will be loaded when needed
        self.question_bg = None
        self.goal_icon = None
        self.miss_icon = None
    
    def _load_start_button(self):
        """Load difficulty-specific start button"""
        start_img_path = os.path.join(IMG_PATH, f"{self.difficulty}.png")
        self.start_img = load_image(start_img_path, alpha=True)
        if self.start_img:
            max_h = int(self.H * 0.6)
            scale = max_h / self.start_img.get_height()
            w = int(self.start_img.get_width() * scale * 0.8)
            h = int(max_h * 0.9)
            self.start_img = pygame.transform.smoothscale(self.start_img, (w, h))
        else:
            # Fallback
            self.start_img = pygame.Surface((int(self.W*0.15), int(self.H*0.5)), pygame.SRCALPHA)
            self.start_img.fill((200,200,200,255))
        
        self.start_scale = 1.0
        self.start_target_scale = 1.0
    
    def _load_feedback_assets(self):
        """Prepare feedback asset paths for lazy loading"""
        # Don't load images/sounds yet - just store paths
        self.correct_feedback_paths = [
            os.path.join(IMG_PATH, f"thumbsup{i if i else ''}.png")
            for i in ['', '1', '2', '3', '4', '5', '6']
        ]
        
        self.wrong_feedback_paths = [
            os.path.join(IMG_PATH, f"thumbsdown{i if i else ''}.png")
            for i in ['', '1', '2', '3', '4', '5', '6']
        ]
        
        self.correct_sound_paths = [
            os.path.join(SOUND_PATH, f"correct{i if i else ''}.wav")
            for i in ['', '1', '2', '3', '4', '5']
        ]
        
        self.wrong_sound_paths = [
            os.path.join(SOUND_PATH, f"wrong{i if i else ''}.wav")
            for i in ['', '1', '2', '3', '4', '5']
        ]
        
        # Cache for loaded assets
        self._feedback_cache = {}

    def _get_feedback_image(self, is_correct):
        """Lazy load feedback image only when needed"""
        import random
        paths = self.correct_feedback_paths if is_correct else self.wrong_feedback_paths
        path = random.choice(paths)
        
        # Check cache first
        if path not in self._feedback_cache:
            img = load_image(path)
            if img:
                self._feedback_cache[path] = img
        
        return self._feedback_cache.get(path)

    def _get_feedback_sound(self, is_correct):
        """Lazy load feedback sound only when needed"""
        import random
        paths = self.correct_sound_paths if is_correct else self.wrong_sound_paths
        path = random.choice(paths)
        
        # Check cache first
        if path not in self._feedback_cache:
            snd = load_sound(path)
            if snd:
                self._feedback_cache[path] = snd
        
        return self._feedback_cache.get(path)
    
    def _load_exit_button(self):
        """Load exit button"""
        exit_img_path = os.path.join(IMG_PATH, "exitball.png")
        self.exit_img = load_image(exit_img_path, alpha=True)
        if self.exit_img:
            size = int(self.W * 0.07)
            self.exit_img = pygame.transform.smoothscale(self.exit_img, (size, size))
            self.exit_rect = self.exit_img.get_rect(center=(self.W // 2, self.H - 80))
        else:
            # Fallback
            size = int(self.W * 0.07)
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(surf, (200, 0, 0, 220), (size//2, size//2), size//2)
            self.exit_img = surf
            self.exit_rect = self.exit_img.get_rect(topleft=(20, 20))
    
    # ==========================================================
    # AUDIO METHODS
    # ==========================================================
    def stop_all_sounds(self):
        """Stop all audio using AudioManager"""
        if self.audio_manager:
            self.audio_manager.stop_all_sounds()
        # Fallback to pygame.mixer if audio_manager not available
        else:
            pygame.mixer.music.stop()
            for s in self.loaded_sounds.values():
                s.stop()
    
    def stop_hover_only(self):
        """Stop only hover sounds"""
        # Hover sounds are on dedicated channel in AudioManager
        # No need to stop explicitly - new hover will override
        pass
    
    def play_sfx(self, name):
        """Play sound effect using AudioManager"""
        sound_path = os.path.join(SOUND_PATH, name)
        if self.audio_manager and os.path.exists(sound_path):
            self.audio_manager.play_sound(sound_path, audio_type='sound_effect')
        else:
            # Fallback to old method if audio_manager not available
            if name not in self.loaded_sounds:
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
    
    # ==========================================================
    # QUESTION MANAGEMENT
    # ==========================================================
    def get_questions(self):
        """Override this method in subclass to return questions list"""
        raise NotImplementedError("Subclass must implement get_questions()")
    
    def build_question_list(self):
        """Shuffle questions"""
        qs = [q.copy() for q in self.get_questions()]
        random.shuffle(qs)
        return qs
    
    def start_quiz(self):
        """Start the quiz"""
        self.stop_all_sounds()
        
        # Clear feedback cache from previous runs
        self._feedback_cache.clear()
        
        # ✅ Lazy load question background now
        if self.question_bg is None and os.path.exists(self.question_bg_path):
            img = load_image(self.question_bg_path, alpha=False)
            if img:
                self.question_bg = pygame.transform.smoothscale(img, (self.W, self.H))
        
        qs = self.build_question_list()
        if not qs:
            print("⚠️ No questions available")
            return
        self.questions = qs
        self.current_idx = 0
        self._cached_progress_text = None
        self._last_progress_idx = -1       
        self.selected_options = set()
        self.score = 0
        self.state = "playing"
        pygame.time.set_timer(pygame.USEREVENT+3, 300, True)
        self.play_current_question_sound()
    
    def play_current_question_sound(self, first_play=True):
        """Play question audio using AudioManager"""
        if not (0 <= self.current_idx < len(self.questions)):
            return
        
        if hasattr(self, "current_question_sound") and self.current_question_sound:
            self.current_question_sound.stop()
            self.current_question_sound = None
        
        s = self.questions[self.current_idx].get("sound")
        if not s:
            return
        
        # ✅ Stop hover sounds using AudioManager
        self.stop_hover_only()
        
        sound_path = os.path.join(SOUND_PATH, s)
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
        
        if first_play:
            self.current_replay = 1
            pygame.time.set_timer(pygame.USEREVENT + 4, self.question_replay_interval)
    
    def unload_current_question_assets(self):
        """Free memory"""
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
        """Check if answer is correct"""
        if not (0 <= self.current_idx < len(self.questions)):
            return
        
        q = self.questions[self.current_idx]
        correct_field = q.get("answer", 0)
        
        # Multi-answer
        if isinstance(correct_field, (list, tuple)):
            correct_set = set(correct_field)
            
            if idx in self.selected_options:
                self.selected_options.remove(idx)
            else:
                self.selected_options.add(idx)
            
            if idx not in correct_set:
                self.stop_all_sounds()
                if hasattr(self, "current_question_sound") and self.current_question_sound:
                    self.current_question_sound.stop()
                    self.current_question_sound = None
                
                self.feedback_correct = False
                self.current_feedback_img = self._get_feedback_image(False)
                snd = self._get_feedback_sound(False)
                self.current_feedback_sound = snd
                if snd:
                    snd.stop()
                    snd.play()
                self.feedback_until = pygame.time.get_ticks() + 4000
                self.state = "feedback"
                return
            
            if self.selected_options >= correct_set and set(correct_set) <= self.selected_options:
                self.stop_all_sounds()
                if hasattr(self, "current_question_sound") and self.current_question_sound:
                    self.current_question_sound.stop()
                    self.current_question_sound = None
                
                self.feedback_correct = True
                self.score += 1
                self.current_feedback_img = self._get_feedback_image(True)
                snd = self._get_feedback_sound(True)
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
            if hasattr(self, "current_question_sound") and self.current_question_sound:
                self.current_question_sound.stop()
                self.current_question_sound = None
            
            self.feedback_correct = (idx == correct_field)
            if self.feedback_correct:
                self.score += 1
                self.current_feedback_img = self._get_feedback_image(True)
                snd = self._get_feedback_sound(True)
            else:
                self.current_feedback_img = self._get_feedback_image(False)
                snd = self._get_feedback_sound(False)
            
            self.current_feedback_sound = snd
            if snd:
                snd.stop()
                snd.play()
            
            self.feedback_until = pygame.time.get_ticks() + 4000
            self.state = "feedback"
    
    # ==========================================================
    # DRAWING METHODS
    # ==========================================================
    def update_menu_hover(self):
        """Handle menu button hover"""
        mouse_pos = pygame.mouse.get_pos()
        if self.start_button_rect and self.start_button_rect.collidepoint(mouse_pos):
            self.start_target_scale = 1.08
            if not self.last_hovered:
                self.stop_hover_only()
                if self.audio_manager and os.path.exists(self.hover_sound_path):
                    self.audio_manager.play_hover_sound(self.hover_sound_path)
                self.last_hovered = True
            try:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            except:
                pass
        else:
            self.start_target_scale = 1.0
            self.last_hovered = False
            try:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            except:
                pass
        
        self.start_scale += (self.start_target_scale - self.start_scale) * 0.18
    
    def draw_menu(self):
        """Draw menu screen"""
        BOLD_ARABIC_FONT = os.path.join(FONTS_PATH, "NotoNaskhArabic-Bold.ttf")
        title_surf = render_arabic_to_surface("ابدأ اللعبة", BOLD_ARABIC_FONT, 80, color=(0, 0, 0), bold=True, italic=True)
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.W//2, int(self.H*0.15))))
        
        # Draw centered start button
        ow, oh = self.start_img.get_size()
        sw = int(ow * self.start_scale)
        sh = int(oh * self.start_scale)
        cx, cy = self.W // 2, int(self.H * 0.55)
        surf = pygame.transform.smoothscale(self.start_img, (sw, sh))
        lift = int((self.start_scale - 1.0) * 20)
        pos = (int(cx - sw//2), int(cy - sh//2) - lift)
        self.screen.blit(surf, pos)
        self.start_button_rect = pygame.Rect(pos[0], pos[1], sw, sh)
    
    def draw_playing(self):
        """Draw quiz question"""
        if not (0 <= self.current_idx < len(self.questions)):
            return
        
        q = self.questions[self.current_idx]
        opts = q.get("options", [])
        margin = q.get("margin", 40)
        
        self.option_images = []
        self.option_rects = []
        
        for opt in opts:
            fname = opt.get("file")
            size = opt.get("size", (200, 200))
            path = os.path.join(IMG_PATH, fname)
            img = load_image(path)
            if img:
                surf = pygame.transform.smoothscale(img, size)
            else:
                surf = pygame.Surface(size, pygame.SRCALPHA)
            self.option_images.append(surf)
        
        options = q["options"]
        total_width = sum([opt.get("size", (200, 200))[0] for opt in options]) + (len(options) - 1) * margin
        start_x = (self.W - total_width) // 2
        baseline_y = int(self.H * 0.75)
        
        x = start_x
        for i, opt in enumerate(options):
            img = self.option_images[i]
            w, h = opt.get("size", (200, 200))
            x_off = opt.get("x_offset", 0)
            y_off = opt.get("y_offset", 0)
            rect = img.get_rect(midbottom=(x + w // 2 + x_off, baseline_y + y_off))
            self.screen.blit(img, rect)
            self.option_rects.append(rect)
            
            if hasattr(self, "selected_options") and i in getattr(self, "selected_options", set()):
                pygame.draw.rect(self.screen, (255, 215, 0), rect.inflate(10, 10), 6, border_radius=12)
            x += w + margin
        
        # Progress counter and bar
        current = self.current_idx + 1
        total = len(self.questions)
        
        if self._last_progress_idx != current:
            counter_text = f"Question {current} from {total}"
            self._cached_progress_text = render_arabic_to_surface(
                counter_text, ARABIC_FONT_PATH, 60, color=(255, 255, 255)
            )
            self._last_progress_idx = current
        self.screen.blit(self._cached_progress_text, self._cached_progress_text.get_rect(center=(self.W//2, int(self.H*0.08))))
        
        bar_w = int(self.W * 0.6)
        bar_h = 28
        bar_x = (self.W - bar_w) // 2
        bar_y = int(self.H * 0.12)
        
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=15)
        progress_w = int((current / total) * bar_w)
        pygame.draw.rect(self.screen, (255, 215, 0), (bar_x, bar_y, progress_w, bar_h), border_radius=15)
        
        # Icons
        icon_spacing = bar_w // total
        for i in range(total):
            x = bar_x + i * icon_spacing + icon_spacing // 4
            y = bar_y + bar_h + 10
            
            if i < self.current_idx:
                if i < self.score:
                    if self.goal_icon:
                        self.screen.blit(self.goal_icon, (x, y))
                else:
                    if self.miss_icon:
                        self.screen.blit(self.miss_icon, (x, y))
            else:
                pygame.draw.circle(self.screen, (200, 200, 200), (x + 20, y + 20), 15)
    
    def draw_feedback(self):
        """Draw feedback overlay"""
        dark = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        dark.fill((0,0,0,120))
        self.screen.blit(dark, (0,0))
        
        img = getattr(self, "current_feedback_img", None)
        if img:
            rect = img.get_rect(center=(self.W//2, self.H//2))
            self.screen.blit(img, rect.topleft)
    
    def draw_results(self):
        """Draw results screen"""
        # ✅ Lazy load icons now if needed
        if self.goal_icon is None and os.path.exists(self.goal_icon_path):
            img = load_image(self.goal_icon_path)
            if img:
                self.goal_icon = pygame.transform.smoothscale(img, (60, 60))
        
        if self.miss_icon is None and os.path.exists(self.miss_icon_path):
            img = load_image(self.miss_icon_path)
            if img:
                self.miss_icon = pygame.transform.smoothscale(img, (60, 60))
        dark = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        dark.fill((0, 0, 0, 160))
        self.screen.blit(dark, (0, 0))
        
        correct = self.score
        wrong = len(self.questions) - self.score
        
        title = render_arabic_to_surface("نتيجة المباراة", ARABIC_FONT_PATH or "", 64, color=(255,255,255), bold=True)
        self.screen.blit(title, title.get_rect(center=(self.W // 2, int(self.H * 0.15))))
        
        icon_size = 80
        spacing = 15
        column_height = self.H * 0.55
        icons_per_column = max(1, int(column_height // (icon_size + spacing)))
        
        x_goal_start = int(self.W * 0.02)
        x_miss_start = int(self.W * 0.95)
        
        for i in range(correct):
            col = i // icons_per_column
            row = i % icons_per_column
            x = x_goal_start + col * (icon_size + spacing)
            y = int(self.H * 0.25) + row * (icon_size + spacing)
            if self.goal_icon:
                self.screen.blit(self.goal_icon, (x, y))
        
        for i in range(wrong):
            col = i // icons_per_column
            row = i % icons_per_column
            x = x_miss_start - col * (icon_size + spacing)
            y = int(self.H * 0.25) + row * (icon_size + spacing)
            if self.miss_icon:
                self.screen.blit(self.miss_icon, (x, y))
        
        txt_correct = render_arabic_to_surface(str(correct), "arial" or "", 500, color=(0,255,0))
        txt_wrong = render_arabic_to_surface(str(wrong), "arial" or "", 500, color=(255,0,0))
        
        x_center = self.W // 2
        y_numeric = int(self.H * 0.20)
        
        self.screen.blit(txt_correct, txt_correct.get_rect(center=(x_center - int(self.W * 0.1), y_numeric)))
        self.screen.blit(txt_wrong, txt_wrong.get_rect(center=(x_center + int(self.W * 0.1), y_numeric)))
        
        button_w, button_h = 300, 80
        x_button = self.W // 2 - button_w // 2
        y_button = int(self.H * 0.8)
        pygame.draw.rect(self.screen, (255, 215, 0), (x_button, y_button, button_w, button_h), border_radius=20)
        txt_play = render_arabic_to_surface("العب مرة أخرى", ARABIC_FONT_PATH or "", 40, color=(0, 0, 0), bold=True)
        self.screen.blit(txt_play, txt_play.get_rect(center=(x_button + button_w // 2, y_button + button_h // 2)))
        
        self.results_buttons["play_again"] = pygame.Rect(x_button, y_button, button_w, button_h)
    
    def draw_exit_confirmation(self):
        """Draw exit confirmation popup"""
        overlay = pygame.Surface((self.W, self.H))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        box_w, box_h = 600, 300
        box_rect = pygame.Rect((self.W - box_w)//2, (self.H - box_h)//2, box_w, box_h)
        pygame.draw.rect(self.screen, (255, 255, 255), box_rect, border_radius=20)
        pygame.draw.rect(self.screen, (0, 0, 0), box_rect, 4, border_radius=20)
        
        msg_surf = render_arabic_to_surface("هل تريد الخروج من اللعبة؟", ARABIC_FONT_PATH, 60, color=(0, 0, 0))
        msg_rect = msg_surf.get_rect(center=(self.W//2, self.H//2 - 50))
        self.screen.blit(msg_surf, msg_rect)
        
        btn_w, btn_h = 200, 80
        yes_rect = pygame.Rect(self.W//2 - 220, self.H//2 + 40, btn_w, btn_h)
        no_rect = pygame.Rect(self.W//2 + 20, self.H//2 + 40, btn_w, btn_h)
        
        pygame.draw.rect(self.screen, (200, 50, 50), yes_rect, border_radius=15)
        pygame.draw.rect(self.screen, (50, 150, 50), no_rect, border_radius=15)
        
        yes_text = render_arabic_to_surface("نعم", ARABIC_FONT_PATH, 50, color=(255, 255, 255))
        no_text = render_arabic_to_surface("لا", ARABIC_FONT_PATH, 50, color=(255, 255, 255))
        
        self.screen.blit(yes_text, yes_text.get_rect(center=yes_rect.center))
        self.screen.blit(no_text, no_text.get_rect(center=no_rect.center))
        
        self.exit_confirm_rects = {"yes": yes_rect, "no": no_rect}
    
    def draw(self):
        """Main draw method"""
        # Draw background
        if self.state == "playing":
            self.screen.fill((255, 255, 255))
            if self.question_bg:
                self.screen.blit(self.question_bg, (0, 0))
            else:
                self.screen.fill(self.bg_color)
        else:
            if self.bg:
                self.screen.blit(self.bg, (0,0))
            else:
                self.screen.fill(self.bg_color)
        
        # Draw state-specific content
        if self.state == "intro":
            if not self.intro_sound_playing and self.audio_manager:
                self.audio_manager.play_sound(self.intro_sound_path, audio_type='sound_effect')
                self.intro_sound_playing = True
            if pygame.time.get_ticks() - self.intro_start_time >= self.intro_delay:
                self.show_menu_icons = True
                self.state = "menu"
        
        if self.state == "menu" and getattr(self, "show_menu_icons", False):
            self.update_menu_hover()
            self.draw_menu()
        elif self.state == "playing":
            self.draw_playing()
        elif self.state == "feedback":
            self.draw_feedback()
        elif self.state == "results":
            self.draw_results()
        
        # Draw exit button on top
        if self.exit_img:
            self.screen.blit(self.exit_img, self.exit_rect.topleft)
        
        # Draw exit confirmation if needed
        if self.show_exit_confirm:
            self.draw_exit_confirmation()
        
        pygame.display.flip()
    
    # ==========================================================
    # EVENT HANDLING
    # ==========================================================
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_exit_confirm:
                    if self.exit_confirm_rects.get("yes", pygame.Rect(0,0,0,0)).collidepoint(event.pos):
                        return False
                    elif self.exit_confirm_rects.get("no", pygame.Rect(0,0,0,0)).collidepoint(event.pos):
                        self.show_exit_confirm = False
                
                elif self.exit_rect and self.exit_rect.collidepoint(event.pos):
                    self.show_exit_confirm = True
                
                elif self.state == "menu":
                    if self.start_button_rect and self.start_button_rect.collidepoint(event.pos):
                        self.start_quiz()
                
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
                        
                        self.state = "menu"
                        self.intro_start_time = pygame.time.get_ticks()
                        self.intro_sound_playing = True
                        self.show_menu_icons = True
            
            elif event.type == pygame.USEREVENT + 4:
                if self.state == "playing" and self.current_replay < self.question_replay_count:
                    self.play_current_question_sound(first_play=False)
                    self.current_replay += 1
                else:
                    pygame.time.set_timer(pygame.USEREVENT + 4, 0)
        
        return True
    
    def handle_exit_hover(self):
        """Handle exit button hover sound using AudioManager"""
        mouse_pos = pygame.mouse.get_pos()
        exit_hovered = hasattr(self, 'exit_rect') and self.exit_rect.collidepoint(mouse_pos)
        if exit_hovered and not self.exit_hovered_last:
            self.stop_hover_only()
            if self.audio_manager and os.path.exists(self.exit_hover_sound_path):
                self.audio_manager.play_hover_sound(self.exit_hover_sound_path)
        self.exit_hovered_last = exit_hovered
    
    def handle_feedback_timer(self):
        """Handle feedback auto-advance timer"""
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
    
    # ==========================================================
    # MAIN LOOP
    # ==========================================================
    def run(self):
        """Main game loop"""
        running = True
        self.intro_start_time = pygame.time.get_ticks()
        
        while running:
            self.clock.tick(60)
            
            # Handle events
            running = self.handle_events()
            if not running:
                break
            
            # Handle hover effects
            self.handle_exit_hover()
            
            # Handle feedback timer
            self.handle_feedback_timer()
            
            # Draw everything
            self.draw()
        
        self.stop_all_sounds()
