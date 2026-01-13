import os
import json
import pygame
import arabic_reshaper
from bidi.algorithm import get_display
from alphabit_name import run_alphabit_name
from alphabit_sound import run_alphabit_sound

# ===========================
# CONFIG
# ===========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(BASE_DIR, "../assets/img/main")
SOUND_PATH = os.path.join(BASE_DIR, "../assets/sounds/main")
AVATAR_PATH = os.path.join(BASE_DIR, "../assets/img/avatars")
ARABIC_FONT_PATH = os.path.join(BASE_DIR, "../assets/fonts/NotoNaskhArabic-Regular.ttf")
ARABIC_BOLD_FONT_PATH = os.path.join(BASE_DIR, "../assets/fonts/NotoNaskhArabic-Bold.ttf")
PROFILES_FILE = os.path.join(BASE_DIR, "profiles.json")

pygame.init()
pygame.mixer.init()
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Learning World - Level One")
clock = pygame.time.Clock()

# ---------------------------
# Helper functions
# ---------------------------
def load_font(size, bold=False):
    font_path = ARABIC_BOLD_FONT_PATH if bold else ARABIC_FONT_PATH
    try:
        return pygame.font.Font(font_path, size)
    except:
        return pygame.font.SysFont("Arial", size)

def load_image(path, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img, (width, height))
    except:
        return None

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        return None

def load_profiles():
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_profiles(profiles):
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)

# ===========================
# Main QuizApp Class
# ===========================
class QuizApp:
    def __init__(self):
        self.running = True
        self.show_profile_screen = False
        self.show_welcome = False
        self.hovered_button = None
        self.hover_channel = pygame.mixer.Channel(5)
        self.start_sound_path = os.path.join(SOUND_PATH, "lets_start.mp3")

        # Load backgrounds
        self.welcome_bg = load_image(os.path.join(IMG_PATH, "background.png"))
        self.section_bg = load_image(os.path.join(IMG_PATH, "section_bg.png"))

        # Section buttons
        self.section_buttons = [
            {"pos": (0.15, 0.36), "text": "أسماء الحُروف", "action": self.launch_alphabit_name, "hover": os.path.join(SOUND_PATH, "hover_alphabetNames.wav")},
            {"pos": (0.50, 0.36), "text": "أصوات الحُروف", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_alphabetSounds.wav")},
            {"pos": (0.85, 0.36), "text": "أشكال الحُروف", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_alphabetShaps.wav")},
            {"pos": (0.15, 0.89), "text": "الأعداد", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_numbers.wav")},
            {"pos": (0.50, 0.89), "text": "الألوان", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_colours.wav")},
            {"pos": (0.85, 0.89), "text": "الكَلِمات", "action": self.launch_alphabit_sound, "hover": os.path.join(SOUND_PATH, "hover_words.wav")},
        ]

        # Precompute rects
        for btn in self.section_buttons:
            x = int(btn["pos"][0]*SCREEN_WIDTH)
            y = int(btn["pos"][1]*SCREEN_HEIGHT)
            w, h = SCREEN_WIDTH*0.25, SCREEN_HEIGHT*0.1
            btn["rect"] = pygame.Rect(x-w//2, y-h//2, w, h)

        # Start button
        self.start_rect = pygame.Rect(
            int(SCREEN_WIDTH*0.45)-SCREEN_WIDTH*0.15//2,
            int(SCREEN_HEIGHT*0.65)-SCREEN_HEIGHT*0.2//2,
            SCREEN_WIDTH*0.15, SCREEN_HEIGHT*0.2
        )

        # Profiles
        self.profiles = load_profiles()
        self.current_profile = None

        # Background music
        self.bg_music = os.path.join(SOUND_PATH, "bg_sound.mp3")
        self.play_bg_music()

    # ---------------------------
    # Arabic text
    # ---------------------------
    def draw_arabic_text(self, text, size, color, center, bold=False):
        reshaped = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped)
        font = load_font(size, bold)
        rendered = font.render(bidi_text, True, color)
        rect = rendered.get_rect(center=center)
        screen.blit(rendered, rect)

    # ---------------------------
    # Background music & hover
    # ---------------------------
    def play_bg_music(self):
        try:
            pygame.mixer.music.load(self.bg_music)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except:
            pass

    def play_hover_sound(self, path):
        sound = load_sound(path)
        if sound:
            if self.hover_channel.get_busy():
                self.hover_channel.stop()
            self.hover_channel.play(sound)

    def start_with_delay(self):
        sound = load_sound(self.start_sound_path)
        if sound:
            sound.play()
            pygame.time.set_timer(pygame.USEREVENT+1, int(sound.get_length()*1000))

    # ---------------------------
    # Profile screens
    # ---------------------------
    def draw_profile_screen(self):
        screen.fill((255,255,255))
        self.draw_arabic_text("اختر الملف الشخصي", 120, (51,51,51), (SCREEN_WIDTH//2, SCREEN_HEIGHT*0.15), bold=True)

        self.profile_buttons = []
        y_start = SCREEN_HEIGHT*0.3
        button_height = SCREEN_HEIGHT*0.12
        spacing = SCREEN_HEIGHT*0.18

        for i, profile in enumerate(self.profiles):
            rect = pygame.Rect(SCREEN_WIDTH*0.35, y_start+i*spacing, SCREEN_WIDTH*0.3, button_height)
            pygame.draw.rect(screen, (255,255,255), rect, border_radius=30)
            pygame.draw.rect(screen, (255,102,0), rect, 5, border_radius=30)
            self.draw_arabic_text(profile["name"], 80, (255,102,0), rect.center, bold=True)
            self.profile_buttons.append(rect)

        # New profile button
        self.new_profile_rect = pygame.Rect(SCREEN_WIDTH*0.35, y_start+len(self.profiles)*spacing, SCREEN_WIDTH*0.3, button_height)
        pygame.draw.rect(screen, (255,255,255), self.new_profile_rect, border_radius=30)
        pygame.draw.rect(screen, (0,200,0), self.new_profile_rect, 5, border_radius=30)
        self.draw_arabic_text("ملف جديد", 80, (0,200,0), self.new_profile_rect.center, bold=True)

    def handle_profile_click(self, mouse_pos):
        for i, rect in enumerate(self.profile_buttons):
            if rect.collidepoint(mouse_pos):
                self.current_profile = self.profiles[i]
                self.verify_pin(self.current_profile)
                return
        if self.new_profile_rect.collidepoint(mouse_pos):
            self.create_profile()

    # Profile PIN verification
    def verify_pin(self, profile):
        pin_input = ""
        message = ""
        entering = True
        while entering:
            screen.fill((255,255,255))
            self.draw_arabic_text(f"أدخل PIN لملف {profile['name']}", 60, (0,0,0), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-100))
            pin_rect = pygame.Rect(SCREEN_WIDTH//2-200, SCREEN_HEIGHT//2, 400, 80)
            pygame.draw.rect(screen, (200,200,200), pin_rect)
            self.draw_arabic_text("*"*len(pin_input) or "أدخل PIN", 50, (0,0,0), pin_rect.center)
            self.draw_arabic_text(message, 40, (255,0,0), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+100))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    entering=False
                    self.running=False
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        entering=False
                    elif event.key==pygame.K_BACKSPACE:
                        pin_input=pin_input[:-1]
                    elif event.unicode.isprintable():
                        pin_input+=event.unicode
                    elif event.key==pygame.K_RETURN:
                        if pin_input==profile["pin"]:
                            entering=False
                            self.show_profile_screen=False
                            self.show_welcome=True
                        else:
                            message="PIN غير صحيح!"
                            pin_input=""
            pygame.display.flip()
            clock.tick(60)

    # ---------------------------
    # Profile creation
    # ---------------------------
    def create_profile(self):
        name=""
        pin=""
        avatar_files=os.listdir(AVATAR_PATH)
        avatar_index=0
        entering=True
        while entering:
            screen.fill((255,255,255))
            self.draw_arabic_text("إنشاء ملف جديد", 80, (0,0,0), (SCREEN_WIDTH//2, SCREEN_HEIGHT*0.1), bold=True)
            # Name
            name_rect=pygame.Rect(SCREEN_WIDTH//2-200, SCREEN_HEIGHT//2-100,400,80)
            pygame.draw.rect(screen,(200,200,200),name_rect)
            self.draw_arabic_text(name or "أدخل الاسم",50,(0,0,0),name_rect.center)
            # PIN
            pin_rect=pygame.Rect(SCREEN_WIDTH//2-200, SCREEN_HEIGHT//2+20,400,80)
            pygame.draw.rect(screen,(200,200,200),pin_rect)
            self.draw_arabic_text("*"*len(pin) or "أدخل PIN",50,(0,0,0),pin_rect.center)
            # Avatar
            avatar_img=load_image(os.path.join(AVATAR_PATH,avatar_files[avatar_index]),150,150)
            avatar_rect=avatar_img.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+180))
            screen.blit(avatar_img, avatar_rect)
            self.draw_arabic_text("اضغط لتغيير الصورة",40,(0,0,0),(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+270))
            # Confirm
            confirm_rect=pygame.Rect(SCREEN_WIDTH//2-100, SCREEN_HEIGHT-150,200,80)
            pygame.draw.rect(screen,(100,200,100),confirm_rect,border_radius=20)
            self.draw_arabic_text("تأكيد",50,(255,255,255),confirm_rect.center,bold=True)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    entering=False
                    self.running=False
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        entering=False
                    elif event.key==pygame.K_BACKSPACE:
                        if name_rect.collidepoint(pygame.mouse.get_pos()):
                            name=name[:-1]
                        elif pin_rect.collidepoint(pygame.mouse.get_pos()):
                            pin=pin[:-1]
                    elif event.unicode.isprintable():
                        if name_rect.collidepoint(pygame.mouse.get_pos()):
                            name+=event.unicode
                        elif pin_rect.collidepoint(pygame.mouse.get_pos()):
                            pin+=event.unicode
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    if avatar_rect.collidepoint(event.pos):
                        avatar_index=(avatar_index+1)%len(avatar_files)
                    elif confirm_rect.collidepoint(event.pos):
                        if name.strip() and pin.strip():
                            profile={"name":name,"avatar":avatar_files[avatar_index],"pin":pin}
                            self.profiles.append(profile)
                            save_profiles(self.profiles)
                            self.current_profile=profile
                            entering=False
                            self.show_profile_screen=False
                            self.show_welcome=True
            pygame.display.flip()
            clock.tick(60)

    # ---------------------------
    # Section buttons
    # ---------------------------
    def draw_button(self, btn):
        self.draw_arabic_text(btn["text"],150,(51,51,51),btn["rect"].center)

    def launch_alphabit_name(self):
        pygame.mixer.stop()
        run_alphabit_name(screen,self)

    def launch_alphabit_sound(self):
        pygame.mixer.stop()
        run_alphabit_sound(screen,main_app=self)

    # ---------------------------
    # Main loop
    # ---------------------------
    def run(self):
        # First screen
        if not self.profiles:
            self.create_profile()
        else:
            self.show_profile_screen = True
            self.show_welcome = False

        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            screen.fill((255,255,255))

            # --- Screens ---
            if self.show_profile_screen:
                self.draw_profile_screen()
            elif self.show_welcome:
                if self.welcome_bg:
                    screen.blit(self.welcome_bg, (0,0))
                self.draw_arabic_text("مرحباً", 250, (51,51,51), (SCREEN_WIDTH//2, SCREEN_HEIGHT//3), bold=True)
                pygame.draw.rect(screen, (255,255,255), self.start_rect, border_radius=30)
                pygame.draw.rect(screen, (255,102,0), self.start_rect, 5, border_radius=30)
                self.draw_arabic_text("هيا نبدأ", 150, (255,102,0), self.start_rect.center, bold=True)
            else:
                if self.section_bg:
                    screen.blit(self.section_bg, (0,0))
                for btn in self.section_buttons:
                    self.draw_button(btn)

            # --- Draw profile avatar on all screens ---
            if self.current_profile and "avatar" in self.current_profile:
                avatar_img = load_image(os.path.join(AVATAR_PATH, self.current_profile["avatar"]), 80, 80)
                if avatar_img:
                    screen.blit(avatar_img, (10, 10))

            # --- Event handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.show_profile_screen:
                        self.handle_profile_click(mouse_pos)
                    elif self.show_welcome:
                        if self.start_rect.collidepoint(mouse_pos):
                            self.start_with_delay()
                    else:
                        for btn in self.section_buttons:
                            if btn["rect"].collidepoint(mouse_pos):
                                btn["action"]()
                elif event.type == pygame.MOUSEMOTION and not self.show_welcome and not self.show_profile_screen:
                    hovered = None
                    for btn in self.section_buttons:
                        if btn["rect"].collidepoint(mouse_pos):
                            hovered = btn
                            break
                    if hovered != self.hovered_button:
                        self.hovered_button = hovered
                        if hovered:
                            self.play_hover_sound(hovered["hover"])
                elif event.type == pygame.USEREVENT + 1:
                    self.show_welcome = False
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


# ===========================
# RUN
# ===========================
if __name__=="__main__":
    app=QuizApp()
    app.run()
