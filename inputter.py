# keyboard input system
#
import time
import sys
sys.path.append('..')
import keyboard
import MPR121

K_LEFT = 105
K_DOWN = 108
K_RIGHT = 106
SPACE = 57

class ArrowKeyController(object):
    def __init__(self, inputs, pads, _reload=lambda x: x):
        self.inputs = inputs
        self.states = [False for i in self.inputs]
        self.play_sound = [False for i in self.inputs]
        self.pads = pads
        self._reload = _reload
        keyboard.hook(self.update)

    def update(self, e):
        if e.event_type == 'down' and e.scan_code == SPACE:
            self.pads = self._reload()
            time.sleep(2)
            print('file_reloaded')

        for i, key in enumerate(self.inputs):
            if i > len(self.states)-1:
                continue
            press = e.scan_code == key
            play = self.play_sound[i]
            state = self.states[i]

            if press and not state and not play and e.event_type == 'down':
                self.states[i] = True
                self.play_sound[i] = True

            elif e.event_type == 'up' and press:
                self.states[i] = False

    @property
    def state(self):
        return self.states


class PiCapController(object):
    def __init__(self, inputs, pads, _reload=lambda x: x):
        self.inputs = inputs
        self.states = [False for i in self.inputs]
        self.play_sound = [False for i in self.inputs]
        self.pads = pads
        self._reload = _reload
        keyboard.hook(self.update)

        try:
            self.sensor = MPR121.begin()
        except Exception as e:
            print e
            sys.exit(1)


    def update(self, e):
        # TODO: add GPIO button for reload
        if false:
            self.pads = self._reload()
            time.sleep(2)
            print('file_reloaded')

        if self.sensor.touch_status_changed():
            for i, key in enumerate(self.inputs):
                if i > len(self.states)-1:
                    continue

                press = self.sensor.is_new_touch(i)
                play = self.play_sound[i]
                state = self.states[i]

                # PICAP
                if press and not state and not play and e.event_type == 'down':
                    self.states[i] = True
                    self.play_sound[i] = True

                elif e.event_type == 'up' and press:
                    self.states[i] = False

    @property
    def state(self):
        return self.states
