#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU/flux_scaling/PA_diskmajoraxis
'''
This file generates the radial PI distribution along PA=15 and 195 (major axis)
The radial PI distribution is generated by plotting the normalized flux as
a function of radius (from boundary of mask to r~80 AU).
The goal is to acquire the power index of the radial distribution.
This is done by fitting a power function (resembling a straight line)
in a log log plot. 
There is some problem regarding what conv sigma of image to use because it yields different power indices. For consistency, use sigma=2.
Export new_rscale and image_ave.txt and use them for plotting and
getting the power index in excel.
'''
from pylab import *
import pyfits
from scipy.ndimage.interpolation import rotate
import numpy as np
from matplotlib.patches import Ellipse
cmap=cm.jet
cmap.set_bad('black',1)

#z=pyfits.open('obj_PI_fs_conv_sigma08.fits')
#z=pyfits.open('obj_PI_fs_conv_sig1.fits')
z=pyfits.open('obj_PI_fs_conv_sig2.fits')
obj_PI_fs_conv=z[0].data-1.1e-7
z.close()

#define image center
xcenter=271
ycenter=318

#crop image; 401x401
#obj_PI_fs_conv_cropped=obj_PI_fs_conv[ycenter-200:ycenter+201,xcenter-200:xcenter+201]
obj_PI_fs_conv_cropped=obj_PI_fs_conv[ycenter-300:ycenter+301,xcenter-270:xcenter+271]

figure(0)
clf()
extent=array([-200,200,-200,200])
imshow(log10(obj_PI_fs_conv_cropped),interpolation='nearest',origin='lower',cmap=cm.jet,extent=extent,vmin=-7.4,vmax=-5)
plot([0,0], [-200, 200], color='r', linestyle='--', linewidth=1)
title('PA=0')

##scale the axes in AU; make array with 400 elements and subtract 200: [-200,-199,..199,200]*AU conversion factor
rscale=arange(401)-200*9.53e-3*140

angle=90
rotated_image=rotate(obj_PI_fs_conv_cropped,angle)
dim=rotated_image.shape[0]
midpoint   =dim/2

extent_PI=array([-midpoint,midpoint,-midpoint,midpoint])

figure(1)
clf()
imshow(log10(rotated_image),extent=extent_PI,vmin=-7.4,vmax=-5,cmap=cmap)
plot([0,0], [-midpoint, midpoint], color='r', linestyle='--', linewidth=1)
axis([-150,150,-150,150])
title('P.A.= %d deg.' % angle)

figure(2)
clf()
scale=9.53e-3*140
#get the average of of flux along the vertical (PA=15) +-2 pixels (5 columns) to increase SNR
image1=rotated_image[midpoint:,midpoint+1]*scale
image2=rotated_image[midpoint:,midpoint-1]*scale
image3=rotated_image[midpoint:,midpoint+2]*scale
image4=rotated_image[midpoint:,midpoint-2]*scale
image5=rotated_image[midpoint:,midpoint]*scale
image_ave=(image1+image2+image3+image4+image5)/5

#new_rscale=log((arange(rotated_image.shape[0])-midpoint)*scale)
new_rscale=(arange(rotated_image.shape[0])-midpoint)*scale
#get only the positive values of flux; midpoint>=0
new_rscale=new_rscale[midpoint:]

#fit a power law with exponent p=-1
power_law_m1= 1e-4 * new_rscale[10:] ** -1
power_law_m2= 0.29 * new_rscale[10:] ** -3.2
loglog(new_rscale,image_ave,'k-') # before
#log log plot of power law 
loglog(new_rscale[10:],power_law_m1,'b--',label='p= -1')
loglog(new_rscale[10:],power_law_m2,'g--',label='p= -3.2')
#plot([0,0], [5e-8, 3e-5], color='r', linestyle='--', linewidth=1) #this is a vertical line along the origin
#31 pixels correspond to the radius of the mask

#plot the point marking the boundary of the mask, before of which the flux is unreliable
loglog(31*scale,image_ave[31], 'ro',label='mask boundary (20 AU)')
#loglog(60*scale,image_ave[60], 'ro',label='fitting boundary (80.1 AU)') 
loglog(65*scale,image_ave[65], 'ro',label='fitting boundary (86.7 AU)') #for PA=15
#plot(31*scale,image_ave[((len(rotated_image)/2)+31)], 'ro') #this corresponds to point in linear scale
axis([30,150,5e-9,3e-5]) #zoom in
ylabel('n_PI / n*')
xlabel('log(r) (AU)')
title('Power law index: -3.2')
legend(loc='upper right', shadow=True)

#Takami+13 used 0."3 arcsec in diameter mask
#0."3 arcsec/*0.00948arcsec/pix = 31.65 pixels
hmask,wmask= 30*scale,30*scale
m=Ellipse(xy=(0,0),height=hmask,width=wmask)
figure(0).add_subplot(111).add_artist(m)
figure(1).add_subplot(111).add_artist(m)
m.set_color('k')
show()

#numpy.savetxt('',)
