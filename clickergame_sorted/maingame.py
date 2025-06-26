# main.py
import pygame, sys
from pictures   import load_images
from sounds     import load_sounds, play_random_meow
from upgrades   import Upgrades
from animation  import Animator
from shop       import Shop
from sounds import MUSIC_TRACKS
from settings import SettingsMenu

volume = 0.5  # Startlautstärke 

# Farben & Schrift
BLACK        = (0, 0, 0)
FONT_PATH    = "font/LavosHandy_99.ttf"
FONT_SIZE    = 30

show_settings = False

pygame.mixer.init()

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    sw, sh = screen.get_size()
    pygame.display.set_caption("Cat Clicker")

    volume = 0.5  # Startwert zwischen 0.0 und 1.0
    settings_menu = SettingsMenu(100, 100, 300, volume)

    #Hintergrundmusik
    current_track = 0
    pygame.mixer.music.load(MUSIC_TRACKS[current_track])
    pygame.mixer.music.play(fade_ms=1500)
    pygame.mixer.music.set_volume(0.5)
    next_track_time = pygame.time.get_ticks() + 120000  #Sekunden

    #Einstellungen
    show_settings = False
    settings_menu = SettingsMenu(100, 100, 300, volume)

    # Ressourcen & Module
    assets   = load_images(sw, sh)
    meows    = load_sounds()
    for sound in meows:
        sound.set_volume(volume)

    pygame.mixer.music.set_volume(volume)

    upgrades = Upgrades()
    shop     = Shop()
    anim     = Animator()
    font     = pygame.font.Font(FONT_PATH, FONT_SIZE)

    # Klickbereich für Katze
    click_rect = assets["clicker"].get_rect(center=(sw // 2, sh * 3 // 4))

    # Exit-Button vorbereiten
    exit_surf = font.render("Escape to Reality", True, BLACK)
    ex_w, ex_h = exit_surf.get_size()
    exit_rect = pygame.Rect(sw - ex_w - 64, sh - ex_h - 36, ex_w + 44, ex_h + 16)

    # Status-Variablen
    score         = 0
    last_auto     = 0
    confirm_quit  = False
    yes_rect      = no_rect = None

    clock = pygame.time.Clock()
    running = True
    while running:
        now = pygame.time.get_ticks()

        # EVENTS
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                confirm_quit = True

            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = ev.pos

                # Wenn Quit-Dialog offen ist, nur darauf reagieren
                if confirm_quit:
                    if yes_rect and yes_rect.collidepoint((mx, my)):
                        running = False
                    elif no_rect and no_rect.collidepoint((mx, my)):
                        confirm_quit = False
                    continue

                # Klick auf Katze
                if click_rect.collidepoint(mx, my):
                    score += 1
                    anim.trigger_click(now)
                    play_random_meow(meows)

                # Klick auf Shop-Icon
                shop_img, shop_rect = assets["shop"]
                if shop_rect.collidepoint(mx, my):
                    shop.toggle()

                # Klick auf Settings
                gear_img, gear_rect = assets["gear"]
                if gear_rect.collidepoint(mx, my):
                    show_settings = not show_settings
                if show_settings:
                    volume = settings_menu.handle_event(ev)
                    pygame.mixer.music.set_volume(volume)
                    for s in meows:
                        s.set_volume(volume)

                # Klick im Shop
                if shop.open:
                    score = shop.handle_click((mx, my), score, upgrades, sw, sh)

                # Klick auf Exit
                if exit_rect.collidepoint(mx, my):
                    confirm_quit = True

        # Hintergrundmusik
        if pygame.time.get_ticks() > next_track_time:
            current_track = (current_track + 1) % len(MUSIC_TRACKS)
            pygame.mixer.music.fadeout(1000)  # sanft ausfaden
            pygame.mixer.music.load(MUSIC_TRACKS[current_track])
            pygame.mixer.music.play(fade_ms=1000)
            next_track_time = pygame.time.get_ticks() + 120000  # nächste Track-Dauer


        # AUTOKLICKER
        rate = upgrades.get_rate()
        if rate and now - last_auto >= 1000:
            score += rate
            last_auto = now

        # ZEICHNEN
        screen.blit(assets["background"], (0, 0))
        screen.blit(*assets["shop"])
        screen.blit(*assets["gear"])

        # Katze & Animation
        anim.draw_click(screen, assets["clicker"], click_rect)
        anim.draw_hand(screen, assets["hand"], click_rect)
        if upgrades.super_active:
            anim.draw_yarn(screen, assets["yarn_roll"], sw, sh)

        # Punktestand-Box
        score_surf = font.render(f"Cat Yarn: {score}", True, BLACK)
        yarn_icon  = assets["yarn_icon"]
        tr, ir     = score_surf.get_rect(), yarn_icon.get_rect()
        box_w      = tr.width + ir.width + 16 + 20
        box_h      = max(tr.height, ir.height) + 16
        box_rect   = pygame.Rect(10, 10, box_w, box_h)
        pygame.draw.rect(screen, (255,204,229), box_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, box_rect, 2, border_radius=10)
        screen.blit(score_surf, (box_rect.x + 10, box_rect.y + 8))
        screen.blit(yarn_icon, (box_rect.x + 20 + tr.width, box_rect.y + 8))

        # Shop
        screen.blit(*assets["shop"])
        if shop.open:
            shop.draw(screen, sw, sh, font, yarn_icon, upgrades)

        # Exit-Button
        pygame.draw.rect(screen, (255,180,180), exit_rect, border_radius=12)
        pygame.draw.rect(screen, BLACK, exit_rect, 2, border_radius=12)
        screen.blit(exit_surf, exit_surf.get_rect(center=exit_rect.center))

        # QUIT-DIALOG
        if confirm_quit:
            overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))

            box_w, box_h = 460, 400
            box = pygame.Rect((sw - box_w) // 2, (sh - box_h) // 2, box_w, box_h)
            pygame.draw.rect(screen, (255, 235, 235), box, border_radius=16)
            pygame.draw.rect(screen, BLACK, box, 2, border_radius=16)

            dialog_font = pygame.font.Font(FONT_PATH, 28)
            prompt = "You really wanna leave?\nPromise me to come back."
            lines = prompt.split("\n")
            for i, line in enumerate(lines):
                t = dialog_font.render(line, True, BLACK)
                screen.blit(t, t.get_rect(center=(box.centerx, box.y + 40 + i * 32)))

            # Katzenbild darunter zentrieren
            sad_cat = assets["sad_cat"]  
            cat_y = box.y + box_h // 2 + 10
            cat_rect = sad_cat.get_rect(center=(box.centerx, cat_y))
            screen.blit(sad_cat, cat_rect)

            mouse_pos = pygame.mouse.get_pos()
            yes_hover = yes_rect and yes_rect.collidepoint(mouse_pos)
            no_hover  = no_rect  and no_rect.collidepoint(mouse_pos)

            yes_color = (180, 240, 180) if yes_hover else (200, 255, 200)
            no_color  = (240, 180, 180) if no_hover  else (255, 200, 200)

            yes_rect = pygame.Rect(box.centerx - 120, box.bottom - 45, 100, 36)
            no_rect  = pygame.Rect(box.centerx +  20, box.bottom - 45, 100, 36)
            pygame.draw.rect(screen, yes_color, yes_rect, border_radius=8)
            pygame.draw.rect(screen, no_color,  no_rect,  border_radius=8)

            y_txt = dialog_font.render("I promise", True, BLACK)
            n_txt = dialog_font.render("Nope", True, BLACK)
            screen.blit(y_txt, y_txt.get_rect(center=yes_rect.center))
            screen.blit(n_txt, n_txt.get_rect(center=no_rect.center))

        # Settings
        if show_settings:
            overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))

        if show_settings:
            settings_menu.draw_popup(screen, sw, sh, FONT_PATH)

            # Gear- und Escape sichtbar über dem Schatten
            screen.blit(*assets["gear"])
            pygame.draw.rect(screen, BLACK, exit_rect, 2, border_radius=12)
            screen.blit(exit_surf, exit_surf.get_rect(center=exit_rect.center))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()