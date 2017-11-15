#!/usr/bin/env python
from pylab import *
from pyraf import iraf
# After trial and error, the shifts in x and y in image 240 are determined. Using channel 1 as reference, then 
#ch2: 0.7,0.3
#ch3: -0.1,0.3
#ch4: 0.2,0.5

filename_ch1='HICA00137241_ch1bfg.fits'
filename_ch2='HICA00137241_ch2bfg.fits'
filename_ch3='HICA00137241_ch3bfg.fits'
filename_ch4='HICA00137241_ch4bfg.fits'

x_list=[0.0,0.2,0.4]
y_list=[0.3,0.5,0.7]

n=1

iraf.imdel('241ch4_?.fits') #delete: program can't overwrite files

for y in y_list:
  for x in x_list:
    iraf.imshift(filename_ch4,'shifted',x,y)
    filename_output='241ch4_%d' % n 
    iraf.imari(filename_ch1,'-','shifted',filename_output)
    iraf.disp(filename_output,n)
    n=n+1
    iraf.imdel('shifted')
