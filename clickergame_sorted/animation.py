# animation.py
import pygame

class Animator:
    def __init__(self, plopp_duration=200, hand_duration=300, wiggle_amp=5, wiggle_speed=100):
        self.plopp_duration = plopp_duration
        self.hand_duration = hand_duration
        self.wiggle_amp = wiggle_amp
        self.wiggle_speed = wiggle_speed

        self.scaled = False
        self.scale_time = 0

        self.show_hand = False
        self.hand_time = 0

        # Woll-Roll
        self.yarn_pos = 0.0
        self.yarn_angle = 0.0
        self.yarn_dir = 1

    def trigger_click(self, now: int):
        self.scaled = True
        self.scale_time = now
        self.show_hand = True
        self.hand_time = now

    def draw_click(self, screen, click_img, click_rect):
        now = pygame.time.get_ticks()
        if self.scaled and now - self.scale_time < self.plopp_duration:
            f = 1.05
            w, h = click_img.get_size()
            scaled = pygame.transform.scale(click_img, (int(w*f), int(h*f)))
            rect = scaled.get_rect(center=click_rect.center)
            screen.blit(scaled, rect)
        else:
            self.scaled = False
            screen.blit(click_img, click_rect)

    def draw_hand(self, screen, hand_img, click_rect):
        now = pygame.time.get_ticks()
        if self.show_hand and now - self.hand_time < self.hand_duration:
            elapsed = now - self.hand_time
            wig = (elapsed // self.wiggle_speed) % 2 * self.wiggle_amp
            hr = hand_img.get_rect(midtop=click_rect.midtop)
            hr.y -= 5 + wig
            screen.blit(hand_img, hr)
        else:
            self.show_hand = False

    def draw_yarn(self, screen, yarn_roll_img, screen_w, screen_h):
        # Position & Drehung aktualisieren
        self.yarn_pos += self.yarn_dir * 1.5
        self.yarn_angle -= self.yarn_dir * 4
        if self.yarn_pos > screen_w - 43 or self.yarn_pos < 0:
            self.yarn_dir *= -1

        rot = pygame.transform.rotate(yarn_roll_img, self.yarn_angle)
        rect = rot.get_rect(center=(int(self.yarn_pos + 36), screen_h - 36))
        screen.blit(rot, rect)
