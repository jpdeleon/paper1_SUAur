#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU/flux_scaling/PA_diskmajoraxis
'''
This file measures the 1D flux (vertical profile along the tail) at 15au<r<250au and plots the flux on a log scale compared with the all the other fluxes.
The width of the flux profile broadening above a given threshold of PI/I* corresponds to the width of the tail associated with the disk.
'''
from pylab import *
import pyfits
import numpy as np
from matplotlib.patches import Ellipse
cmap=cm.jet
cmap.set_bad('black',1)

#z=pyfits.open('obj_PI_fs_conv_sig01.fits')
z=pyfits.open('obj_PI_fs_conv_sig02.fits')
obj_PI_fs_conv=z[0].data-1.1e-7
z.close()

scale=9.53e-3*140
#define image center
xcenter=271
ycenter=318
mask_radius=15 #pixels
disk_radius=65 #of major axis in pixels


#crop image; 401x401
#obj_PI_fs_conv_cropped=obj_PI_fs_conv[ycenter-270:ycenter+271,xcenter-270:xcenter+271]

dim=obj_PI_fs_conv.shape[0]
midpoint=dim/2

ion()
profile = {}
rscale_pix=((arange(dim))-(dim-xcenter))
rscale_shifted=rscale_pix+((dim-xcenter)-xcenter)
rscale_AU=rscale_shifted*scale

n=70 #pixels above and below midpoint that will be extracted for plotting
hscale_AU=(arange(2*n)-n)*scale
extent=array([-271,368,-n,n])*scale

start=(xcenter+disk_radius)
end=dim
tail_len=arange(0,end-start,15) 			#end pixel - mask radius in pixels

for i in tail_len:
  profile[i]=obj_PI_fs_conv[:,start+i]
  profile[i]=profile[i][ycenter-n:ycenter+n] 		#get only n pixels above and below midpoint 
for i in tail_len:
  figure(1)
  clf()
  for j in tail_len: 					#plot first all profiles
    plot(hscale_AU,profile[j],'c-')
  #then plot current profile
  plot(hscale_AU,profile[i],'k-')
  plot([-300,300], [1e-7, 1e-7], color='r', linestyle='--', linewidth=1)	#superpose one chosen profile
  plot([-300,300], [0, 0], color='r', linestyle='--', linewidth=1)		#mark a line along which flux=0
  axis([-200,200,-0.2e-6,0.2e-6])			#zoom in to tail
  xlabel('r (AU)')					#r refers to distance above or below PA=270 deg
  ylabel('PI / I*')
  title('r= %d + %d pixel (%.1f AU)' % (disk_radius,i,i+(disk_radius)*scale))
  figure(0)
  clf()
  imshow(log10(obj_PI_fs_conv),interpolation='nearest',origin='lower',vmin=-7.4,vmax=-5,extent=extent, cmap=cmap)
  axis([-200,360,-150,150])
  plot([disk_radius+i,disk_radius+i], [-100, 100], color='r', linestyle='--', linewidth=1)
  plot([340,340], [-100, 100], color='r', linestyle='--', linewidth=1)
  xlabel('AU')
  ylabel('AU')
  hmask,wmask= 30*scale,30*scale 			#radius = 15 pix = 20 AU
  m=Ellipse(xy=(0,0),height=hmask,width=wmask)
  figure(0).add_subplot(111).add_artist(m)
  m.set_color('k')
  show()
  raw_input()
'''
# add flux of the tail along cross-wise
for n tail_len:
  for o in range(len(profile[n])):
    if profile[p]>0:
    sum(profile[])
'''
