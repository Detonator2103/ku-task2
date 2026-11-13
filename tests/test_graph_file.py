import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graph import GraphError
from graph_file import parse_graph_text, read_graph_file

BROKEN_FILE = os.path.join(os.path.dirname(__file__), "data", "broken.txt")


class GraphFileTest(unittest.TestCase):
    
    def test_parse(self):
        graph = parse_graph_text("A: B C B\nB:\n")
        self.assertEqual(graph, {"A": ["B", "C"], "B": []})

    def test_blank_lines_ignored(self):
        graph = parse_graph_text("\nA: B\n\nB:\n")
        self.assertEqual(list(graph), ["A", "B"])

    def test_bad_line(self):
        with self.assertRaises(GraphError):
            parse_graph_text("A B C")

    def test_lowercase_rejected(self):
        with self.assertRaises(GraphError):
            parse_graph_text("A: b")

    def test_duplicate(self):
        with self.assertRaises(GraphError):
            parse_graph_text("A: B\nA: C")

    def test_broken_file(self):
        with self.assertRaises(GraphError):
            read_graph_file(BROKEN_FILE)

    def test_missing_file(self):
        with self.assertRaises(GraphError):
            read_graph_file("no_such_file.txt")


if __name__ == "__main__":
    unittest.main()