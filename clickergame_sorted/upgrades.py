# upgrades.py
from typing import Tuple

class Upgrades:
    def __init__(self, autocost=50, supercost=200):
        self.autocost = autocost
        self.supercost = supercost
        self.autoclicker_active = False
        self.super_active = False

    def buy_autoclicker(self, score: int) -> Tuple[int, bool]:
        """
        Versucht, den Autoclicker zu kaufen.
        Gibt (neuer_score, erfolgreich_gekauft) zurück
        und setzt bei Erfolg self.autoclicker_active = True.
        """
        if not self.autoclicker_active and score >= self.autocost:
            score -= self.autocost
            self.autoclicker_active = True      # WICHTIG!
            return score, True
        return score, False

    def buy_super(self, score: int) -> Tuple[int, bool]:
        """
        Versucht, das Super-Autopet zu kaufen.
        Gibt (neuer_score, erfolgreich_gekauft) zurück
        und setzt bei Erfolg self.super_active = True.
        """
        if not self.super_active and score >= self.supercost:
            score -= self.supercost
            self.super_active = True            # WICHTIG!
            return score, True
        return score, False

    def get_rate(self) -> int:
        """1/s pro Autoclicker, 2/s pro Super-Autopet."""
        return int(self.autoclicker_active) * 1 + int(self.super_active) * 2
