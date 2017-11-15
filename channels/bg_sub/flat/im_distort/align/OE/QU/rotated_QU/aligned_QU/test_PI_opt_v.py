#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU
'''
This file makes the polarized intensity image (PI) of SU Aur of various sigma.
The goal is to determine what parameters (e.g. sigma) can reveal more features
related to different parts of the circumstellar disk (i.e. inner region, extended material, etc.)
Different color scales (spectral,jet,hot,gray) and interpolation/smoothing can be used.
The optimum sigma, vmin/vmax, and color scale must be determined.
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

PI_obj=sqrt(U_obj**2+Q_obj**2)
#convolution smoothens the image

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

#vmin=-10; vmax=80
vmin=0			#!!! CHANGE THIS
vmax=2
xzoommin=-200
xzoommax=200
yzoommin=-200
yzoommax=200

figure(0)
clf()
imshow(PI_obj,interpolation='nearest',origin='lower',cmap=cm.jet,vmin=0,vmax=80,extent=extent_PI)
axis([xzoommin,xzoommax,yzoommin,yzoommax])
title('obj_PI_sigma=1.3_vmin=0_vmax=80')

num=14
delta=0.1		#!!!
sigma=1.3
for i in range(num):
  vmin=vmin+delta
  PI_obj_conv=gaussian_filter(PI_obj,sigma=sigma)
  fname='obj_PI_conv_sigma='+str(sigma)+'_vmin='+str(vmin)+'_vmax=2'
  figure(i+1)
  clf()
#subplot(121)
#interpolation prevents default smoothing
  imshow(log10(PI_obj_conv),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax,extent=extent_PI)
  axis([xzoommin,xzoommax,yzoommin,yzoommax])
#colorbar()
  title(fname)
  show()
'''
figure(2)
clf()
#subplot(122)
imshow(log10(PI_obj_conv_b),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax,extent=extent_PI)
axis([xzoommin,xzoommax,yzoommin,yzoommax])
#colorbar()
title(fname2)

figure(3)
clf()
#subplot(121)
imshow(log10(PI_obj_conv_c),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax,extent=extent_PI)
axis([xzoommin,xzoommax,yzoommin,yzoommax])
#colorbar()
title(fname3)

figure(4)
clf()
#subplot(122)
imshow(log10(PI_obj_conv_d),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax,extent=extent_PI)
axis([xzoommin,xzoommax,yzoommin,yzoommax])
#colorbar()
title(fname4)
xlabel("AU")
ylabel("AU")
show()

figure(5)
clf()
#subplot(121)
imshow(log10(PI_obj_conv_e),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax,extent=extent_PI)
axis([xzoommin,xzoommax,yzoommin,yzoommax])
#colorbar()
title(fname5)
xlabel("AU")
ylabel("AU")
show()

figure(6)
clf()
#subplot(122)
imshow(log10(PI_obj_conv_f),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax,extent=extent_PI)
axis([xzoommin,xzoommax,yzoommin,yzoommax])
#colorbar()
title(fname6)
xlabel("AU")
ylabel("AU")
show()

#save
pyfits.writeto(fname1,PI_obj_conv_a)
pyfits.writeto(fname2,PI_obj_conv_b)
pyfits.writeto(fname3,PI_obj_conv_c)
pyfits.writeto(fname4,PI_obj_conv_d)
'''
