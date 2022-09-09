#
# Author : Peng CAI
# ID : 21053409
#
# map.py - Class definitions for map
#
# Revisions:
#
# no
#
import numpy as np


class Map:
    livings = []
    foods = []
    food_cells = []
    terrain = []
    terrain_cells = []

    def __init__(self, width=500, height=500):
        # by default, map are 500*500
        self.width = width
        self.height = height
        self.food_cells = np.zeros((height, width), dtype=int)
        self.terrain_cells = np.zeros((height, width), dtype=int)

    def __str__(self):
        return f"Map {self.width}*{self.height} with {len(self.livings)} livings and {len(self.foods)} foods."

    def add_food(self, positions):
        self.foods = positions
        # put all foods into cells
        for x, y in positions:
            self.food_cells[x, y] = 1

    def eat_food(self, position):
        print(f"Eating food...@ {position[0]},{position[1]}")
        self.foods.remove(position)
        self.food_cells[position[0], position[1]] = 0

    def set_terrain(self, positions):
        self.terrain = positions
        # put all altitude into cells
        for x, y in positions:
            self.terrain_cells[x, y] = 1

'''
    def add_livings(self, livings):
        self.livings = livings
'''
