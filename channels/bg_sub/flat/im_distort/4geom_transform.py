#!/usr/bin/env python
from pylab import *
from pyraf import iraf
import pyfits
import glob

file_list1=glob.glob('HICA*ch1bf.fits')
file_list2=glob.glob('HICA*ch2bf.fits')
file_list3=glob.glob('HICA*ch3bf.fits')
file_list4=glob.glob('HICA*ch4bf.fits')

file_list1=list(file_list1)
file_list2=list(file_list2)
file_list3=list(file_list3)
file_list4=list(file_list4)

file_list1.sort()
file_list2.sort()
file_list3.sort()
file_list4.sort()


for filename1 in file_list1:
  fname1=filename1[:-5]+'g.fits'
  iraf.geotran(filename1,fname1,database='ch1_2014Jan.db',transfor='ch1_2014Jan.dat')

for filename2 in file_list2:
  fname2=filename2[:-5]+'g.fits'
  iraf.geotran(filename2,fname2,database='ch2_2014Jan.db',transfor='ch2_2014Jan.dat')

for filename3 in file_list3:
  fname3=filename3[:-5]+'g.fits'
  iraf.geotran(filename3,fname3,database='ch3_2014Jan.db',transfor='ch3_2014Jan.dat')

for filename4 in file_list4:
  fname4=filename4[:-5]+'g.fits'
  iraf.geotran(filename4,fname4,database='ch4_2014Jan.db',transfor='ch4_2014Jan.dat')

#iraf.geotran('HICA00137132_ch1bf','HICA00137132_ch1bfg',database='ch1_2014Jan.db',transfor='ch1_2014Jan.dat')

