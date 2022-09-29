import pygame

COLOR_SEA = (141, 213, 242)
COLOR_WHITE = (255, 255, 255)
COLOR_DEEPGREEN = (77, 150, 50)  # mountains
PI = 3.141592653


# Terrain
def draw_terrain(screen, my_map):
    LAND_HEIGHT = my_map.land_height
    WIDTH = my_map.width
    HEIGHT = my_map.height
    # Draws the sea and waves
    pygame.draw.rect(screen, COLOR_SEA, [0, LAND_HEIGHT, WIDTH, int(HEIGHT * 2 / 3)], 0)
    for x_offset in range(0, WIDTH, 30):
        pygame.draw.arc(screen, COLOR_WHITE, [0 + x_offset, LAND_HEIGHT - 10, 30, 30], PI / 2, PI, 12)
        pygame.draw.arc(screen, COLOR_WHITE, [0 + x_offset, LAND_HEIGHT - 10, 30, 30], 0, PI / 2, 12)

    # Draws mountains
    for row in range(0, my_map.height - 1):
        for col in range(0, my_map.width - 1):
            if my_map.mountains_cells[row, col] == 1:
                screen.set_at((col, row), COLOR_DEEPGREEN)


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
