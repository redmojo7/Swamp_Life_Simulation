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
from swamp import Duck, Shrimp, Newt
from tools import is_inside, get_edge_points


def remove_creatures(creatures, position):
    x = position[0]
    y = position[1]
    return list(filter(lambda n: n.x != x and n.y != y, creatures))


class Map:
    # list of Duck, Newt, and Shrimps
    ducks_list = []
    newts_list = []
    shrimps_list = []

    # foods, etc. is a list of each food position, like [[1,2],[1,3]]
    foods = []
    mountains_borders = []

    # foods, etc. is a numpy array, value 1 means that entity exist here
    food_cells = None

    def __init__(self, width=500, height=500, land_height=166):
        # width:y:col,  height:x:row
        # by default, map are 500*500
        self.land_height = land_height
        self.width = width
        self.height = height
        self.food_cells = np.zeros((height, width), dtype=int)
        self.mountains_cells = np.zeros((height, width), dtype=int)
        self.lands_cells = np.zeros((height, width), dtype=int)

    def __str__(self):
        return f"Map {self.width}*{self.height} with {len(self.livings)} livings and {len(self.foods)} foods."

    def add_food(self, positions):
        self.foods = positions
        # put all foods into cells
        for x, y in positions:
            self.food_cells[y, x] = 1

    def eat_food(self, position):
        print(f"Eating food...@ {position[0]},{position[1]}")
        self.foods.remove(position)
        self.food_cells[position[1], position[0]] = 0

    def set_mountains(self, x1, y1, x2, y2, x3, y3):
        x_min = min(x1, x2, x3)
        x_max = max(x1, x2, x3)
        y_min = min(y1, y2, y3)
        y_max = max(y1, y2, y3)
        for row in range(y_min, y_max):
            for col in range(x_min, x_max):
                if is_inside(x1, y1, x2, y2, x3, y3, col, row):
                    self.mountains_cells[row, col] = 1
        # get all points of border of all mountains (join two list by '+')
        self.mountains_borders += get_edge_points(x1, y1, x2, y2, x3, y3)

    def set_lands(self):
        for row in range(self.land_height):
            for col in range(self.width):
                self.lands_cells[row, col] = 1

    def add_creatures(self, creatures):
        for c in creatures:
            if isinstance(c, Duck):
                self.ducks_list.append(c)
            elif isinstance(c, Newt):
                self.newts_list.append(c)
            elif isinstance(c, Shrimp):
                self.shrimps_list.append(c)

    def remove_newt(self, position):
        self.newts_list = remove_creatures(self.newts_list, position)

    def remove_shrimps(self, position):
        self.shrimps_list = remove_creatures(self.shrimps_list, position)

    def remove_foods(self, position):
        self.foods.remove(position)
        # self.food_cells[row, col] = 0
        self.food_cells[position[1], position[0]] = 0

    def get_ducks_pos(self):
        pos_list = []
        [pos_list.append([duck.x, duck.y]) for duck in self.ducks_list]
        return pos_list

    def get_newts_pos(self):
        pos_list = []
        [pos_list.append([newt.x, newt.y]) for newt in self.newts_list]
        return pos_list

    def get_shrimps_pos(self):
        pos_list = []
        [pos_list.append([shrimp.x, shrimp.y]) for shrimp in self.shrimps_list]
        return pos_list

    def get_foods_pos(self):
        return self.foods

    def get_ducks_cells(self):
        ducks_cells = np.zeros((self.height, self.width), dtype=int)
        for duck in self.ducks_list:
            ducks_cells[duck.y, duck.x] = 1
        return ducks_cells

    def get_newts_cells(self):
        newts_cells = np.zeros((self.height, self.width), dtype=int)
        for newt in self.newts_list:
            newts_cells[newt.y, newt.x] = 1
        return newts_cells

    def get_shrimps_cells(self):
        shrimps_cells = np.zeros((self.height, self.width), dtype=int)
        for shrimp in self.shrimps_list:
            shrimps_cells[shrimp.y, shrimp.x] = 1
        return shrimps_cells
