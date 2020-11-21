

class Participant:

    def __init__(self, tournament, name, teams):
        self.__tournament = tournament
        self.__name = name
        self.__html = self.__name
        self.__team_names = teams
        self.__teams = []
        self.__initial_max = 0
        self.__current_max = 0
        self.__total = 0
        self.set_teams()
        self.set_initial_max()
        self.set_current_max()

    def __str__(self):
        s = '{}: Total Points={}, Initial Max={}, Current Max={}'.format(self.__name, self.__total,
                                                                         self.__initial_max, self.__current_max)
        return s

    def get_name(self):
        return self.__name

    def get_team_names(self):
        return self.__team_names

    def get_teams(self):
        return self.__teams

    def set_teams(self):
        for team in self.__team_names:
            self.__teams.append(self.__tournament.get_team_by_name(team))

    def get_initial_max(self):
        return self.__initial_max

    def set_initial_max(self):
        print(self.get_name())
        for team in self.__teams:
            print(team.get_name())
            self.__initial_max += team.get_initial_max()

    def get_current_max(self):
        return self.__current_max

    def set_current_max(self):
        for team in self.__teams:
            self.__current_max += team.get_current_max()

    def get_total(self):
        return self.__total

    def set_total(self):
        for team in self.__teams:
            self.__total += team.get_total_points()
