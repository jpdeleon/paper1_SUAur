#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU
'''
This file maps polarization vectors given the
convolved PI image (e.g. sigma=0.8).
The file came from output of 10PI_set.
This files works for those are flux calibrated images ONLY.
obj_PI_conva_sigma05.fits
The input PI conva image can be changed with different sigma.
Change parameters such as threshold of polarization.

optimized parameters determined from test_PI_opt_v_fs.py
obj_PI_fs: vmin=0.4, vmax=2, sigma=0.8
obj_PI_fs_conv: vmin=-7.4, vmax=-5
'''
from pylab import*
import pyfits
from scipy.ndimage.filters import gaussian_filter

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
a=pyfits.open('obj_PI_a.fits')
obj_PI_a=a[0].data
a.close()

#fscaled PI
b=pyfits.open('obj_PI_fscaled.fits')
obj_PI_fs=b[0].data
b.close()
#fscaled convolved PI
c=pyfits.open('obj_PI_fs_conv_sigma08.fits') 
obj_PI_fs_conv=c[0].data
c.close()

#d=pyfits.open('obj_PI_fscaled_sig3.fits') 
#obj_PI_conva_fs=d[0].data
#d.close()

#Q
e=pyfits.open('obj_medQa.fits')
obj_medQa=e[0].data
e.close()
#U
f=pyfits.open('obj_medUa.fits')
obj_medUa=f[0].data
f.close()
#I
g=pyfits.open('obj_medI_a.fits')
obj_medI_a=g[0].data
g.close()

xcenter_obj=271
ycenter_obj=318

pix_scale=0.00948 #HiCIAO pixel scale (arcsec/pix)
#place plot origin to center of object
a=0-xcenter_obj
b=640-xcenter_obj
c=0-ycenter_obj
d=640-ycenter_obj
#convert pix to arcsec
extent_PI=array([a*pix_scale,b*pix_scale,c*pix_scale,d*pix_scale])
extent_PI*=140 

figure(1)
imshow(log10(obj_PI_a),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=0.4,vmax=2,extent=extent_PI)
colorbar()
title('obj_PI_fs')
xlabel('AU')
ylabel('AU')

figure(2)
imshow(log10(obj_PI_fs),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=-7.4,vmax=-5,extent=extent_PI)
colorbar()
title('obj_PI_fs_conv')
xlabel('AU')
ylabel('AU')

figure(3)
clf()
ax=subplot(111)

#imshow(log10(obj_PI_conva_fs),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=0,vmax=2,extent=extent_PI)
#colorbar()
#title('obj_PI_conv_sig=3')

imshow(log10(obj_PI_fs_conv),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=-7.4,vmax=-5,extent=extent_PI)
colorbar()
title('obj_PI_fs_conv_sig=0.8')
xlabel('AU')
ylabel('AU')
show()

varray=[]
scale=pix_scale*140 
#dx=dy=4
dx=dy=9
area=(2*dx+1)*(2*dy+1)

#inc=10
inc=20
xmin=xcenter_obj-100	#extent of the region where pol vectors will be drawn
xmax=xcenter_obj+310
ymin=ycenter_obj-100
ymax=ycenter_obj+110

x_in_AU=(arange(640)-xcenter_obj)*scale
y_in_AU=(arange(640)-ycenter_obj)*scale

for x in range(xmin,xmax,inc):
  for y in range(ymin,ymax,inc):
    if log10(obj_PI_fs_conv[y,x]) > -6.83: #threshold of polarization (smaller- wider)
      I=sum(obj_medI_a[y-dy:y+dy+1,x-dx:x+dx+1])/area
      Q=sum(obj_medQa[y-dy:y+dy+1,x-dx:x+dx+1])/area
      U=sum(obj_medUa[y-dy:y+dy+1,x-dx:x+dx+1])/area
      v=Linear_pol_vector(x_in_AU[x],y_in_AU[y],I,-Q,-U,ax,max_length=max_length,color='w')
#pyfits.writeto('obj_PI_conva_sigma05_pol.fits',v???)
draw()
show()
