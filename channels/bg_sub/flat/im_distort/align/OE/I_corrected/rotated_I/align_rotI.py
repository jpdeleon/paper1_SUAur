#!usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/I_corrected/rotated_I
'''
By using imexam in pyraf (press r and then a to show center (row,col) of central bright source being measured), I found out that images' center shift by some pixels and hence makes stacking unreliable.
To compensate for this, this file aligns the rotI.fits images by value (x_new,y_new) relative to the first image (120-123) (x[0],y[0]). The measured (Xi,Yi) values are scanned in the center.txt file. The shifted files are named as rotIa.fits found in the aligned_I folder.
'''
from pylab import *
from pyraf import iraf
import glob
import math

a=loadtxt('center.txt',dtype=str) #load Xi,Yi values are str temporarily
x=a[:,1] #x array contains Xi and so does x for Yi
y=a[:,2]

x_new=range(len(x))
y_new=range(len(y))
for i in range(len(x)):
  x_new[i]=271-float(x[i]) #get the difference in x=271 (relative to the X[0] which is x of 120-123 (reference))
  y_new[i]=318-float(y[i]) #do the same for y=318
#]  print x_new[i], y_new[i]

file_list=glob.glob('*_rotI.fits')
file_list=list(file_list)
file_list.sort()

i=0
for filename_tmp in file_list:
  filename_org=filename_tmp[:-10] #get only the file no.: e.g. 120-123
  filename_align=filename_org+'_rotIa.fits' #rename as 120-123_rotIa.fits
#shifting
  iraf.imshift(filename_tmp,filename_align,x_new[i],y_new[i]) #load e.g. 120-123_rotI.fits and shift it by x_new[0] and y_new[0] pixels and save as above
  print filename_tmp, filename_align #double-check
  print x_new[i], y_new[i]
  print '\n'
  i=i+1
  raw_input() #do this one at a time
