# config.py
import os

# --- Base Directory ---
# Assumes config.py is in the same directory as main_menu28.py
# If you move config.py, adjust BASE_DIR accordingly.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Asset Paths ---
# All paths are relative to BASE_DIR and point to the /assets folder structure
ASSETS_PATH = os.path.join(BASE_DIR, "../assets")

# Images
IMG_MAIN_PATH = os.path.join(ASSETS_PATH, "img/main")
# You might want to add other specific image paths here if they are reused
# e.g., IMG_LEARNING_BG = os.path.join(IMG_MAIN_PATH, "learning_bg_1.png")

# Sounds
SOUND_MAIN_PATH = os.path.join(ASSETS_PATH, "sounds/main")

# Fonts
ARABIC_FONT_REGULAR = os.path.join(ASSETS_PATH, "fonts/NotoNaskhArabic-Regular.ttf")
ARABIC_FONT_BOLD = os.path.join(ASSETS_PATH, "fonts/NotoNaskhArabic-Bold.ttf")

# Profile System Paths
AVATAR_PROFILES_PATH = os.path.join(ASSETS_PATH, "profiles/avatars")
PROFILE_DATA_PATH = os.path.join(ASSETS_PATH, "profiles/data")
PROFILE_FILE = os.path.join(PROFILE_DATA_PATH, "profiles.json") # The actual JSON file
REWARDS_CARDS_PATH = os.path.join(ASSETS_PATH, "rewards/cards")

# --- Game Settings ---
# Initial screen dimensions (will be updated by Pygame info.current_w/h)
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720 

# Mixer Settings
HOVER_CHANNEL_ID = 5
BG_MUSIC_VOLUME = 0.3
