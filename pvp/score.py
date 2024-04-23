class Score:
    def __init__(self):
        self.score = 0

    def count_score(self, points):
        self.score += points

    def get_score(self):
        return self.score