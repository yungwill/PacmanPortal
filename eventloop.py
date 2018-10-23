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

        self.display = 0
        self.image = None

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
            self.sb.prep_level()
            self.sb.prep_pacmen()

            self.pac.empty()
            self.points.empty()
            self.pills.empty()
            self.fruits.empty()
            self.ghosts.empty()

            self.maze.build()
            self.maze.build_points()
            self.pacman = Pacman(self.screen, self.settings, self.maze, self.portal, self.stats)
            self.pac.add(self.pacman)
            EventLoop.create_ghosts(self)

    def check_high_scores(self, mouse_x, mouse_y):
        """Checks if the score button has been pressed and takes user to high score screen"""
        score_clicked = self.high_scores.rect.collidepoint(mouse_x, mouse_y)
        if score_clicked and not self.stats.game_active:
            self.stats.score_screen_active = True

    def check_collisions(self):
        """Checks if there are any collisions and what happens because of the collisions"""
        self.collisions = pygame.sprite.groupcollide(self.pac, self.points, False, True)
        self.collisions2 = pygame.sprite.groupcollide(self.pac, self.pills, False, True)
        self.collisions3 = pygame.sprite.groupcollide(self.pac, self.fruits, False, True)
        self.collisions4 = pygame.sprite.groupcollide(self.pac, self.ghosts, False, False)

        if self.collisions:
            self.settings.eat.play()
            self.stats.score += 10
            self.sb.prep_score()

        if self.collisions2:
            self.settings.ghost.stop()
            self.settings.eat_pill.play()
            self.settings.scared_ghost.play()
            self.stats.score += 50
            self.stats.ghost_scared = True
            self.sb.prep_score()

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

        if self.collisions4 and not self.stats.ghost_scared:
            self.settings.death.play()
            EventLoop.update_pacman_death(self)

            if self.stats.pacmen_left > 0:
                self.stats.pacmen_left -= 1
                self.pac.empty()
                self.fruits.empty()
                self.ghosts.empty()
                self.sb.prep_pacmen()
                self.pacman = Pacman(self.screen, self.settings, self.maze, self.portal, self.stats)
                self.pac.add(self.pacman)
                EventLoop.create_ghosts(self)

            else:
                self.sb.check_high_score()
                self.pac.empty()
                self.fruits.empty()
                self.ghosts.empty()
                self.points.empty()
                self.pills.empty()
                self.sb.prep_pacmen()
                self.stats.pacman_dead = False
                self.stats.game_active = False
                pygame.mixer.stop()
                pygame.mouse.set_visible(True)

        if self.collisions4 and self.stats.ghost_scared:
            for ghosts in self.collisions4.values():
                for ghost in ghosts:
                    self.stats.score += 200
                    self.sb.prep_score()
                    ghost.eaten = True
                    EventLoop.draw_ghost_points(self, ghost.rect.x, ghost.rect.y)
            self.settings.eat_ghost.play()

        if len(self.points) == 0 and len(self.pills) == 0:
            # Increase level when all points are eaten
            self.pac.empty()
            self.fruits.empty()
            self.pacman = Pacman(self.screen, self.settings, self.maze, self.portal, self.stats)
            self.stats.level += 1
            self.sb.prep_level()
            self.pac.add(self.pacman)
            self.maze.build_points()

    def update_pacman_death(self):
        """Updates what is on the screen"""
        self.stats.pacman_dead = True
        while self.stats.pacman_dead:
            self.pac.update()
            if self.stats.pacman_dead:
                self.screen.fill(self.settings.bg_color)
                # displays statrup screen
                # Main game starts if active
                self.maze.blitme()
                self.pac.draw(self.screen)
                self.points.draw(self.screen)
                self.pills.draw(self.screen)
                self.fruits.draw(self.screen)
                self.ghosts.draw(self.screen)
                self.sb.show_score()
                pygame.display.flip()

    def draw_ghost_points(self, x, y):
        self.stats.ghost_points = True
        self.image = pygame.image.load('images/200pt.bmp')
        while self.stats.ghost_points:
            self.screen.fill(self.settings.bg_color)
            # displays statrup screen
            # Main game starts if active
            self.maze.blitme()
            self.pac.draw(self.screen)
            self.points.draw(self.screen)
            self.pills.draw(self.screen)
            self.fruits.draw(self.screen)
            self.ghosts.draw(self.screen)
            self.screen.blit(self.image, (x, y - 30))
            self.sb.show_score()
            if self.display < 1000:
                self.display = 0
                self.stats.ghost_points = False
            else:
                self.display += 1
            pygame.display.flip()

    def create_ghosts(self):
        self.ghost = Ghost(self.screen, self.settings, self.maze, self.stats, 0)
        self.ghosts.add(self.ghost)
        self.ghost = Ghost(self.screen, self.settings, self.maze, self.stats, 1)
        self.ghosts.add(self.ghost)
        self.ghost = Ghost(self.screen, self.settings, self.maze, self.stats, 2)
        self.ghosts.add(self.ghost)
        self.ghost = Ghost(self.screen, self.settings, self.maze, self.stats, 3)
        self.ghosts.add(self.ghost)
