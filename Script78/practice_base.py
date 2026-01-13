# practice_base.py - Simple practice questions without scoring (PART 1)
import pygame
import sys
import os
import random
from screen_helpers import confirm_popup, load_font
import config
import math

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
        self.check_button_rect = None  # ✅ ADD: For drag-drop check button
        
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

        # Drag-and-drop state
        self.dragging = False
        self.dragged_item = None
        self.drag_offset = (0, 0)
        self.drop_zones = []
        self.placed_items = {}
        
        # Tracing state
        self.tracing_active = False
        self.trace_points = []
        self.trace_path = []
        self.trace_tolerance = 50
        self.trace_progress = 0.0
        self.trace_complete = False
    
    def _init_asset_paths(self):
        """Initialize asset paths"""
        self.bg_path = os.path.join(IMG_PATH, "soccerfield.png")
        self.question_bg_path = os.path.join(IMG_PATH, "bg_ft.png")
        self.start_img_path = os.path.join(IMG_PATH, "practice.png")
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

    def _load_question_assets(self, q):
        """Load assets specific to current question type"""
        q_type = q.get("type", "multiple_choice")
        
        if q_type == "drag_drop":
            # Load draggable items
            items = q.get("items", [])
            for item in items:
                path = os.path.join(IMG_PATH, item.get("file"))
                img = load_image(path)
                if img:
                    size = item.get("size", (150, 150))
                    item["image"] = pygame.transform.smoothscale(img, size)
                    
                    # Convert relative positions to absolute screen positions
                    x_offset = item.get("x", 0)
                    y_offset = item.get("y", 0)
                    
                    if abs(x_offset) < self.W * 0.5:
                        abs_x = (self.W // 2) + x_offset
                    else:
                        abs_x = x_offset
                    
                    if abs(y_offset) < self.H * 0.5:
                        abs_y = (self.H // 2) + y_offset
                    else:
                        abs_y = y_offset
                    
                    item["rect"] = pygame.Rect(abs_x, abs_y, size[0], size[1])
            
            # Load drop zones
            zones = q.get("drop_zones", [])
            for zone in zones:
                x_offset = zone.get("x", 0)
                y_offset = zone.get("y", 0)
                w = zone.get("w", 200)
                h = zone.get("h", 150)
                
                if abs(x_offset) < self.W * 0.5:
                    abs_x = (self.W // 2) + x_offset - (w // 2)
                else:
                    abs_x = x_offset
                
                if abs(y_offset) < self.H * 0.5:
                    abs_y = (self.H // 2) + y_offset - (h // 2)
                else:
                    abs_y = y_offset
                
                zone["rect"] = pygame.Rect(abs_x, abs_y, w, h)
        
        elif q_type == "tracing":
            # Load tracing path points
            self.trace_path = q.get("trace_path", [])
            self.trace_points = []
            self.trace_progress = 0.0
            self.trace_complete = False
            
            # Load letter background image
            path = os.path.join(IMG_PATH, q.get("letter_image"))
            img = load_image(path)
            if img:
                size = q.get("letter_size", (400, 600))
                q["letter_surface"] = pygame.transform.smoothscale(img, size)
    
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
        
        # Load assets for first question BEFORE changing state
        if self.questions:
            self._load_question_assets(self.questions[0])
        
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

    # ==========================================================
    # ANSWER CHECKING - CONTINUES FROM PART 1
    # ==========================================================
    def check_answer(self, idx=None):
        """Check answer based on question type"""
        if not (0 <= self.current_idx < len(self.questions)):
            return
        
        q = self.questions[self.current_idx]
        q_type = q.get("type", "multiple_choice")
        
        if q_type == "multiple_choice":
            self._check_multiple_choice(idx)
        elif q_type == "drag_drop":
            self._check_drag_drop()
        elif q_type == "tracing":
            self._check_tracing()

    def _check_multiple_choice(self, idx):
        """Check multiple choice answer - ONLY CALLED ON CLICK"""
        q = self.questions[self.current_idx]
        correct_answer = q.get("answer", 0)
        is_correct = (idx == correct_answer)
        
        if is_correct:
            self._show_correct_feedback()
        else:
            self._play_tryagain_sound()

    def _check_drag_drop(self):
        """Check if all items are correctly placed - ONLY CALLED WHEN CHECK BUTTON PRESSED"""
        q = self.questions[self.current_idx]
        items = q.get("items", [])
        
        # Check if all items are correctly placed
        correct = True
        for item in items:
            correct_zone_id = item.get("correct_zone")
            placed_zone_id = self.placed_items.get(item.get("id"))
            
            if placed_zone_id != correct_zone_id:
                correct = False
                break
        
        if correct and len(self.placed_items) == len(items):
            self._show_correct_feedback()
        else:
            self._play_tryagain_sound()

    def _check_tracing(self):
        """Check if tracing is complete - ONLY CALLED WHEN USER FINISHES"""
        if self.trace_complete:
            self._show_correct_feedback()
        else:
            self._play_tryagain_sound()

    def _show_correct_feedback(self):
        """Show correct answer feedback"""
        self.stop_all_sounds()
        if self.current_question_sound:
            self.current_question_sound.stop()
            self.current_question_sound = None
        
        self.feedback_correct = True
        self.current_feedback_img = self._get_feedback_image(True)
        snd = self._get_feedback_sound(True)
        self.current_feedback_sound = snd
        
        if snd:
            snd.stop()
            snd.play()
        
        self.feedback_until = pygame.time.get_ticks() + 3000
        self.state = "feedback"

    def _play_tryagain_sound(self):
        """Play try again sound - NO VISUAL FEEDBACK"""
        tryagain_path = os.path.join(SOUND_PATH, "tryagain.wav")
        if os.path.exists(tryagain_path):
            try:
                wrong_snd = pygame.mixer.Sound(tryagain_path)
                wrong_channel = pygame.mixer.Channel(1)
                wrong_channel.play(wrong_snd)
            except Exception as e:
                print(f"⚠️ Failed to play tryagain sound: {e}")
    
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
        """Draw multiple choice practice question"""
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

    def draw_drag_drop(self):
        """Draw drag and drop question"""
        if self.question_bg:
            self.screen.blit(self.question_bg, (0, 0))
        else:
            self.screen.fill((255, 255, 255))
        
        if not (0 <= self.current_idx < len(self.questions)):
            return
        
        q = self.questions[self.current_idx]
        
        # Safety check - ensure assets are loaded
        zones = q.get("drop_zones", [])
        for zone in zones:
            if "rect" not in zone:
                print("⚠️ Drop zone rect not initialized, loading assets...")
                self._load_question_assets(q)
                return
        
        # Draw drop zones
        for zone in zones:
            color = (200, 200, 200, 100) if zone.get("id") not in self.placed_items.values() else (100, 255, 100, 150)
            zone_surf = pygame.Surface((zone["rect"].w, zone["rect"].h), pygame.SRCALPHA)
            zone_surf.fill(color)
            self.screen.blit(zone_surf, zone["rect"])
            
            # Draw zone border
            pygame.draw.rect(self.screen, (100, 100, 100), zone["rect"], 3, border_radius=10)
            
            # Draw zone label
            try:
                font = pygame.font.Font(config.ARABIC_FONT_REGULAR, int(self.H * 0.03))
            except:
                font = pygame.font.SysFont("Arial", int(self.H * 0.03))
            
            label = font.render(zone.get("label", ""), True, (50, 50, 50))
            self.screen.blit(label, label.get_rect(center=zone["rect"].center))
        
        # Draw draggable items
        items = q.get("items", [])
        for item in items:
            if item.get("image") and "rect" in item:
                # Skip if item is being dragged (will draw it last)
                if self.dragging and self.dragged_item == item:
                    continue
                
                self.screen.blit(item["image"], item["rect"])
        
        # Draw dragged item on top
        if self.dragging and self.dragged_item and self.dragged_item.get("image") and "rect" in self.dragged_item:
            self.screen.blit(self.dragged_item["image"], self.dragged_item["rect"])
        
        # Draw instruction
        try:
            font = pygame.font.Font(config.ARABIC_FONT_REGULAR, int(self.H * 0.04))
        except:
            font = pygame.font.SysFont("Arial", int(self.H * 0.04))
        
        instruction = font.render("Drag items to the correct zones", True, (20, 120, 20))
        self.screen.blit(instruction, instruction.get_rect(center=(self.W // 2, int(self.H * 0.1))))
        
        # ✅ Check button - only appears after all items placed
        if len(self.placed_items) == len(items):
            btn_rect = pygame.Rect(self.W // 2 - 175, self.H - 250, 350, 70)
            pygame.draw.rect(self.screen, (0, 200, 0), btn_rect, border_radius=15)
            
            try:
                font = pygame.font.Font(config.ARABIC_FONT_BOLD, int(self.H * 0.03))
            except:
                font = pygame.font.SysFont("Arial", int(self.H * 0.03), bold=True)
            
            check_text = font.render("Check Answer", True, (255, 255, 255))
            self.screen.blit(check_text, check_text.get_rect(center=btn_rect.center))
            self.check_button_rect = btn_rect
        else:
            self.check_button_rect = None
        
        # Profile icon
        if self.main_app and hasattr(self.main_app, 'profile_icon'):
            self.screen.blit(self.main_app.profile_icon, self.main_app.profile_rect)

    def draw_tracing(self):
        """Draw letter tracing question"""
        if self.question_bg:
            self.screen.blit(self.question_bg, (0, 0))
        else:
            self.screen.fill((255, 255, 255))
        
        if not (0 <= self.current_idx < len(self.questions)):
            return
        
        q = self.questions[self.current_idx]
        
        # Letter position on screen
        letter_x_ratio = q.get("letter_x_ratio", 0.5)
        letter_y_ratio = q.get("letter_y_ratio", 0.45)
        
        letter_x = int(self.W * letter_x_ratio)
        letter_y = int(self.H * letter_y_ratio)
        
        # Draw letter to trace (faded)
        if q.get("letter_surface"):
            letter_surf = q["letter_surface"].copy()
            letter_surf.set_alpha(80)
            letter_rect = letter_surf.get_rect(center=(letter_x, letter_y))
            self.screen.blit(letter_surf, letter_rect)
            
            q["letter_offset"] = (letter_rect.x, letter_rect.y)
        
        # Draw trace path (guide dots)
        # Draw trace path (guide dots)
        if self.trace_path:
            letter_offset = q.get("letter_offset", (0, 0))
            current_target = getattr(self, 'last_matched_index', 0)
            
            for i, point in enumerate(self.trace_path):
                adjusted_point = (point[0] + letter_offset[0], point[1] + letter_offset[1])
                
                # Color coding for visual feedback
                if i < current_target:
                    # Already traced - GREEN
                    color = (0, 255, 0)
                    radius = 8
                elif i == current_target:
                    # NEXT point to trace - YELLOW (pulsing)
                    pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500.0
                    color = (255, 255, 0)
                    radius = int(12 + pulse * 4)  # Pulsing effect
                else:
                    # Not yet traced - GRAY
                    color = (200, 200, 200)
                    radius = 8
                
                pygame.draw.circle(self.screen, color, adjusted_point, radius)
                
                # Draw a ring around the LAST point to make it obvious
                if i == len(self.trace_path) - 1:
                    pygame.draw.circle(self.screen, (255, 0, 0), adjusted_point, radius + 5, 3)
        
        # Draw traced line
        if len(self.trace_points) > 1:
            pygame.draw.lines(self.screen, (0, 0, 255), False, self.trace_points, 5)
        
        # Draw progress bar
        progress_width = int(self.W * 0.6)
        progress_x = (self.W - progress_width) // 2
        progress_y = int(self.H * 0.85)
        
        pygame.draw.rect(self.screen, (200, 200, 200), (progress_x, progress_y, progress_width, 30), border_radius=15)
        filled_width = int(progress_width * self.trace_progress)
        pygame.draw.rect(self.screen, (0, 255, 0), (progress_x, progress_y, filled_width, 30), border_radius=15)
        
        # Draw instruction
        try:
            font = pygame.font.Font(config.ARABIC_FONT_REGULAR, int(self.H * 0.04))
        except:
            font = pygame.font.SysFont("Arial", int(self.H * 0.04))
        
        instruction = font.render("Trace the letter with your finger or mouse", True, (20, 120, 20))
        self.screen.blit(instruction, instruction.get_rect(center=(self.W // 2, int(self.H * 0.1))))
        
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
        """Draw completion screen"""
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
    # EVENT HANDLING - ✅ FIXED: Only check answers on explicit actions
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
                    q = self.questions[self.current_idx] if 0 <= self.current_idx < len(self.questions) else {}
                    q_type = q.get("type", "multiple_choice")
                    
                    if q_type == "multiple_choice":
                        # ✅ FIXED: Check answer ONLY when option is clicked
                        for i, rect in enumerate(self.option_rects):
                            if rect.collidepoint(event.pos):
                                self.check_answer(i)
                                break
                    
                    elif q_type == "drag_drop":
                        # ✅ FIXED: Start drag, or check answer if check button clicked
                        if hasattr(self, 'check_button_rect') and self.check_button_rect and self.check_button_rect.collidepoint(event.pos):
                            # Check answer when button pressed
                            self.check_answer()
                        else:
                            # Start dragging
                            items = q.get("items", [])
                            for item in items:
                                if "rect" in item and item["rect"].collidepoint(event.pos):
                                    self.dragging = True
                                    self.dragged_item = item
                                    self.drag_offset = (
                                        item["rect"].x - event.pos[0],
                                        item["rect"].y - event.pos[1]
                                    )
                                    break
                    
                    elif q_type == "tracing":
                        # Start tracing - only if not already complete
                        if not self.trace_complete:
                            self.tracing_active = True
                            self.trace_points = [event.pos]
                            self.trace_progress = 0.0
                            self.last_matched_index = 0  # ✅ ADD THIS LINE
                
                elif self.state == "feedback":
                    # Click to continue
                    if self.current_feedback_sound:
                        self.current_feedback_sound.stop()
                    
                    self.current_idx += 1
                    
                    if self.current_idx >= len(self.questions):
                        self.state = "complete"
                    else:
                        # Not enough traced, play try again
                        self._play_tryagain_sound()
                        # Reset for retry
                        self.trace_points = []
                        self.trace_progress = 0.0
                        self.trace_complete = False
                        self.last_matched_index = 0  # ✅ ADD THIS LINE
                        
                        self.state = "playing"
                        next_q = self.questions[self.current_idx]
                        self._load_question_assets(next_q)
                        self.play_current_question_sound()
                
                elif self.state == "complete":
                    if hasattr(self, 'done_rect') and self.done_rect.collidepoint(event.pos):
                        return False
            
            # ✅ FIXED: Handle mouse release for drag-drop AND tracing
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.state == "playing":
                    q = self.questions[self.current_idx] if 0 <= self.current_idx < len(self.questions) else {}
                    q_type = q.get("type", "multiple_choice")
                    
                    if q_type == "drag_drop" and self.dragging:
                        zones = q.get("drop_zones", [])
                        
                        # Check if item dropped in any zone
                        for zone in zones:
                            if "rect" in zone and zone["rect"].collidepoint(event.pos):
                                # Place item in this zone
                                self.placed_items[self.dragged_item["id"]] = zone["id"]
                                # Snap item to zone center
                                self.dragged_item["rect"].center = zone["rect"].center
                                break
                        
                        self.dragging = False
                        self.dragged_item = None
                    
                    elif q_type == "tracing":
                        # Stop tracing when mouse released
                        if self.tracing_active:
                            self.tracing_active = False
                            
                            # ✅ STRICT: Must have passed through ALL points INCLUDING the last one
                            total_points = len(self.trace_path)
                            matched = getattr(self, 'last_matched_index', 0)
                            
                            print(f"\n🏁 TRACING FINISHED:")
                            print(f"   Total guide points: {total_points}")
                            print(f"   Points matched: {matched}")
                            print(f"   Last index in path: {total_points - 1}")
                            print(f"   Required to pass: {total_points} (all points)")
                            
                            # ✅ Must have incremented past the last index (meaning last point was matched)
                            if matched >= total_points:
                                # Matched ALL points exactly
                                print("   ✅ COMPLETE - All points traced!")
                                self.trace_complete = True
                                self.check_answer()
                            else:
                                # Didn't complete the full path
                                print(f"   ❌ INCOMPLETE - Only {matched}/{total_points} points traced")
                                self._play_tryagain_sound()
                                # Reset for retry
                                self.trace_points = []
                                self.trace_progress = 0.0
                                self.trace_complete = False
                                self.last_matched_index = 0
            
            # ✅ Handle mouse motion for dragging and tracing
            elif self.state == "playing" and self.tracing_active:
                q = self.questions[self.current_idx]
                
                # Get current mouse position
                mouse_pos = pygame.mouse.get_pos()
                
                # Add point to tracing
                self.trace_points.append(mouse_pos)
                
                # Calculate progress by checking how many guide points have been reached IN ORDER
                if self.trace_path and q.get("letter_offset"):
                    letter_offset = q["letter_offset"]
                    
                    # Start from the last matched point (or 0 if none matched yet)
                    if not hasattr(self, 'last_matched_index'):
                        self.last_matched_index = 0
                    
                    # ✅ CHECK: Is user too far from the expected path?
                    if self.last_matched_index < len(self.trace_path):
                        next_guide = self.trace_path[self.last_matched_index]
                        adjusted_guide = (
                            next_guide[0] + letter_offset[0],
                            next_guide[1] + letter_offset[1]
                        )
                        
                        # Check distance to next expected point
                        dx = mouse_pos[0] - adjusted_guide[0]
                        dy = mouse_pos[1] - adjusted_guide[1]
                        distance = (dx * dx + dy * dy) ** 0.5
                        
                        # ✅ If too far off-path, STOP and reset
                        off_path_tolerance = self.trace_tolerance * 2  # 60 pixels max deviation
                        if distance > off_path_tolerance:
                            # User went too far off path - stop and reset
                            self._play_tryagain_sound()
                            self.tracing_active = False
                            self.trace_points = []
                            self.trace_progress = 0.0
                            self.trace_complete = False
                            self.last_matched_index = 0
                            print(f"❌ OFF PATH: Distance {distance:.1f} > {off_path_tolerance}")
                        elif distance < self.trace_tolerance:
                            # Within tolerance - matched next point in sequence!
                            print(f"✅ MATCHED point {self.last_matched_index} (distance: {distance:.1f})")
                            self.last_matched_index += 1
                    
                    # Update progress based on sequential matches
                    self.trace_progress = self.last_matched_index / max(1, len(self.trace_path))
                    print(f"Progress: {self.last_matched_index}/{len(self.trace_path)} = {self.trace_progress*100:.1f}%")
            
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
                q = self.questions[self.current_idx] if 0 <= self.current_idx < len(self.questions) else {}
                q_type = q.get("type", "multiple_choice")
                
                if q_type == "multiple_choice":
                    self.draw_playing()
                elif q_type == "drag_drop":
                    self.draw_drag_drop()
                elif q_type == "tracing":
                    self.draw_tracing()
            
            elif self.state == "feedback":
                self.draw_feedback()
                
                if pygame.time.get_ticks() >= self.feedback_until:
                    if self.current_feedback_sound:
                        self.current_feedback_sound.stop()
                    
                    self.current_idx += 1
                    
                    if self.current_idx >= len(self.questions):
                        self.state = "complete"
                    else:
                        # Reset state for next question
                        self.placed_items = {}
                        self.trace_points = []
                        self.trace_progress = 0.0
                        self.trace_complete = False
                        
                        self.state = "playing"
                        next_q = self.questions[self.current_idx]
                        self._load_question_assets(next_q)
                        self.play_current_question_sound()
            
            elif self.state == "complete":
                self.draw_complete()
            
            # Draw exit button
            if self.exit_img and self.exit_rect:
                self.screen.blit(self.exit_img, self.exit_rect)
            
            pygame.display.flip()
        
        self.stop_all_sounds()

    
