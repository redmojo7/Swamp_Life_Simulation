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
from tools import is_inside, is_outside

HEIGHT = 600
WIDTH = 1200
POP = 20
STEPS = 10

COLOR_GRID = (40, 40, 40)
COLOR_NEWT = (0, 255, 255)  # Cyan
COLOR_DUCK = (128, 128, 128)  # Gray
COLOR_SHRIMP = (220, 20, 60)  # Crimson
COLOR_FOOD = (255, 99, 71)  # Tomato
COLOR_TURQUOISE = (64, 224, 208)  # Turquoise
COLOR_DARK_BLUE = (0, 60, 95)  #
COLOR_LAND = (242, 191, 141)  # A ztec Gold
COLOR_SEA = (141, 213, 242)
COLOR_WHITE = (255, 255, 255)
COLOR_DEEPGREEN = (77, 150, 50)
COLOR_BROWN = (117, 41, 19)

PI = 3.141592653

# Initializing Pygame
pygame.init()
# Initializing surface, create the display screen object  pygame.display.set_mode((width, height))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# set the pygame window name
pygame.display.set_caption("Swamp Life Simulation")
# Initialing Color
# screen.fill(COLOR_GRID)
screen.fill(COLOR_LAND)
# Drawing :This function is used to update the content of the entire display surface of the screen.
pygame.display.flip()
pygame.display.update()

# use current_gen as grid   np.zeros(row, col)
current_gen = np.zeros((HEIGHT, WIDTH), dtype=int)

'''
mountains in sea :
[450, 450],[300, 550],[600, 550]
mountains in sea :
[650, 450],[500, 550],[800, 550]
mountains in sea :
[850, 450],[700, 550],[1000, 550]
mountains on land :
[350, 50],[250, 150],[450, 150]
'''


# return a random position [x,y]
def random_position():
    # keep away from the boarder, at least 10 points
    recreate = True
    while recreate:
        [x, y] = [random.randint(0, HEIGHT - 10), random.randint(0, WIDTH - 10)]
        # but not on the mountain
        if myMap.mountains_cells[x, y] == 0:
            recreate = False
    return [x, y]


def random_position_in_water():
    # keep away from the boarder, at least 10 points
    recreate = True
    while recreate:
        [x, y] = [random.randint(int(HEIGHT / 3), HEIGHT - 10), random.randint(0, WIDTH - 10)]
        # but not on the mountain
        if myMap.mountains_cells[x, y] == 0:
            recreate = False
    return [x, y]


# create Map Object
myMap = Map(WIDTH, HEIGHT)

# Initialing terrain (for high altitude)


# Initialing mountains
# Draws mountains in sea
for xOffset in range(int(0.25 * WIDTH), int(0.75 * WIDTH), 200):
    print(f"Initialing mountains in sea :\n {[150 + xOffset, int(0.55 * HEIGHT)]},"
          f"{[0 + xOffset, int(0.75 * HEIGHT)]},{[300 + xOffset, int(0.75 * HEIGHT)]}")
    myMap.set_mountains(150 + xOffset, int(0.55 * HEIGHT), 0 + xOffset, int(0.75 * HEIGHT), 300 + xOffset, int(0.75 * HEIGHT))

# Draws mountains on land
myMap.set_mountains(350, 50, 250, 150, 450, 150)
print(f"Initialing mountains on land :\n{[350, 50]},{[250, 150]},{[450, 150]}")



ducks = []
newts = []
# Initialing duck population
for i in range(5):
    ducks.append(Duck(random_position(), myMap))
    print(ducks[i])

# Initialing newt population

for i in range(40):
    newts.append(Newt(random_position_in_water(), myMap))
    print(newts[i])

myMap.add_creatures(ducks)
myMap.add_creatures(newts)

duck_img = pygame.image.load('png/duck2.png')
duck_egg_img = pygame.image.load('png/duck_egg.png')
newt_img = pygame.image.load('png/newt.png')


def update_cell():
    next_gen = np.zeros((HEIGHT, WIDTH), dtype=int)
    print("\n ### next generation ###")
    # add new egg to ducks
    mama_ducks = list(filter(lambda d: d.egg is not None, myMap.ducks_list))
    for duck in mama_ducks:
        ducks.append(Duck(duck.egg, myMap))
        duck.egg = None  # remove from mama

    # remove ducks who died
    alive_duck = list(filter(lambda d: d.state != d.DEATH, myMap.ducks_list))
    for duck in alive_duck:
        row = duck.x
        col = duck.y
        # if there is any newts stay at same position, then an adult duck will eat one of them, and stay same cell
        # newts_at_same_cell = list(filter(lambda n: n.x == duck.x and n.y == duck.y, newts))
        # move
        duck.step_change()
        row_moved = duck.x
        col_moved = duck.y
        # pygame.drawduck.y
        width = duck.get_size() - 1
        height = duck.get_size() - 1
        print(
            f"duck moved from position ({row}, {col}) to position: ({row_moved}, {col_moved}) with size {duck.get_size()} ")
        # pygame.draw.rect(screen, COLOR_DUCK, (col_moved, row_moved, width, height))
        if duck.state == duck.ADULT:
            img = duck_img
        elif duck.state == duck.EGG:
            img = duck_egg_img
        scaled_duck_img = pygame.transform.scale(img, (width, height))
        screen.blit(scaled_duck_img, (col_moved, row_moved))

    # remove newts who died
    alive_newt = list(filter(lambda n: n.state != n.DEATH, myMap.newts_list))
    if not alive_newt:
        print("aaa")
    for newt in alive_newt:
        row = newt.x
        col = newt.y
        # move aRnd board check
        newt.step_change()

        row_moved = newt.x
        col_moved = newt.y
        width = newt.get_size() - 1
        height = newt.get_size() - 1
        print(
            f"newt moved from position ({row}, {col}) to position: ({row_moved}, {col_moved}) with size {newt.get_size()} ")
        # pygame.draw.rect(screen, color, (col_moved, row_moved, width, height))
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
        if random.random() > 0.0:
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



def draw_terrain():
    # Draws the sea and waves
    pygame.draw.rect(screen, COLOR_SEA, [0, int(HEIGHT / 3), WIDTH, int(HEIGHT * 2 / 3)], 0)
    for xOffset in range(0, WIDTH, 30):
        pygame.draw.arc(screen, COLOR_WHITE, [0 + xOffset, int(HEIGHT / 3) - 10, 30, 30], PI / 2, PI, 12)
        pygame.draw.arc(screen, COLOR_WHITE, [0 + xOffset, int(HEIGHT / 3) - 10, 30, 30], 0, PI / 2, 12)

    # Draws the mountains in sea
    for xOffset in range(int(0.25 * WIDTH), int(0.75 * WIDTH), 200):
        print(f"mountains in sea :\n{[150 + xOffset, int(0.55 * HEIGHT)]}, "
              f"{[0 + xOffset, int(0.75 * HEIGHT)]},{[300 + xOffset, int(0.75 * HEIGHT)]}")
        pygame.draw.polygon(screen, COLOR_DEEPGREEN,
                            [[150 + xOffset, int(0.55 * HEIGHT)], [0 + xOffset, int(0.75 * HEIGHT)],
                             [300 + xOffset, int(0.75 * HEIGHT)]], 0)

    # mountains on land
    pygame.draw.polygon(screen, COLOR_DEEPGREEN, [[350, 50], [250, 150], [450, 150]], 0)
    print(f"mountains on land :\n{[350, 50]},{[250, 150]},{[450, 150]}")


while True:
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
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            running = not running
        if pygame.mouse.get_pos()[0]:
            pos = pygame.mouse.get_pos()
            print(f"mouse click at ({pos})")

    # completely fill the screen with initialing colour
    # screen.fill(COLOR_GRID)
    screen.fill(COLOR_LAND)
    if running:
        draw_terrain()
        current_gen = update_cell()
        #
        reproduce_food(25)
        # show terrain

        pygame.display.update()

# closes the pygame window
pygame.quit()
