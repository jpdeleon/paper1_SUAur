#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU
'''
This file is just used to change vmin/vmax of obj_PI_fs images
to reveal more features associated with the extended material.
Comparison is done visually by plotting.
The next step is producing various sigma (test_PI_opt_sigma.py) given optimized vmin/vmax value derived here.
vmin=0.65,vmax=2.8 or 0.7 to 2 for conv_sigma05
no derived value for obj_PI_fs
'''
from pylab import*
import pyfits
from scipy.ndimage.filters import gaussian_filter

#obj
a1=pyfits.open('obj_PI_fscaled.fits')
obj_PI_fs=a1[0].data
obj_PI_fs_log=log10(obj_PI_fs)
a1.close()

a2=pyfits.open('obj_PI_conva_sigma05.fits')
obj_PI_conv_fs=a2[0].data
a2.close()

'''
#ref
b1=pyfits.open('ref_PI.fits')
ref_PI=b1[0].data
b1.close()

b2=pyfits.open('ref_PI_a.fits')
ref_PI_a=b2[0].data
b2.close()

b3=pyfits.open('ref_PI_convolved.fits')
ref_PI_convolved=b3[0].data
b3.close()

b4=pyfits.open('ref_PI_convolved_a.fits')
ref_PI_convolved_a=b4[0].data
b4.close()

#ND1
c1=pyfits.open('ND1_PI.fits')
ND1_PI=c1[0].data
c1.close()

c2=pyfits.open('ND1_PI_a.fits')
ND1_PI_a=c2[0].data
c2.close()

c3=pyfits.open('ND1_PI_convolved.fits')
ND1_PI_convolved=c3[0].data
c3.close()

c4=pyfits.open('ND1_PI_convolved_a.fits')
ND1_PI_convolved_a=c4[0].data
c4.close()
'''
#vmin=-10
#vmax=80
#vmin=0
#vmax=2.62

xzoommin=150
xzoommax=500
yzoommin=100
yzoommax=450
xcenter_obj=271
ycenter_obj=318

pix_scale=0.00948
a=0-xcenter_obj
b=640-xcenter_obj
c=0-ycenter_obj
d=640-ycenter_obj
extent_PI=array([a*pix_scale,b*pix_scale,c*pix_scale,d*pix_scale])
extent_PI*=140 

figure(1)
clf()
##obj
imshow(log10(obj_PI_fs),interpolation='nearest',origin='lower',cmap=cm.jet,extent=extent_PI)
colorbar()
#axis([xzoommin,xzoommin,yzoommin,yzoommax])

figure(2)
clf()
subplot(121)
imshow(log10(obj_PI_conv_fs),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=0.65,vmax=2.8,extent=extent_PI)
#axis([xzoommin,xzoommin,yzoommin,yzoommax])
colorbar()

subplot(122)
imshow(log10(obj_PI_conv_fs),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=0.7,vmax=2,extent=extent_PI)
#axis([xzoommin,xzoommin,yzoommin,yzoommax])
colorbar()
show()

#save
#pyfits.writeto('obj_PI_fs_log.fits',obj_PI_fs_log)
'''
NOTE: to get vmin, vmax values, I used
import numpy as np
In [67]: log10(np.mean(obj_PI_fs))
Out[67]: -6.6877797215769856

In [68]: log10(np.min(obj_PI_fs))
Out[68]: -9.8257728961242208

In [69]: log10(np.max(obj_PI_fs))
Out[69]: -4.5486361167285647

and also for obj_PI_conv_fs
'''
