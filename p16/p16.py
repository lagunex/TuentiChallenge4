#!/usr/bin/python
  
import sys
from operator import attrgetter
from math import sqrt
  
class Event():
  '''An event is a moment in space where we can start to consider
     (or stop considering, depending on the event category) collisions 
     with a given point
  '''
  IN,OUT = 0,1 # in-event is zero to make it < out-event
  def __init__(self, point, category):
    self.category = category
    self.point = point
    self.x = point[0]
    if self.category == Event.IN: # we begin considering collisions at this x-coord
      self.x -= point[2]
    else: # we stop considering collisions at this x-coord
      self.x += point[2]

if __name__ == '__main__':
  first,total = map(int,raw_input().split(','))
  point_report = open(sys.argv[1])

  # skip lines
  for i in range(first-1):
    point_report.readline()
  
  events = [] # we will sweep the x-coordinates using the events

  # read next total points
  for i in range(total):
    (x,y,r) = map(int,point_report.readline().split())

    # each point creates two events, to begin and stop considering collisions
    events.append(Event((x,y,r), Event.IN))  
    events.append(Event((x,y,r), Event.OUT)) 

  # sort events according to their x-value
  # for same x, first in-events
  events.sort(key=attrgetter('x','category'))
  
  collisions = 0
  points = [] # all possible points that could collide in a given time

  for e in events:
    if e.category == Event.IN: 
      # check if e.point collides with any of the possible points
      for p in points:
        distance = sqrt((p[0]-e.point[0])**2+(p[1]-e.point[1])**2)
        if distance < p[2]+e.point[2]: collisions += 1

      # e.point may collide with future near points
      points.append(e.point) 

    else: 
      points.remove(e.point) # e.point is to far away to keep colliding

  print collisions
