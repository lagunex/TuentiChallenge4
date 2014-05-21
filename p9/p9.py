#!/usr/bin/python
'''
The key for solving the problem was in the sentence.
  "When you begin the calculations, the roads are already full"

This means that the cars will be coming in all the time. And we assume
infinite cars coming out of our city.

Then the problem is equivalent to a Maximum Flow problem and the 
Ford Fulkerson algorithm solve this problem if the capacities are
integer (and they are)

Wikipedia offers a nice Python implementation of Ford-Fulkerson,
I made a variation in find_path to use BFS instead of DFS

Ford-Fulkerson with DFS is O(Ef) and with BFS is O(VE^2)
Because the flow values are in thousands, I chose BFS
'''
from edmondskarp import * # use the Wikipedia impl of Ford-Fulkerson

cities = int(raw_input())
r = 0
for c in range(cities):
  g = FlowNetwork()
  
  city_name = raw_input()
  normal_speed, dirt_speed = map(int,raw_input().split(' '))
  speeds = {'normal': normal_speed, 'dirt': dirt_speed} # a dict for easier access
  intersections, roads = map(int,raw_input().split(' '))

  for r in range(roads):
    node_from, node_to, road_type, lanes = raw_input().split(' ')

    # do not add a node twice
    if not node_from in g.get_vertex(): g.add_vertex(node_from)
    if not node_to in g.get_vertex(): g.add_vertex(node_to)

    # speeds[road_type] - if a road has a speed of X km/h, it cannot be 
    #                     longer than X km because a car in one edge will not 
    #                     be able to enter the city in time
    # int(lanes) - each lane can hold a queue of cards
    # 200 = 1000m / 5m - the number of cars that can be lined up in one km
    #                    5m is the length of each car (4m + 1m space in-between)
    capacity = speeds[road_type]*int(lanes)*200
    g.add_edge(r, node_from, node_to, capacity)
  
  #g.add_vertex('__source__')
  #g.add_vertex('__sink__')
  #r += 1
  #g.add_edge(r,'__source__',city_name,999999)
  #r += 1
  #g.add_edge(r,'AwesomeVille','__sink__',999999)
  print city_name, g.max_flow(city_name,'AwesomeVille')
