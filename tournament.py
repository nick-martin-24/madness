from datetime import datetime
from ftplib import FTP
import getpass
import os
import madftp
import requests
from team import Team
from participant import Participant


class Tournament:

    s = 'https://data.ncaa.com/casablanca/carmen/brackets/championships/basketball-men/d1/{}/data.json'
    json_source = s.format(2019)
    size = 12
    type = 'March Madness'

    def __init__(self):
        self.name = 'tournament'
        self.user = getpass.getuser()
        self.base_directory = '/Users/{}/personal/madness/{}'.format(self.user, datetime.now().year)
        self.ftp_directory = 'golfpools.net/{}/ocdebauchery/'.format(datetime.now().year)
        if not os.path.exists(self.base_directory):
            os.makedirs(self.base_directory)
            madftp.create_ftp_directory('golfpools.net/2020/')
            madftp.create_ftp_directory(self.ftp_directory)

        self.json = requests.get(self.json_source).json()
        self.group = []
        self.bracket_rounds = []
        self.teams = []
        self.team_names = []
        self.define_bracket_rounds()
        self.multiplier = {'First Four&#174;': 0,
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
        s += '{} Tournament\n'.format(self.type)
        s += 'Participants:\n'
        for participant in self.group:
            s += '{}\n'.format(participant.name)
        return s

    def upload_file_to_ftp(self, path, filename, destination):
        ftp = FTP(self.ftp_site, self.ftp_user, self.ftp_password)
        ftp.cwd(destination)
        file = open(path + filename, 'rb')
        ftp.storbinary('STOR ' + filename, file)
        file.close()
        ftp.quit()

    def create_ftp_directory(self, directory_name):
        ftp = FTP(self.ftp_site, self.ftp_user, self.ftp_password)
        ftp.mkd(directory_name)
        ftp.quit()

    def define_bracket_rounds(self):
        for game in self.json['games']:
            bracket_round = game['game']['bracketRound']
            if bracket_round not in self.bracket_rounds:
                self.bracket_rounds.append(bracket_round)

    def define_tournament_team_names(self):
        for game in self.json['games']:
            team1 = game['game']['away']['names']['short']
            team2 = game['game']['home']['names']['short']
            if team1 not in self.team_names:
                self.team_names.append(team1)
            if team2 not in self.team_names:
                self.team_names.append(team2)

    def get_team_by_name(self, name):
        for team in self.teams:
            if team.name == name:
                return team

    def create_and_process_teams(self):
        for game in self.json['games']:
            for team in ['home', 'away']:
                data = game['game'][team]
                name = data['names']['short']
                if name == '':
                    continue

                if game['game']['bracketRound'] == 'First Round' \
                        or game['game']['bracketRound'] == self.bracket_rounds[0]:
                    self.teams.append(Team(self, name, data))

                if game['game']['gameState'] == 'final':
                    t = self.get_team_by_name(name)
                    if data['winner']:
                        multiplier = self.multiplier[game['game']['bracketRound']]
                        t.add_to_total(multiplier)
                    else:
                        t.eliminate()

    def create_participants(self):
        self.group.append(Participant(self, 'Brad', ['Texas Tech', 'Kansas', 'VCU', 'Florida', 'Vermont']))
        self.group.append(Participant(self, 'Mark', ['Tennessee', 'Wisconsin', 'Baylor', 'Murray St.', 'Yale']))
        self.group.append(Participant(self, 'Chris', ['Gonzaga', 'Kansas St.', 'UCF', 'New Mexico St.', 'Northeastern']))
        self.group.append(Participant(self, 'Dan', ['Michigan St.', 'Maryland', 'Utah St.', 'Saint Mary\'s (CA)', 'Montana']))
        self.group.append(Participant(self, 'Ken', ['Purdue', 'Buffalo', 'Oklahoma', 'Arizona St.', 'Northern Ky.']))
        self.group.append(Participant(self, 'Nick the Younger', ['North Carolina', 'Villanova', 'Washington', 'Minnesota', 'Georgia St.']))
        self.group.append(Participant(self, 'Nick the Elder', ['Michigan', 'Iowa St.', 'Nevada', 'Oregon', 'Old Dominion']))
        self.group.append(Participant(self, 'Patrick', ['Virginia', 'Florida St.', 'Cincinnati', 'Seton Hall', 'Abilene Christian']))
        self.group.append(Participant(self, 'Paul', ['LSU', 'Mississippi St.', 'Ole Miss', 'Liberty', 'Bradley']))
        self.group.append(Participant(self, 'Robbie', ['Duke', 'Virginia Tech', 'Syracuse', 'Belmont', 'UC Irvine']))
        self.group.append(Participant(self, 'Stephen', ['Kentucky', 'Auburn', 'Louisville', 'Ohio St.', 'Saint Louis']))
        self.group.append(Participant(self, 'Zeke', ['Houston', 'Marquette', 'Wofford', 'Iowa', 'Colgate']))
