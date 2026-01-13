# quiz_lvl1_3_refactored.py - OPTIMIZED VERSION
# No changes needed - uses optimized QuizPlayer base class

import os
import pygame
from quiz_base import QuizPlayer, load_image

# ==========================================================
# QUESTIONS DATA (Levels 1-3)
# ==========================================================
QUESTIONS = [
    # Easy Level
    {
        "sound": "01alef-s.wav",
        "options": [
            {"file": "12sen01.png", "size": (520, 440)}, 
            {"file": "01alef01.png", "size": (151, 700)}, 
            {"file": "08dal.png", "size": (250, 285)}, 
            {"file": "26heh.png", "size": (400, 400)}
        ],
        "answer": 1,
        "difficulty": "easy",
        "margin": 350
    },
    {
        "sound": "28yaa-s.wav",
        "options": [
            {"file": "09thal.png", "size": (250, 430)}, 
            {"file": "11zay.png", "size": (300, 640)}, 
            {"file": "10ra.png", "size": (300, 450)}, 
            {"file": "28yaa.png", "size": (450, 450)}
        ],
        "answer": 3,
        "difficulty": "easy",
        "margin": 300
    },
    
    # Medium Level
    {
        "sound": "01alef-f.wav",
        "options": [
            {"file": "01alef-f.png", "size": (180, 680)}, 
            {"file": "01alef.png", "size": (151, 600)}, 
            {"file": "01alef-k.png", "size": (151, 650), "y_offset": 175}, 
            {"file": "01alef-d.png", "size": (181, 770)}
        ],
        "answer": 0,
        "difficulty": "medium",
        "margin": 450
    },
    {
        "sound": "28yaa-d.wav",
        "options": [
            {"file": "28yaa.png", "size": (450, 450)}, 
            {"file": "28yaa-k.png", "size": (450, 540), "y_offset": 90}, 
            {"file": "28yaa-d.png", "size": (450, 600)}, 
            {"file": "28yaa-f.png", "size": (450, 530)}
        ],
        "answer": 2,
        "difficulty": "medium",
        "margin": 250
    },
    
    # Hard Level
    {
        "sound": "tung.wav",
        "options": [
            {"file": "27waw.png", "size": (200, 225), "y_offset": -450}, 
            {"file": "25noon01.png", "size": (200, 250)}, 
            {"file": "21kf.png", "size": (200, 250), "y_offset": -450}, 
            {"file": "09thal01.png", "size": (150, 200)}, 
            {"file": "17zaa01.png", "size": (200, 340), "y_offset": -450}, 
            {"file": "15dad.png", "size": (200, 250)},
            {"file": "11zay.png", "size": (200, 270), "y_offset": -450}, 
            {"file": "19gean.png", "size": (200, 390)}, 
            {"file": "07ka.png", "size": (200, 350), "y_offset": -450}, 
            {"file": "04tha.png", "size": (200, 240)}
        ],
        "answer": [3, 4, 9],
        "difficulty": "hard",
        "margin": 20
    },
    {
        "sound": "./Sound-Location/28yaa-v-k_-b.wav",
        "options": [
            {"file": "28yaa-e-d.png", "size": (200, 250), "y_offset": -400}, 
            {"file": "28yaa-b-k.png", "size": (200, 250), "y_offset": 50}, 
            {"file": "28yaa-m-f.png", "size": (200, 250), "y_offset": -450}, 
            {"file": "28yaa-b-f.png", "size": (200, 250)}, 
            {"file": "28yaa-e-k.png", "size": (200, 250), "y_offset": -350}, 
            {"file": "28yaa-m-d.png", "size": (200, 250)}, 
            {"file": "28yaa-e-f.png", "size": (200, 250), "y_offset": -400}, 
            {"file": "28yaa-b-d.png", "size": (200, 250)}
        ],
        "answer": 1,
        "difficulty": "hard",
        "margin": 150
    },
]

# ==========================================================
# EXTENDED QUIZ PLAYER
# ==========================================================
class AlphabetQuizPlayer(QuizPlayer):
    """Quiz player for alphabet questions (levels 1-3)."""
    
    def draw_playing(self):
        """Draw the current question with options."""
        if not (0 <= self.current_idx < len(self.questions)):
            return
        
        q = self.questions[self.current_idx]
        options = q.get("options", [])
        margin = q.get("margin", 200)
        
        # ✅ Lazy load option images (only when needed)
        if not hasattr(self, 'option_images') or not self.option_images:
            self.option_images = []
            for opt in options:
                fname = opt.get("file")
                size = opt.get("size", (200, 200))
                path = os.path.join(self.IMG_PATH, fname)
                img = load_image(path)
                if img:
                    surf = pygame.transform.smoothscale(img, size)
                else:
                    surf = pygame.Surface(size, pygame.SRCALPHA)
                self.option_images.append(surf)
        
        # Calculate positions (bottom aligned)
        total_width = sum([opt.get("size", (200, 200))[0] for opt in options]) + (len(options) - 1) * margin
        start_x = (self.W - total_width) // 2
        baseline_y = int(self.H * 0.75)
        
        # Draw options
        self.option_rects = []
        x = start_x
        for i, opt in enumerate(options):
            img = self.option_images[i]
            w, h = opt.get("size", (200, 200))
            x_off = opt.get("x_offset", 0)
            y_off = opt.get("y_offset", 0)
            
            rect = img.get_rect(midbottom=(x + w // 2 + x_off, baseline_y + y_off))
            self.screen.blit(img, rect)
            self.option_rects.append(rect)
            
            # Draw selection outline
            if i in self.selected_options:
                pygame.draw.rect(self.screen, (255, 215, 0), rect.inflate(10, 10), 6, border_radius=12)
            
            x += w + margin
        
        # Progress counter
        current = self.current_idx + 1
        total = len(self.questions)
        
        from quiz_base import render_arabic_to_surface
        counter_text = f"Question {current} from {total}"
        counter_surf = render_arabic_to_surface(counter_text, self.ARABIC_FONT_PATH, 60, color=(255, 255, 255))
        self.screen.blit(counter_surf, counter_surf.get_rect(center=(self.W//2, int(self.H*0.08))))
        
        # Progress bar
        bar_w = int(self.W * 0.6)
        bar_h = 28
        bar_x = (self.W - bar_w) // 2
        bar_y = int(self.H * 0.12)
        
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=15)
        progress_w = int((current / total) * bar_w)
        pygame.draw.rect(self.screen, (255, 215, 0), (bar_x, bar_y, progress_w, bar_h), border_radius=15)
        
        # Progress icons
        icon_spacing = bar_w // total
        for i in range(total):
            x = bar_x + i * icon_spacing + icon_spacing // 4
            y = bar_y + bar_h + 10
            
            if i < self.current_idx:
                if i < self.score:
                    if self.goal_icon:
                        self.screen.blit(self.goal_icon, (x, y))
                else:
                    if self.miss_icon:
                        self.screen.blit(self.miss_icon, (x, y))
            else:
                pygame.draw.circle(self.screen, (200, 200, 200), (x + 20, y + 20), 15)

# ==========================================================
# RUN FUNCTION
# ==========================================================
def run_quiz_lvl1_3(screen, main_app, auto_difficulty=None):
    """
    Launch alphabet quiz (levels 1-3) with optimized loading.
    
    Args:
        screen: Pygame screen surface
        main_app: Reference to main QuizApp
        auto_difficulty: Optional - auto-select difficulty ("easy", "medium", "hard")
    """
    print(f"🎮 [RUNNING] quiz_lvl1_3 with auto_difficulty={auto_difficulty}")
    
    # ✅ Keep background music playing during loading
    # Don't stop audio manager - let loading happen with music
    
    # Create and run quiz (loading happens in background)
    player = AlphabetQuizPlayer(
        screen=screen,
        main_app=main_app,
        questions=QUESTIONS,
        level=1,
        auto_difficulty=auto_difficulty
    )
    player.run()
    
    # Restore background music after quiz
    if hasattr(main_app, 'audio_manager'):
        main_app.audio_manager.play_bg_music()
