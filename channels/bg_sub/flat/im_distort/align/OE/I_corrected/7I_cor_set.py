#!usr/bin/env python
'''
FILENAME: 7IP_set.py
FOLDER LOCATION: 
required file: IP_SUAur_20140119.txt
DESCRIPTION: This file is used to compute for Q and U (corrected).
Previously, Q and U were computed by simply adding or subtracting pairs of summed channels (ie. I=(ch1+ch3)+(ch2+ch4) [see test_oe.py].
This then accounts for corrections to better aprroximate ~Q and ~U.
First, the columns (=Xij) of the .txt file is scanned.
Naming scheme for columns, left to right is: 
image_no, x11,x12,x13,x14; x21,x22,x23,x24

Xij are important in computing for a,b,c,d & p,q,r,s

Try first set only:120(0),121(45),122(22.5),123(67.5),
where (n)= half-wave plate angle

[120_I/x11,120 + 121_I/x11,121 + 122_I/x11,122 + 123_I/x11,123]/4
check test_IP3.py for manual input and saving with more comments
'''
from pylab import *
import pyfits
#from pyraf import iraf 
import glob
import numpy

loadfile1=loadtxt('IP_SUAur_20140119',dtype=str)
loadfile2=loadtxt('IP_SUAur_ref_20140119',dtype=str)
loadfile=list(loadfile1)
loadfile.extend(list(loadfile2))
loadfile=array(loadfile)	

file_list_I=glob.glob('*_I.fits')
file_list_I=list(file_list_I)
file_list_I.sort()

numofimage_I=len(file_list_I)
x11_all=loadfile[:,1]

x11=range(len(x11_all))	

for m in range(numofimage_I):			         
  x11[m]=float(loadfile[m,1]) 
  
hdu_list_I=range(numofimage_I)
hdu_I=range(numofimage_I)
image_list_I=range(numofimage_I)

for f in hdu_list_I:
  hdu_list_I[f]= pyfits.open(file_list_I[f])
#  print "\n", hdu_list_I[f]		
  hdu_I[f]=hdu_list_I[f][0]
  image_list_I[f]=zeros((640,640))
  image_list_I[f]=hdu_I[f].data

#import numpy as np
#set = 4*np.array(zz)

z=(numofimage_I)/4
zz=range(z)
#set_I=arange(zz)*4
set_I=map(lambda x:x*4, zz) #replaces set elements with {0,4,8,12,...,N}

for num1 in set_I:
#  print num
#A=120_I/x11,120
  A=image_list_I[num1]/x11[num1]
#B=121_I/x11,121
  B=image_list_I[num1+1]/x11[num1+1]
#AB=A+B 
  AB=A+B
#C=122_I/x11,122
  C=image_list_I[num1+2]/x11[num1+2]
#D=123_I/x11,123
  D=image_list_I[num1+3]/x11[num1+3]
  #CD=C+D
  CD=C+D
#ABCD=AB+CD
  ABCD=AB+CD
  #I=ABCD/4
  I=ABCD/4
  #save file
  num1=num1+120
  I_name=str(num1)+'-'+str(num1+3)+'_I.fits'
  pyfits.writeto(I_name,I)  #you should correct the problem in saving name
# first set: 120-171 inclusive => 171-120= 51+1 = 52/4 = 13 image sets
# so rename starting image no. 120+(13*4)=172 to 
# next set: 215-226 inclusive => 3 image sets
# so rename 172 to 215, 176 to 219, and 180 to 223
# next set: 240-271 => 8 image sets
# so rename 184 to 240, 188 to 244, 192 to 248, 196 to 252, 200 to 256, 204 to 260, 208 to 264, and 212 to 268
