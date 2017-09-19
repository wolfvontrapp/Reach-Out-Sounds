import json
import os
from time import sleep, time

import pygame

import config
from inputter import ArrowKeyController
#from touch_input import TouchController
from config import Pad

def load_config(filename):
    config = {}
    with open('config.json', 'r') as f:
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

def load():
    pass


def main():
    pygame.mixer.pre_init(frequency = 44100, channels = 2, buffer = 1024)
    pygame.init()

    # This is demo specific
    controller = ArrowKeyController([105,108,106])
    #controller = TouchController([14, 15])

    # load the config
    #
    config = load_config('config.json')
    # deserialise the config into Pad objects
    pads = load_pads_from_config('/mnt/ef6394f1-9c8d-4e75-96cd-b17480a3ab2d/downloads/projects/Reach-out-sounds', config, 0)
    if pads == None:
        print("No pads loaded!")
        exit(0)

    # Main loop
    #
    while True:
        current_time = pygame.time.get_ticks()
        # cycle through inputs
        # check if the pad has been touched
        #
        for i, _input in enumerate(controller.play_sound):
            try:
                pad = pads[i]
            except IndexError:
                continue
            if _input:
                play_sound(i, pad.sample)
                controller.play_sound[i] = False
            pad.update()

        sleep(0.01)


if __name__ == '__main__':
    main()
