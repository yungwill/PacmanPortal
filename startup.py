import pygame.ftfont


class Startup:

    def __init__(self, screen, settings, msg):
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()
        self.centerx = self.screen_rect.centerx

        self.delay = 0
        self.delay2 = 0
        self.move = 0

        self.image = pygame.image.load('images/Pac-Man_Title.png')
        self.image = pygame.transform.scale(self.image, (500, 150))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx

        self.clyde = pygame.image.load('images/clyde_right1.bmp')
        self.pinky = pygame.image.load('images/pinky_right1.bmp')
        self.blinky = pygame.image.load('images/blinky_right1.bmp')
        self.inkey = pygame.image.load('images/inkey_right1.bmp')

        self.scared_ghost = pygame.image.load('images/scared_ghost.png')

        self.img = {0: 'images/Pacman.bmp',
                    1: 'images/Pacman2.bmp'}
        self.pacman = pygame.image.load(self.img[0])
        self.base_pacman = pygame.image.load(self.img[0])
        self.animate = False
        self.move_left = False

        self.pill = pygame.image.load('images/power_pill.png')
        self.pill = pygame.transform.scale(self.pill, (15, 15))

        self.width, self.height = 160, 70
        self.button_color = (255, 0, 255)
        self.text_color = (255, 255, 255)

        # Colors
        self.white = (255, 255, 255)
        self.red = (239, 24, 32)
        self.yellow = (255, 189, 66)
        self.blue = (0, 255, 223)
        self.pink = (254, 189, 221)

        # Fonts
        self.font = pygame.font.SysFont('snap itc', 48)
        self.font2 = pygame.font.SysFont('snap itc', 30)

        # Build the button's rect obj and center it
        self.rect2 = pygame.Rect(0, 0, self.width, self.height)
        self.rect2.center = (self.centerx, 530)

        self.intro1 = self.font2.render('"BLINKY"', False, self.red)
        self.intro2 = self.font2.render('"PINKY"', False, self.pink)
        self.intro3 = self.font2.render('"CLYDE"', False, self.yellow)
        self.intro4 = self.font2.render('"INKEY"', False, self.blue)

        # Defining
        self.msg_image = None
        self.msg_image_rect = None

        # The button message needs to be prepped only once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center the text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.msg_image, (self.screen_rect.centerx - 50, 500))

        if self.delay < 1100:
            self.screen.blit(self.blinky, (-50 + self.move, 340))
            self.screen.blit(self.pinky, (-85 + self.move, 340))
            self.screen.blit(self.clyde, (-120 + self.move, 340))
            self.screen.blit(self.inkey, (-155 + self.move, 340))
        else:
            self.screen.blit(self.scared_ghost, (-50 + self.move, 340))
            self.screen.blit(self.scared_ghost, (-85 + self.move, 340))
            self.screen.blit(self.scared_ghost, (-120 + self.move, 340))
            self.screen.blit(self.scared_ghost, (-155 + self.move, 340))

        if self.delay < 1100:
            self.screen.blit(self.pill, (self.settings.screen_width/1.1, 350))
        self.screen.blit(self.pacman, (self.move, 340))
        if self.move <= 540 and not self.move_left:
            self.move += .5
        if self.move >= 540:
            self.move_left = True
        if self.move >= -40 and self.move_left:
            self.move -= .5

        if not self.animate and self.delay2 == 50 and not self.move_left:
            self.pacman = pygame.image.load(self.img[0])
            self.animate = True
            self.delay2 = 0
        if not self.animate and self.delay2 == 50 and self.move_left:
            self.pacman = pygame.transform.flip(self.base_pacman, True, False)
            self.animate = True
            self.delay2 = 0
        if self.animate and self.delay2 == 50:
            self.pacman = pygame.image.load(self.img[1])
            self.animate = False
            self.delay2 = 0
        self.delay2 += 1

        if self.delay >= 2400:
            self.screen.blit(self.blinky, (self.settings.screen_width / 2.7, 250))
            self.screen.blit(self.intro1, (self.settings.screen_width / 2.3, 250))

        if self.delay >= 2600:
            self.screen.blit(self.pinky, (self.settings.screen_width / 2.7, 300))
            self.screen.blit(self.intro2, (self.settings.screen_width / 2.3, 300))

        if self.delay >= 2800:
            self.screen.blit(self.clyde, (self.settings.screen_width / 2.7, 350))
            self.screen.blit(self.intro3, (self.settings.screen_width / 2.3, 350))

        if self.delay >= 3000:
            self.screen.blit(self.inkey, (self.settings.screen_width / 2.7, 400))
            self.screen.blit(self.intro4, (self.settings.screen_width / 2.3, 400))

        if self.delay >= 3400:
            self.delay = 0
            self.move_left = False

        self.delay += 1
