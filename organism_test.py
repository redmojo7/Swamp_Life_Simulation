import numpy as np

from swamp import Duck, Newt
from map import Map

map = Map(50, 50)
map.add_food([20, 20])

duck = Duck([10, 20], map)
for i in range(6):
    duck.step_change()
    print(duck.__str__())

newt = Newt([10, 20], map)
for i in range(6):
    newt.step_change()
    print(newt.__str__())

food_cells = np.zeros((50, 50), dtype=int)

food_cells[10, 10] = 1
food_cells[5, 5] = 1


# if I stand at O(0,0)


def check_neighbour_with_points(points):
    if np.sum(food_cells[0 - points:points+1, 0 - points:points+1]) == 0:
        next_points = points - (points//2)
        check_neighbour_with_points(next_points)
