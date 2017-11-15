#!/usr/bin/env python
'''
This file do flux scaling I_flux/stellar_flux of the object.
This is done by first measuring the flux of ND1 using iraf's photometry utility (phot).
The output is obj_medIaf.fits. 
'''
from pylab import *
import pyfits

ND1_flux=1711181 #measured flux using iraf's phot (in the ND1_medI_a.fits.mag.1)
stellar_flux=ND1_flux*20 #measured from iraf's phot and computed based on filter transmission (10%) and time exposure relative to object (30s- twice of ND1)

a=pyfits.open('obj_medI_a.fits')
b=a[0].data
c=b/stellar_flux
c_log=log10(c)
xcenter_obj=271
ycenter_obj=318

scale=9.53e-3*140 #HiCIAO pixel scale (arcsec/pix)
#place plot origin to center of object
a=0-xcenter_obj
b=640-xcenter_obj
c=0-ycenter_obj
d=640-ycenter_obj

#convert pix to arcsec then AU
extent_PI=array([a,b,c,d])*scale
#convert arcsec to AU; distance of object is 140 pc

imshow(c_log,interpolation='nearest',origin='lower',cmap=cm.jet,vmin=0.7,vmax=2.0,extent=extent_PI)
colorbar()

#save
#pyfits.writeto('obj_medIaf.fits',c_log)
