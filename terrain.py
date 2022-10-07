import pygame
import random

from config import load_config

COLOR_SEA = (141, 213, 242)
COLOR_WHITE = (255, 255, 255)
COLOR_DEEPGREEN = (77, 150, 50)  # mountains
PI = 3.141592653

# load configuration
config = load_config()


def initial_terrain(my_map):
    # Initialing lands
    my_map.set_lands()

    # Initialing mountains
    # triangle (top_middle, left_bottom, right_bottom)

    # Draws the mountains in sea
    EXPANDED_POINT = 15
    WIDTH = my_map.width
    HEIGHT = my_map.height

    num_mountains_sea = config['mountains']['inSea']
    step = int((0.4*WIDTH)/num_mountains_sea)
    for x_offset in range(int(0.225 * WIDTH), int(0.625 * WIDTH), step):
        print(f"Initialing mountains in sea :\n "
              f"{[int(0.125 * WIDTH) + x_offset, int(0.65 * HEIGHT) - EXPANDED_POINT]},"
              f"{[0 + x_offset - EXPANDED_POINT, int(0.75 * HEIGHT) + EXPANDED_POINT]},"
              f"{[int(0.25 * WIDTH) + x_offset + EXPANDED_POINT, int(0.75 * HEIGHT) + EXPANDED_POINT]}")
        my_map.set_mountains(int(0.125 * WIDTH) + x_offset, int(0.65 * HEIGHT) - EXPANDED_POINT,
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


# Terrain
def draw_terrain(screen, my_map):
    land_height = my_map.land_height
    width = my_map.width
    height = my_map.height
    water_height = height - land_height
    # Draws the sea and waves
    # argument : pygame.draw.rect(window, color, (x, y, width, height))
    pygame.draw.rect(screen, COLOR_SEA, [0, land_height, width, water_height], 0)
    for x_offset in range(0, width, 30):
        # pygame.draw.arc(surface, color, rect, start_angle, stop_angle, width=1) -> Rect
        # arc rect (Rect) -- rectangle to indicate the position and dimensions of the ellipse
        #     which the arc will be based on, the ellipse will be centered inside the rectangle
        # Greek letter τ that equals 2π, 1/2π is 90°
        pygame.draw.arc(screen, COLOR_WHITE, [0 + x_offset, land_height - 10, 30, 30], 0, PI, 12)

    # Draws mountains
    for row in range(0, height - 1):
        for col in range(0, width - 1):
            if my_map.mountains_cells[row, col] == 1:
                screen.set_at((col, row), COLOR_DEEPGREEN)


# return a random position [x,y]
def random_position(my_map):
    # keep away from the boarder, at least 10 points
    recreate = True
    while recreate:
        [col, row] = [random.randint(0, my_map.width - 10),
                      random.randint(0, my_map.height - 10)]
        # but not on the mountain
        if my_map.mountains_cells[row, col] == 0:
            recreate = False
    return [col, row]


# return a random position [x,y]
def random_position_in_water(my_map):
    # keep away from the boarder, at least 10 points
    recreate = True
    while recreate:
        [col, row] = [random.randint(0, my_map.width - 10),
                      random.randint(my_map.land_height, my_map.height - 10)]
        # but not on the mountain
        if my_map.mountains_cells[row, col] == 0:
            recreate = False
    return [col, row]


# should be removed
'''
def draw_terrain_old(screen, my_map):
    LAND_HEIGHT = my_map.land_height
    WIDTH = my_map.width
    HEIGHT = my_map.HEIGHT
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
'''
