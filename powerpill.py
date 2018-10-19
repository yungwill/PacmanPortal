import pygame
from pygame.sprite import Sprite


class PowerPill(Sprite):
    PILL_SIZE = 15

    def __init__(self, screen, settings):
        super().__init__()
        self.screen = screen
        self.settings = settings

        sz = PowerPill.PILL_SIZE
        self.image = pygame.image.load('images/power_pill.png')
        self.image = pygame.transform.scale(self.image, (sz, sz))
        self.rect = self.image.get_rect()
