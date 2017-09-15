# keyboard input system
#
import pygame as pg
import RPi.GPIO as GPIO

class TouchController(object):
    def __init__(self, inputs):
        if not inputs:
            exit()
        self.inputs = inputs

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
                print("button down", i, self.states[i])

            elif not press:
                self.states[i] = False

    @property
    def state(self):
        return self.states


