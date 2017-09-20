import json
import os
import sys
from time import sleep, time

import pygame

import config
from inputter import ArrowKeyController
#from touch_input import TouchController
from config import Pad


def load_config(filename):
    print("loading config file...")
    config = {}
    with open(filename, 'r') as f:
        config = json.load(f)
    return config


def play_sound(channel, sound):
    pygame.mixer.Channel(channel).play(sound)


def load_pads_from_config(sample_path, config, config_id):
    pads = []
    for bank in config['configs'][config_id]['banks']:
        for i, pad in enumerate(bank['pads']):
            pad = Pad(bank, i)
            pad.load_samples(sample_path)
            pads.append(pad)
    return pads


def load_pads(base_path, config_file):
    # load the config
    #
    config = load_config(config_file)
    # deserialise the config into Pad objects
    pads = load_pads_from_config(base_path, config, 0)
    if pads == None:
        print("No pads loaded!")
        exit(0)

    return pads


def main():

    config_file = 'config_example.json'
    if len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]):
            config_file = sys.argv[1]

    pygame.mixer.pre_init(frequency = 44100, channels = 2, buffer = 2048)
    pygame.init()

    base_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'samples')
    pads = load_pads(config_file)

    # Wrap the config load so we can hopefully reload the config on the fly
    def _reload():
        print("reloading...")
        return load_pads(config_file)


    # This is demo specific
    controller = ArrowKeyController([105,108,106], pads, _reload)

    # Main loop
    #
    while True:
        current_time = pygame.time.get_ticks()
        # cycle through inputs
        # check if the pad has been touched
        #
        for i, _input in enumerate(controller.play_sound):
            try:
                pad = controller.pads[i]
            except IndexError:
                continue
            if _input:
                play_sound(i, pad.sample)
                controller.play_sound[i] = False
            pad.update()

        sleep(0.01)


if __name__ == '__main__':
    main()
