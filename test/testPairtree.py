import unittest

import pandas as pd
import random as rand
import numpy as np
from itertools import combinations

from pairtreeOrchard import pairtree
class MyTestCase(unittest.TestCase):
    def test_something(self):
        df = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6],
                           'b': [4, 5, 6, 7, 7, 8],
                           'c': [9, 8, 7, 6, 5, 4],
                           'd': [8, 4, 3, 2, 3, 4],
                           'e': [5, 3, 3, 4, 2, 3],
                           'f': [8, 7, 7, 1, 1, 2],
                           't': [0, 0, 1, 1, 1, 0]})
        # make a tree
        t1 = pairtree.pairtree(id=1, df=df, target='t', nvars=3, depth=3).grow()
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
