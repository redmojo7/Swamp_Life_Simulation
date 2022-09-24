#
# Author : Peng
# ID : 21053409
#
# duck eat newt
# newt eat shrimp
#
# Revisions:
#
# 12/4/21 – Base version for assignment
#
import pygame
import os.path
from os import path
from config import load_config
from terrain import draw_terrain
from grass import reproduce_food
from map import Map
from swamp import Duck, Shrimp, Newt
from simulation import restore, save_states, interactions, next_generation
from tools import random_position_in_water, random_position

# load configuration
config = load_config()

# create output folder
if not path.exists('output'):
    # Create a new directory because it does not exist
    os.makedirs('output')
    print("The new directory 'output' is created!")

# window size
HEIGHT = config['window']['height']
LAND_HEIGHT = int(HEIGHT / 3)
WIDTH = config['window']['width']

# creatures
NUM_DUCK = config['creatures']['duck']
NUM_NEWT = config['creatures']['newt']
NUM_SHRIMP = config['creatures']['shrimp']

# if it needs to restore simulation
need_restore = config['need_restore']

# set colors
COLOR_LAND = (242, 191, 141)


def main():
    # generation is 0
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
    screen.fill(COLOR_LAND)
    # Drawing :This function is used to update the content of the entire display surface of the screen.
    pygame.display.flip()
    pygame.display.update()

    # create Map Object
    my_map = Map(WIDTH, HEIGHT, LAND_HEIGHT)

    # Initialing terrain (for high altitude)
    my_map.initial_terrain()

    ducks = []
    newts = []
    shrimps = []

    if need_restore is True:
        # reset generation
        generation = config['generation']
        restore(ducks, newts, shrimps)
    else:
        # Initialing Creatures
        [ducks.append(Duck(random_position(WIDTH, HEIGHT, my_map.mountains_cells))) for i in range(NUM_DUCK)]
        [newts.append(Newt(random_position(WIDTH, HEIGHT, my_map.mountains_cells))) for i in range(NUM_NEWT)]
        [shrimps.append(Shrimp(random_position_in_water(WIDTH, LAND_HEIGHT, HEIGHT, my_map.mountains_cells))) for i in
         range(NUM_SHRIMP)]

    my_map.add_creatures(ducks)
    my_map.add_creatures(newts)
    my_map.add_creatures(shrimps)

    # Indicates program is running
    program_running = True
    # Indicates simulation is running
    simulation_running = True

    while program_running:
        # Creates time delay of 10ms
        pygame.time.delay(800)

        # iterate over the list of Event objects
        # that was returned by pygame.event.get() method.
        simulation_running = interactions(screen, simulation_running, my_font)

        if simulation_running:
            # completely fill the screen with initialing colour
            screen.fill(COLOR_LAND)
            # show terrain
            draw_terrain(screen, my_map)
            # next generation
            generation = next_generation(generation, screen, my_map, my_font)
            # reproduce grass
            reproduce_food(10, screen, my_map)
            # save app states
            save_states(generation, my_map)
            # update screen
            pygame.display.update()

    # closes the pygame window
    pygame.quit()


if __name__ == "__main__":
    main()
