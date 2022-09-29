import os

import pygame
import yaml

from config import load_config, CREATURES_CSV
from grid import add_baby, remove_died_creatures, update_cells
from swamp import Duck, Shrimp, Newt
import csv

config = load_config()


def restore_asking():
    need_restore = False
    if os.path.exists(CREATURES_CSV) and os.stat(CREATURES_CSV).st_size != 0:
        key = input('\nDo you want restore simulation? y/n\n')
        if key.upper() == 'Y':
            input("your choose to restore the simulation. Click any key to continue.\n")
            need_restore = True
        else:
            input("Dont restore the simulation. Click any key to continue.\n")
    return need_restore


def restore(ducks, newts, shrimps):
    # load data from csv
    print(f"Restore creatures from file {CREATURES_CSV}")
    with open(CREATURES_CSV) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] == Duck.name:
                d = Duck([row[5], row[6]])
                d.set_attributes(row[1], row[2], row[3], row[4])
                # print(f"Restore duck for {d}")
                ducks.append(d)
            elif row[0] == Newt.name:
                n = Newt([row[5], row[6]])
                n.set_attributes(row[1], row[2], row[3], row[4])
                # print(f"Restore newt for {n}")
                newts.append(n)
            elif row[0] == Shrimp.name:
                s = Shrimp([row[5], row[6]])
                s.set_attributes(row[1], row[2], row[3], row[4])
                # print(f"Restore shrimp for {s}")
                shrimps.append(s)


def save_states(generation, my_map):
    # save generation
    if config:
        config['generation'] = generation
        with open(CREATURES_CSV, 'w') as config_file:
            yaml.safe_dump(config, config_file)  # Also note the safe_dump
    # save all creatures status
    with open(CREATURES_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        for d in my_map.ducks_list + my_map.newts_list + my_map.shrimps_list:
            writer.writerow([d.name, d.age, d.state, d.get_size(), d.velocity, d.x, d.y])


def show_simulation_info(screen, my_font, generation, my_map):
    WIDTH = my_map.width
    # show generation info
    gen_info = my_font.render(f"Gen : {generation}", False, (0, 0, 0))
    screen.blit(gen_info, (int(0.9 * WIDTH), 0))
    # show ducks info
    duck_info = my_font.render(f"duck : {len(my_map.ducks_list)}", False, (0, 0, 0))
    screen.blit(duck_info, (int(0.9 * WIDTH), 15))
    # show newts info
    newt_info = my_font.render(f"newt : {len(my_map.newts_list)}", False, (0, 0, 0))
    screen.blit(newt_info, (int(0.9 * WIDTH), 30))
    # show shrimps info
    shrimps_info = my_font.render(f"shrimp : {len(my_map.shrimps_list)}", False, (0, 0, 0))
    screen.blit(shrimps_info, (int(0.9 * WIDTH), 45))
    # show foods info
    foods_info = my_font.render(f"food : {len(my_map.foods)}", False, (0, 0, 0))
    screen.blit(foods_info, (int(0.9 * WIDTH), 60))


# set colors
COLOR_LAND = (242, 191, 141)


def interactions(screen, simulation_running, my_font):
    program_running = True
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
        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pos()[0]:
                pos = pygame.mouse.get_pos()
                print(f"mouse was clicked at ({pos})")
                point_info = my_font.render(f"point : {pos}", False, (0, 0, 0))
                screen.fill(COLOR_LAND, (10, 10, 100, 20))
                screen.blit(point_info, (10, 10))
                pygame.display.update()
    return (simulation_running, program_running)


def next_generation(generation, screen, my_map, my_font):
    print("\n ### next generation ###")
    generation += 1
    # add baby into creatures list
    add_baby(my_map)
    # remove died creatures
    remove_died_creatures(my_map)
    # show the number of alive creatures
    show_simulation_info(screen, my_font, generation, my_map)
    # update cells for ducks, newts, shrimps
    update_cells(screen, my_map)
    # return generation
    return generation
