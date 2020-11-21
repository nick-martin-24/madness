from participant import Participant


class Team:

    def __init__(self, tournament, name, data):
        self.name = name
        self.tournament = tournament
        self.total_points = 0
        self.seed = int(data['seed'])
        self.initial_max = self.seed * sum(self.tournament.multiplier.values())
        self.current_max = self.initial_max
        self.status = 'active'

    def __str__(self):
        s = '{}: Total Points={}, Initial Max={}, Current Max={}'.format(self.name, self.total_points,
                                                                         self.initial_max, self.current_max)
        return s

    def add_to_total(self, multiplier):
        self.total_points += multiplier * self.seed

    def eliminate(self):
        self.status = 'eliminated'
        self.current_max = self.total_points
