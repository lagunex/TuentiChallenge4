#!/usr/bin/python

def add_node(node, graph):
  '''add_node(str, dict) -> add the node to the graph 
                            and compute its transitions
  '''
  if not node in graph: graph[node] = set()

  # compute valid transitions
  for other_node in graph:
    if other_node == node: continue

    # diff('ACB','AXB') = [0,1,0]
    diff = [int(x!=y) for (x,y) in zip(node, other_node)] 
    if sum(diff) == 1: # a transition is valid if only one nucleotid is changed
      graph[node].add(other_node)
      graph[other_node].add(node)
  return node

def bfs(begin, end, graph):
  '''bfs(str, str, dict) -> list

  Returns the shortest path between between begin and end.
  It is computed using breadth first search
  '''
  queue = []
  visited = set()
  previous = {}

  queue.append(begin)
  visited.add(begin)
  previous[begin] = None
  
  # BFS Algorithm
  found = False
  while len(queue) > 0 and not found:
    node_from = queue.pop(0)
    neighbors = graph[node_from]
    for node_to in neighbors:
      if not node_to in visited:
        queue.append(node_to)
        visited.add(node_to)
        previous[node_to] = node_from
        if node_to == end:
          found = True
          break

  # Backtrack to obtain shortest path
  path = [end]
  node = end
  while previous[node] != None:
    path.append(previous[node])
    node = previous[node]

  path.reverse() # Reverse the stack to get the order right
  return path

if __name__ == '__main__':
  begin = ''
  end = ''
  graph = {}

  try:
    begin = add_node(raw_input(), graph)
    end = add_node(raw_input(), graph)
    while True: add_node(raw_input(), graph)
  except EOFError: pass # Reach end of input

  path = bfs(begin,end,graph)
  print '->'.join(path)
