# keyboard input system
#
import sys
sys.path.append('..')
import keyboard


K_LEFT = 105
K_DOWN = 108
K_RIGHT = 106


class ArrowKeyController(object):
    def __init__(self, inputs):
        self.inputs = inputs
        self.states = [False for i in self.inputs]
        self.play_sound = [False for i in self.inputs]

        keyboard.hook(self.update)

    def update(self, e):
        for i, key in enumerate(self.inputs):
            if i > len(self.states)-1:
                continue
            press = e.scan_code == key
            play = self.play_sound[i]
            state = self.states[i]

            if press and not state and not play and e.event_type == 'down':
                self.states[i] = True
                self.play_sound[i] = True
                #print("button down", i, self.states[i])

            elif e.event_type == 'up' and press:
                self.states[i] = False


    def update2(self, e):
        if e.event_type == 'down':
            for i, key in enumerate(self.inputs):
                if i > len(self.states)-1:
                    continue
                if key == e.scan_code and self.states[i] != True:
                    self.states[i] = True
                else:
                    self.states[i] = False
        elif e.event_type == 'up':
            for i, key in enumerate(self.inputs):
                if i > len(self.states)-1:
                    continue
                if self.states[i]:
                    self.states[i] = False

    @property
    def state(self):
        return self.states
