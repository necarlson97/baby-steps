from itertools import combinations
import pygame as pg

from game_object import Wall
from player import Player
from gaurd import Gaurd
from level import Level, load_levels

class Game():

    bg = (170, 170, 170)

    dev = False

    def __init__(self, display):
        self.display = display
        self.levels = load_levels(self)
        self.set_level(0)        

    def set_level(self, index: int):
        self.level = self.levels[0]
        self.game_objects = self.level.game_objects
        self.cell_size = self.level.cell_size
        self.graph = self.level.graph

        self.walls = [o for o in self.game_objects if isinstance(o, Wall)]
        self.player = [o for o in self.game_objects if isinstance(o, Player)][0]
        self.gaurds = [o for o in self.game_objects if isinstance(o, Gaurd)]
        # # self.gaurds = [self.gaurds[0]] # # For debug

        self.input_objects = [self.player]
        self.update_objects = self.walls + self.gaurds + self.input_objects
        self.render_objects = self.update_objects


    def inputs(self, events):
        for e in [e for e in events if e.type == pg.KEYDOWN]:
            k = e.key
            if k == 49:
                self.dev = not self.dev

        for io in self.input_objects:
            io.inputs(events)

    def update(self):
        for o in self.update_objects:
            o.update()

        self.check_collsions()

    def check_collsions(self):

        def is_touching(o1, o2):
            return o1.r == o2.r and o1.c == o2.c
        
        collide_pairs = ((o1, o2) for o1, o2 in combinations(self.update_objects, 2)
                                  if is_touching(o1, o2))

        for o1, o2 in collide_pairs:
            o1.collide(o2)
            o2.collide(o1)


    def render(self, s):
        s.fill(self.bg)

        for o in self.render_objects:
            o.pre_render(s)
        for o in self.render_objects:
            o.render(s)
