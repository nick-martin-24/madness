import os
import ftputils
from datetime import datetime as dt
from scrapeutils.ncaa import utils

output_directory = '/Users/{}/data/madness/{}/'.format(os.environ['USER'], dt.now().year)

def setup():
    os.makedirs(output_directory)
    ftputils.setup()

