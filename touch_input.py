# keyboard input system
#
import pygame as pg
import RPi.GPIO as GPIO

class TouchController(object):
    def __init__(self):
        self.inputs = [14]

        self.states = [False for i in self.inputs]
        self.play_sound = [False for i in self.inputs]

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for pin in self.inputs:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def update(self):
        for i, key in enumerate(self.inputs):
            press = not bool(GPIO.input(key))
            play = self.play_sound[i]
            state = self.states[i]

            if press and not state and not play:
                self.states[i] = True
                self.play_sound[i] = True

            elif not press:
                self.states[i] = False

            print("button down", self.states[i])

    @property
    def state(self):
        return self.states


