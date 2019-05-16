#! /usr/bin/python

import sys
from datetime import datetime

filename = sys.argv[1]
file = open(filename, 'r')

times = []
for line in file:
  line = list(filter(lambda l: l, line.split(' ')))
  year = 2000 + int(line[3][0:2])
  month = int(line[3][2:4])
  day = int(line[3][4:6])
  hour = int(line[4][0:2])
  minute = int(line[4][2:4])
  if 1 <= month <= 12:
    times.append(datetime(year, month, day, hour, minute))

if len(times) > 0:
  print(str(times[0].year) + "01010000")
  print(str(times[0].year) + "12312230")
  print(str(times[-1].year) + "01010000")
  print(str(times[-1].year) + "12312230")