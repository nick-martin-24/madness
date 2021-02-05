import os
import ftputils
import pandas as pd
from datetime import datetime as dt
from scrapeutils.ncaa import utils as nsu

output_directory = '{}/data/madness/{}/'.format(os.environ['HOME'], dt.now().year)

round_values = {'First Four&#174;': 0,
                'First Round': 1,
                'Second Round': 2,
                'Sweet 16&#174;': 3,
                'Elite Eight&#174;': 4,
                'FINAL FOUR&#174;': 6,
                'Championship': 10}

def setup():
    os.makedirs(output_directory)
    ftputils.setup()

def get_team_total(team):
    total = 0
    games = nsu.get_games_by_team(team)
    for game in games:
        if nsu.won_game(team,game):
            total += round_values[game['game']['bracketRound']]
    return total

def calculate_participant_total(roster):
    total = 0
    for team in roster:
        total += get_team_total(team)
    return total

def calculate_team_points():
    team_points = {}
    for team in nsu.get_team_names():
        team_points[team] = get_team_total(team)
    return team_points

def load_teams(filename):
    return pd.read_csv(filename)

