#!usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU
'''
After aligning the rotI.fits images, this file realigns rotQ and rotU too by measured values (x_new,y_new). The x values are scanned in the center_rotQU.txt file. The shifted files are named as *_rotQa  and *_rotUa.fits found in the rotated_QU folder.
'''
from pylab import *
from pyraf import iraf
import glob
import math

a=loadtxt('center_rotQU.txt',dtype=str) #load Xi,Yi values are str temporarily
x_Q=a[:,1] #x array contains Xi and so does x for Yi
y_Q=a[:,2]
x_U=a[:,1] #x array contains Xi and so does x for Yi
y_U=a[:,2]

x_new_Q=range(len(x_Q))
y_new_Q=range(len(y_Q))
x_new_U=range(len(x_U))
y_new_U=range(len(y_U))

for i in range(len(x_Q)):
  x_new_Q[i]=271-float(x_Q[i]) #get the difference in x=271 (relative to the X[0] which is x of 120-123 (reference))
  y_new_Q[i]=318-float(y_Q[i]) #do the same for y=318
#]  print x_new[i], y_new[i]
  x_new_U[i]=271-float(x_U[i]) #get the difference in x=271 (relative to the X[0] which is x of 120-123 (reference))
  y_new_U[i]=318-float(y_U[i]) #do the same for y=318
# 

file_list_Q=glob.glob('*_rotQ.fits')
file_list_Q=list(file_list_Q)
file_list_Q.sort()

file_list_U=glob.glob('*_rotU.fits')
file_list_U=list(file_list_U)
file_list_U.sort()

i=0
for filename_tmp_Q in file_list_Q:
  filename_org_Q=filename_tmp_Q[:-10] #get only the file no.: e.g. 120-123
  filename_align_Q=filename_org_Q+'_rotQa.fits' #rename as 120-123_rotIa.fits
#shifting
  iraf.imshift(filename_tmp_Q,filename_align_Q,x_new_Q[i],y_new_Q[i]) #load e.g. 120-123_rotI.fits and shift it by x_new[0] and y_new[0] pixels and save as above
  print filename_tmp_Q, filename_align_Q #double-check
  print x_new_Q[i], y_new_Q[i]
  print '\n'
  i=i+1
  raw_input() #do this one at a time

j=0
for filename_tmp_U in file_list_U:
  filename_org_U=filename_tmp_U[:-10] #get only the file no.: e.g. 120-123
  filename_align_U=filename_org_U+'_rotUa.fits' #rename as 120-123_rotIa.fits
#shifting
  iraf.imshift(filename_tmp_U,filename_align_U,x_new_U[j],y_new_U[j]) #load e.g. 120-123_rotI.fits and shift it by x_new[0] and y_new[0] pixels and save as above
  print filename_tmp_U, filename_align_U #double-check
  print x_new_U[j], y_new_U[j]
  print '\n'
  j=j+1
  raw_input() #do this one at a time
