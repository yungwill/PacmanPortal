import pygame.ftfont


class HighScores:

    def __init__(self, screen, highscr, settings):
        """Initializes the high scores button attributes"""
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()

        self.centerx = self.screen_rect.centerx
        # Set the dimensions and properties of the button
        self.width, self.height = 360, 50
        self.button_color = (255, 0, 255)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('snap itc', 48)

        # Build the button's rect obj and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.centerx, 630)

        # Defining
        self.highscr_image = None
        self.highscr_image_rect = None

        # The button message needs to be prepped only once
        self.prep_highscr(highscr)

    def prep_highscr(self, msg):
        """Turn msg into a rendered image and center the text on the button"""
        self.highscr_image = self.font.render(msg, True, self.text_color)
        self.highscr_image_rect = self.highscr_image.get_rect()
        self.highscr_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw a blank button and then draw the message
        self.screen.blit(self.highscr_image, (self.settings.screen_width/4, 600))

    def draw_back(self):
        # Draw a blank button and then draw the message to go back to main menu
        self.screen.blit(self.highscr_image, (self.settings.screen_width / 3, 600))
