#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU/flux_scaling/PA_diskmajoraxis
'''
This file combines the radial PI distribution along PA=15 and 195 (major axis)
in a single plot. 
See 15radial_PI_dist.py to see individual results.
'''
from pylab import *
import pyfits
from scipy.ndimage.interpolation import rotate
import numpy as np
from matplotlib.patches import Ellipse
cmap=cm.jet
cmap.set_bad('black',1)

#z=pyfits.open('obj_PI_fs_conv_sigma08.fits')
#z=pyfits.open('obj_PI_fs_conv_sig1.fits')
z=pyfits.open('obj_PI_a_fs_conv_sig02.fits')
obj_PI_fs_conv=z[0].data-1.1e-7
z.close()

#define image center
scale=9.53e-3*140
xcenter=271
ycenter=318

obj_PI_fs_conv_cropped=obj_PI_fs_conv[ycenter-270:ycenter+271,xcenter-270:xcenter+271]
'''
figure(0)
clf()
extent=array([-200,200,-200,200])*scale 
imshow(log10(obj_PI_fs_conv_cropped),interpolation='nearest',origin='lower',cmap=cm.jet,extent=extent,vmin=-7.4,vmax=-5)
plot([0,0], [0, 200*scale], color='w', linestyle='--', linewidth=1)
xlabel('AU')
ylabel('AU')
title('original image (PA=0)')
'''
##scale the axes in AU; make array with 400 elements and subtract 200: [-200,-199,..199,200]*AU conversion factor
rscale=(arange(401)-200)*scale

#angle of image rotation along the major axis
angle1, angle2= 15, 195
rotated_image1=rotate(obj_PI_fs_conv_cropped,angle1)
rotated_image2=rotate(obj_PI_fs_conv_cropped,angle2)
dim1=rotated_image1.shape[0]
dim2=rotated_image2.shape[0]
midpoint1   =dim1/2
midpoint2   =dim2/2

extent_PI1=array([-midpoint1,midpoint1,-midpoint1,midpoint1])*scale
extent_PI2=array([-midpoint2,midpoint2,-midpoint2,midpoint2])*scale

#This combines subplots in figure 1 in one figure
figure(0)
clf()
imshow(log10(rotated_image1),extent=extent_PI1,vmin=-7.4,vmax=-5,cmap=cmap)
plot([0,0], [15*scale, midpoint1*scale], color='w', linestyle='--', linewidth=2)
plot([0,0], [-midpoint1*scale,-15*scale], color='w', linestyle='--', linewidth=2)
xlabel('AU')
ylabel('AU')
axis([-150,150,-150,150])
colorbar()

figure(1)
subplot(121)
imshow(log10(rotated_image1),extent=extent_PI1,vmin=-7.4,vmax=-5,cmap=cmap)
plot([0,0], [0, midpoint1*scale], color='w', linestyle='--', linewidth=1)
xlabel('AU')
ylabel('AU')
axis([-150,150,-150,150])
colorbar()
title('P.A.= %d deg.' % angle1)
# 195
subplot(122)
imshow(log10(rotated_image2),extent=extent_PI2,vmin=-7.4,vmax=-5,cmap=cmap)
plot([0,0], [0, midpoint2*scale], color='w', linestyle='--', linewidth=1)
xlabel('AU')
ylabel('AU')
axis([-150,150,-150,150])
colorbar()
title('P.A.= %d deg.' % angle2)

figure(2)
clf()
#get the average of of flux along the vertical (PA=15) +-2 pixels (5 columns) to increase SNR
image1a=rotated_image1[midpoint1:,midpoint1+1]*scale
image2a=rotated_image1[midpoint1:,midpoint1-1]*scale
image3a=rotated_image1[midpoint1:,midpoint1+2]*scale
image4a=rotated_image1[midpoint1:,midpoint1-2]*scale
image5a=rotated_image1[midpoint1:,midpoint1]*scale
image_ave1=(image1a+image2a+image3a+image4a+image5a)/5

image1b=rotated_image2[midpoint2:,midpoint2+1]*scale
image2b=rotated_image2[midpoint2:,midpoint2-1]*scale
image3b=rotated_image2[midpoint2:,midpoint2+2]*scale
image4b=rotated_image2[midpoint2:,midpoint2-2]*scale
image5b=rotated_image2[midpoint2:,midpoint2]*scale
image_ave2=(image1b+image2b+image3b+image4b+image5b)/5


#new_rscale=log((arange(rotated_image.shape[0])-midpoint)*scale)
new_rscale1=(arange(rotated_image1.shape[0])-midpoint1)*scale
new_rscale2=(arange(rotated_image2.shape[0])-midpoint2)*scale
#get only the positive values of flux; midpoint>=0
new_rscale1=new_rscale1[midpoint1:]
new_rscale2=new_rscale2[midpoint2:]
p1, p2 = -2.9, -2.8
constant1= 0.1037
constant2= 0.0498

label15 = 'PI flux for PA = %d deg.' % angle1
label195 = 'PI flux for PA = %d deg.' % angle2

#fit a power law with exponent p=-1
power_law_m1= constant1 * new_rscale1 ** p1
power_law_m2= constant2 * new_rscale2 ** p2
loglog(new_rscale1,image_ave1,'bo-',label=label15)
loglog(new_rscale2,image_ave2,'bs',mfc="None",label=label195) #unfilled circle
#You can draw multiple lines with a single plot command and  plot() returns a "list" of lines that were added.  In this case, the return value is a list of a single line, which is  unpacked with the comma .
t,=loglog(new_rscale2,image_ave2,'bo',mfc="None")
t.set_mec(t.get_color())

#log log plot of power law 
label1 = str(constant1)+'r ** %.1f (PA = %d deg.)' % (p1,angle1)
label2 = str(constant2)+'r ** %.1f (PA = %d deg.)' % (p2,angle2)

loglog(new_rscale1,power_law_m1,'b-',label=label1)
loglog(new_rscale2,power_law_m2,'b--',label=label2)

fontsize=20
xticks(fontsize=fontsize)
yticks(fontsize=fontsize)
#plot([0,0], [5e-8, 3e-5], color='r', linestyle='--', linewidth=1) #this is a vertical line along the origin

#input the last pixel = boundary of disk
end_pix_disk= 60
label3= 'mask boundary (r=20 AU); disk boundary r=%.1f AU' % ((end_pix_disk+1)*scale)

#mark the point marking the boundary of the mask at r=15, before of which the flux is unreliable, and also the last pixel used in fitting (flux>0)
loglog(15*scale,image_ave1[15], 'ro',label=label3)
loglog(15*scale,image_ave2[15], 'rs')

loglog(end_pix_disk*scale,image_ave1[end_pix_disk], 'ro') #for PA=15
loglog(end_pix_disk*scale,image_ave2[end_pix_disk], 'rs')
axis([0,1000,5e-8,3e-5]) #AU scale
ylabel('log ($n_{PI}$ / $n_*$)',fontsize=fontsize)
xlabel('log(r) (AU)',fontsize=fontsize)
#title('Radial PI distribution for PA=%d and %d' % (angle1,angle2))
legend(loc='upper right', shadow=True)

#Takami+13 used 0."3 arcsec in diameter mask
#0."3 arcsec/*0.00948arcsec/pix = 31.65 pixels
hmask,wmask= 30*scale,30*scale #radius = 15 pix = 20 AU
l=Ellipse(xy=(0,0),height=hmask,width=wmask)
figure(0).add_subplot(111).add_artist(l)
m=Ellipse(xy=(0,0),height=hmask,width=wmask)
figure(1).add_subplot(121).add_artist(m)
n=Ellipse(xy=(0,0),height=hmask,width=wmask)
figure(1).add_subplot(122).add_artist(n)
l.set_color('k')
m.set_color('k')
n.set_color('k')
show()

'''
np.savetxt('image_ave_PA15.txt',image_ave)
np.savetxt('new_rscale_PA15.txt',new_rscale)

import powerlaw
data = array([1.7, 3.2 ...]) # data can be list or numpy array
results = powerlaw.Fit(data)
print results.power_law.alpha
print results.power_law.xmin
R, p = results.distribution_compare('power_law', 'lognormal')
'''
