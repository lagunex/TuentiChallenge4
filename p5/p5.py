#!/usr/bin/python

SIZE = 8 # board dimension
LIVE_CELL = 'X'
DEAD_CELL = '-'

def compute_neighbors(start_state, position):
  '''compute_neighbots(list, int) -> int

  Return the number of living neighbors of the cell 
  located at the given position
  '''
  row = position / SIZE
  column = position % SIZE
  
  num_neighbors = 0

  if column > 0: num_neighbors += int(start_state[position-1] == LIVE_CELL) # previous column
  if column < SIZE-1: num_neighbors += int(start_state[position+1] == LIVE_CELL) # next column

  if row > 0: # previous row 
    num_neighbors += int(start_state[position-SIZE] == LIVE_CELL)
    if column > 0: num_neighbors += int(start_state[position-SIZE-1] == LIVE_CELL)
    if column < SIZE-1: num_neighbors += int(start_state[position-SIZE+1] == LIVE_CELL)

  if row < SIZE-1: # next row
    num_neighbors += int(start_state[position+SIZE] == LIVE_CELL)
    if column > 0: num_neighbors += int(start_state[position+SIZE-1] == LIVE_CELL)
    if column < SIZE-1: num_neighbors += int(start_state[position+SIZE+1] == LIVE_CELL)

  return num_neighbors

def compute_step(start_state):
  '''compute_step(list) -> list

  Compute a new generation following John Conway's rules of Life
  '''
  end_state = list(start_state) # make a copy of start_state
  for (position, cell) in enumerate(start_state):
    num_neighbors = compute_neighbors(start_state, position)
    if cell == DEAD_CELL and num_neighbors == 3: 
      end_state[position] = LIVE_CELL # new cell borned by reproduction
    elif cell == LIVE_CELL and not num_neighbors in [2,3]: 
      end_state[position] = DEAD_CELL # died for underpopulation or overcrowding
  return end_state

if __name__ == '__main__':
  g0 = []
  for row in range(8): g0 += list(raw_input()) # read the board as a 1D list 

  generations = [g0] # the list of generations computed so far

  first_gen = -1 # first generation in the loop
  period = 0 # loop duration 

  next_gen = g0
  cur_gen = 0
  while period == 0: # no loop found
    next_gen = compute_step(next_gen)
    cur_gen += 1
    try:
      first_gen = generations.index(next_gen)
      period = cur_gen-first_gen # a loop has being found
    except ValueError: pass
    generations.append(next_gen)

  print first_gen, period
