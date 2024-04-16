from menu.menu import *
from menu.options import *
from menu.music import *
from play_game import *


class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False, False
        self.WINDOW_GAME = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        title = pygame.display.set_caption("Pocket Carrom")
        icon = pygame.display.set_icon(pygame.image.load(PATH_IMAGE + "icon.ico"))
        self.font_name = 'dogicapixelbold.ttf'
        self.window_color = COLOR_BACKGROUND
        self.master_volume = MasterVolume(self)
        self.music = Music(self)
        self.sfx = SoundEffect(self)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.volume = VolumeMenu(self)
        self.curr_menu = self.main_menu
        self.run = True
        self.music.load_music(PATH_SOUND + "8-bit.mp3")
        self.music.play_music()

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
                game = PlayGame()
                game.start_game()
            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_RETURN:
                    self.START_KEY = True
               if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
               if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
               if event.key == pygame.K_UP:
                    self.UP_KEY = True
               if event.key == pygame.K_LEFT:
                   self.LEFT_KEY = True
               if event.key == pygame.K_RIGHT:
                   self.RIGHT_KEY = True
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self,text,size,x,y):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text,True,COLOR_WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.WINDOW_GAME.blit(text_surface,text_rect)