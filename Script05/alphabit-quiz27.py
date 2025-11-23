# alphabit_pygame_quiz_with_hover_fixed.py
# Requires: pygame, pillow, arabic_reshaper, python-bidi
# pip install pygame pillow arabic_reshaper python-bidi

import os
import random
import pygame
import random
from PIL import Image, ImageFont, ImageDraw

# Optional shaping libraries for Arabic
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_BIDI = True
except Exception:
    HAS_BIDI = False
    print("⚠️ Missing 'arabic_reshaper' and/or 'python-bidi'. Arabic shaping may be incorrect.")
    print("Install: pip install arabic_reshaper python-bidi")

# ============================== CONFIG ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "../assets")
IMG_PATH = os.path.join(ASSET_PATH, "img/alphabitSound")
SOUND_PATH = os.path.join(ASSET_PATH, "sounds/alphabitSound")
FONTS_PATH = os.path.join(ASSET_PATH, "fonts")

PREFERRED_ARABIC_FONTS = [
    os.path.join(FONTS_PATH, "NotoNaskhArabic-Regular.ttf"),
    os.path.join(FONTS_PATH, "arabic.ttf"),
    os.path.join(FONTS_PATH, "NotoSansArabic-Regular.ttf"),
]

def find_arabic_font():
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

ARABIC_FONT_PATH = None  # assigned after pygame.init()

QUESTIONS = [
##    {
##        "sound": "01alef-s.wav",
##        "options": [{"file": "12sen.png", "size": (350, 400), "y_offset": 130}, {"file": "01alef.png", "size": (120, 530)}, {"file": "08dal.png", "size": (200, 400), "y_offset": 130}, {"file": "06ha.png", "size": (280, 530)},],
##        "answer": 1,
##        "difficulty": "easy",
##        "margin": 450   # custom spacing for this question
##    },
    {
        "sound": "02ba-s.wav",
        "options": [{"file": "27waw.png", "size": (200, 350)}, {"file": "10ra.png", "size": (200, 350)}, {"file": "02ba.png", "size": (350, 400)}, {"file": "25noon.png", "size": (250, 400), "y_offset": -50},],
        "answer": 2,
        "difficulty": "easy",
        "margin": 400   # custom spacing for this question
    },
##    {
##        "sound": "03ta-s.wav",
##        "options": [{"file": "21kf.png", "size": (120, 530)}, {"file": "26heh.png", "size": (120, 530)}, {"file": "03ta.png", "size": (120, 530)}, {"file": "04tha.png", "size": (120, 530)},],
##        "answer": 3,
##        "difficulty": "easy",
##        "margin": 500   # custom spacing for this question
##    },
##    {
##        "sound": "04tha-s.wav",
##        "options": [{"file": "04tha.png", "size": (428, 379)}, {"file": "02ba.png", "size": (428, 379)}, {"file": "09thal.png", "size": (428, 379)}, {"file": "17zaa.png", "size": (428, 379)},],
##        "answer": 0,
##        "difficulty": "easy",
##        "margin": 300   # custom spacing for this question
##    },{
##        "sound": "05gem-s.wav",
##        "options": [{"file": "23lam.png", "size": (120, 530)}, {"file": "07ka.png", "size": (120, 530)}, {"file": "12sen.png", "size": (120, 530)}, {"file": "05gem.png", "size": (120, 530)},],
##        "answer": 3,
##        "difficulty": "easy",
##        "margin": 500   # custom spacing for this question
##    },
##    {
##        "sound": "06ha-s.wav",
##        "options": [{"file": "26heh.png", "size": (428, 379)}, {"file": "06ha.png", "size": (428, 379)}, {"file": "04tha.png", "size": (428, 379)}, {"file": "07ka.png", "size": (428, 379)},],
##        "answer": 1,
##        "difficulty": "easy",
##        "margin": 300   # custom spacing for this question
##    },{
##        "sound": "07ka-s.wav",
##        "options": [{"file": "05gem.png", "size": (120, 530)}, {"file": "21kf.png", "size": (120, 530)}, {"file": "20feh.png", "size": (120, 530)}, {"file": "07ka.png.png", "size": (120, 530)},],
##        "answer": 3,
##        "difficulty": "easy",
##        "margin": 500   # custom spacing for this question
##    },
##    {
##        "sound": "08dal-s",
##        "options": [{"file": "03ta.png", "size": (428, 379)}, {"file": "08dal.png", "size": (428, 379)}, {"file": "16taa.png", "size": (428, 379)}, {"file": "28yaa.png", "size": (428, 379)},],
##        "answer": 1,
##        "difficulty": "easy",
##        "margin": 300   # custom spacing for this question
##    },
##    # ------------------------- Medium Level Questions -------------------------
##    {
##        "sound": "01alef-s.wav",
##        "options": [{"file": "01alef-t.png", "size": (120, 530)}, {"file": "01alef-d-t.png", "size": (120, 530)}, {"file": "01alef-f-t.png", "size": (120, 530)}, {"file": "01alef-k.png", "size": (120, 530)},],
##        "answer": 0,
##        "difficulty": "medium",
##        "margin": 100   # custom spacing for this question
##    },
##    # ------------------------- Hard Level Questions -------------------------
##    {
##        "sound": "02ba-s.wav",
##        "options": [{"file": "02ba.png", "size": (428, 379)}, {"file": "02ba-d.png", "size": (428, 379)}, {"file": "02ba-f.png", "size": (428, 379)}, {"file": "02ba-k.png", "size": (428, 379)},],
##        "answer": 0,
##        "difficulty": "hard",
##        "margin": 100   # custom spacing for this question
##    },
]

# Difficulty inclusion map:
# easy -> [easy]
# medium -> [medium, easy]
# hard -> [hard, medium]
DIFFICULTY_MAP = {
    "easy": ["easy"],
    "medium": ["medium", "easy"],
    "hard": ["hard", "medium"]
}


# ============================== Helpers ==============================
def load_image(path, alpha=True):
    if not os.path.exists(path):
        print(f"⚠️ Missing image: {path}")
        return None
    try:
        surf = pygame.image.load(path)
        return surf.convert_alpha() if alpha else surf.convert()
    except Exception as e:
        print(f"⚠️ Failed to load image {path}: {e}")
        return None

def load_sound(path):
    if not os.path.exists(path):
        print(f"⚠️ Missing sound: {path}")
        return None
    try:
        return pygame.mixer.Sound(path)
    except Exception as e:
        print(f"⚠️ Failed to load sound {path}: {e}")
        return None

def render_arabic_to_surface(text, font_path, size, color=(255,255,255), bold=False, italic=False):
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
    
    # Fallback for non-Arabic text
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


# ============================== Game Class ==============================
class AlphabitQuiz:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.last_hover_id = None

        # ----------------- Create Black Loading Screen -----------------
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.W, self.H = self.screen.get_size()
        self.screen.fill((0,0,0))  # black screen
        pygame.display.flip()

        # Audio volumes
        self.volume_bg = 0.15
        self.volume_intro = 1.0
        self.volume_hover = 0.8
        self.volume_questions = 1.0
        self.volume_feedback = 1.0

        # Load hover sounds
        self.hover_sounds = {}
        for level in ("easy","medium","hard"):
            path = os.path.join(SOUND_PATH, f"hover_{level}.wav")
            if os.path.exists(path):
                try:
                    self.hover_sounds[level] = pygame.mixer.Sound(path)
                    self.hover_sounds[level].set_volume(self.volume_hover)
                except Exception as e:
                    print(f"⚠️ Failed to load hover sound {level}: {e}")
            else:
                print(f"⚠️ Missing hover sound file: {path}")

        global ARABIC_FONT_PATH
        ARABIC_FONT_PATH = find_arabic_font()

        # ----------------- Game State -----------------
        self.state = "intro"
        self.intro_sound_playing = False
        self.intro_start_time = pygame.time.get_ticks()
        self.intro_delay = 1000
        self.last_hovered = None
        self.selected_difficulty = None
        self.questions = []
        self.current_idx = 0
        self.score = 0
        self.feedback_until = 0
        self.feedback_correct = False
        self.current_feedback_sound = None
        self.menu_rects = {}
        self.results_buttons = {}

        # ----------------- Load Sounds -----------------
        self.intro_sound = load_sound(os.path.join(SOUND_PATH, "WelcIntro.wav"))
        if self.intro_sound:
            self.intro_sound.set_volume(self.volume_intro)

        self.loaded_sounds = {}
        pre_sounds = ["correct.wav", "wrong.wav", "welcome.wav"]
        for q in QUESTIONS:
            if q.get("sound"):
                pre_sounds.append(q["sound"])
        for s in set(pre_sounds):
            snd = load_sound(os.path.join(SOUND_PATH, s))
            if snd:
                snd.set_volume(self.volume_questions)
                self.loaded_sounds[s] = snd
        # -------------- attributes for sound replay ------------
        self.question_replay_count = 5      # number of times to replay
        self.question_replay_interval = 10000  # 10 seconds in milliseconds
        self.current_replay = 0

        # Background music (only for intro)
        self.bg_music_path = os.path.join(SOUND_PATH, "bg_music.mp3")
        if not os.path.exists(self.bg_music_path):
            self.bg_music_path = None
        self.intro_music_playing = False

        # ----------------- Window -----------------
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.W, self.H = self.screen.get_size()
        pygame.display.set_caption("ما هذا؟ 🧠 - Pygame (hover + Arabic)")

        self.font_big = pygame.font.SysFont("arial", 48, bold=True)
        self.font_med = pygame.font.SysFont("arial", 36)
        self.font_small = pygame.font.SysFont("arial", 28)

        # ----------------- Background -----------------
        bg_path = os.path.join(IMG_PATH, "soccerfield.png")
        self.bg = load_image(bg_path, alpha=False)
        if self.bg:
            self.bg = pygame.transform.smoothscale(self.bg, (self.W, self.H))
        else:
            self.bg_color = (20,120,20)

        # ----------------- Question Background -----------------
        question_bg_path = os.path.join(IMG_PATH, "quiz_bg.png")  # <-- your question background image
        self.question_bg = load_image(question_bg_path, alpha=False)
        if self.question_bg:
            self.question_bg = pygame.transform.smoothscale(self.question_bg, (self.W, self.H))

        # Feedback icons for results
        self.goal_icon = load_image(os.path.join(IMG_PATH, "football_goal.png"))
        if self.goal_icon:
            self.goal_icon = pygame.transform.smoothscale(self.goal_icon, (60,60))

        self.miss_icon = load_image(os.path.join(IMG_PATH, "football_miss.png"))
        if self.miss_icon:
            self.miss_icon = pygame.transform.smoothscale(self.miss_icon, (60,60))



        # ----------------- EXIT BUTTON (ADDED) -----------------
        # Load exitball.png from IMG_PATH. If missing, create a fallback.
        exit_img_path = os.path.join(IMG_PATH, "exitball.png")
        self.exit_img = load_image(exit_img_path, alpha=True)
        if self.exit_img:
            # scale to a reasonable size relative to screen width
            size = int(self.W * 0.07)
            try:
                self.exit_img = pygame.transform.smoothscale(self.exit_img, (size, size))
            except Exception:
                # if scaling fails, keep original
                pass
            self.exit_rect = self.exit_img.get_rect(center=(self.W // 2, self.H - 80))
        else:
            # fallback circular button (semi-transparent red)
            size = int(self.W * 0.07)
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(surf, (200, 0, 0, 220), (size//2, size//2), size//2)
            # small white 'X'
            try:
                pygame.draw.line(surf, (255,255,255), (size*0.28, size*0.28), (size*0.72, size*0.72), 3)
                pygame.draw.line(surf, (255,255,255), (size*0.72, size*0.28), (size*0.28, size*0.72), 3)
            except Exception:
                pass
            self.exit_img = surf
            self.exit_rect = self.exit_img.get_rect(topleft=(20, 20))

        # ----------------- Exit Hover Sound -----------------
        self.exit_hover_sound = load_sound(os.path.join(SOUND_PATH, "hover_exit.wav"))
        if self.exit_hover_sound:
            self.exit_hover_sound.set_volume(1.0)
        self.exit_hovered_last = False  # track hover state

        # background fallback
        self.bg_color = (20, 120, 20)
        self.clock = pygame.time.Clock()

        # ----------------- Difficulty Icons -----------------
        self.diff_orig = {}
        for d in ("easy","medium","hard"):
            p = os.path.join(IMG_PATH, f"{d}.png")
            img = load_image(p, alpha=True)
            if img:
                max_h = int(self.H * 0.6)
                scale = max_h / img.get_height()
                w = int(img.get_width() * scale * 0.8)
                h = int(max_h * 0.9)
                img = pygame.transform.smoothscale(img, (w,h))
            self.diff_orig[d] = img

        self.diff_state = {}
        for d in ("easy","medium","hard"):
            orig = self.diff_orig.get(d)
            if orig:
                self.diff_state[d] = {'orig': orig, 'scale':1.0, 'target':1.0}
            else:
                placeholder = pygame.Surface((int(self.W*0.15), int(self.H*0.5)), pygame.SRCALPHA)
                placeholder.fill((200,200,200,255))
                self.diff_state[d] = {'orig': placeholder, 'scale':1.0, 'target':1.0}

        self.diff_centers = [
            (int(self.W*0.25), int(self.H*0.55)),
            (int(self.W*0.5), int(self.H*0.55)),
            (int(self.W*0.75), int(self.H*0.55))
        ]

        # ----------------- Feedback Images -----------------
        self.thumb_up = load_image(os.path.join(IMG_PATH, "thumbsup.png"), True)
        self.thumb_down = load_image(os.path.join(IMG_PATH, "thumbsdown.png"), True)
        if self.thumb_up: self.thumb_up = pygame.transform.smoothscale(self.thumb_up, (300,300))
        if self.thumb_down: self.thumb_down = pygame.transform.smoothscale(self.thumb_down, (300,300))
        # ----------------- MULTIPLE FEEDBACK IMAGES & SOUNDS -----------------
        self.correct_feedback_imgs = [
            load_image(os.path.join(IMG_PATH, "thumbsup.png")),
            load_image(os.path.join(IMG_PATH, "thumbsup1.png")),
            load_image(os.path.join(IMG_PATH, "thumbsup2.png"))
        ]

        self.wrong_feedback_imgs = [
            load_image(os.path.join(IMG_PATH, "thumbsdown.png")),
            load_image(os.path.join(IMG_PATH, "thumbsdown1.png")),
            load_image(os.path.join(IMG_PATH, "thumbsdown2.png"))
        ]

        self.correct_feedback_sounds = [
            load_sound(os.path.join(SOUND_PATH, "correct.wav")),
            load_sound(os.path.join(SOUND_PATH, "correct1.wav")),
            load_sound(os.path.join(SOUND_PATH, "correct2.wav"))
        ]

        self.wrong_feedback_sounds = [
            load_sound(os.path.join(SOUND_PATH, "wrong.wav")),
            load_sound(os.path.join(SOUND_PATH, "wrong1.wav")),
            load_sound(os.path.join(SOUND_PATH, "wrong2.wav"))
        ]
        
        # ----------------- Start Intro Music -----------------
        if self.bg_music_path:
            try:
                pygame.mixer.music.load(self.bg_music_path)
                pygame.mixer.music.set_volume(self.volume_bg)
                pygame.mixer.music.play(-1)
                self.intro_music_playing = True
            except Exception as e:
                print("⚠️ Failed to play intro music:", e)

    # ----------------- Play SFX -----------------
    def play_sfx(self, name):
        s = self.loaded_sounds.get(name)
        if s:
            s.play()

    # ----------------- Stop all sounds -----------------
    def stop_all_sounds(self):
        # Stop music
        pygame.mixer.music.stop()

        # Stop all loaded sounds
        for s in self.loaded_sounds.values():
            s.stop()
        for s in self.hover_sounds.values():
            s.stop()
        if hasattr(self, "exit_hover_sound") and self.exit_hover_sound:
            self.exit_hover_sound.stop()
        if hasattr(self, "intro_sound") and self.intro_sound:
            self.intro_sound.stop()

    # ----------------- Stop hover sounds only -----------------
    def stop_hover_only(self):
        """Stop only hover-related sounds (exit + menu hover)"""
        try:
            for s in getattr(self, "hover_sounds", {}).values():
                s.stop()
        except:
            pass
        try:
            if hasattr(self, "exit_hover_sound") and self.exit_hover_sound:
                self.exit_hover_sound.stop()
        except:
            pass



    # ----------------- Questions -----------------
    def build_question_list_for(self, level):
        include = DIFFICULTY_MAP.get(level, [level])
        filtered = [q.copy() for q in QUESTIONS if q.get("difficulty") in include]
        random.shuffle(filtered)
        return filtered

    def select_difficulty(self, level):
##        # stop intro music
##        if self.intro_music_playing:
##            pygame.mixer.music.stop()
##            self.intro_music_playing = False
        self.stop_all_sounds()

        self.selected_difficulty = level
        qs = self.build_question_list_for(level)
        if not qs:
            print("⚠️ No questions for:", level)
            return
        self.questions = qs
        self.current_idx = 0
        self.score = 0
        self.state = "playing"

##        if "welcome.wav" in self.loaded_sounds:
##            self.play_sfx("welcome.wav")

        pygame.time.set_timer(pygame.USEREVENT+3, 300, True)
        self.play_current_question_sound()

    def play_current_question_sound(self, first_play=True):
        if not (0 <= self.current_idx < len(self.questions)):
            return
        s = self.questions[self.current_idx].get("sound")
        if s:
            for snd in self.hover_sounds.values():
                snd.stop()
            self.play_sfx(s)

            if first_play:
                # Reset replay counter and start timer
                self.current_replay = 1
                pygame.time.set_timer(pygame.USEREVENT + 4, self.question_replay_interval)


    # ----------------- Menu Hover -----------------
    def update_menu_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        hovered_any = False
        for idx, key in enumerate(("easy","medium","hard")):
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
                    self.stop_hover_only()  # stops all hover sounds including exit
                    snd = self.hover_sounds.get(key)
                    if snd: snd.play()
                    self.last_hovered = key
                try: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                except: pass
            else:
                st['target'] = 1.0
        if not hovered_any:
            self.last_hovered = None
            try: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            except: pass
        for st in self.diff_state.values():
            st['scale'] += (st['target'] - st['scale'])*0.18

    # ----------------- Draw -----------------
    def draw_menu(self):
        BOLD_ARABIC_FONT = os.path.join(FONTS_PATH, "NotoNaskhArabic-Bold.ttf")
        title_surf = render_arabic_to_surface("إختر المستوى", BOLD_ARABIC_FONT, 80, color=(0, 0, 0), bold=True, italic=True)
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.W//2, int(self.H*0.03))))
        for idx, key in enumerate(("easy","medium","hard")):
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
##        hint = render_arabic_to_surface("انقر على مستوى للبدء", ARABIC_FONT_PATH or "", 28)
##        self.screen.blit(hint, hint.get_rect(center=(self.W//2, int(self.H*0.9))))

    def draw_playing(self):
        if not (0 <= self.current_idx < len(self.questions)):
            return

        q = self.questions[self.current_idx]
        opts = q.get("options", [])
        count = len(opts)
        margin = q.get("margin", 40)
        
        imgs = []
        for opt in opts:
            fname = opt.get("file")
            size = opt.get("size", (200,200))
            img = load_image(os.path.join(IMG_PATH, fname))
            if img:
                surf = pygame.transform.smoothscale(img, size)
            else:
                surf = pygame.Surface(size, pygame.SRCALPHA)
                #surf.fill((240,240,240,255))
            imgs.append(surf)

        total_w = sum(i.get_width() for i in imgs) + margin*(count-1)
        start_x = (self.W - total_w)//2
        y = int(self.H*0.35)
        self.option_rects = []

        # --- only draw once per image ---
        for i, surf in enumerate(imgs):
            x = start_x + sum(imgs[j].get_width() + margin for j in range(i))
            y_offset = opts[i].get("y_offset", 0)
            rect = pygame.Rect(x, y + y_offset, surf.get_width(), surf.get_height())
            self.screen.blit(surf, rect.topleft)
            self.option_rects.append(rect)

    def draw_feedback(self):
        dark = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        dark.fill((0,0,0,120))
        self.screen.blit(dark, (0,0))

        img = getattr(self, "current_feedback_img", None)
        if img:
            rect = img.get_rect(center=(self.W//2, self.H//2))
            self.screen.blit(img, rect.topleft)


    def draw_results(self):
        # Dim the background
        dark = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        dark.fill((0, 0, 0, 160))
        self.screen.blit(dark, (0, 0))

        correct = self.score
        wrong = len(self.questions) - self.score
        total = len(self.questions)

        # Scoreboard title
        title = render_arabic_to_surface("نتيجة المباراة", ARABIC_FONT_PATH or "", 64, color=(255,255,255), bold=True)
        self.screen.blit(title, title.get_rect(center=(self.W // 2, int(self.H * 0.15))))

        # Layout
        icon_size = 80
        spacing = 15

        # Calculate total height for all icons in each column
        total_icon_height = total * (icon_size + spacing) - spacing

        # Vertical centering start positions
        y_start = (self.H - total_icon_height) // 2

        # X positions for left (goals) and right (misses)
        x_goal = int(self.W * 0.02) - icon_size // 2
        x_miss = int(self.W * 0.98) - icon_size // 2

        # ✅ Correct answers - vertical column on left
        for i in range(correct):
            y = y_start + i * (icon_size + spacing)
            if hasattr(self, "goal_icon") and self.goal_icon:
                self.screen.blit(self.goal_icon, (x_goal, y))
            else:
                pygame.draw.circle(self.screen, (0, 200, 0), (x_goal + icon_size // 2, y + icon_size // 2), icon_size // 2)

        # ❌ Wrong answers - vertical column on right
        for i in range(wrong):
            y = y_start + i * (icon_size + spacing)
            if hasattr(self, "miss_icon") and self.miss_icon:
                self.screen.blit(self.miss_icon, (x_miss, y))
            else:
                pygame.draw.circle(self.screen, (200, 0, 0), (x_miss + icon_size // 2, y + icon_size // 2), icon_size // 2)

        # ----------------- Numeric Results -----------------
        txt_correct = render_arabic_to_surface(str(correct), "arial" or "", 500, color=(0,255,0), bold=False)
        txt_wrong   = render_arabic_to_surface(str(wrong), "arial" or "", 500, color=(255,0,0), bold=False)

        # Dynamic positions near the center but separated from icons
        x_center = self.W // 2
        y_numeric = int(self.H * 0.20)  # roughly middle of the screen vertically

        # Place correct number slightly left of center, wrong number slightly right of center
        self.screen.blit(txt_correct, txt_correct.get_rect(center=(x_center - int(self.W * 0.1), y_numeric)))
        self.screen.blit(txt_wrong,   txt_wrong.get_rect(center=(x_center + int(self.W * 0.1), y_numeric)))


        # Play Again button
        button_w, button_h = 300, 80
        x_button = self.W // 2 - button_w // 2
        y_button = int(self.H * 0.8)
        pygame.draw.rect(self.screen, (255, 215, 0), (x_button, y_button, button_w, button_h), border_radius=20)
        txt_play = render_arabic_to_surface("العب مرة أخرى", ARABIC_FONT_PATH or "", 40, color=(0, 0, 0), bold=True)
        self.screen.blit(txt_play, txt_play.get_rect(center=(x_button + button_w // 2, y_button + button_h // 2)))

        # Clickable button rect
        self.results_buttons["play_again"] = pygame.Rect(x_button, y_button, button_w, button_h)


    def check_answer(self, idx):
        if not (0 <= self.current_idx < len(self.questions)):
            return

        q = self.questions[self.current_idx]
        correct_idx = q.get("answer")
        self.feedback_correct = (idx == correct_idx)
        
        # increment score for correct answers
        if self.feedback_correct:
            self.score += 1

        self.feedback_until = pygame.time.get_ticks() + 5000  # feedback duration
        self.state = "feedback"

        # Random feedback image
        if self.feedback_correct:
            self.current_feedback_img = random.choice(self.correct_feedback_imgs)
            snd = random.choice(self.correct_feedback_sounds) if self.correct_feedback_sounds else None
        else:
            self.current_feedback_img = random.choice(self.wrong_feedback_imgs)
            snd = random.choice(self.wrong_feedback_sounds) if self.wrong_feedback_sounds else None

        # Play feedback sound
        self.current_feedback_sound = None
        if snd:
            snd.stop()  # make sure it starts clean
            self.current_feedback_sound = snd
            self.current_feedback_sound.play()





    # ----------------- Main Draw -----------------
    def draw(self):
        # ----------------- DRAW BACKGROUND -----------------
        if self.state == "playing":
            # fill the screen with white
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

        if self.state == "intro":
            if self.intro_sound and not self.intro_sound_playing:
                self.intro_sound.play()
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

        # ----------------- Draw Exit Button ON TOP OF EVERYTHING -----------------
        try:
            # blit exit button so it's always visible & clickable
            if self.exit_img:
                self.screen.blit(self.exit_img, self.exit_rect.topleft)
        except Exception:
            pass

        pygame.display.flip()

    # ----------------- Run -----------------
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            dt = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # ----------------- EXIT BUTTON CLICK HANDLING -----------------
                    if hasattr(self, 'exit_rect') and self.exit_rect.collidepoint(event.pos):
                        running = False
                        break
                    
                    # Menu click
                    if self.state == "menu":
                        for key, rect in self.menu_rects.items():
                            if rect.collidepoint(event.pos):
                                self.select_difficulty(key)

                 # ----------------- QUESTION OPTION CLICK HANDLING -----------------
                    elif self.state == "playing":
                        for i, rect in enumerate(getattr(self, "option_rects", [])):
                            if rect.collidepoint(event.pos):
                                self.check_answer(i)
                                break
                            
                    elif self.state == "feedback":
                        # Stop feedback sound immediately
                        if self.current_feedback_sound:
                            self.current_feedback_sound.stop()
                            self.current_feedback_sound = None

                        # Cancel the feedback timer
                        self.feedback_until = 0

                        # Move to next question
                        self.current_idx += 1
                        if self.current_idx >= len(self.questions):
                            self.state = "results"
                        else:
                            self.state = "playing"
                            self.play_current_question_sound()

                        # Reset feedback state
                        self.feedback_correct = False
                        self.current_feedback_img = None

                        break  # important to stop further event processing

                    
                    # ----------------- Play Again -----------------
                    if self.state == "results":
                        if "play_again" in self.results_buttons and self.results_buttons["play_again"].collidepoint(event.pos):
                            self.stop_all_sounds()
                            self.score = 0
                            self.current_idx = 0
                            self.feedback_correct = False
                            self.current_feedback_img = None
                            self.feedback_until = 0
                            self.current_feedback_sound = None
                            self.selected_difficulty = None  # reset difficulty

                            # Return to intro state
                            #self.state = "intro"
                            self.state = "menu"
                            self.intro_start_time = pygame.time.get_ticks()
                            #self.intro_sound_playing = False
                            self.intro_sound_playing = True
                            #self.show_menu_icons = False
                            self.show_menu_icons = True
                            break




                # ----------------- QUESTION REPLAY TIMER -----------------
                elif event.type == pygame.USEREVENT + 4:
                    if self.state == "playing" and self.current_replay < self.question_replay_count:
                        self.play_current_question_sound(first_play=False)
                        self.current_replay += 1
                    else:
                        pygame.time.set_timer(pygame.USEREVENT + 4, 0)

            # ----------------- EXIT BUTTON HOVER SOUND -----------------
            mouse_pos = pygame.mouse.get_pos()
            exit_hovered = hasattr(self, 'exit_rect') and self.exit_rect.collidepoint(mouse_pos)
            if exit_hovered and not self.exit_hovered_last:
                self.stop_hover_only()  # stop other hover sounds
                if self.exit_hover_sound:
                    self.exit_hover_sound.play()
            self.exit_hovered_last = exit_hovered

            # ----------------- Handle Feedback Timer -----------------
            if self.state == "feedback" and self.feedback_until > 0:
                if pygame.time.get_ticks() >= self.feedback_until:
                    # Stop feedback sound before moving on
                    if self.current_feedback_sound:
                        self.current_feedback_sound.stop()
                        self.current_feedback_sound = None

                    # Move to next question
                    self.current_idx += 1
                    if self.current_idx >= len(self.questions):
                        self.state = "results"
                    else:
                        self.state = "playing"
                        self.play_current_question_sound()

                    # Reset feedback
                    self.feedback_until = 0
                    self.feedback_correct = False
                    self.current_feedback_img = None

            self.draw()
        pygame.quit()

# ============================== Main ==============================
if __name__ == "__main__":
    app = AlphabitQuiz()
    app.run()
