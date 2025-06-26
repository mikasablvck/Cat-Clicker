# shop.py
import pygame

# Farben & Kosten
BLACK               = (0, 0, 0)
SHOP_BG             = (245, 230, 255)
SHOP_BORDER         = (180, 160, 200)
AUTOCLICKER_COST    = 50
SUPER_AUTOPET_COST  = 200

class Shop:
    WIDTH, HEIGHT  = 300, 300
    BTN_W, BTN_H   = 200, 35
    X_OFF          = 50
    Y_OFF          = [135, 210]

    def __init__(self):
        self.open = False

    def toggle(self):
        self.open = not self.open

    def _rects(self, sw: int, sh: int):
        x = (sw - self.WIDTH)//2
        y = (sh - self.HEIGHT)//2
        popup = pygame.Rect(x, y, self.WIDTH, self.HEIGHT)
        btn1  = pygame.Rect(x + self.X_OFF, y + self.Y_OFF[0], self.BTN_W, self.BTN_H)
        btn2  = pygame.Rect(x + self.X_OFF, y + self.Y_OFF[1], self.BTN_W, self.BTN_H)
        return popup, btn1, btn2

    def handle_click(self, pos, score, upgrades, sw: int, sh: int) -> int:
        _, btn1, btn2 = self._rects(sw, sh)

        if btn1.collidepoint(pos):
            score, bought = upgrades.buy_autoclicker(score)
            if bought:
                return score

        if btn2.collidepoint(pos):
            score, bought = upgrades.buy_super(score)
            if bought:
                return score

        return score

    def draw(self,
        screen: pygame.Surface,
        sw: int,
        sh: int,
        font: pygame.font.Font,
        yarn_icon: pygame.Surface,
        upgrades
        ):
        # Popup und Buttons berechnen
        popup, btn1, btn2 = self._rects(sw, sh)
        pygame.draw.rect(screen, SHOP_BG, popup, border_radius=16)
        pygame.draw.rect(screen, SHOP_BORDER, popup, 2, border_radius=16)

        # Überschrift
        title_font = pygame.font.Font("font/LavosHandy_99.ttf", font.get_height() + 1)
        title = title_font.render("Buy Autopets", True, BLACK)
        screen.blit(title, (popup.x + 30, popup.y + 10))  


        # Gemeinsame Icon-X‐Position berechnen (von Option 2)
        cost2_surf = font.render(f"{SUPER_AUTOPET_COST} for +2/s", True, BLACK)
        cost2_rect = cost2_surf.get_rect(midbottom=(btn2.centerx, btn2.y - 5))
        icon_x = cost2_rect.left - 8

        # Optionen definieren
        options = [
            (yarn_icon, f"{AUTOCLICKER_COST} for +1/s",   btn1, upgrades.autoclicker_active),
            (yarn_icon, f"{SUPER_AUTOPET_COST} for +2/s", btn2, upgrades.super_active)
        ]

        for idx, (icon, txt, btn, active) in enumerate(options):
            # 1) Kosten-Text rendern
            cost_surf = font.render(txt, True, BLACK)
            # beim zweiten Eintrag etwas weiter runter schieben
            y_offset = btn.y - 5    if idx == 0 else btn.y + 5
            cost_rect = cost_surf.get_rect(midbottom=(btn.centerx, y_offset))
            screen.blit(cost_surf, cost_rect)

            # 2) Icon auf gleicher X-Position, Y passend zum cost_rect
            icon_rect = icon.get_rect(midright=(icon_x, cost_rect.centery))
            screen.blit(icon, icon_rect)

            # 3) Button oder „Activated“ zeichnen
            if active:
                act = font.render("Activated", True, (0,200,0))
                act_rect = act.get_rect(midleft=(btn.x + 60, btn.y + 2))
                screen.blit(act, act_rect)
            else:
                pygame.draw.rect(screen, (200,255,200), btn, border_radius=8)
                buy = font.render("Buy", True, BLACK)
                buy_rect = buy.get_rect(center=btn.center)
                screen.blit(buy, buy_rect)

