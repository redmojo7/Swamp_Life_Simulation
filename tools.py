#
# Author :
# ID :
#
#
# Revisions:
#
#


# Calculating Manhattan Distance from Scratch
# https://datagy.io/manhattan-distance-python/
def manhattan_distance(point1, point2):
    return sum(abs(value1 - value2) for value1, value2 in zip(point1, point2))
