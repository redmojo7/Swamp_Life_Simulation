#
# Author :
# ID :
#
# duck eat newt
# newt eat shrimp
#
# Revisions:
#
# 12/4/21 – Base version for assignment
#

import numpy as np
import pygame
import random

from map import Map
from swamp import Duck, Newt

HEIGHT = 600
WIDTH = 1200
POP = 20
STEPS = 10

COLOR_GRID = (40, 40, 40)
COLOR_NEWT = (0, 255, 255)  # Cyan
COLOR_DUCK = (128, 128, 128)  # Gray
COLOR_SHRIMP = (220, 20, 60)  # Crimson
COLOR_FOOD = (255, 99, 71)  # Tomato
COLOR_TURQUOISE = (64, 224, 208)# Turquoise

# Initializing Pygame
pygame.init()
# Initializing surface, create the display screen object  pygame.display.set_mode((width, height))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# set the pygame window name
pygame.display.set_caption("Swamp Life Simulation")
# Initialing Color
screen.fill(COLOR_GRID)
# Drawing :This function is used to update the content of the entire display surface of the screen.
pygame.display.flip()
pygame.display.update()

# use current_gen as grid   np.zeros(row, col)
current_gen = np.zeros((HEIGHT, WIDTH), dtype=int)


# return a random position [x,y]
def random_position():
    # keep away from the boarder, at least 10 points
    return [random.randint(0, HEIGHT - 10), random.randint(0, WIDTH - 10)]


# create Map Object
myMap = Map(WIDTH, HEIGHT)
# Initialing terrain
terrain_min_x = 100
terrain_max_x = 410
terrain_min_y = 80
terrain_max_y = 90

terrain = [[row, col] for row in range(terrain_min_x, terrain_max_x) for col in range(terrain_min_y, terrain_max_y)]
myMap.set_terrain(terrain)

ducks = []
newts = []
# Initialing duck population
for i in range(5):
    ducks.append(Duck(random_position(), myMap))
    print(ducks[i])

# Initialing newt population

for i in range(10):
    newts.append(Newt(random_position(), myMap))
    print(newts[i])

duck_img = pygame.image.load('png/duck2.png')
duck_egg_img = pygame.image.load('png/duck_egg.png')
newt_img = pygame.image.load('png/newt.png')

def update_cell():
    next_gen = np.zeros((HEIGHT, WIDTH), dtype=int)
    print("\n ### next generation ###")
    # add new egg to ducks
    mama_ducks = list(filter(lambda d: d.egg is not None, ducks))
    for duck in mama_ducks:
        ducks.append(Duck(duck.egg, myMap))
        duck.egg = None  # remove from mama

    # remove ducks who died
    alive_duck = list(filter(lambda d: d.state != d.DEATH, ducks))
    for duck in alive_duck:
        row = duck.x
        col = duck.y
        # if there is any newts stay at same position, then an adult duck will eat one of them, and stay same cell
        newts_at_same_cell = list(filter(lambda n: n.x == duck.x and n.y == duck.y, newts))
        if newts_at_same_cell and duck.state == duck.ADULT:
            newts.remove(newts_at_same_cell[0])
            duck.age -= 3
        else:  # move
            duck.step_change()
        row_moved = duck.x
        col_moved = row_moved = duck.x
        col_moved = duck.y
        width = duck.get_size() - 1
        height = duck.get_size() - 1
        print(f"duck moved from position ({row}, {col}) to position: ({row_moved}, {col_moved} with size {duck.get_size()}) ")
        # pygame.drawduck.y
        width = duck.get_size() - 1
        height = duck.get_size() - 1
        print(f"duck moved from position ({row}, {col}) to position: ({row_moved}, {col_moved} with size {duck.get_size()}) ")
        # pygame.draw.rect(screen, COLOR_DUCK, (col_moved, row_moved, width, height))
        if duck.state == duck.ADULT:
            img = duck_img
        else:
            img = duck_egg_img
        scaled_duck_img = pygame.transform.scale(img, (width, height))
        screen.blit(scaled_duck_img, (col_moved, row_moved))

    # remove newts who died
    alive_newt = list(filter(lambda n: n.state != n.DEATH, newts))
    for newt in alive_newt:
        color = COLOR_NEWT
        row = newt.x
        col = newt.y
        # move aRnd board check
        newt.step_change()

        row_moved = newt.x
        col_moved = newt.y
        width = newt.get_size() - 1
        height = newt.get_size() - 1
        print(
            f"newt moved from position ({row}, {col}) to position: ({row_moved}, {col_moved} with size {newt.get_size()}) ")
        #pygame.draw.rect(screen, color, (col_moved, row_moved, width, height))
        scaled_newt_img = pygame.transform.scale(newt_img, (width, height))
        screen.blit(scaled_newt_img, (col_moved, row_moved))

    return next_gen


food_positions = []


# reproduce food with max number
def reproduce_food(number):
    food_width = 5
    food_height = 5
    # if there is no food left
    if len(food_positions) <= 0:
        # product_food - 10% chance of reproducing  in cell
        if random.random() > 0.9:
            return
        for index in range(number):  # range(random.randint(1, number)):
            reproduce = True
            try_times = 5
            while reproduce or try_times == 0:
                try_times -= 1
                x = random.randint(0, HEIGHT - 10)  # - 10: not close to the board
                y = random.randint(0, WIDTH - 10)
                # Moore's neighbourhoods with 5 points, there is no any creatures
                if np.sum(current_gen[x - 5:x + 6, y - 5:y + 6]) == 0:
                    food_positions.append([x, y])
                    reproduce = False
                    print(f"Food was produced at ({x}, {y})")

    # add foods to map
    myMap.add_food(food_positions)
    # show food left on the screen
    for row, col in food_positions:
        pygame.draw.rect(screen, COLOR_FOOD, (col, row, food_width, food_height))
        print(f"Food will be show at ({row}, {col})")


# infinite loop
# Indicates pygame is running
running = True


def show_terrain():
    width = terrain_max_y - terrain_min_y
    height = terrain_max_x - terrain_min_x
    pygame.draw.rect(screen, COLOR_TURQUOISE, (terrain_min_x, terrain_min_y, width, height))


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
    reproduce_food(25)
    # show terrain
    show_terrain()

    pygame.display.update()

# closes the pygame window
pygame.quit()
