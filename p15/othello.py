#!/usr/bin/python

def next_moves(board, cur_player):
  '''Returns an iterator with the possible moves that
     cur_player can make in this turn

     Each move will be represented by the squared played and the
     resulting board
  '''
  directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

  for row in range(len(board)):
    for column in range(len(board)):
      if board[row][column] == '.':
        valid = False
        new_board = list([list(x) for x in board])
        for d in directions:
          if will_flip(new_board, cur_player, (row,column), d):
            flip(new_board, cur_player, (row,column), d)
            valid = True
        if valid: 
          new_board[row][column] = cur_player
          yield (row,column), new_board

def flip(board, cur_player, square, direction):
  '''Flip in-place all squares with cur_player in a given direction'''
  limits = [-1,8]

  board[square[0]][square[1]] = cur_player

  next_square = (square[0]+direction[0],square[1]+direction[1])
  while next_square[0] not in limits and next_square[1] not in limits:
    if board[next_square[0]][next_square[1]] == cur_player: break
    else: board[next_square[0]][next_square[1]] = cur_player
    next_square = (next_square[0]+direction[0],next_square[1]+direction[1])

  return board

def will_flip(board,cur_player,square,direction):
  '''Determines if cur_player in square causes an
     flip in the given direction
  '''
  limits = [-1,8]

  valid = False
  next_square = (square[0]+direction[0],square[1]+direction[1])
  while next_square[0] not in limits and next_square[1] not in limits:
    next_value = board[next_square[0]][next_square[1]]
    if next_value == '.': # can't flip
      valid = False
      break
    elif next_value == cur_player: break # stop fliping
    else: valid = True # continue fliping

    next_square = (next_square[0]+direction[0],next_square[1]+direction[1])

    if next_square[0] in limits or next_square[1] in limits: valid = False
  return valid

def is_valid(board,cur_player,square):
  '''Returns true if the cur_player move at square is valid
     in the given board
  '''
  if board[square[0]][square[1]] != '.': return False
 
  directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
  valid = False
  for d in directions:
    valid = will_flip(board,cur_player,square,d)
    if valid: break
  return valid

