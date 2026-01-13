# screen_helpers.py
import pygame
import sys
import os
import arabic_reshaper
from bidi.algorithm import get_display

# ==========================================================
# ASSET LOADING
# ==========================================================
def load_image(path, width=None, height=None, alpha=True, keep_aspect=False):
    """
    Centralized image loader.
    - Handles missing files (returns placeholder).
    - Handles alpha conversion.
    - Handles scaling (smoothscale).
    """
    if not os.path.exists(path):
        print(f"⚠️ Missing image: {path}")
        # Return a magenta placeholder to make missing assets obvious
        surf = pygame.Surface((width or 50, height or 50))
        surf.fill((255, 0, 255))
        return surf
    
    try:
        img = pygame.image.load(path)
        img = img.convert_alpha() if alpha else img.convert()
        
        if width and height:
            if keep_aspect:
                img_w, img_h = img.get_size()
                scale_factor = min(width / img_w, height / img_h)
                new_size = (int(img_w * scale_factor), int(img_h * scale_factor))
                img = pygame.transform.smoothscale(img, new_size)
            else:
                img = pygame.transform.smoothscale(img, (int(width), int(height)))
        
        return img
    except Exception as e:
        print(f"❌ Error loading image {path}: {e}")
        surf = pygame.Surface((width or 50, height or 50))
        surf.fill((255, 0, 0)) # Red for error
        return surf

def load_sound(path):
    """Centralized sound loader with error handling."""
    if not os.path.exists(path):
        print(f"⚠️ Missing sound: {path}")
        return None
    try:
        return pygame.mixer.Sound(path)
    except Exception as e:
        print(f"❌ Error loading sound {path}: {e}")
        return None

def load_icon(path, size=(50, 50), fallback_color=(200, 200, 200)):
    """
    Loads an icon. If missing, draws a colored circle placeholder.
    Used for profile icons, feedback icons, etc.
    """
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.smoothscale(img, size)
        except Exception as e:
            print(f"⚠️ Error loading icon {path}: {e}")
    
    # Fallback: create colored circle
    surf = pygame.Surface(size, pygame.SRCALPHA)
    radius = min(size) // 2
    pygame.draw.circle(surf, fallback_color + (220,), (size[0]//2, size[1]//2), radius - 2)
    pygame.draw.circle(surf, (255, 255, 255, 180), (size[0]//2, size[1]//2), radius - 2, 2)
    return surf

def load_lock_icon(path=None, size=(80, 80)):
    """
    Loads a specific lock icon or draws a vector padlock fallback.
    """
    if path and os.path.exists(path):
        return load_icon(path, size)

    # Fallback: create red lock surface
    surf = pygame.Surface(size, pygame.SRCALPHA)
    lock_w, lock_h = size[0] // 2, size[1] // 2
    lock_x, lock_y = (size[0] - lock_w) // 2, size[1] // 2
    
    # Padlock body
    pygame.draw.rect(surf, (200, 0, 0, 220), (lock_x, lock_y, lock_w, lock_h), border_radius=5)
    # Padlock shackle
    shackle_rect = pygame.Rect(lock_x + lock_w//4, lock_y - lock_h//2, lock_w//2, lock_h//2)
    pygame.draw.arc(surf, (200, 0, 0, 220), shackle_rect, 0, 3.14, 5)
    return surf

# ==========================================================
# TEXT RENDERING
# ==========================================================
def load_font(font_path, bold_font_path, size, bold=False, default_font_name="Arial"):
    """Robust font loader."""
    try:
        path = bold_font_path if bold else font_path
        if path and os.path.exists(path):
            return pygame.font.Font(path, size)
        return pygame.font.SysFont(default_font_name, size, bold=bold)
    except Exception as e:
        print(f"⚠️ Font load error: {e}")
        return pygame.font.SysFont(default_font_name, size, bold=bold)

def dynamic_font(screen_height, font_path, bold_font_path, size_ratio=0.05, bold=False):
    """Scale font size relative to screen height."""
    return load_font(font_path, bold_font_path, int(screen_height * size_ratio), bold=bold)

def render_text(text, font, color=(0,0,0)):
    """
    Renders Arabic text correctly using reshaping and bidi algorithm.
    Args:
        text: String to render
        font: pygame.font.Font object
        color: RGB tuple
    """
    try:
        reshaped = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped)
        return font.render(bidi_text, True, color)
    except Exception as e:
        print(f"⚠️ Text render error: {e}")
        return font.render(text, True, color)

# ==========================================================
# POPUPS
# ==========================================================
def confirm_popup(screen, msg, font_loader):
    """Display Yes/No confirmation popup."""
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    box_width = int(SCREEN_WIDTH * 0.3)
    box_height = int(SCREEN_HEIGHT * 0.25)
    box = pygame.Rect(0, 0, box_width, box_height)
    box.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    pygame.draw.rect(screen, (255, 255, 255), box, border_radius=20)
    pygame.draw.rect(screen, (255, 102, 0), box, 4, border_radius=20)

    # Use font_loader callback to get font
    title_font = font_loader(int(SCREEN_HEIGHT * 0.04), bold=True)
    button_font = font_loader(int(SCREEN_HEIGHT * 0.03))

    text = render_text(msg, title_font, (0,0,0))
    screen.blit(text, (box.centerx - text.get_width() // 2, box.top + 25))

    btn_w, btn_h = int(box_width * 0.3), int(box_height * 0.35)
    yes = pygame.Rect(box.centerx - btn_w - 20, box.bottom - btn_h - 20, btn_w, btn_h)
    no = pygame.Rect(box.centerx + 20, box.bottom - btn_h - 20, btn_w, btn_h)

    pygame.draw.rect(screen, (0, 170, 0), yes, border_radius=10)
    pygame.draw.rect(screen, (170, 0, 0), no, border_radius=10)

    yes_text = render_text("Yes", button_font, (255, 255, 255))
    no_text = render_text("No", button_font, (255, 255, 255))
    screen.blit(yes_text, yes_text.get_rect(center=yes.center))
    screen.blit(no_text, no_text.get_rect(center=no.center))
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if yes.collidepoint(e.pos): return True
                elif no.collidepoint(e.pos): return False
        pygame.time.wait(10)

def info_popup(screen, msg, font_loader):
    """Display informational popup with OK button."""
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    box_width = int(SCREEN_WIDTH * 0.35)
    box_height = int(SCREEN_HEIGHT * 0.25)
    box = pygame.Rect(0, 0, box_width, box_height)
    box.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    pygame.draw.rect(screen, (255, 255, 255), box, border_radius=20)
    pygame.draw.rect(screen, (255, 102, 0), box, 4, border_radius=20)

    title_font = font_loader(int(SCREEN_HEIGHT * 0.035), bold=True)
    button_font = font_loader(int(SCREEN_HEIGHT * 0.03))

    lines = msg.split('\n')
    y_offset = box.top + 30
    for line in lines:
        text = render_text(line, title_font, (0,0,0))
        screen.blit(text, (box.centerx - text.get_width() // 2, y_offset))
        y_offset += int(SCREEN_HEIGHT * 0.045)

    btn_w, btn_h = int(box_width * 0.4), int(box_height * 0.35)
    ok_btn = pygame.Rect(box.centerx - btn_w // 2, box.bottom - btn_h - 20, btn_w, btn_h)

    pygame.draw.rect(screen, (0, 170, 0), ok_btn, border_radius=10)
    ok_text = render_text("OK", button_font, (255, 255, 255))
    screen.blit(ok_text, ok_text.get_rect(center=ok_btn.center))
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if ok_btn.collidepoint(e.pos): return
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_SPACE): return
        pygame.time.wait(10)
