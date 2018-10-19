import pygame
from pygame.sprite import Sprite


class Fruit(Sprite):
    FRUIT_SIZE = 30

    def __init__(self, screen, settings):
        super().__init__()
        self.screen = screen
        self.settings = settings

        self.sz = Fruit.FRUIT_SIZE
        self.img = {0: 'images/apple.bmp',
                    1: 'images/cherry.bmp',
                    2: 'images/banana.bmp',
                    3: 'images/strawberry.bmp'}
        self.image = pygame.image.load(self.img[0])
        self.image = pygame.transform.scale(self.image, (self.sz, self.sz))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

    def which_fruit(self, fruit_count):
        self.image = pygame.image.load(self.img[fruit_count])
        self.image = pygame.transform.scale(self.image, (self.sz, self.sz))
