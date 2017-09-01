import json
import os


def load_config(filename):
    config = {}
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config


if __name__ == '__main__':

    # load the config
    #
    config = load_config('config.json')

    # Main loop
    #
    while True:
        # cycle through inputs
        #
        for _input in range(inputs):
            if pad.state:
                play(pad.sample)
            pass
        pass
