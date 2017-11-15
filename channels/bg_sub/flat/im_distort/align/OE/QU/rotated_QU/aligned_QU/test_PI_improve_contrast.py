#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU
#ur_setup
#ipython -pylab
#run test_PI
'''
This file is just used to change (optimize parameters)
to reveal more features associated with the extended material.
Comparison is done visually by plotting.
'''
from pylab import*
import pyfits
from scipy.ndimage.filters import gaussian_filter

#sigma=3

#obj
#a1=pyfits.open('obj_PI.fits')
#obj_PI=a1[0].data
#a1.close()

a2=pyfits.open('obj_PI_a.fits')
obj_PI_a=a2[0].data
a2.close()

#a3=pyfits.open('obj_PI_convolved.fits')
#obj_PI_convolved=a3[0].data
#a3.close()

a4=pyfits.open('obj_PI_convolved_a.fits')
obj_PI_convolved_a=a4[0].data
a4.close()
'''
#ref
b1=pyfits.open('ref_PI.fits')
ref_PI=b1[0].data
b1.close()

b2=pyfits.open('ref_PI_a.fits')
ref_PI_a=b2[0].data
b2.close()

b3=pyfits.open('ref_PI_convolved.fits')
ref_PI_convolved=b3[0].data
b3.close()

b4=pyfits.open('ref_PI_convolved_a.fits')
ref_PI_convolved_a=b4[0].data
b4.close()

#ND1
c1=pyfits.open('ND1_PI.fits')
ND1_PI=c1[0].data
c1.close()

c2=pyfits.open('ND1_PI_a.fits')
ND1_PI_a=c2[0].data
c2.close()

c3=pyfits.open('ND1_PI_convolved.fits')
ND1_PI_convolved=c3[0].data
c3.close()

c4=pyfits.open('ND1_PI_convolved_a.fits')
ND1_PI_convolved_a=c4[0].data
c4.close()
'''
vmin=-10
vmax=80
#vmin=0
#vmax=2.62

yzoommin=-200
yzoommax=200
xzoommin=-200
xzoommax=200
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

figure(1)
clf()
##obj
subplot(121)
imshow(obj_PI_a,interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax,extent=extent_PI)
colorbar()
axis([xzoommin,xzoommax,yzoommin,yzoommax])
subplot(122)
imshow(obj_PI_convolved_a,interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax,extent=extent_PI)
axis([xzoommin,xzoommax,yzoommin,yzoommax])
colorbar()

figure(2)
subplot(111)
imshow(obj_PI_a,interpolation='nearest',origin='lower',cmap=cm.jet,vmin=vmin,vmax=vmax,extent=extent_PI)
axis([-200,200,-200,200])
colorbar()
show()
