import pygame
from define import *

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
        self.start_img = pygame.image.load(PATH_MENU + 'start_btn.png').convert()
        self.start_hover_img = pygame.image.load(PATH_MENU + 'start_hover.png').convert()
        self.options_img = pygame.image.load(PATH_MENU + 'option_btn.png').convert()
        self.options_hover_img = pygame.image.load(PATH_MENU + 'option_hover.png').convert()
        self.exit_img = pygame.image.load(PATH_MENU + 'exit_btn.png').convert()
        self.exit_hover_img = pygame.image.load(PATH_MENU + 'exit_hover.png').convert()
        self.volume_img = pygame.image.load(PATH_MENU + 'volume_btn.png').convert()
        self.volume_hover_img = pygame.image.load(PATH_MENU + 'volume_hover.png').convert()
        self.credits_img = pygame.image.load(PATH_MENU + 'credits_btn.png').convert()
        self.credits_hover_img = pygame.image.load(PATH_MENU + 'credits_hover.png').convert()


    def blit_screen(self):
        self.game.WINDOW_GAME.blit(self.game.WINDOW_GAME, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state = "Start"
        self.startx, self.starty = START_POSITION
        self.optionsx, self.optionsy = OPTIONS_POSITION
        self.exitx, self.exity = EXIT_POSITION


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.WINDOW_GAME.fill(self.game.window_color)
            self.game.draw_text('Main Menu', 48, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4 - 60)
            self.draw_menu_options()
            self.blit_screen()

    def draw_menu_options(self):
        if self.state == 'Start':
            self.game.WINDOW_GAME.blit(self.start_hover_img, (self.startx, self.starty))
            self.game.WINDOW_GAME.blit(self.options_img, (self.optionsx, self.optionsy))
            self.game.WINDOW_GAME.blit(self.exit_img, (self.exitx, self.exity))
        elif self.state == 'Options':
            self.game.WINDOW_GAME.blit(self.start_img, (self.startx, self.starty))
            self.game.WINDOW_GAME.blit(self.options_hover_img, (self.optionsx, self.optionsy))
            self.game.WINDOW_GAME.blit(self.exit_img, (self.exitx, self.exity))
        elif self.state == 'Exit':
            self.game.WINDOW_GAME.blit(self.start_img, (self.startx, self.starty))
            self.game.WINDOW_GAME.blit(self.options_img, (self.optionsx, self.optionsy))
            self.game.WINDOW_GAME.blit(self.exit_hover_img, (self.exitx, self.exity))

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
                self.game.game_loop()
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Exit':
                self.game.running, self.game.playing = False, False
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volumex, self.volumey = VOLUME_POSITION
        self.creditsx, self.creditsy = CREDITS_POSITION

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.WINDOW_GAME.fill(self.game.window_color)
            self.game.draw_text('Options', 48, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4 - 60)
            self.draw_menu_options()
            self.blit_screen()

    def draw_menu_options(self):
        if self.state == 'Volume':
            self.game.WINDOW_GAME.blit(self.volume_hover_img, (self.volumex, self.volumey))
            self.game.WINDOW_GAME.blit(self.credits_img, (self.creditsx, self.creditsy))
        elif self.state == 'Credits':
            self.game.WINDOW_GAME.blit(self.volume_img, (self.volumex, self.volumey))
            self.game.WINDOW_GAME.blit(self.credits_hover_img, (self.creditsx, self.creditsy))

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.volumex + self.offset, self.volumey)
                self.state = 'Volume'
        elif self.game.UP_KEY:
            if self.state == 'Volume':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.volumex + self.offset, self.volumey)
                self.state = 'Volume'

    def check_input(self):
        self.move_cursor()
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.START_KEY:
            if self.state == 'Volume':
                #TODO: Add volume control
                self.game.curr_menu = self.game.volume
                self.run_display = False
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
                self.run_display = False



