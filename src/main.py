import utils
import os
from scrapeutils.ncaa import utils as nsu

if __name__ == '__main__':
    if not os.path.exists(utils.output_directory):
        utils.setup()

    t = nsu.get_tournament()
    filename = '{}/data/madness/test.csv'.format(os.environ['HOME'])
    mad_data = utils.load_teams(filename)
    participants = {}
    for participant in mad_data.columns:
        participants[participant] = utils.calculate_participant_total(mad_data[participant].values)

