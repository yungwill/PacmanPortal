import pygame
from pygame.sprite import Sprite


class Ghost(Sprite):
    """Ghost Sprite with all of its atrributes"""
    def __init__(self, screen, settings, maze):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.maze = maze
        self.img = {0: 'images/clyde_left1.bmp',
                    1: 'images/pinky_left1.bmp',
                    2: 'images/inkey_left_1.bmp',
                    3: 'iamges/blinky_left1.bmp'}

        self.scared_img = {0: 'images/scared_ghost.png',
                           1: 'images/scared_ghost2.png'}

        self.image = pygame.image.load(self.img[0])
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.array_y = 19
        self.array_x = 24

        self.rect.centerx = self.array_x * 13
        self.rect.centery = self.array_y * 13

        self.animate = False
        self.scared = False
        self.count_right = 0
        self.count_left = 0
        self.count_up = 0
        self.count_down = 0
        self.move = 0
        self.delay = 0
        self.delay2 = 0

    # Checks to see if ghost is moving into a wall
    def check_right_wall(self):
        if self.maze.rows[self.array_y][self.array_x + 1] == 'X':
            return True
        else:
            return False

    def check_left_wall(self):
        if self.maze.rows[self.array_y][self.array_x - 2] == 'X':
            return True
        else:
            return False

    def check_top_wall(self):
        if self.maze.rows[self.array_y - 2][self.array_x] == 'X':
            return True
        else:
            return False

    def check_bottom_wall(self):
        if self.maze.rows[self.array_y + 1][self.array_x] == 'X':
            return True
        else:
            return False

    def update(self):
        """Updates ghost's position based on the movement flag"""

        if self.move == 0 and not Ghost.check_right_wall(self):
            self.rect.centerx += self.settings.ghost_speed_factor
            self.count_right += 1
            if self.count_right == 13:
                self.array_x += 1
                self.count_right = 0

        if self.move == 1 and not Ghost.check_left_wall(self):
            self.rect.centerx -= self.settings.ghost_speed_factor
            self.count_left += 1
            if self.count_left == 13:
                self.array_x -= 1
                self.count_left = 0

        if self.move == 2 and not Ghost.check_top_wall(self):
            self.rect.centery -= self.settings.ghost_speed_factor
            self.count_up += 1
            if self.count_up == 13:
                self.array_y -= 1
                self.count_up = 0

        if self.move == 3 and not Ghost.check_bottom_wall(self):
            self.rect.centery += self.settings.ghost_speed_factor
            self.count_down += 1
            if self.count_down == 13:
                self.array_y += 1
                self.count_down = 0

        if Ghost.check_right_wall(self):
            self.move = 3

        if Ghost.check_left_wall(self):
            self.move = 2

        if Ghost.check_top_wall(self):
            self.move = 0

        if Ghost.check_bottom_wall(self):
            self.move = 1

        if self.scared and self.delay2 < 1600:
            if not self.animate and self.delay == 50:
                self.image = pygame.image.load(self.scared_img[0])
                self.animate = True
                self.delay = 0
            if self.animate and self.delay == 50:
                if self.delay2 > 800:
                    self.image = pygame.image.load(self.scared_img[1])
                self.animate = False
                self.delay = 0
            else:
                self.delay += 1
            self.delay2 += 1
        else:
            self.scared = False
            self.image = pygame.image.load(self.img[0])
            self.delay2 = 0
