# reward_popup.py - NEW FILE
# Displays unlocked rewards in a feedback overlay similar to quiz feedback

import pygame
import os
import config

class RewardPopup:
    """
    Displays a feedback overlay when rewards are unlocked.
    Similar to quiz feedback but shows reward card images.
    """
    
    def __init__(self, screen):
        """Initialize reward popup manager."""
        self.screen = screen
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen.get_size()
        
        # Popup state
        self.active = False
        self.reward_queue = []  # Queue of rewards to show
        self.current_reward_img = None
        self.current_reward_name = ""
        self.display_until = 0
        self.display_duration = 10000  # 4 seconds per reward
        
        # Load celebration sound
        self.celebration_sound = None
        celebration_path = os.path.join(config.SOUND_MAIN_PATH, "reward_unlock.wav")
        if os.path.exists(celebration_path):
            try:
                self.celebration_sound = pygame.mixer.Sound(celebration_path)
            except Exception as e:
                print(f"⚠️ Failed to load celebration sound: {e}")
        
        # Fallback: use quiz correct sounds if reward sound doesn't exist
        if not self.celebration_sound:
            correct_sound_path = os.path.join(config.ASSETS_PATH, "sounds/alphabitSound/correct1.wav")
            if os.path.exists(correct_sound_path):
                try:
                    self.celebration_sound = pygame.mixer.Sound(correct_sound_path)
                except Exception as e:
                    print(f"⚠️ Failed to load fallback sound: {e}")
    
    def add_reward(self, reward_filename):
        """Add a reward to the display queue."""
        reward_path = os.path.join(config.REWARDS_CARDS_PATH, reward_filename)
        
        if not os.path.exists(reward_path):
            print(f"⚠️ Reward image not found: {reward_path}")
            return
        
        try:
            # Load reward image
            img = pygame.image.load(reward_path).convert_alpha()
            
            # Scale to fit screen (max 60% of screen size)
            max_w = int(self.SCREEN_WIDTH * 0.6)
            max_h = int(self.SCREEN_HEIGHT * 0.7)
            
            img_w, img_h = img.get_size()
            scale = min(max_w / img_w, max_h / img_h)
            
            new_w = int(img_w * scale)
            new_h = int(img_h * scale)
            
            scaled_img = pygame.transform.smoothscale(img, (new_w, new_h))
            
            # Add to queue
            self.reward_queue.append({
                "image": scaled_img,
                "name": reward_filename
            })
            
            print(f"🎁 Added reward to display queue: {reward_filename}")
            
        except Exception as e:
            print(f"⚠️ Failed to load reward image {reward_filename}: {e}")
    
    def show_next_reward(self):
        """Display the next reward in the queue."""
        if not self.reward_queue:
            self.active = False
            return False
        
        # Get next reward
        reward = self.reward_queue.pop(0)
        self.current_reward_img = reward["image"]
        self.current_reward_name = reward["name"]
        self.display_until = pygame.time.get_ticks() + self.display_duration
        self.active = True
        
        # Play celebration sound
        if self.celebration_sound:
            self.celebration_sound.stop()
            self.celebration_sound.play()
        
        print(f"🎉 Displaying reward: {self.current_reward_name}")
        return True
    
    def update(self):
        """Update popup state - call this in your main loop."""
        if not self.active:
            # Try to show next reward if queue is not empty
            if self.reward_queue:
                self.show_next_reward()
            return False
        
        # Check if current reward display time is over
        if pygame.time.get_ticks() >= self.display_until:
            # Show next reward or deactivate
            if self.reward_queue:
                self.show_next_reward()
            else:
                self.active = False
                self.current_reward_img = None
                self.current_reward_name = ""
                return False
        
        return True
    
    def draw(self):
        """Draw the reward popup overlay."""
        if not self.active or not self.current_reward_img:
            return
        
        # Dark overlay
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        
        # Draw reward image centered
        img_rect = self.current_reward_img.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.screen.blit(self.current_reward_img, img_rect)
        
        # Draw "NEW REWARD UNLOCKED!" text above
        try:
            font_path = config.ARABIC_FONT_BOLD
            if os.path.exists(font_path):
                font = pygame.font.Font(font_path, int(self.SCREEN_HEIGHT * 0.06))
            else:
                font = pygame.font.SysFont("Arial", int(self.SCREEN_HEIGHT * 0.06), bold=True)
            
            text = font.render("NEW REWARD UNLOCKED One!", True, (255, 215, 0))
            text_rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, img_rect.top - 60))
            
            # Draw text with shadow effect
            shadow = font.render("NEW REWARD UNLOCKED Two!", True, (0, 0, 0))
            shadow_rect = shadow.get_rect(center=(self.SCREEN_WIDTH // 2 + 3, img_rect.top - 57))
            self.screen.blit(shadow, shadow_rect)
            self.screen.blit(text, text_rect)
            
        except Exception as e:
            print(f"⚠️ Failed to render reward text: {e}")
        
        # Draw "Click to continue" hint at bottom
        try:
            if os.path.exists(config.ARABIC_FONT_REGULAR):
                hint_font = pygame.font.Font(config.ARABIC_FONT_REGULAR, int(self.SCREEN_HEIGHT * 0.03))
            else:
                hint_font = pygame.font.SysFont("Arial", int(self.SCREEN_HEIGHT * 0.03))
            
            hint_text = hint_font.render("Click anywhere to continue", True, (255, 255, 255))
            hint_rect = hint_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 80))
            self.screen.blit(hint_text, hint_rect)
            
        except Exception as e:
            print(f"⚠️ Failed to render hint text: {e}")
    
    def handle_click(self):
        """Handle mouse click - skip to next reward or close."""
        if not self.active:
            return False
        
        # Show next reward immediately or close
        if self.reward_queue:
            self.show_next_reward()
        else:
            self.active = False
            self.current_reward_img = None
            self.current_reward_name = ""
        
        return True
    
    def is_active(self):
        """Check if popup is currently active."""
        return self.active
    
    def has_pending_rewards(self):
        """Check if there are rewards waiting to be displayed."""
        return len(self.reward_queue) > 0 or self.active
