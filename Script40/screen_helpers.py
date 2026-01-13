# screen_helpers.py
import pygame, sys, os

def load_font(font_path, bold_font_path, size, bold=False, default_font_name="Arial"):
    try:
        path = bold_font_path if bold else font_path
        if path and os.path.exists(path):
            return pygame.font.Font(path, size)
        else:
            return pygame.font.SysFont(default_font_name, size)
    except Exception as e:
        print(f"Font load error: {e}. Falling back to default.")
        return pygame.font.SysFont(default_font_name, size)

def dynamic_font(screen_height, font_path, bold_font_path, size_ratio=0.05, bold=False):
    """Scale font size relative to screen height."""
    return load_font(font_path, bold_font_path, int(screen_height * size_ratio), bold=bold)

def confirm_popup(screen, msg, font_loader):
    """Display Yes/No confirmation popup centered on screen."""
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

    title_font = font_loader(int(SCREEN_HEIGHT * 0.04), bold=True)
    button_font = font_loader(int(SCREEN_HEIGHT * 0.03))

    text = title_font.render(msg, True, (0, 0, 0))
    screen.blit(text, (box.centerx - text.get_width() // 2, box.top + 25))

    btn_w, btn_h = int(box_width * 0.3), int(box_height * 0.35)
    yes = pygame.Rect(box.centerx - btn_w - 20, box.bottom - btn_h - 20, btn_w, btn_h)
    no = pygame.Rect(box.centerx + 20, box.bottom - btn_h - 20, btn_w, btn_h)

    pygame.draw.rect(screen, (0, 170, 0), yes, border_radius=10)
    pygame.draw.rect(screen, (170, 0, 0), no, border_radius=10)

    yes_text = button_font.render("Yes", True, (255, 255, 255))
    no_text = button_font.render("No", True, (255, 255, 255))
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
