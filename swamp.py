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

from tools import manhattan_distance


class Creature(object):  #
    DEATH = "death"

    def __init__(self, pos, map):
        self.velocity = None
        self.vision = None
        self.x = pos[0]
        self.y = pos[1]
        self.age = 0
        self.map = map

    # target is array [x,y]
    def move_to_target(self, target):
        print(f"Move to target ({target[0]},{target[1]})")
        if self.under_one_step(target):
            # move to target directly
            self.x = target[0]
            self.y = target[1]
            return
        if self.x == target[0]:
            # move on y
            print("move on y")
            self.move_to_target_y(target)
        elif self.y == target[1]:
            # move on y
            print("move on x")
            self.move_to_target_x(target)
        else:
            print("move on x or y")
            if random.random() > 0.5:
                self.move_to_target_x(target)
            else:
                self.move_to_target_y(target)

    def move_to_target_y(self, target):
        if abs(self.y - target[1]) > self.velocity:  # farther than a velocity
            if (self.y - target[1]) > 0:
                y_moved = self.y - self.velocity
            else:
                y_moved = self.y + self.velocity
        else:
            y_moved = target[1]
        # change position for y
        self.y = y_moved

    def move_to_target_x(self, target):
        if abs(self.x - target[0]) > self.velocity:  # farther than a velocity
            if (self.x - target[0]) > 0:
                x_moved = self.x - self.velocity
            else:
                x_moved = self.x + self.velocity
        else:
            x_moved = target[0]
        # change position for x
        self.x = x_moved

    def random_run_x(self):
        x_moved = self.x + random.choice([-abs(self.velocity), 0, self.velocity])
        if x_moved < 0:
            x_moved = 0
        # "height - self.get_size()" --- prevent living cross border at the first time
        if x_moved > self.map.height - self.get_size():
            x_moved = self.map.height - self.get_size()
        # change position for x
        self.x = x_moved

    def random_run_y(self):
        y_moved = self.y + random.choice([-abs(self.velocity), 0, self.velocity])
        if y_moved < 0:
            y_moved = 0
        # "width - self.get_size()" --- prevent living cross border at the first time
        if y_moved >= self.map.width - self.get_size():
            y_moved = self.map.width - self.get_size()
        # change position for y
        self.y = y_moved

    # random run
    def random_run(self):
        if random.random() < 0.5:
            print("Random running on x")
            self.random_run_x()
        else:
            self.random_run_y()
            print("Random running on y")

    def step_change(self):
        # before moving, check if there are some food around ** points (it depends on vision)
        if self.map.foods and self.search_target(self.map.food_cells):
            # to find the nearest one by calculating the Euclidean distance
            # https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_math_vector_and_reflection.md
            food = min([f for f in self.map.foods], key=lambda f: pow(f[0] - self.x, 2) + pow(f[1] - self.y, 2))
            # move forward to food
            print(f"Food was found! @ ({food[0]},{food[1]})")
            if food[0] == self.x and food[1] == self.y:
                self.map.eat_food(food)
                self.age -= 3
            else:
                self.move_to_target(food)
        else:
            # there is no food, then random running
            self.random_run()

    def saw_alive_newts(self):
        return self.map.get_newts_pos() and self.search_target(self.map.get_newts_cells())

    def is_same_position(self, position):
        return position[0] == self.x and position[1] == self.y

    # if target was found, return true
    # target is a numpy array
    def search_target(self, target):
        return np.sum(target[self.x - self.vision:self.x + self.vision + 1,
                      self.y - self.vision:self.y + self.vision + 1]) != 0

    # to find the nearest one by calculating the Euclidean distance
    # https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_math_vector_and_reflection.md
    # target is a position[x,y] list
    # return the nearest position [x,y]
    def search_nearst_target(self, target_positions):
        return min([t for t in target_positions], key=lambda t: pow(t[0] - self.x, 2) + pow(t[1] - self.y, 2))


class Duck(Creature):
    TIME_2_HATCH = 4
    TIME_2_LAY_EGG = 10
    TIME_2_AGED = 15
    TIME_2_DEATH = 50
    EGG = "egg"
    ADULT = "adult"

    def __init__(self, pos, map):
        super().__init__(pos, map)  # Call parent __init__
        self.egg = None
        self.state = self.EGG
        self.velocity = 10  # velocity / speed of movement
        self.vision = 50  # can see food from max 40 points away

    def __str__(self):
        return f"{self.state} Duck aged {self.age} @ ({self.x},{self.y})"

    def step_change(self):
        # change age, state, velocity, ect...
        self.change_status()
        if self.state == self.ADULT:
            # before moving, check if there are some food around ** points (it depends on vision)
            if self.saw_alive_newts():
                position = self.search_nearst_target(self.map.get_newts_pos())
                # move forward to food
                print(f"Newt was found! @ ({position[0]},{position[1]})")
                # if distance under a velocity?
                if self.under_one_step(position):
                    # move to target and eat it
                    self.x = position[0]
                    self.y = position[1]
                    self.eat_newt(position)
                    self.age -= 3  # live longer
                else:
                    self.move_to_target(position)
            else:
                super().random_run()  # Call parent step_change

    def change_status(self):
        self.age += 1
        if self.state == self.EGG and self.age >= self.TIME_2_HATCH:  # ready to HATCH
            self.state = self.ADULT
        elif self.state == self.ADULT:
            if self.velocity == 10 and self.age >= self.TIME_2_AGED:  # old
                self.velocity = 5
            if self.age >= self.TIME_2_LAY_EGG and random.random() < 0.03:  # 10% chance to lay eggs
                self.egg = [self.x, self.y]
            if self.age > self.TIME_2_DEATH:  # death
                self.state = self.DEATH

    def get_size(self):
        if self.state == "egg":
            size = 10
        else:
            size = 20
        return size

    # eat a newt
    def eat_newt(self, position):
        print(f"{self.__str__()} is eating newts...")
        self.map.remove_newt(position)

    def under_one_step(self, position):
        return manhattan_distance([self.x, self.y], position) <= self.velocity


class Newt(Creature):
    TIME_2_DEATH = 50

    def __init__(self, pos, map):
        super().__init__(pos, map)  # Call parent __init__
        self.velocity = 3
        self.size = 10
        self.state = "Newt"
        self.vision = 30  # can see food from max 40 points away

    def __str__(self):
        return f"Newt aged {self.age} @ ({self.x},{self.y})"

    def step_change(self):
        self.age += 1
        if self.age > self.TIME_2_DEATH:  # death
            self.state = self.DEATH
        super().step_change()

    def get_size(self):
        return self.size
