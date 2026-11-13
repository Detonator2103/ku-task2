import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graph import GraphError, build_graph, find_cycles
from graph_file import read_graph_file

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load(name):
    return read_graph_file(os.path.join(DATA_DIR, name)).get


class GraphTest(unittest.TestCase):

    def test_diamond_bfs_order(self):
        graph = build_graph("A", load("diamond.txt"))
        self.assertEqual(list(graph), ["A", "B", "C", "D"])
        self.assertEqual(graph["A"], ["B", "C"])

    def test_diamond_has_no_cycles(self):
        graph = build_graph("A", load("diamond.txt"))
        self.assertEqual(find_cycles(graph), [])

    def test_simple_cycle(self):
        graph = build_graph("A", load("cycle.txt"))
        self.assertEqual(list(graph), ["A", "B", "C"])
        self.assertEqual(find_cycles(graph), [["A", "B", "C", "A"]])

    def test_many_cycles(self):
        graph = build_graph("A", load("many_cycles.txt"))
        cycles = find_cycles(graph)
        self.assertEqual(
            cycles,
            [["A", "B", "A"], ["C", "C"], ["D", "E", "D"]],
        )

    def test_start_from_middle_of_cycle(self):
        graph = build_graph("B", load("cycle.txt"))
        self.assertEqual(list(graph), ["B", "C", "A"])

    def test_undefined_package_is_leaf(self):
        graph = build_graph("A", load("undefined.txt"))
        self.assertEqual(graph, {"A": ["B"], "B": []})

    def test_unknown_start(self):
        with self.assertRaises(GraphError):
            build_graph("Z", load("diamond.txt"))


if __name__ == "__main__":
    unittest.main()