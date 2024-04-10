from define import *
from menu.menu import Menu
from menu.music import Music

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

        # Resize the images
        resized_plus_btn_img = pygame.transform.scale(plus_btn_img, (24, 24))
        resized_minus_btn_img = pygame.transform.scale(minus_btn_img, (24, 24))

        self.plus_btn_img = resized_plus_btn_img
        self.minus_btn_img = resized_minus_btn_img
        self.btn_width, self.btn_height = self.plus_btn_img.get_width(), self.plus_btn_img.get_height()
        self.plus_x, self.plus_y = PLUS_BTN_POSITION
        self.minus_x, self.minus_y = MINUS_BTN_POSITION
        self.volume_bar_width, self.volume_bar_height = VOLUME_BAR_SIZE
        self.volume_bar_position = VOLUME_BAR_POSITION
        self.filled_bar_width, self.filled_bar_height = FILLED_BAR_SIZE
        self.filled_bar_position = FILLED_BAR_POSITION
        self.music = Music(game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.BACK_KEY:
                self.game.curr_menu = self.game.options
                self.run_display = False
            self.game.WINDOW_GAME.fill(COLOR_BACKGROUND)
            self.game.draw_text('Volume', 20, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)
            self.draw_volume_control()
            self.handle_input()
            self.blit_screen()


    def draw_volume_control(self):
        # Draw minus button
        self.game.WINDOW_GAME.blit(self.minus_btn_img, (self.minus_x, self.minus_y))

        # Draw plus button
        self.game.WINDOW_GAME.blit(self.plus_btn_img, (self.plus_x, self.plus_y))

        # Draw volume bar
        pygame.draw.rect(self.game.WINDOW_GAME, COLOR_WHITE,
                         (self.volume_bar_position[0], self.volume_bar_position[1],
                          self.volume_bar_width, self.volume_bar_height), 2)

        # Calculate the width of the filled bar based on the volume level
        filled_width = int(self.music.get_volume() * self.volume_bar_width - 4)

        # Draw filled bar
        pygame.draw.rect(self.game.WINDOW_GAME, COLOR_RED,
                         (self.filled_bar_position[0], self.filled_bar_position[1],
                          filled_width, self.filled_bar_height))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Left arrow key
                    self.music.decrease_volume()
                    print("Left arrow key pressed")
                elif event.key == pygame.K_RIGHT:  # Right arrow key
                    self.music.increase_volume()
                    print("Right arrow key pressed")


    #TODO: Add volume control
