#!/usr/bin/env python
'''
This file is just used to change (optimize parameters)
to reveal more features associated with the extended material.
Comparison is done visually by plotting.
'''
from pylab import*
import pyfits
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage.filters import gaussian_laplace

a1=pyfits.open('obj_medQ.fits')
Q_obj=a1[0].data
a1.close()

a2=pyfits.open('obj_medU.fits')
U_obj=a2[0].data
a2.close()

PI_obj=sqrt(U_obj**2+Q_obj**2)
#convolution smoothens the image
PI_obj_convolved1=gaussian_filter(PI_obj,sigma=2.42)
PI_obj_convolved2=gaussian_filter(PI_obj,sigma=2)

vmin1=0
vmax1=2.62
vmin2=0
vmax2=2.5

#rough estimate of object's center
xcenter_obj=270
ycenter_obj=320

pix_scale=0.00948 #HiCIAO pixel scale (arcsec/pix)
#place plot origin to center of object
a=0-xcenter_obj
b=640-xcenter_obj
c=0-ycenter_obj
d=640-ycenter_obj
#convert pix to arcsec
extent_PI=array([a*pix_scale,b*pix_scale,c*pix_scale,d*pix_scale])
#convert arcsec to AU; distance of object is 140 pc
extent_PI*=140 

xzoommin=150
xzoommax=500
yzoommin=100
yzoommax=450

figure(1)
clf()
subplot(121)
#imshow(PI_obj[xzoommin:xzoommax,yzoommin:yzoommax],interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax)

imshow(log10(PI_obj_convolved1),interpolation='nearest',origin='lower',cmap=cm.spectral,vmin=vmin1,vmax=vmax1,extent=extent_PI)
colorbar()

subplot(122)
#log scale
imshow(log10(PI_obj_convolved2),interpolation='nearest',origin='lower',cmap=cm.spectral,vmin=vmin1,vmax=vmax2,extent=extent_PI)
colorbar()
title('PI_convolved_log_obj')
#xlabel("AU")
#ylabel("AU")
show()
