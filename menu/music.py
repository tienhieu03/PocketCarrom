import pygame
from define import *


class MasterVolume:
    def __init__(self, game):
        self.game = game
        self.volume = 1

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        self.update_music_volume()
        self.update_sfx_volume()

    def increase_volume(self):
        self.set_volume(self.volume + 0.01)

    def decrease_volume(self):
        self.set_volume(self.volume - 0.01)

    def get_master_volume(self):
        return self.volume

    def update_music_volume(self):
        self.game.music.set_master_volume(self.volume)

    def update_sfx_volume(self):
        self.game.sfx.set_master_volume(self.volume)

class Music:
    def __init__(self, game):
        self.game = game
        self.volume = 0.5  # Initial music volume
        self.master_volume = 1  # Initial master volume
        pygame.mixer.music.set_volume(self.volume * self.master_volume)
        pygame.mixer.init()  # Initialize the mixer

    def load_music(self, music_file):
        pygame.mixer.music.load(music_file)

    def play_music(self):
        pygame.mixer.music.play(-1)

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))  # Ensure volume is within [0, 1]
        self.update_volume()

    def update_volume(self):
        # Adjust the music volume based on both its own volume and the master volume
        pygame.mixer.music.set_volume(self.volume * self.master_volume)

    def set_master_volume(self, master_volume):
        self.master_volume = max(0.0, min(1.0, master_volume))  # Ensure volume is within [0, 1]
        self.update_volume()

    def increase_volume(self):
        self.set_volume(self.volume + 0.01)

    def decrease_volume(self):
        self.set_volume(self.volume - 0.01)

    def get_volume(self):
        return self.volume


class SoundEffect():
    def __init__(self, game):
        self.game = game
        self.master_volume = 1
        self.volume = 0.5
        pygame.mixer.init()



    def load_sound(self, sound_file):
        return pygame.mixer.Sound(sound_file)

    def play_sound(self, sound):
        sound.set_volume(self.volume * self.master_volume)  # Set volume of the sound
        sound.play()

    def stop_sound(self, sound):
        sound.stop()

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))  # Ensure volume is within [0, 1]

    def set_master_volume(self, master_volume):
        self.master_volume = max(0.0, min(1.0, master_volume))  # Ensure volume is within [0, 1]

    def increase_volume(self):
        self.volume = min(1.0, self.volume + 0.01)

    def decrease_volume(self):
        self.volume = max(0.0, self.volume - 0.01)

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
                 ->  effect1 = self.sfx.load_sound(PATH_SOUND + "shot.mp3")
                -> self.sfx.play_sound(effect1)
                 print("T key pressed")

Example2:
in init:
def __init__(self, game):
self.sfx = SoundEffect(game)
        self.effect1 = self.sfx.load_sound(PATH_SOUND + "shot.mp3")


in event:
                elif event.key == pygame.K_t:  # T key
        ->            self.sfx.play_sound(self.effect1)
                    print("T key pressed")

"""

