#!/usr/bin/env python
'''
This file stacks the images in each set (science/ND10, ND1 and ref) to increase SNR. It requires the rotated images and simply calculates and then applies the median pixel-wise to make a "stacked image." There are 2 outputs for each set: obj_medQ, obj_medU, ref_medQ, ref_medU, ND1_medQ, ND1_medU. 
'''

from pylab import*
import pyfits

file_no_list_obj=['132-135','136-139','140-143','144-147','148-151','152-155','156-159','160-163','164-167','168-171','172-175','176-179'] #the last 2 are 215-218 & 219-222 actually
file_no_list_ND1=['120-123','124-127','128-131','180-183'] # the last image comes from another ap pol set
file_no_list_ref=['184-187','188-191','192-195','196-199','200-203','204-207','208-211','212-215']

##science Q
Q_obj_array=[]
Q_ND1_array=[]
Q_ref_array=[]

for file_no_Q in file_no_list_obj:
  a1=pyfits.open(file_no_Q+'_rotQ.fits')
  Q_obj_array.append(a1[0].data)
  a1.close()
Q_obj_array=array(Q_obj_array)
Q_obj=median(Q_obj_array,axis=0)
#save 
pyfits.writeto('obj_medQ.fits',Q_obj)  

##ND1
for file_no_ND1 in file_no_list_ND1:
  a2=pyfits.open(file_no_ND1+'_rotQ.fits')
  Q_ND1_array.append(a2[0].data)
  a2.close()
Q_ND1_array=array(Q_ND1_array)
Q_ND1=median(Q_ND1_array,axis=0)
#save 
pyfits.writeto('ND1_medQ.fits',Q_ND1)

##ref
for file_no_ref in file_no_list_ref:
  a3=pyfits.open(file_no_ref+'_rotQ.fits')
  Q_ref_array.append(a3[0].data)
  a3.close()
Q_ref_array=array(Q_ref_array)
Q_ref=median(Q_ref_array,axis=0)
#save 
pyfits.writeto('ref_medQ.fits',Q_ref)

figure(1)
clf()
subplot(131)
imshow(Q_obj[250:350,200:300],vmin=-200,vmax=200,interpolation='nearest',cmap=cm.gray)
title('Q_obj')
xlabel("Dec")
ylabel("R.A.")
subplot(132)
imshow(Q_ND1[250:350,200:300],vmin=-200,vmax=200,interpolation='nearest',cmap=cm.gray)
title('Q_ND1')
subplot(133)
imshow(Q_ref[250:350,200:300],vmin=-200,vmax=200,interpolation='nearest',cmap=cm.gray)
title('Q_ref')
### Science U
U_obj_array=[]
U_ND1_array=[]
U_ref_array=[]

for file_no_U in file_no_list_obj:
  b1=pyfits.open(file_no_U+'_rotU.fits')
  U_obj_array.append(b1[0].data)
  b1.close()
U_obj_array=array(U_obj_array)
U_obj=median(U_obj_array,axis=0)
#save 
pyfits.writeto('obj_medU.fits',U_obj)  

##ND1
for file_no_ND1 in file_no_list_ND1:
  b2=pyfits.open(file_no_ND1+'_rotU.fits')
  U_ND1_array.append(b2[0].data)
  b2.close()
U_ND1_array=array(U_ND1_array)
U_ND1=median(U_ND1_array,axis=0)
#save 
pyfits.writeto('ND1_medU.fits',U_ND1)

##ref
for file_no_ref in file_no_list_ref:
  b3=pyfits.open(file_no_ref+'_rotU.fits')
  U_ref_array.append(b3[0].data)
  b3.close()
U_ref_array=array(U_ref_array)
U_ref=median(U_ref_array,axis=0)
#save 
pyfits.writeto('ref_medU.fits',U_ref)

figure(2)
clf()
subplot(131)
imshow(U_obj[250:350,200:300],vmin=-200,vmax=200,interpolation='nearest',cmap=cm.gray)
title('U_obj')
xlabel("Dec")
ylabel("R.A.")

subplot(132)
imshow(U_ND1[250:350,200:300],vmin=-200,vmax=200,interpolation='nearest',cmap=cm.gray)
title('U_ND1')

subplot(133)
imshow(U_ref[250:350,200:300],vmin=-200,vmax=200,interpolation='nearest',cmap=cm.gray)
title('U_ref')
