#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU
'''
This file makes the flux-scaled polarized intensity image (PI) of SU Aur of various sigma.
This does this by using onj_PI_fs images then applying convolution of log10(obj_PI_fs) to all possible sigma.
The goal is to determine what parameters (e.g. sigma) can reveal more features
related to different parts of the circumstellar disk (i.e. inner region, extended material, etc.)
Different color scales (spectral,jet,hot,gray), optimum sigma, vmin/vmax, and color scale must be determined.\
save figures manually
make a gif
http://gifmaker.me/

RESULT: sigma=0.5,0.6,0.7,0.8
vmin:0.5,0.6,0.7-2
'''
from pylab import*
import pyfits
from scipy.ndimage.filters import gaussian_filter

#z=pyfits.open('obj_PI_a.fits')
#obj_PI_a=z[0].data
#z.close()
z=pyfits.open('obj_PI_fscaled.fits')
obj_PI_fs=z[0].data
z.close()

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
xzoommin=-200
xzoommax=200
yzoommin=-200
yzoommax=200

figure(0)
clf()
imshow(log(obj_PI_fs),interpolation='nearest',origin='lower',cmap=cm.jet,extent=extent_PI)
axis([xzoommin,xzoommax,yzoommin,yzoommax])
title('obj_PI_fs')

num=30	#change this depending on how many images you want
delta=0.1	#change this
sigma=0		#change this
for i in range(num):
  sigma=sigma+delta
  obj_PI_conv=gaussian_filter(obj_PI_fs,sigma=sigma)
  fname='obj_PI_fs_conv_sigma='+str(sigma)+'.fits'
  figure(i+1)
  clf()
  imshow(log10(obj_PI_conv),interpolation='nearest',origin='lower',cmap=cm.jet,extent=extent_PI)
#  axis([xzoommin,xzoommax,yzoommin,yzoommax])
  colorbar()
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
