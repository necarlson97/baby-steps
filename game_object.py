import pygame as pg
import random as rand
import utils

class GameObject():

    color = (255, 0, 0)
    # Current row and column
    r, c = 0, 0
    # Change in row / col
    dr, dc = 0, 0

    # Whether or not this blocks paths
    blocking = False

    def __init__(self, game, r=0, c=0):
        self.game = game
        self.r, self.c = r, c

    def update(self):
        self.move()

    def move(self):
        self.r += self.dr
        self.c += self.dc

    def collide(self, o):
        # collided with object 'o', which probibly has a rect and such

        # Move back one step
        self.r -= self.dr
        self.c -= self.dc

    def pre_render(self, s):
        pass

    def render(self, s):
        cs = self.game.cell_size
        x, y = utils.pos_to_pixels(self.r, self.c, cs)

        draw_rect = (x, y, cs, cs)
        if not self.blocking: # Little less imposing size
            shave_off = cs / 10
            draw_rect = (x+shave_off, y+shave_off, cs-shave_off*2, cs-shave_off*2)
        pg.draw.rect(s, self.color, draw_rect)

class Wall(GameObject):
    
    color = (50, 50 , 50)
    blocking = True

    def collide(self, o):
        pass
