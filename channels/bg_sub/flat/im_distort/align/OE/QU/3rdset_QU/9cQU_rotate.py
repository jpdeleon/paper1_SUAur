#!/usr/bin/env python
"""
  This is the third part of 9QU_rotate that rotates a total of 8 sets of *_Q and *_U images.
  271-240 inclusive = 32/4 = 8 image sets 
  <ND10> 184 to 240, 188 to 244, 192 to 248, 196 to 252, 200 to 256, 204 to 260, 208 to 264, and 
  212 to 268 (filename changes that must be made)
  To run this, I put orig sci images in a test2 folder (240-271)
  together with 184,188,..,212_QU images.
  There are total of 16 output images (8 for _rotQ and 8 for _rotU).
  Note that this is for ref star (HD241730).
  Main difference from a and b is the rotator angle value.
"""
from pylab import *
from pyraf import iraf
iraf.images()
iraf.imgeom()
import pyfits

list_SUAur={}
list_SUAur[0]=240+arange(8)*4	#240 is the starting image (HICA*249.fits)
list_SUAur[45]=241+arange(8)*4
list_SUAur[22.5]=242+arange(8)*4
list_SUAur[67.5]=243+arange(8)*4

### get rotation angles ###
alt=19.823806 * pi / 180.0 	#alt of Subaru in Mauna Kea

z=range(8)
set_name=map(lambda x:x*4, z)

#for the 1st four images
for i in range(8):		#total of 52 images in the first set
  az_list=[]
  el_list=[]
  for retarder_PA in (0,45,22.5,67.5):
    hdllist=pyfits.open("HICA00137%d.fits" % list_SUAur[retarder_PA][i])
    az_list.append(hdllist[0].header['AZIMUTH'])
    el_list.append(hdllist[0].header['ALTITUDE'])
    hdllist.close()
  az=sum(az_list)*0.25 		# Get an averaged azimuth value in rad
  az=(az-180.0)*pi/180.0     	# for the 1st for images
  el=sum(el_list)*0.25   	# Get an averaged altitude (or elevation)value in rad
  el*=pi/180.0 
  den=sin(el)*cos(az)+cos(el)*tan(alt)   # Get a parameter for field rotation
  fr=arctan2(sin(az),den)*180.0/pi 
  fr=fr+132.0020+180  		#rotator angle (D_IMRPAP in the fits header)= +132.0020 for its ref star (HD241730).
  name=set_name[i]+184		#start
  if fr > 360: fr-=360
  elif fr < -360: fr+=360 
  print fr
  q_in=str(name)+'-'+str(name+3)+'_Q.fits'
  u_in=str(name)+'-'+str(name+3)+'_U.fits'
  q_out=str(name)+'-'+str(name+3)+'_rotQ.fits'
  u_out=str(name)+'-'+str(name+3)+'_rotU.fits'
#  print q_in,q_out,u_in,u_out
  iraf.rotate(q_in, q_out, fr, xin=320., xout=320., yin=320., yout=320.)
  iraf.rotate(u_in, u_out, fr, xin=320., xout=320., yin=320., yout=320.)
