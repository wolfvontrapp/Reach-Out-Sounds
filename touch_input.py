# keyboard input system
#
import pygame as pg


class TouchController(object):
    def __init__(self):
        self.inputs = [23, 18]
        self.states = [False for i in range(self.inputs)]

    def update(self):
        for event in events:
            for i, key in enumerate(self.inputs):
                if GPIO.input(key):
                    if inputs[key] and self.states[i] != True:
                        self.states[i] = True
                    else:
                        self.states[i] = False

    @property
    def state(self):
        return self.states
