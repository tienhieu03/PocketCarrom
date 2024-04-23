import sys

import pygame

from define import *
from menu.menu import Menu
from menu.music import *


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.BACK_KEY:
                self.game.curr_menu = self.game.options
                self.run_display = False
            self.game.WINDOW_GAME.fill(COLOR_BLACK)
            self.game.draw_text('Credits', 20, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)
            self.game.draw_text('Nguyen Tien Hieu', 15, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
            self.game.draw_text('Trinh Gia Khanh', 15, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 30)
            self.game.draw_text('Nguyen Trung Hieu', 15, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 60)
            self.blit_screen()

class VolumeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        plus_btn_img = pygame.image.load(PATH_MENU + 'plus_btn.png').convert_alpha()
        minus_btn_img = pygame.image.load(PATH_MENU + 'minus_btn.png').convert_alpha()
        self.red_bar_img = pygame.image.load(PATH_MENU + 'red_bar.png').convert_alpha()
        # Resize the images
        resized_plus_btn_img = pygame.transform.scale(plus_btn_img, (40, 40))
        resized_minus_btn_img = pygame.transform.scale(minus_btn_img, (40, 40))
        self.plus_btn_img = resized_plus_btn_img
        self.minus_btn_img = resized_minus_btn_img
        self.volume_bar_width, self.volume_bar_height = VOLUME_BAR_SIZE
        self.filled_bar_width, self.filled_bar_height = FILLED_BAR_SIZE
        self.master_volume = MasterVolume(self)
        self.game = game
        self.music = Music(game)
        self.sfx = SoundEffect(game)
        self.effect1 = self.sfx.load_sound(PATH_SOUND + "collat.wav")
        self.selected_sound = "Master"

    def display_menu(self):
        self.run_display = True
        music_text_y = WINDOW_HEIGHT / 4 + 120
        sfx_text_y = WINDOW_HEIGHT / 4 + 230
        master_text_y = WINDOW_HEIGHT / 4 - 10
        while self.run_display:
            self.game.check_events()
            if self.game.BACK_KEY:
                self.game.curr_menu = self.game.options
                self.run_display = False
            self.game.WINDOW_GAME.fill(COLOR_BACKGROUND)
            self.game.draw_text('Volume', 20, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4 - 120)
            self.game.draw_text('Press T to test sound effect', 20, WINDOW_WIDTH / 2 + 350, WINDOW_HEIGHT - 20)
            self.game.draw_text('Master', 20, WINDOW_WIDTH / 2, master_text_y)
            self.game.draw_text('Music', 20, WINDOW_WIDTH / 2, music_text_y)
            self.game.draw_text('Sfx', 20, WINDOW_WIDTH / 2, sfx_text_y)

            if self.selected_sound == "Master":
                self.game.draw_text('>', 20, WINDOW_WIDTH / 2 - 80, master_text_y)
                self.game.draw_text('<', 20, WINDOW_WIDTH / 2 + 80, master_text_y)
            elif self.selected_sound == "Music":
                self.game.draw_text('>', 20, WINDOW_WIDTH / 2 - 80, music_text_y)
                self.game.draw_text('<', 20, WINDOW_WIDTH / 2 + 80, music_text_y)
            elif self.selected_sound == "Sfx":
                self.game.draw_text('>', 20, WINDOW_WIDTH / 2 - 80, sfx_text_y)
                self.game.draw_text('<', 20, WINDOW_WIDTH / 2 + 80, sfx_text_y)
            self.check_input()
            self.draw_volume_control()
            self.blit_screen()


    def draw_volume_control(self):
        # Draw minus button
        self.game.WINDOW_GAME.blit(self.minus_btn_img, (WINDOW_WIDTH / 2 - 160, WINDOW_HEIGHT / 3 + 80))
        self.game.WINDOW_GAME.blit(self.minus_btn_img, (WINDOW_WIDTH / 2 - 160, WINDOW_HEIGHT / 3 + 210))
        self.game.WINDOW_GAME.blit(self.minus_btn_img, (WINDOW_WIDTH / 2 - 160, WINDOW_HEIGHT / 3 - 50))

        # Draw plus button
        self.game.WINDOW_GAME.blit(self.plus_btn_img, (WINDOW_WIDTH / 2 + 120, WINDOW_HEIGHT / 3 + 80))
        self.game.WINDOW_GAME.blit(self.plus_btn_img, (WINDOW_WIDTH / 2 + 120, WINDOW_HEIGHT / 3 + 210))
        self.game.WINDOW_GAME.blit(self.plus_btn_img, (WINDOW_WIDTH / 2 + 120, WINDOW_HEIGHT / 3 - 50))

        # Calculate the width of the filled bar based on the volume level

        music_width = int(self.music.get_volume() * self.volume_bar_width - 4)
        music_width = max(0, min(music_width, self.volume_bar_width))
        music_red_bar = pygame.transform.scale(self.red_bar_img, (music_width, self.filled_bar_height))

        sfx_width = int(self.sfx.get_volume() * self.volume_bar_width - 4)
        sfx_width = max(0, min(sfx_width, self.volume_bar_width))
        sfx_red_bar = pygame.transform.scale(self.red_bar_img, (sfx_width, self.filled_bar_height))

        master_volume_width = int(self.master_volume.get_master_volume() * self.volume_bar_width - 4)
        master_volume_width = max(0, min(master_volume_width, self.volume_bar_width))
        master_volume_red_bar = pygame.transform.scale(self.red_bar_img, (master_volume_width, self.filled_bar_height))

        pygame.draw.rect(self.game.WINDOW_GAME, COLOR_WHITE,
                         (WINDOW_WIDTH / 2 - 102, WINDOW_HEIGHT / 3 + 80 - 2,
                          self.volume_bar_width, self.volume_bar_height), 2)
        self.game.WINDOW_GAME.blit(music_red_bar, (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 3 + 80))



        pygame.draw.rect(self.game.WINDOW_GAME, COLOR_WHITE,
                         (WINDOW_WIDTH / 2 - 102, WINDOW_HEIGHT / 3 + 210 - 2,
                          self.volume_bar_width, self.volume_bar_height), 2)
        self.game.WINDOW_GAME.blit(sfx_red_bar, (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 3 + 210))

        pygame.draw.rect(self.game.WINDOW_GAME, COLOR_WHITE,
                         (WINDOW_WIDTH / 2 - 102, WINDOW_HEIGHT / 3 - 50 - 2,
                          self.volume_bar_width, self.volume_bar_height), 2)
        self.game.WINDOW_GAME.blit(master_volume_red_bar, (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 3 - 50))

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.selected_sound == 'Master':
                self.selected_sound = 'Music'
                print("Selected sound:", self.selected_sound)
            elif self.selected_sound == 'Music':
                self.selected_sound = 'Sfx'
                print("Selected sound:", self.selected_sound)
            elif self.selected_sound == 'Sfx':
                self.selected_sound = 'Master'
                print("Selected sound:", self.selected_sound)
        elif self.game.UP_KEY:
            if self.selected_sound == 'Master':
                self.selected_sound = 'Sfx'
                print("Selected sound:", self.selected_sound)
            elif self.selected_sound == 'Music':
                self.selected_sound = 'Master'
                print("Selected sound:", self.selected_sound)
            elif self.selected_sound == 'Sfx':
                self.selected_sound = 'Music'
                print("Selected sound:", self.selected_sound)

    def check_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.selected_sound == "Master":
                self.master_volume.decrease_volume()
            elif self.selected_sound == "Music":
                self.music.decrease_volume()
            elif self.selected_sound == "Sfx":
                self.sfx.decrease_volume()

        if keys[pygame.K_RIGHT]:
            if self.selected_sound == "Master":
                self.master_volume.increase_volume()
            elif self.selected_sound == "Music":
                self.music.increase_volume()
            elif self.selected_sound == "Sfx":
                self.sfx.increase_volume()

        if keys[pygame.K_t]:
            self.sfx.play_sound(self.effect1)

        self.move_cursor()
    #TODO: Add volume control
