#!/usr/bin/env python
from pylab import *
from pyraf import iraf
import glob
import pyfits

#ch2: 
ch2_x=0.7
ch2_y=0.3
#ch3: 
ch3_x=-0.1
ch3_y=0.3
#ch4: 
ch4_x=0.2
ch4_y=0.5

file_list=glob.glob('HICA*_ch1bfg.fits')
file_list=list(file_list)
file_list.sort()

for filename_tmp in file_list:
  filename_org=filename_tmp[:-12]
  filename_ch1=filename_org+'_ch1bfg'
  filename_ch2=filename_org+'_ch2bfg'
  filename_ch3=filename_org+'_ch3bfg'
  filename_ch4=filename_org+'_ch4bfg'
  print "\n", filename_ch1,filename_ch2,filename_ch3,filename_ch4

  iraf.imshift(filename_ch3,'shiftxy3',ch3_x,ch3_y)
#O:(ch1+ch3)  
  out_ch1ch3=filename_ch1[9:-7]+'_ch1ch3.fits'
  iraf.imarith(filename_ch1,'+','shiftxy3',out_ch1ch3)
  iraf.imdel('shiftxy3')

  iraf.imshift(filename_ch2,'shiftxy2',ch2_x,ch2_y)
  iraf.imshift(filename_ch4,'shiftxy4',ch4_x,ch4_y)
#E: (ch2+ch4)
  shiftxy2='shiftxy2.fits'
  out_ch2ch4=filename_ch1[9:-7]+'_ch2ch4.fits'
  iraf.imarith(shiftxy2,'+','shiftxy4',out_ch2ch4)
  iraf.imdel('shiftxy2')
  iraf.imdel('shiftxy4')
  iraf.imdel('out_ch1ch3')
  iraf.imdel('out_ch2ch4')

#OE rays: (ch1+ch3) - (ch2+ch4)
  oe=filename_ch1[9:-7]+'_oe.fits' #retrive only the image number (e.g. 240_oe)

  iraf.imshift(out_ch1ch3,'out_ch1ch3',0,0)
  iraf.imshift(out_ch2ch4,'out_ch2ch4',0,0)
  iraf.imarith(out_ch1ch3,'-','out_ch2ch4',oe)

#I: (ch1+ch3) + (ch2+ch4)
  I=filename_ch1[9:-7]+'_I'
  iraf.imarith(out_ch1ch3,'+','out_ch2ch4',I)
