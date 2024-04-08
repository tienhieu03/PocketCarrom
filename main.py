import pygame
from game import Game

FPS = 60
clock = pygame.time.Clock()

g = Game()

while g.running:
    clock.tick(FPS)
    g.curr_menu.display_menu()
    g.game_loop()