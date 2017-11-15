#!/usr/bin/env python

import pyfits
from glob import glob

all_info_for_print=[]
all_info={}
#make_list_RYTau_30s      = False # for making list (Default: False)
#make_list_ref_star_15s   = False # for making list (Default: False)
#make_list_dark_30s       = False # for making list (Default: False)
#make_list_dark_15s       = False # for making list (Default: False)
#make_list_domeflat_H_PDI = False # for making list (Default: False)

fitslist=glob("HICA????????.fits")
for fn in fitslist:
  a=pyfits.open(fn)
  all_info[fn]=a[0].header
  line=""
  line+=a[0].header['DATE'][-5:] # Creation UTC (CCCC-MM-DD) date of FITS header 
  line+="  "
  line+=a[0].header['P_HSTSTR'] # HST when exposure starts
  line+="  "
  line+=a[0].header['FRAMEID'] # Image sequential number 
  line+="  "
  line+="%-6s" % a[0].header['DATA-TYP'] # Type / Characteristics of this data  
  line+="  "
  line+="%-9s" % a[0].header['OBJECT'] # Target Description  
  line+="  "

  # Those are removed as COADD=1 for all the frames
  #
  #line+="%4.1f" % a[0].header['EXP1TIME'] # Each exposure time (sec)   
  #line+="  "
  #line+="%s" % a[0].header['COADD'] # number of coadd 
  #line+="  "

  line+="%4.1f" % a[0].header['EXPTIME'] # Total exposure time (sec) 
  line+="  "
  line+="%4.2f" % a[0].header['AIRMASS'] # Air Mass at start 
  line+="  "
  line+=a[0].header['FILTER01'] # Filter name/ID
  line+="  "
  line+="%-6s" % a[0].header['FILTER02'] # Filter name/ID
  line+="  "
  line+=a[0].header['FILTER03'] # Filter name/ID

  # "ADI" or "SDRL"
  line+="  "
  line+=a[0].header['P_TRMODE'] # Tracking mode of Lyot stop


  line+="  "
  line+="%-3s" % a[0].header['P_FMID'] # Field Mask ID   
  # The number below is linked with the ID (PDI=1, DI=2, SDI=3)
  #
  #line+="  "
  #line+="%d" % a[0].header['P_FMSLT'] # Slot number of field mask 

  line+="  "
  line+="%-3s" % a[0].header['P_WPID'] # Wolliston prism ID
  # The number below is linked with the ID (PDI=1, DI=2, SDI=3)
  #
  #line+="  "
  #line+="%d" % a[0].header['P_WPSLT'] # Slot number of Wollaston prism

  # Polarizer: "POLARIZER" for all the files
  #
  #line+="  "
  #line+=a[0].header['POLARIZ1'] # Name of polarizer1

  # "0." for all the files
  #
  #line+="  "
  #line+="%4.1f" % a[0].header['POL-ANG1'] # Position angle of polarizer1 (deg)
  line+="  "
  line+="%5.2f" % a[0].header['P_RTAGL1'] # Angle of retarder1 (deg)  
  line+="  "
  line+="%8.2f" % a[0].header['RET-ANG1'] # Position angle of retarder1 (deg)  
     
  # Image rotator: "0.00" or "0.01" for all
  #
  #line+="  "
  #line+="%5.2f" % a[0].header['IMGROT'] # Angle of the image rotator        

  # ADC: "NONE" "0.04" for all
  #
  #line+="  "
  #line+=a[0].header['ADC-TYPE'] # ADC name/type if used  
  #line+="  "
  #line+="%5.2f" % a[0].header['ADC'] # ADC PA during exposure (degrees)  

#  line+="  "
#  line+=a[0].header[''] # Image sequential number 
#  line+="  "

  # azimuth and elevation
  line+="  "
  line+="%8.4f" % a[0].header['AZIMUTH'] # Azimuth of telescope pointing
  line+="  "
  line+="%7.4f" % a[0].header['ALTITUDE'] # Altitude of telescope pointing

  # image rotator
  #
  # (almost zero)
  #line+="  "
  #line+="%7.3f" % a[0].header['IMGROT'] # Angle of the image rotator (tel)
  line+="  "
  line+="%7.4f" % a[0].header['D_IMRANG'] # IMR angle (deg) (AO)
  # (zero)
  #line+="  "
  #line+="%7.4f" % a[0].header['D_IMRPAD'] # IMR position angle of dec. axis (deg) 
  # (-40 deg. for RY Tau)
  line+="  "
  line+="%7.4f" % a[0].header['D_IMRPAP'] # IMR position angle (deg)
  # (same as 'D_IMRANG')
  #line+="  "
  #line+="%7.4f" % a[0].header['P_AOIMR'] # Position of AOImR (degree)

  a.close()
  all_info_for_print.append(line)

all_info_for_print.sort()

for line in all_info_for_print:
  print line

### the following lines are to make files for the list of objects, flat and dark. ###

#if make_list_RYTau_30s:
#  f=open('list_RYTau_30s.txt','w')
#  for filename in fitslist:
#    if all_info[filename]['OBJECT']  == 'RYTAU' and \
#       all_info[filename]['EXPTIME'] == 30.0:
#      #print filename,all_info[filename]['OBJECT'],all_info[filename]['EXPTIME']
#      f.write("%s\n" % filename[:-5])
#  f.close()

#if make_list_ref_star_15s:
#  f=open('list_ref_star_15s.txt','w')
#  for filename in fitslist:
#    if all_info[filename]['OBJECT']  == 'HD282411' and \
#       all_info[filename]['EXPTIME'] == 15.0:
#      #print filename,all_info[filename]['OBJECT'],all_info[filename]['EXPTIME']
#      f.write("%s\n" % filename[:-5])
#  f.close()

#if make_list_dark_15s:
#  f=open('list_dark_15s.txt','w')
#  for filename in fitslist:
#    if all_info[filename]['FILTER03']  == 'DARK' and \
#       all_info[filename]['EXPTIME'] == 15.0:
#      #print filename,all_info[filename]['FILTER03'],all_info[filename]['EXPTIME']
#      f.write("%s\n" % filename[:-5])
#  f.close()

#if make_list_dark_30s:
#  f=open('list_dark_30s.txt','w')
#  for filename in fitslist:
#    if all_info[filename]['FILTER03']  == 'DARK' and \
#       all_info[filename]['EXPTIME'] == 30.0:
#      #print filename,all_info[filename]['FILTER03'],all_info[filename]['EXPTIME']
#      f.write("%s\n" % filename[:-5])
#  f.close()

#if make_list_domeflat_H_PDI:
#  f=open('list_domeflat_H_PDI.txt','w')
#  for filename in fitslist:
#    if all_info[filename]['OBJECT']  == 'DOMEFLAT' and \
#       all_info[filename]['DATA-TYP'] == 'OBJECT':
#      #print filename,all_info[filename]['OBJECT'],all_info[filename]['EXPTIME']
#      f.write("%s\n" % filename[:-5])
#  f.close()

