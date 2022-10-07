import os
import unittest

import numpy as np
import vg
import tools

# A Python program to print all
# permutations of given length
from itertools import combinations


class ManhattanDisTest(unittest.TestCase):
    def test_normal_case(self):
        dis = tools.manhattan_distance([10, 0], [12, 33])
        self.assertEqual(dis, 2 + 33, "incorrect dis")

    def test_negative_case(self):
        dis = tools.manhattan_distance([0, 0], [12, 33])
        self.assertNotEqual(dis, 0, "incorrect negative dis")


class TriangleAreaTestDis(unittest.TestCase):
    def test_normal_case(self):
        area = tools.area(0, 0, 0, 3, 4, 0)
        self.assertEqual(area, 3 * 4 / 2, "incorrect area")

    def test_negative_case(self):
        area = tools.area(0, 0, 0, 8, 9, 0)
        self.assertNotEqual(area, 0, "incorrect negative area")


class TriangleIsInsideTest(unittest.TestCase):
    def test_normal_case(self):
        inside = tools.is_inside(300, 25, 185, 140, 415, 140, 310, 131)
        self.assertTrue(inside, "incorrect")

    def test_negative_case(self):
        inside = tools.is_inside(0, 0, 0, 4, 5, 0, 6, 0)
        self.assertFalse(inside, "incorrect negative")


class TriangleIsEdgeTest(unittest.TestCase):
    def test_normal_case(self):
        edge = tools.is_edge(0, 0, 0, 4, 4, 0, 2, 2)
        self.assertTrue(edge, "incorrect")

    def test_negative_case(self):
        edge = tools.is_edge(0, 0, 0, 4, 5, 0, 1, 1)
        self.assertFalse(edge, "incorrect negative")


class TriangleEdgePointsTest(unittest.TestCase):
    def test_normal_case(self):
        points = tools.get_edge_points(0, 0, 0, 4, 4, 0)
        for p in points:
            print(p)
            # at least one line parallel with the border
            # Get all permutations of length 2
            comb = list(combinations([[0, 0], [0, 4], [4, 0]], 2))
            comb2 = list(combinations([[0, 0], [0, 4], [4, 0]], 1))
            # Print the obtained combinations
            result = False
            for i in comb:
                for j in comb2:
                    p1 = list(i)
                    v1 = np.array([p1[0][0], p1[0][1]]) - np.array([p1[1][0], p1[1][1]])
                    v2 = np.array([p[0], p[1]]) - np.array([j[0][0], j[0][1]])
                    # print(f"v1 = {v1}, v2 = {v2}")
                    result = vg.almost_collinear(v1, v2) or result
            self.assertTrue(result, "incorrect")

    def test_negative_case(self):
        for p in [[1, 1], [3, 3]]:
            print(p)
            # at least one line parallel with the border
            # Get all permutations of length 2
            comb = list(combinations([[0, 0], [0, 4], [4, 0]], 2))
            comb2 = list(combinations([[0, 0], [0, 4], [4, 0]], 1))
            # Print the obtained combinations
            result = False
            for i in comb:
                for j in comb2:
                    p1 = list(i)
                    v1 = np.array([p1[0][0], p1[0][1]]) - np.array([p1[1][0], p1[1][1]])
                    v2 = np.array([p[0], p[1]]) - np.array([j[0][0], j[0][1]])
                    # print(f"v1 = {v1}, v2 = {v2}")
                    result = vg.almost_collinear(v1, v2) or result
            self.assertFalse(result, "incorrect negative")


class TraceTest(unittest.TestCase):
    def test_normal_case(self):
        pox = tools.trace([30, 30], [0, 0], 5)
        origin_dis = tools.manhattan_distance([30, 30], [0, 0])
        now_dis = tools.manhattan_distance([30, 30], pox)
        self.assertLess(now_dis, origin_dis, "incorrect")

    def test_negative_case(self):
        edge = tools.is_edge(0, 0, 0, 4, 5, 0, 1, 1)
        self.assertFalse(edge, "incorrect negative")
