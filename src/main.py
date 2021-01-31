import utils
import os
from scrapeutils.ncaa import utils as nsu

if __name__ == '__main__':
    if not os.path.exists(utils.output_directory):
        utils.setup()

    t = nsu.get_tournament()
    participants = 0
    for participant in participants:
        participant.total = utils.get_participant_total(participant['roster'],t)

