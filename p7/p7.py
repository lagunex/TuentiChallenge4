#!/usr/bin/python
  
import sys
  
class UnionFind():
  def __init__(self):
    self.unions = {} # contains nodes' partitions
  
  def find(self, node0):
    '''self.find(int) -> int
    returns the union that contains node0
    '''
    if not node0 in self.unions:
      self.unions[node0] = node0 # initially, all nodes are in their own union
    else:
      # iterate over all joined unions until we get to the root
      while node0 != self.unions[node0]:
        # optimize self.unions structure by transitivity
        # if A->B and B->C, then A->C
        parent = self.unions[node0]
        self.unions[node0] = self.unions[parent] # child now points to grandpa
        node0 = parent
    return node0
  
  def same_union(self, node0, node1):
    '''self.same_union(int, int)
    returns True if node0 and node1 are in same union
    '''
    return self.find(node0) == self.find(node1)
  
  def union(self, node0, node1):
    '''self.union(int, int) -> self
    join the paritions of node0 and node1 together
    '''
    if not self.same_union(node0, node1):
      union0 = self.find(node0)
      union1 = self.find(node1)
      self.unions[union0] = union1
    return self
  
def obtain_connection(terroristA, terroristB, filename):
  '''obtain_connection(int,int,str) -> str
  Iterates over the phone calls registered in filename and
  return the index of the call that connected terroristA and terroristB

  To solve this problem, we use a union_find structure
  that is built one line at a time to try to avoid processing the
  whole file

  The return value is indicates the index found (if there was one)
  '''
  call_logs = open(filename)
  union_find = UnionFind()
  connection = 'Not connected'
  for (index, call) in enumerate(call_logs):
    (begin, end) = [int(x) for x in call.split(' ')]
    union_find.union(begin, end)
    if union_find.same_union(terroristA, terroristB):
      connection = 'Connected at %d' % index 
      break
  return connection
  
if __name__ == '__main__':
  terroristA = int(raw_input())
  terroristB = int(raw_input())
  print obtain_connection(terroristA, terroristB, sys.argv[1])
  
