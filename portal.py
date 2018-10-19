import pygame
from pygame.sprite import Sprite


class Portal(Sprite):
    def __init__(self, screen, settings):
        super().__init__()
        self.screen = screen
        self.settings = settings

        self.img = {0: 'images/blue_portal.bmp',
                    1: 'images/orange_portal.bmp'}

        self.image = pygame.image.load(self.img[1])
        self.temp = pygame.image.load(self.img[0])
        self.horizontal_oPortal = pygame.transform.rotate(self.image, 90)
        self.horizontal_bPortal = pygame.transform.rotate(self.temp, 90)

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.blue_portal = False
        self.orange_portal = False
