from pvp.pvp import *

class Player:
    def __init__(self, game, name, cue_ball_pos, window_game):
        self.name = name
        self.game = game  # Reference to the game
        self.cue_ball = self.create_cue_ball(cue_ball_pos)
        self.ball_color = None  # Initialize ball color as None

    def create_cue_ball(self, pos):
        cue_ball = self.game.create_ball(38/2 , pos)
        return cue_ball

    # Method to set the ball color based on the first potted ball
    def set_ball_color(self, color):
        self.ball_color = color
        print(f"{self.name} registered ball color: {self.ball_color}")
    def increase_score(self, points):
        self.score += points

    def get_score(self):
        return self.score