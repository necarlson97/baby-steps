import pygame as pg

import utils
from game_object import GameObject

class Player(GameObject):

    color = (0, 0, 100)

    key_functs = {
        # wasd
        119: 'up',
        115: 'down',
        100: 'right',
        97: 'left',
        
        # arrows
        273: 'up',
        274: 'down',
        275: 'right',
        276: 'left',

        # 304: 'run', # shift
        # 310: 'slow', # cmd
    }

    up, down, left, right = [False]*4

    def inputs(self, events):
        self.dr, self.dc = 0, 0
        for e in [e for e in events if e.type == pg.KEYDOWN]:
            func_name = self.key_functs.get(e.key)
            if func_name is not None:
                func = getattr(self, func_name)
                func()


    def update(self):
        super().update()

    def up(self): self.dr -= 1
    def down(self): self.dr += 1
    def left(self): self.dc -= 1
    def right(self): self.dc += 1

