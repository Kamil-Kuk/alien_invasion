import json


class GameStats():
    """Tracking statistics for Alien Invasion"""

    def __init__(self, ai_settings):
        """Initialize statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()
        #Start Alien Invasion in an inactive state.
        self.game_active = False
        #High score should never be reset
        self.high_score = self.get_high_score()
        # Start Alien Invasion displays help menu
        self.help_active = False


    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def get_high_score(self):
        """Reads previous highscore from a file"""
        filename = 'highscore.json'
        try:
            with open(filename) as f_obj:
                high_score = json.load(f_obj)
            return high_score
        except FileNotFoundError:
            return 0

