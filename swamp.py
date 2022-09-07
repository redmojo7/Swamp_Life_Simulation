#
# Author : 
# ID : 
#
# swamp.py - Class definitions for simulation of swamp life
#
# Revisions: 
#
# 01/09/2022 – Base version for assignment
#
import random

import numpy as np


class Creature(object):  #
    DEATH = "death"

    def __init__(self, pos, map):
        self.x = pos[0]
        self.y = pos[1]
        self.age = 0
        self.map = map

    # target is array [x,y]
    def move_to_target(self, target):
        # move for x
        print(f"Move to target ({target[0]},{target[1]})")
        if abs(self.x - target[0]) > self.velocity:  # farther than a velocity
            if (self.x - target[0]) > 0:
                x_moved = self.x - self.velocity
            else:
                x_moved = self.x + self.velocity
        else:
            x_moved = target[0]
        # move for y
        if abs(self.y - target[1]) > self.velocity:  # farther than a velocity
            if (self.y - target[1]) > 0:
                y_moved = self.y - self.velocity
            else:
                y_moved = self.y + self.velocity
        else:
            y_moved = target[1]
        # change position
        self.x = x_moved
        self.y = y_moved

    # random_run
    def random_run(self):
        print("Random running")
        x_moved = self.x + random.choice([-abs(self.velocity), 0, self.velocity])
        y_moved = self.y + random.choice([-abs(self.velocity), 0, self.velocity])
        if x_moved < 0: x_moved = 0
        if y_moved < 0: y_moved = 0
        # "ROW_MAX - self.get_size()" --- prevent living cross border at the first time
        if x_moved > self.map.height - self.get_size():
            x_moved = self.map.height - self.get_size()
        if y_moved >= self.map.width - self.get_size():
            y_moved = self.map.width - self.get_size()
        # change position
        self.x = x_moved
        self.y = y_moved

    def step_change(self):
        # before moving, check if there are some food around ** points (it depends on vision)
        food_cells = np.zeros((self.map.height, self.map.width), dtype=int)
        # put all foods into cells
        for x, y in self.map.foods:
            food_cells[x, y] = 1
        if self.map.foods:
            # to find the nearest one by calculating the Euclidean distance
            # https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_math_vector_and_reflection.md
            food = min([f for f in self.map.foods], key=lambda f: pow(f[0] - self.x, 2) + pow(f[1] - self.y, 2))
            # move forward to food
            # if np.sum(food_cells[self.x - 5:self.x + 6, self.y - 5:self.y + 6]) == 0:
            print(f"Food was found! @ ({food[0]},{food[1]})")
            if food[0] == self.x and food[1] == self.y:
                print(f"Eating food...@ {food[0]},{food[1]}")
                self.map.foods.remove(food)
            self.move_to_target(food)
        else:
            # there is no food, then random running
            self.random_run()


class Duck(Creature):
    TIME_2_HATCH = 4
    TIME_2_AGED = 15
    TIME_2_DEATH = 20
    EGG = "egg"
    ADULT = "adult"

    def __init__(self, pos, map):
        self.state = self.EGG
        self.velocity = 10  # velocity / speed of movement
        self.vision = 40  # can see food from max 40 points away
        super().__init__(pos, map)  # Call parent __init__

    def __str__(self):
        return f"{self.state} Duck aged {self.age} @ ({self.x},{self.y})"

    def step_change(self):
        self.age += 1
        if self.state == self.EGG and self.age >= self.TIME_2_HATCH:    # ready to HATCH
            self.state = self.ADULT
        else:
            if self.velocity == 10 and self.age >= self.TIME_2_AGED:    # old
                self.velocity = 5
            if self.age > self.TIME_2_DEATH:    # death
                self.state = self.DEATH
            else:                               # run if it doesn't die
                super().step_change()  # Call parent step_change


    def get_size(self):
        if self.state == "egg":
            size = 5
        else:
            size = 15
        return size


class Newt(Creature):
    TIME_2_DEATH = 20

    def __init__(self, pos, map):
        self.velocity = 5
        self.size = 10
        self.state = "Newt"
        self.vision = 30  # can see food from max 40 points away
        super().__init__(pos, map)  # Call parent __init__

    def __str__(self):
        return f"Newt aged {self.age} @ ({self.x},{self.y})"

    def step_change(self):
        self.age += 1
        if self.age > self.TIME_2_DEATH:    # death
            self.state = self.DEATH
        super().step_change()

    def get_size(self):
        return self.size