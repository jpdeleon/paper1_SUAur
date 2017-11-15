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

#z=pyfits.open('obj_PI_fs_conv_sig1.fits')
z=pyfits.open('obj_PI_fs_conv_sig2.fits')
obj_PI_fs_conv=z[0].data-1.1e-7
z.close()

cmap=cm.jet
cmap.set_bad('black',1)

scale=9.53e-3*140
#define image center
xcenter=271
ycenter=318
mask_radius=15 #pixels
disk_radius=65 #of major axis in pixels

obj_PI_fs_conv_cropped2=obj_PI_fs_conv[ycenter-150:ycenter+150,xcenter-200:xcenter+369]

dimy=obj_PI_fs_conv_cropped2.shape[0]
dimx=obj_PI_fs_conv_cropped2.shape[1]
midpointy=dimy/2
midpointx=dimx/2
extent=array([-midpointx,midpointx+85,-midpointy,midpointy])*scale


ion()
profile = {}
n=120 #pixels above and below midpointy
rscale=(arange(dimx)-midpointx)
rscale=rscale[len(rscale)/2-120:len(rscale)/2+120]*scale #len(rscale)=240
start=midpointx+disk_radius				#349
end=dimx						#569
tail_len=arange(0,end-start,15) 			#0 to 220 in increments of 15

for i in tail_len:
  profile[i]=obj_PI_fs_conv_cropped2[:,start+i]
  profile[i]=profile[i][midpointy-n:midpointy+n] 		#get only n pixels above and below midpoint 
for i in tail_len:
  figure(1)
  clf()
  for j in tail_len: 					#plot first all profiles
    plot(rscale,profile[j],'c-')
  plot(rscale,profile[i],'k-')
  plot([-300,300], [1e-7, 1e-7], color='r', linestyle='--', linewidth=1)	#superpose one chosen profile
  plot([-300,300], [0, 0], color='r', linestyle='--', linewidth=1)		#mark a line along which flux=0
  axis([-200,200,-0.2e-6,0.2e-6])			#zoom in to tail/ axis of profile
  xlabel('r (AU)')					#r refers to distance above or below PA=270 deg
  ylabel('PI / I*')
  title('r= %d + %d pixel (%.1f AU)' % (disk_radius,i,i+(disk_radius)*scale))
  figure(0)
  clf()
  imshow(log10(obj_PI_fs_conv_cropped2),interpolation='nearest',origin='lower',vmin=-7.4,vmax=-5, cmap=cmap,extent=extent)
  plot([disk_radius+i,disk_radius+i], [-100, 100], color='r', linestyle='--', linewidth=1)
  plot([340,340], [-100, 100], color='r', linestyle='--', linewidth=1)
  axis([-380,380,-150,150])				#axis of PI image
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
