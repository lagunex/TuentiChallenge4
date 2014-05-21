#!/usr/bin/python

from math import sqrt

def compute_dijkstra(dijkstra, current, graph):
  '''compute_dijkstra(dijkstra, str, graph)

     dijkstra - dictionary without the key current
     current - starting node for dijkstra algorithm
     graph - graph[begin][end] != 0 if the edge exists

     Returns: 
     for destination in graph.keys() if current->destination is reachable
       dijkstra[current][destination]['d'] -> minimum distance
       dijkstra[current][destination]['p'] -> minimum path
  '''
  previous = {current: None}
  distance = {current:0} 
  nodes = routes.keys()

  while nodes:
    # pop the minimum node to relax
    min_node = None
    for node in nodes:
      if node in distance and \
          (min_node is None or distance[node] < distance[min_node]):
        min_node = node
    if min_node is None: break

    nodes.remove(min_node)
    current_weight = distance[min_node]

    # update distances
    for edge in routes[min_node]:
      weight = current_weight+routes[min_node][edge]
      if edge not in distance or weight < distance[edge]:
        distance[edge] = weight
        previous[edge] = min_node
  
  # build paths
  for destination in previous:
    if current not in dijkstra: dijkstra[current] = {}
    dijkstra[current][destination] = {'d':distance[destination], \
                                      'p':[destination]}
    node = destination
    while previous[node] is not None:
      node = previous[node]
      dijkstra[current][destination]['p'].append(node)

def maximum(station, routes, dijkstra, before, current, fuel, \
            previous_score, current_wagon):
  '''maximum(station, routes, dijkstra, before, current, fuel, 
             previous_score, current_wagon)

     Recursive function that backtracks all possible roads and returns
     the maximum score possible.

     station - description of each station with its current wagons
     routes - (readonly) graph for this routes
     dijkstra - minimum distance and path for each station in this route
                it is filled during recursion
     before - station I came from
     current - station I am in now
     fuel - fuel left
     previous_score - score achieved so far
     current_wagon - wagon I came with
  '''
  if fuel < 0.0: return previous_score # can't go further

  if current_wagon is not None:
    if current_wagon['n'] == current:
      previous_score += current_wagon['v'] # reach destination
    else:
      station[current]['w'].append(current_wagon) # (1) deposit to iterate later

  # dijkstra information is used to prune the recursion from this station
  if current not in dijkstra: compute_dijkstra(dijkstra, current, routes)

  max_score = previous_score
  for neighbor in routes[current]:
    if routes[current][neighbor] > fuel: continue # can't reach, don't go

    if (neighbor != before or current_wagon is not None) and \
           routes[current][neighbor] <= fuel: # go with empty train
      new_score = maximum(station, routes, dijkstra, current, neighbor, \
                          fuel-routes[current][neighbor], previous_score, None)
      max_score = max(new_score, max_score) # improve so far

    for idx,w in enumerate(station[current]['w']): # go with a wagon 
      if neighbor == before and w == current_wagon: continue # do not reverse
      if w['n'] not in dijkstra[current]: continue # don't belong to this route
      if neighbor not in dijkstra[current][w['n']]['p']: continue # not getting closer
      if dijkstra[current][w['n']]['d'] > fuel: continue # can't reach, don't go

      station[current]['w'].pop(idx) # (2) move w to neighbor station
      new_score = maximum(station, routes, dijkstra, current, neighbor, \
                          fuel-routes[current][neighbor], previous_score, w)
      station[current]['w'].insert(idx,w) # backtrack (2)

      max_score = max(new_score, max_score) # improve so far

  if current_wagon in station[current]['w']: 
    station[current]['w'].remove(current_wagon) # backtrack (1)

  return max_score

if __name__ == '__main__':  
  N = int(raw_input())
  for i in range(N):
    S,R,F = map(int,raw_input().split(','))
    station = {}

    # read stations
    for j in range(S):
      name,xy,d,v = raw_input().split(' ')
      (x,y) = map(int,xy.split(','))
      v = int(v)
      # station = {station_name: {"xy": (x,y) coordinates, 
      #                           "w": list of wagons parked}}
      # wagon = {"n": destination name, "n": wagon value}
      station[name] = {'xy': (x,y), 'w': [{'n':d,'v':v}]}

    total = 0
    for k in range(R):
      info = raw_input().split(' ') # A A-B B-C
      # read route
      start = info[0]
      routes = {} # routes[begin][end] = distance for connection begin-end
      for c in info[1:]:
        (c0,c1) = c.split('-')
        if c0 not in routes: routes[c0] = {}
        routes[c0][c1] = sqrt((station[c0]['xy'][0]-station[c1]['xy'][0])**2+\
                              (station[c0]['xy'][1]-station[c1]['xy'][1])**2)
        if c1 not in routes: routes[c1] = {}
        routes[c1][c0] = routes[c0][c1] # undirected graph
      
      # solve route
      # - begin the recursion going from "nowhere" to start
      #   with the start wagon and complete fuel
      wagon = station[start]['w'].pop()
      this_route = maximum(station, routes, {}, None, start, F, 0, wagon)
      total += this_route
    print total
