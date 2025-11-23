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
ARABIC_FONT_PATH = os.path.join(BASE_DIR, "../assets/fonts/NotoNaskhArabic-Regular.ttf")
ARABIC_BOLD_FONT_PATH = os.path.join(BASE_DIR, "../assets/fonts/NotoNaskhArabic-Bold.ttf")
PROFILES_FILE = os.path.join(BASE_DIR, "profiles.json")
AVATAR_PATH = os.path.join(BASE_DIR, "../assets/img/avatars")  # folder with avatar options

pygame.init()
pygame.mixer.init()

info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = int(info.current_w * 0.9), int(info.current_h * 0.9)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # windowed, not fullscreen
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
        print("no FOOONT")
        return pygame.font.SysFont("Arial", size)

def load_image(path, width=None, height=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if width and height:
            img = pygame.transform.smoothscale(img, (width, height))
        return img
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

# ---------------------------
# Main App
# ---------------------------
class QuizApp:
    def __init__(self):
        self.running = True
        self.show_profile_screen = True  # Start with profile selection
        self.show_welcome = False
        self.show_new_profile = False
        self.hovered_button = None
        self.hover_channel = pygame.mixer.Channel(5)

        # Load profiles
        self.profiles = load_profiles()
        self.current_profile = None
        self.selected_avatar_index = 0

        # Load images
        self.welcome_bg = pygame.image.load(os.path.join(IMG_PATH, "background.png")).convert()
        self.section_bg = pygame.image.load(os.path.join(IMG_PATH, "section_bg.png")).convert()

        # Scale them to fit the screen exactly
        self.welcome_bg = pygame.transform.scale(self.welcome_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.section_bg = pygame.transform.scale(self.section_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))


        # Section buttons
        self.section_buttons = [
            {"pos": (0.15, 0.36), "text": "أسماء الحُروف", "action": self.launch_alphabit_name},
            {"pos": (0.50, 0.36), "text": "أصوات الحُروف", "action": self.launch_alphabit_sound},
            {"pos": (0.85, 0.36), "text": "أشكال الحُروف", "action": self.launch_alphabit_sound},
            {"pos": (0.15, 0.89), "text": "الأعداد", "action": self.launch_alphabit_sound},
            {"pos": (0.50, 0.89), "text": "الألوان", "action": self.launch_alphabit_sound},
            {"pos": (0.85, 0.89), "text": "الكَلِمات", "action": self.launch_alphabit_sound},
        ]
        # Precompute rects
        for btn in self.section_buttons:
            x = int(btn["pos"][0] * SCREEN_WIDTH)
            y = int(btn["pos"][1] * SCREEN_HEIGHT)
            w, h = SCREEN_WIDTH*0.25, SCREEN_HEIGHT*0.1
            btn["rect"] = pygame.Rect(x-w//2, y-h//2, w, h)

        # Start button
        self.start_rect = pygame.Rect(
            int(SCREEN_WIDTH * 0.45) - SCREEN_WIDTH * 0.15 // 2,
            int(SCREEN_HEIGHT * 0.65) - SCREEN_HEIGHT * 0.2 // 2,
            SCREEN_WIDTH*0.15, SCREEN_HEIGHT*0.2
        )

    # ---------------------------
    # Arabic text rendering
    # ---------------------------
    def draw_arabic_text(self, text, size, color, center, bold=False):
        reshaped = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped)
        font = load_font(size, bold)
        rendered = font.render(bidi_text, True, color)
        rect = rendered.get_rect(center=center)
        screen.blit(rendered, rect)
        return rect

    # ---------------------------
    # Profile screens
    # ---------------------------
    def draw_profile_screen(self):
        screen.fill((255,255,255))
        self.draw_arabic_text("اختر ملفك الشخصي", 150, (0,0,0), (SCREEN_WIDTH//2, SCREEN_HEIGHT*0.1), bold=True)

        profile_rects = []
        edit_rects = []
        delete_rects = []

        for idx, profile in enumerate(self.profiles):
            x = SCREEN_WIDTH*(0.25 + idx*0.25)
            y = SCREEN_HEIGHT*0.4
            avatar_img = load_image(os.path.join(AVATAR_PATH, profile.get("avatar","")), 150,150)
            if avatar_img:
                rect = avatar_img.get_rect(center=(x,y))
                screen.blit(avatar_img, rect)
                profile_rects.append((rect, profile))
                self.draw_arabic_text(profile.get("name",""), 40, (0,0,0), (x, y+100))

            # Edit button
            edit_rect = pygame.Rect(x-60, y+150, 50, 50)
            pygame.draw.rect(screen, (0,102,255), edit_rect)
            self.draw_arabic_text("✎", 40, (255,255,255), edit_rect.center)
            edit_rects.append((edit_rect, profile))

            # Delete button
            delete_rect = pygame.Rect(x+10, y+150, 50, 50)
            pygame.draw.rect(screen, (255,0,0), delete_rect)
            self.draw_arabic_text("🗑", 40, (255,255,255), delete_rect.center)
            delete_rects.append((delete_rect, profile))

        # Add new profile button
        add_rect = pygame.Rect(SCREEN_WIDTH//2-150, SCREEN_HEIGHT*0.7, 300, 80)
        pygame.draw.rect(screen, (100,200,100), add_rect, border_radius=20)
        self.draw_arabic_text("إضافة ملف جديد", 50, (255,255,255), add_rect.center, bold=True)

        return profile_rects, edit_rects, delete_rects, add_rect

    def draw_background(self, image):
        if not image:
            screen.fill((255, 255, 255))
            return

        img_w, img_h = image.get_size()
        scale = min(SCREEN_WIDTH / img_w, SCREEN_HEIGHT / img_h)
        new_size = (int(img_w * scale), int(img_h * scale))
        scaled_img = pygame.transform.smoothscale(image, new_size)

        x = (SCREEN_WIDTH - new_size[0]) // 2
        y = (SCREEN_HEIGHT - new_size[1]) // 2
        screen.blit(scaled_img, (x, y))




    def create_new_profile(self):
        """Ask user for name and PIN to create a new profile"""
        entering = True
        name = ""
        pin = ""

        while entering:
            screen.fill((255,255,255))
            self.draw_arabic_text("إنشاء ملف جديد", 100, (0,0,0), (SCREEN_WIDTH//2, SCREEN_HEIGHT*0.1), bold=True)

            # Name input
            name_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 100, 400, 80)
            pygame.draw.rect(screen, (200,200,200), name_rect)
            self.draw_arabic_text(name or "أدخل الاسم", 50, (0,0,0), name_rect.center)

            # PIN input
            pin_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 + 20, 400, 80)
            pygame.draw.rect(screen, (200,200,200), pin_rect)
            self.draw_arabic_text("*"*len(pin) or "أدخل PIN", 50, (0,0,0), pin_rect.center)

            # Confirm button
            confirm_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 150, 200, 80)
            pygame.draw.rect(screen, (100,200,100), confirm_rect, border_radius=20)
            self.draw_arabic_text("تأكيد", 50, (255,255,255), confirm_rect.center, bold=True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    entering = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        entering = False
                    elif event.key == pygame.K_BACKSPACE:
                        if name_rect.collidepoint(pygame.mouse.get_pos()):
                            name = name[:-1]
                        elif pin_rect.collidepoint(pygame.mouse.get_pos()):
                            pin = pin[:-1]
                    elif event.unicode.isprintable():
                        if name_rect.collidepoint(pygame.mouse.get_pos()):
                            name += event.unicode
                        elif pin_rect.collidepoint(pygame.mouse.get_pos()):
                            pin += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if confirm_rect.collidepoint(event.pos):
                        if name.strip() and pin.strip():
                            # Assign avatar automatically
                            avatar_files = os.listdir(AVATAR_PATH)
                            avatar_file = avatar_files[self.selected_avatar_index % len(avatar_files)]
                            profile = {"name": name, "avatar": avatar_file, "pin": pin}
                            self.profiles.append(profile)
                            save_profiles(self.profiles)
                            self.current_profile = profile
                            self.show_profile_screen = False
                            self.show_welcome = True
                            entering = False

            pygame.display.flip()
            clock.tick(60)




    def verify_pin(self, profile, on_success=None):
        """Ask for PIN before selecting or editing a profile"""
        entering = True
        pin_input = ""
        message = ""

        while entering:
            screen.fill((255,255,255))
            self.draw_arabic_text(f"أدخل PIN لملف {profile['name']}", 80, (0,0,0), (SCREEN_WIDTH//2, SCREEN_HEIGHT//3), bold=True)

            # PIN box
            pin_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2, 400, 80)
            pygame.draw.rect(screen, (200,200,200), pin_rect)
            self.draw_arabic_text("*"*len(pin_input), 50, (0,0,0), pin_rect.center)

            # Show message if incorrect
            if message:
                self.draw_arabic_text(message, 40, (255,0,0), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 120))

            # Confirm button
            confirm_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 150, 200, 80)
            pygame.draw.rect(screen, (100,200,100), confirm_rect, border_radius=20)
            self.draw_arabic_text("تأكيد", 50, (255,255,255), confirm_rect.center, bold=True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    entering = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        entering = False
                    elif event.key == pygame.K_BACKSPACE:
                        pin_input = pin_input[:-1]
                    elif event.unicode.isprintable():
                        pin_input += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if confirm_rect.collidepoint(event.pos):
                        if pin_input == profile.get("pin"):
                            entering = False
                            if on_success:
                                on_success()
                        else:
                            message = "رمز PIN غير صحيح"
                            pin_input = ""

            pygame.display.flip()
            clock.tick(60)

            
    def select_profile(self, profile):
        self.current_profile = profile
        self.show_profile_screen = False
        self.show_welcome = True


    def show_message(self, text, duration=2):
        """Display a temporary message in the center of the screen."""
        reshaped = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped)
        font = load_font(60, bold=True)
        rendered = font.render(bidi_text, True, (255, 0, 0))
        rect = rendered.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(rendered, rect)
        pygame.display.flip()
        pygame.time.delay(int(duration * 1000))


        
    def edit_profile(self, profile):
        """
        Edit the given profile: change name or avatar.
        This opens a simple temporary screen for editing.
        """
        editing = True
        input_name = profile.get("name", "")
        avatar_files = os.listdir(AVATAR_PATH)
        avatar_index = avatar_files.index(profile["avatar"]) if profile.get("avatar") in avatar_files else 0

        while editing:
            screen.fill((255,255,255))
            self.draw_arabic_text("تعديل الملف الشخصي", 150, (0,0,0), (SCREEN_WIDTH//2, SCREEN_HEIGHT*0.1), bold=True)
            
            # Name input box
            input_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50, 300, 80)
            pygame.draw.rect(screen, (200,200,200), input_rect)
            self.draw_arabic_text(input_name or "أدخل الاسم هنا", 50, (0,0,0), input_rect.center)
            
            # Avatar selection
            avatar_img = load_image(os.path.join(AVATAR_PATH, avatar_files[avatar_index]), 150, 150)
            avatar_rect = avatar_img.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 150))
            screen.blit(avatar_img, avatar_rect)
            self.draw_arabic_text("اضغط لتغيير الصورة", 40, (0,0,0), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 250))
            
            # Confirm button
            confirm_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 150, 200, 80)
            pygame.draw.rect(screen, (100,200,100), confirm_rect, border_radius=20)
            self.draw_arabic_text("تأكيد", 50, (255,255,255), confirm_rect.center, bold=True)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    editing = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        editing = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_name = input_name[:-1]
                    elif event.unicode.isprintable():
                        input_name += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if avatar_rect.collidepoint(event.pos):
                        avatar_index = (avatar_index + 1) % len(avatar_files)
                    if confirm_rect.collidepoint(event.pos):
                        profile["name"] = input_name or profile["name"]
                        profile["avatar"] = avatar_files[avatar_index]
                        save_profiles(self.profiles)
                        editing = False
            
            pygame.display.flip()
            clock.tick(60)

    def delete_profile(self, profile):
        if profile in self.profiles:
            self.profiles.remove(profile)
            save_profiles(self.profiles)
            # If the deleted profile was the current profile, reset current_profile
            if self.current_profile == profile:
                self.current_profile = None
            # Stay on profile screen to select another or create new
            self.show_profile_screen = True
            self.show_welcome = False

    def enter_profile(self, profile):
        """After correct PIN, enter the selected profile."""
        self.current_profile = profile
        self.show_profile_screen = False
        self.show_welcome = True


    # ---------------------------
    # Main menu
    # ---------------------------
    def draw_button(self, btn):
        self.draw_arabic_text(btn["text"], 150, (51,51,51), btn["rect"].center)

    def draw_profile_button(self):
        if self.current_profile:
            rect = pygame.Rect(SCREEN_WIDTH-150, 20, 130, 130)
            avatar_img = load_image(os.path.join(AVATAR_PATH, self.current_profile["avatar"]), 130,130)
            if avatar_img:
                screen.blit(avatar_img, rect)
            return rect
        return None

    # ---------------------------
    # Launch sub-apps
    # ---------------------------
    def launch_alphabit_name(self):
        pygame.mixer.stop()
        run_alphabit_name(screen, self)

    def launch_alphabit_sound(self):
        pygame.mixer.stop()
        run_alphabit_sound(screen, main_app=self)

    # ---------------------------
    # Main loop
    # ---------------------------
    def run(self):
        profile_rects, edit_rects, delete_rects, add_rect = [], [], [], None

        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            screen.fill((255, 255, 255))

            # =========================
            # PROFILE SELECTION SCREEN
            # =========================
            if self.show_profile_screen:
                profile_rects, edit_rects, delete_rects, add_rect = self.draw_profile_screen()

            # =========================
            # WELCOME SCREEN
            # =========================
            elif self.show_welcome:
                if self.welcome_bg:
                    self.draw_background(self.welcome_bg)
                self.draw_arabic_text("مرحباً", 250, (51,51,51), (SCREEN_WIDTH//2, SCREEN_HEIGHT//3), bold=True)
                pygame.draw.rect(screen, (255,255,255), self.start_rect, border_radius=30)
                pygame.draw.rect(screen, (255,102,0), self.start_rect, 5, border_radius=30)
                self.draw_arabic_text("هيا نبدأ", 150, (255,102,0), self.start_rect.center, bold=True)

            # =========================
            # MAIN MENU SCREEN
            # =========================
            else:
                if self.section_bg:
                    self.draw_background(self.section_bg)
                for btn in self.section_buttons:
                    self.draw_button(btn)

            # =========================
            # PERSISTENT PROFILE BUTTON
            # =========================
            profile_btn_rect = self.draw_profile_button()

            # =========================
            # EVENT HANDLING
            # =========================
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    # --- Profile screen clicks ---
                    if self.show_profile_screen:
                        # 1️⃣ Select existing profile → verify PIN
                        for rect, profile_obj in profile_rects:
                            if rect.collidepoint(mouse_pos):
                                self.verify_pin(
                                    profile_obj,
                                    on_success=lambda p=profile_obj: self.enter_profile(p)
                                )
                                break

                        # 2️⃣ Edit profile → verify PIN, then edit
                        for rect, profile_obj in edit_rects:
                            if rect.collidepoint(mouse_pos):
                                self.verify_pin(
                                    profile_obj,
                                    on_success=lambda p=profile_obj: self.edit_profile(p)
                                )
                                break

                        # 3️⃣ Delete profile → verify PIN, then delete
                        for rect, profile_obj in delete_rects:
                            if rect.collidepoint(mouse_pos):
                                self.verify_pin(
                                    profile_obj,
                                    on_success=lambda p=profile_obj: self.delete_profile(p)
                                )
                                break

                        # 4️⃣ Add new profile → go to creation screen
                        if add_rect and add_rect.collidepoint(mouse_pos):
                            self.create_profile_screen()  # ask name + PIN
                            break


                    # --- Welcome screen click ---
                    elif self.show_welcome:
                        if self.start_rect.collidepoint(mouse_pos):
                            self.show_welcome = False

                    # --- Main menu screen click ---
                    else:
                        for btn in self.section_buttons:
                            if btn["rect"].collidepoint(mouse_pos):
                                btn["action"]()
                                break

                    # --- Persistent top-right profile button ---
                    if profile_btn_rect and profile_btn_rect.collidepoint(mouse_pos):
                        if self.current_profile:
                            # Go directly to edit the current user’s profile
                            self.edit_profile(self.current_profile)
                        else:
                            # If no user is currently selected, show the selection screen
                            self.show_profile_screen = True
                            self.show_welcome = False


            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


# ---------------------------
# Run app
# ---------------------------
if __name__ == "__main__":
    app = QuizApp()
    app.run()
