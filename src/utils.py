import os
import ftputils
from datetime import datetime as dt
from scrapeutils.ncaa import utils as nu

output_directory = '/Users/{}/data/madness/{}/'.format(os.environ['USER'], dt.now().year)

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
    games = nu.get_games_by_team(team)
    for game in games:
        if nu.won_game(team,game):
            total += round_values[game['game']['bracketRound']]
    return total

def get_participant_total(roster):
    total = 0
    for team in roster:
        total += get_team_total(team)
    return total

