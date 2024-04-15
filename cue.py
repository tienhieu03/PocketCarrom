import pygame
class Cue():
    cue_image = pygame.image.load("assets/game/circles2.png")
    def __init__(self, pos):
        self.original_image = self.cue_image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, (self.rect.centerx - self.image.get_width() / 2,self.rect.centery - self.image.get_height() / 2))
        #pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)
    def update(self, angle):
        self.angle = angle