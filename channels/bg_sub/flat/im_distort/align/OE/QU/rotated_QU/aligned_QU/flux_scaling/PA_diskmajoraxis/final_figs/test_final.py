#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU/flux_scaling/PA_diskmajoraxis/final_figs
'''
'''
from pylab import*
import pyfits
from scipy.ndimage.filters import gaussian_filter
from matplotlib.patches import Ellipse
cmap=cm.jet
cmap.set_bad('black',1)

max_length=300       # Pol=100 % in pixel

### Classes and Modules ###
class Linear_pol_vector:
  def __init__(self,x,y,I,Q,U,ax,max_length=10,linewidth=2,color='b'):
    self.x=x
    self.y=y
    self.I=I
    self.Q=Q
    self.U=U
    self.ax=ax
    self.max_length=max_length
    self.P=sqrt(Q**2+U**2)/I
    if self.P == 0:
      self.pl,=ax.plot([self.x,self.x],[self.y,self.y],linestyle='-',color=color,
                   linewidth=2)
    else:
      self.ang=arctan2(self.U,self.Q)*0.5
      dx=self.P*cos(self.ang)*0.5*self.max_length
      dy=self.P*sin(self.ang)*0.5*self.max_length
      self.pl,=ax.plot([self.x-dx,self.x+dx],[self.y-dy,self.y+dy],
                   linestyle='-',color=color,linewidth=2)

  def change_max_length(self,max_length=10):
    if self.P != 0:
      dx=self.P*cos(self.ang)*0.5*self.max_length
      dy=self.P*sin(self.ang)*0.5*self.max_length
      self.pl.set_xdata=[self.x-dx,self.x+dx]
      self.pl.set_ydata=[self.y-dy,self.y+dy]

  def reset(self):
    self.change_max_length()
    self.pl.set_linewidth=2
    self.pl.set_color='w'

### Begin ###
#z=pyfits.open('obj_PI_fs_conv_sigma08.fits')
#z=pyfits.open('obj_PI_fs_conv_sig1.fits')
a=pyfits.open('obj_PI_fs_conv_sig2.fits')
obj_PI_fs_conv=a[0].data-1.1e-7
a.close()

#fscaled PI
b=pyfits.open('obj_PI_fscaled.fits')
obj_PI_fs=b[0].data
b.close()

#fscaled convolved PI
c=pyfits.open('obj_PI_fs_conv_sig1.fits') 
obj_PI_fs_conv_sig1=c[0].data
c.close()

#Q
d=pyfits.open('obj_medQa.fits')
obj_medQa=d[0].data
d.close()
#U
e=pyfits.open('obj_medUa.fits')
obj_medUa=e[0].data
e.close()
#I
f=pyfits.open('obj_medI_a.fits')
obj_medI_a=f[0].data
f.close()

#define image center
xcenter=271
ycenter=318
scale=9.53e-3*140
extent=array([-200,200,-200,200])*scale 

#place plot origin to center of object
a=0-xcenter
b=640-xcenter
c=0-ycenter
d=640-ycenter

#convert pix to arcsec
extent_PI=array([a,b,c,d])*scale
'''
figure(1)
clf()
extent=array([-200,200,-200,200])*scale 
imshow(log10(obj_PI_fs_conv),interpolation='nearest',origin='lower',cmap=cmap,extent=extent,vmin=-7.4,vmax=-5)
plot([0,0], [0, 200*scale], color='w', linestyle='--', linewidth=1)
colorbar()
xlabel('AU')
ylabel('AU')
title('original image (PA=0)')

figure(2)
clf()
imshow(log10(obj_PI_fs),interpolation='nearest',origin='lower',cmap=cmap,vmin=-7.4,vmax=-5,extent=extent_PI)
colorbar()
title('obj_PI_fs_conv')
xlabel('AU')
ylabel('AU')
'''
figure(3)
clf()
ax=subplot(111)

#imshow(log10(obj_PI_conva_fs),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=0,vmax=2,extent=extent_PI)
#colorbar()
#title('obj_PI_conv_sig=3')

imshow(log10(obj_PI_fs_conv),interpolation='nearest',origin='lower',cmap=cmap,vmin=-7.4,vmax=-5,extent=extent_PI)
colorbar()
contour(log10(obj_PI_fs_conv_sig1),extent=extent_PI,colors='k',levels=[-6.75,-6.5,-6.25,-6.0],linestyles='solid')
#title('obj_PI_fs_conv_sig=2')
xlabel('AU')
ylabel('AU')
axis([-200,400,-150,150])

##superpose an ellipse centered at xy
h,w=130*scale,100*scale
e=Ellipse(xy=(3,-3),height=h,width=w,linewidth=2,angle=15)
figure(3).add_subplot(111).add_artist(e)
e.set_ec('r')
e.set_fc('none')
e.set_ls('dashed')

varray=[]
#dx=dy=4
dx=dy=9
area=(2*dx+1)*(2*dy+1)

#inc=10
inc=20
xmin=xcenter-100	#extent of the region where pol vectors will be drawn
xmax=xcenter+310
ymin=ycenter-100
ymax=ycenter+110

x_in_AU=(arange(640)-xcenter)*scale
y_in_AU=(arange(640)-ycenter)*scale

for x in range(xmin,xmax,inc):
  for y in range(ymin,ymax,inc):
    r_in_AU=sqrt(x_in_AU[x]**2+y_in_AU[y]**2)
    if r_in_AU < 15: continue			#put pol vectors outside r=15
    if log10(obj_PI_fs_conv[y,x]) > -7.4: #threshold of polarization (smaller- wider)
      I=sum(obj_medI_a[y-dy:y+dy+1,x-dx:x+dx+1])/area
      Q=sum(obj_medQa[y-dy:y+dy+1,x-dx:x+dx+1])/area
      U=sum(obj_medUa[y-dy:y+dy+1,x-dx:x+dx+1])/area
      v=Linear_pol_vector(x_in_AU[x],y_in_AU[y],I,-Q,-U,ax,max_length=max_length,color='w')
draw()

#Takami+13 used 0."3 arcsec in diameter mask
#0."3 arcsec/*0.00948arcsec/pix = 31.65 pixels
hmask,wmask= 30*scale,30*scale #radius = 15 pix = 20 AU
m=Ellipse(xy=(0,0),height=hmask,width=wmask)
figure(3).add_subplot(111).add_artist(m)
m.set_color('k')
show()
