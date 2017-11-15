#!/usr/bin/python2.5
"""
  This rotates Q**_inst_corrected.fits and U**_inst_corrected.fits
  (i.e., Q and U images for each sequence of retarder P.A.s).
  The files are saved as Q**_inst_corrected_rot.fits and
  U**_inst_corrected_rot.fits. 
  Note that, these are actually -Q and -U (i.e. the sign is opposite)
  as Hashimoto-kun's equation does not include the effect for rotation
  for the ADI mode (i.e., 180 deg.).
"""
from pylab import *
from pyraf import iraf
import pyfits

list_RYTau={}

###
# all
list_RYTau[0]    = 719+arange(14)*4
list_RYTau[45]   = 720+arange(14)*4
list_RYTau[22.5] = 721+arange(13)*4
list_RYTau[67.5] = 722+arange(13)*4

### get rotation angles ###

alt = 19.823806 * pi / 180.0 

# for the 1st for images

for i in range(13):
  az_list=[]
  el_list=[]
  for retarder_PA in (0,45,22.5,67.5):
    hdllist=pyfits.open("HICA00042%dfc_gch1c.fits" % list_RYTau[retarder_PA][i])
    az_list.append(hdllist[0].header['AZIMUTH'])
    el_list.append(hdllist[0].header['ALTITUDE'])
    hdllist.close()

  # Get an averaged azimuth value in rad
  az = sum(az_list)*0.25
  az = (az-180.0)*pi/180.0     # for the 1st for images

  # Get an averaged altitude (or elevation)value in rad
  el = sum(el_list)*0.25
  el*= pi/180.0 

  # Get a parameter for field rotation
  den = sin(el) * cos(az) + cos(el) * tan(alt)
  fr = arctan2(sin(az), den) * 180.0 / pi 

  fr=fr-40+180  # -40 is the rotator angle (D_IMRPAP in the fits header).
                # Replace it by +138.799 for SU Aur; +132.0020 for its ref star (HD241730).

  #print fr


  iraf.rotate(input_filename_for_Q,output_filename_for_Q,fr,xin=201,xout=201,yin=201,yout=201)
  iraf.rotate(input_filename_for_Q,output_filename_for_Q,fr,xin=201,xout=201,yin=201,yout=201)

