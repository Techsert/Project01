# alphabit_pygame_quiz_with_hover.py
# Requires: pygame, pillow, arabic_reshaper, python-bidi
# pip install pygame pillow arabic_reshaper python-bidi

import os
import random
import pygame
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

# ==============================
# CONFIG
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "../assets")
IMG_PATH = os.path.join(ASSET_PATH, "img/alphabitSound")
SOUND_PATH = os.path.join(ASSET_PATH, "sounds/alphabitSound")
FONTS_PATH = os.path.join(ASSET_PATH, "fonts")

# Put an Arabic-capable TTF in ../assets/fonts/ (e.g. NotoNaskhArabic-Regular.ttf)
PREFERRED_ARABIC_FONTS = [
    os.path.join(FONTS_PATH, "NotoNaskhArabic-Regular.ttf"),
    os.path.join(FONTS_PATH, "arabic.ttf"),
    os.path.join(FONTS_PATH, "NotoSansArabic-Regular.ttf"),
]

def find_arabic_font():
    for p in PREFERRED_ARABIC_FONTS:
        if os.path.exists(p):
            return p
    # try some system fonts via pygame
    try:
        candidate = pygame.font.match_font("arial")
        if candidate:
            return candidate
    except Exception:
        pass
    return None

ARABIC_FONT_PATH = None  # assigned after pygame.init()

QUESTIONS = [
    {"sound": "01alef-s.wav", "options": ["01alef.png", "02ba.png", "03ta.png", "04tha.png"], "answer": 0, "option_size": (200,200), "difficulty": "easy"},
    {"sound": "02ba-s.wav", "options": ["01alef-f.png", "01alef-k.png", "01alef-d.png", "01alef.png"], "answer": 0, "option_size": (250,250), "difficulty": "hard"},
    {"sound": "01alef-s.wav", "options": ["01alef.png", "02ba.png", "03ta.png", "04tha.png"], "answer": 0, "option_size": (200,200), "difficulty": "medium"},
    {"sound": "02ba-s.wav", "options": ["01alef-f.png", "01alef-k.png", "01alef-d.png", "01alef.png"], "answer": 0, "option_size": (250,250), "difficulty": "hard"}
]

DIFFICULTY_MAP = {
    "easy": ["easy"],
    "medium": ["medium", "easy"],
    "hard": ["hard", "medium"]
}

# ==============================
# Helpers
# ==============================
def load_image(path, alpha=True):
    if not os.path.exists(path):
        # warning printed but continuing
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

def render_arabic_to_surface(text, font_path, size, color=(255,255,255)):
    """
    Use arabic_reshaper + python-bidi + PIL to render correct shaped RTL Arabic text
    and convert to a pygame.Surface with alpha. Falls back to pygame.font if unavailable.
    """
    if HAS_BIDI and font_path and os.path.exists(font_path):
        try:
            reshaped = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped)
            pil_font = ImageFont.truetype(font_path, size)
            # measure
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
            # fall back below
    # fallback - simple pygame font (no shaping, may look wrong)
    try:
        if font_path and os.path.exists(font_path):
            f = pygame.font.Font(font_path, size)
        else:
            f = pygame.font.SysFont("arial", size)
        surf = f.render(text, True, color)
        return surf.convert_alpha()
    except Exception as e:
        print("⚠️ Fallback rendering failed:", e)
        # return a tiny blank surface
        return pygame.Surface((1,1), pygame.SRCALPHA)

# ==============================
# Game class with hover animation & Arabic rendering
# ==============================
class AlphabitQuiz:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.hover_sounds = {}
        for level in ("easy","medium","hard"):
            path = os.path.join(SOUND_PATH, f"hover_{level}.wav")
            if os.path.exists(path):
                try:
                    self.hover_sounds[level] = pygame.mixer.Sound(path)
                except Exception as e:
                    print(f"⚠️ Failed to load hover sound {level}: {e}")
            else:
                print(f"⚠️ Missing hover sound file: {path}")

        global ARABIC_FONT_PATH
        ARABIC_FONT_PATH = find_arabic_font()

        self.state = "intro"           # intro sequence state
        self.intro_start_time = pygame.time.get_ticks()
        self.intro_delay = 11500        # 2 seconds before showing difficulty icons
        self.intro_sound_played = False
        self.show_menu_icons = False

        # load intro sound
        self.intro_sound = load_sound(os.path.join(SOUND_PATH, "WelcIntro.wav"))




        # Fullscreen window
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.W, self.H = self.screen.get_size()
        pygame.display.set_caption("ما هذا؟ 🧠 - Pygame (hover + Arabic)")

        # Fonts for non-Arabic fallback
        self.font_big = pygame.font.SysFont("arial", 48, bold=True)
        self.font_med = pygame.font.SysFont("arial", 36)
        self.font_small = pygame.font.SysFont("arial", 28)

        # hover sound tracking
        self.last_hovered = None

        # Load background
        bg_path = os.path.join(IMG_PATH, "soccerfield.png")
        self.bg = load_image(bg_path, alpha=False)
        if self.bg:
            self.bg = pygame.transform.smoothscale(self.bg, (self.W, self.H))
        else:
            self.bg = None
            self.bg_color = (20,120,20)

        # Load difficulty images (original surfaces)
        self.diff_orig = {}
        for d in ("easy","medium","hard"):
            p = os.path.join(IMG_PATH, f"{d}.png")
            img = load_image(p, alpha=True)
            if img:
                # reduce to reasonable size
                max_h = int(self.H * 0.6)
                scale = max_h / img.get_height()
                w = int(img.get_width() * scale * 0.8)
                h = int(max_h * 0.9)
                img = pygame.transform.smoothscale(img, (w,h))
            self.diff_orig[d] = img

        # hover state dict
        # each: { 'orig': surface, 'scale': float, 'target': float }
        self.diff_state = {}
        for d in ("easy","medium","hard"):
            orig = self.diff_orig.get(d)
            if orig:
                self.diff_state[d] = {'orig': orig, 'scale': 1.0, 'target': 1.0}
            else:
                # placeholder rect if no image
                placeholder = pygame.Surface((int(self.W*0.15), int(self.H*0.5)), pygame.SRCALPHA)
                placeholder.fill((200,200,200,255))
                self.diff_state[d] = {'orig': placeholder, 'scale': 1.0, 'target': 1.0}
        self.last_hovered = None
    
        # menu positions (centers)
        self.diff_centers = [
            (int(self.W*0.25), int(self.H*0.55)),
            (int(self.W*0.5), int(self.H*0.55)),
            (int(self.W*0.75), int(self.H*0.55))
        ]

        # load thumbs, sounds, music
        self.thumb_up = load_image(os.path.join(IMG_PATH, "thumbsup.png"), True)
        self.thumb_down = load_image(os.path.join(IMG_PATH, "thumbsdown.png"), True)
        if self.thumb_up: self.thumb_up = pygame.transform.smoothscale(self.thumb_up, (300,300))
        if self.thumb_down: self.thumb_down = pygame.transform.smoothscale(self.thumb_down, (300,300))

        # sounds
        self.loaded_sounds = {}
        pre_sounds = ["correct.wav", "wrong.wav", "welcome.wav"]
        for q in QUESTIONS:
            if q.get("sound"):
                pre_sounds.append(q["sound"])
        for s in set(pre_sounds):
            path = os.path.join(SOUND_PATH, s)
            snd = load_sound(path)
            if snd:
                self.loaded_sounds[s] = snd

        # bg music optional
        self.bg_music_path = os.path.join(SOUND_PATH, "bg_music.mp3")
        if os.path.exists(self.bg_music_path):
            try:
                pygame.mixer.music.load(self.bg_music_path)
                pygame.mixer.music.set_volume(0.35)
                pygame.mixer.music.play(-1)
            except Exception as e:
                print("⚠️ Failed to play bg music:", e)
        else:
            self.bg_music_path = None

        # ----------------------
        # VOLUME SETTINGS
        # ----------------------
        self.volume_bg = 0.15         # background music
        self.volume_intro = 1.0       # intro sound
        self.volume_hover = 0.8       # hover sounds
        self.volume_questions = 1.0   # question sounds
        self.volume_feedback = 1.0    # correct/wrong/welcome

        # set hover volumes
        for snd in self.hover_sounds.values():
            snd.set_volume(self.volume_hover)

        # set intro volume
        if self.intro_sound:
            self.intro_sound.set_volume(self.volume_intro)

        # set question & feedback volumes
        for snd in self.loaded_sounds.values():
            snd.set_volume(self.volume_questions)

        # set background music volume
        if self.bg_music_path:
            pygame.mixer.music.set_volume(self.volume_bg)
            

        # game state
##        self.state = "menu"  # menu, playing, feedback, results
        self.state = "intro"
        self.selected_difficulty = None
        self.questions = []
        self.current_idx = 0
        self.score = 0
        self.feedback_until = 0
        self.feedback_correct = False

        # dynamic rects updated each frame
        self.menu_rects = {}  # key -> rect for current scaled image
        self.results_buttons = {}  # set when drawing results

    # play sfx if loaded
    def play_sfx(self, name):
        s = self.loaded_sounds.get(name)
        if s:
            s.play()
        else:
            print("⚠️ Sound not found:", name)

    def build_question_list_for(self, level):
        include = DIFFICULTY_MAP.get(level, [level])
        filtered = [q.copy() for q in QUESTIONS if q.get("difficulty") in include]
        random.shuffle(filtered)
        return filtered

    def select_difficulty(self, level):
        self.selected_difficulty = level
        qs = self.build_question_list_for(level)
        if not qs:
            print("⚠️ No questions for:", level)
            return
        self.questions = qs
        self.current_idx = 0
        self.score = 0
        self.state = "playing"
        # play welcome if exists
        if "welcome.wav" in self.loaded_sounds:
            self.play_sfx("welcome.wav")
        # play first question sound
        pygame.time.set_timer(pygame.USEREVENT+3, 300, True)  # small delay to let music attenuate
        # (play question sound immediately in event handling after timer if needed)
        self.play_current_question_sound()

    def play_current_question_sound(self):
        if not (0 <= self.current_idx < len(self.questions)):
            return
        s = self.questions[self.current_idx].get("sound")
        if s:
            # stop any hover sounds before playing question sound
            for snd in self.hover_sounds.values():
                snd.stop()
            self.play_sfx(s)  # play at the volume set earlier
            # attenuate music quickly if present
            if self.bg_music_path:
                oldv = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(max(0, oldv * 0.25))  # attenuate
                pygame.time.set_timer(pygame.USEREVENT+2, 1400, True) # restore after 1.4 sec
            self.play_sfx(s)

    def update_menu_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        hovered_any = False

        for idx, key in enumerate(("easy", "medium", "hard")):
            st = self.diff_state[key]
            orig = st['orig']
            scale = st['scale']

            # compute current scaled size
            ow, oh = orig.get_size()
            scaled_w = int(ow * scale)
            scaled_h = int(oh * scale)
            cx, cy = self.diff_centers[idx]
            rect = pygame.Rect(int(cx - scaled_w//2), int(cy - scaled_h//2), scaled_w, scaled_h)
            self.menu_rects[key] = rect

            if rect.collidepoint(mouse_pos):
                st['target'] = 1.08
                hovered_any = True

                # play hover sound only once per hover
                if self.last_hovered != key:
                    snd = self.hover_sounds.get(key)
                    if snd:
                        # stop any other hover sounds first
                        for s in self.hover_sounds.values():
                            s.stop()
                        snd.play()
                    self.last_hovered = key

                try:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                except Exception:
                    pass
            else:
                st['target'] = 1.0

        if not hovered_any:
            self.last_hovered = None
            try:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            except Exception:
                pass

        # smooth interpolate scales
        for key, st in self.diff_state.items():
            st['scale'] += (st['target'] - st['scale']) * 0.18



    def draw_menu(self):
        # Title (Arabic)
        title_surf = render_arabic_to_surface("اختر المستوى", ARABIC_FONT_PATH or "", 64, color=(255,255,255))
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.W//2, int(self.H*0.12))))

        # icons
        for idx, key in enumerate(("easy","medium","hard")):
            st = self.diff_state[key]
            orig = st['orig']
            scale = st['scale']
            ow, oh = orig.get_size()
            sw = int(ow * scale)
            sh = int(oh * scale)
            cx, cy = self.diff_centers[idx]
            surf = pygame.transform.smoothscale(orig, (sw, sh))
            # slight lift on hover (based on scale)
            lift = int((scale - 1.0) * 20)
            pos = (int(cx - sw//2), int(cy - sh//2) - lift)
            self.screen.blit(surf, pos)
            # update rect for this draw (used for clicks)
            self.menu_rects[key] = pygame.Rect(pos[0], pos[1], sw, sh)

        hint = render_arabic_to_surface("انقر على مستوى للبدء", ARABIC_FONT_PATH or "", 28, color=(255,255,255))
        self.screen.blit(hint, hint.get_rect(center=(self.W//2, int(self.H*0.9))))

    def draw_playing(self):
        # show progress (use Arabic numbers if you prefer; here we keep normal numbers)
        total = len(self.questions)
        prog_text = f"{self.current_idx+1} / {total}"
        prog_surf = self.font_med.render(prog_text, True, (255,255,255))
        self.screen.blit(prog_surf, prog_surf.get_rect(topright=(self.W-20, 20)))

        # replay hint (R)
        replay_surf = render_arabic_to_surface("🔊 إعادة الصوت (R)", ARABIC_FONT_PATH or "", 26, color=(255,255,255))
        self.screen.blit(replay_surf, (20, 20))

        # draw options
        if not (0 <= self.current_idx < len(self.questions)):
            return
        q = self.questions[self.current_idx]
        opts = q.get("options", [])
        count = len(opts)
        margin = 40
        imgs = []
        for fname in opts:
            p = os.path.join(IMG_PATH, fname)
            img = load_image(p, alpha=True)
            if img:
                ow, oh = q.get("option_size", (200,200))
                surf = pygame.transform.smoothscale(img, (ow, oh))
            else:
                surf = pygame.Surface((200,200), pygame.SRCALPHA)
                surf.fill((240,240,240,255))
            imgs.append(surf)
        total_w = sum(i.get_width() for i in imgs) + margin*(count-1)
        start_x = (self.W - total_w)//2
        y = int(self.H*0.35)
        self.option_rects = []
        for i, surf in enumerate(imgs):
            x = start_x + sum(imgs[j].get_width() + margin for j in range(i))
            rect = pygame.Rect(x, y, surf.get_width(), surf.get_height())
            self.screen.blit(surf, rect.topleft)
            pygame.draw.rect(self.screen, (0,0,0), rect, 1)
            self.option_rects.append(rect)

    def draw_feedback(self):
        dark = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        dark.fill((0,0,0,120))
        self.screen.blit(dark, (0,0))
        img = self.thumb_up if self.feedback_correct else self.thumb_down
        if img:
            rect = img.get_rect(center=(self.W//2, self.H//2))
            self.screen.blit(img, rect.topleft)
        else:
            text = "صحيح" if self.feedback_correct else "خطأ"
            surf = render_arabic_to_surface(text, ARABIC_FONT_PATH or "", 64, color=(255,255,255))
            self.screen.blit(surf, surf.get_rect(center=(self.W//2, self.H//2)))

    def draw_results(self):
        dark = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        dark.fill((0,0,0,160))
        self.screen.blit(dark, (0,0))
        msg = f"لقد حصلت على {self.score} من {len(self.questions)} 🎉"
        surf = render_arabic_to_surface(msg, ARABIC_FONT_PATH or "", 48, color=(255,255,255))
        self.screen.blit(surf, surf.get_rect(center=(self.W//2, int(self.H*0.35))))

        # buttons as rectangles
        btn_w, btn_h = 360, 80
        spacing = 40
        total_w = btn_w*3 + spacing*2
        start_x = (self.W - total_w)//2
        y = int(self.H*0.55)
        rect_restart = pygame.Rect(start_x, y, btn_w, btn_h)
        rect_menu = pygame.Rect(start_x + btn_w + spacing, y, btn_w, btn_h)
        rect_exit = pygame.Rect(start_x + (btn_w+spacing)*2, y, btn_w, btn_h)
        pygame.draw.rect(self.screen, (200,230,255), rect_restart, border_radius=12)
        pygame.draw.rect(self.screen, (255,240,200), rect_menu, border_radius=12)
        pygame.draw.rect(self.screen, (255,200,200), rect_exit, border_radius=12)
        self.screen.blit(self.font_med.render("🔁 إعادة اللعب", True, (0,0,0)), (rect_restart.x+40, rect_restart.y+20))
        self.screen.blit(self.font_med.render("🏠 العودة إلى القائمة", True, (0,0,0)), (rect_menu.x+20, rect_menu.y+20))
        self.screen.blit(self.font_med.render("⏪ إنهاء", True, (0,0,0)), (rect_exit.x+120, rect_exit.y+20))
        self.results_buttons = {"restart": rect_restart, "menu": rect_menu, "exit": rect_exit}

    def draw(self):
        # draw background
        if self.bg:
            self.screen.blit(self.bg, (0,0))
        else:
            self.screen.fill(self.bg_color)

        if self.state == "intro":
            # play intro sound once
            if not self.intro_sound_played and self.intro_sound:
                self.intro_sound.play()
                self.intro_sound_played = True

            # check if delay passed
            if pygame.time.get_ticks() - self.intro_start_time >= self.intro_delay:
                self.show_menu_icons = True
                self.state = "menu"

            # optionally draw a title or animation here while waiting
##            title_surf = render_arabic_to_surface("loading", ARABIC_FONT_PATH or "", 64, color=(255,255,255))
##            self.screen.blit(title_surf, title_surf.get_rect(center=(self.W//2, int(self.H*0.3))))

        if self.state == "menu":
            if self.show_menu_icons:
                self.update_menu_hover()
                self.draw_menu()

        elif self.state == "playing":
            self.draw_playing()
        elif self.state == "feedback":
            self.draw_feedback()
        elif self.state == "results":
            self.draw_results()

        pygame.display.flip()



    def handle_click_menu(self, pos):
        for key, rect in self.menu_rects.items():
            if rect.collidepoint(pos):
                self.select_difficulty(key)
                return

    def handle_click_playing(self, pos):
        for idx, rect in enumerate(self.option_rects):
            if rect.collidepoint(pos):
                self.check_answer(idx)
                return

    def check_answer(self, idx):
        if not (0 <= self.current_idx < len(self.questions)):
            return
        q = self.questions[self.current_idx]
        correct = (idx == q.get("answer", 0))
        if correct:
            self.score += 1
            self.play_sfx("correct.wav")
        else:
            self.play_sfx("wrong.wav")
        self.feedback_correct = correct
        self.feedback_until = pygame.time.get_ticks() + 1500
        self.state = "feedback"

    def next_or_results(self):
        self.current_idx += 1
        if self.current_idx >= len(self.questions):
            self.state = "results"
        else:
            self.state = "playing"
            self.play_current_question_sound()

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
                        # Toggle fullscreen instead of quitting
                        fullscreen = self.screen.get_flags() & pygame.FULLSCREEN
                        if fullscreen:
                            pygame.display.set_mode((1280, 720))  # switch to windowed
                        else:
                            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        self.W, self.H = self.screen.get_size()
                        if self.bg:
                            self.bg = pygame.transform.smoothscale(self.bg, (self.W, self.H))
                        # update positions if needed
                        self.diff_centers = [
                            (int(self.W*0.25), int(self.H*0.55)),
                            (int(self.W*0.5), int(self.H*0.55)),
                            (int(self.W*0.75), int(self.H*0.55))
                        ]

                    if event.key == pygame.K_r and self.state == "playing":
                        self.play_current_question_sound()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = event.pos
                        if self.state == "menu":
                            self.handle_click_menu(pos)
                        elif self.state == "playing":
                            self.handle_click_playing(pos)
                        elif self.state == "results":
                            for name, rect in self.results_buttons.items():
                                if rect.collidepoint(pos):
                                    if name == "restart":
                                        self.select_difficulty(self.selected_difficulty)
                                    elif name == "menu":
                                        self.state = "menu"
                                    elif name == "exit":
                                        running = False
                elif event.type == pygame.USEREVENT+2:
                    # restore music volume
                    if self.bg_music_path:
                        pygame.mixer.music.set_volume(0.35)
                elif event.type == pygame.USEREVENT+3:
                    # optional small timer, ignored
                    pass

            # feedback timeout
            if self.state == "feedback" and pygame.time.get_ticks() >= self.feedback_until:
                self.next_or_results()

            # draw frame
            self.draw()

        pygame.quit()

# ==============================
# Run
# ==============================
if __name__ == "__main__":
    game = AlphabitQuiz()
    game.run()
