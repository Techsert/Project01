import os
import pygame
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image

# =========================
# CONFIG
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(BASE_DIR, "../assets/img/alphabitSound")
SOUND_PATH = os.path.join(BASE_DIR, "../assets/sounds/alphabitSound")
ARABIC_FONT_PATH = os.path.join(BASE_DIR, "../assets/fonts/NotoNaskhArabic-Regular.ttf")

# =========================
# SAMPLE SLIDES
# =========================
slides = [
    {
        "title": "الحُروف العَرَبية",
        "narration": os.path.join(SOUND_PATH, "intro.wav"),
        "images": [
            {"path": os.path.join(IMG_PATH, "bg-nt.png"), "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": os.path.join(IMG_PATH, "hard.png"), "sound": os.path.join(SOUND_PATH, "areyouready.wav"),
             "delay": 4000, "scale": (0.25, 0.55), "position": "center"},
        ]
    },
    # Add more slides here...
]

# =========================
# Pygame AlphabitNameApp
# =========================
class PygameAlphabitNameApp:
    def __init__(self, main_app=None):
        self.main_app = main_app
        pygame.init()
        pygame.mixer.init()

        info = pygame.display.Info()
        self.screen_width, self.screen_height = info.current_w, info.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption("Alphabet Names - أسماء الحروف")
        self.clock = pygame.time.Clock()

        # Load font
        self.font = pygame.font.Font(ARABIC_FONT_PATH, 60)
        self.bold_font = pygame.font.Font(os.path.join(BASE_DIR, "../assets/fonts/NotoNaskhArabic-Bold.ttf"), 60)

        # Slides
        self.slide_index = 0
        self.image_objects = []
        self.image_display_times = []  # timestamps for delayed images
        self.narration_channel = pygame.mixer.Channel(1)
        self.running = True

        # Navigation buttons
        btn_w, btn_h = 250, 80
        self.prev_rect = pygame.Rect(50, self.screen_height - 120, btn_w, btn_h)
        self.next_rect = pygame.Rect(self.screen_width - btn_w - 50, self.screen_height - 120, btn_w, btn_h)
        self.back_rect = pygame.Rect(self.screen_width//2 - btn_w//2, self.screen_height - 120, btn_w, btn_h)

        self.load_slide()

    # Draw Arabic text
    def draw_arabic_text(self, text, size, color, center, bold=False):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        
        # Choose font file
        font_file = "NotoNaskhArabic-Bold.ttf" if bold else "NotoNaskhArabic-Regular.ttf"
        font_path = os.path.join(BASE_DIR, "../assets/fonts", font_file)
        
        font = pygame.font.Font(font_path, size)
        rendered = font.render(bidi_text, True, color)
        rect = rendered.get_rect(center=center)
        self.screen.blit(rendered, rect)


    # Load current slide images
    def load_slide(self):
        self.image_objects.clear()
        self.image_display_times.clear()
        slide = slides[self.slide_index]

        # Play narration
        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.load(slide["narration"])
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play()
        except Exception as e:
            print("Narration error:", e)

        # Schedule images
        current_time = pygame.time.get_ticks()
        for img in slide["images"]:
            try:
                image = pygame.image.load(img["path"]).convert_alpha()
                img_w = int(self.screen_width * img.get("scale", (0.2,0.2))[0])
                img_h = int(self.screen_height * img.get("scale", (0.2,0.2))[1])
                image = pygame.transform.smoothscale(image, (img_w, img_h))
                self.image_objects.append({"image": image, "pos": img.get("position","center"), "sound": img.get("sound")})
                self.image_display_times.append(current_time + img.get("delay",0))
            except Exception as e:
                print("Image load error:", e)
                self.image_objects.append({"image": None, "pos":"center", "sound": None})
                self.image_display_times.append(current_time + img.get("delay",0))

    # Draw images with delay
    def draw_images(self):
        now = pygame.time.get_ticks()
        for idx, img_obj in enumerate(self.image_objects):
            if now >= self.image_display_times[idx]:
                image = img_obj["image"]
                if image:
                    pos = img_obj["pos"]
                    rect = image.get_rect()
                    if pos=="center":
                        rect.center = (self.screen_width//2, self.screen_height//2)
                    elif pos=="top-left":
                        rect.topleft = (0,0)
                    elif pos=="top-right":
                        rect.topright = (self.screen_width,0)
                    elif pos=="bottom-left":
                        rect.bottomleft = (0,self.screen_height)
                    elif pos=="bottom-right":
                        rect.bottomright = (self.screen_width,self.screen_height)
                    self.screen.blit(image, rect)

                    # Play associated sound
                    if img_obj["sound"] and not self.narration_channel.get_busy():
                        try:
                            sound = pygame.mixer.Sound(img_obj["sound"])
                            self.narration_channel.play(sound)
                        except Exception as e:
                            print("Image sound error:", e)

    # Draw navigation buttons
    def draw_buttons(self):
        pygame.draw.rect(self.screen, (200,200,200), self.prev_rect)
        pygame.draw.rect(self.screen, (200,200,200), self.next_rect)
        pygame.draw.rect(self.screen, (255,180,180), self.back_rect)
        self.draw_arabic_text("السابق", 30, (0,0,0), self.prev_rect.center, bold=True)
        self.draw_arabic_text("التالي", 30, (0,0,0), self.next_rect.center, bold=True)
        self.draw_arabic_text("⬅ العودة", 30, (0,0,0), self.back_rect.center, bold=True)

    # Handle clicks
    def handle_click(self, pos):
        if self.prev_rect.collidepoint(pos) and self.slide_index>0:
            pygame.mixer.stop()
            self.slide_index -= 1
            self.load_slide()
        elif self.next_rect.collidepoint(pos) and self.slide_index<len(slides)-1:
            pygame.mixer.stop()
            self.slide_index += 1
            self.load_slide()
        elif self.back_rect.collidepoint(pos):
            pygame.mixer.stop()
            if self.main_app:
                self.main_app.show_section_screen()
            self.running = False

    # Main loop
    def run(self):
        while self.running:
            self.screen.fill((255,255,255))
            self.draw_images()
            self.draw_buttons()
            # Title
            self.draw_arabic_text(slides[self.slide_index]["title"], 60, (0,0,0), (self.screen_width//2, 100), bold=True)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running=False
                elif event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                    self.running=False
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

# Run the app
def run_alphabit_name(main_app=None):
    app = PygameAlphabitNameApp(main_app)
    app.run()
