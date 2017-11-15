#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU/flux_scaling/PA_diskmajoraxis
'''
This file measures the 1D flux (vertical profile at the image center) at a given position ang (0-180) and plots the flux on a log scale compared with the all the other fluxes.
The image is rotated at various position angles (PA's) to see at 
which PA has the widest flux broadening profile which corresponds to the major axis
of the disk.
'''
from pylab import *
import pyfits
from scipy.ndimage.interpolation import rotate
import numpy as np

#z=pyfits.open('obj_PI_fs_conv_sig1.fits') 
z=pyfits.open('obj_PI_fs_conv_sigma08.fits')
obj_PI_fs_conv=z[0].data-1.1e-7
z.close()

#define image center
xcenter=271
ycenter=318

#crop image; 401x401
obj_PI_fs_conv_cropped=obj_PI_fs_conv[ycenter-200:ycenter+201,xcenter-200:xcenter+201]

figure(0)
clf()
extent=array([-200,200,-200,200])
imshow(log10(obj_PI_fs_conv_cropped),interpolation='nearest',origin='lower',cmap=cm.jet,extent=extent,vmin=-7.4,vmax=-5)
plot([0,0], [-200, 200], color='r', linestyle='--', linewidth=1)
title('PA=0')

##scale the axes in AU; make array with 400 elements and subtract 200: [-200,-199,..199,200]*AU conversion factor
rscale=arange(401)-200*9.53e-3*140
'''
figure(1)
clf()
semilogy(rscale,obj_PI_fs_conv_cropped[200,:],label='horizontal')
semilogy(rscale,obj_PI_fs_conv_cropped[:,200],label='vertical')
title('PA=0')
ylabel('Flux (normalized)')
xlabel('pixel position')
legend(loc='upper right', shadow=True)
'''

profile ={}
midpoint={}
image   ={}
profile[0]  =obj_PI_fs_conv_cropped[:,200]
midpoint[0] =200
image[0]    =obj_PI_fs_conv_cropped

angles=arange(0,181,10)
for i in angles:
  rotated_image=rotate(obj_PI_fs_conv_cropped,i)
  dim=rotated_image.shape[0]
  midpoint[i]   =dim/2
  profile[i]    =rotated_image[:,midpoint[i]]
  image[i]      =rotated_image

ion()
for i in range(0,181,10):
  extent_PI=array([-midpoint[i],midpoint[i],-midpoint[i],midpoint[i]])
  figure(0)
  clf()
  imshow(log10(image[i]),extent=extent_PI,vmin=-7.4,vmax=-5)
  plot([0,0], [-midpoint[i], midpoint[i]], color='r', linestyle='--', linewidth=1)
  axis([-150,150,-150,150])
  title('P.A.= %d deg.' % i)
  figure(1)
  clf()
  for ii in range(0,181,10):
    new_rscale=(arange(profile[ii].shape[0])-midpoint[ii])*9.53e-3*140
    semilogy(new_rscale,profile[ii],'c-')
  new_rscale=(arange(profile[i].shape[0])-midpoint[i])*9.53e-3*140
  semilogy(new_rscale,profile[i],'k-')
  axis([-100,100,5e-8,3e-5])
  title('P.A.= %d deg.' % i)
  show()
  raw_input()

#flux line broadening: 160
