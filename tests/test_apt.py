import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from apt import (
    AptError,
    get_dependencies,
    parse_depends,
    parse_packages,
    read_index,
)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data",
                         "packages_test.txt")


class AptTest(unittest.TestCase):

    def setUp(self):
        self.packages = parse_packages(read_index(DATA_FILE, True))

    def test_parse_depends(self):
        result = parse_depends("b (>= 1.0), c | d, libx:any")
        self.assertEqual(result, ["b", "c", "libx"])

    def test_dependencies(self):
        result = get_dependencies("a", self.packages)
        self.assertEqual(result, ["b", "c", "libx"])

    def test_no_dependencies(self):
        self.assertEqual(get_dependencies("c", self.packages), [])

    def test_unknown_package(self):
        with self.assertRaises(AptError):
            get_dependencies("zzz", self.packages)

    def test_missing_file(self):
        with self.assertRaises(AptError):
            read_index("no_such_file.txt", True)


if __name__ == "__main__":
    unittest.main()