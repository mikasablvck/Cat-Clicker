# sounds.py
import pygame, random

def load_sounds() -> list:
    return [
        pygame.mixer.Sound("meow/meow.wav"),
        pygame.mixer.Sound("meow/meow2.wav"),
        pygame.mixer.Sound("meow/meow3.wav")
    ]

def play_random_meow(meow_sounds: list):
    random.choice(meow_sounds).play()

MUSIC_TRACKS = [
    "sounds_lofi/lofi1.wav",
    "sounds_lofi/lofi2.wav",
    "sounds_lofi/lofi3.wav",
    "sounds_lofi/lofi4.wav",
    "sounds_lofi/lofi5.wav",
    "sounds_lofi/lofi6.wav",
    "sounds_lofi/lofi7.wav"
]
