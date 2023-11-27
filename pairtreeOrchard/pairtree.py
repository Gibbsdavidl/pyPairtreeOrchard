

import random as rand
from itertools import combinations

from pairtreeOrchard import node

class pairtree:

  id = None     # tree identifier
  root = None   # the root node
  target = None # the column in df to predict
  pairs = None  # list of variable pairs
  depth = None  # height of the tree
  df = None

  def __init__(self, id, df, target, nvars, depth):
    self.id = id
    self.target = target
    self.depth = depth
    # select K number of RANDOM variables
    vars = [ci for ci in df.columns if ci != 't']
    randvars = rand.sample(vars, k=nvars)
    # create pair list
    self.pairs = list(combinations(randvars, 2))
    # hang on to the dataframe
    self.df=df

  def grow(self):
    self.root = node.node(self.id + 1, self.target)
    self.root.grow(0, self.depth, self.pairs, self.df)
    return(None)