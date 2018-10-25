import pygame


class Settings:
    """A class to store all settings for Pacman"""

    def __init__(self):
        """Initializes the game's static settings"""

        self.screen_width = 600
        self.screen_height = 740
        # Sets background color
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.pacmen_limit = 3

        self.pacman_speed_factor = 1
        self.ghost_speed_factor = 1

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        self.play_once = False

        self.music = pygame.mixer.Sound('sounds/pacman_beginning.wav')
        self.death = pygame.mixer.Sound('sounds/pacman_death.wav')
        self.eat_fruit = pygame.mixer.Sound('sounds/pacman_eatfruit.wav')
        self.eat_ghost = pygame.mixer.Sound('sounds/pacman_eatghost.wav')
        self.eat_pill = pygame.mixer.Sound('sounds/eat_pill.wav')
        self.eat = pygame.mixer.Sound('sounds/eat.wav')
        self.scared_ghost = pygame.mixer.Sound('sounds/scared_ghost.wav')
        self.ghost = pygame.mixer.Sound('sounds/ghost.wav')

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.pacman_speed_factor *= self.speedup_scale
        self.ghost_speed_factor *= self.speedup_scale
