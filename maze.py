import pygame
from imagerect import ImageRect
from point import Point
from powerpill import PowerPill
from fruit import Fruit


class Maze:
    """Implements Maze"""
    RED = (255, 0, 0)
    BRICK_SIZE = 13
    
    def __init__(self, screen, settings, pac, points, pills, fruits, mazefile, brickfile):
        self.screen = screen
        self.pac = pac
        self.points = points
        self.pills = pills
        self.fruits = fruits
        self.settings = settings

        self.point = Point(self.screen, self.settings)
        self.pill = PowerPill(self.screen, self.settings)
        self.fruit = Fruit(self.screen, self.settings)
        self.filename = mazefile
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

        self.bricks = []
        sz = Maze.BRICK_SIZE
        self.brick = ImageRect(screen, brickfile, sz, sz)
        self.deltax = self.deltay = Maze.BRICK_SIZE
        
    def __str__(self): return 'maze(' + self.filename + ')'

    # Obtain the location of where the maze is and stores them in a list
    def build(self):
        b = self.brick.rect
        b_w, b_h = b.width, b.height
        dx, dy = self.deltax, self.deltay
        
        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'X':
                    self.bricks.append(pygame.Rect(ncol*dx, nrow*dy, b_w, b_h))

    # Obtain the location of where the points and pills are is and stores them in a list
    def build_points(self):
        dx, dy = self.deltax, self.deltay

        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'P':
                    Maze.create_pill(self, ncol*dx, nrow*dy)
                if col == '-':
                    Maze.create_point(self, ncol*dx + 5, nrow*dy + 5)

    # draws maze
    def blitme(self):
        for rect in self.bricks:
            self.screen.blit(self.brick.image, rect)

    # ceates and stores points, pills and fuirts in their respective groups
    def create_point(self, x, y):
        self.point = Point(self.screen, self.settings)
        self.point.rect.x = x
        self.point.rect.y = y
        self.points.add(self.point)

    def create_pill(self, x, y):
        self.pill = PowerPill(self.screen, self.settings)
        self.pill.rect.x = x
        self.pill.rect.y = y
        self.pills.add(self.pill)

    def create_fruit(self, fruit_count):
        self.fruit = Fruit(self.screen, self.settings)
        self.fruit.which_fruit(fruit_count)
        self.fruits.add(self.fruit)
