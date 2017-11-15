#!/usr/bin/env python
#cd ~/../../media/Seagate\ Backup\ Plus\ Drive/asiaa/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU/flux_scaling/PA_diskmajoraxis/final_figs
#updated: 01/07/2015

###TASKS### 
#1. Draw the contour used in Figure 1 (done using "level1, level2, ...")
#2. Apply the mask at the center (done using Ellipse)
#3. Change the color contrast (done using vmin, vmax)
#4.   Convolution (done by changing FWHM_in_arcsec) 
#5.   Power index (done by changing power_index

from pylab import *
import pyfits
from scipy.ndimage.filters import gaussian_filter
from matplotlib.patches import Ellipse
cmap1=cm.jet
cmap1.set_bad('black',1)
cmap2=cm.Blues

############################################################
### Constants ##############################################
############################################################

filename = 'obj_PI_a_fs.fits'
x_center = 271
y_center = 318

FWHM_in_arcsec  = 0.08    # FWHM for gaussian convolution
flux_scaling    = 1e-7   # PI_I0; to display the images
background      = 9.4e-8 # PI/I_0. Measured using test.py
#note, we've been using background = 1.1e-7 eversince 

power_index     = 2.1    # We will scale the PI flux multiplying
                         #   r**power_index, where r is the distance
                         #   from the center in arcsec

range_for_showing_image = [-1.3,1.3,-1.2,1.2]
pix_scale       = 9.53e-3 # arcsec


a,b,c,d= -6.75,-6.5,-6.25,-6.0      #contour lines used before
level1=((10**a+1.1e-7)-background)/flux_scaling
level2=((10**b+1.1e-7)-background)/flux_scaling
level3=((10**c+1.1e-7)-background)/flux_scaling
level4=((10**d+1.1e-7)-background)/flux_scaling

#another constants for improving contrast#
#vmin = median(im_processed_new/flux_scaling)/2= 0.2 
#vmax = median(im_processed_new/flux_scaling)*2= 0.9
vmin, vmax = 0.25, 0.95

############################################################
### Begin ##################################################
############################################################

### Load the image ###
# We also subtract the background described above.

a=pyfits.open(filename)
im_org=a[0].data-background
a.close()

### Convolve the image with a gaussian ###

im_convolved = gaussian_filter(im_org,
                 sigma=FWHM_in_arcsec/pix_scale/2.354820)

### Preparation to use the imshow and contour commands ###
### to display the results with arcsec                 ###
x_template = (arange(im_convolved.shape[1])-x_center)*pix_scale
y_template = (arange(im_convolved.shape[0])-y_center)*pix_scale
X,Y        = meshgrid(x_template,y_template)


### Make the image with a special effect ###
#this looks like getting the radial component and multiplying it
#to each pixels following a power law
im_processed_old=copy(im_convolved)
im_processed_new=copy(im_convolved)
for x in range(im_processed_old.shape[1]):
  for y in range(im_processed_old.shape[0]):
    r=sqrt((x-x_center)**2+(y-y_center)**2)*pix_scale
    im_processed_new[y,x]*=r**power_index
    im_processed_old[y,x]*=r**2.1

### Display the results ###
figure(1)
clf()
ax=subplot(221)
imshow(im_processed_old/flux_scaling,origin='lower',interpolation='nearest',
       vmin=0.2,vmax=0.9,cmap=cmap2,
       extent=[x_template[0],x_template[-1],y_template[0],y_template[-1]])
colorbar()
axis(range_for_showing_image)

###Adding masks###
#0."3 arcsec/*pix_scale = 31.65 pixels
hmask,wmask= 30*pix_scale,30*pix_scale #radius = 15 pix = 20 AU
m=Ellipse(xy=(0,0),height=hmask,width=wmask)
figure(1).add_subplot(221).add_artist(m)
m.set_color('k')

subplot(222)
imshow(im_processed_old/flux_scaling,origin='lower',interpolation='nearest',
       vmin=0.1,vmax=1.1, cmap=cmap1,
       extent=[x_template[1],x_template[-2],y_template[1],y_template[-2]])
colorbar()
axis(range_for_showing_image)
#add mask#
n=Ellipse(xy=(0,0),height=hmask,width=wmask)
figure(1).add_subplot(222).add_artist(n)
n.set_color('k')

subplot(223)
imshow(im_processed_new/flux_scaling,origin='lower',interpolation='nearest',
       vmin=vmin,vmax=vmax,cmap=cmap2,
       extent=[x_template[0],x_template[-1],y_template[0],y_template[-1]])
colorbar()
#2,6,12
contour(X,Y,im_convolved/flux_scaling,levels=[level1,level2,level3,level4],colors='r',linewidth=2)
axis(range_for_showing_image)

#add mask#
o=Ellipse(xy=(0,0),height=hmask,width=wmask)
figure(1).add_subplot(223).add_artist(o)
o.set_color('k')

subplot(224)
imshow(im_processed_new/flux_scaling,origin='lower',interpolation='nearest',
       vmin=vmin,vmax=vmax, cmap=cmap1,
       extent=[x_template[0],x_template[-1],y_template[0],y_template[-1]])
colorbar()
#2,4,8
contour(X,Y,im_convolved/flux_scaling,levels=[level1,level2,level3,level4],colors='w')
axis(range_for_showing_image)
#add mask#
p=Ellipse(xy=(0,0),height=hmask,width=wmask)
figure(1).add_subplot(224).add_artist(p)
p.set_color('k')

show()