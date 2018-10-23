import pygame
from pygame.sprite import Sprite


class Pacman(Sprite):
    """Pacman Sprite that controls all of Pacman's attributes"""
    def __init__(self, screen, settings, maze, portal, stats):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.stats = stats
        self.maze = maze
        self.portal = portal

        self.img = {0: 'images/Pacman.bmp',
                    1: 'images/Pacman2.bmp'}

        self.death_img = {0: 'images/Pacman.bmp',
                          1: 'images/pacman_death1.bmp',
                          2: 'images/pacman_death2.bmp',
                          3: 'images/pacman_death3.bmp',
                          4: 'images/pacman_death4.bmp',
                          5: 'images/pacman_death5.bmp'}

        self.image = pygame.image.load(self.img[0])
        self.left_image = pygame.transform.flip(self.image, True, False)
        self.up_image = pygame.transform.rotate(self.image, 90)
        self.down_image = pygame.transform.rotate(self.image, -90)

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        self.array_y = int(self.rect.centery/13)
        self.array_x = int(self.rect.centerx/13)
        self.count_right = 0
        self.count_left = 0
        self.count_up = 0
        self.count_down = 0
        self.delay = 0
        self.delay2 = 0

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.animate = False
        self.dead = False

    # Checks if pacman is in front of a wall
    def check_right_wall(self):
        if self.maze.rows[self.array_y][self.array_x + 2] == 'X' or \
                self.maze.rows[self.array_y+1][self.array_x + 2] == 'X' or \
                self.maze.rows[self.array_y-1][self.array_x + 2] == 'X':
            return True
        else:
            return False

    def check_left_wall(self):
        if self.maze.rows[self.array_y][self.array_x - 2] == 'X' or \
                self.maze.rows[self.array_y + 1][self.array_x - 2] == 'X' or \
                self.maze.rows[self.array_y - 1][self.array_x - 2] == 'X':
            return True
        else:
            return False

    def check_top_wall(self):
        if self.maze.rows[self.array_y - 2][self.array_x] == 'X' or \
                self.maze.rows[self.array_y - 2][self.array_x + 1] == 'X' or \
                self.maze.rows[self.array_y - 2][self.array_x - 1] == 'X':
            return True
        else:
            return False

    def check_bottom_wall(self):
        if self.maze.rows[self.array_y + 2][self.array_x] == 'X' or \
                self.maze.rows[self.array_y + 2][self.array_x + 1] == 'X' or \
                self.maze.rows[self.array_y + 2][self.array_x - 1] == 'X':
            return True
        else:
            return False

    def update(self):
        """Updates pacman's position as well as animating him"""

        # Animates pacman when he is moving
        if self.moving_right or self.moving_left or self.moving_up or self.moving_down:
            if not self.animate and self.delay == 50:
                if self.moving_right:
                    self.image = pygame.image.load(self.img[0])
                if self.moving_left:
                    self.image = self.left_image
                if self.moving_up:
                    self.image = self.up_image
                if self.moving_down:
                    self.image = self.down_image
                self.animate = True
                self.delay = 0
            if self.animate and self.delay == 50:
                self.image = pygame.image.load(self.img[1])
                self.animate = False
                self.delay = 0
            if self.delay > 50:
                self.delay = 0
            else:
                self.delay += 1

        # Moves when keys are pressed and not against a wall
        if self.moving_right and not Pacman.check_right_wall(self):
            self.rect.centerx += self.settings.pacman_speed_factor
            self.count_right += 1
            if self.count_right == 13:
                self.array_x += 1
                self.count_right = 0

        if self.moving_left and not Pacman.check_left_wall(self):
            self.rect.centerx -= self.settings.pacman_speed_factor
            self.count_left += 1
            if self.count_left == 13:
                self.array_x -= 1
                self.count_left = 0

        if self.moving_up and not Pacman.check_top_wall(self):
            self.rect.centery -= self.settings.pacman_speed_factor
            self.count_up += 1
            if self.count_up == 13:
                self.array_y -= 1
                self.count_up = 0

        if self.moving_down and not Pacman.check_bottom_wall(self):
            self.rect.centery += self.settings.pacman_speed_factor
            self.count_down += 1
            if self.count_down == 13:
                self.array_y += 1
                self.count_down = 0

        # Suppose to loop through to show pacman's death
        if self.delay2 == 100 and self.stats.index < 6 and self.stats.pacman_dead:
            self.image = pygame.image.load(self.death_img[self.stats.index])
            self.stats.index += 1
            self.delay2 = 0
        elif self.stats.index >= 6 and self.stats.pacman_dead:
            self.stats.index = 0
            self.stats.pacman_dead = False
        elif self.stats.pacman_dead:
            self.delay2 += 1

    def draw_portal(self):
        """Suppose to draw portal on wall"""
        if self.portal.orange_portal and Pacman.check_right_wall:
            self.portal.image = pygame.image.load(self.portal.img[1])
            self.screen.blit(self.portal.image, (self.rect.centerx, self.rect.centery))
        if self.portal.blue_portal and Pacman.check_right_wall:
            self.portal.image = pygame.image.load(self.portal.img[0])
            self.screen.blit(self.portal.image, (self.rect.centerx, self.rect.centery))
