# keyboard input system
#
import pygame as pg
import RPi.GPIO as GPIO

class TouchController(object):
    def __init__(self):
        self.inputs = [14]
        self.states = [False for i in self.inputs]

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for pin in self.inputs:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def update(self):
        for i, key in enumerate(self.inputs):
            if GPIO.input(key):
                if inputs[key] and self.states[i] != True:
                    self.states[i] = True
                else:
                    self.states[i] = False
            print(self.states[i])

    @property
    def state(self):
        return self.states
