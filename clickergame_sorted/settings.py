# settings.py
import pygame

class SettingsMenu:
    def __init__(self, x, y, width, initial_volume):
        self.slider_rect = pygame.Rect(x, y, width, 8)
        self.knob_radius = 8
        self.volume = initial_volume
        self.title_font = pygame.font.Font("font/LavosHandy_99.ttf", 48)
        self.font = pygame.font.Font("font/LavosHandy_99.ttf", 30) 

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_rect.collidepoint(event.pos):
                rel_x = event.pos[0] - self.slider_rect.x
                self.volume = max(0.0, min(1.0, rel_x / self.slider_rect.width))
        return self.volume

    def draw(self, screen, center_x, y):
        self.slider_rect = pygame.Rect(center_x - 150, y + 20, 300, 8)
        knob_x = self.slider_rect.x + int(self.volume * self.slider_rect.width)
        knob_center = (knob_x, self.slider_rect.y + 4)

        pygame.draw.rect(screen, (180, 180, 180), self.slider_rect, border_radius=4)
        pygame.draw.circle(screen, (100, 100, 255), knob_center, self.knob_radius)

        vol_text = self.font.render(f"Volume: {int(self.volume * 100)}%", True, (0, 0, 0))
        screen.blit(vol_text, (self.slider_rect.centerx - vol_text.get_width() // 2, self.slider_rect.y - 50))

    def draw_popup(self, screen, sw, sh, font_path, title_size=48):
        # Halbtransparenter Hintergrund
        overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        # Dialogbox
        box_w, box_h = 460, 220
        box = pygame.Rect((sw - box_w) // 2, (sh - box_h) // 2, box_w, box_h)
        pygame.draw.rect(screen, (235, 245, 255), box, border_radius=16)
        pygame.draw.rect(screen, (0, 0, 0), box, 2, border_radius=16)

        # Überschrift
        title_font = pygame.font.Font(font_path, title_size)
        title = title_font.render("Settings", True, (0, 0, 0))
        screen.blit(title, title.get_rect(center=(box.centerx, box.y + 36)))

        # Regler zeichnen
        self.draw(screen, center_x=box.centerx, y=box.y + 100)
