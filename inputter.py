# keyboard input system
#
import pygame as pg


class ArrowKeyController(object):
    def __init__(self):
        self.inputs = [False for i in range(4)]
        self.keys = [
            pg.K_UP,
            pg.K_RIGHT,
            pg.K_DOWN,
            pg.K_LEFT,
        ]
        print(self.inputs, len(self.inputs))

    def update(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                if keys[pg.K_ESCAPE]:
                    exit()

                for i, key in enumerate(self.keys):
                    if keys[key] and self.inputs[i] != True:
                        self.inputs[i] = True
                    else:
                        self.inputs[i] = False
            elif event.type == pg.KEYUP:
                for i, key in enumerate(self.keys):
                    if self.inputs[i]:
                        self.inputs[i] = False

    @property
    def state(self):
        return self.inputs
