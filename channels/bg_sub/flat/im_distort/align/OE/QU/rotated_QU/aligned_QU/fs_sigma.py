#!/usr/bin/env python
'''
This file produces obj_PI_fs_conv of various sigma 
and saves it as fits file.
The output will be used as input for 12PI_pol_vec.py
'''
from pylab import*
import pyfits
from scipy.ndimage.filters import gaussian_filter

a1=pyfits.open('obj_medQa.fits')
Q_obj=a1[0].data
a1.close()

a2=pyfits.open('obj_medUa.fits')
U_obj=a2[0].data
a2.close()

obj_PI=sqrt(U_obj**2+Q_obj**2)

#flux scaling
ND1_flux=1711181 #measured flux using iraf's phot (in the ND1_medI_a.fits.mag.1)
stellar_flux=ND1_flux*20 

obj_PI_fs=obj_PI/stellar_flux

#convolution smoothens the image
obj_PI_fs_conv1=gaussian_filter(obj_PI_fs,sigma=1)
obj_PI_fs_conv15=gaussian_filter(obj_PI_fs,sigma=1.5)
obj_PI_fs_conv2=gaussian_filter(obj_PI_fs,sigma=2)
obj_PI_fs_conv25=gaussian_filter(obj_PI_fs,sigma=2.5)
obj_PI_fs_conv3=gaussian_filter(obj_PI_fs,sigma=3)

#rough estimate of object's center; but after rotation and alignment, it is defined as such
xcenter_obj=271
ycenter_obj=318

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

#vmin=-10 #use this if objPI is not log10
#vmax=80
#vmin=0.4 #use this for obj_PI_fs
#vmax=2
vmin=-7.4 #use this for obj_PI_fs_conv
vmax=-5

figure(1)
clf()
imshow(log10(obj_PI_fs_conv1),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax,extent=extent_PI)
colorbar()
title('obj_PI_fs_conv_sig=1')
xlabel("AU")
ylabel("AU")

figure(2)
clf()
imshow(log10(obj_PI_fs_conv15),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax,extent=extent_PI)
colorbar()
title('obj_PI_fs_conv_sig=1.5')
xlabel("AU")
ylabel("AU")

figure(3)
clf()
imshow(log10(obj_PI_fs_conv2),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax,extent=extent_PI)
colorbar()
title('obj_PI_fs_conv_sig=2')
xlabel("AU")
ylabel("AU")

figure(4)
clf()
imshow(log10(obj_PI_fs_conv25),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax,extent=extent_PI)
colorbar()
title('obj_PI_fs_conv_sig=2.5')
xlabel("AU")
ylabel("AU")

figure(5)
clf()
imshow(log10(obj_PI_fs_conv3),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax,extent=extent_PI)
colorbar()
title('obj_PI_fs_conv_sig=3')
xlabel("AU")
ylabel("AU")
show()

#save
#pyfits.writeto('obj_PI_fs_conv_sig1.fits',obj_PI_fs_conv1)
pyfits.writeto('obj_PI_fs_conv_sig15.fits',obj_PI_fs_conv15)
pyfits.writeto('obj_PI_fs_conv_sig2.fits',obj_PI_fs_conv2)
pyfits.writeto('obj_PI_fs_conv_sig25.fits',obj_PI_fs_conv25)
pyfits.writeto('obj_PI_fs_conv_sig3.fits',obj_PI_fs_conv3)









