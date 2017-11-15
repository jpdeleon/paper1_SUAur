#!/usr/bin/env python
from pylab import *
from pyraf import iraf
import pyfits
import glob

file_list1=glob.glob('HICA*ch1b.fits')
file_list2=glob.glob('HICA*ch2b.fits')
file_list3=glob.glob('HICA*ch3b.fits')
file_list4=glob.glob('HICA*ch4b.fits')

file_list1=list(file_list1)
file_list2=list(file_list2)
file_list3=list(file_list3)
file_list4=list(file_list4)

file_list1.sort()
file_list2.sort()
file_list3.sort()
file_list4.sort()

for filename1 in file_list1: #loop to all the science images (ch1b)
  fname1=filename1[:-5]+'f.fits'
  #print filename1,fname1
  iraf.imarith(filename1,'/','flat_ch1',fname1)#make flat field by dividing flat

for filename2 in file_list2: #loop to all the science images (ch2b)
  fname2=filename2[:-5]+'f.fits'
  #print filename1,fname2
  iraf.imarith(filename2,'/','flat_ch2',fname2)

for filename3 in file_list3: #loop to all the science images (ch3b)
  fname3=filename3[:-5]+'f.fits'
  #print filename1,fname3
  iraf.imarith(filename3,'/','flat_ch3',fname3)

for filename4 in file_list4: #loop to all the science images (ch4b)
  fname4=filename4[:-5]+'f.fits'
  #print filename4,fname4
  iraf.imarith(filename4,'/','flat_ch4',fname4)

 #hdu = pyfits.PrimaryHDU(image1)
 #hdulist = pyfits.HDUList([hdu])
 #hdulist.writeto(fname1+'bf.fits') #make it as 'HICA..ch1bf.fits' instead
 #hdulist.close()
