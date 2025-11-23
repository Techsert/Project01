# quiz_base.py - COMPLETE OPTIMIZED VERSION with threaded loading
import pygame
import sys
import os
import random
import time
import threading
from PIL import Image, ImageFont, ImageDraw
import config
from screen_helpers import confirm_popup as general_confirm_popup

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
# LOADING SCREEN
# ==========================================================
class LoadingScreen:
    """Display animated loading screen while assets load."""
    
    def __init__(self, screen):
        self.screen = screen
        self.W, self.H = screen.get_size()
        self.progress = 0
        self.max_progress = 100
        self.message = "Loading..."
        self.running = True
        self.clock = pygame.time.Clock()
        
        # Animation
        self.spinner_angle = 0
        self.pulse_alpha = 255
        self.pulse_direction = -5
    
    def set_progress(self, value, message=""):
        """Update progress bar."""
        self.progress = min(value, self.max_progress)
        if message:
            self.message = message
    
    def draw(self):
        """Draw loading screen."""
        self.screen.fill((30, 30, 40))
        
        # Title
        try:
            font = pygame.font.Font(None, 72)
            title = font.render("Loading Quiz...", True, (255, 255, 255))
            self.screen.blit(title, title.get_rect(center=(self.W//2, self.H//3)))
        except:
            pass
        
        # Progress bar
        bar_w = int(self.W * 0.6)
        bar_h = 40
        bar_x = (self.W - bar_w) // 2
        bar_y = self.H // 2
        
        # Background
        pygame.draw.rect(self.screen, (60, 60, 70), (bar_x, bar_y, bar_w, bar_h), border_radius=20)
        
        # Progress fill
        fill_w = int((self.progress / self.max_progress) * bar_w)
        if fill_w > 0:
            pygame.draw.rect(self.screen, (0, 200, 100), (bar_x, bar_y, fill_w, bar_h), border_radius=20)
        
        # Border
        pygame.draw.rect(self.screen, (100, 100, 110), (bar_x, bar_y, bar_w, bar_h), 3, border_radius=20)
        
        # Percentage
        try:
            font = pygame.font.Font(None, 36)
            percent_text = font.render(f"{int(self.progress)}%", True, (255, 255, 255))
            self.screen.blit(percent_text, percent_text.get_rect(center=(self.W//2, bar_y + bar_h + 30)))
        except:
            pass
        
        # Status message
        try:
            font = pygame.font.Font(None, 32)
            msg = font.render(self.message, True, (200, 200, 200))
            self.screen.blit(msg, msg.get_rect(center=(self.W//2, bar_y + bar_h + 70)))
        except:
            pass
        
        # Spinner (if progress < 100)
        if self.progress < 100:
            spinner_radius = 30
            center = (self.W//2, self.H - 100)
            
            # Draw rotating arc
            for i in range(8):
                angle = self.spinner_angle + (i * 45)
                rad = pygame.math.Vector2()
                rad.from_polar((spinner_radius, angle))
                alpha = int(255 * (i / 8))
                color = (alpha, alpha, 255)
                pygame.draw.circle(self.screen, color, 
                                 (int(center[0] + rad.x), int(center[1] + rad.y)), 5)
            
            self.spinner_angle += 10
        
        pygame.display.flip()
    
    def update(self):
        """Update animation and handle events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
        
        self.draw()
        self.clock.tick(60)

# ==========================================================
# BASE QUIZ PLAYER CLASS
# ==========================================================
class QuizPlayer:
    """
    Base class for quiz presentations with optimized loading.
    """
    
    def __init__(self, screen, main_app, questions, level=1, 
                 img_path=None, sound_path=None, fonts_path=None, 
                 auto_difficulty=None, quiz_level=None):
        """Initialize quiz player."""
        self.screen = screen
        self.main_app = main_app
        self.all_questions = questions
        self.level = level
        self.quiz_level = quiz_level or level
        self.auto_difficulty = auto_difficulty
        
        # Paths
        self.IMG_PATH = img_path or os.path.join(config.ASSETS_PATH, "img/alphabitSound/letters")
        self.SOUND_PATH = sound_path or os.path.join(config.ASSETS_PATH, "sounds/alphabitSound")
        self.FONTS_PATH = fonts_path or os.path.join(config.ASSETS_PATH, "fonts")
        
        # Screen setup
        self.W, self.H = screen.get_size()
        self.clock = pygame.time.Clock()
        
        # Find Arabic font
        self.ARABIC_FONT_PATH = self.find_arabic_font()
        self.font_loader = lambda size, bold=False: pygame.font.Font(
            config.ARABIC_FONT_BOLD if bold else config.ARABIC_FONT_REGULAR, size
        )
        
        # Audio volumes
        self.volume_hover = 0.8
        self.volume_questions = 1.0
        self.volume_feedback = 1.0
        
        # Game state
        self.state = "menu" if not auto_difficulty else "loading"
        self.selected_difficulty = auto_difficulty
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
        
        # ✅ Asset loading
        self.assets_loaded = False
        self.loading_thread = None
        self.loading_screen = None
        
        self.running = True
        
        # ✅ Start background asset loading
        print("🎮 Starting quiz initialization...")
        self.start_background_loading()
    
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
    
    # ==========================================================
    # OPTIMIZED ASSET LOADING
    # ==========================================================
    def start_background_loading(self):
        """Start loading assets in background thread."""
        if self.auto_difficulty:
            # Pre-load for auto-difficulty
            self.loading_screen = LoadingScreen(self.screen)
            self.loading_thread = threading.Thread(target=self.load_all_assets_threaded, daemon=True)
            self.loading_thread.start()
        else:
            # Load minimal assets for menu
            self.load_menu_assets()
    
    def load_menu_assets(self):
        """Load only assets needed for menu screen (fast)."""
        print("📦 Loading menu assets...")
        
        # Load hover sounds (small files)
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
        
        # Load backgrounds (compress if needed)
        self.bg = load_image(os.path.join(self.IMG_PATH, "soccerfield.png"), alpha=False)
        if self.bg:
            self.bg = pygame.transform.smoothscale(self.bg, (self.W, self.H))
        
        # Load difficulty icons
        self.load_difficulty_icons()
        
        # Load exit button
        self.setup_exit_button()
        
        print("✅ Menu assets loaded")
    
    def load_all_assets_threaded(self):
        """Load all assets in background thread with progress updates."""
        try:
            total_steps = 7
            current_step = 0
            
            # Step 1: Build question list
            current_step += 1
            self.loading_screen.set_progress((current_step/total_steps)*100, "Preparing questions...")
            self.questions = self.build_question_list(self.auto_difficulty)
            
            # Step 2: Load backgrounds
            current_step += 1
            self.loading_screen.set_progress((current_step/total_steps)*100, "Loading backgrounds...")
            self.bg = load_image(os.path.join(self.IMG_PATH, "soccerfield.png"), alpha=False)
            if self.bg:
                self.bg = pygame.transform.smoothscale(self.bg, (self.W, self.H))
            
            self.question_bg = load_image(os.path.join(self.IMG_PATH, "quiz_bg.png"), alpha=False)
            if self.question_bg:
                self.question_bg = pygame.transform.smoothscale(self.question_bg, (self.W, self.H))
            
            # Step 3: Load feedback icons
            current_step += 1
            self.loading_screen.set_progress((current_step/total_steps)*100, "Loading feedback icons...")
            self.goal_icon = load_image(os.path.join(self.IMG_PATH, "football_goal.png"))
            if self.goal_icon:
                self.goal_icon = pygame.transform.smoothscale(self.goal_icon, (60, 60))
            
            self.miss_icon = load_image(os.path.join(self.IMG_PATH, "football_miss.png"))
            if self.miss_icon:
                self.miss_icon = pygame.transform.smoothscale(self.miss_icon, (60, 60))
            
            # Step 4: Load feedback assets
            current_step += 1
            self.loading_screen.set_progress((current_step/total_steps)*100, "Loading feedback...")
            self.load_feedback_assets()
            
            # Step 5: Load hover sounds
            current_step += 1
            self.loading_screen.set_progress((current_step/total_steps)*100, "Loading sounds...")
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
            
            # Step 6: Setup exit button
            current_step += 1
            self.loading_screen.set_progress((current_step/total_steps)*100, "Finalizing...")
            self.setup_exit_button()
            
            # Step 7: Complete
            current_step += 1
            self.loading_screen.set_progress(100, "Ready!")
            time.sleep(0.3)  # Brief pause to show 100%
            
            self.assets_loaded = True
            print("✅ All assets loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading assets: {e}")
            self.assets_loaded = True  # Allow fallback to continue
    
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
            size = int(self.W * 0.07)
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(surf, (200, 0, 0, 220), (size//2, size//2), size//2)
            self.exit_img = surf
            self.exit_rect = self.exit_img.get_rect(topleft=(20, 20))
        
        self.exit_hover_sound = load_sound(os.path.join(self.SOUND_PATH, "hover_exit.wav"))
        if self.exit_hover_sound:
            self.exit_hover_sound.set_volume(1.0)
        self.exit_hovered_last = False
    
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
        
        # Show loading screen
        self.state = "loading"
        self.loading_screen = LoadingScreen(self.screen)
        
        # Start loading in background
        self.loading_thread = threading.Thread(target=self.load_difficulty_assets, args=(level,), daemon=True)
        self.loading_thread.start()
    
    def load_difficulty_assets(self, level):
        """Load assets for selected difficulty."""
        try:
            qs = self.build_question_list(level)
            
            if not qs:
                print(f"⚠️ No questions for: {level}")
                return
            
            self.questions = qs
            self.loading_screen.set_progress(10, "Loading questions...")
            
            # ✅ FIX 1: Load main background if not already loaded
            if not hasattr(self, 'bg'):
                self.loading_screen.set_progress(20, "Loading backgrounds...")
                self.bg = load_image(os.path.join(self.IMG_PATH, "soccerfield.png"), alpha=False)
                if self.bg:
                    self.bg = pygame.transform.smoothscale(self.bg, (self.W, self.H))
            
            # ✅ FIX 2: Load question background if not already loaded
            if not hasattr(self, 'question_bg'):
                self.question_bg = load_image(os.path.join(self.IMG_PATH, "quiz_bg.png"), alpha=False)
                if self.question_bg:
                    self.question_bg = pygame.transform.smoothscale(self.question_bg, (self.W, self.H))
            
            # ✅ FIX 3: Load goal/miss icons if not already loaded
            if not hasattr(self, 'goal_icon'):
                self.loading_screen.set_progress(40, "Loading icons...")
                self.goal_icon = load_image(os.path.join(self.IMG_PATH, "football_goal.png"))
                if self.goal_icon:
                    self.goal_icon = pygame.transform.smoothscale(self.goal_icon, (60, 60))
                
                self.miss_icon = load_image(os.path.join(self.IMG_PATH, "football_miss.png"))
                if self.miss_icon:
                    self.miss_icon = pygame.transform.smoothscale(self.miss_icon, (60, 60))
            
            # ✅ FIX 4: Load feedback assets if not loaded
            if not hasattr(self, 'correct_feedback_imgs'):
                self.loading_screen.set_progress(60, "Loading feedback...")
                self.load_feedback_assets()
            
            # ✅ FIX 5: Load hover sounds if not loaded (used in menu after replay)
            if not hasattr(self, 'hover_sounds') or not self.hover_sounds:
                self.loading_screen.set_progress(80, "Loading sounds...")
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
            
            # ✅ FIX 6: Ensure exit button assets are loaded
            if not hasattr(self, 'exit_img') or not hasattr(self, 'exit_rect'):
                self.setup_exit_button()
            
            self.loading_screen.set_progress(100, "Ready!")
            time.sleep(0.3)
            
            self.current_idx = 0
            self.selected_options = set()
            self.score = 0
            self.assets_loaded = True
            
            pygame.time.set_timer(pygame.USEREVENT+3, 300, True)
            
        except Exception as e:
            print(f"❌ Error loading difficulty assets: {e}")
            import traceback
            traceback.print_exc()
            self.assets_loaded = True
    
    def play_current_question_sound(self, first_play=True):
        """Play current question's sound."""
        if not (0 <= self.current_idx < len(self.questions)):
            return
        
        if self.current_question_sound:
            self.current_question_sound.stop()
            self.current_question_sound = None
        
        s = self.questions[self.current_idx].get("sound")
        if not s:
            return
        
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
            
            if idx in self.selected_options:
                self.selected_options.remove(idx)
            else:
                self.selected_options.add(idx)
            
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
        """Draw the current question (implemented by subclass)."""
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
        dark = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        dark.fill((0, 0, 0, 160))
        self.screen.blit(dark, (0, 0))
        
        correct = self.score
        wrong = len(self.questions) - self.score
        
        title = render_arabic_to_surface("نتيجة المباراة", self.ARABIC_FONT_PATH, 64, color=(255, 255, 255), bold=True)
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
        
        txt_correct = render_arabic_to_surface(str(correct), "arial", 500, color=(0, 255, 0))
        txt_wrong = render_arabic_to_surface(str(wrong), "arial", 500, color=(255, 0, 0))
        
        x_center = self.W // 2
        y_numeric = int(self.H * 0.20)
        
        self.screen.blit(txt_correct, txt_correct.get_rect(center=(x_center - int(self.W * 0.1), y_numeric)))
        self.screen.blit(txt_wrong, txt_wrong.get_rect(center=(x_center + int(self.W * 0.1), y_numeric)))
        
        button_w, button_h = 300, 80
        x_button = self.W // 2 - button_w // 2
        y_button = int(self.H * 0.8)
        pygame.draw.rect(self.screen, (255, 215, 0), (x_button, y_button, button_w, button_h), border_radius=20)
        txt_play = render_arabic_to_surface("العب مرة أخرى", self.ARABIC_FONT_PATH, 40, color=(0, 0, 0), bold=True)
        self.screen.blit(txt_play, txt_play.get_rect(center=(x_button + button_w // 2, y_button + button_h // 2)))
        
        self.results_buttons["play_again"] = pygame.Rect(x_button, y_button, button_w, button_h)
    
    def draw_loading(self):
        """Draw loading screen."""
        if self.loading_screen:
            self.loading_screen.update()
    
    def draw(self):
        """Main draw method."""
        # Loading state
        if self.state == "loading":
            self.draw_loading()
            return
        
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
        if self.exit_img and self.state != "loading":
            self.screen.blit(self.exit_img, self.exit_rect.topleft)
        
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
                    pygame.event.clear()
                    return
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "loading":
                    continue  # Ignore clicks during loading
                
                if self.exit_rect and self.exit_rect.collidepoint(event.pos):
                    if general_confirm_popup(self.screen, "Exit the Quiz?", self.font_loader):
                        self.running = False
                        return
                
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
        if self.state != "loading":
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
        """Main game loop with loading state management."""
        print("🎮 Starting quiz...")
        
        # If auto-difficulty, wait for assets to load
        if self.auto_difficulty:
            while not self.assets_loaded and self.running:
                self.draw_loading()
                self.handle_events()
                self.clock.tick(60)
            
            # Transition to playing
            if self.assets_loaded and self.running:
                self.state = "playing"
                pygame.time.set_timer(pygame.USEREVENT+3, 300, True)
                self.play_current_question_sound()
        
        # Main game loop
        while self.running:
            # Check if loading is complete
            if self.state == "loading" and self.assets_loaded:
                self.state = "playing"
                self.play_current_question_sound()
            
            self.draw()
            self.handle_events()
            self.clock.tick(60)
        
        # Cleanup
        self.stop_all_sounds()
        
        quiz_level = getattr(self, 'quiz_level', self.level)
        
        from quiz_topics import run_quiz_topics
        run_quiz_topics(self.screen, self.main_app, level=quiz_level)
        
