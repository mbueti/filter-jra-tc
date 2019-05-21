#! /Users/mbueti/anaconda/envs/python37/bin/python3.7

import sys
import numpy as np
from scipy import signal
from netCDF4 import Dataset
from datetime import datetime
from datetime import timedelta
from matplotlib import pyplot as plt

ufile_name = sys.argv[1]
vfile_name = sys.argv[2]
ufield_name = sys.argv[3]
vfield_name = sys.argv[4]
track_file = sys.argv[5]
ufile = Dataset(ufile_name, 'r+', format='NETCDF4')
vfile = Dataset(vfile_name, 'r+', format='NETCDF4')

b, a = signal.cheby2(6, 10, 1/48, btype='lowpass')
w, h = signal.freqs(b, a)

lon = ufile.variables['lon'][:]
lat = vfile.variables['lat'][:]
time = ufile.variables['time'][:]
ufield = ufile.variables[ufield_name][:]
vfield = vfile.variables[vfield_name][:]
time = [datetime(1900, 1, 1) + timedelta(t) for t in time]

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

# print(time)
# print(track_times)

ti = np.where(fdt == dti[0])[0][0]
tf = np.where(fdt == dti[-1])[0][0]

def calc_weight(x, y, xo, yo, rcls_t, w):
  dx = np.abs(x - xo)
  dy = np.abs(y - yo)
  dl = np.sqrt(dx**2 + dy**2)
  r1 = rcls_t
  r2 = r1 * 1.5
  dr = r2 - r1
  # wo = 34.0 * 0.5144
  wo = 15.0
  if dl <= r1 and w >= wo:
    return 1
  if dl >= r2 or w < wo:
    return 0
  return 1 - (dl - r1) / dr

ufilt_field = signal.filtfilt(b, a, ufield, axis=0)
vfilt_field = signal.filtfilt(b, a, vfield, axis=0)
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
  weights = np.array([[calc_weight(lon[x], lat[y], lon_t, lat_t, rcls_t, np.sqrt(ufield[i,y,x]**2 + vfield[i,y,x]**2)) for x in range(0, len(lon))] for y in range(0, len(lat))])
  ufield[i, :, :] = weights * ufilt_field[i, :, :] + (1 - weights) * ufield[i, :, :]
  vfield[i, :, :] = weights * vfilt_field[i, :, :] + (1 - weights) * vfield[i, :, :]
  ufile.variables[ufield_name][:] = ufield
  vfile.variables[vfield_name][:] = vfield

ufile.sync()
vfile.sync()