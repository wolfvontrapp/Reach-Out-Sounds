import json
import os


class Pad(object):
    def __init__(self, config, name, bank, pad):
        self._bank_id = bank
        self._pad_id = pad
        self._pad = config['configs'][name]['banks'][bank]['pads'][pad]
        self.samples = self._pad['samples']
        self.sample_position = 0
        self.mode = self._pad['mode']
        self.timeout = self._pad['timeout']

    def reset_position():
        self.position = 0

    @property
    def sample(self):
        return self.samples[self.position]

    def __str__(self):
        return "Pad {}, {}, {}".format(self._pad_id, self.samples, self.mode)


if __name__ == '__main__':
    config = {}
    with open('config.json', 'r') as f:
        config = json.load(f)

    pad0 = Pad(config, 0, 0, 0)
    print(pad0)
