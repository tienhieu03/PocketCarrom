from define import *
from menu.menu import Menu

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

    #TODO: Add volume control
