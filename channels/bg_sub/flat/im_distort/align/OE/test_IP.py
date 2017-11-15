#!usr/bin/env python
'''
FILENAME: test_IP.py
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

Then, compute for a,b,c,d and p,q,r,s for image no. 120-123.
Finally, compute for:
Q ~ {[(a/d)-(p/s)] - [(b/d)-(q/s)]*I} / [(c/d) - (r/s)]
U ~ (a - bI - cQ) / d
'''
import numpy as np
from pylab import *
import pyfits
from pyraf import iraf 
import glob
from numpy import matrix


#1. Compute for more accurate I

loadfile=loadtxt('IP_SUAur_20140119',dtype=str) #convert all values to string

#image_no[:,0], x11[:,1],x12[:,2],x13[:,3],x14[:,4]; x21[:,5],x22[:,6],x23[:,7],x24[:,8]

#Xij=X(row,column)
#I ~ [120_I/x11,120 + 121_I/x11,121 + 122_I/x11,122 + 123_I/x11,123]/4

file_list=glob.glob('*_I.fits')
file_list=list(file_list)
file_list.sort()

#numofimages=4			#[0:3]
numofimages=len(file_list)	#used to consider total no. of images in file_list

x11_all=loadfile[:,1]		#x11 corresponds to 1-> 2nd column
#list=range(numofimages)

list=range(4)
x11=range(len(x11_all))		#define the length of x11 array
m=0
for m in list:			#load x11 values
  x11[m]=float(loadfile[m,1])
'''
x11[0]_120=float(a[0,1])
x11[1]_121=float(a[1,1])
x11[2]_122=float(a[2,1])
x11[3]_123=float(a[3,1])
'''
#manually open the 4 image files
#120_I
hdu_list1= pyfits.open(file_list[0])
hdu1=hdu_list1[0]
image1=hdu1.data 
#121_I
hdu_list2= pyfits.open(file_list[1])
hdu2=hdu_list2[0]
image2=hdu2.data 
#122_I
hdu_list3= pyfits.open(file_list[2])
hdu3=hdu_list3[0]
image3=hdu3.data 
#123_I
hdu_list4= pyfits.open(file_list[3])
hdu4=hdu_list4[0]
image4=hdu4.data 

#A=120_I/x11,120 
A=image1/x11[0]
#B=121_I/x11,121
B=image2/x11[1]
#AB=A+B 
AB=A+B
#C=122_I/x11,122
C=image3/x11[2]
#D=123_I/x11,123
D=image4/x11[3]
#CD=C+D
CD=C+D
#ABCD=AB+CD
ABCD=AB+CD
#I=ABCD/4
I=ABCD/4
#save file
pyfits.writeto('120-123_I.fits',I)

#2. Compute for constants
#a=120_oe - 121_oe

#b=x21,120 - x21,121
#c=x22,120 - x22,121
#d=x23,120 - x23,121

#p=122_oe - 123_oe
#q=x21,122 - x21,123
#r=x22,122 - x22,123
#s=x23,122 - x23,123


'''
#for filename in file_list:
#  hdu_list = pyfits.open(filename)
#  hdu = hdu_list[0]	
#  image1 = hdu.data

#I think I need a tuple, library, dictionary? (image file (matrix) inside a 2D array)
#hdu_list=range(len(file_list)) OR hdu_list=np.zeros((size(file_list),1))
#hdu=                define as list of images with matrix inside
#image=              define as the image itself

#n=0
#for filename in file_list:
#  hdu_list[n] = pyfits.open(filename)
#  print hdu_list[n]
#  hdu[n] = hdu_list[0]		
#  image[n] = hdu[n].data
#  n=n+1
'''
