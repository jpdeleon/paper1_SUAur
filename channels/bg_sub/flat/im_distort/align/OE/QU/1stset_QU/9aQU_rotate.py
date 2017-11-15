#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/1stset_QU
"""
  This rotates *_Q.fits and *_U.fits at a computed angle, fr
  The files are saved as *_rotQ.fits and *_rotU.fits.
  Note that, these are actually -Q and -U (i.e. the sign is opposite)
  as Hashimoto-kun's equation does not include the effect for rotation
  for the ADI mode (i.e., 180 deg.).
  This is the first part 9a that has total of 13 sets.
  # first set: 120-171 inclusive => 171-120= 51+1 = 52/4 = 13 image sets
  <ND1> 120, 124 128
  <ND10> 132, 136, 140, 144, 148, 152, 156, 160, 164, 168
To run this, I put orig sci images (HICA*120-171)
together with 120,124,128,...168_Q and _U images. There are total of 13x2 output images.
After, I pasted the images to the rotated_QU folder.
"""
from pylab import *
from pyraf import iraf
iraf.images()
iraf.imgeom()
import pyfits

list_SUAur={}
list_SUAur[0]=120+arange(13)*4
list_SUAur[45]=121+arange(13)*4
list_SUAur[22.5]=122+arange(13)*4
list_SUAur[67.5]=123+arange(13)*4

### get rotation angles ###
alt=19.823806 * pi / 180.0 	#alt of Subaru in Mauna Kea

z=range(13)
set_name=map(lambda x:x*4, z)

#for the 1st four images
for i in range(13):		#total of 52 images in the first set
  az_list=[]
  el_list=[]
  for retarder_PA in (0,45,22.5,67.5):
    hdllist=pyfits.open("HICA00137%d.fits" % list_SUAur[retarder_PA][i])#get's the filenames of the original raw images in the folder
    az_list.append(hdllist[0].header['AZIMUTH'])			#get values in the header file
    el_list.append(hdllist[0].header['ALTITUDE'])
    hdllist.close()
  az=sum(az_list)*0.25 		# Get an averaged azimuth value in rad
  az=(az-180.0)*pi/180.0    	# for the 1st for images
  el=sum(el_list)*0.25   	# Get an averaged altitude (or elevation)value in rad
  el*=pi/180.0 
  den=sin(el)*cos(az)+cos(el)*tan(alt)   	# Get a parameter for field rotation
  fr=arctan2(sin(az),den)*180.0/pi 
  fr=fr+138.799+180  #rotator angle (D_IMRPAP in the fits header)= +138.799 for SU Aur; +132.0020 for its ref star (HD241730).
  name=set_name[i]+120
  if fr > 360: fr-=360
  elif fr < -360: fr+=360
  print fr, name
#print '\n', name

  Q_in=str(name)+'-'+str(name+3)+'_Q.fits'
  Q_out=str(name)+'-'+str(name+3)+'_rotQ.fits'
  U_in=str(name)+'-'+str(name+3)+'_U.fits'
  U_out=str(name)+'-'+str(name+3)+'_rotU.fits'

#  print q_in,q_out,u_in,u_out
  iraf.rotate(Q_in, Q_out, fr, xin=320., xout=320., yin=320., yout=320.)
  iraf.rotate(U_in, U_out, fr, xin=320., xout=320., yin=320., yout=320.)
