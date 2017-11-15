#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU
'''
This file makes the flux scaled PI image of SU Aur of various sigma.
The goal is to determine what parameters (e.g. sigma) can reveal more features
related to different parts of the circumstellar disk (i.e. inner region, extended material, etc.)
The optimum scales determined are
obj_PI_fs: vmin=0.4, vmax=2, sigma=0.8
obj_PI_fs_conv: vmin=-7.4, vmax=-5
'''
from pylab import*
import pyfits
from scipy.ndimage.filters import gaussian_filter

a0=pyfits.open('obj_PI_a.fits')
obj_PI_a=a0[0].data
a0.close()

a1=pyfits.open('obj_PI_fs.fits')
obj_PI_fs=a1[0].data
a1.close()

a2=pyfits.open('obj_PI_fs_conv_sigma08.fits')
obj_PI_fs_conv=a2[0].data
a2.close()

#rough estimate of object's center
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

figure(0)
clf()
imshow(log10(obj_PI_fs),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=0.4,vmax=2,extent=extent_PI)
title('obj_PI_fs_vmin=0.4_vmax=2')
colorbar()

delta=0.1
z=arange(-7.5,-6.4,delta,dtype=float) #from -7.5 to -6.4 in increments of 0.1
vmax=-5
sigma=0.8
j=1
for i in z:
  vmin=i
  obj_PI_fs_conv=gaussian_filter(obj_PI_fs,sigma=sigma)
  fname='obj_PI_conv_sigma='+str(sigma)+'_vmin='+str(vmin)+'_vmax='+str(vmax)
  figure(j)
  j=j+1
  clf()
#subplot(121)
#interpolation prevents default smoothing
  imshow(log10(obj_PI_fs_conv),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax,extent=extent_PI)
#colorbar()
  title(fname)
  show()
'''
#save
pyfits.writeto(fname1,PI_obj_conv_a)
pyfits.writeto(fname2,PI_obj_conv_b)
pyfits.writeto(fname3,PI_obj_conv_c)
pyfits.writeto(fname4,PI_obj_conv_d)
'''
