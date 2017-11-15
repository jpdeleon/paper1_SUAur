#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU
'''
This file maps polarization vectors given the
convolved PI image (sigma=0.5).
obj_PI_conva_sigma05.fits
The input PI conva image can be changed with different sigma.
Change parameters such as threshold of polarization (optimum 0.61).
This files works for those are not flux calibrated.
Check 12PI_pol_vec.py for those that maps pol vectors to flux calibrated images: e.g. obj_PI_fscaled_sig05.fits
'''
from pylab import*
import pyfits
from scipy.ndimage.filters import gaussian_filter

### Constant ###
max_length     = 300       # Pol=100 % in pixel

### Classes and Modules ###
class Linear_pol_vector:
  """
    Show the vector map for linear polarization
    # modules
    __init__           plot the results
    change_max_length  scale the length of the vector, defining the length
                       for the 100 % polarization
    reset              reset the parameters for the vector    
  """
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
#      self.ang=arctan2(self.Q,self.U)*0.5
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
#obj
a=pyfits.open('obj_PI_a.fits')
obj_PI_a=a[0].data
a.close()

b=pyfits.open('obj_PI_conva_sigma05.fits')
obj_PI_convolved_a=b[0].data
b.close()

#Q
c=pyfits.open('obj_medQa.fits')
obj_medQa=c[0].data
c.close()
#U
d=pyfits.open('obj_medUa.fits')
obj_medUa=d[0].data
d.close()
#I
e=pyfits.open('obj_medI_a.fits')
obj_medI_a=e[0].data
e.close()

vmin=-10
vmax=80

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
#convert arcsec to AU; distance of object is 140 pc
extent_PI*=140 

figure(1)
clf()
ax=subplot(111)
imshow(log10(obj_PI_convolved_a),interpolation='nearest',origin='lower',vmin=0.6,vmax=2,cmap=cm.jet,extent=extent_PI)
colorbar()
title('obj_PI_conv_sig=0.5')
xlabel('AU')
ylabel('AU')

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
    if log10(obj_PI_convolved_a[y,x]) > 0.60: #threshold of polarization (smaller- wider)
      I=sum(obj_medI_a[y-dy:y+dy+1,x-dx:x+dx+1])/area
      Q=sum(obj_medQa[y-dy:y+dy+1,x-dx:x+dx+1])/area
      U=sum(obj_medUa[y-dy:y+dy+1,x-dx:x+dx+1])/area
      v=Linear_pol_vector(x_in_AU[x],y_in_AU[y],I,-Q,-U,ax,max_length=max_length,color='w')
#      PI=sqrt(Q*Q+U*U)
#      if PI > 20:
#        v=Linear_pol_vector(x,y,I,Q,U,ax,max_length=max_length,color='w',linewidth=4)
#      else:
#        v=Linear_pol_vector(x,y,I,Q,U,ax,max_length=max_length,color='k',linewidth=4)
#      varray.append(v)

#pyfits.writeto('obj_PI_conva_sigma05_pol.fits',v???)
draw()
show()
