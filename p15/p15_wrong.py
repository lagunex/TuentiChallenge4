#!/usr/bin/python

from othello import *

def solve(board, player, move, cur_player, cur_move):
  '''If player can force her opponent to lose a corner
     in the given move, it returns the first play to make it happen.
     If player can force the corner, None is returned

     This algorithms performs a backtracking over all possible move
     with the following pruning rules:
     (1) If player found a forced solution to win a corner,
         do not go further
     (2) If the opponent can make a non-forced move to not lose a 
         corner, do not go further
  '''
  solution = None
  
  if cur_move == move and cur_player == player:
    # check if the corner can be taken
    for corner in [(0,0),(0,7),(7,0),(7,7)]:
      if is_valid(board,cur_player,corner):
        solution = corner
        break
  else: # keep recursing
    next_player = 'X'
    if cur_player == 'X': next_player = 'O'
    if cur_player == player: cur_move+=1

    for this_move,next_board in next_moves(board, cur_player):
      is_solution = solve(next_board, player, move, next_player, cur_move)
      # prune (1) player took the corner
      if cur_player == player and is_solution is not None:
        solution = this_move
        break
      # prune (2) opponent did not lose the corner
      elif cur_player != player and is_solution is None:
        solution = is_solution
        break
      # opponent lost the corner, keep looking
      elif cur_player != player:
        solution = this_move

  return solution

if __name__ == '__main__':
  N = int(raw_input())
  for i in range(N):
    player, dummy, move = raw_input().split(' ')
    if player == 'White': player = 'O'
    else: player = 'X'

    board = [] # board[row][column]
    for j in range(8):
      row = []
      row.extend(raw_input())
      board.append(row)

    solution = solve(board, player, int(move), player, 1) # move is str

    if solution is None: print 'Impossible'
    else: print chr(ord('a')+solution[1])+str(solution[0]+1)
