#!/usr/bin/python

from itertools import repeat

distance = {}
previous = {}

def swap(current_table,i,di):
  new_table = list(current_table) # make a copy
  new_table[i], new_table[i+di] = new_table[i+di], new_table[i]
  return ''.join(new_table) # return as a string

def neighbors(current_table):
  for index in range(len(current_table)):
    row,column = index/3,index%3
    if column > 0: yield swap(current_table, index, -1)
    if column < 2: yield swap(current_table, index, 1)
    if row > 0: yield swap(current_table, index, -3)
    if row < 2: yield swap(current_table, index, +3)

def bfs():
  distance['012345678'] = 0
  previous['012345678'] = None
  queue = ['012345678']
  while len(queue) > 0:
    elem = queue.pop(0)
    for n in neighbors(elem):
      if n not in distance:
        queue.append(n)
        distance[n] = distance[elem]+1
        previous[n] = elem

def read_organized_table(inverse_index):
  desired_order = []
  rows, columns = 3, 3
  for row in range(rows):
    names = raw_input().split(', ')
    for column in range(columns):
      desired_order.append(inverse_index[names[column]])
  return ''.join(desired_order)

def read_current_table():
  inverse_index = {}
  rows = 3
  cur_index = 0
  for r in range(rows):
    names = raw_input().split(', ')
    for name in names:
      inverse_index[name] = str(cur_index)
      cur_index += 1
  return inverse_index

if __name__ == '__main__':
  bfs()
  cases = int(raw_input())

  for case in range(cases):
    raw_input() # blank line
    inverse_index = read_current_table()
    raw_input() # blank line
    desired_order = read_organized_table(inverse_index)
    node = previous[desired_order]
    print distance[desired_order]

