#
# Author :
# ID :
#
#
# Revisions:
#
#

import math


# Calculating Manhattan Distance from Scratch
# https://datagy.io/manhattan-distance-python/
def manhattan_distance(point1, point2):
    return sum(abs(value1 - value2) for value1, value2 in zip(point1, point2))


# A utility function to calculate area
# of triangle formed by (x1, y1),
# (x2, y2) and (x3, y3)

def area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1)
                + x3 * (y1 - y2)) / 2.0)


# https://www.geeksforgeeks.org/check-whether-a-given-point-lies-inside-a-triangle-or-not/
# A function to check whether point P(x, y)
# lies inside the triangle formed by
# A(x1, y1), B(x2, y2) and C(x3, y3)
def is_inside(x1, y1, x2, y2, x3, y3, x, y):
    # Calculate area of triangle ABC
    A = area(x1, y1, x2, y2, x3, y3)

    # Calculate area of triangle PBC
    A1 = area(x, y, x2, y2, x3, y3)

    # Calculate area of triangle PAC
    A2 = area(x1, y1, x, y, x3, y3)

    # Calculate area of triangle PAB
    A3 = area(x1, y1, x2, y2, x, y)

    # Check if sum of A1, A2 and A3
    # is same as A
    if (A == A1 + A2 + A3):
        return True
    else:
        return False


def is_outside(x1, y1, x2, y2, x3, y3, x, y):
    return not is_inside(x1, y1, x2, y2, x3, y3, x, y)


def is_edge(x1, y1, x2, y2, x3, y3, x, y):
    # Calculate area of triangle ABC
    A = area(x1, y1, x2, y2, x3, y3)

    # Calculate area of triangle PBC
    A1 = area(x, y, x2, y2, x3, y3)

    # Calculate area of triangle PAC
    A2 = area(x1, y1, x, y, x3, y3)

    # Calculate area of triangle PAB
    A3 = area(x1, y1, x2, y2, x, y)

    # Check if sum of A1, A2 and A3
    # is same as A
    if A == A1 + A2 + A3 and A1 * A2 * A3 == 0:
        return True
    else:
        return False


def get_edge_points(x1, y1, x2, y2, x3, y3):
    points = []
    x_min = min(x1, x2, x3)
    x_max = max(x1, x2, x3)
    y_min = min(y1, y2, y3)
    y_max = max(y1, y2, y3)
    for x in range(x_min, x_max+1):
        for y in range(y_min, y_max+1):
            if is_edge(x1, y1, x2, y2, x3, y3, x, y):
                points.append([x, y])
    return points
