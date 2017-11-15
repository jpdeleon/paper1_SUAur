#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU/flux_scaling/PA_diskmajoraxis
from pylab import *
import pyfits
from scipy.ndimage.interpolation import rotate
import numpy as np

z=pyfits.open('obj_PI_fs_conv_sig1.fits')
obj_PI_fs_conv=z[0].data
z.close()

#define image center
xcenter=271
ycenter=318

#crop image; 401x401
obj_PI_fs_conv_cropped=obj_PI_fs_conv[ycenter-200:ycenter+201,xcenter-200:xcenter+201]

###
angle=60

rotated_image=rotate(obj_PI_fs_conv_cropped,angle)
figure(1)
clf()
dim=rotated_image.shape[0]
midpoint=dim/2
extent_PI=array([0-midpoint,dim-midpoint,0-midpoint,dim-midpoint])
imshow(log10(rotated_image),extent=extent_PI)
plot([0,0], [-midpoint, midpoint], color='r', linestyle='--', linewidth=1)
plot([-midpoint,midpoint], [0, 0], color='r', linestyle='--', linewidth=1)
name1='PA='+str(angle)
title(name1)
new_rscale=(arange(dim)-midpoint)*9.53e-3*140
figure(2)
clf()
semilogy(new_rscale,rotated_image[midpoint,:],label='horizontal')
semilogy(new_rscale,rotated_image[:,midpoint],label='vertical')
xmax=round(np.max(rotated_image[midpoint,:]),7)
ymax=round(np.max(rotated_image[:,midpoint]),7)
name2='PA='+str(angle)
title(name2)
ylabel('Flux (normalized)')
xlabel('pixel position')
legend(loc='upper right', shadow=True)
show()
#0 - -113-9=122

#10- -47-115=162

#20- -87-64=151

#25- -46-25=71 minimum (visual)
#a=[-47,1.7e-7],[42,1.77e-7]
#30- -58-45=103

#40- -41-77=118

#50- -85-98=183

#60- -81-107=188 maximum
#b=[],[]
#70- -82-91=178

#80- -85-90=175 

#85- -90-93=183 2nd max (visual)

#90- -75-96=171

#95- - 82-86=168
