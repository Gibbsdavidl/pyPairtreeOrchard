
import numpy as np

class node:

  id = None      # node ID number
  mode = None    # node or leaf
  target = None
  targetSet = None
  varL = None    # column name on left side of expression
  varR = None    # column name on right side of expression
  targetL = None # pandas series to left
  targetR = None # pandas series to right
  idxL = None
  idxR = None
  left = None    # node to the left
  right = None   # node to the right
  parent = None  # parent node
  gini = None

  def __init__(self, id, target):
    self.id = id
    self.target = target

  def print(self):
    print("node: "+ str(self.id))
    print("mode: "+ str(self.mode))
    print("target: " + str(self.target))
    print("varL: "+ str(self.varL))
    print("varR: "+ str(self.varR))

  def giniFold(self, xs):
    val = 1
    for x in xs:
      val -= x
    return(val)

  def gini(self, splitL, splitR):
    # gini = 1 - p1^2 - p2^2 where p1 is probability of target[0] in array
    symbols1 = splitL.unique()
    symbols2 = splitR.unique()
    ps1 = [pow( sum(si == splitL)/len(splitL), 2) for si in symbols1]
    ps2 = [pow( sum(si == splitR)/len(splitR), 2) for si in symbols2]
    gini1 = self.giniFold(ps1)
    gini2 = self.giniFold(ps2)
    return(gini1 + gini2)

  def split(self, df):
    self.idxL = df[self.varL] <= df[self.varR]
    self.targetL = df.loc[self.idxL, self.target]
    self.idxR = df[self.varL] > df[self.varR]
    self.targetR = df.loc[self.idxR, self.target]
    return( )

  def search(self, pairs, df):
    giniScores = np.array([])
    for i, pi in enumerate(pairs):
      self.varL = pi[0]
      self.varR = pi[1]
      self.split(df)
      giniScores = np.append(giniScores,  self.gini(self.targetL, self.targetR))
    # winning pair with min gini impurity #
    idx = np.argmin(giniScores)
    self.gini = giniScores[idx]
    self.varL = pairs[idx][0]
    self.varR = pairs[idx][1]
    self.split(df)
    shortPairs = [pi for pi in pairs if pi != pairs[idx]]
    return( shortPairs )

  def grow(self, currDepth, maxDepth, pairs, df):
    print("grow currDepth: " + str(currDepth))
    print("df: " + str(df.shape))
    print("len pairs: " + str(len(pairs)))
    print("cols df: " + str(df.columns))
    if ( (currDepth > maxDepth) or
     (len(pairs) == 0) or
     (len(df.loc[:,self.target].unique()) == 1) ):
      self.mode = 'leaf'
      self.targetSet = df.loc[:,self.target]
      print("leaf id: " + str(self.id))
      print("currDepth: " + str(currDepth))
      self.print()
      return()
    else:
      print("in node, curr depth " + str(currDepth))
      self.mode = 'node'
      newPairs = self.search(pairs, df)
      self.growL(currDepth, maxDepth, newPairs, df)
      self.growR(currDepth, maxDepth, newPairs, df)

  def growL (self, currDepth, maxDepth, pairs, df):
      print("grow Left")
      print("idxL: " + str(self.idxL))
      self.left = node(self.id+1, self.target)
      self.left.parent = self
      self.left.print()
      self.left.grow(currDepth+1, maxDepth, pairs, df.loc[self.idxL,:])

  def growR (self, currDepth, maxDepth, pairs, df):
      print("grow Right")
      print("idxR: " + str(self.idxR))
      self.right = node(self.id+1, self.target)
      self.right.parent = self
      self.right.print()
      self.right.grow(currDepth+1, maxDepth, pairs, df.loc[self.idxR,:])

