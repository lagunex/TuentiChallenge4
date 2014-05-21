#!/usr/bin/python

from itertools import repeat

NONE,UP,RIGHT,DOWN,LEFT = -1,0,1,2,3

def h(begin, end):
  '''h((int,int),(int,int)) -> int

     Heuristic base in Manhattan distance
  '''
  return abs(begin[0]-end[0]) + abs(begin[1]-end[1])

def neighbors(matrix, rows, columns, current):
  '''neighbors(matrix, rows, columns, (row,column,direction)) -> iterator

     Return an enumerate object with the two possible neighbors of
     the current node, depending on the direction it is going. At the
     beginning (direction==NONE), all for directions are possible
  '''
  r,c,direction = current
  if direction in (NONE, LEFT, DOWN) and c > 0 and matrix[r][c-1] != '#': 
    yield (r,c-1, LEFT) 
  if direction in (NONE, RIGHT, UP) and c < columns-1 and matrix[r][c+1] != '#':  
    yield (r,c+1, RIGHT)
  if direction in (NONE, UP, LEFT) and r > 0 and matrix[r-1][c] != '#': 
    yield (r-1,c, UP)
  if direction in (NONE, DOWN, RIGHT) and r < rows-1 and matrix[r+1][c] != '#':
    yield (r+1,c, DOWN)

def a_star(matrix, rows, columns, begin, end):
  '''A* algorithm to accelerate the shortest path search
     If we substitute use h(...) == 0 for all values,
     then f_score == g_score and this algorithm becomes Dijkstra
  '''
  g_score = {} # minimum cost so far to read a node
  f_score = {} # future cost estimation to reach a node
  
  # each state is described with its position and direction
  # same position, different direction == different state
  visited = set()
  pending = [(begin[0],begin[1],NONE)]

  g_score[(begin[0],begin[1],NONE)] = 0
  f_score[(begin[0],begin[1],NONE)] = g_score[(begin[0],begin[1],NONE)] + h(begin, end)
  while len(pending) > 0:
    current = min(pending, key=lambda x:f_score[x])
    position = (current[0], current[1])

    if position == end: return g_score[current]
 
    pending.remove(current)
    visited.add(current)
    
    for neighbor in neighbors(matrix, rows, columns, current):
      if neighbor in visited: continue

      tmp_g_score = g_score[current]+1

      if neighbor not in pending or tmp_g_score < g_score[neighbor]:
        position = (neighbor[0], neighbor[1])
        g_score[neighbor] = tmp_g_score
        f_score[neighbor] = g_score[neighbor] + h(position, end)
        if neighbor not in pending: 
          pending.append(neighbor)

  return 'ERROR'

def read_graph():
  '''read_graph() -> matrix, M,N, begin, end

  Reads from standard input and returns
  matrix - road map 
  M,N - columns and rows
  begin - (r0,c0) start position
  end - (r1,c1) end position
  '''
  M,N = map(int,raw_input().split(' '))
  matrix = []
  begin = (0,0)
  end = (0,0)
  
  for r in range(N):
    row_line = raw_input()
    if 'S' in row_line: begin = (r,row_line.index('S'))
    if 'X' in row_line: end = (r,row_line.index('X'))
    matrix.append(row_line)

  return matrix,M,N,begin,end

if __name__ == '__main__':
  cases = int(raw_input())

  for case in range(1,cases+1):
    matrix, columns, rows, begin, end = read_graph()
    print 'Case #%d: %s' % (case,str(a_star(matrix, rows, columns, begin, end)))

