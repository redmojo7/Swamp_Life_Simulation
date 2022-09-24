import unittest
import tools


class TestManhattanDis(unittest.TestCase):
    def runTest(self):
        dis = tools.manhattan_distance([0, 0], [12, 33])
        self.assertEqual(dis, 12+33, "incorrect dis")
