import pygame
import random
from pygame.sprite import Group
from eventloop import EventLoop
from maze import Maze
from settings import Settings
from pacman import Pacman
from point import Point
from scoreboard import Scoreboard
from game_stats import GameStats
from startup import Startup
from high_scores import HighScores
from portal import Portal


class Game:
    """Runs the game"""

    def __init__(self):
        pygame.init()
        # declares all and sets classes, data, groups
        self.pac = Group()
        self.points = Group()
        self.pills = Group()
        self.fruits = Group()
        self.ghosts = Group()
        self.delay = 0
        self.count = 0
        self.timer = random.randint(3000, 5001)
        self.timer2 = 4500

        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Pacman Portal")

        self.point = Point(self.screen, self.settings)
        self.maze = Maze(self.screen, self.settings, self.pac, self.points, self.pills, self.fruits,
                         mazefile='images/maze.txt', brickfile='square')
        self.portal = Portal(self.screen, self.settings)
        self.pacman = Pacman(self.screen, self.settings, self.maze, self.portal)

        self.stats = GameStats(self.settings)
        self.sb = Scoreboard(self.settings, self.screen, self.stats, self.maze, self.portal)
        self.play_button = Startup(self.screen, self.settings, 'Play')
        self.score_button = HighScores(self.screen, "High Scores", self.settings)
        self.back_button = HighScores(self.screen, "Back (B)", self.settings)

    def __str__(self): return 'Game(Pacman Portal), maze=' + str(self.maze) + ')'

    def play(self):
        # Starts the game
        eloop = EventLoop(self.screen, self.settings, self.play_button, self.score_button, self.maze, self.stats,
                          self.sb, self.pacman, self.pac, self.ghosts, self.points, self.pills, self.fruits,
                          self.portal, finished=False)
        # loops while not finished
        while not eloop.finished:
            # Check events
            eloop.check_events()
            if self.stats.game_active:
                # spawns fruits at random times
                if self.delay == self.timer:
                    self.maze.create_fruit(self.stats.fruit_count)
                    if self.stats.fruit_count >= 3:
                        self.stats.fruit_count = 0
                    else:
                        self.stats.fruit_count += 1
                    self.delay = 0
                    self.timer = random.randint(3000, 5001)
                else:
                    self.delay += 1
                # deletes fruit after a period of time
                if self.count == self.timer2:
                    self.fruits.empty()
                    self.count = 0
                else:
                    self.count += 1

                # updates sprites
                self.pac.update()
                self.ghosts.update()
                self.portal.update()
                # Checks for collision
                eloop.check_collisions()
            self.update_screen()

    def update_screen(self):
        """Updates what is on the screen"""
        self.screen.fill(self.settings.bg_color)
        # displays statrup screen
        if not self.stats.game_active and not self.stats.score_screen_active:
            self.play_button.draw_button()
            self.score_button.draw_button()
        # displays score screen if score button is pressed
        if not self.stats.game_active and self.stats.score_screen_active:
            self.sb.draw_score_screen()
            self.back_button.draw_back()
        # Main game starts if active
        if self.stats.game_active:
            self.maze.blitme()
            self.pac.draw(self.screen)
            self.points.draw(self.screen)
            self.pills.draw(self.screen)
            self.fruits.draw(self.screen)
            self.ghosts.draw(self.screen)
            self.sb.show_score()
        pygame.display.flip()


game = Game()
game.play()
