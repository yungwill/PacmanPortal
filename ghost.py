import pygame
import random
from pygame.sprite import Sprite


class Ghost(Sprite):
    """Ghost Sprite with all of its atrributes"""
    def __init__(self, screen, settings, maze, stats, num):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.stats = stats
        self.maze = maze
        self.num = num
        self.clyde_img = {0: 'images/clyde_left1.bmp',
                          1: 'images/clyde_right1.bmp',
                          2: 'images/clyde_up1.bmp',
                          3: 'images/clyde_down1.bmp',
                          4: 'images/clyde_left2.bmp',
                          5: 'images/clyde_right2.bmp',
                          6: 'images/clyde_up2.bmp',
                          7: 'images/clyde_down2.bmp'}

        self.blinky_img = {0: 'images/blinky_left1.bmp',
                           1: 'images/blinky_right1.bmp',
                           2: 'images/blinky_up1.bmp',
                           3: 'images/blinky_down1.bmp',
                           4: 'images/blinky_left2.bmp',
                           5: 'images/blinky_right2.bmp',
                           6: 'images/blinky_up2.bmp',
                           7: 'images/blinky_down2.bmp'}

        self.inkey_img = {0: 'images/inkey_left1.bmp',
                          1: 'images/inkey_right1.bmp',
                          2: 'images/inkey_up1.bmp',
                          3: 'images/inkey_down1.bmp',
                          4: 'images/inkey_left2.bmp',
                          5: 'images/inkey_right2.bmp',
                          6: 'images/inkey_up2.bmp',
                          7: 'images/inkey_down2.bmp'}

        self.pinky_img = {0: 'images/pinky_left1.bmp',
                          1: 'images/pinky_right1.bmp',
                          2: 'images/pinky_up1.bmp',
                          3: 'images/pinky_down1.bmp',
                          4: 'images/pinky_left2.bmp',
                          5: 'images/pinky_right2.bmp',
                          6: 'images/pinky_up2.bmp',
                          7: 'images/pinky_down2.bmp'}

        self.scared_img = {0: 'images/scared_ghost.png',
                           1: 'images/scared_ghost2.png'}

        self.eaten_img = {0: 'images/eyes_left.bmp',
                          1: 'images/eyes_right.bmp',
                          2: 'images/eyes_up.bmp',
                          3: 'images/eyes_down.bmp'}

        if self.num == 0:
            self.image = pygame.image.load(self.clyde_img[1])
        if self.num == 1:
            self.image = pygame.image.load(self.blinky_img[1])
        if self.num == 2:
            self.image = pygame.image.load(self.pinky_img[1])
        if self.num == 3:
            self.image = pygame.image.load(self.inkey_img[1])

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.array_y = 19
        self.array_x = 24

        self.rect.centerx = self.array_x * 13
        self.rect.centery = self.array_y * 13

        self.scared_animate, self.right_animate, self.left_animate = False, False, False
        self.up_animate, self.down_animate = False, False
        self.eaten = False
        self.count_right, self.count_left, self.count_up, self.count_down = 0, 0, 0, 0
        self.move = random.randint(0, 3)
        self.delay = 0
        self.delay2 = 0
        self.delay_right, self.delay_left, self.delay_up, self.delay_down = 0, 0, 0, 0

    # Checks to see if ghost is moving into a wall
    def check_right_wall(self):
        if self.maze.rows[self.array_y][self.array_x + 1] == 'X':
            self.move = random.randint(0, 3)
            return True
        else:
            return False

    def check_left_wall(self):
        if self.maze.rows[self.array_y][self.array_x - 2] == 'X':
            self.move = random.randint(0, 3)
            return True
        else:
            return False

    def check_top_wall(self):
        if self.maze.rows[self.array_y - 2][self.array_x] == 'X':
            self.move = random.randint(0, 3)
            return True
        else:
            return False

    def check_bottom_wall(self):
        if self.maze.rows[self.array_y + 1][self.array_x] == 'X':
            self.move = random.randint(0, 3)
            return True
        else:
            return False

    def update(self):
        """Updates ghost's position based on the movement flag"""

        if self.move == 0 and not Ghost.check_right_wall(self):
            if not self.stats.ghost_scared and self.delay_right == 75 and not self.right_animate \
                    and not self.eaten:
                if self.num == 0:
                    self.image = pygame.image.load(self.clyde_img[1])
                if self.num == 1:
                    self.image = pygame.image.load(self.blinky_img[1])
                if self.num == 2:
                    self.image = pygame.image.load(self.pinky_img[1])
                if self.num == 3:
                    self.image = pygame.image.load(self.inkey_img[1])
                self.right_animate = True
                self.delay_right = 0
            if not self.stats.ghost_scared and self.delay_right == 75 and self.right_animate \
                    and not self.eaten:
                if self.num == 0:
                    self.image = pygame.image.load(self.clyde_img[5])
                if self.num == 1:
                    self.image = pygame.image.load(self.blinky_img[5])
                if self.num == 2:
                    self.image = pygame.image.load(self.pinky_img[5])
                if self.num == 3:
                    self.image = pygame.image.load(self.inkey_img[5])
                self.right_animate = False
                self.delay_right = 0
            else:
                self.delay_right += 1
            if self.eaten:
                self.image = pygame.image.load(self.eaten_img[1])

            self.rect.centerx += self.settings.ghost_speed_factor
            self.count_right += 1
            if self.count_right == 13:
                self.array_x += 1
                self.count_right = 0

        elif self.move == 1 and not Ghost.check_left_wall(self):
            if not self.stats.ghost_scared and self.delay_left == 75 and not self.left_animate \
                    and not self.eaten:
                if self.num == 0:
                    self.image = pygame.image.load(self.clyde_img[0])
                if self.num == 1:
                    self.image = pygame.image.load(self.blinky_img[0])
                if self.num == 2:
                    self.image = pygame.image.load(self.pinky_img[0])
                if self.num == 3:
                    self.image = pygame.image.load(self.inkey_img[0])
                self.left_animate = True
                self.delay_left = 0
            if not self.stats.ghost_scared and self.delay_left == 75 and self.left_animate \
                    and not self.eaten:
                if self.num == 0:
                    self.image = pygame.image.load(self.clyde_img[4])
                if self.num == 1:
                    self.image = pygame.image.load(self.blinky_img[4])
                if self.num == 2:
                    self.image = pygame.image.load(self.pinky_img[4])
                if self.num == 3:
                    self.image = pygame.image.load(self.inkey_img[4])
                self.left_animate = False
                self.delay_left = 0
            else:
                self.delay_left += 1
            if self.eaten:
                self.image = pygame.image.load(self.eaten_img[0])

            self.rect.centerx -= self.settings.ghost_speed_factor
            self.count_left += 1
            if self.count_left == 13:
                self.array_x -= 1
                self.count_left = 0

        elif self.move == 2 and not Ghost.check_top_wall(self):
            if not self.stats.ghost_scared and self.delay_up == 75 and not self.up_animate \
                    and not self.eaten:
                if self.num == 0:
                    self.image = pygame.image.load(self.clyde_img[2])
                if self.num == 1:
                    self.image = pygame.image.load(self.blinky_img[2])
                if self.num == 2:
                    self.image = pygame.image.load(self.pinky_img[2])
                if self.num == 3:
                    self.image = pygame.image.load(self.inkey_img[2])
                self.up_animate = True
                self.delay_up = 0
            if not self.stats.ghost_scared and self.delay_up == 75 and self.up_animate \
                    and not self.eaten:
                if self.num == 0:
                    self.image = pygame.image.load(self.clyde_img[6])
                if self.num == 1:
                    self.image = pygame.image.load(self.blinky_img[6])
                if self.num == 2:
                    self.image = pygame.image.load(self.pinky_img[6])
                if self.num == 3:
                    self.image = pygame.image.load(self.inkey_img[6])
                self.up_animate = False
                self.delay_up = 0
            else:
                self.delay_up += 1
            if self.eaten:
                self.image = pygame.image.load(self.eaten_img[2])

            self.rect.centery -= self.settings.ghost_speed_factor
            self.count_up += 1
            if self.count_up == 13:
                self.array_y -= 1
                self.count_up = 0

        elif self.move == 3 and not Ghost.check_bottom_wall(self):
            if not self.stats.ghost_scared and self.delay_down == 75 and not self.down_animate \
                    and not self.eaten:
                if self.num == 0:
                    self.image = pygame.image.load(self.clyde_img[3])
                if self.num == 1:
                    self.image = pygame.image.load(self.blinky_img[3])
                if self.num == 2:
                    self.image = pygame.image.load(self.pinky_img[3])
                if self.num == 3:
                    self.image = pygame.image.load(self.inkey_img[3])
                self.down_animate = True
                self.delay_down = 0
            if not self.stats.ghost_scared and self.delay_down == 75 and self.down_animate \
                    and not self.eaten:
                if self.num == 0:
                    self.image = pygame.image.load(self.clyde_img[7])
                if self.num == 1:
                    self.image = pygame.image.load(self.blinky_img[7])
                if self.num == 2:
                    self.image = pygame.image.load(self.pinky_img[7])
                if self.num == 3:
                    self.image = pygame.image.load(self.inkey_img[7])
                self.down_animate = False
                self.delay_down = 0
            else:
                self.delay_down += 1
            if self.eaten:
                self.image = pygame.image.load(self.eaten_img[3])
            
            self.rect.centery += self.settings.ghost_speed_factor
            self.count_down += 1
            if self.count_down == 13:
                self.array_y += 1
                self.count_down = 0

        if self.stats.ghost_scared and self.delay2 < 1600:
            if not self.scared_animate and self.delay == 50 and not self.eaten:
                self.image = pygame.image.load(self.scared_img[0])
                self.scared_animate = True
                self.delay = 0
            if self.scared_animate and self.delay == 50 and not self.eaten:
                if self.delay2 > 800:
                    self.image = pygame.image.load(self.scared_img[1])
                self.scared_animate = False
                self.delay = 0
            else:
                self.delay += 1
            self.delay2 += 1
        elif self.stats.ghost_scared and self.delay2 >= 1600:
            self.settings.ghost.play(-1)
            self.stats.ghost_scared = False
            self.eaten = False
            self.delay2 = 0
            self.delay_right, self.delay_left, self.delay_up, self.delay_down = 0, 0, 0, 0
            self.scared_animate, self.right_animate, self.left_animate = False, False, False
            self.up_animate, self.down_animate = False, False
