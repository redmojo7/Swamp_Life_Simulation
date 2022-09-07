import numpy as np

from swamp import Duck, Newt
from map import Map

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


enemies = [
    [1, 1],
    [1,2],
    [4,5]
]

x = 5
y = 5

enemy = min([e for e in enemies], key=lambda e: pow(e[0]-x, 2) + pow(e[1]-y, 2))
print(enemy)
