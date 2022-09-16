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
#
# max life span :
# duck is 10 years
# newt is 6 years
# shrimp is 2 years
import math
import random

import numpy as np

from tools import manhattan_distance, trace


class Creature(object):  #
    DEATH = "death"
    EGG = "egg"
    ADULT = "adult"

    def __init__(self, pos):
        self.velocity = None
        self.vision = None
        self.eggs = None
        self.state = self.EGG
        self.x = int(pos[0])
        self.y = int(pos[1])
        self.age = 0

    # target is array [x,y]
    def move_to_target(self, target):
        print(f"{self} Move to target ({target[0]},{target[1]})")
        tracer = trace(target, [self.x, self.y], self.velocity)
        self.x = tracer[0]
        self.y = tracer[1]

    def move_away_from(self, pos):
        print(f"{self} move away from {pos}")
        moved_cell_x = random.randint(0, self.velocity)
        moved_cell_y = self.velocity - moved_cell_x
        #
        if self.x - pos[0] > 0:
            self.x += moved_cell_x
        else:
            self.x -= moved_cell_x
        #
        if self.y - pos[1] > 0:
            self.y += moved_cell_y
        else:
            self.y -= moved_cell_y

    # random run(max is velocity, total distance(Manhattan) on x and y)
    def random_run(self):
        moved_cells_x = random.randint(-self.velocity, self.velocity)
        left_steps = self.velocity - abs(moved_cells_x)
        moved_cells_y = random.randint(-left_steps, left_steps)
        self.x += moved_cells_x
        self.y += moved_cells_y

    def step_change(self, my_map):
        # before moving, check if there are some food around ** points (it depends on vision)
        if my_map.foods and self.search_target(my_map.food_cells):
            # to find the nearest one by calculating the Euclidean distance
            # https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_math_vector_and_reflection.md
            food = min([f for f in my_map.foods], key=lambda f: pow(f[0] - self.x, 2) + pow(f[1] - self.y, 2))
            # move forward to food
            print(f"Food was found! @ ({food[0]},{food[1]}) by {self}")
            if food[0] == self.x and food[1] == self.y:
                my_map.eat_food(food)
                self.age -= 3
            else:
                self.move_to_target(food)
        else:
            # if there is no food around, then random running
            self.random_run()

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
            self.time_2_death += 2  # live longer
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
            self.time_2_death += 1  # live longer
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

    def in_water(self, my_map):
        # my_map.lands_cells[row, col] == 0
        return my_map.lands_cells[self.y, self.x] == 0

    def get_size(self):
        return self.size

    def set_attributes(self, age, state, size, velocity):
        self.age = int(age)
        self.state = state
        self.size = int(size)
        self.velocity = int(velocity)


class Duck(Creature):
    name = "Duck"
    TIME_2_HATCH = 10
    TIME_2_AGED = 90
    time_2_death = 100
    VELOCITY_SWIMMING = 30
    VELOCITY_RUNNING = 40

    def __init__(self, pos):
        super().__init__(pos)  # Call parent __init__
        self.state = self.EGG
        self.velocity = self.VELOCITY_SWIMMING  # velocity / speed of movement
        self.vision = 200  # can see food from max 40 points away

    def __str__(self):
        return f"{self.state} Duck aged {self.age} @ ({self.x},{self.y})"

    def step_change(self, my_map):
        # change age, state, velocity, ect...
        self.change_status(my_map)
        # run for ADULT
        if self.state == self.ADULT:
            # before moving, check if there are some newts or shrimps around * points (it depends on vision)
            # if self.saw_alive_newts(my_map):
            newt_pos = self.search_nearst_target(my_map.get_newts_pos())
            # 30% of chance it wants to eat some foods
            if newt_pos and random.random() > 0.3:
                self.track_newts(my_map, newt_pos)
            else:
                shrimp_pos = self.search_nearst_target(my_map.get_shrimps_pos())
                if shrimp_pos:
                    self.track_shrimp(my_map, shrimp_pos)
                else:  # don't found any newts or shrimps
                    super().random_run()  # Call parent step_change

    def change_status(self, my_map):
        self.age += 1
        if self.state == self.EGG and self.age >= self.TIME_2_HATCH:  # ready to HATCH
            self.state = self.ADULT
        elif self.state == self.ADULT:
            if self.velocity == 10 and self.age >= self.TIME_2_AGED:  # old
                self.velocity = 5
            if random.random() < 0.01/math.log2(len(my_map.ducks_list)+2):  # (0.01/log2(num+1))% chance to lay eggs for adult
                self.eggs = [self.x, self.y]
            if self.age > self.time_2_death:  # death
                self.state = self.DEATH
        # Ducks can run around 6-8 miles per hour
        # Ducks can swim up to 6 miles per hour
        # Is the duck on land?
        if self.in_water(my_map):
            self.velocity = self.VELOCITY_SWIMMING
        else:
            self.velocity = self.VELOCITY_RUNNING

    def get_size(self):
        if self.state == "egg":
            size = 20
        else:
            size = 25
        return size


class Newt(Creature):
    TIME_2_HATCH = 5
    TIME_2_AGED = 55
    time_2_death = 60
    name = "Newt"

    def __init__(self, pos):
        super().__init__(pos)  # Call parent __init__
        self.velocity = 15
        self.size = 15
        self.vision = 150  # can see food from max 40 points away

    def __str__(self):
        return f"Newt aged {self.age} @ ({self.x},{self.y})"

    def step_change(self, my_map):
        # change age, state, velocity, ect...
        self.age += 1
        if self.age > self.time_2_death:  # death
            self.state = self.DEATH
        if self.state == self.EGG and self.age >= self.TIME_2_HATCH:  # ready to HATCH
            self.state = self.ADULT
        if random.random() < 0.03/math.log2(len(my_map.newts_list)+1):  # (0.03/log2(num+1))% chance to lay eggs for adult
            self.eggs = [[self.x, self.y]]*random.randint(1, 2)
        # run for ADULT
        if self.state == self.ADULT:
            # before moving, check if there are some Duck around * points (it depends on vision)
            duck_pos = self.search_nearst_target(my_map.get_ducks_pos())
            if duck_pos:
                self.move_away_from(duck_pos)
            else:
                # check if there are some shrimps around * points (it depends on vision)
                shrimp_pos = self.search_nearst_target(my_map.get_shrimps_pos())
                # 50% of chance it wants to eat some foods
                if shrimp_pos and random.random() > 0.4:
                    self.track_shrimp(my_map, shrimp_pos)
                else:  # don't found any newts or shrimps
                    super().random_run()  # Call parent step_change

    def get_size(self):
        if self.state == self.EGG:
            size = 10
        else:
            size = 15
        return size


class Shrimp(Creature):
    TIME_2_HATCH = 2
    TIME_2_AGED = 28
    time_2_death = 30
    name = "Shrimp"
    ADULT_AGE = 10

    def __init__(self, pos):
        super().__init__(pos)  # Call parent __init__
        self.velocity = 5
        self.size = 8
        self.vision = 80  # can see food from max 40 points away

    def __str__(self):
        return f"Shrimp aged {self.age} @ ({self.x},{self.y})"

    def step_change(self, my_map):
        # change age, state, velocity, ect...
        self.age += 1
        if self.age > self.time_2_death:  # death
            self.state = self.DEATH
        if self.state == self.EGG and self.age >= self.TIME_2_HATCH:  # ready to HATCH
            self.state = self.ADULT
        if random.random() < 0.05/math.log2(len(my_map.shrimps_list)+1):  # (0.1/log2(num+1))% chance to lay eggs for adult
            self.eggs = [[self.x, self.y]]*random.randint(1, 5)
        # run for ADULT
        if self.state == self.ADULT:
            # before moving, check if there are some Duck around * points (it depends on vision)
            predictor_pos = self.search_nearst_target(my_map.get_ducks_pos() + my_map.get_newts_pos())
            if predictor_pos:
                self.move_away_from(predictor_pos)
            else:
                # before moving, check if there are some foods around * points (it depends on vision)
                food_pos = self.search_nearst_target(my_map.get_foods_pos())
                # 100% of chance it wants to eat some foods
                if food_pos:
                    self.track_food(my_map, food_pos)
                else:  # don't found any newts or shrimps
                    super().random_run()  # Call parent step_change

    def get_size(self):
        if self.state == self.EGG:
            size = 5
        else:
            size = 8
        return size
