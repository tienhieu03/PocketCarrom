import pygame
from define import *

class ForceBar:
    def __init__(self, window, max_force, current_force, color_max=(50, 248, 8, 1), color_current=COLOR_BLACK):
        self.window = window
        self.max_force = max_force
        self.current_force = current_force
        self.color_max = color_max
        self.color_current = color_current
        self.position = (350, 700)

    def draw(self):
        pygame.draw.rect(self.window, self.color_max, (*self.position, self.max_force * 5, 30))
        pygame.draw.rect(self.window, self.color_current, (*self.position, self.current_force * 5, 30))