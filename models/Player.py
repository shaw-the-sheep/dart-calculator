from models.utils import calculate_total_score


class Player:
    def __init__(self, name, score, status):
        self.name = name
        self.score = score
        self.playing = status
        self.history = []
        self.legs_won = 0
        self.sets_won = 0
        self.in_option_checked = False

    def start_turn(self):
        self.playing = True

    def end_playing(self):
        self.playing = False

    def is_busted(self, shots:list):
        total = calculate_total_score(shots)
        new_score = self.score - total
        if new_score < 0:
            return True
        return False

    def validate_shots(self, shots: list):
        total = calculate_total_score(shots)
        new_score = self.score - total
        if new_score < 0:
            return "Busted"
        self.history += shots
        self.score -= total
        return ""

    def __str__(self):
        print(self.name)