# alphabit_pygame_quiz.py
# Pygame version of "ما هذا؟" quiz (converted from the Tkinter version)
# Requirements: pygame, pillow
# pip install pygame pillow

import os
import random
import pygame
from PIL import Image

# ==============================
# CONFIG (adapted from your Tkinter layout)
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "../assets")
IMG_PATH = os.path.join(ASSET_PATH, "img/alphabitSound")
SOUND_PATH = os.path.join(ASSET_PATH, "sounds/alphabitSound")

# Use your QUESTIONS structure; keep same filenames as in your assets
QUESTIONS = [
    {
        "sound": "01alef-s.wav",
        "options": ["01alef.png", "02ba.png", "03ta.png", "04tha.png"],
        "answer": 0,
        "option_size": (200, 200),
        "difficulty": "easy"
    },
    {
        "sound": "02ba-s.wav",
        "options": ["01alef-f.png", "01alef-k.png", "01alef-d.png", "01alef.png"],
        "answer": 0,
        "option_size": (250, 250),
        "difficulty": "hard"
    },
    {
        "sound": "01alef-s.wav",
        "options": ["01alef.png", "02ba.png", "03ta.png", "04tha.png"],
        "answer": 0,
        "option_size": (200, 200),
        "difficulty": "medium"
    },
    {
        "sound": "02ba-s.wav",
        "options": ["01alef-f.png", "01alef-k.png", "01alef-d.png", "01alef.png"],
        "answer": 0,
        "option_size": (250, 250),
        "difficulty": "hard"
    }
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

# ==============================
# Helper utilities
# ==============================
def load_image(path, convert_alpha=True):
    if not os.path.exists(path):
        print(f"⚠️ Missing image: {path}")
        return None
    try:
        if convert_alpha:
            return pygame.image.load(path).convert_alpha()
        else:
            return pygame.image.load(path).convert()
    except Exception as e:
        print(f"⚠️ Failed loading image {path}: {e}")
        return None

def load_sound(path):
    if not os.path.exists(path):
        print(f"⚠️ Missing sound: {path}")
        return None
    try:
        return pygame.mixer.Sound(path)
    except Exception as e:
        print(f"⚠️ Failed loading sound {path}: {e}")
        return None

# ==============================
# Game class
# ==============================
class AlphabitQuiz:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        # Fullscreen
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.W, self.H = self.screen.get_size()
        pygame.display.set_caption("ما هذا؟ 🧠 - Pygame Edition")

        # Fonts
        try:
            # try to use a font likely to support Arabic; fallback to default
            self.font_big = pygame.font.SysFont("Arial", 48, bold=True)
            self.font_med = pygame.font.SysFont("Arial", 36)
            self.font_small = pygame.font.SysFont("Arial", 28)
        except:
            self.font_big = pygame.font.Font(None, 48)
            self.font_med = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 28)

        # Load background
        bg_path = os.path.join(IMG_PATH, "soccerfield.png")
        self.bg_image = load_image(bg_path, convert_alpha=False)
        if self.bg_image:
            self.bg_image = pygame.transform.scale(self.bg_image, (self.W, self.H))
        else:
            # fallback fill color
            self.bg_image = None
            self.bg_color = (245, 245, 245)

        # Load difficulty icons (transparent PNGs)
        self.diff_images = {}
        for name in ("easy", "medium", "hard"):
            p = os.path.join(IMG_PATH, f"{name}.png")
            img = load_image(p, convert_alpha=True)
            if img:
                # scale to a reasonable size based on screen
                target_h = int(self.H * 0.6)  # tall cards
                scale = target_h / img.get_height()
                w = int(img.get_width() * scale * 0.6)  # narrower
                scaled = pygame.transform.smoothscale(img, (int(w), int(target_h*0.9)))
                self.diff_images[name] = scaled
            else:
                self.diff_images[name] = None

        # Load feedback thumbs
        self.thumb_up = load_image(os.path.join(IMG_PATH, "thumbsup.png"), True)
        self.thumb_down = load_image(os.path.join(IMG_PATH, "thumbsdown.png"), True)
        if self.thumb_up:
            self.thumb_up = pygame.transform.smoothscale(self.thumb_up, (300,300))
        if self.thumb_down:
            self.thumb_down = pygame.transform.smoothscale(self.thumb_down, (300,300))

        # Preload sounds (question & feedback) + background music
        self.loaded_sounds = {}
        sound_files = ["correct.wav", "wrong.wav", "welcome.wav"]
        for q in QUESTIONS:
            if q.get("sound"):
                sound_files.append(q["sound"])
        # unique only
        sound_files = list(dict.fromkeys(sound_files))
        for s in sound_files:
            path = os.path.join(SOUND_PATH, s)
            snd = load_sound(path)
            if snd:
                self.loaded_sounds[s] = snd

        # background music (loop)
        self.bg_music_path = os.path.join(SOUND_PATH, "bg_music.mp3")  # optional file name
        if os.path.exists(self.bg_music_path):
            try:
                pygame.mixer.music.load(self.bg_music_path)
                pygame.mixer.music.set_volume(0.4)  # base volume
            except Exception as e:
                print("⚠️ Failed to load background music:", e)
        else:
            # If no mp3 provided, that's fine; we won't play bg music.
            self.bg_music_path = None

        # State
        self.running = True
        self.state = "menu"  # menu, playing, feedback, results
        self.selected_difficulty = None
        self.questions = []  # list of questions for current session (shuffled)
        self.current_idx = 0
        self.score = 0
        self.feedback_timer = 0
        self.feedback_correct = False

        # UI geometry: positions for 3 difficulty images
        self.diff_positions = []
        self.prepare_menu_positions()

        # Option buttons geometry (set when showing a question)
        self.option_rects = []

        # Start music if available
        if self.bg_music_path:
            try:
                pygame.mixer.music.play(-1)
            except:
                pass

    def prepare_menu_positions(self):
        # center horizontally positions at 0.25, 0.5, 0.75 with some vertical center
        xs = [0.25, 0.5, 0.75]
        y = 0.55
        self.diff_positions = []
        for i, key in enumerate(("easy", "medium", "hard")):
            img = self.diff_images.get(key)
            if img:
                w, h = img.get_size()
                x = int(self.W * xs[i] - w // 2)
                yy = int(self.H * y - h // 2)
                self.diff_positions.append((key, pygame.Rect(x, yy, w, h)))
            else:
                # place an invisible rect as placeholder
                w, h = int(self.W * 0.15), int(self.H * 0.5)
                x = int(self.W * xs[i] - w // 2)
                yy = int(self.H * y - h // 2)
                self.diff_positions.append((key, pygame.Rect(x, yy, w, h)))

    def build_question_list_for(self, level):
        include = DIFFICULTY_MAP.get(level, [level])
        filtered = [q.copy() for q in QUESTIONS if q.get("difficulty") in include]
        # To avoid altering original, make sure each question copy is independent
        random.shuffle(filtered)
        return filtered

    def play_sfx(self, name, channel=0):
        # Play a preloaded sound by name; channel arg currently unused but kept for clarity
        snd = self.loaded_sounds.get(name)
        if snd:
            snd.play()
        else:
            print("⚠️ Sound not found:", name)

    def draw(self):
        # Draw background
        if self.bg_image:
            self.screen.blit(self.bg_image, (0,0))
        else:
            self.screen.fill(self.bg_color)

        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            self.draw_question()
        elif self.state == "feedback":
            self.draw_feedback()
        elif self.state == "results":
            self.draw_results()

        pygame.display.flip()

    def draw_menu(self):
        # Title
        title_surf = self.font_big.render("اختر المستوى", True, (255,255,255))
        title_rect = title_surf.get_rect(center=(self.W//2, int(self.H*0.12)))
        # draw a soft shadow for readability
        shadow = self.font_big.render("اختر المستوى", True, (0,0,0))
        self.screen.blit(shadow, (title_rect.x+2, title_rect.y+2))
        self.screen.blit(title_surf, title_rect)

        # draw difficulty icons
        for key, rect in self.diff_positions:
            img = self.diff_images.get(key)
            if img:
                self.screen.blit(img, rect.topleft)
            else:
                # draw placeholder rectangle with label
                pygame.draw.rect(self.screen, (200,200,200), rect, border_radius=12)
                txt = self.font_med.render(key, True, (20,20,20))
                self.screen.blit(txt, txt.get_rect(center=rect.center))

        # optional hint text
        hint = self.font_small.render("انقر على مستوى للبدء", True, (255,255,255))
        self.screen.blit(hint, hint.get_rect(center=(self.W//2, int(self.H*0.9))))

    def draw_question(self):
        # show progress
        total = len(self.questions)
        prog = f"{self.current_idx+1} / {total}"
        prog_surf = self.font_med.render(prog, True, (255,255,255))
        self.screen.blit(prog_surf, (int(self.W*0.9), int(self.H*0.05)))

        # play area: render options horizontally centered
        if not (0 <= self.current_idx < len(self.questions)):
            return

        q = self.questions[self.current_idx]
        # show play sound icon / replay button
        replay_text = self.font_small.render("🔊 إعادة الصوت (R)", True, (255,255,255))
        self.screen.blit(replay_text, (int(self.W*0.05), int(self.H*0.05)))

        # prepare option images and positions
        opts = q.get("options", [])
        count = len(opts)
        margin = 40
        # compute total width
        imgs = []
        for fname in opts:
            p = os.path.join(IMG_PATH, fname)
            img = load_image(p, True)
            if img:
                # scale to option size if provided
                ow, oh = q.get("option_size", (200,200))
                scaled = pygame.transform.smoothscale(img, (ow, oh))
                imgs.append(scaled)
            else:
                # placeholder
                surf = pygame.Surface((200,200), pygame.SRCALPHA)
                surf.fill((220,220,220,255))
                imgs.append(surf)
        total_w = sum(i.get_width() for i in imgs) + margin * (count - 1)
        start_x = (self.W - total_w)//2
        y = int(self.H * 0.4)
        self.option_rects = []
        for i, surf in enumerate(imgs):
            x = start_x + sum(imgs[j].get_width() + margin for j in range(i))
            rect = pygame.Rect(x, y, surf.get_width(), surf.get_height())
            self.screen.blit(surf, rect.topleft)
            # draw subtle border
            pygame.draw.rect(self.screen, (0,0,0,30), rect, 1)
            self.option_rects.append(rect)

    def draw_feedback(self):
        # Show the thumbs up/down centered, then after timer returns to next question or results
        if self.feedback_correct:
            img = self.thumb_up
        else:
            img = self.thumb_down

        if img:
            rect = img.get_rect(center=(self.W//2, self.H//2))
            # dim background
            dark = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
            dark.fill((0,0,0,120))
            self.screen.blit(dark, (0,0))
            self.screen.blit(img, rect.topleft)
        else:
            text = "صحيح" if self.feedback_correct else "خطأ"
            surf = self.font_big.render(text, True, (255,255,255))
            rect = surf.get_rect(center=(self.W//2, self.H//2))
            self.screen.blit(surf, rect)

    def draw_results(self):
        # dim background
        dark = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        dark.fill((0,0,0,160))
        self.screen.blit(dark, (0,0))

        msg = f"لقد حصلت على {self.score} من {len(self.questions)} 🎉"
        surf = self.font_big.render(msg, True, (255,255,255))
        rect = surf.get_rect(center=(self.W//2, int(self.H*0.35)))
        self.screen.blit(surf, rect)

        # buttons: replay, menu, exit (simple rectangles)
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

        # store rects for click detection
        self.results_buttons = {
            "restart": rect_restart,
            "menu": rect_menu,
            "exit": rect_exit
        }

    def handle_menu_event(self, mouse_pos):
        # check difficulty clicks
        for key, rect in self.diff_positions:
            if rect.collidepoint(mouse_pos):
                # if we don't have images for that key, ignore
                self.select_difficulty(key)
                return

    def select_difficulty(self, level):
        # assign and build question list
        self.selected_difficulty = level
        qs = self.build_question_list_for(level)
        if not qs:
            # no questions for selected difficulty
            print("⚠️ No questions for selected difficulty:", level)
            return
        self.questions = qs
        random.shuffle(self.questions)
        self.current_idx = 0
        self.score = 0
        self.state = "playing"
        # play welcome or first sound
        if "welcome.wav" in self.loaded_sounds:
            self.play_sfx("welcome.wav")
        # play the question sound immediately
        self.play_current_question_sound()

    def play_current_question_sound(self):
        if not (0 <= self.current_idx < len(self.questions)):
            return
        q = self.questions[self.current_idx]
        s = q.get("sound")
        if s:
            # option: temporarily reduce music volume for clarity
            if self.bg_music_path:
                current_vol = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(max(0.0, current_vol * 0.25))
                # schedule to bring back after 1.5s using a timer event
                pygame.time.set_timer(pygame.USEREVENT+2, 1500)
            self.play_sfx(s)

    def handle_playing_click(self, mouse_pos):
        # replay region? we used R key for replay; we won't implement a separate UI replay click here
        # check option rects
        for idx, rect in enumerate(self.option_rects):
            if rect.collidepoint(mouse_pos):
                # check answer
                self.check_answer(idx)
                break

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
        # switch to feedback display for 1.5s
        self.feedback_correct = correct
        self.feedback_timer = pygame.time.get_ticks() + 1500
        self.state = "feedback"

    def next_question_or_results(self):
        self.current_idx += 1
        if self.current_idx >= len(self.questions):
            self.state = "results"
        else:
            self.state = "playing"
            self.play_current_question_sound()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if self.state == "playing" and event.key == pygame.K_r:
                        # replay sound
                        self.play_current_question_sound()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if self.state == "menu":
                        self.handle_menu_event(pos)
                    elif self.state == "playing":
                        self.handle_playing_click(pos)
                    elif self.state == "results":
                        # check which results button clicked
                        for name, rect in self.results_buttons.items():
                            if rect.collidepoint(pos):
                                if name == "restart":
                                    # restart with same difficulty
                                    self.select_difficulty(self.selected_difficulty)
                                elif name == "menu":
                                    self.state = "menu"
                                elif name == "exit":
                                    self.running = False

                elif event.type == pygame.USEREVENT+2:
                    # restore music volume after short attenuation
                    pygame.mixer.music.set_volume(0.4)
                    pygame.time.set_timer(pygame.USEREVENT+2, 0)

            # Handle feedback timer
            if self.state == "feedback":
                if pygame.time.get_ticks() >= self.feedback_timer:
                    # close feedback and advance
                    self.next_question_or_results()

            # draw frame
            self.draw()

        # cleanup
        pygame.quit()


# ==============================
# Run the game
# ==============================
if __name__ == "__main__":
    game = AlphabitQuiz()
    game.run()
