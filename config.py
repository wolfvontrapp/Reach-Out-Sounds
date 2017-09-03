import json
import os

import pygame


class Pad(object):
    def __init__(self, bank, pad_id):
        self._bank = bank
        self._pad_id = pad_id
        self._pad = bank['pads'][pad_id]
        self.sample_files = self._pad['samples']
        self.samples = []
        self.sample_position = 0
        self.mode = self._pad['mode']
        self.timeout = self._pad['timeout']
        self._lasttime = 0

    def load_samples(self, base_path):
        for f in self._pad['samples']:
            wav = os.path.join(base_path, self._bank['name'], f+'.wav')
            if os.path.exists(wav):
                self.samples.append(pygame.mixer.Sound(wav))
            else:
                print("File {} does not exist".format(wav))
                exit(0)

    def reset_position():
        self.position = 0

    @property
    def sample(self):
        if self.mode == 'cycle':
            if self.sample_position == len(self.samples)-1:
                self.sample_position = 0
            else:
                self.sample_position += 1
        elif self.mode == 'random':
            self.sample_position = random.randint(len(self.samples)-1)
        return self.samples[self.sample_position]

    def update(self, dt=0.0):
        """
        Handle timeouts and other timed events
        """
        if (dt - self.timeout) > self.timeout:
            self.position = 0

    def __str__(self):
        return "Bank [{}] Pad {}, {}, {}".format(
                self._bank['name'], self._pad_id, self.samples, self.mode)


if __name__ == '__main__':
    config = {}
    with open('config.json', 'r') as f:
        config = json.load(f)

    for bank in config['configs'][0]['banks']:
        for i, pad in enumerate(bank['pads']):
            pad = Pad(bank, i)
            print(pad)
