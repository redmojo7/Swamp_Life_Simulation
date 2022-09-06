#
# Author :
# ID :
#
#
#
# Revisions:
#
# 12/4/21 – Base version for assignment
#

import numpy as np
import pygame
import random
from swamp import Duck, Newt

ROW_MAX = 400
COL_MAX = 400
POP = 20
STEPS = 10

COLOR_GRID = (40, 40, 40)
COLOR_NEWT = (0, 255, 255)  # Cyan
COLOR_DUCK = (128, 128, 128)  # Gray
COLOR_SHRIMP = (220, 20, 60)  # Crimson
COLOR_FOOD = (255, 99, 71)  # Tomato

# Initializing Pygame
pygame.init()
# Initializing surface
# create the display screen object
screen = pygame.display.set_mode((COL_MAX, ROW_MAX))

# set the pygame window name
pygame.display.set_caption("Swamp Life Simulation")

running = True
current_gen = np.zeros((ROW_MAX, COL_MAX), dtype=int)
# Initialing Color
screen.fill(COLOR_GRID)
# Drawing :This function is used to update the content of the entire display surface of the screen.
pygame.display.flip()
pygame.display.update()


# return a random position
def random_position():
    # keep away from the boarder, at least 10 points
    return [random.randint(0, ROW_MAX - 10), random.randint(0, COL_MAX - 10)]


ducks = []
newts = []
# Initialing duck population
for i in range(5):
    ducks.append(Duck(random_position()))
    print(ducks[i])

# Initialing newt population
for i in range(10):
    newts.append(Newt(random_position()))
    print(newts[i])

SIZE = 10
# dimensions of the object
WIDTH = SIZE - 1
HEIGHT = SIZE - 1


# velocity / speed of movement
# VELOCITY = 10


def board_check(living):
    row_moved = living.pos[0]
    col_moved = living.pos[1]
    if row_moved < 0:
        row_moved = 0
    if col_moved < 0:
        col_moved = 0
    # "ROW_MAX - living.get_size()" --- prevent living cross border at the first time
    if row_moved > ROW_MAX - living.get_size():
        row_moved = ROW_MAX - living.get_size()
    if col_moved >= COL_MAX - living.get_size():
        col_moved = COL_MAX - living.get_size()
    living.pos = [row_moved, col_moved]


def update_cell():
    next_gen = np.zeros((current_gen.shape[0], current_gen.shape[1]), dtype=int)
    #color = COLOR_GRID
    print("\n ### next generation ###")

    for duck in ducks:
        color = COLOR_DUCK
        row = duck.pos[0]
        col = duck.pos[1]
        # move and board check
        duck.step_change()
        board_check(duck)

        row_moved = duck.pos[0]
        col_moved = duck.pos[1]
        width = duck.get_size() - 1
        height = duck.get_size() - 1
        print(
            f"duck moved from position ({row}, {col}) to position: ({row_moved}, {col_moved} with size {duck.get_size()}) ")
        pygame.draw.rect(screen, color, (col_moved, row_moved, width, height))

    for newt in newts:
        color = COLOR_NEWT
        row = newt.pos[0]
        col = newt.pos[1]
        # move aRnd board check
        newt.step_change()
        board_check(newt)

        row_moved = newt.pos[0]
        col_moved = newt.pos[1]
        width = newt.get_size() - 1
        height = newt.get_size() - 1
        print(
            f"newt moved from position ({row}, {col}) to position: ({row_moved}, {col_moved} with size {newt.get_size()}) ")
        pygame.draw.rect(screen, color, (col_moved, row_moved, width, height))
    return next_gen


food_positions = []


# reproduce food with max number
def reproduce_food(number):
    # product_food - 10% chance of reproducing  in cell

    food_width = 5
    food_height = 5
    # if there is no food left
    if len(food_positions) <= 0:
        for index in range(number):  # range(random.randint(1, number)):
            reproduce = True
            try_times = 5
            while reproduce or try_times == 0:
                try_times -= 1
                x = random.randint(0, ROW_MAX - 10)
                y = random.randint(0, COL_MAX - 10)
                # Moore's neighbourhoods with 5 points, there are some livings
                if np.sum(current_gen[x - 5:x + 6, y - 5:y + 6]) == 0:
                    food_positions.append([x, y])
                    reproduce = False
                    print(f"Food was produced at ({x}, {y})")

    # show food left on the screen
    for row, col in food_positions:
        pygame.draw.rect(screen, COLOR_FOOD, (col, row, food_width, food_height))
        print(f"Food will be show at ({row}, {col})")


# infinite loop
# Indicates pygame is running
running = True

while running:
    # Creates time delay of 10ms
    pygame.time.delay(800)

    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get():

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:
            # it will make exit the while loop
            run = False

    # completely fill the screen with initialing colour
    screen.fill(COLOR_GRID)
    current_gen = update_cell()
    #
    reproduce_food(5)

    pygame.display.update()

# closes the pygame window
pygame.quit()
