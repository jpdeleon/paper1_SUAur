#!/usr/bin/env python

from pylab import *
import pyfits
import glob

file_list=glob.glob('HICA*')
file_list=list(file_list)
file_list.sort()

for filename in file_list: #subtract the background to all the science images (ch1-ch4)
  a=pyfits.open(filename)
  image=copy(a[0].data)
  a.close()
  for y in range(image.shape[0]):
    med1=median(image[y,:100]) #take the median of y-values from 0:100 (101-499 is omitted because it contains bright star)
    med2=median(image[y,-100:])#take the median of y-values from 500:600
    image[y]-=(med1+med2)*0.5 #bg is subtracted by subtracting the average of the median of pixels along x-values considered above to y-values
    filename=filename.translate(None, '.fits') #remove '.fits' from filename to be appended as 'b.fits'
#figure(1)
#clf()
#imshow(image,vmin=-20,vmax=20)
#show()
  hdu = pyfits.PrimaryHDU(image) #retain header file
  hdulist = pyfits.HDUList([hdu])
  hdulist.writeto(filename+'b.fits') #save as 'HICA*b.fits'
  hdulist.close()

#a[0].data=image
#a.writeto('HICA00137132b_ch1.fits')
#a.close()
