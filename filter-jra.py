#! /Users/mbueti/anaconda/envs/python37/bin/python3.7

import sys
import pandas
import numpy as np
from scipy import signal
from netCDF4 import Dataset
from datetime import datetime
from datetime import timedelta
from matplotlib import pyplot as plt

file_name1 = sys.argv[1]
file_name2 = sys.argv[2]
field_name = sys.argv[3]
track_file = sys.argv[4]
file1 = Dataset(file_name1, 'r+', format='NETCDF4')
file2 = Dataset(file_name2, 'r+', format='NETCDF4')

b, a = signal.cheby2(6, 80, 1/48, btype='lowpass')
w, h = signal.freqs(b, a)

lon = file1.variables['lon'][:]
lat = file1.variables['lat'][:]
time = file1.variables['time'][:]
field = file1.variables[field_name][:]
time = [datetime(1900, 1, 1) + timedelta(t) for t in time]

if file_name1 != file_name2:
  field2 = file2.variables[field_name][:]
  field = np.concatenate((field, field2), axis=0)
  time2 = file2.variables['time'][:]
  time2 = [datetime(1900, 1, 1) + timedelta(t) for t in time2]
  time = np.concatenate((time, time2), axis=0)

time_diff = lambda x, y: (x - y).days + (x - y).seconds / (24*3600)

track = open(track_file, 'r')
track_times = []
track_lons = []
track_lats = []
track_rcls = []
for line in track:
  line = list(filter(lambda l: l, line.split(' ')))
  lat_o = float(line[5][0:-1]) / 10
  if line[5][-1] == 'S':
    lat_o *= -1
  lon_o = float(line[6][0:-1]) / 10
  if line[6][-1] == 'W':
    lon_o *= -1
  year = 2000 + int(line[3][0:2])
  month = int(line[3][2:4])
  day = int(line[3][4:6])
  hour = int(line[4][0:2])
  minute = int(line[4][2:4])
  current_time = datetime(year, month, day, hour, minute)
  rcls = float(line[11]) / 111.111
  track_times.append(current_time)
  track_lons.append(lon_o)
  track_lats.append(lat_o)
  track_rcls.append(rcls)

dt = [time_diff(t, track_times[0]) for t in track_times]
dti = np.arange(dt[0], dt[-1], 1/8)
track_lons = np.interp(dti, dt, track_lons)
track_lats = np.interp(dti, dt, track_lats)
track_rcls = np.interp(dti, dt, track_rcls)
fdt = [time_diff(t, track_times[0]) for t in time]

print(time)
print(track_times)

ti = np.where(fdt == dti[0])[0][0]
tf = np.where(fdt == dti[-1])[0][0]

def calc_weight(x, y, xo, yo, rcls_t):
  dx = np.abs(x - xo)
  dy = np.abs(y - yo)
  dl = np.sqrt(dx**2 + dy**2)
  r1 = rcls_t
  r2 = r1 * 2.0
  dr = r2 - r1
  if dl <= r1:
    return 1
  if dl >= r2:
    return 0
  return 1 - (dl - r1) / dr


filt_field = signal.filtfilt(b, a, field, axis=0)
for i in range(ti, tf + 1):
  t = fdt[i]
  print(time[i])
  tt = np.where(dti == t)
  if len(tt) > 0:
    tt = tt[0][0]
  else:
    break
  lon_t = track_lons[tt]
  if lon_t < 0:
    lon_t += 360
  lat_t = track_lats[tt]
  rcls_t = track_rcls[tt]
  weights = np.array([[calc_weight(x, y, lon_t, lat_t, rcls_t * 2) for x in lon] for y in lat])
  field[i, :, :] = weights * filt_field[i, :, :] + (1 - weights) * field[i, :, :]
  if file_name1 != file_name2:
    td = len(time) - len(time2)
    file1.variables[field_name][:] = field[0:dt, :, :]
    file2.variables[field_name][:] = field[dt:-1, :, :]
  else:
    file1.variables[field_name][:] = field

file1.sync()
if file_name1 != file_name2:
  file2.sync()