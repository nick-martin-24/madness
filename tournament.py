from datetime import datetime
from ftplib import FTP
import getpass
import os
import requests
from team import Team
from participant import Participant


class Tournament:

    __ftp_user = '2096943'
    __ftp_password = 'Bonner10!'
    __ftp_site = 'golfpools.net'
    s = 'https://data.ncaa.com/casablanca/carmen/brackets/championships/basketball-men/d1/{}/data.json'
    __json_source = s.format(2019)
    __size = 12
    __type = 'March Madness'

    def __init__(self):
        self.__name = 'tournament'
        self.__user = getpass.getuser()
        self.__base_directory = '/Users/{}/personal/madness/{}'.format(self.__user, datetime.now().year)
        self.__ftp_directory = '{}/{}/ocdebauchery/'.format(self.__ftp_site, datetime.now().year)
        if not os.path.exists(self.__base_directory):
            os.makedirs(self.__base_directory)
            self.create_ftp_directory('golfpools.net/2020/')
            self.create_ftp_directory(self.__ftp_directory)

        self.__json = requests.get(self.__json_source).json()
        self.__group = []
        self.__bracket_rounds = []
        self.__teams = []
        self.__team_names = []
        self.define_bracket_rounds()
        self.__multiplier = {'First Four&#174;': 0,
                             'First Round': 1,
                             'Second Round': 2,
                             'Sweet 16&#174;': 3,
                             'Elite Eight&#174;': 4,
                             'FINAL FOUR&#174;': 6,
                             'Championship': 10}
        self.create_and_process_teams()
        self.create_participants()

    def __str__(self):
        s = ''
        s += '{} Tournament\n'.format(self.__type)
        s += 'Participants:\n'
        for participant in self.get_group():
            s += '{}\n'.format(participant.get_name())
        return s

    def get_bracket_rounds(self):
        return self.__bracket_rounds

    def get_team_names(self):
        return self.__team_names

    def get_multiplier(self):
        return self.__multiplier

    def get_teams(self):
        return self.__teams

    def get_group(self):
        return self.__group

    def upload_file_to_ftp(self, path, filename, destination):
        ftp = FTP(self.__ftp_site, self.__ftp_user, self.__ftp_password)
        ftp.cwd(destination)
        file = open(path + filename, 'rb')
        ftp.storbinary('STOR ' + filename, file)
        file.close()
        ftp.quit()

    def create_ftp_directory(self, directory_name):
        ftp = FTP(self.__ftp_site, self.__ftp_user, self.__ftp_password)
        ftp.mkd(directory_name)
        ftp.quit()

    def define_bracket_rounds(self):
        for game in self.__json['games']:
            bracket_round = game['game']['bracketRound']
            if bracket_round not in self.__bracket_rounds:
                self.__bracket_rounds.append(bracket_round)

    def define_tournament_team_names(self):
        for game in self.__json['games']:
            team1 = game['game']['away']['names']['short']
            team2 = game['game']['home']['names']['short']
            if team1 not in self.__team_names:
                self.__team_names.append(team1)
            if team2 not in self.__team_names:
                self.__team_names.append(team2)

    def get_team_by_name(self, name):
        for team in self.__teams:
            if team.get_name() == name:
                return team

    def create_and_process_teams(self):
        for game in self.__json['games']:
            for team in ['home', 'away']:
                data = game['game'][team]
                name = data['names']['short']
                if name == '':
                    continue

                if game['game']['bracketRound'] == 'First Round' \
                        or game['game']['bracketRound'] == self.__bracket_rounds[0]:
                    self.__teams.append(Team(self, name, data))

                if game['game']['gameState'] == 'final':
                    t = self.get_team_by_name(name)
                    if data['winner']:
                        multiplier = self.__multiplier[game['game']['bracketRound']]
                        t.add_to_total(multiplier)
                    else:
                        t.eliminate()

    def create_participants(self):
        self.__group.append(Participant(self, 'Brad', ['Texas Tech', 'Kansas', 'VCU', 'Florida', 'Vermont']))
        self.__group.append(Participant(self, 'Mark', ['Tennessee', 'Wisconsin', 'Baylor', 'Murray St.', 'Yale']))
        self.__group.append(Participant(self, 'Chris', ['Gonzaga', 'Kansas St.', 'UCF', 'New Mexico St.', 'Northeastern']))
        self.__group.append(Participant(self, 'Dan', ['Michigan St.', 'Maryland', 'Utah St.', 'Saint Mary\'s (CA)', 'Montana']))
        self.__group.append(Participant(self, 'Ken', ['Purdue', 'Buffalo', 'Oklahoma', 'Arizona St.', 'Northern Ky.']))
        self.__group.append(Participant(self, 'Nick the Younger', ['North Carolina', 'Villanova', 'Washington', 'Minnesota', 'Georgia St.']))
        self.__group.append(Participant(self, 'Nick the Elder', ['Michigan', 'Iowa St.', 'Nevada', 'Oregon', 'Old Dominion']))
        self.__group.append(Participant(self, 'Patrick', ['Virginia', 'Florida St.', 'Cincinnati', 'Seton Hall', 'Abilene Christian']))
        self.__group.append(Participant(self, 'Paul', ['LSU', 'Mississippi St.', 'Ole Miss', 'Liberty', 'Bradley']))
        self.__group.append(Participant(self, 'Robbie', ['Duke', 'Virginia Tech', 'Syracuse', 'Belmont', 'UC Irvine']))
        self.__group.append(Participant(self, 'Stephen', ['Kentucky', 'Auburn', 'Louisville', 'Ohio St.', 'Saint Louis']))
        self.__group.append(Participant(self, 'Zeke', ['Houston', 'Marquette', 'Wofford', 'Iowa', 'Colgate']))
