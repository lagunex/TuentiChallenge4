#!/usr/bin/python

import sys
from itertools import repeat

def compute_size(track):
  '''compute_size(str) -> (row,column,width,height)
  
  Given a track, compute the position of the first character and
  the track's width and height
 
  ex:
  compute_size('#-\--/---\--/-') -> (0,2,5,3)
  /-#-\
  |   |
  \---/
  '''
  (min_dx, min_dy, max_dx, max_dy) = (0, 0, 0, 0)

  horizontal = True # asume first character horizontal
  forward = True # asume first character going forward
  (dx,dy) = (-1,0) # keeps the current position in the map
                   # dx begins at -1 to make the first character's position 0
                   # dy begins at 0 because the first turn does not count for
                   #    the new direction, hence the first '-' of the new 
                   #   direction will be at position 0
  for char in track:
    if horizontal and forward: dx += 1
    elif horizontal and not forward: dx -= 1
    elif not horizontal and forward: dy += 1
    else: dy -= 1

    min_dx = min(min_dx,dx)
    min_dy = min(min_dy,dy)
    max_dx = max(max_dx,dx)
    max_dy = max(max_dy,dy)

    if char == '/': forward = not forward # left and up means backwards
    if char == '/' or char == '\\': horizontal = not horizontal # change of orientation

  return (0-min_dy, 0-min_dx, max_dx-min_dx+1, max_dy-min_dy+1)

def prettify(track, row, column, width, height):
  '''prettify(str, int, int, int, int) -> returns a 2D representation 
       with size width x height, beginning the track at position (row,column)
  
  ex:
  prettify('#-\-/---\-/-', 0,2,5,3) -> /-#-\
                                       |   |
                                       \---/
  '''
  track_grid = [list(repeat(' ',width)) for i in range(height)] # creates an empty track

  (i,j) = (row,column) # move cursor to first character's position
  orientation = '-' # assume first orientation horizontal
  forward = True # assume first orientation forward
  for char in track:
    # first determine which character is to be set
    cur_char = ' '
    if char == '/' or char == '\\': # change of orientation
      if orientation == '-': orientation = '|'
      else: orientation = '-'
      cur_char = char
    elif char == '-':
      cur_char = orientation
    elif char == '#':
      cur_char = char
    track_grid[i][j] = cur_char

    # then update orientation and direction accordingly
    if char == '/': forward = not forward
    if forward:
      if orientation == '-': j+=1
      else: i+=1
    else:
      if orientation == '-': j-=1
      else: i-=1

  return track_grid

if __name__ == '__main__':
  ''' The algorithm builds the track in two steps
      1) Reads the single-line track to compute its size and
         the position of the first character
      2) Reads it again to prettify using the info computed before
  '''
  for track in sys.stdin:
    if track == '\n': break
    track = track[:-1]

    track_info = compute_size(track)
    track_grid = prettify(track, *track_info)
    for line in track_grid: 
      print ''.join(line)
