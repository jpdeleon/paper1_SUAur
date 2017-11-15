#!/usr/bin/env python
from pylab import *
import pyfits

file_no_list_obj=['132-135','136-139','140-143','144-147','148-151','152-155','156-159','160-163','164-167','168-171','172-175','176-179'] #the last 2 are 215-218 & 219-222 actually
file_no_list_ND1=['120-123','124-127','128-131','180-183'] # the last image comes from another ap pol set
file_no_list_ref=['184-187','188-191','192-195','196-199','200-203','204-207','208-211','212-215']

### Science I
I_obj_array=[]
I_ND1_array=[]
I_ref_array=[]

for file_no_I in file_no_list_obj:
  c1=pyfits.open(file_no_I+'_rotIa.fits')
  I_obj_array.append(c1[0].data)
  c1.close()
I_obj_array=array(I_obj_array)
I_obj=median(I_obj_array,axis=0)
#save 
pyfits.writeto('obj_medI.fits',I_obj)  

##ND1
for file_no_ND1 in file_no_list_ND1:
  c2=pyfits.open(file_no_ND1+'_rotIa.fits')
  I_ND1_array.append(c2[0].data)
  c2.close()
I_ND1_array=array(I_ND1_array)
I_ND1=median(I_ND1_array,axis=0)
#save 
pyfits.writeto('ND1_medI.fits',I_ND1)

##ref
for file_no_ref in file_no_list_ref:
  c3=pyfits.open(file_no_ref+'_rotIa.fits')
  I_ref_array.append(c3[0].data)
  c3.close()
I_ref_array=array(I_ref_array)
I_ref=median(I_ref_array,axis=0)
#save 
pyfits.writeto('ref_medI.fits',I_ref)

figure(1)
clf()
subplot(131)
imshow(I_obj,vmin=-200,vmax=200,interpolation='nearest',cmap=cm.gray)
title('I_obj')
xlabel("X (pixels)")
ylabel("X (pixels)")

subplot(132)
imshow(I_ND1,vmin=-200,vmax=200,interpolation='nearest',cmap=cm.gray)
title('I_ND1')
subplot(133)
imshow(I_ref,vmin=-200,vmax=200,interpolation='nearest',cmap=cm.gray)
title('I_ref')
show()
