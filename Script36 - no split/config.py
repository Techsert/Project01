# config.py - UPDATED
import os

# ==========================================================
# BASE DIRECTORY
# ==========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================================
# ASSET PATHS
# ==========================================================
ASSETS_PATH = os.path.join(BASE_DIR, "../assets")

# Images
IMG_MAIN_PATH = os.path.join(ASSETS_PATH, "img/main")

# Sounds
SOUND_MAIN_PATH = os.path.join(ASSETS_PATH, "sounds/main")

# Fonts
ARABIC_FONT_REGULAR = os.path.join(ASSETS_PATH, "fonts/NotoNaskhArabic-Regular.ttf")
ARABIC_FONT_BOLD = os.path.join(ASSETS_PATH, "fonts/NotoNaskhArabic-Bold.ttf")

# Profile System Paths
AVATAR_PROFILES_PATH = os.path.join(ASSETS_PATH, "profiles/avatars")
PROFILE_DATA_PATH = os.path.join(ASSETS_PATH, "profiles/data")
PROFILE_FILE = os.path.join(PROFILE_DATA_PATH, "profiles.json")
REWARDS_CARDS_PATH = os.path.join(ASSETS_PATH, "rewards/cards")

# ==========================================================
# DISPLAY SETTINGS (DO NOT MODIFY AT RUNTIME)
# ==========================================================
# These are default/fallback values
DEFAULT_SCREEN_WIDTH = 1280
DEFAULT_SCREEN_HEIGHT = 720

# ❌ REMOVED: Don't define SCREEN_WIDTH/SCREEN_HEIGHT here
# They should be instance variables in QuizApp, not globals

# ==========================================================
# AUDIO SETTINGS
# ==========================================================
HOVER_CHANNEL_ID = 5
BG_MUSIC_VOLUME = 0.3

# ==========================================================
# VIDEO SETTINGS
# ==========================================================
VIDEO_FPS = 30  # Frame rate for video playback
VIDEO_CACHE_CLEANUP_INTERVAL = 300  # Seconds between cache cleanups

# ==========================================================
# UI CONSTANTS (eliminates magic numbers)
# ==========================================================
CURSOR_BLINK_MS = 500
BUTTON_BORDER_RADIUS = 15
PROFILE_ICON_SIZE_RATIO = 0.04  # Relative to screen width
EXIT_ICON_WIDTH_RATIO = 0.05
EXIT_ICON_HEIGHT_RATIO = 0.09

# ==========================================================
# COLOR CONSTANTS
# ==========================================================
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_ORANGE = (255, 102, 0)
COLOR_GREEN = (0, 170, 0)
COLOR_RED = (200, 0, 0)
COLOR_BLUE = (60, 120, 200)
COLOR_GREY = (150, 150, 150)
COLOR_LIGHT_GREY = (220, 220, 220)

# ==========================================================
# LAYOUT RATIOS (for consistent scaling)
# ==========================================================
TITLE_SIZE_RATIO = 0.04
BUTTON_TEXT_SIZE_RATIO = 0.035
SMALL_TEXT_SIZE_RATIO = 0.03

# ==========================================================
# HELPER FUNCTION
# ==========================================================
def get_screen_dimensions():
    """
    Get actual screen dimensions at runtime.
    Call this after pygame.init() in main_menu28.py
    """
    import pygame
    info = pygame.display.Info()
    return info.current_w, info.current_h
