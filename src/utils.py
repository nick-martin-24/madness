import os
import ftputils
from datetime import datetime as dt
from scrapeutils.ncaa import utils as ncaa_utils

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

def get_team_total(team,t=[]):
    total = 0
    if not t:
        t = ncaa_utils.get_tournament()
    games = ncaa_utils.get_games_by_team(team)
    for game in games:
        if ncaa_utils.won_game(team,game):
            total += round_values[game['game']['bracketRound']]
    return total

