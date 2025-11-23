import pygame
import os
import time

pygame.init()
pygame.mixer.init()

# ✅ Slides data (unchanged)
slides = [
    {
        "title": "حرف الألف",
        "narration": "../assets/sounds/alphabitSound/01alef-s.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82),
             "position": "center"},
            {"path": "../assets/img/alphabitSound/01alef.png", "delay": 0, "scale": (0.05, 0.50),
             "position": "center", "duration": 2000},
            {"path": "../assets/img/alphabitSound/01alef-f.png", "sound": "../assets/sounds/alphabitSound/01alef-f.wav",
             "delay": 3000, "scale": (0.05, 0.45), "position": "center-right", "offset": {"x": -200, "y": 0}},
            {"path": "../assets/img/alphabitSound/01alef-k.png", "sound": "../assets/sounds/alphabitSound/01alef-k.wav",
             "delay": 7000, "scale": (0.05, 0.45), "position": "center"},
            {"path": "../assets/img/alphabitSound/01alef-d.png", "sound": "../assets/sounds/alphabitSound/01alef-d.wav",
             "delay": 10000, "scale": (0.05, 0.45), "position": "center-left", "offset": {"x": 180, "y": 0}},
        ],
    },
    {
        "title": "أحسنت",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82),
             "position": "center"},
            {"path": "../assets/img/alphabitSound/coach.png",
             "sound": "../assets/sounds/alphabitSound/welldone.wav",
             "delay": 1000, "scale": (0.30, 0.40), "position": "center"}
        ]
    },
]

class SlideShow:
    def __init__(self, screen, main_app=None):
        self.screen = screen
        self.main_app = main_app
        self.slide_index = 0
        self.start_time = time.time()
        self.loaded_images = []  # holds dict: {"surf":..., "rect":..., "delay":...}

        self.font = pygame.font.Font("../assets/fonts/NotoNaskhArabic-Bold.ttf", 72)

        self.load_slide()

    def stop_sounds(self):
        pygame.mixer.stop()

    def load_slide(self):
        self.stop_sounds()
        self.start_time = time.time()
        self.loaded_images.clear()

        slide = slides[self.slide_index]

        # ✅ Play narration if exists
        narration = slide.get("narration")
        if narration and os.path.exists(narration):
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(narration))

        # ✅ Pre-load images but respect delays when drawing
        for img_data in slide["images"]:
            abs_path = os.path.abspath(img_data["path"])
            if not os.path.exists(abs_path):
                continue

            img = pygame.image.load(abs_path).convert_alpha()
            scale = img_data.get("scale", (0.3, 0.3))
            w = int(self.screen.get_width() * scale[0])
            h = int(self.screen.get_height() * scale[1])
            img = pygame.transform.smoothscale(img, (w, h))

            rect = img.get_rect(center=self.screen.get_rect().center)

            self.loaded_images.append({
                "img_data": img_data,
                "surf": img,
                "rect": rect,
                "delay": img_data.get("delay", 0),
                "start": None,
                "active": False
            })

    def draw_slide(self):
        now_ms = (time.time() - self.start_time) * 1000
        slide = slides[self.slide_index]

        self.screen.fill((255, 255, 255))

        # ✅ Draw title
        title = slide["title"]
        text_surface = self.font.render(title, True, (0, 0, 0))
        self.screen.blit(text_surface, (50, 50))

        # ✅ Draw images after delay
        for img_obj in self.loaded_images:
            img_data = img_obj["img_data"]

            if not img_obj["active"]:
                if now_ms >= img_obj["delay"]:
                    img_obj["active"] = True
                    img_obj["start"] = time.time()

                    # play sound if exists
                    sound = img_data.get("sound")
                    if sound and os.path.exists(sound):
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound(sound))

            if img_obj["active"]:
                rect = img_obj["rect"]

                # Offset adjustment
                offset = img_data.get("offset", {})
                rect.x += offset.get("x", 0)
                rect.y += offset.get("y", 0)

                self.screen.blit(img_obj["surf"], rect)

                # Auto-remove after duration
                dur = img_data.get("duration")
                if dur and (time.time() - img_obj["start"]) * 1000 >= dur:
                    img_obj["active"] = False

        pygame.display.flip()

    def next_slide(self):
        if self.slide_index < len(slides) - 1:
            self.slide_index += 1
            self.load_slide()

    def prev_slide(self):
        if self.slide_index > 0:
            self.slide_index -= 1
            self.load_slide()

    def back_to_main(self):
        self.stop_sounds()
        if self.main_app:
            self.main_app.show_section_screen()

def run_learn_lvl1_T1(screen, main_app=None):
    slideshow = SlideShow(screen, main_app)
    clock = pygame.time.Clock()

    running = True
    while running:
        slideshow.draw_slide()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                slideshow.stop_sounds()
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    slideshow.next_slide()
                if event.key == pygame.K_LEFT:
                    slideshow.prev_slide()
                if event.key == pygame.K_ESCAPE:
                    slideshow.back_to_main()
                    return

        clock.tick(60)
