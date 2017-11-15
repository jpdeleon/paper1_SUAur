#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU/flux_scaling/PA_diskmajoraxis
'''
This file measures 1D flux (vertical and horizontal) along
a given at the image center for and plots it on a log log plot.
The image is rotated at various position angles (PA's) to see at 
which PA has the largest flux which corresponds the major axis
of the disk.

Criteria for evaluating major axis (boundary) based on flux graphs:
(1) flux curve is oscillating (damped)
(2) flux curve is decreasing fast
(3) double checked with PI graphs
'''
from pylab import *
import pyfits
from scipy.ndimage.interpolation import rotate
import numpy as np

z=pyfits.open('obj_PI_fs_conv_sig1.fits')
obj_PI_fs_conv=z[0].data
z.close()

#define image center
xcenter=271
ycenter=318

#crop image; 401x401
obj_PI_fs_conv_cropped=obj_PI_fs_conv[ycenter-200:ycenter+201,xcenter-200:xcenter+201]

figure(0)
clf()
extent=array([-200,200,-200,200])
imshow(log10(obj_PI_fs_conv_cropped),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=-7.4,vmax=-5,extent=extent)
plot([0,0], [-200, 200], color='r', linestyle='--', linewidth=1)
plot([-200,200], [0, 0], color='r', linestyle='--', linewidth=1)
title('PA=0')

##scale the axes in AU; make array with 400 elements and subtract 200: [-200,-199,..199,200]*AU conversion factor
rscale=arange(401)-200*9.53e-3*140

figure(1)
clf()
##plot logy 1D-flux values along center (cross-hair)
##plot x-values (flux) along y=200 (new center, horizontal)
semilogy(rscale,obj_PI_fs_conv_cropped[200,:],label='horizontal')
##plot y-values (:) along x=200 (new center, vertical)
semilogy(rscale,obj_PI_fs_conv_cropped[:,200],label='vertical')
title('PA=0')
ylabel('Flux (normalized)')
xlabel('pixel position')
legend(loc='upper right', shadow=True)

#angles=range(91)
angles=arange(10,91,10)
for i in angles:
  rotated_image=rotate(obj_PI_fs_conv_cropped,i)
  figure(i)
  clf()
  dim=rotated_image.shape[0]
  midpoint=dim/2
  extent_PI=array([0-midpoint,dim-midpoint,0-midpoint,dim-midpoint])
  imshow(log10(rotated_image),extent=extent_PI)
  plot([0,0], [-midpoint, midpoint], color='r', linestyle='--', linewidth=1)
  plot([-midpoint,midpoint], [0, 0], color='r', linestyle='--', linewidth=1)
  name1='PA='+str(i)
  title(name1)
  new_rscale=(arange(dim)-midpoint)*9.53e-3*140
  figure(i+1)
  clf()
  semilogy(new_rscale,rotated_image[midpoint,:],label='horizontal')
  semilogy(new_rscale,rotated_image[:,midpoint],label='vertical')
  xmax=round(np.max(rotated_image[midpoint,:]),7)
  ymax=round(np.max(rotated_image[:,midpoint]),7)
  name2='PA='+str(i)+';   xmax='+str(xmax)+';   ymax='+str(ymax)
  title(name2)
  ylabel('Flux (normalized)')
  xlabel('pixel position')
  legend(loc='upper right', shadow=True)
  show()
#0 - -113-9=122

#10- -47-115=162

#20- -87-64=151

#25- -46-25=71 minimum (visual)

#30- -58-45=103

#40- -41-77=118

#50- -85-98=183

#60- -81-107=188 maximum

#70- -82-91=178

#80- -85-90=175 

#85- -90-93=183 2nd max (visual)

#90- -75-96=171

#95- - 82-86=168
