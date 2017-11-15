#!/usr/bin/env python
#cd ~/Desktop/ref
'''
This file crops the four channels from the original raw image
and saves them as individual .fits file.
'''
from pylab import *
from pyraf import iraf
import glob

ch1='[60:669,1100:1739]' 	#1.624 microns
ch2='[695:1334,1100:1739]' 	#1.600
ch3='[755:1394,415:1054]' 	#1.575
ch4='[1395:2034,410:1049]' 	#1.644

file_list=glob.glob('HICA*')
file_list=list(file_list)
file_list.sort()

#n=len(file_list)
#loop over file_list[0-n]
for filename in file_list:
    #filename changes from file_list[0-n]; e.g. 'HICA*132.fits to HICA*271.fits'
    filename=filename.translate(None, '.fits')
    a1=filename+ch1
    b1=filename+'_ch1'
    a2=filename+ch2
    b2=filename+'_ch2'
    a3=filename+ch3
    b3=filename+'_ch3'
    a4=filename+ch4
    b4=filename+'_ch4'
    print filename, a1, b1, a2, b2, a3, b3, a4, b4
    iraf.imcopy(a1,b1) ##extract (crop) the 4 portions of the image file and 
    iraf.imcopy(a2,b2) ##save using the filename[i]
    iraf.imcopy(a3,b3)
    iraf.imcopy(a4,b4)
'''
#for renaming flat frames
iraf.imcopy('flat.fits[1395:2034,410:1049]','flat_ch4')

filename='flat'
ch1='[60:669,1100:1739]'
ch2='[695:1334,1100:1739]'
ch3='[755:1394,415:1054]'
ch4='[1395:2034,410:1049]'

a1=filename+ch1
b1=filename+'_ch1'
a2=filename+ch2
b2=filename+'_ch2'
a3=filename+ch3
b3=filename+'_ch3'
a4=filename+ch4
b4=filename+'_ch4'

for filename in file_list:
iraf.imcopy(a1,b1)
iraf.imcopy(a2,b2)
iraf.imcopy(a3,b3)
iraf.imcopy(a4,b4)
'''
