# keyboard input system
#
import pygame as pg


class ArrowKeyController(object):
    def __init__(self):
        self.states = [False for i in range(4)]
        self.inputs = [
            pg.K_UP,
            pg.K_RIGHT,
            pg.K_DOWN,
            pg.K_LEFT,
        ]

    def update(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                inputs = pg.key.get_pressed()
                if inputs[pg.K_ESCAPE]:
                    exit()

                for i, key in enumerate(self.inputs):
                    if inputs[key] and self.states[i] != True:
                        self.states[i] = True
                    else:
                        self.states[i] = False
            elif event.type == pg.KEYUP:
                for i, key in enumerate(self.inputs):
                    if self.states[i]:
                        self.states[i] = False

    @property
    def state(self):
        return self.states
