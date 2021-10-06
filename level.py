import os
import random as rand
import pygame as pg

from game_object import GameObject, Wall
from player import Player
from gaurd import Gaurd

class Level():

    char_mapping = {
        'x': Gaurd, # Target
        'o': Gaurd,
        'p': Player,
        '#': Wall
    }

    cell_size = 10

    def __init__(self, game, lvl_str_lines):
        self.game = game
        self.lvl_str_lines = lvl_str_lines
        self.game_objects = self.create_objects(self.lvl_str_lines)
        self.graph = self.create_graph()

    def create_objects(self, lvl_str_lines):
        objs = []

        r, c = 0, 0
        for line in lvl_str_lines:
            c = 0
            for ch in line:
                if ch in self.char_mapping:
                    Klass = self.char_mapping[ch]
                    new = Klass(self.game, r, c)
                    objs.append(new)
                c += 1
            r += 1

        # Set max row and column
        self.row_count = r
        self.col_count = c
        return objs

    def create_graph(self):
        w, h = self.game.display.screen_res
        col_size =  w // self.col_count
        row_size = h // self.row_count
        self.cell_size = col_size if col_size < row_size else row_size
        graph = Graph(w, h, self.cell_size)
        
        for o in self.game_objects:
            graph.place(o)

        return graph


class Graph():
    # A searchable node graph that allows ai navigation

    def __init__(self, width, height, cell_size):
        # width and hight, and cell_size screen pixels
        self.cell_size = cell_size
        self.row_count = height // cell_size
        self.col_count = width // cell_size
        # GameObjet matrix
        self.matrix = [[None]*self.col_count for i in range(self.row_count)]

    def place(self, o: GameObject):
        # set that object as starting in this cell
        self.matrix[o.r][o.c] = o

    def path_to(self, from_r, from_c, to_r, to_c):
        # returns a list of coordinates that is an path
        # right now breadth first, could do a*
        start = (from_r, from_c)
        end = (to_r, to_c)
        front = [start]
        path_dict = {start: None} # mapping of nodes to where they came from

        while not front == []:
            # Get an unexplored node from the front
            curr = front.pop(0)

            # Found goal, exit
            if curr[0] == end[0] and curr[1] == end[1]:
                break

            # Get unexplored neighbors
            neighbors = [n for n in self.get_neighbors(*curr)
                         if not n in path_dict]
            for nei in neighbors:
                front.append(nei)
                path_dict[nei] = curr

        # Reconstruct cell_path from dict
        cell_path = []
        while curr in path_dict:
            cell_path.append(curr)
            curr = path_dict[curr]

        return cell_path

    def get_neighbors(self, r, c):
        # up, down, left, right
        points = ((r-1, c),
                  (r, c-1),
                  (r+1, c),
                  (r, c+1))
        # only return points in bounds, and not blocked
        points = [(r, c) for r, c in points
                  if c > 0 and c < self.col_count
                  and r > 0 and r < self.row_count
                  and self.matrix[r][c] is not None
                  and not self.matrix[r][c].blocking]
        return points


    def rand_cell(self):
        rx = int(rand.uniform(0, self.col_count))
        ry = int(rand.uniform(0, self.row_count))
        return rx, ry


def load_levels(game):
    lvl_dir = 'levels'

    lvls = []
    for file in os.listdir(lvl_dir):
        if file.endswith('.txt'):
            file_name = os.path.join(lvl_dir, file)
            with open(file_name) as f:
                lvl_lines= f.readlines()
                lvls.append(Level(game, lvl_lines))

    lvls
    return lvls