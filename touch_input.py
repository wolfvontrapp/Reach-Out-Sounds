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
            if GPIO.input(key) == 0 and self.states[i] == False:
                self.states[i] = True
                print(self.states[i])
            else:
                self.states[i] = False

    @property
    def state(self):
        return self.states
