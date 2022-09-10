import numpy as np

from swamp import Duck, Newt
from map import Map
from tools import is_inside, get_edge_points

map = Map(500, 500)
map.add_food([[100, 100]])

duck = Duck([10, 20], map)
for i in range(100):
    duck.step_change()
    print(duck.__str__())
'''
newt = Newt([10, 20], map)
for i in range(6):
    newt.step_change()
    print(newt.__str__())
'''
food_cells = np.zeros((50, 50), dtype=int)

food_cells[10, 10] = 1
food_cells[5, 5] = 1


# if I stand at O(0,0)

# drop this (binary search algorithm)
def check_neighbour_with_points(points):
    if np.sum(food_cells[0 - points:points+1, 0 - points:points+1]) == 0:
        next_points = points - (points//2)
        check_neighbour_with_points(next_points)

# find the nearest enemy
enemies = [
    [1, 1],
    [1, 2],
    [4, 5]
]
x = 5
y = 5

enemy = min([e for e in enemies], key=lambda e: pow(e[0]-x, 2) + pow(e[1]-y, 2))
print(enemy)


#
countries = [
    ['China', 1394015977],
    ['United States', 329877505],
    ['India', 1326093247],
    ['Indonesia', 267026366],
    ['Bangladesh', 162650853],
    ['Pakistan', 233500636],
    ['Nigeria', 214028302],
    ['Brazil', 21171597],
    ['Russia', 141722205],
    ['Mexico', 128649565]
]

populated = filter(lambda c: c[1] > 300000000, countries)
print(list(populated))

# Initialing terrain
grid = [[row, col] for row in range(3) for col in range(3)]
print(grid)

terrain = [[row, col] for row in range(100, 210) for col in range(80, 90)]
print(terrain)

list = [[1,1], [2,2]]
print(list.index([1,1]))
if [1,2] not in list:
    print("not")



# Driver program to test above function
# Let us check whether the point P(10, 15)
# lies inside the triangle formed by
# A(0, 0), B(20, 0) and C(10, 30)
if (is_inside(0, 0, 20, 0, 10, 30, 10, 15)):
    print('Inside')
else:
    print('Not Inside')

# This code is contributed by Danish Raza
if (is_inside(450, 450, 300, 550, 600, 550, 435, 498)):
    print('Inside')
else:
    print('Not Inside')
if (is_inside(650, 450, 500, 550, 800, 550, 435, 498)):
    print('Inside')
else:
    print('Not Inside')
if (is_inside(850, 450, 700, 550, 1000, 550, 435, 498)):
    print('Inside')
else:
    print('Not Inside')

list = []

for i in range(500, 800):
    for j in range(450, 551):
        if is_inside(650, 450,500, 550,800, 550, i, j):
            list.append([i, j])
print(list)
if is_inside(850, 450, 700, 550, 1000, 550, 850, 450):
    print('Inside')
else:
    print('Not Inside')

# to Print Rectangle all possible points
points = get_edge_points(850, 450, 700, 550, 1000, 550)
print(len(points))

# Initialing land
land_min_x = 100
land_max_x = 310
land_min_y = 400
land_max_y = 480

land = [[row, col] for row in range(land_min_y, land_max_y) for col in range(land_min_x, land_max_x)]
# myMap.set_land(land)
def show_land():
    width = land_max_y - land_min_y
    height = land_max_x - land_min_x
    # pygame.draw.rect(screen, COLOR_LAND, (land_min_x, land_min_y, width, height))
