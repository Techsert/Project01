# practice_base.py - Simple practice questions without scoring
import pygame
import sys
import os
import random
from screen_helpers import confirm_popup, load_font
import config

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_BIDI = True
except Exception:
    HAS_BIDI = False

# ==========================================================
# PATHS
# ==========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "../assets")
IMG_PATH = os.path.join(ASSET_PATH, "img/alphabitSound/letters")
SOUND_PATH = os.path.join(ASSET_PATH, "sounds/alphabitSound")

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================
def load_image(path, alpha=True):
    """Load image with error handling"""
    if not os.path.exists(path):
        print(f"⚠️ Missing image: {path}")
        return None
    try:
        surf = pygame.image.load(path).convert_alpha() if alpha else pygame.image.load(path).convert()
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

# ==========================================================
# PRACTICE BASE CLASS
# ==========================================================
class PracticeBase:
    """
    Base class for practice exercises - NO SCORING, just learning feedback
    """
    
    def __init__(self, level=1):
        """Initialize practice session"""
        self.level = level
        self.audio_manager = None
        self.main_app = None
        self.screen = None
        self.W = 0
        self.H = 0
        
        # State
        self.state = "intro"
        self.questions = []
        self.current_idx = 0
        self.feedback_until = 0
        self.feedback_correct = False
        self.current_feedback_img = None
        self.current_feedback_sound = None
        
        # UI elements
        self.start_button_rect = None
        self.option_rects = []
        self.option_images = []
        self.exit_rect = None
        self.exit_img = None
        
        # Assets
        self.bg = None
        self.question_bg = None
        self.current_question_sound = None
        
        # Timing
        self.clock = pygame.time.Clock()
        self.intro_delay = 3000
        self.intro_start_time = 0
        
        # Sound replay
        self.question_replay_count = 5
        self.question_replay_interval = 10000
        self.current_replay = 0
        
        # Feedback cache
        self._feedback_cache = {}
        
        # Asset paths
        self._init_asset_paths()
    
    def _init_asset_paths(self):
        """Initialize asset paths"""
        self.bg_path = os.path.join(IMG_PATH, "soccerfield.png")
        self.question_bg_path = os.path.join(IMG_PATH, "bg_ft.png")
        self.start_img_path = os.path.join(IMG_PATH, "practice.png")  # New button
        self.exit_img_path = os.path.join(IMG_PATH, "exitball.png")
        
        # Feedback paths
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
    
    def _load_assets(self):
        """Load visual assets"""
        # Background
        self.bg = load_image(self.bg_path, alpha=False)
        if self.bg and self.W > 0 and self.H > 0:
            self.bg = pygame.transform.smoothscale(self.bg, (self.W, self.H))
        
        # Question background
        self.question_bg = load_image(self.question_bg_path, alpha=False)
        if self.question_bg and self.W > 0 and self.H > 0:
            self.question_bg = pygame.transform.smoothscale(self.question_bg, (self.W, self.H))
        
        # Start button
        self.start_img = load_image(self.start_img_path, alpha=True)
        if self.start_img:
            max_h = int(self.H * 0.5)
            scale = max_h / self.start_img.get_height()
            w = int(self.start_img.get_width() * scale * 0.8)
            h = int(max_h * 0.9)
            self.start_img = pygame.transform.smoothscale(self.start_img, (w, h))
        
        # Exit button
        self.exit_img = load_image(self.exit_img_path, alpha=True)
        if self.exit_img:
            size = int(self.W * 0.07)
            self.exit_img = pygame.transform.smoothscale(self.exit_img, (size, size))
            self.exit_rect = self.exit_img.get_rect(center=(self.W // 2, self.H - 80))
    
    def _get_feedback_image(self, is_correct):
        """Lazy load feedback image"""
        paths = self.correct_feedback_paths if is_correct else self.wrong_feedback_paths
        path = random.choice(paths)
        
        if path not in self._feedback_cache:
            img = load_image(path)
            if img:
                self._feedback_cache[path] = img
        
        return self._feedback_cache.get(path)
    
    def _get_feedback_sound(self, is_correct):
        """Lazy load feedback sound"""
        paths = self.correct_sound_paths if is_correct else self.wrong_sound_paths
        path = random.choice(paths)
        
        if path not in self._feedback_cache:
            snd = load_sound(path)
            if snd:
                self._feedback_cache[path] = snd
        
        return self._feedback_cache.get(path)
    
    # ==========================================================
    # AUDIO METHODS
    # ==========================================================
    def stop_all_sounds(self):
        """Stop all audio"""
        if self.audio_manager:
            self.audio_manager.stop_all_sounds()
    
    # ==========================================================
    # QUESTION MANAGEMENT
    # ==========================================================
    def get_questions(self):
        """Override this in subclass"""
        raise NotImplementedError("Subclass must implement get_questions()")
    
    def build_question_list(self):
        """Shuffle questions"""
        qs = [q.copy() for q in self.get_questions()]
        random.shuffle(qs)
        return qs
    
    def start_practice(self):
        """Start the practice session"""
        self.stop_all_sounds()
        self._feedback_cache.clear()
        
        qs = self.build_question_list()
        if not qs:
            print("⚠️ No questions available")
            return
        
        self.questions = qs
        self.current_idx = 0
        self.state = "playing"
        self.play_current_question_sound()
    
    def play_current_question_sound(self, first_play=True):
        """Play question audio"""
        if not (0 <= self.current_idx < len(self.questions)):
            return
        
        if self.current_question_sound:
            self.current_question_sound.stop()
            self.current_question_sound = None
        
        s = self.questions[self.current_idx].get("sound")
        if not s:
            return
        
        sound_path = os.path.join(SOUND_PATH, s)
        if not os.path.exists(sound_path):
            print(f"⚠️ Missing question sound: {sound_path}")
            return
        
        try:
            self.current_question_sound = pygame.mixer.Sound(sound_path)
            self.current_question_sound.play()
        except Exception as e:
            print(f"⚠️ Failed to play question sound: {e}")
            return
        
        if first_play:
            self.current_replay = 1
            pygame.time.set_timer(pygame.USEREVENT + 4, self.question_replay_interval)
    
    def check_answer(self, idx):
        """Check answer and provide feedback - NO SCORING"""
        if not (0 <= self.current_idx < len(self.questions)):
            return
        
        q = self.questions[self.current_idx]
        correct_answer = q.get("answer", 0)
        
        # Check if correct
        is_correct = (idx == correct_answer)
        
        if is_correct:
            # âœ… CORRECT ANSWER: Show feedback overlay and advance
            self.stop_all_sounds()
            if self.current_question_sound:
                self.current_question_sound.stop()
                self.current_question_sound = None
            
            self.feedback_correct = True
            
            # Get feedback assets
            self.current_feedback_img = self._get_feedback_image(True)
            snd = self._get_feedback_sound(True)
            self.current_feedback_sound = snd
            
            if snd:
                snd.stop()
                snd.play()
            
            self.feedback_until = pygame.time.get_ticks() + 3000
            self.state = "feedback"
        else:
            # âŒ WRONG ANSWER: Play custom tryagain sound, let them try again
            tryagain_path = os.path.join(SOUND_PATH, "tryagain.wav")
            if os.path.exists(tryagain_path):
                try:
                    wrong_snd = pygame.mixer.Sound(tryagain_path)
                    # Play on a separate channel so it doesn't interrupt question sound
                    wrong_channel = pygame.mixer.Channel(1)
                    wrong_channel.play(wrong_snd)
                except Exception as e:
                    print(f"âš ï¸ Failed to play tryagain sound: {e}")
            else:
                print(f"âš ï¸ tryagain.wav not found at: {tryagain_path}")
            
            # Stay in "playing" state - no feedback overlay, no advance
    
    # ==========================================================
    # DRAWING METHODS
    # ==========================================================
    def draw_intro(self):
        """Draw intro screen"""
        if self.bg:
            self.screen.blit(self.bg, (0, 0))
        else:
            self.screen.fill((20, 120, 20))
        
        # Title
        try:
            font = pygame.font.Font(config.ARABIC_FONT_BOLD, int(self.H * 0.08))
        except:
            font = pygame.font.SysFont("Arial", int(self.H * 0.08), bold=True)
        
        title = font.render("Practice Time!", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(self.W // 2, int(self.H * 0.15))))
        
        # Profile icon
        if self.main_app and hasattr(self.main_app, 'profile_icon'):
            self.screen.blit(self.main_app.profile_icon, self.main_app.profile_rect)
    
    def draw_menu(self):
        """Draw menu with start button"""
        if self.bg:
            self.screen.blit(self.bg, (0, 0))
        else:
            self.screen.fill((20, 120, 20))
        
        # Title
        try:
            font = pygame.font.Font(config.ARABIC_FONT_BOLD, int(self.H * 0.08))
        except:
            font = pygame.font.SysFont("Arial", int(self.H * 0.08), bold=True)
        
        title = font.render("Let's Practice!", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(self.W // 2, int(self.H * 0.15))))
        
        # Start button
        if self.start_img:
            rect = self.start_img.get_rect(center=(self.W // 2, int(self.H * 0.55)))
            self.screen.blit(self.start_img, rect)
            self.start_button_rect = rect
        
        # Profile icon
        if self.main_app and hasattr(self.main_app, 'profile_icon'):
            self.screen.blit(self.main_app.profile_icon, self.main_app.profile_rect)
    
    def draw_playing(self):
        """Draw practice question"""
        if self.question_bg:
            self.screen.blit(self.question_bg, (0, 0))
        else:
            self.screen.fill((255, 255, 255))
        
        if not (0 <= self.current_idx < len(self.questions)):
            return
        
        q = self.questions[self.current_idx]
        opts = q.get("options", [])
        margin = q.get("margin", 40)
        
        # Load option images
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
        
        # Draw options centered
        total_width = sum([opt.get("size", (200, 200))[0] for opt in opts]) + (len(opts) - 1) * margin
        start_x = (self.W - total_width) // 2
        baseline_y = int(self.H * 0.75)
        
        x = start_x
        for i, opt in enumerate(opts):
            img = self.option_images[i]
            w, h = opt.get("size", (200, 200))
            x_off = opt.get("x_offset", 0)
            y_off = opt.get("y_offset", 0)
            rect = img.get_rect(midbottom=(x + w // 2 + x_off, baseline_y + y_off))
            self.screen.blit(img, rect)
            self.option_rects.append(rect)
            x += w + margin
        
        # Progress text
        try:
            font = pygame.font.Font(config.ARABIC_FONT_REGULAR, int(self.H * 0.06))
        except:
            font = pygame.font.SysFont("Arial", int(self.H * 0.06))
        
        progress_text = f"Question {self.current_idx + 1} of {len(self.questions)}"
        text = font.render(progress_text, True, (20, 120, 20))
        self.screen.blit(text, text.get_rect(center=(self.W // 2, int(self.H * 0.1))))
        
        # Profile icon
        if self.main_app and hasattr(self.main_app, 'profile_icon'):
            self.screen.blit(self.main_app.profile_icon, self.main_app.profile_rect)
    
    def draw_feedback(self):
        """Draw feedback overlay"""
        dark = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        dark.fill((0, 0, 0, 120))
        self.screen.blit(dark, (0, 0))
        
        img = self.current_feedback_img
        if img:
            rect = img.get_rect(center=(self.W // 2, self.H // 2))
            self.screen.blit(img, rect)
    
    def draw_complete(self):
        """Draw completion screen - NO SCORING"""
        if self.bg:
            self.screen.blit(self.bg, (0, 0))
        else:
            self.screen.fill((20, 120, 20))
        
        # Title
        try:
            font = pygame.font.Font(config.ARABIC_FONT_BOLD, int(self.H * 0.08))
        except:
            font = pygame.font.SysFont("Arial", int(self.H * 0.08), bold=True)
        
        title = font.render("Great Practice!", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(self.W // 2, int(self.H * 0.3))))
        
        # Message
        try:
            font = pygame.font.Font(config.ARABIC_FONT_REGULAR, int(self.H * 0.05))
        except:
            font = pygame.font.SysFont("Arial", int(self.H * 0.05))
        
        msg = font.render("Keep practicing to improve!", True, (255, 215, 0))
        self.screen.blit(msg, msg.get_rect(center=(self.W // 2, int(self.H * 0.5))))
        
        # Done button
        btn_rect = pygame.Rect(self.W // 2 - 150, int(self.H * 0.7), 300, 80)
        pygame.draw.rect(self.screen, (255, 215, 0), btn_rect, border_radius=20)
        
        try:
            font = pygame.font.Font(config.ARABIC_FONT_BOLD, int(self.H * 0.04))
        except:
            font = pygame.font.SysFont("Arial", int(self.H * 0.04), bold=True)
        
        done_text = font.render("Done", True, (0, 0, 0))
        self.screen.blit(done_text, done_text.get_rect(center=btn_rect.center))
        
        self.done_rect = btn_rect
        
        # Profile icon
        if self.main_app and hasattr(self.main_app, 'profile_icon'):
            self.screen.blit(self.main_app.profile_icon, self.main_app.profile_rect)
    
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
                # Profile icon click
                if self.main_app and hasattr(self.main_app, 'profile_rect') and self.main_app.profile_rect.collidepoint(event.pos):
                    if self.audio_manager:
                        self.audio_manager.push_audio_context()
                    self.stop_all_sounds()
                    self.main_app.open_profile_manager()
                    if self.audio_manager:
                        self.audio_manager.pop_audio_context(restore=True)
                    continue
                
                # Exit button
                if self.exit_rect and self.exit_rect.collidepoint(event.pos):
                    if confirm_popup(
                        self.screen,
                        "Exit practice?",
                        lambda size, bold=False: load_font(
                            config.ARABIC_FONT_REGULAR,
                            config.ARABIC_FONT_BOLD,
                            size,
                            bold
                        )
                    ):
                        return False
                
                # State-specific clicks
                if self.state == "menu":
                    if self.start_button_rect and self.start_button_rect.collidepoint(event.pos):
                        self.start_practice()
                
                elif self.state == "playing":
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(event.pos):
                            self.check_answer(i)
                            break
                
                elif self.state == "feedback":
                    # Click to continue
                    if self.current_feedback_sound:
                        self.current_feedback_sound.stop()
                    
                    self.current_idx += 1
                    
                    if self.current_idx >= len(self.questions):
                        self.state = "complete"
                    else:
                        self.state = "playing"
                        self.play_current_question_sound()
                
                elif self.state == "complete":
                    if hasattr(self, 'done_rect') and self.done_rect.collidepoint(event.pos):
                        return False
            
            elif event.type == pygame.USEREVENT + 4:
                if self.state == "playing" and self.current_replay < self.question_replay_count:
                    self.play_current_question_sound(first_play=False)
                    self.current_replay += 1
        
        return True
    
    # ==========================================================
    # MAIN LOOP
    # ==========================================================
    def run(self):
        """Main practice loop"""
        if self.screen is None or self.W == 0 or self.H == 0:
            raise RuntimeError("Screen must be set before calling run()")
        
        self._load_assets()
        
        running = True
        self.intro_start_time = pygame.time.get_ticks()
        
        while running:
            self.clock.tick(60)
            
            # Handle events
            running = self.handle_events()
            if not running:
                break
            
            # Draw based on state
            if self.state == "intro":
                self.draw_intro()
                if pygame.time.get_ticks() - self.intro_start_time >= self.intro_delay:
                    self.state = "menu"
            
            elif self.state == "menu":
                self.draw_menu()
            
            elif self.state == "playing":
                self.draw_playing()
            
            elif self.state == "feedback":
                self.draw_feedback()
                
                # Auto-advance after feedback
                if pygame.time.get_ticks() >= self.feedback_until:
                    if self.current_feedback_sound:
                        self.current_feedback_sound.stop()
                    
                    self.current_idx += 1
                    
                    if self.current_idx >= len(self.questions):
                        self.state = "complete"
                    else:
                        self.state = "playing"
                        self.play_current_question_sound()
            
            elif self.state == "complete":
                self.draw_complete()
            
            # Draw exit button
            if self.exit_img and self.exit_rect:
                self.screen.blit(self.exit_img, self.exit_rect)
            
            pygame.display.flip()
        
        self.stop_all_sounds()
