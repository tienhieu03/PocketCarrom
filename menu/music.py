import pygame
from define import *


class Music():
    def __init__(self, game):
        self.game = game
        pygame.mixer.init()  # Initialize the mixer
        self.load_music()
        pygame.mixer.music.play()

    def load_music(self):
        pygame.mixer.music.load(PATH_SOUND + "8-bit.mp3")
        self.set_volume(1)  # Set initial volume

    def set_volume(self, volume=None):
        if volume is not None:
            self.volume = volume
        pygame.mixer.music.set_volume(self.volume)

    def increase_volume(self):
        self.volume = min(1.0, self.volume + 0.1)
        self.set_volume()

    def decrease_volume(self):
        self.volume = max(0.0, self.volume - 0.1)
        self.set_volume()

    def get_volume(self):
        return self.volume

