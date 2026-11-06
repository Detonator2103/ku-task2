import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from config import ConfigError, validate_config


def make_config(**changes):
    config = {
        "package_name": "curl",
        "repository_url": "http://example.com/Packages.gz",
        "test_mode": False,
        "output_file": "graph.png",
    }
    config.update(changes)
    return config


class ConfigTest(unittest.TestCase):
    def test_valid(self):
        validate_config(make_config())

    def test_missing_key(self):
        config = make_config()
        del config["package_name"]
        with self.assertRaises(ConfigError):
            validate_config(config)

    def test_bad_package(self):
        with self.assertRaises(ConfigError):
            validate_config(make_config(package_name="Bad Name"))

    def test_bad_mode(self):
        with self.assertRaises(ConfigError):
            validate_config(make_config(test_mode="yes"))

    def test_bad_url(self):
        with self.assertRaises(ConfigError):
            validate_config(make_config(repository_url="ftp://x"))

    def test_missing_test_file(self):
        config = make_config(test_mode=True, repository_url="nope.txt")
        with self.assertRaises(ConfigError):
            validate_config(config)

    def test_bad_extension(self):
        with self.assertRaises(ConfigError):
            validate_config(make_config(output_file="graph.txt"))


if __name__ == "__main__":
    unittest.main()