import sys
import os.path as path
import unittest

# owww ;-(
current_dir = path.dirname(path.realpath(__file__))
sys.path.append(path.join(current_dir, '..'))

import module


class TestTools(unittest.TestCase):
    def test_all(self):
        pass
