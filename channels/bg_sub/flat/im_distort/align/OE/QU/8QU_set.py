#!usr/bin/env python
'''
FILENAME: 8UQ_set.py
FOLDER LOCATION: OE => UQ
This file is computes the U and Q (Stokes parameters) for a set of images 
per full half-wave plate cycle (0,45,22.5,67.5).
The given txt files are required to obtain the x?? values needed for computing the U and Q.
This also requires the output of 7I_cor_set.py which are more accurate computation of I images 
for the same set.
It does this by loading the total of 24 image data and putting them in a list called image_list_I.
Just like in 7I_cor_set.py, I_172.fits must be renamed to 215 and so on.
'''
from pylab import *
import pyfits
from pyraf import iraf 
import glob
import numpy

loadfile1=loadtxt('IP_SUAur_20140119',dtype=str)
loadfile2=loadtxt('IP_SUAur_ref_20140119',dtype=str)
loadfile=list(loadfile1)
loadfile.extend(list(loadfile2))
loadfile=array(loadfile)	

###2. Compute for constants
file_list_oe=glob.glob('*_oe.fits')
file_list_oe=list(file_list_oe)
file_list_oe.sort()

x21_all=loadfile[:,5]                           #load other x2? parameters
x22_all=loadfile[:,6]
x23_all=loadfile[:,7]
x24_all=loadfile[:,8]

x21=range(len(x21_all))                         #make arrays with length equal to total number of x21 corresponding to 
x22=range(len(x22_all))				#all science images and fill it up with dummy numbers using range function
x23=range(len(x23_all))
x24=range(len(x24_all))

numofimage_oe=len(file_list_oe)                 #I think numofimage_oe = *_I
numofimage_I=numofimage_oe

#import numpy as np
#set_oe = 4*np.array(zz)
z=(numofimage_oe)/4
zz=range(z)
set_oe=map(lambda x:x*4, zz) 			#multiplies 4 element-wise to zz => {0,4,8,12,...,N}, where N= (numofimage_oe)-4

#load I matrices computed in 7I_core_set.py
file_list_I=glob.glob('I_*.fits')		#refers to file output of 7I_cor_set.py (e.g. I_120)
file_list_I=list(file_list_I)
file_list_I.sort()				#file_list_I contains 24 image filenames; len(file_list_I)=24 

hdu_list_I=range(len(file_list_I))		#hdu_list now contains only 24 items, NOT 96!
hdu_I=range(len(file_list_I))			
image_list_I=range(len(file_list_I))

for f in hdu_list_I:
  hdu_list_I[f]= pyfits.open(file_list_I[f]) 
#  print "\n", hdu_list_I[f]		
  hdu_I[f]=hdu_list_I[f][0]
  image_list_I[f]=zeros((640,640))		#make again a dummy matrices
  image_list_I[f]=hdu_I[f].data			#load only the data

for v in range(numofimage_oe):                  #numofimage_oe=96
  x21[v]=float(loadfile[v,5])                   #load x2? with real values
  x22[v]=float(loadfile[v,6])
  x23[v]=float(loadfile[v,7])
  x24[v]=float(loadfile[v,8])

hdu_list_oe=range(numofimage_oe)                #make a mirror list for _oe
hdu_oe=range(numofimage_oe)
image_list_oe=range(numofimage_oe)

for g in hdu_list_oe:
  hdu_list_oe[g]= pyfits.open(file_list_oe[g])
#  print "\n", hdu_list_oe[g]		
  hdu_oe[g]=hdu_list_oe[g][0]			
  image_list_oe[g]=zeros((640,640))		#image_list_oe[0].shape
  image_list_oe[g]=hdu_oe[g].data

z=(numofimage_oe)/4 
zz=range(z) 
set_I=map(lambda x:x*4, zz)

for num2 in set_I:				# set_I=set_oe
  name=num2+120					#if 
  a=str(name)+'oe_minus_'+str(name+1)+'oe.fits'	#'120oe_minus_121oe.fits'
  iraf.imarith(file_list_oe[num2],'-',file_list_oe[num2+1],a)
  open_a= pyfits.open(a)
  image_a=open_a[0].data
#rm('120_oe_minus_121_oe.fits')
  iraf.imdel(a)					#need not to save as .fits in the folder
#b=x21,120 - x21,121 {const}			#a,b,c,d requires ch1 [num2] and ch2
  b=x21[num2] - x21[num2+1]
#c=x22,120 - x22,121 {const}
  c=x22[num2] - x22[num2+1]
#d=x23,120 - x23,121 {const}
  d=x23[num2] - x23[num2+1]  
  p=str(name+2)+'oe_minus_'+str(name+3)+'oe.fits'	#'122oe_minus_123oe.fits'
  iraf.imarith(file_list_oe[num2+2],'-',file_list_oe[num2+3],p)
  open_p= pyfits.open(p)				
  image_p=open_p[0].data
#rm('122_oe_minus_123_oe.fits')
  iraf.imdel(p)					#this .fits file need not be saved
#q=x21,122 - x21,123 {const}
  q=x21[num2+2] - x21[num2+3]			
#r=x22,122 - x22,123v{const}
  r=x22[num2+2] - x22[num2+3]
#s=x23,122 - x23,123 {const}
  s=x23[num2+2] - x23[num2+3]
#3. Compute for Q
#Q~{[(a/d)-(p/s)]-[(b/d)-(q/s)]*I}/[(c/d)-(r/s)]
  Q=((image_a/d-image_p/s)-(b/d-q/s)*image_list_I[num2/4])/(c/d-r/s)
#savefile
  q_name=str(name)+'-'+str(name+3)+'_Q.fits'		#e.g. 120-123_Q.fits
  pyfits.writeto(q_name,Q)
#4. Computer for U
#U~(a-bI-cQ)/d
  U=(image_a-b*image_list_I[num2/4]-c*Q)/d		#image_list_I[num2/4] = {0,1,2,3,4,...,23}; check if right by using 'for num2 in set_I: print name,num2/4'
#savefile
  u_name=str(name)+'-'+str(name+3)+'_U.fits'		#120-123_U.fits
  pyfits.writeto(u_name,U)
