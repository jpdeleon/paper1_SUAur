#!/usr/bin/env python
"""
  This is the second part of 9QU_rotate that rotates a total of 3 sets of images.
  215-226 inclusive = 12/4 = 3 image sets 
  <ND10>
  172 to 215, (filename changes that must be made)
  176 to 219, and 
  <ND1>
  180 to 223
  To run this, I put orig sci images in a test1 folder (215-226)
  together with 172,176,180_QU images.
  There are total of 6 output images (3 for _rotQ and 3 for _rotU)
  After, I pasted the images to the rotated_QU folder.
"""
from pylab import *
from pyraf import iraf
iraf.images()
iraf.imgeom()
import pyfits

list_SUAur={}
list_SUAur[0]=215+arange(3)*4
list_SUAur[45]=216+arange(3)*4
list_SUAur[22.5]=217+arange(3)*4
list_SUAur[67.5]=218+arange(3)*4

### get rotation angles ###
alt=19.823806 * pi / 180.0 	#alt of Subaru in Mauna Kea

z=range(3)
set_name=map(lambda x:x*4, z)

#for the 1st four images
for i in range(3):		#total of 52 images in the first set
  az_list=[]
  el_list=[]
  for retarder_PA in (0,45,22.5,67.5):
    hdllist=pyfits.open("HICA00137%d.fits" % list_SUAur[retarder_PA][i])
    az_list.append(hdllist[0].header['AZIMUTH'])
    el_list.append(hdllist[0].header['ALTITUDE'])
    hdllist.close()
  az=sum(az_list)*0.25 # Get an averaged azimuth value in rad
  az=(az-180.0)*pi/180.0     # for the 1st for images
  el=sum(el_list)*0.25   # Get an averaged altitude (or elevation)value in rad
  el*=pi/180.0 
  den=sin(el)*cos(az)+cos(el)*tan(alt)   # Get a parameter for field rotation
  fr=arctan2(sin(az),den)*180.0/pi 
  fr=fr+138.799+180  #rotator angle (D_IMRPAP in the fits header)= +138.799 for SU Aur; +132.0020 for its ref star (HD241730).
  name=set_name[i]+172	#start
  if fr > 360: fr-=360
  elif fr < -360: fr+=360 
#  print fr, name
  q_in=str(name)+'-'+str(name+3)+'_Q.fits'
  u_in=str(name)+'-'+str(name+3)+'_U.fits'
  q_out=str(name)+'-'+str(name+3)+'_rotQ.fits'
  u_out=str(name)+'-'+str(name+3)+'_rotU.fits'
#  print q_in,q_out,u_in,u_out
  iraf.rotate(q_in, q_out, fr, xin=320., xout=320., yin=320., yout=320.)
  iraf.rotate(u_in, u_out, fr, xin=320., xout=320., yin=320., yout=320.)
