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

        try:
            self.sensor = MPR121.begin()
        except Exception as e:
            print e
            sys.exit(1)


        # this is the touch threshold - setting it low makes it more like a proximity trigger default value is 40 for touch
        touch_threshold = 40

        # this is the release threshold - must ALWAYS be smaller than the touch threshold default value is 20 for touch
        release_threshold = 20

        # set the thresholds
        self.sensor.set_touch_threshold(touch_threshold)
        self.sensor.set_release_threshold(release_threshold)



    def update(self):
        # TODO: add GPIO button for reload
        if self.sensor.touch_status_changed():
            self.sensor.update_touch_data()
            for i, key in enumerate(self.inputs):
                if i > len(self.states)-1:
                    print("change")
                    continue

                press = self.sensor.is_new_touch(i)
                play = self.play_sound[i]
                state = self.states[i]

                if press and i == 11:
                    self.pads = self._reload()
                    time.sleep(2)
                    print('file_reloaded')
                    continue

                # PICAP
                if press and not state and not play:
                    self.states[i] = True
                    self.play_sound[i] = True

                elif self.sensor.is_new_release(i):
                    self.states[i] = False

    @property
    def state(self):
        return self.states
