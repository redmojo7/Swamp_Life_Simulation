# reproduce food with max number
import random

import pygame

import tools

COLOR_FOOD = (52, 140, 49)  # Grass
grass_img = pygame.image.load('png/grass.png')


# Non-moving objects
def reproduce_food(number, screen, my_map):
    food_positions = []
    food_width = 5
    food_height = 5
    WIDTH = my_map.width
    LAND_HEIGHT = my_map.land_height
    HEIGHT = my_map.height
    # if there is no food left
    if len(my_map.foods) <= 0:
        # product_food - 10% chance of reproducing  in cell
        if random.random() > 0.5:
            return
        for index in range(number):  # range(random.randint(1, number)):
            [x, y] = tools.random_position_in_water(WIDTH, LAND_HEIGHT, HEIGHT, my_map.mountains_cells)
            food_positions.append([x, y])
            print(f"Food was produced at ({x}, {y})")
        # add foods to map
        my_map.add_food(food_positions)

    # show food left on the screen
    for col, row in my_map.foods:
        # pygame.draw.rect(screen, COLOR_FOOD, (col, row, food_width, food_height))
        scaled_grass_img = pygame.transform.scale(grass_img, (food_width, food_height))
        screen.blit(scaled_grass_img, (col, row))
        # print(f"Food will be show at ({col}, {row})")
