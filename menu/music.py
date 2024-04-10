import pygame
from define import *


class Music():
    def __init__(self, game):
        pygame.mixer.init()  # Initialize the mixer
        self.load_music()
        pygame.mixer.music.play()


    def load_music(self):
        pygame.mixer.music.load(PATH_SOUND + "8-bit.mp3")
        self.set_volume(0.5)  # Set initial volume

    def set_volume(self, volume=None):
        if volume is not None:
            self.volume = volume
        pygame.mixer.music.set_volume(self.volume)

    def increase_volume(self):
        self.volume = min(1.0, self.volume + 0.25)
        self.set_volume()

    def decrease_volume(self):
        self.volume = max(0.0, self.volume - 0.25)
        self.set_volume()

    def get_volume(self):
        return self.volume
class SoundEffect():
    def __init__(self, game):
        pygame.mixer.init()  # Initialize the mixer
         # Set initial volume

    def load_sound(self, sound_file):
        self.set_volume(0.5)
        return pygame.mixer.Sound(sound_file)

    def play_sound(self, sound):
        sound.set_volume(self.volume)
        sound.play()

    def stop_sound(self, sound):
        sound.stop()

    def set_volume(self, volume):
        self.volume = volume

    def increase_volume(self):
        self.volume = min(1.0, self.volume + 0.25)

    def decrease_volume(self):
        self.volume = max(0.0, self.volume - 0.25)

    def get_volume(self):
        return self.volume


"""
if want to use
from menu.music import *

Example1: 
In init:
def __init__(self, game):
self.sfx = SoundEffect(game)
in event:
elif event.key == pygame.K_t:  # T key
                 ->  effect1 = self.sfx.load_sound(PATH_SOUND + "ahuevo.mp3")
                -> self.sfx.play_sound(effect1)
                 print("T key pressed")
                 
Example2:
in init:
def __init__(self, game):
self.sfx = SoundEffect(game)
        self.effect1 = self.sfx.load_sound(PATH_SOUND + "ahuevo.mp3")
        
        
in event:
                elif event.key == pygame.K_t:  # T key
        ->            self.sfx.play_sound(self.effect1)
                    print("T key pressed")

"""

