#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU/flux_scaling/PA_diskmajoraxis
'''
last edited: aug16
This file draws contour map for a rotated obj_PA_fs_conv
image for varius sigma. The major axis was determined to be
along PA=20.
An ellipse is also fitted.
Mask is also put.
'''
from pylab import *
import pyfits
from scipy.ndimage.interpolation import rotate
import numpy as np
from matplotlib.patches import Ellipse
#measured parameters
#major axis= h= 231.4 AU
#minor axis= w= 133.4 AU
#inclination=arccos(w/h)/180*pi=39.7 degrees
cmap=cm.jet
#because of log of negative values in imshow, we have infinite values (=white pixels) after applying log; set bad pixels to 1 to fix this
cmap.set_bad('black',1)
#z=pyfits.open('obj_PI_fs_conv_sig008.fits')
#z=pyfits.open('obj_PI_fs_conv_sig01.fits') 
#z=pyfits.open('obj_PI_fs_conv_sig015.fits')
z=pyfits.open('obj_PI_a_fs_conv_sig02.fits')
#z=pyfits.open('obj_PI_fs_conv_sig25.fits')
sigma=2
#subtract the median of the image=1.1e-7 (referring to the background noise)
obj_PI_fs_conv=z[0].data-1.1e-7
z.close()

#define image center
xcenter=271
ycenter=318
#pixel to AU conversion
scale=9.53e-3*140

#crop image; 401x401
#obj_PI_fs_conv_cropped=obj_PI_fs_conv[ycenter-250:ycenter+251,xcenter-250:xcenter+251]
obj_PI_fs_conv_cropped=obj_PI_fs_conv[ycenter-300:ycenter+301,xcenter-270:xcenter+271]
angle=15 #PA of major axis
rotated_image=rotate(obj_PI_fs_conv_cropped,angle)
dim=rotated_image.shape[0]
midpoint=dim/2

extent_PI=array([-midpoint,midpoint,-midpoint,midpoint])*scale
figure(0)
clf()
imshow(log10(rotated_image),extent=extent_PI,vmin=-7.4,vmax=-5,cmap=cmap)
colorbar()
#plot([0,0], [-midpoint*scale, midpoint*scale], color='w', linestyle='--', linewidth=1)
xlabel('AU')
ylabel('AU')

#plot contour lines having given specific flux values in the []
contour(log10(rotated_image),extent=extent_PI,colors='k',levels=[-6.75,-6.5,-6.25,-6.0],linestyles='solid')
axis(array([-150,150,-150,150])*scale)
#axis(array([-150,300,-150,150])*scale)

##superpose an ellipse centered at xy
h,w=130*scale,100*scale
e=Ellipse(xy=(3,-3),height=h,width=w,linewidth=1.5)
figure(0).add_subplot(111).add_artist(e)
e.set_ec('w')
e.set_fc('none')
e.set_ls('dashed')
#compute for inclination of disk
i=arccos(w/h)/pi*180
major_axis=h*scale
#title('P.A.= %d deg.; sigma= %.1f; major axis= %.1f AU; inclination= %.1f deg.'  % (angle,sigma,major_axis,i))

##put a mask
#Takami+13 used 0."3 arcsec in diameter mask
#0."3 arcsec/*0.00948arcsec/pix = 30 pixels
hmask,wmask= 30*scale,30*scale
m=Ellipse(xy=(0,0),height=hmask,width=wmask)
figure(0).add_subplot(111).add_artist(m)
m.set_color('k')
show()
