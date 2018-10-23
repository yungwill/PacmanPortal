class GameStats:
    """tracks statistics for Alien Invasion"""

    def __init__(self, settings):
        """Initialize statistics"""
        self.settings = settings
        self.reset_stats()
        self.game_active = False
        self.score_screen_active = False
        # Start game in an inactive flags
        self.ghost_scared = False
        self.ghost_points = False

        # Flag for if pacman is hit
        self.pacman_hit = False
        self.pacman_dead = False
        self.index = 0

        self.score = 0

        self.pacmen_left = self.settings.pacmen_limit
        self.level = 1

        self.fruit_count = 0
        self.count = 0
        self.height = 100

    def reset_stats(self):
        """Initializes statistics that can change during the game"""
        self.pacmen_left = self.settings.pacmen_limit
        self.score = 0
        self.level = 1
