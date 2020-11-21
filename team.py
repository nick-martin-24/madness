from participant import Participant


class Team:

    def __init__(self, tournament, name, data):
        self.__name = name
        self.__tournament = tournament
        self.__total_points = 0
        self.__seed = int(data['seed'])
        self.__initial_max = self.__seed * sum(self.__tournament.get_multiplier().values())
        self.__current_max = self.__initial_max
        self.__status = 'active'

    def __str__(self):
        s = '{}: Total Points={}, Initial Max={}, Current Max={}'.format(self.__name, self.__total_points,
                                                                         self.__initial_max, self.__current_max)
        return s

    def get_name(self):
        return self.__name

    def get_seed(self):
        return self.__seed

    def get_initial_max(self):
        return self.__initial_max

    def get_current_max(self):
        return self.__current_max

    def get_total_points(self):
        return self.__total_points

    def add_to_total(self, points):
        self.__total_points += points

    def eliminate(self):
        self.__status = 'eliminated'
        self.__current_max = self.__total_points
