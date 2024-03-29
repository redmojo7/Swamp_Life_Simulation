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
from terrain import initial_terrain, draw_terrain, random_position_in_water, random_position
from grass import reproduce_food
from map import Map
from swamp import Duck, Shrimp, Newt
from simulation import restore, save_states, interactions, next_generation, restore_asking

# load configuration
config = load_config()

# create output folder
if not path.exists('output'):
    # Create a new directory because it does not exist
    os.makedirs('output')
    print("The new directory 'output' is created!")

# window size
HEIGHT = config['window']['height']
LAND_HEIGHT = config['land']['height']  # int(HEIGHT / 3)
WIDTH = config['window']['width']

# creatures
NUM_DUCK = config['creatures']['duck']
NUM_NEWT = config['creatures']['newt']
NUM_SHRIMP = config['creatures']['shrimp']

# set colors
COLOR_LAND = (242, 191, 141)


def main():
    need_restore = restore_asking()

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
    initial_terrain(my_map)

    ducks = []
    newts = []
    shrimps = []

    # if it needs to restore simulation
    if need_restore:
        # reset generation
        generation = config['generation']
        restore(ducks, newts, shrimps)
    else:
        # Initialing Creatures
        [ducks.append(Duck(random_position(my_map))) for i in range(NUM_DUCK)]
        [newts.append(Newt(random_position(my_map))) for i in range(NUM_NEWT)]
        [shrimps.append(Shrimp(random_position_in_water(my_map))) for i in range(NUM_SHRIMP)]

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

        for event in pygame.event.get():
            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:
                # it will make exit the while loop
                simulation_running = False
                program_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # pause or restart simulation
                simulation_running = not simulation_running
                if simulation_running:
                    pygame.display.set_caption("Swamp Life Simulation")
                else:
                    pygame.display.set_caption("Swamp Life Simulation(Pause)")
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pos()[0]:
                    pos = pygame.mouse.get_pos()
                    print(f"mouse was clicked at ({pos})")
                    point_info = my_font.render(f"point : {pos}", False, (0, 0, 0))
                    screen.fill(COLOR_LAND, (10, 10, 100, 20))
                    screen.blit(point_info, (10, 10))

                    # mouse as a duck
                    # my_map.ducks_list = []
                    # duck = Duck(pos)
                    # duck.age = 5
                    # my_map.add_creatures([duck])

                    # mouse as a newt
                    my_map.newts_list = []
                    n = Newt(pos)
                    n.set_attributes(10, "adult", 15, 15)
                    my_map.add_creatures([n])

                    # mouse as a shrimp
                    # my_map.shrimps_list = []
                    # my_map.add_creatures([Shrimp(pos)])

                    pygame.display.update()

        # if all died, the quit
        if (not my_map.ducks_list) and (not my_map.newts_list) and (not my_map.shrimps_list):
            print("All creatures died. Simulation Finished")
            simulation_running = False
            program_running = False
        # Visualization
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
