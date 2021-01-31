import utils
import os

if __name__ == '__main__':
    if not os.path.exists(utils.output_directory):
        utils.setup()
