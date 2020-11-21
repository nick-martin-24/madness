

class Participant:

    def __init__(self, tournament, name, teams):
        self.tournament = tournament
        self.name = name
        self.html = self.name
        self.team_names = teams
        self.teams = []
        self.initial_max = 0
        self.current_max = 0
        self.total = 0
        self.set_teams()
        self.set_initial_max()
        self.set_current_max()
        self.set_total()
        print(self)

    def __str__(self):
        s = '{}: Total Points={}, Initial Max={}, Current Max={}'.format(self.name, self.total,
                                                                         self.initial_max, self.current_max)
        return s

    def set_teams(self):
        for team in self.team_names:
            self.teams.append(self.tournament.get_team_by_name(team))

    def set_initial_max(self):
        print(self.name)
        for team in self.teams:
            print(team.name)
            self.initial_max += team.initial_max

    def set_current_max(self):
        for team in self.teams:
            self.current_max += team.current_max

    def set_total(self):
        for team in self.teams:
            print(team)
            self.total += team.total_points
