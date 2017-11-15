#!/usr/bin/env python
'''
This file do flux scaling (i.e. PI_flux/stellar_flux) of the object.
This is done by first measuring the flux of ND1 using iraf's photometry utility (phot).
The output is objPI_conva_fs and obj_PI_a_fs.fits.
Always view output in log10 so (vmin,vmax) range is compressed.
The obj_PI_a_fs are used to make obj_PI_conv_fs_sig?.fits.
optimum vmin,vmax is acquired from test_PI_fs.py
Optimizing sigma is done next in test_PI_opt_sigma.py

You can save obj_PI_a_fs.fits here or do it in 10PI_set.py
The output of 10PI_set.py which is obj_PI_fs_conv_sig02 will
be used as input in 12PI_fs_conv_polvec.
'''
from pylab import *
import pyfits

ND1_flux=1711181 #measured flux using iraf's phot (in the ND1_medI_a.fits.mag.1)
stellar_flux=ND1_flux*20 #measured from iraf's phot and computed based on filter transmission (10%) and time exposure relative to object (30s- twice of ND1)

z1=pyfits.open('obj_PI_conva_sig005.fits')
obj_PI_conv_sig05=z1[0].data
objPIconv_fs_sig05=obj_PI_conv_sig05/stellar_flux
z1.close()

#obj_PI_a
z2=pyfits.open('obj_PI_a.fits')
obj_PI_a=z2[0].data			#uncalibrated
objPIa_fs=obj_PI_a/stellar_flux		#calibrated
z2.close()
'''
z3=pyfits.open('obj_PI_conv_sig2.fits')
obj_PI_conv_sig2=z3[0].data
objPIconv_fs_sig2=obj_PI_conv_sig2/stellar_flux
z3.close()
'''
xcenter_obj=271
ycenter_obj=318
scale=9.53e-3*140

pix_scale=0.00948 #HiCIAO pixel scale (arcsec/pix)
#place plot origin to center of object
a=0-xcenter_obj
b=640-xcenter_obj
c=0-ycenter_obj
d=640-ycenter_obj
#convert pix to arcsec convert arcsec to AU; distance of object is 140 pc
extent_PI=array([a,b,c,d])*scale

xzoommin=-200
xzoommax=200
yzoommin=-200
yzoommax=200

figure(1)
clf()
imshow(log10(obj_PI_a),interpolation='nearest',origin='lower',vmin=0.5,vmax=2.5,extent=extent_PI)
title('obj_PI_a (uncalibrated flux)')
xlabel('AU')
ylabel('AU')
colorbar()
axis([xzoommin,xzoommax,yzoommin,yzoommax])

figure(2)
clf()
imshow(log10(objPIa_fs),interpolation='nearest',origin='lower',vmin=-7,vmax=-5,extent=extent_PI)
title('obj_PI_fs (calibrated flux)')
xlabel('AU')
ylabel('AU')
colorbar()
axis([xzoommin,xzoommax,yzoommin,yzoommax])
show()
'''
figure(3)
clf()
imshow(log10(objPIa_fs),interpolation='nearest',origin='lower',extent=extent_PI)
colorbar()
'''
#save
#pyfits.writeto('obj_PI_a.fits',obj_PI_a)
#pyfits.writeto('obj_PI_a_fs.fits',objPIa_fs)
