import unittest

import tools
from swamp import Duck, Shrimp, Newt


class ManhattanDisTest(unittest.TestCase):
    duck = Duck([20, 20])
    duck.set_attributes(7, "egg", 10, 30)

    def test_move_to_target(self):
        print(f"{self.duck}")
        target = [50, 50]
        x, y = self.duck.x, self.duck.y
        self.duck.move_to_target(target)
        x2, y2 = self.duck.x, self.duck.y
        origin_dis = tools.manhattan_distance(target, [x, y])
        now_dis = tools.manhattan_distance(target, [x2, y2])
        self.assertLess(now_dis, origin_dis, "incorrect")

    def test_move_away_from(self):
        print(f"{self.duck}")
        target = [10, 10]
        x, y = self.duck.x, self.duck.y
        self.duck.move_away_from(target)
        x2, y2 = self.duck.x, self.duck.y
        print(f"duck moved from position ({x},{y}) to position: "
              f"({x2},{y2}) with velocity {self.duck.velocity} ")
        origin_dis = tools.manhattan_distance(target, [x, y])
        now_dis = tools.manhattan_distance(target, [x2, y2])
        self.assertGreater(now_dis, origin_dis, "incorrect")

    def test_random_run(self):
        print(f"{self.duck}")
        x, y = self.duck.x, self.duck.y
        self.duck.random_run()
        x2, y2 = self.duck.x, self.duck.y
        print(f"duck moved from position ({x},{y}) to position: "
              f"({x2},{y2}) with velocity {self.duck.velocity} ")
        dis = tools.manhattan_distance([x2, y2], [x, y])
        self.assertLess(dis, self.duck.velocity, "incorrect")

    def test_search_nearst_target(self):
        print(f"{self.duck}")
        pos_list = [[0, 0], [1, 1], [20, 26], [22, 23]]
        x, y = self.duck.x, self.duck.y
        pos = self.duck.search_nearst_target(pos_list)
        self.assertEqual(pos, [22, 23], "incorrect")

    def test_under_one_step(self):
        print(f"{self.duck}")
        pos = [20, 30]
        x, y = self.duck.x, self.duck.y
        result = self.duck.under_one_step(pos)
        self.assertTrue(result, "incorrect")
        dis = tools.manhattan_distance(pos, [x, y])
        self.assertLessEqual(dis, self.duck.velocity, "incorrect")
