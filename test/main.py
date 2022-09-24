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
import time

import numpy as np
import pygame
import random


ROW_MAX = 400
COL_MAX = 400
POP = 20
STEPS = 10

COLOR_BG = (10,10,10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)

# Initializing Pygame
pygame.init()
# Initializing surface
# create the display screen object
screen = pygame.display.set_mode((COL_MAX, ROW_MAX))

# set the pygame window name
pygame.display.set_caption("Swamp Life Simulation")

running = True
cell = np.zeros((ROW_MAX, COL_MAX), dtype=int)
# Initialing Color
screen.fill(COLOR_GRID)
# Drawing :This function is used to update the content of the entire display surface of the screen.
pygame.display.flip()

# Initialing Color
for i in range(10):
    # index from 0 to (max-1)
    randX = random.randint(0, ROW_MAX-1)
    randY = random.randint(0, COL_MAX-1)
    cell[randX, randY] = 1
    print("position: ", randX, randY)
    pygame.draw.rect(screen, COLOR_ALIVE_NEXT, (randX, randY, 9, 9))
    pygame.display.update()


SIZE = 10
# dimensions of the object
WIDTH = SIZE - 1
HEIGHT = SIZE - 1

# velocity / speed of movement
VELOCITY = 10

def update_cell():
    next_grid = np.zeros((cell.shape[0], cell.shape[1]), dtype=int)
    color = COLOR_GRID
    print("next generation")
    for row, col in np.ndindex(cell.shape):
        for index in range(cell[row, col]):
            row_moved = row + random.choice([-abs(VELOCITY), 0, VELOCITY])
            col_moved = col + random.choice([-abs(VELOCITY), 0, VELOCITY])
            if row_moved < 0:
                row_moved = 0
            if col_moved < 0:
                col_moved = 0
            if row_moved >= ROW_MAX:
                row_moved = ROW_MAX - VELOCITY
            if col_moved >= COL_MAX:
                col_moved = COL_MAX - VELOCITY
            # Reproduction - 10% chance of reproducing +1 to pop in cell
            if random.random() <= 1:
                next_grid[row_moved, col_moved] += 1
                color = COLOR_ALIVE_NEXT
                print(f"from position ({row}, {col}) to position: ({row_moved}, {col_moved})")
            #else:
            #    color = COLOR_DIE_NEXT

            # drawing object on screen which is rectangle here
            pygame.draw.rect(screen, color, (col_moved, row_moved, WIDTH, HEIGHT))
    return next_grid

# Indicates pygame is running
running = True

# infinite loop
while running:
    # Creates time delay of 10ms
    pygame.time.delay(10)

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
    cell = update_cell()

    pygame.display.update()

# closes the pygame window
pygame.quit()
