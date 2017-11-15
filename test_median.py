#!/usr/bin/env python

from pylab import *
import pyfits

a=pyfits.open('HICA00137132_ch1.fits')
image=copy(a[0].data)
a.close()

for y in range(image.shape[0]):
  med1=median(image[y,:100])
  med2=median(image[y,-100:])
  image[y]-=(med1+med2)*0.5

#figure(1)
#clf()
#imshow(image,vmin=-20,vmax=20)

#show()

hdu = pyfits.PrimaryHDU(image)
hdulist = pyfits.HDUList([hdu])
hdulist.writeto('HICA00137132b_ch1.fits')
hdulist.close()

#a[0].data=image
#a.writeto('HICA00137132b_ch1.fits')
#a.close()

