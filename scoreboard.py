import pygame.ftfont
from pygame.sprite import Group
from pacman import Pacman


class Scoreboard:
    """A class to report sccring info"""

    def __init__(self, settings, screen, stats, maze, portal):
        """Initializes score keeping attributes"""
        self.screen = screen
        self.maze = maze
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.portal = portal

        self.count = 0

        # Font settings for scoring info
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        self.score_image = None
        self.score_rect = None
        self.high_score_image = None
        self.high_score_rect = None
        self.level_image = None
        self.level_rect = None
        self.pacmen = None

        # Prepare the initial score images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_pacmen()

    def prep_score(self):
        """Turn the score into a rendered image"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.settings.bg_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = self.screen_rect.bottom - 35

    def prep_high_score(self):
        """Turn the high score into a rendered image"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color,
                                                 self.settings.bg_color)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image"""
        self.level_image = self.font.render(str(self.stats.level), True,
                                            self.text_color, self.settings.bg_color)

        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.screen_rect.bottom - 70

    def prep_pacmen(self):
        """Shows how many ships are left"""
        self.pacmen = Group()
        for pacmen_number in range(self.stats.pacmen_left):
            pacman = Pacman(self.screen, self.settings, self.maze, self.portal)
            pacman.rect.x = 10 + pacmen_number * pacman.rect.width
            pacman.rect.y = self.screen_rect.bottom - 70
            self.pacmen.add(pacman)

    def show_score(self):
        """Draw scores and ships to the screen when game is active"""
        if self.stats.game_active:
            self.screen.blit(self.score_image, self.score_rect)
            self.screen.blit(self.high_score_image, self.high_score_rect)
            self.screen.blit(self.level_image, self.level_rect)
            # Draw pacmen
            self.pacmen.draw(self.screen)

    def draw_score_screen(self):
        """Draws the high scores screen"""
        if self.stats.score_screen_active:
            while self.stats.count <= 9:
                self.score_image = self.font.render(str(self.stats.count + 1) + ". -----",
                                                    True, self.white, self.black)
                self.screen.blit(self.score_image, (self.settings.screen_width / 2.5, self.stats.height))
                self.stats.count += 1
                self.stats.height += 50
            self.stats.count = 0
            self.stats.height = 100
