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

    def __init__(self, width=500, height=500):
        # by default, map are 500*500
        self.width = width
        self.height = height
        self.food_cells = np.zeros((height, width), dtype=int)

    def __str__(self):
        return f"Map {self.width}*{self.height} with {len(self.livings)} livings and {len(self.foods)} foods."

    def add_food(self, foods):
        self.foods = foods
        # put all foods into cells
        for x, y in foods:
            self.food_cells[x, y] = 1

    def eat_food(self, food):
        print(f"Eating food...@ {food[0]},{food[1]}")
        self.foods.remove(food)
        self.food_cells[food[0], food[1]] = 0
'''
    def add_livings(self, livings):
        self.livings = livings
'''
