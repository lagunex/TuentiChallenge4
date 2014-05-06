#!/usr/bin/python

import math

N = int(raw_input())
for n in range(N):
  (x,y) = [int(i) for i in raw_input().split(' ')]
  z = math.sqrt(x**2 + y**2)
  z = ("%.2f" % z).rstrip('.0')
  print z
