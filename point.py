import pygame
from pygame.sprite import Sprite


class Point(Sprite):
    POINT_SIZE = 5

    def __init__(self, screen, settings):
        super().__init__()
        self.screen = screen
        self.settings = settings

        sz = Point.POINT_SIZE
        self.image = pygame.image.load('images/point.png')
        self.image = pygame.transform.scale(self.image, (sz, sz))
        self.rect = self.image.get_rect()
