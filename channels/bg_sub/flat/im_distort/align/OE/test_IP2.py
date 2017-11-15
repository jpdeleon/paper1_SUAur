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
from pylab import *
import pyfits
from pyraf import iraf 
import glob
import numpy

###1. Compute for more accurate I
#SigmaI_subj~(o_subj + e_subj)/x11;j where j=4 ->{120,121,122,123}
loadfile1=loadtxt('IP_SUAur_20140119',dtype=str) #convert all values to string
loadfile2=loadtxt('IP_SUAur_ref_20140119',dtype=str)
loadfile=list(loadfile1)
loadfile.extend(list(loadfile2))		#append textfile 1 and 2 together
loadfile=array(loadfile)			#this fixes the problem with array something

file_list_I=glob.glob('*_I.fits')
file_list_I=list(file_list_I)
file_list_I.sort()

#numofimage=4			                #[0:3]
numofimage_I=len(file_list_I)	                #used to consider total no. of images in file_list_I

x11_all=loadfile[:,1]		                #x11 parameter corresponds to 2nd column in txt file [:,1]

#list=range(numofimage_I)
list=range(4)			                #test only the first 4 science images: 120-123
x11=range(len(x11_all))		                #define the length of x11 array

m=0
for m in list:			                #!!! change list to len(numofimage_I) to generalize
  x11[m]=float(loadfile[m,1])                   ##load x11 values 

#open all images and put it in hdu_list_I
hdu_list_I=range(numofimage_I)		        #define hdu_list_I,hdu_I,image_list as an array
hdu_I=range(numofimage_I)                       #their length must equal the number of image files
image_list_I=range(numofimage_I)

f=0
for f in hdu_list_I:			        #iterate to all image filenames
  hdu_list_I[f]= pyfits.open(file_list_I[f])    #hdu_list_I contains info of fits files (images)
#  print "\n", hdu_list_I[f]		
  hdu_I[f]=hdu_list_I[f][0]		        #hdu_I contains the data [0] of images
  image_list_I[f]=zeros((640,640)) 	        #fill up image_list with zero-matrices with size equal to fits image data 640sq.pix.
  image_list_I[f]=hdu_I[f].data			#append the image_list with the actual image data

#A=120_I/x11,120
A=image_list_I[89]/x11[61]			#to compute for other sets of images,eg.268- 271, 
#B=121_I/x11,121				#change I[0] to I[89]
B=image_list_I[90]/x11[62]
#AB=A+B 
AB=A+B						#I think calculating by each term reduces errors
#C=122_I/x11,122
C=image_list_I[91]/x11[63]
#D=123_I/x11,123
D=image_list_I[92]/x11[64]
#CD=C+D
CD=C+D
#ABCD=AB+CD
ABCD=AB+CD
#I=ABCD/4
I=ABCD/4
#save file
pyfits.writeto('268-271_I.fits',I)              #!!!generalize naming system

'''
###2. Compute for constants
file_list_oe=glob.glob('*_oe.fits')
#file_list_oe=list(file_list_oe)                #fix this issue: "list not callable"
file_list_oe.sort()

x21_all=loadfile[:,5]                           #load other parameters
x22_all=loadfile[:,6]
x23_all=loadfile[:,7]
x24_all=loadfile[:,8]

x21=range(len(x21_all))                         #make arrays with length equal to total number of x21 corresponding to 
x22=range(len(x22_all))				#all science images and fill it up with dummy numbers using range function
x23=range(len(x23_all))
x24=range(len(x24_all))

v=0				
for v in list:			                        #change list to len(numofimage_o) to generalize
  x21[v]=float(loadfile[v,5])                   #load x2? with real values
  x22[v]=float(loadfile[v,6])
  x23[v]=float(loadfile[v,7])
  x24[v]=float(loadfile[v,8])

numofimage_oe=len(file_list_oe)                 #I think numofimage_oe = *_I

hdu_list_oe=range(numofimage_oe)                #make a mirror list for _oe
hdu_oe=range(numofimage_oe)
image_list_oe=range(numofimage_oe)

g=0
for g in hdu_list_oe:
  hdu_list_oe[g]= pyfits.open(file_list_oe[g])
#  print "\n", hdu_list_oe[g]		
  hdu_oe[g]=hdu_list_oe[g][0]			
  image_list_oe[g]=zeros((640,640))
  image_list_oe[g]=hdu_oe[g].data

a='120_oe_minus_121_oe.fits'
#a=120_oe - 121_oe {matrix}
iraf.imarith(image_list_oe[0],'-',image_list_oe[1],a)
#b=x21,120 - x21,121 {const}
b=x21[0] - x21[1]
#c=x22,120 - x22,121 {const}
c=x22[0] - x22[1]
#d=x23,120 - x23,121 {const}
d=x23[0] - x23[1]

p='122_oe_minus_123_oe.fits'
#p=122_oe - 123_oe {matrix}
iraf.imarith(image_list_oe[2],'-',image_list_oe[3],p)
#q=x21,122 - x21,123 {const}
q=x21[2] - x21[3]
#r=x22,122 - x22,123v{const}
r=x22[2] - x22[3]
#s=x23,122 - x23,123 {const}
s=x23[2] - x23[3]


#3. Compute for Q
#Q~{[(a/d)-(p/s)]-[(b/d)-(q/s)]*I}/[(c/d)-(r/s)]
#numerator of Q
#E=a{matrix}/d{const}; E={matrix}
E=a/d
#F=p{matrix}/a{const}; F={matrix}
F=p/s
#EF={matrix}; EF=E-F
iraf.imarith(E,'-',F,EF)
#G={const}
G=b/d
#H={const}
H=q/s
#GH={const}
GH=G-H
#GHI={matrix}
GHI=I*GH
#EFGHI={matrix}
EFGHI=EF-GHI
iraf.imarith(EF,'*',GHI,EFGHI)
#denominator of Q
J=c/d
K=r/s
JK=J-K

Q=EFGHI/JK
#savefile
pyfits.writeto('120-123_Q.fits',Q)

#4. Computer for U
#U~(a-bI-cQ)/d
bI=I*b
cQ=Q*c
num_Q= a-bI-cQ

Q=num_Q/d
#savefile
pyfits.writeto('120-123_U.fits',U)
'''
