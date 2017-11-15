#!/usr/bin/env python
'''
last edit: aug16
This file makes the polarized intensity image (PI) of SU Aur
and its convolved counter part of a given sigma.
It does this by first importing medQa and medUa (aligned 2nd time) and then 
computing PI=sqrt(obj_medQ**2+obj_medU**2).
Different sigma and v scales are used to increase the contrast and reveal the somewhat extended structure (tail) in the final image. There are two output images (PI and PI_conv) per set (obj_?, ref_?, ND1_?).
The optimum sigma=2, vmin=-7.4, vmax=-5 for log was determined.

The output obj_PI_a_fs_conv_sig02.fits will be used for drawing polvec in 
12PI_fs_conv_polvec.py. Copy the outputs in the flux_scaling folder.
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
obj_PI_fs_conv=gaussian_filter(obj_PI_fs,sigma=2)

#rough estimate of object's center; but after rotation and alignment, it is defined as such
xcenter_obj=271
ycenter_obj=318

#convert pix to arcsec to AU; distance of object is 140 pc
scale=9.53e-3*140 #HiCIAO pixel scale (arcsec/pix)

#place plot origin to center of object
a=0-xcenter_obj
b=640-xcenter_obj
c=0-ycenter_obj
d=640-ycenter_obj
#convert pix to arcsec
extent_PI=array([a,b,c,d])*scale

#vmin=-10 #use this if objPI is not log10
#vmax=80
#vmin=0.4 #use this for obj_PI_fs
#vmax=2
#vmin=-7 #use this for obj_PI_fs_conv
#vmax=-5

xzoommin=-200
xzoommax=200
yzoommin=-200
yzoommax=200

figure(1)
clf()
subplot(221)
#interpolation prevents default smoothing
imshow(Q_obj,interpolation='nearest',origin='lower',cmap=cm.gray,vmin=-200,vmax=200,extent=extent_PI)
title('obj_Qa')
colorbar()
axis([xzoommin,xzoommax,yzoommin,yzoommax])

subplot(222)
imshow(U_obj,interpolation='nearest',origin='lower',cmap=cm.gray,vmin=-200,vmax=200,extent=extent_PI)
title('obj_Ua')
colorbar()
axis([xzoommin,xzoommax,yzoommin,yzoommax])

subplot(223)
imshow(log10(obj_PI_fs),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=-7.4,vmax=-5,extent=extent_PI)
colorbar()
title('obj_PI_fs_log')
xlabel("AU")
ylabel("AU")
axis([xzoommin,xzoommax,yzoommin,yzoommax])

subplot(224)
#log scale
imshow(log10(obj_PI_fs_conv),interpolation='nearest',origin='lower',vmin=-7.4,vmax=-5,cmap=cm.jet,extent=extent_PI)
colorbar()
title('obj_PI_fs_conv_log')
xlabel("AU")
ylabel("AU")
axis([xzoommin,xzoommax,yzoommin,yzoommax])

#figure(2)
#clf()
#imshow(obj_medI_a,interpolation='nearest',origin='lower',cmap=cm.gray,vmin=0,vmax=80,extent=extent_PI)
show()
#save
#pyfits.writeto('obj_PI_a_fs.fits',obj_PI_fs)
#pyfits.writeto('obj_PI_a_fs_conv_sig02.fits',obj_PI_fs_conv)

'''
###ND1
b1=pyfits.open('ND1_medQa.fits')
Q_ND1=b1[0].data
b1.close()

b2=pyfits.open('ND1_medUa.fits')
U_ND1=b2[0].data
b2.close()

PI_ND1=sqrt(U_ND1**2+Q_ND1**2)
#convolution smoothens the image
PI_ND1_convolved=gaussian_filter(PI_ND1,sigma=5)

figure(2)
clf()
subplot(221)
#interpolation prevents default smoothing
imshow(Q_ND1,interpolation='nearest',origin='lower',cmap=cm.gray,vmin=-vmax,vmax=vmax)
axis([xzoommin:xzoommax,yzoommin:yzoommax])
colorbar()

subplot(222)
imshow(U_ND1,interpolation='nearest',origin='lower',cmap=cm.gray,vmin=-vmax,vmax=vmax)
axis([xzoommin:xzoommax,yzoommin:yzoommax])
colorbar()

subplot(223)
imshow(PI_ND1,interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax)
axis([xzoommin:xzoommax,yzoommin:yzoommax])
colorbar()

subplot(224)
#log scale
imshow(log10(PI_ND1_convolved),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=0.5,vmax=2,extent=extent_PI)
axis([xzoommin:xzoommax,yzoommin:yzoommax])
colorbar()

title('PI_convolved_log_ND1')
xlabel("AU")
ylabel("AU")
show()
#save
pyfits.writeto('ND1_PI_a.fits',PI_ND1)
pyfits.writeto('ND1_PI_convolved_a.fits',PI_ND1_convolved)


###ref
c1=pyfits.open('ref_medQa.fits')
Q_ref=c1[0].data
c1.close()

c2=pyfits.open('ref_medUa.fits')
U_ref=c2[0].data
c2.close()

PI_ref=sqrt(U_ref**2+Q_ref**2)
#convolution smoothens the image
PI_ref_convolved=gaussian_filter(PI_ref,sigma=3)

figure(3)
clf()
subplot(221)
#interpolation prevents default smoothing
imshow(Q_ref,interpolation='nearest',origin='lower',cmap=cm.gray,vmin=-vmax,vmax=vmax)
colorbar()
subplot(222)
imshow(U_ref,interpolation='nearest',origin='lower',cmap=cm.gray,vmin=-vmax,vmax=vmax)
colorbar()
subplot(223)
imshow(PI_ref,interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax)
colorbar()
subplot(224)
#log scale
imshow(log10(PI_ref_convolved),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=0.5,vmax=2,extent=extent_PI)
colorbar()
title('PI_convolved_log_ref')
xlabel("AU")
ylabel("AU")
show()
#save
pyfits.writeto('ref_PI_a.fits',PI_ref)
pyfits.writeto('ref_PI_convolved_a.fits',PI_ref_convolved)
'''
