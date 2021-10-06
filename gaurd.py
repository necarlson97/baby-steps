import pygame as pg

import utils
from game_object import GameObject
from player import Player

class Gaurd(GameObject):

    color = (0, 100 , 50)
    deathtouch_classes = [Player]
    path = []
    slow = True

    alive = True

    # List of points to move directly to, no
    # intellegence for pathfining here
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        

    def update(self):
        self.left, self.right, self.up, self.down = [False]*4

        if self.alive:
            # If I am going somewhere
            if self.path != []:
                den_r, den_c = self.path[0]
                if self.r < den_r:
                    self.down = True
                elif self.r > den_r:
                    self.up = True
                if self.c < den_c:
                    self.right = True
                elif self.c > den_c:
                    self.left = True

                # If we arrived at the destination
                if not any([self.left, self.right, self.up, self.down]):
                    self.path.pop(0)
            # If I have arrived, make up a new place to go
            else:
                rand_dest = self.game.graph.rand_cell()
                self.path = self.game.graph.path_to(self.r, self.c, *rand_dest)

        super().update()

    def collide(self, o):
        # Gaurds walk through gaurds
        if isinstance(o, Gaurd):
            return
        if isinstance(o, Player):
            self.kill()

        super().collide(o)

    def kill(self):
        self.path = []
        self.alive = False
        self.color = (100, 0, 0)

    def render(self, s):
        super().render(s)

        if self.game.dev:
            cs = self.game.cell_size

            path_link = (r, c)
            pg.draw.circle(s, (0, 0, 0), path_link, 5)
            for d in self.path:
                x, y = utils.pos_to_pixels(*path_link, cs)
                pg.draw.line(s, (50, 50, 50), path_link, (x, y))
                path_link = d
            pg.draw.circle(s, (100, 100, 100), path_link, 5)

