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

        with open('high_score.txt', 'r') as f:
            self.high_score = f.readlines()

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
        self.prep_level()
        self.prep_pacmen()

    def check_high_score(self):
        """Check to see if there's a new high score"""
        if self.stats.score > int(self.high_score[0]):
            self.high_score[0] = str(self.stats.score)
            with open('high_score.txt', 'w') as file:
                file.writelines(self.high_score)

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
            pacman = Pacman(self.screen, self.settings, self.maze, self.portal, self.stats)
            pacman.rect.x = 10 + pacmen_number * pacman.rect.width
            pacman.rect.y = self.screen_rect.bottom - 70
            self.pacmen.add(pacman)

    def show_score(self):
        """Draw scores and ships to the screen when game is active"""
        if self.stats.game_active:
            self.screen.blit(self.score_image, self.score_rect)
            self.screen.blit(self.level_image, self.level_rect)
            # Draw pacmen
            self.pacmen.draw(self.screen)

    def draw_score_screen(self):
        """Draws the high scores screen"""
        if self.stats.score_screen_active:

            self.score_image = self.font.render(str(self.stats.count + 1) + '. ' + self.high_score[0],
                                                True, self.white, self.black)
            self.screen.blit(self.score_image, (self.settings.screen_width / 2.5, self.stats.height))
