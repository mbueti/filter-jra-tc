import sys
from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes
GeoAxes._pcolormesh_patched = Axes.pcolormesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import cartopy.crs as ccrs
import numpy as np
from netCDF4 import Dataset as netcdf
from datetime import datetime
from datetime import timedelta

ufilt_filename = sys.argv[1]
vfilt_filename = sys.argv[2]
u_filename = sys.argv[3]
v_filename = sys.argv[4]
ufield = sys.argv[5]
vfield = sys.argv[6]
to = int(sys.argv[7])
tf = int(sys.argv[8])

ufilt_file = netcdf(ufilt_filename, 'r', format='NETCDF4')
vfilt_file = netcdf(vfilt_filename, 'r', format='NETCDF4')
u_file = netcdf(u_filename, 'r', format='NETCDF4')
v_file = netcdf(v_filename, 'r', format='NETCDF4')
lon = u_file.variables['lon'][:]
lat = u_file.variables['lat'][:]
time = u_file.variables['time'][:]
lons, lats = lons, lats = np.meshgrid(lon, lat)

cmap = plt.cm.RdBu_r
cmap.set_bad((0.2, 0.2, 0.2), 1.)

FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='JRA55do Wind', artist='Mike Bueti')
writer = FFMpegWriter(fps=12, metadata=metadata)

fig = plt.figure(figsize=[12,7], dpi=400)
fig.subplots_adjust(left=0.01, bottom=0, right=0.99, top=0.95, wspace=None, hspace=None)
ax = plt.axes(projection=ccrs.Robinson(central_longitude=-70))

with writer.saving(fig, "wind_diff_frances.mp4", 400):
  for t in range(to, tf):
    print(t)
    U = np.sqrt(u_file.variables[ufield][t, :, :]**2 + v_file.variables[vfield][t, :, :]**2)
    Ufilt = np.sqrt(ufilt_file.variables[ufield][t, :, :]**2 + vfilt_file.variables[vfield][t, :, :]**2)
    dU = U - Ufilt
    dU = np.ma.array(dU, mask=np.isnan(dU))
    p = plt.contourf(lon, lat, dU, np.arange(-25, 26, 1), transform=ccrs.PlateCarree(), cmap=cmap, extend='both')
    plt.contour(lon, lat, dU, np.arange(-25, 30, 5), transform=ccrs.PlateCarree(), extend='both', colors='k', linestyles='dashed', linewidths=1)
    plt.title('JRA55do Filtered Storm - ' + (datetime(1900,1,1) + timedelta(time[t])).strftime("%Y/%m/%d %H:%M"))
    ax.coastlines('10m', color='k')
    plt.clim([-25, 25])
    if 'cbar' not in locals():
      cbar = plt.colorbar(p, orientation='horizontal', extend='both', aspect=40, pad=0.025, ticks=np.arange(-25, 30, 5))
      cbar.set_label('m/s')
    ax.set_extent((-115, -25, -7.5, 37.5), crs=ccrs.PlateCarree())
    writer.grab_frame()
    plt.cla()

plt.close()
del cbar
cmap = plt.cm.jet
cmap.set_bad((0.2, 0.2, 0.2), 1.)
fig = plt.figure(figsize=[12,7], dpi=400)
fig.subplots_adjust(left=0.01, bottom=0, right=0.99, top=0.95, wspace=None, hspace=None)
ax = plt.axes(projection=ccrs.Robinson(central_longitude=-70))
with writer.saving(fig, "wind_frances.mp4", 400):
  for t in range(to, tf):
    print(t)
    U = np.sqrt(u_file.variables[ufield][t, :, :]**2 + v_file.variables[vfield][t, :, :]**2)
    Ufilt = np.sqrt(ufilt_file.variables[ufield][t, :, :]**2 + vfilt_file.variables[vfield][t, :, :]**2)
    # dU = U - Ufilt
    U = np.ma.array(U, mask=np.isnan(U))
    p = plt.contourf(lon, lat, U, np.arange(0,31, 1), transform=ccrs.PlateCarree(), cmap=cmap, extend='both')
    plt.contour(lon, lat, U, np.arange(0, 35, 5), transform=ccrs.PlateCarree(), extend='both', colors='k', linestyles='dashed', linewidths=1)
    plt.title('JRA55do Wind - ' + (datetime(1900,1,1) + timedelta(time[t])).strftime("%Y/%m/%d %H:%M"))
    ax.coastlines('10m', color='k')
    plt.clim([0, 30])
    if 'cbar' not in locals():
      cbar = plt.colorbar(p, orientation='horizontal', extend='both', aspect=40, pad=0.025, ticks=np.arange(-25, 30, 5))
      cbar.set_label('m/s')
    ax.set_extent((-115, -25, -7.5, 37.5), crs=ccrs.PlateCarree())
    writer.grab_frame()
    plt.cla()

plt.close()
del cbar
cmap = plt.cm.jet
cmap.set_bad((0.2, 0.2, 0.2), 1.)
fig = plt.figure(figsize=[12,7], dpi=400)
fig.subplots_adjust(left=0.01, bottom=0, right=0.99, top=0.95, wspace=None, hspace=None)
ax = plt.axes(projection=ccrs.Robinson(central_longitude=-70))
with writer.saving(fig, "wind_filt_frances.mp4", 400):
  for t in range(to, tf):
    print(t)
    U = np.sqrt(u_file.variables[ufield][t, :, :]**2 + v_file.variables[vfield][t, :, :]**2)
    Ufilt = np.sqrt(ufilt_file.variables[ufield][t, :, :]**2 + vfilt_file.variables[vfield][t, :, :]**2)
    # dU = U - Ufilt
    Ufilt = np.ma.array(Ufilt, mask=np.isnan(Ufilt))
    p = plt.contourf(lon, lat, Ufilt, np.arange(0,31, 1), transform=ccrs.PlateCarree(), cmap=cmap, extend='both')
    plt.contour(lon, lat, Ufilt, np.arange(0, 35, 5), transform=ccrs.PlateCarree(), extend='both', colors='k', linestyles='dashed', linewidths=1)
    plt.title('JRA55do Filtered Wind - ' + (datetime(1900,1,1) + timedelta(time[t])).strftime("%Y/%m/%d %H:%M"))
    ax.coastlines('10m', color='k')
    plt.clim([0, 30])
    if 'cbar' not in locals():
      cbar = plt.colorbar(p, orientation='horizontal', extend='both', aspect=40, pad=0.025, ticks=np.arange(-25, 30, 5))
      cbar.set_label('m/s')
    ax.set_extent((-115, -25, -7.5, 37.5), crs=ccrs.PlateCarree())
    writer.grab_frame()
    plt.cla()