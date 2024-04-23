class Player:
    def __init__(self, name, cue_ball, window_game, ball_color):
        self.name = name
        self.score = 0
        self.position1 = (cue_ball.body.position[0] - cue_ball.radius,
                          cue_ball.body.position[1] - cue_ball.radius)
        self.position2 = (window_game.get_width() // 2, 140)
        self.ball_color = ball_color  # new attribute
        self.cue = cue_ball