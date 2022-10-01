import pygame
from border import step_check
from swamp import Duck, Shrimp, Newt

# load images
duck_img = pygame.image.load('png/duck2.png')
duck_egg_img = pygame.image.load('png/duck_egg.png')
newt_img = pygame.image.load('png/newt2.png')
shrimp_img = pygame.image.load('png/shrimp.png')


def update_cells(screen, my_map):
    # for ducks
    update_cells_4_ducks(screen, my_map)
    # for newts
    update_cells_4_newts(screen, my_map)
    # for shrimps
    update_cells_4_shrimps(screen, my_map)


def update_cells_4_shrimps(screen, my_map):
    if not my_map.shrimps_list:
        print("all shrimps died")
    for shrimp in my_map.shrimps_list:
        x = shrimp.x
        y = shrimp.y
        # move and board check
        shrimp.step_change(my_map)
        step_check(x, y, shrimp, my_map)
        x_moved = shrimp.x
        y_moved = shrimp.y
        width = shrimp.get_size() - 1
        height = shrimp.get_size() - 1
        print(f"{shrimp} moved from position ({x},{y}) to position: "
              f"({x_moved},{y_moved}) with size {shrimp.get_size()} ")
        scaled_shrimp_img = pygame.transform.scale(shrimp_img, (width, height))
        screen.blit(scaled_shrimp_img, (x_moved, y_moved))


def update_cells_4_newts(screen, my_map):
    if not my_map.newts_list:
        print("all newts died")
    for newt in my_map.newts_list:
        x = newt.x
        y = newt.y
        # move and board check
        newt.step_change(my_map)
        step_check(x, y, newt, my_map)
        x_moved = newt.x
        y_moved = newt.y
        width = newt.get_size() - 1
        height = newt.get_size() - 1
        print(
            f"{newt} moved from position ({x},{y}) to position: "
            f"({x_moved},{y_moved}) with size {newt.get_size()} ")
        # pygame.draw.rect(screen, color, (col_moved, row_moved, width, height))
        scaled_newt_img = pygame.transform.scale(newt_img, (width, height))
        screen.blit(scaled_newt_img, (x_moved, y_moved))


def update_cells_4_ducks(screen, my_map):
    if not my_map.ducks_list:
        print("all ducks died")
    # iterate all alive duck
    for duck in my_map.ducks_list:
        x = duck.x
        y = duck.y
        # move
        duck.step_change(my_map)
        step_check(x, y, duck, my_map)
        x_moved = duck.x
        y_moved = duck.y
        width = duck.get_size() - 1
        height = duck.get_size() - 1
        print(f"{duck} moved from position ({x},{y}) to position: "
              f"({x_moved},{y_moved}) with size {duck.get_size()} ")
        # pygame.draw.rect(screen, COLOR_DUCK, (col_moved, row_moved, width, height))
        if duck.state != duck.DEATH:
            if duck.state == duck.ADULT:
                img = duck_img
            elif duck.state == duck.EGG:
                img = duck_egg_img
            scaled_duck_img = pygame.transform.scale(img, (width, height))
            screen.blit(scaled_duck_img, (x_moved, y_moved))


def remove_died_creatures(my_map):
    # remove ducks who died
    my_map.ducks_list = list(filter(lambda d: d.state != d.DEATH, my_map.ducks_list))
    # remove newts who died
    my_map.newts_list = list(filter(lambda n: n.state != n.DEATH, my_map.newts_list))
    # remove shrimps who died
    my_map.shrimps_list = list(filter(lambda s: s.state != s.DEATH, my_map.shrimps_list))


def add_baby(my_map):
    # add new egg to map for duck
    mama_ducks = list(filter(lambda d: d.eggs is not None, my_map.ducks_list))
    for duck in mama_ducks:
        my_map.ducks_list.append(Duck(duck.eggs))
        print(f"{duck} has a baby @ {duck.eggs}")
        duck.eggs = None  # remove from mama

    # add new egg to map for newts
    mama_newts = list(filter(lambda n: n.eggs is not None, my_map.newts_list))
    for newt in mama_newts:
        for baby in newt.eggs:
            my_map.newts_list.append(Newt(baby))
            print(f"{newt} has a baby @ {baby}")
        newt.eggs = None  # remove from mama

    # add new egg to map for shrimps
    mama_shrimps = list(filter(lambda s: s.eggs is not None, my_map.shrimps_list))
    for shrimp in mama_shrimps:
        for baby in shrimp.eggs:
            my_map.shrimps_list.append(Shrimp(baby))
            print(f"{shrimp} has a baby @ {baby}")
        shrimp.eggs = None  # remove from mama
