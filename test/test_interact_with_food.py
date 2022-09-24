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
import csv
import os

import numpy as np
import pandas as pd
import pygame
import random
import yaml

from map import Map
from swamp import Duck, Shrimp, Newt

config_yaml = f"{os.path.abspath(os.path.dirname(os.getcwd()))}/config/config.yml"
creatures_csv = f'{os.path.abspath(os.path.dirname(os.getcwd()))}/output/creatures.csv'
with open(config_yaml, 'r') as config_file:
    config = yaml.safe_load(config_file)

HEIGHT = config['window']['height']
WIDTH = config['window']['width']
NUM_DUCK = config['creatures']['duck']
NUM_NEWT = config['creatures']['newt']
NUM_SHRIMP = config['creatures']['shrimp']

need_restore = config['need_restore']

LAND_HEIGHT = int(HEIGHT / 3)

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
generation = 0

# Initializing Pygame
pygame.init()
# setting the pygame font style and size of font
my_font = pygame.font.SysFont('Comic Sans MS', 12)
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

# create Map Object
my_map = Map(WIDTH, HEIGHT, LAND_HEIGHT)

# Initialing terrain (for high altitude)


# Initialing mountains
# triangle (top_middle, left_bottom, right_bottom)
# Draws the mountains in sea
EXPANDED_POINT = 15
for x_offset in range(int(0.125 * WIDTH), int(0.625 * WIDTH), int(WIDTH / 6)):
    print(f"Initialing mountains in sea :\n "
          f"{[int(0.125 * WIDTH) + x_offset, int(0.55 * HEIGHT) - EXPANDED_POINT]},"
          f"{[0 + x_offset - EXPANDED_POINT, int(0.75 * HEIGHT) + EXPANDED_POINT]},"
          f"{[int(0.25 * WIDTH) + x_offset + EXPANDED_POINT, int(0.75 * HEIGHT) + EXPANDED_POINT]}")
    my_map.set_mountains(int(0.125 * WIDTH) + x_offset, int(0.55 * HEIGHT) - EXPANDED_POINT,
                         0 + x_offset - EXPANDED_POINT, int(0.75 * HEIGHT) + EXPANDED_POINT,
                         int(0.25 * WIDTH) + x_offset + EXPANDED_POINT, int(0.75 * HEIGHT) + EXPANDED_POINT)

# Draws mountains on land (extend mountains for 10 points for each side)

my_map.set_mountains(int(0.3 * WIDTH), int(0.08 * HEIGHT) - EXPANDED_POINT,
                     int(0.2 * WIDTH) - EXPANDED_POINT, int(0.25 * HEIGHT) + EXPANDED_POINT,
                     int(0.4 * WIDTH) + EXPANDED_POINT, int(0.25 * HEIGHT) + EXPANDED_POINT)
print(f"Initialing mountains on land :\n"
      f"{[int(0.3 * WIDTH), int(0.08 * HEIGHT) - EXPANDED_POINT]},"
      f"{[int(0.2 * WIDTH) - EXPANDED_POINT, int(0.25 * HEIGHT) + EXPANDED_POINT]},"
      f"{[int(0.4 * WIDTH) + EXPANDED_POINT, int(0.25 * HEIGHT) + EXPANDED_POINT]}")

# Initialing lands
#
#
#
#
my_map.set_lands(LAND_HEIGHT)


# return a random position [x,y]
def random_position():
    # keep away from the boarder, at least 10 points
    recreate = True
    while recreate:
        [col, row] = [random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 10)]
        # but not on the mountain
        if my_map.mountains_cells[row, col] == 0:
            recreate = False
    return [col, row]


def random_position_in_water():
    # keep away from the boarder, at least 10 points
    recreate = True
    while recreate:
        [col, row] = [random.randint(0, WIDTH - 10), random.randint(LAND_HEIGHT, HEIGHT - 10)]
        # but not on the mountain
        if my_map.mountains_cells[row, col] == 0:
            recreate = False
    return [col, row]


ducks = []
newts = []
shrimps = []

if need_restore is True:
    print(f"Restore creatures from file {creatures_csv}")
    with open(creatures_csv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] == Duck.name:
                d = Duck([row[5], row[6]])
                d.set_attributes(row[1], row[2], row[3], row[4])
                print(f"Restore duck for {d}")
                ducks.append(d)
            elif row[0] == Newt.name:
                n = Newt([row[5], row[6]])
                n.set_attributes(row[1], row[2], row[3], row[4])
                print(f"Restore newt for {n}")
                newts.append(n)
            elif row[0] == Shrimp.name:
                s = Shrimp([row[5], row[6]])
                s.set_attributes(row[1], row[2], row[3], row[4])
                print(f"Restore shrimp for {s}")
                shrimps.append(s)

else:
    # Initialing duck population
    for i in range(NUM_DUCK):
        ducks.append(Duck(random_position()))
        print(ducks[i])

    # Initialing newt population
    for i in range(NUM_NEWT):
        newts.append(Newt(random_position()))
        print(newts[i])

    for i in range(NUM_SHRIMP):
        shrimps.append(Shrimp(random_position_in_water()))
        print(shrimps[i])

my_map.add_creatures(ducks)
my_map.add_creatures(newts)
my_map.add_creatures(shrimps)

duck_img = pygame.image.load('../png/duck2.png')
duck_egg_img = pygame.image.load('../png/duck_egg.png')
newt_img = pygame.image.load('../png/newt2.png')
shrimp_img = pygame.image.load('../png/shrimp.png')


def map_border_check(creature):
    # check left and right boarder for all creature
    if creature.x < 0:
        creature.x = 0
    # "WIDTH - creature.get_size()" --- prevent living cross border at the first time
    if creature.x > WIDTH - creature.get_size():
        creature.x = my_map.width - creature.get_size()
    # check bottom boarder for all
    # "HEIGHT - creature.get_size()" --- prevent living cross border at the first time
    if creature.y >= HEIGHT - creature.get_size():
        creature.y = HEIGHT - creature.get_size()
    # check top boarder for each differently
    # for Duck
    if (isinstance(creature, Duck) or isinstance(creature, Newt)) and creature.y < 0:
        creature.y = 0
    # for Newt
    if isinstance(creature, Shrimp) and creature.y < LAND_HEIGHT:
        # stay in water
        creature.y = LAND_HEIGHT


def step_check(pos_x, pos_y, creature):
    #
    map_border_check(creature)
    #
    mountains_border_check(pos_x, pos_y, creature)


def mountains_border_check(pos_x, pos_y, creature):
    # find the nearst border point before moving
    [n_x, n_y] = min([t for t in my_map.mountains_borders],
                     key=lambda t: pow(t[0] - pos_x, 2) + pow(t[1] - pos_y, 2))
    #  if the rectangle area of passing through contains any mountain points
    # (maybe few points, it is ok,like conor of triangle mountain)
    #  then wrong_way = Ture
    #    x,y-----------
    #    --------------
    #    ----------x2,y2
    wrong_way = False
    for col in range(min(pos_x, creature.x), max(pos_x, creature.x) + 1):
        for row in range(min(pos_y, creature.y), max(pos_y, creature.y) + 1):
            if my_map.mountains_cells[row, col] == 1:
                wrong_way = True
                break
        if wrong_way:
            break
    if wrong_way:
        print(f"{creature} move to boarder of mountain ({n_x},{n_y})")
        # move away from this mountain border point
        for [col, row] in [[n_x, n_y - 1], [n_x, n_y + 1], [n_x - 1, n_y], [n_x + 1, n_y]]:
            if my_map.mountains_cells[row, col] == 0:  # move to this way
                if col > n_x:
                    creature.x = n_x + creature.velocity
                    break
                if col < n_x:
                    creature.x = n_x - creature.velocity
                    break
                if row > n_y:
                    creature.y = n_y + creature.velocity
                    break
                if row < n_y:
                    creature.y = n_y - creature.velocity
                    break
        print(f"new position: {creature.x}, {creature.y}")


def remove_died_creatures():
    # remove ducks who died
    my_map.ducks_list = list(filter(lambda d: d.state != d.DEATH, my_map.ducks_list))
    # remove newts who died
    my_map.newts_list = list(filter(lambda n: n.state != n.DEATH, my_map.newts_list))
    # remove shrimps who died
    my_map.shrimps_list = list(filter(lambda s: s.state != s.DEATH, my_map.shrimps_list))


def next_generation():
    print("\n ### next generation ###")
    global generation
    generation += 1
    duck_info = my_font.render(f"Gen : {generation}", False, (0, 0, 0))
    screen.blit(duck_info, (int(0.9 * WIDTH), 0))
    next_gen = np.zeros((HEIGHT, WIDTH), dtype=int)
    
    # remove died creatures
    remove_died_creatures()
    
    # for ducks
    update_cells_4_ducks()
    # for newts
    update_cells_4_newts()
    # for shrimps
    update_cells_4_shrimps()

    return next_gen


def update_cells_4_shrimps():
    my_map.shrimps_list = list(filter(lambda s: s.state != s.DEATH, my_map.shrimps_list))
    shrimps_info = my_font.render(f"shrimp : {len(my_map.shrimps_list)}", False, (0, 0, 0))
    screen.blit(shrimps_info, (int(0.9 * WIDTH), 35))
    if not my_map.shrimps_list:
        print("all shrimps die")
    for shrimp in my_map.shrimps_list:
        x = shrimp.x
        y = shrimp.y
        # move and board check
        shrimp.step_change(my_map)
        step_check(x, y, shrimp)
        x_moved = shrimp.x
        y_moved = shrimp.y
        width = shrimp.get_size() - 1
        height = shrimp.get_size() - 1
        print(f"shrimp moved from position ({x},{y}) to position: "
              f"({x_moved},{y_moved}) with size {shrimp.get_size()} ")
        scaled_shrimp_img = pygame.transform.scale(shrimp_img, (width, height))
        screen.blit(scaled_shrimp_img, (x_moved, y_moved))


def update_cells_4_newts():
    newt_info = my_font.render(f"newt : {len(my_map.newts_list)}", False, (0, 0, 0))
    screen.blit(newt_info, (int(0.9 * WIDTH), 25))
    if not my_map.newts_list:
        print("all newts die")
    for newt in my_map.newts_list:
        x = newt.x
        y = newt.y
        # move and board check
        newt.step_change(my_map)
        step_check(x, y, newt)
        x_moved = newt.x
        y_moved = newt.y
        width = newt.get_size() - 1
        height = newt.get_size() - 1
        print(
            f"newt moved from position ({x},{y}) to position: "
            f"({x_moved},{y_moved}) with size {newt.get_size()} ")
        # pygame.draw.rect(screen, color, (col_moved, row_moved, width, height))
        scaled_newt_img = pygame.transform.scale(newt_img, (width, height))
        screen.blit(scaled_newt_img, (x_moved, y_moved))


def update_cells_4_ducks():
    # add new egg to ducks
    mama_ducks = list(filter(lambda d: d.eggs is not None, my_map.ducks_list))
    for duck in mama_ducks:
        ducks.append(Duck(duck.eggs))
        duck.eggs = None  # remove from mama
    duck_info = my_font.render(f"duck : {len(my_map.ducks_list)}", False, (0, 0, 0))
    screen.blit(duck_info, (int(0.9 * WIDTH), 15))
    for duck in my_map.ducks_list:
        x = duck.x
        y = duck.y
        # move
        duck.step_change(my_map)
        step_check(x, y, duck)
        x_moved = duck.x
        y_moved = duck.y
        width = duck.get_size() - 1
        height = duck.get_size() - 1
        print(f"duck moved from position ({x},{y}) to position: "
              f"({x_moved},{y_moved}) with size {duck.get_size()} ")
        # pygame.draw.rect(screen, COLOR_DUCK, (col_moved, row_moved, width, height))
        if duck.state != duck.DEATH:
            if duck.state == duck.ADULT:
                img = duck_img
            elif duck.state == duck.EGG:
                img = duck_egg_img
            scaled_duck_img = pygame.transform.scale(img, (width, height))
            screen.blit(scaled_duck_img, (x_moved, y_moved))


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
    my_map.add_food(food_positions)
    # show food left on the screen
    for row, col in food_positions:
        pygame.draw.rect(screen, COLOR_FOOD, (col, row, food_width, food_height))
        print(f"Food will be show at ({row}, {col})")


# infinite loop
# Indicates pygame is running
running = True


def draw_terrain():
    # Draws the sea and waves
    pygame.draw.rect(screen, COLOR_SEA, [0, LAND_HEIGHT, WIDTH, int(HEIGHT * 2 / 3)], 0)
    for x_offset in range(0, WIDTH, 30):
        pygame.draw.arc(screen, COLOR_WHITE, [0 + x_offset, LAND_HEIGHT - 10, 30, 30], PI / 2, PI, 12)
        pygame.draw.arc(screen, COLOR_WHITE, [0 + x_offset, LAND_HEIGHT - 10, 30, 30], 0, PI / 2, 12)

    # Draws mountains in sea (zoom out mountains for 20 points for each side)
    # triangle ([x1, y1+20], [x2+20, y2-20], [x3-20, y3-20]])
    for x_offset in range(int(0.125 * WIDTH), int(0.625 * WIDTH), int(WIDTH / 6)):
        # print(f"mountains in sea :\n{[int(0.125 * WIDTH) + x_offset, int(0.55 * HEIGHT)]}, "
        #      f"{[0 + x_offset, int(0.75 * HEIGHT)]},{[int(0.25 * WIDTH) + x_offset, int(0.75 * HEIGHT)]}")
        pygame.draw.polygon(screen, COLOR_DEEPGREEN,
                            [[int(0.125 * WIDTH) + x_offset, int(0.55 * HEIGHT)],
                             [0 + x_offset, int(0.75 * HEIGHT)],
                             [int(0.25 * WIDTH) + x_offset, int(0.75 * HEIGHT)]], 0)

    # mountains on land(zoom out mountains for 20 points for each side)
    #     # triangle ([x1, y1+20], [x2+20, y2-20], [x3-20, y3-20]])
    pygame.draw.polygon(screen, COLOR_DEEPGREEN,
                        [[int(0.3 * WIDTH), int(0.08 * HEIGHT)],
                         [int(0.2 * WIDTH), int(0.25 * HEIGHT)],
                         [int(0.4 * WIDTH), int(0.25 * HEIGHT)]], 0)
    # print(f"mountains on land :\n{[350, 50]},{[250, 150]},{[450, 150]}")

points = []
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
        elif event.type == pygame.MOUSEMOTION:
            print()
            #points.append(event.pos)
        if pygame.mouse.get_pos()[0]:
            pos = pygame.mouse.get_pos()
            print(f"mouse click at ({pos})")

            # mouse as a duck
            #my_map.ducks_list = []
            #duck = Duck(pos)
            #duck.age = 5
            #my_map.add_creatures([duck])

            # mouse as a newt
            my_map.newts_list = []
            my_map.add_creatures([Newt(pos)])

            # mouse as a shrimp
            #my_map.shrimps_list = []
            #my_map.add_creatures([Shrimp(pos)])

            point_info = my_font.render(f"point : {pos}", False, (0, 0, 0))
            screen.fill(COLOR_LAND, (10, 10, 100, 20))
            screen.blit(point_info, (10, 10))
            pygame.display.update()

    if running:
        # completely fill the screen with initialing colour
        screen.fill(COLOR_LAND)
        draw_terrain()
        current_gen = next_generation()
        #
        reproduce_food(25)
        # show terrain

        RED = (255, 0, 0)
        df = pd.read_csv('../foo.csv', sep=',', header=None)
        #if len(points) > 1:
            #rect = pygame.draw.lines(screen, RED, True, points, 3)
        '''
        for i in range(df.shape[0]): #iterate over rows
            for j in range(df.shape[1]): #iterate over columns
                if df.at[i, j] == 0: #get cell value
                    for x in range(i, i*20+1):
                        for y in range(j, j*20+1):
                            #pygame.draw.rect(screen, COLOR_FOOD, (x, y, 1, 1))
                            #screen.set_at((x, y), COLOR_FOOD)
        '''

        pygame.display.update()
        #points.append(pygame.mouse.get_pos())
        #print(f"***************** ({x}, {y})")

# closes the pygame window
pygame.quit()
