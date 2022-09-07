#
# Author : Peng CAI
# ID : 21053409
#
# map.py - Class definitions for map
#
# Revisions:
#
# no
#

class Map:
    livings = []
    foods = []

    def __init__(self, width=500, height=500):
        # by default, map are 500*500
        self.width = width
        self.height = height

    def __str__(self):
        return f"Map {self.width}*{self.height} with {len(self.livings)} livings and {len(self.foods)} foods."

    def add_food(self, foods):
        self.foods = foods

'''
    def add_livings(self, livings):
        self.livings = livings
'''
