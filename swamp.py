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

    def __init__(self, pos):
        self.velocity = None
        self.vision = None
        self.x = pos[0]
        self.y = pos[1]
        self.age = 0

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
        self.x += random.choice([-abs(self.velocity), 0, self.velocity])

    def random_run_y(self):
        self.y += random.choice([-abs(self.velocity), 0, self.velocity])

    # random run
    def random_run(self):
        if random.random() < 0.5:
            print("Random running on x")
            self.random_run_x()
        else:
            self.random_run_y()
            print("Random running on y")

    def step_change(self, my_map):
        # before moving, check if there are some food around ** points (it depends on vision)
        if my_map.foods and self.search_target(my_map.food_cells):
            # to find the nearest one by calculating the Euclidean distance
            # https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_math_vector_and_reflection.md
            food = min([f for f in my_map.foods], key=lambda f: pow(f[0] - self.x, 2) + pow(f[1] - self.y, 2))
            # move forward to food
            print(f"Food was found! @ ({food[0]},{food[1]})")
            if food[0] == self.x and food[1] == self.y:
                my_map.eat_food(food)
                self.age -= 3
            else:
                self.move_to_target(food)
        else:
            # if there is no food around, then random running
            self.random_run()

    def is_same_position(self, position):
        return position[0] == self.x and position[1] == self.y

    # if target was found, return true
    # target is a numpy array
    def search_target(self, target):
        return np.sum(target[self.x - self.vision:self.x + self.vision + 1,
                      self.y - self.vision:self.y + self.vision + 1]) != 0

    # to find the nearest one by calculating the Manhattan distance
    # target is a position[x,y] list
    # return the nearest position [x,y]
    def search_nearst_target(self, target_positions):
        target_pos = list(filter(lambda p: manhattan_distance(p, [self.x, self.y]) < self.vision, target_positions))
        if target_pos:
            return min([t for t in target_pos], key=lambda p: manhattan_distance(p, [self.x, self.y]))
        else:
            return None

    def under_one_step(self, position):
        return manhattan_distance([self.x, self.y], position) <= self.velocity

    # eat a newt
    def eat_newt(self, my_map, newt_pos):
        print(f"{self} is eating newts @ {newt_pos}")
        my_map.remove_newt(newt_pos)

    # eat a shrimp
    def eat_shrimp(self, my_map, shrimp_pos):
        print(f"{self} is eating shrimp @ {shrimp_pos}")
        my_map.remove_shrimps(shrimp_pos)

    # eat a food
    def eat_food(self, my_map, food_pos):
        print(f"{self} is eating food @ {food_pos}")
        my_map.remove_foods(food_pos)

    def track_newts(self, my_map, newt_pos):
        # move forward to newts
        print(f"Newt was found! @ ({newt_pos}) by {self}")
        # if the distance is under a velocity?
        if self.under_one_step(newt_pos):
            # move to target and eat it
            self.x = newt_pos[0]
            self.y = newt_pos[1]
            self.eat_newt(my_map, newt_pos)
            self.time_2_death += 15  # live longer
        else:
            self.move_to_target(newt_pos)

    def track_shrimp(self, my_map, shrimp_pos):
        # move forward to newts
        print(f"Shrimp was found! @ ({shrimp_pos}) by {self}")
        # if the distance is under a velocity?
        if self.under_one_step(shrimp_pos):
            # move to target and eat it
            self.x = shrimp_pos[0]
            self.y = shrimp_pos[1]
            self.eat_shrimp(my_map, shrimp_pos)
            self.time_2_death += 10  # live longer
        else:
            self.move_to_target(shrimp_pos)

    def track_food(self, my_map, food_pos):
        # move forward to newts
        print(f"Food was found! @ ({food_pos}) by {self}")
        # if the distance is under a velocity?
        if self.under_one_step(food_pos):
            # move to target and eat it
            self.x = food_pos[0]
            self.y = food_pos[1]
            self.eat_food(my_map, food_pos)
            self.time_2_death += 5  # live longer
        else:
            self.move_to_target(food_pos)


class Duck(Creature):
    TIME_2_HATCH = 4
    TIME_2_LAY_EGG = 10
    TIME_2_AGED = 15
    time_2_death = 100
    EGG = "egg"
    ADULT = "adult"
    VELOCITY_SWIMMING = 30
    VELOCITY_RUNNING = 40

    def __init__(self, pos):
        super().__init__(pos)  # Call parent __init__
        self.egg = None
        self.state = self.EGG
        self.velocity = self.VELOCITY_SWIMMING  # velocity / speed of movement
        self.vision = 200  # can see food from max 40 points away

    def __str__(self):
        return f"{self.state} Duck aged {self.age} @ ({self.x},{self.y})"

    def step_change(self, my_map):
        # change age, state, velocity, ect...
        self.change_status()
        if self.state == self.ADULT:
            # before moving, check if there are some newts or shrimps around * points (it depends on vision)
            # if self.saw_alive_newts(my_map):
            newt_pos = self.search_nearst_target(my_map.get_newts_pos())
            if newt_pos:
                self.track_newts(my_map, newt_pos)
            else:
                shrimp_pos = self.search_nearst_target(my_map.get_shrimps_pos())
                if shrimp_pos:
                    self.track_shrimp(my_map, shrimp_pos)
                else:  # don't found any newts or shrimps
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
            if self.age > self.time_2_death:  # death
                self.state = self.DEATH
        # Ducks can run around 6-8 miles per hour
        # Ducks can swim up to 6 miles per hour
        # Is the duck on land?
        '''
        if [self.x, self.y] in self.map.land:
            self.velocity = self.VELOCITY_RUNNING
        else:
            self.velocity = self.VELOCITY_SWIMMING
        '''

    def get_size(self):
        if self.state == "egg":
            size = 20
        else:
            size = 25
        return size


class Newt(Creature):
    time_2_death = 80

    def __init__(self, pos):
        super().__init__(pos)  # Call parent __init__
        self.velocity = 15
        self.size = 15
        self.state = "Newt"
        self.vision = 150  # can see food from max 40 points away

    def __str__(self):
        return f"Newt aged {self.age} @ ({self.x},{self.y}) with velocity"

    def step_change(self, my_map):
        # change age, state, velocity, ect...
        self.age += 1
        if self.age > self.time_2_death:  # death
            self.state = self.DEATH
        if self.state == "Newt":
            # before moving, check if there are some shrimps around * points (it depends on vision)
            shrimp_pos = self.search_nearst_target(my_map.get_shrimps_pos())
            if shrimp_pos:
                self.track_shrimp(my_map, shrimp_pos)
            else:  # don't found any newts or shrimps
                super().random_run()  # Call parent step_change

    def get_size(self):
        return self.size


class Shrimp(Creature):
    time_2_death = 50

    def __init__(self, pos):
        super().__init__(pos)  # Call parent __init__
        self.velocity = 5
        self.size = 8
        self.state = "Shrimp"
        self.vision = 80  # can see food from max 40 points away

    def __str__(self):
        return f"Shrimp aged {self.age} @ ({self.x},{self.y})"

    def step_change(self, my_map):
        # change age, state, velocity, ect...
        self.age += 1
        if self.age > self.time_2_death:  # death
            self.state = self.DEATH
        if self.state == "Shrimp":
            # before moving, check if there are some foods around * points (it depends on vision)
            food_pos = self.search_nearst_target(my_map.get_foods_pos())
            if food_pos:
                self.track_foods(my_map, food_pos)
            else:  # don't found any newts or shrimps
                super().random_run()  # Call parent step_change

    def get_size(self):
        return self.size
