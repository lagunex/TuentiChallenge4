#!/usr/bin/python

from itertools import repeat

def h(current_table, desired_position, strong):
  rows, columns = 3,3
  distance = 0
  for (index,seat) in enumerate(current_table):
    (seat_row, seat_column) = (index / rows, index % columns)
    (desired_row, desired_column) = desired_position[seat]
    if strong:
      distance += abs(seat_row - desired_row) + abs(seat_column - desired_column)
    else:
      distance += int((index/rows,index%columns) != desired_position[seat])
  return distance

def pop_minimum(pending, f_score):
  return minimum_elem

def get_candidate(current_table,i,di):
  new_table = list(current_table)
  new_table[i], new_table[i+di] = new_table[i+di], new_table[i]
  return new_table

def neighbors(current_table):
  for index in range(len(current_table)):
    row,column = index/3,index%3
    if column > 0: yield get_candidate(current_table, index, -1)
    if column < 2: yield get_candidate(current_table, index, 1)
    if row > 0: yield get_candidate(current_table, index, -3)
    if row < 2: yield get_candidate(current_table, index, +3)

def a_star(current_table, desired_position, desired_order, strong, cost):
  desired_key = str(desired_order)

  g_score = {}
  f_score = {}
  
  visited = set()
  pending = [current_table]
  current_key = str(current_table)

  g_score[current_key] = 0
  f_score[current_key] = g_score[current_key] + h(current_table, desired_position, strong)
  while len(pending) > 0:
    current_table = min(pending, key=lambda x: f_score[str(x)])
    current_key = str(current_table)
    if current_key == desired_key: break

    pending.remove(current_table)
    visited.add(current_key)
    
    for neighbor in neighbors(current_table):
      neighbor_key = str(neighbor)
      
      if neighbor_key in visited: continue

      tmp_g_score = g_score[current_key]+1
      if not neighbor in pending or tmp_g_score < g_score[neighbor_key]:
        g_score[neighbor_key] = tmp_g_score
        w = 1
        if not strong and g_score[neighbor_key] <= cost: w = (1+(1-g_score[neighbor_key]/cost))
        f_score[neighbor_key] = g_score[neighbor_key] + w*h(neighbor, desired_position, strong)
        if not neighbor in pending: pending.append(neighbor)

  if desired_key in g_score: return g_score[desired_key]
  else: return -1

def read_organized_table(inverse_index):
  desired_position = {}
  desired_order = []
  rows, columns = 3, 3
  for row in range(rows):
    names = raw_input().split(', ')
    for column in range(columns):
      desired_position[inverse_index[names[column]]] = (row, column)
      desired_order.append(inverse_index[names[column]])
  return (desired_position,desired_order)

def read_current_table():
  inverse_index = {}
  current_table = []
  rows = 3
  cur_index = 0
  for r in range(rows):
    names = raw_input().split(', ')
    for name in names:
      inverse_index[name] = cur_index
      current_table.append(cur_index)
      cur_index += 1
  return (inverse_index, current_table)

if __name__ == '__main__':
  cases = int(raw_input())

  for case in range(cases):
    raw_input() # blank line
    inverse_index, current_table = read_current_table()
    raw_input() # blank line
    desired_position, desired_order = read_organized_table(inverse_index)
    cost = a_star(current_table, desired_position, desired_order, True, 999999.0)
    print min(cost,a_star(current_table, desired_position, desired_order, False, float(cost)))

