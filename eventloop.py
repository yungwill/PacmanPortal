import pygame
import sys
from pacman import Pacman
from ghost import Ghost


class EventLoop:
    def __init__(self, screen, settings, play, high_scores, maze, stats, sb,
                 pacman, pac, ghosts, points, pills, fruits, portal, finished):
        self.finished = finished
        self.screen = screen
        self.settings = settings
        self.play = play
        self.high_scores = high_scores
        self.maze = maze
        self.stats = stats
        self.sb = sb
        self.pacman = pacman
        self.pac = pac
        self.ghost = None
        self.ghosts = ghosts
        self.points = points
        self.pills = pills
        self.fruits = fruits
        self.portal = portal

        self.collisions = False
        self.collisions2 = False
        self.collisions3 = False
        self.collisions4 = False

    def __str__(self):
        return 'eventloop, finished =' + str(self.finished) + ')'

    def check_keydown_events(self, event):
        """Checks for keys being pressed"""
        if event.key == pygame.K_RIGHT:
            self.pacman.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.pacman.moving_left = True
        elif event.key == pygame.K_UP:
            self.pacman.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.pacman.moving_down = True
        elif event.key == pygame.K_b:
            self.stats.score_screen_active = False
        elif event.key == pygame.K_q:
            self.portal.orange_portal = True
        elif event.key == pygame.K_e:
            self.portal.blue_portal = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()

    def check_keyup_events(self, event):
        """Checks for keys being released"""
        if event.key == pygame.K_RIGHT:
            self.pacman.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.pacman.moving_left = False
        elif event.key == pygame.K_UP:
            self.pacman.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.pacman.moving_down = False

    def check_events(self):
        """Checks for any events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                EventLoop.check_keydown_events(self, event)
            elif event.type == pygame.KEYUP:
                EventLoop.check_keyup_events(self, event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                EventLoop.check_play(self, mouse_x, mouse_y)
                EventLoop.check_high_scores(self, mouse_x, mouse_y)

    def check_play(self, mouse_x, mouse_y):
        """Checks if play button is pressed"""
        button_clicked = self.play.rect2.collidepoint(mouse_x, mouse_y)
        if button_clicked and not self.stats.game_active:
            self.settings.music.play()
            pygame.mouse.set_visible(False)
            # Reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            # Reset the scoreboard image
            self.sb.prep_score()
            self.sb.prep_high_score()
            self.sb.prep_level()
            self.sb.prep_pacmen()

            self.pac.empty()
            self.points.empty()
            self.pills.empty()
            self.fruits.empty()
            self.ghosts.empty()

            self.maze.build()
            self.maze.build_points()
            self.pacman = Pacman(self.screen, self.settings, self.maze, self.portal)
            self.pac.add(self.pacman)
            self.ghost = Ghost(self.screen, self.settings, self.maze)
            self.ghosts.add(self.ghost)

    def check_high_scores(self, mouse_x, mouse_y):
        """Checks if the score button has been pressed and takes user to high score screen"""
        score_clicked = self.high_scores.rect.collidepoint(mouse_x, mouse_y)
        if score_clicked and not self.stats.game_active:
            self.stats.score_screen_active = True

    def check_high_score(self):
        """Check to see if there's a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.sb.prep_high_score()

    def check_collisions(self):
        """Checks if there are any collisions and what happens because of the collisions"""
        self.collisions = pygame.sprite.groupcollide(self.pac, self.points, False, True)
        self.collisions2 = pygame.sprite.groupcollide(self.pac, self.pills, False, True)
        self.collisions3 = pygame.sprite.groupcollide(self.pac, self.fruits, False, True)
        self.collisions4 = pygame.sprite.groupcollide(self.pac, self.ghosts, True, False)

        if self.collisions:
            self.settings.eat.play()
            self.stats.score += 10
            self.sb.prep_score()
            EventLoop.check_high_score(self)

        if self.collisions2:
            self.settings.eat_pill.play()
            self.settings.scared_ghost.play()
            self.stats.score += 50
            for ghost in self.ghosts:
                ghost.scared = True
            self.sb.prep_score()
            EventLoop.check_high_score(self)

        if self.collisions3:
            self.settings.eat_fruit.play()
            if self.stats.fruit_count == 1:
                self.stats.score += 1000
                self.sb.prep_score()
            if self.stats.fruit_count == 2:
                self.stats.score += 100
                self.sb.prep_score()
            if self.stats.fruit_count == 3:
                self.stats.score += 5000
                self.sb.prep_score()
            if self.stats.fruit_count == 0:
                self.stats.score += 200
                self.sb.prep_score()

        if self.collisions4:
            self.settings.death.play()
            if self.stats.pacmen_left > 0:
                self.stats.pacmen_left -= 1

                for pacman in self.pac:
                    pacman.dead = True
                    pacman.able_move = False

                self.pac.empty()
                self.fruits.empty()
                self.ghosts.empty()
                self.sb.prep_pacmen()

                self.pacman = Pacman(self.screen, self.settings, self.maze, self.portal)
                self.pac.add(self.pacman)
                self.ghost = Ghost(self.screen, self.settings, self.maze)
                self.ghosts.add(self.ghost)
            else:
                self.pac.empty()
                self.fruits.empty()
                self.ghosts.empty()
                self.points.empty()
                self.pills.empty()
                self.sb.prep_pacmen()
                self.stats.game_active = False
                pygame.mouse.set_visible(True)
            EventLoop.check_high_score(self)

        if len(self.points) == 0 and len(self.pills) == 0:
            # Increase level when all points are eaten
            self.pac.empty()
            self.fruits.empty()
            self.pacman = Pacman(self.screen, self.settings, self.maze, self.portal)
            self.stats.level += 1
            self.sb.prep_level()
            self.pac.add(self.pacman)
            self.maze.build_points()
