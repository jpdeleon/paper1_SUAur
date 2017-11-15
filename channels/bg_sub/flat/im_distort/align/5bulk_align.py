#!/usr/bin/env python
'''
This file is used to check whether shifting in x and y of channels 2 to 4 with respect to channel 1
will yield good results. This is done by doing <imarith channel 1 - shifted channel2,3,4>.
In other words, their PSF is aligned and then subtracted.
The output is image_num_ch2,3,4 (e.g. 240_ch2.fits) which can be viewed using ds9.
The image shows good alignment if black (oversubtraction) and white (residue) regions are centrosymmetric.
After doing successfully, the next step is to compute:
1) OE rays: (ch1+ch3) - (ch2+ch4)
2) I- intensity: (ch1+ch3) + (ch2+ch4)
'''

from pylab import *
from pyraf import iraf
import glob

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
#  print filename_ch1,filename_ch2,filename_ch3,filename_ch4

##shifting and subtraction of channel 2 from channel 1
  iraf.imshift(filename_ch2,'shiftxy2',ch2_x,ch2_y) #shiftxy is the shifted output image (temporary file)
  fname_out2=filename_ch2[9:-7]+'_ch2' #retrive only the image number (e.g. 240)
  print "\n", fname_out2
#  raw_input()
  iraf.imarith(filename_ch1,'-','shiftxy2',fname_out2) #subtract ch1 to ch2
  iraf.imdel('shiftxy2') #delete temporary image file

##shifting and subtraction of channel 3 from channel 1
  iraf.imshift(filename_ch3,'shiftxy3',ch3_x,ch3_y)
  fname_out3=filename_ch3[9:-7]+'_ch3'
  print "\n", fname_out3
  iraf.imarith(filename_ch1,'-','shiftxy3',fname_out3)
  iraf.imdel('shiftxy3')

##shifting and subtraction of channel 4 from channel 1
  iraf.imshift(filename_ch4,'shiftxy4',ch4_x,ch4_y)
  fname_out4=filename_ch4[9:-7]+'_ch4'
  print "\n", fname_out4
  iraf.imarith(filename_ch1,'-','shiftxy4',fname_out4)
  iraf.imdel('shiftxy4')
