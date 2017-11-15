#!/usr/bin/env python
'''
xdg-open file.py
~/.bashrc
alias go='xdg-open'

PS1='\u:\W\$'
python filename.py&

chmod +x filename.py
filename.py
'''
'''
>>additive errors: bias offset & dark current
correction: 
>dark frames (mage taken by the CCD for the same exposure length as the exposure it is meant 
to correct (it should also be taken at the same CCD operating temperature; will correct both bias and offset)
>bias frames ( zero length dark frame, so it corrects bias offset, but not dark current)
>>multiplicative errors: arise from differences in QE, illumination (vignetting), and dust halos.
correction: flat field (mage of an evenly illuminated field (usually a white spot on the inside of the dome)
*cosmic rays: uncommon error source

FINAL_IMAGE= (raw_image - dark1)/ [(flat - dark2)/(flat - dark 2)]

^combine darks, subtract darks, combine flats, normalize flat, *divide flats, align images for stacking, combine images
*things actually done in this file
'''
***********************************************************************************
###>>>>>>>>>>1. Extract images
'''
FILENAME: 1cropping.py
#cd ~/Desktop/SU_Aur_backup/channels
This file crops the four channels from the original raw image
and saves them as individual .fits file e.g. HICA*_ch1.fits.
There are 4 channels in each science images.
The program is run on ipython -pylab
'''
from pylab import *
from pyraf import iraf
import glob

ch1='[60:669,1100:1739]' 	#This channel refers to wavelength of 1.624 microns
ch2='[695:1334,1100:1739]' 	#1.600
ch3='[755:1394,415:1054]' 	#1.575
ch4='[1395:2034,410:1049]' 	#1.644
file_list=glob.glob('HICA*.fits')
file_list=list(file_list)
file_list.sort()

for filename in file_list:
#filename changes from file_list[0-n]; e.g. 'HICA*120.fits -> HICA*271.fits'
    filename=filename.translate(None, '.fits')
    a1=filename+ch1
    b1=filename+'_ch1'
    a2=filename+ch2
    b2=filename+'_ch2'
    a3=filename+ch3
    b3=filename+'_ch3'
    a4=filename+ch4
    b4=filename+'_ch4'
#   print filename, a1, b1, a2, b2, a3, b3, a4, b4
    iraf.imcopy(a1,b1) ##extract (crop) the 4 portions of the image file and 
    iraf.imcopy(a2,b2) ##save using the filename[i]
    iraf.imcopy(a3,b3)
    iraf.imcopy(a4,b4)

***********************************************************************************
###>>>>>>>>>>2. background subtraction
'''
FILENAME: 2test_median_all.py
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub
This file is used to do background subtraction by subtracting the median of the pixel values 
(intensity) in the images excluding the bright central source.
The mean was not used because it is susceptible with outliers (pixels with erroneous values) 
and so will likely yield erroneous results.
The output is 'HICA*_ch1b.fits'.
The program is run in ipython -pylab
'''
from pylab import *
import pyfits
import glob
file_list=glob.glob('HICA*')
file_list=list(file_list)
file_list.sort()

for filename in file_list: #subtract the background to all the science images (ch1-ch4)
  a=pyfits.open(filename)
  image=copy(a[0].data)
  a.close()
  for y in range(image.shape[0]):
    med1=median(image[y,:100]) #take the median of y-values from 0:100 (101-499 is omitted because it contains bright star)
    med2=median(image[y,-100:])#take the median of y-values from 500:600
    image[y]-=(med1+med2)*0.5 #bg is subtracted by subtracting the average of the median of pixels along x-values considered above to y-values
    filename=filename.translate(None, '.fits') #remove '.fits' from filename to be appended as 'b.fits'
#figure(1)
#clf()
#imshow(image,vmin=-20,vmax=20)
#show()

#Saving fits files
  hdu = pyfits.PrimaryHDU(image) #retain header file
  hdulist = pyfits.HDUList([hdu])
  hdulist.writeto(filename+'b.fits') #save as 'HICA*b.fits'
  hdulist.close()

***********************************************************************************
###>>>>>>>>>>3. flat fielding
'''
FILENAME: 3test_flat.py
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat
This file is used to make flattened images using background-subtracted images and dividing them 
by the given flat images (e.g. flat_ch1.fits).
The output is 'HICA*_ch1bf.fits'.
The program is run in pyraf
'''
from pylab import *
import pyfits
import glob
file_list1=glob.glob('HICA*ch1b.fits')
file_list2=glob.glob('HICA*ch2b.fits')
file_list3=glob.glob('HICA*ch3b.fits')
file_list4=glob.glob('HICA*ch4b.fits')
file_list1=list(file_list1)
file_list2=list(file_list2)
file_list3=list(file_list3)
file_list4=list(file_list4)
file_list1.sort()
file_list2.sort()
file_list3.sort()
file_list4.sort()

for filename1 in file_list1: #loop to all the science images (ch1b)
  fname1=filename1[:-5]+'f.fits'
  #print filename1,fname1
  iraf.imarith(filename1,'/','flat_ch1',fname1)#make flat field by dividing flat
for filename2 in file_list2: #loop to all the science images (ch2b)
  fname2=filename2[:-5]+'f.fits'
  #print filename1,fname2
  iraf.imarith(filename2,'/','flat_ch2',fname2)
for filename3 in file_list3: #loop to all the science images (ch3b)
  fname3=filename3[:-5]+'f.fits'
  #print filename1,fname3
  iraf.imarith(filename3,'/','flat_ch3',fname3)
for filename4 in file_list4: #loop to all the science images (ch4b)
  fname4=filename4[:-5]+'f.fits'
  #print filename4,fname4
  iraf.imarith(filename4,'/','flat_ch4',fname4)

***********************************************************************************
###>>>>>>>>>>4. correct image distortion due to instrumental errors such as optical aberration 
'''
FILENAME: 4im_distort.py
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort
This file is used to correct geometrical distortion caused by the imperfection in the optics.
This file makes use of the given .db files.
The output is 'HICA*_ch1bfg.fits'.
The program is run in ipython -pylab
'''
from pylab import *
import pyfits
import glob

file_list1=glob.glob('HICA*ch1b.fits')
file_list2=glob.glob('HICA*ch2b.fits')
file_list3=glob.glob('HICA*ch3b.fits')
file_list4=glob.glob('HICA*ch4b.fits')
file_list1=list(file_list1)
file_list2=list(file_list2)
file_list3=list(file_list3)
file_list4=list(file_list4)
file_list1.sort()
file_list2.sort()
file_list3.sort()
file_list4.sort()

for filename1 in file_list1:
  fname1=filename1[:-5]+'g.fits'
  iraf.geotran(filename1,fname1,database='ch1_2014Jan.db',transfor='ch1_2014Jan.dat')
for filename2 in file_list2:
  fname2=filename2[:-5]+'g.fits'
  iraf.geotran(filename2,fname2,database='ch2_2014Jan.db',transfor='ch2_2014Jan.dat')
for filename3 in file_list3:
  fname3=filename3[:-5]+'g.fits'
  iraf.geotran(filename3,fname3,database='ch3_2014Jan.db',transfor='ch3_2014Jan.dat')
for filename4 in file_list4:
  fname4=filename4[:-5]+'g.fits'
  iraf.geotran(filename4,fname4,database='ch4_2014Jan.db',transfor='ch4_2014Jan.dat')

***********************************************************************************
###>>>>>>>>>>5. get QU images: QU images refers to that which have linear polarization
#>>>>>5.1 align all 4 channels to each other
'''
FILENAME: 5test_align.py
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align
This file is used to align a series of (up to 9) channel 2 images with respect to channel 1.
This is done by providing a combination of test values in x_list and y_list
corresponding to the pixel by which the channel will be shifted.
The outputs (e.g. 241ch4_1, 241ch4_2,etc.) are viewed in ds9 (9 frames, tile view)
From the output, the best image with best alignment is chosen.
The 1st row shows increasing shift in x.
The 1st column shows increasing shift in y.
The code is run in ipython -pylab
'''
#Get only the shift values that you need. Afterwards, delete all the unnecessary images just made.
#>>>>>
from pylab import *
from pyraf import iraf
#These are the best value for 240. This shift values can be applied to all images
#ch2: 0.7,0.3
#ch3: -0.1,0.3
#ch4: 0.2,0.5
filename_ch1='HICA00137241_ch1bfg.fits'
filename_ch2='HICA00137241_ch2bfg.fits'
filename_ch3='HICA00137241_ch3bfg.fits'
filename_ch4='HICA00137241_ch4bfg.fits'

x_list=[0.0,0.2,0.4]
y_list=[0.3,0.5,0.7]

n=1
iraf.imdel('241ch4_?.fits') #delete: program can't overwrite files

for y in y_list:
  for x in x_list:
    iraf.imshift(filename_ch4,'shifted',x,y)
    filename_output='241ch4_%d' % n 
    iraf.imarith(filename_ch1,'-','shifted',filename_output)
    iraf.disp(filename_output,n)
    n=n+1
    iraf.imdel('shifted')

***********************************************************************************
#The next program is used to check if the alignment holds good to all other images
'''
FILENAME: 5bulk_align.py
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align
This file is used to check whether shifting in x and y of channels 2 to 4 with respect to channel 1
will yield good results. This is done by doing <imarith channel 1 - shifted channel2,3,4>.
In other words, their PSF is aligned and then subtracted.
The output is image_num_ch2,3,4 (e.g. 240_ch2.fits) which can be viewed using ds9.
The image shows good alignment if black (oversubtraction) and white (residue) regions are centrosymmetric.
The file is run in pyraf.
'''
#>>>>>
from pylab import *
from pyraf import iraf
import glob

#ch2: 
ch2_x=0.7
ch2_y=0.3
#ch3: 
ch3_x=-0.1
ch3_y=0.3
#ch4: 
ch4_x=0.2
ch4_y=0.5

file_list=glob.glob('HICA*_ch1bfg.fits')
file_list=list(file_list)
file_list.sort()

for filename_tmp in file_list:
  filename_org=filename_tmp[:-12]
  filename_ch1=filename_org+'_ch1bfg'
  filename_ch2=filename_org+'_ch2bfg'
  filename_ch3=filename_org+'_ch3bfg'
  filename_ch4=filename_org+'_ch4bfg'
#  print filename_ch1,filename_ch2,filename_ch3,filename_ch4

##shifting and subtraction of channel 2 from channel 1
  iraf.imshift(filename_ch2,'shiftxy2',ch2_x,ch2_y) #shiftxy is the shifted output image (temporary file)
  fname_out2=filename_ch2[9:-7]+'_ch2' #retrive only the image number (e.g. 240)
  print "\n", fname_out2
#  raw_input()
  iraf.imarith(filename_ch1,'-','shiftxy2',fname_out2) #subtract ch1 to ch2
  iraf.imdel('shiftxy2') #delete temporary image file

##shifting and subtraction of channel 3 from channel 1
  iraf.imshift(filename_ch3,'shiftxy3',ch3_x,ch3_y)
  fname_out3=filename_ch3[9:-7]+'_ch3'
  print "\n", fname_out3
  iraf.imarith(filename_ch1,'-','shiftxy3',fname_out3)
  iraf.imdel('shiftxy3')

##shifting and subtraction of channel 4 from channel 1
  iraf.imshift(filename_ch4,'shiftxy4',ch4_x,ch4_y)
  fname_out4=filename_ch4[9:-7]+'_ch4'
  print "\n", fname_out4
  iraf.imarith(filename_ch1,'-','shiftxy4',fname_out4)
  iraf.imdel('shiftxy4')

***********************************************************************************
'''
FILENAME: OE_&_I.py
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE
This file computes for OE rays and intensity of aligned science images (120-271).
1) OE rays: (ch1+ch3) - (ch2+ch4)
2) I- intensity: (ch1+ch3) + (ch2+ch
This is done by first shifting ch2, ch3, and ch4 with respect to ch1 of the same images.
Due to good alignment, results show that OE images have centrosymmetric pattern 
(i.e. no over subtraction outside the central bright region).
Moreover, I images seem to have been improved.
Sample images include: oe2.png, oe3.png, oe_i.png, 120_121_122_269_270_271.png.
This file is run in ipython -pylab.
'''
from pylab import *
from pyraf import iraf
import glob
import pyfits
#ch2: 
ch2_x=0.7
ch2_y=0.3
#ch3: 
ch3_x=-0.1
ch3_y=0.3
#ch4: 
ch4_x=0.2
ch4_y=0.5

file_list=glob.glob('HICA*_ch1bfg.fits')
file_list=list(file_list)
file_list.sort()

for filename_tmp in file_list:
  filename_org=filename_tmp[:-12]
  filename_ch1=filename_org+'_ch1bfg'
  filename_ch2=filename_org+'_ch2bfg'
  filename_ch3=filename_org+'_ch3bfg'
  filename_ch4=filename_org+'_ch4bfg'
  print "\n", filename_ch1,filename_ch2,filename_ch3,filename_ch4

  iraf.imshift(filename_ch3,'shiftxy3',ch3_x,ch3_y)
#O:(ch1+ch3)  
  out_ch1ch3=filename_ch1[9:-7]+'_ch1ch3.fits'
  iraf.imarith(filename_ch1,'+','shiftxy3',out_ch1ch3)
  iraf.imdel('shiftxy3')

  iraf.imshift(filename_ch2,'shiftxy2',ch2_x,ch2_y)
  iraf.imshift(filename_ch4,'shiftxy4',ch4_x,ch4_y)
#E: (ch2+ch4)
  shiftxy2='shiftxy2.fits'
  out_ch2ch4=filename_ch1[9:-7]+'_ch2ch4.fits'
  iraf.imarith(shiftxy2,'+','shiftxy4',out_ch2ch4)
  iraf.imdel('shiftxy2')
  iraf.imdel('shiftxy4')
#OE rays: (ch1+ch3) - (ch2+ch4)
  oe=filename_ch1[9:-7]+'_oe.fits' #retrive only the image number (e.g. 240_oe)
  iraf.imarith(out_ch1ch3,'-',out_ch2ch4,oe)
#I: (ch1+ch3) + (ch2+ch4)
  I=filename_ch1[9:-7]+'_I'
  iraf.imarith(out_ch1ch3,'+',out_ch2ch4,I)
  iraf.imdel('out_ch1ch3')
  iraf.imdel('out_ch2ch4') 

***********************************************************************************
###>>>>> compute for more accurate I and then Q and U
'''
FILENAME: test_IP3.py
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU
required file: IP_SUAur_20140119.txt
This file is used to compute for Q and U (corrected).
Previously, Q and U were computed by simply adding or subtracting pairs of 
summed channels (ie. I=(ch1+ch3)+(ch2+ch4) [see test_oe.py].
This then accounts for corrections to better aprroximate ~Q and ~U.
First, the columns (=Xij) of the .txt file is scanned.
Naming scheme for columns, left to right is: 
image_no, x11,x12,x13,x14; x21,x22,x23,x24
Xij are important in computing for a,b,c,d & p,q,r,s
Try first set only:120(0),121(45),122(22.5),123(67.5),
where (n)= half-wave plate angle
[120_I/x11,120 + 121_I/x11,121 + 122_I/x11,122 + 123_I/x11,123]/4
Then, compute for a,b,c,d and p,q,r,s for image no. 120-123.
Finally, compute for:
Q ~ {[(a/d)-(p/s)] - [(b/d)-(q/s)]*I} / [(c/d) - (r/s)]
U ~ (a - bI - cQ) / d
'''
from pylab import *
import pyfits
from pyraf import iraf 
import glob
import numpy

#A. Compute for more accurate I
#MANUAL METHOD: manually changing filenames
#SigmaI_subj~(o_subj + e_subj)/x11;j where j=4 ->{120,121,122,123}
loadfile=loadtxt('IP_SUAur_20140119',dtype=str) #convert all values to string

file_list_I=glob.glob('*_I.fits')
file_list_I=list(file_list_I)
file_list_I.sort()

numofimage_I=len(file_list_I)	                #used to consider total no. of images in file_list_I

x11_all=loadfile[:,1]		                #x11 parameter corresponds to 2nd column in txt file [:,1]

#list=range(numofimage_I)
list=range(4)			                #test only the first 4 science images: 120-123
x11=range(len(x11_all))		                #define the length of x11 array
m=0
for m in list:			                #!!! change list to len(numofimage_I) to generalize
  x11[m]=float(loadfile[m,1])                   ##load x11 values 

#open all images and put it in hdu_list_I
hdu_list_I=range(numofimage_I)		        #define hdu_list_I,hdu_I,image_list as an array
hdu_I=range(numofimage_I)                       #their length must equal the number of image files
image_list_I=range(numofimage_I)

for f in hdu_list_I:			        #iterate to all image filenames
  hdu_list_I[f]= pyfits.open(file_list_I[f])    #hdu_list_I contains info of fits files (images)
#  print "\n", hdu_list_I[f]		
  hdu_I[f]=hdu_list_I[f][0]		        #hdu_I contains the data [0] of images
  image_list_I[f]=zeros((640,640)) 	        #fill up image_list with zero-matrices with size equal to fits image data 640sq.pix.
  image_list_I[f]=hdu_I[f].data			#append the image_list with the actual image data

#A=120_I/x11,120
A=image_list_I[0]/x11[0]
#B=121_I/x11,121
B=image_list_I[1]/x11[1]
#AB=A+B 
AB=A+B						#I think calculating by each term reduces errors
#C=122_I/x11,122
C=image_list_I[2]/x11[2]
#D=123_I/x11,123
D=image_list_I[3]/x11[3]
#CD=C+D
CD=C+D
#ABCD=AB+CD
ABCD=AB+CD
#I=ABCD/4
I=ABCD/4
#save file
pyfits.writeto('120-123_I.fits',I)		#!!!generalize naming system

***********************************************************************************
###***#>>>>>GENERALIZED- applicable to all images
'''
FILENAME: 7IP_cor_set.py
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/I_corrected
required file: IP_SUAur_20140119.txt
This file is used to compute for Q and U (corrected). Before, Q and U were computed by 
simply adding or subtracting pairs of summed  channels (ie. I=(ch1+ch3)+(ch2+ch4) [see test_oe.py].
This then accounts for corrections to better aprroximate ~Q and ~U.
First, the columns (=Xij) of the .txt file is scanned.
Naming scheme for columns, left to right is: 
image_no, x11,x12,x13,x14; x21,x22,x23,x24
Xij are important in computing for a,b,c,d & p,q,r,s
Try first set only:120(0),121(45),122(22.5),123(67.5),
where (n)= half-wave plate angle
[120_I/x11,120 + 121_I/x11,121 + 122_I/x11,122 + 123_I/x11,123]/4
check test_IP3.py for manual input and saving with more comments
'''
from pylab import *
import pyfits
from pyraf import iraf 
import glob
import numpy

loadfile1=loadtxt('IP_SUAur_20140119',dtype=str)
loadfile2=loadtxt('IP_SUAur_ref_20140119',dtype=str)
loadfile=list(loadfile1)
loadfile.extend(list(loadfile2))
loadfile=array(loadfile)	

file_list_I=glob.glob('*_I.fits')
file_list_I=list(file_list_I)
file_list_I.sort()

numofimage_I=len(file_list_I)
x11_all=loadfile[:,1]
x11=range(len(x11_all))	

for m in range(numofimage_I):			         
  x11[m]=float(loadfile[m,1]) 
  
hdu_list_I=range(numofimage_I)
hdu_I=range(numofimage_I)
image_list_I=range(numofimage_I)

for f in hdu_list_I:
  hdu_list_I[f]= pyfits.open(file_list_I[f])
#  print "\n", hdu_list_I[f]		
  hdu_I[f]=hdu_list_I[f][0]
  image_list_I[f]=zeros((640,640))
  image_list_I[f]=hdu_I[f].data

z=(numofimage_I)/4
zz=range(z)
set_I=map(lambda x:x*4, zz) #replaces set elements with {0,4,8,12,...,N}

for num1 in set_I:
#  print num
#A=120_I/x11,120
  A=image_list_I[num1]/x11[num1]
#B=121_I/x11,121
  B=image_list_I[num1+1]/x11[num1+1]
#AB=A+B 
  AB=A+B
#C=122_I/x11,122
  C=image_list_I[num1+2]/x11[num1+2]
#D=123_I/x11,123
  D=image_list_I[num1+3]/x11[num1+3]
  #CD=C+D
  CD=C+D
#ABCD=AB+CD
  ABCD=AB+CD
  #I=ABCD/4
  I=ABCD/4
  #save file
  num1=num1+120
  I_name='I_'+str(num1)+'.fits'
  pyfits.writeto(I_name,I)  #you should correct the problem in saving name
# first set: 120-171 inclusive => 171-120= 51+1 = 52/4 = 13 image sets
# so rename starting image no. 120+(13*4)=172 to 
# next set: 215-226 inclusive => 3 image sets
# so rename 172 to 215, 176 to 219, and 180 to 223
# next set: 240-271 => 8 image sets
# so rename 184 to 240, 188 to 244, 192 to 248, 196 to 252, 200 to 256, 204 to 260, 208 to 264, and 212 to 268

***********************************************************************************
##>>>>>B. Compute for Q and U 
#MANUAL METHOD: manually changing filenames
'''
FILENAME: test_IP3.py
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU
required file: IP_SUAur_20140119.txt
DESCRIPTION: This file is used to compute for Q and U (corrected).
Previously, Q and U were computed by simply adding or subtracting pairs of summed channels 
(ie. I=(ch1+ch3)+(ch2+ch4) [see test_oe.py].
This then accounts for corrections to better aprroximate ~Q and ~U.
First, the columns (=Xij) of the .txt file is scanned.
Naming scheme for columns, left to right is: 
image_no, x11,x12,x13,x14; x21,x22,x23,x24
Xij are important in computing for a,b,c,d & p,q,r,s
Try first set only:120(0),121(45),122(22.5),123(67.5), where (n)= half-wave plate angle
[120_I/x11,120 + 121_I/x11,121 + 122_I/x11,122 + 123_I/x11,123]/4
Then, compute for a,b,c,d and p,q,r,s for image no. 120-123.
Finally, compute for:
Q ~ {[(a/d)-(p/s)] - [(b/d)-(q/s)]*I} / [(c/d) - (r/s)]
U ~ (a - bI - cQ) / d
'''
from pylab import *
import pyfits
from pyraf import iraf 
import glob
import numpy

#SigmaI_subj~(o_subj + e_subj)/x11;j where j=4 ->{120,121,122,123}
loadfile1=loadtxt('IP_SUAur_20140119',dtype=str) #convert all values to string
loadfile2=loadtxt('IP_SUAur_ref_20140119',dtype=str)
loadfile=list(loadfile1)
loadfile.extend(list(loadfile2))		#append textfile 1 and 2 together
loadfile=array(loadfile)			#this fixes the problem with array something

file_list_I=glob.glob('*_I.fits')
file_list_I=list(file_list_I)
file_list_I.sort()

numofimage_I=len(file_list_I)	                #used to consider total no. of images in file_list_I
x11_all=loadfile[:,1]		                #x11 parameter corresponds to 2nd column in txt file [:,1]

#list=range(numofimage_I)
#list=range(4)			                #test only the first 4 science images: 120-123
x11=range(len(x11_all))		                #define the length of x11 array

# lists are used to check if x11, x21, ... have the same len as number of science images
#x11={}, x21={}, x22={}, x23={}, x24={}

for m in range(numofimage_I):			#!!! change list to len(numofimage_I) to generalize
  x11[m]=float(loadfile[m,1])                   ##load x11 values 

#open all images and put it in hdu_list_I
hdu_list_I=range(numofimage_I)		        #define hdu_list_I,hdu_I,image_list as an array
hdu_I=range(numofimage_I)                       #their length must equal the number of image files
image_list_I=range(numofimage_I)

for f in hdu_list_I:			        #iterate to all image filenames
  hdu_list_I[f]= pyfits.open(file_list_I[f])    #hdu_list_I contains info of fits files (images)
#  print "\n", hdu_list_I[f]		
  hdu_I[f]=hdu_list_I[f][0]		        #hdu_I contains the data [0] of images
  #image_list_I[f]=zeros((640,640)) 	        #fill up image_list with zero-matrices with size equal to fits image data 640sq.pix.
  image_list_I[f]=hdu_I[f].data			#append the image_list with the actual image data

num=0
#A=120_I/x11,120
A=image_list_I[num]/x11[num]			#to compute for other sets of images,eg.268- 271, 
#B=121_I/x11,121				#change I[0] to I[89]
B=image_list_I[num+1]/x11[num+1]
#AB=A+B 
AB=A+B						#I think calculating by each term reduces errors
#C=122_I/x11,122
C=image_list_I[num+2]/x11[num+2]
#D=123_I/x11,123
D=image_list_I[num+3]/x11[num+3]
#CD=C+D
CD=C+D
#ABCD=AB+CD
ABCD=AB+CD
#I=ABCD/4
I=ABCD/4
#save file
#pyfits.writeto('268_269_270_271_.fits',I)	#!generalize naming system

####>>>>>2. Compute for constants
file_list_oe=glob.glob('*_oe.fits')
file_list_oe=list(file_list_oe)			#fix this issue: "list not callable"
file_list_oe.sort()

x21_all=loadfile[:,5]                           #load other parameters
x22_all=loadfile[:,6]
x23_all=loadfile[:,7]
x24_all=loadfile[:,8]

x21=range(len(x21_all))                         #make arrays with length equal to total number of x21 corresponding to 
x22=range(len(x22_all))				#all science images and fill it up with dummy numbers using range function
x23=range(len(x23_all))
x24=range(len(x24_all))

numofimage_oe=len(file_list_oe)                 #I think numofimage_oe = *_I

for v in range(numofimage_oe):			#change list to len(numofimage_o) to generalize
  x21[v]=float(loadfile[v,5])                   #load x2? with real values
  x22[v]=float(loadfile[v,6])
  x23[v]=float(loadfile[v,7])
  x24[v]=float(loadfile[v,8])

hdu_list_oe=range(numofimage_oe)                #make a mirror list for _oe
hdu_oe=range(numofimage_oe)
image_list_oe=range(numofimage_oe)

for g in hdu_list_oe:
  hdu_list_oe[g]= pyfits.open(file_list_oe[g])
#  print "\n", hdu_list_oe[g]		
  hdu_oe[g]=hdu_list_oe[g][0]			
  image_list_oe[g]=zeros((640,640))		#image_list_oe[0].shape
  image_list_oe[g]=hdu_oe[g].data

a='120_oe_minus_121_oe.fits'			#!
#a=120_oe - 121_oe {matrix}
#iraf.imarith(image_list_oe[0],'-',image_list_oe[1],a)
iraf.imarith(file_list_oe[num],'-',file_list_oe[num+1],a)

open_a= pyfits.open(a)				#!		
image_a=open_a[0].data
#rm('120_oe_minus_121_oe.fits')
iraf.imdel('a')

#b=x21,120 - x21,121 {const}
b=x21[num] - x21[num+1]				#!
#c=x22,120 - x22,121 {const}
c=x22[num] - x22[num+1]
#d=x23,120 - x23,121 {const}
d=x23[num] - x23[num+1]

p='121_oe_minus_122_oe.fits'			#!
#p=122_oe - 123_oe {matrix}
iraf.imarith(file_list_oe[num+2],'-',file_list_oe[num+3],p)		#!

open_p= pyfits.open(p)				#!	
image_p=open_p[0].data
#rm('122_oe_minus_123_oe.fits')
iraf.imdel('p')

#q=x21,122 - x21,123 {const}
q=x21[num+2] - x21[num+3]			#!
#r=x22,122 - x22,123v{const}
r=x22[num+2] - x22[num+3]
#s=x23,122 - x23,123 {const}
s=x23[num+2] - x23[num+3]

#3. Compute for Q
#Q~{[(a/d)-(p/s)]-[(b/d)-(q/s)]*I}/[(c/d)-(r/s)]
#numerator of Q; E=a{matrix}/d{const}; E={matrix}
E=image_a/d
#F=p{matrix}/a{const}; F={matrix}
F=image_p/s
#EF={matrix}; EF=E-F; 
EF=E-F
#G={const}
G=b/d
#H={const}
H=q/s
#GH={const}
GH=G-H
#GHI={matrix}
GHI=I*GH
#EFGHI={matrix}
EFGHI=EF-GHI
#denominator of Q
J=c/d
K=r/s
JK=J-K
Q=EFGHI/JK
#savefile
pyfits.writeto('120-123_Q.fits',Q)		#! filename

##4. Compute for U
#U~(a-bI-cQ)/d
bI=I*b
cQ=Q*c
abI=image_a-bI					#! image_a
num_U= abI-cQ
U=num_U/d
#savefile
pyfits.writeto('120-123_U.fits',U)		#! filename

***********************************************************************************
###>>>>>GENERALIZED CODE
'''
FILENAME: 8UQ_set.py
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU
This file is computes the U and Q (Stokes parameters) for a set of images 
per full half-wave plate cycle (0,45,22.5,67.5).
The given txt files are required to obtain the x?? values needed for computing the U and Q.
This also requires the output of 7I_cor_set.py which are more accurate computation of I images 
for the same set.
It does this by loading the total of 24 image data and putting them in a list called image_list_I.
Just like in 7I_cor_set.py, I_172.fits must be renamed to 215 and so on.
'''
from pylab import *
import pyfits
from pyraf import iraf 
import glob
import numpy

loadfile1=loadtxt('IP_SUAur_20140119',dtype=str)
loadfile2=loadtxt('IP_SUAur_ref_20140119',dtype=str)
loadfile=list(loadfile1)
loadfile.extend(list(loadfile2))
loadfile=array(loadfile)	

###2. Compute for constants
file_list_oe=glob.glob('*_oe.fits')
file_list_oe=list(file_list_oe)
file_list_oe.sort()

x21_all=loadfile[:,5]                           #load other x2? parameters
x22_all=loadfile[:,6]
x23_all=loadfile[:,7]
x24_all=loadfile[:,8]

x21=range(len(x21_all))                         #make arrays with length equal to total number of x21 corresponding to 
x22=range(len(x22_all))				#all science images and fill it up with dummy numbers using range function
x23=range(len(x23_all))
x24=range(len(x24_all))

numofimage_oe=len(file_list_oe)                 #I think numofimage_oe = *_I
numofimage_I=numofimage_oe

z=(numofimage_oe)/4
zz=range(z)
set_oe=map(lambda x:x*4, zz) 			#multiplies 4 element-wise to zz => {0,4,8,12,...,N}, where N= (numofimage_oe)-4

#load I matrices computed in 7I_core_set.py
file_list_I=glob.glob('I_*.fits')		#refers to file output of 7I_cor_set.py (e.g. I_120)
file_list_I=list(file_list_I)
file_list_I.sort()				#file_list_I contains 24 image filenames; len(file_list_I)=24 

hdu_list_I=range(len(file_list_I))		#hdu_list now contains only 24 items, NOT 96!
hdu_I=range(len(file_list_I))			
image_list_I=range(len(file_list_I))

for f in hdu_list_I:
  hdu_list_I[f]= pyfits.open(file_list_I[f]) 
#  print "\n", hdu_list_I[f]		
  hdu_I[f]=hdu_list_I[f][0]
  image_list_I[f]=zeros((640,640))		#make again a dummy matrices
  image_list_I[f]=hdu_I[f].data			#load only the data

for v in range(numofimage_oe):                  #numofimage_oe=96
  x21[v]=float(loadfile[v,5])                   #load x2? with real values
  x22[v]=float(loadfile[v,6])
  x23[v]=float(loadfile[v,7])
  x24[v]=float(loadfile[v,8])

hdu_list_oe=range(numofimage_oe)                #make a mirror list for _oe
hdu_oe=range(numofimage_oe)
image_list_oe=range(numofimage_oe)

for g in hdu_list_oe:
  hdu_list_oe[g]= pyfits.open(file_list_oe[g])
#  print "\n", hdu_list_oe[g]		
  hdu_oe[g]=hdu_list_oe[g][0]			
  image_list_oe[g]=zeros((640,640))		#image_list_oe[0].shape
  image_list_oe[g]=hdu_oe[g].data

z=(numofimage_oe)/4 
zz=range(z) 
set_I=map(lambda x:x*4, zz)

for num2 in set_I:				# set_I=set_oe
  name=num2+120
  a=str(name)+'oe_minus_'+str(name+1)+'oe.fits'	#'120_oe_minus_121_oe.fits'
  iraf.imarith(file_list_oe[num2],'-',file_list_oe[num2+1],a)
  open_a= pyfits.open(a)
  image_a=open_a[0].data
#rm('120_oe_minus_121_oe.fits')
  iraf.imdel(a)					#need not to save as .fits in the folder
#b=x21,120 - x21,121 {const}			#a,b,c,d requires ch1 [num2] and ch2
  b=x21[num2] - x21[num2+1]
#c=x22,120 - x22,121 {const}
  c=x22[num2] - x22[num2+1]
#d=x23,120 - x23,121 {const}
  d=x23[num2] - x23[num2+1]  
  p=str(name+2)+'oe_minus_'+str(name+3)+'oe.fits'	#'122_oe_minus_123_oe.fits'
  iraf.imarith(file_list_oe[num2+2],'-',file_list_oe[num2+3],p)
  open_p= pyfits.open(p)				
  image_p=open_p[0].data
#rm('122_oe_minus_123_oe.fits')
  iraf.imdel(p)					#this .fits file should not be saved
#q=x21,122 - x21,123 {const}
  q=x21[num2+2] - x21[num2+3]			
#r=x22,122 - x22,123v{const}
  r=x22[num2+2] - x22[num2+3]
#s=x23,122 - x23,123 {const}
  s=x23[num2+2] - x23[num2+3]
#3. Compute for Q
#Q~{[(a/d)-(p/s)]-[(b/d)-(q/s)]*I}/[(c/d)-(r/s)]
  Q=((image_a/d-image_p/s)-(b/d-q/s)*image_list_I[num2/4])/(c/d-r/s)
#savefile
  q_name=str(name)+'-'+str(name+3)+'_Q.fits'		#120-123_Q.fits
  pyfits.writeto(q_name,Q)
#4. Computer for U
#U~(a-bI-cQ)/d
  U=(image_a-b*image_list_I[num2/4]-c*Q)/d		#image_list_I[num2/4] = {0,1,2,3,4,...,23}; check if right by using for num2 in set_I: print name,num2/4
#savefile
  u_name=str(name)+'-'+str(name+3)+'_U.fits'		#120-123_U.fits
  pyfits.writeto(u_name,U)

#>>>>6.2 correct instrumental effects
#This was done during computation of Q, U, and PI

***********************************************************************************
#>>>>6.3 rotate images
### I images
"""
FILENAME: 9aI_rotate.py (see 9bI,9cI,9aQU,9bQU,9cQU)
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/I_corrected
This rotates *_I.fits by an angle fr. The files are saved as *_rotI.fits.
# first set: 120-171 inclusive => 171-120= 51+1 = 52/4 = 13 image sets
<ND1> 120, 124 128
<ND10> 132, 136, 140, 144, 148, 152, 156, 160, 164, 168
To run this, I put orig sci images (HICA*120-171) together with 120,124,128,...168_I images.
There are total of 13 output images.

The same is done using the *_Q and *_U.fits data.
Just change the input and output filenames.
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
  name=set_name[i]+120
  if fr > 360: fr-=360
  elif fr < -360: fr+=360 
  print fr, name
#print '\n', name

  I_in=str(name)+'-'+str(name+3)+'_I.fits'
  I_out=str(name)+'-'+str(name+3)+'_rotI.fits'

  iraf.rotate(I_in, I_out, fr, xin=320., xout=320., yin=320., yout=320.)

***********************************************************************************
'''
#FILENAME: align_rotI.py
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/I_corrected/rotated_I
By using imexam in pyraf (press r and then a to show center (row,col) of central bright 
source being measured), I found out that images' center shift by some pixels and hence makes stacking unreliable.
To compensate for this, this file aligns the rotI.fits images by value (x_new,y_new) relative to the first image (120-123) (x[0],y[0]). The measured (Xi,Yi) values are scanned in the center.txt file. The shifted files are named as rotIa.fits found in the aligned_I folder.
'''
from pylab import *
from pyraf import iraf
import glob
import math

a=loadtxt('center.txt',dtype=str) #load Xi,Yi values are str temporarily
x=a[:,1] #x array contains Xi and so does x for Yi
y=a[:,2]

x_new=range(len(x))
y_new=range(len(y))
for i in range(len(x)):
  x_new[i]=271-float(x[i]) #get the difference in x=271 (relative to the X[0] which is x of 120-123 (reference))
  y_new[i]=318-float(y[i]) #do the same for y=318
  print x_new[i], y_new[i]

file_list=glob.glob('*_rotI.fits')
file_list=list(file_list)
file_list.sort()
i=0
for filename_tmp in file_list:
  filename_org=filename_tmp[:-10] #get only the file no.: e.g. 120-123
  filename_align=filename_org+'_rotIa.fits' #rename as 120-123_rotIa.fits
#shifting
  iraf.imshift(filename_tmp,filename_align,x_new[i],y_new[i]) #load e.g. 120-123_rotI.fits and shift it by x_new[0] and y_new[0] pixels and save as above
  print filename_tmp, filename_align #double-check
  print x_new[i], y_new[i]
  print '\n'
  i=i+1
  raw_input() #do this one at a time

***********************************************************************************
##### rotated QU images
#FILENAME: 8align_rotQUa.py
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/I_corrected/rotated_QU
'''
After aligning the rotI.fits images, this file realigns rotQ and rotU too by measured values (x_new,y_new). The x values are scanned in the center_rotQU.txt file. The shifted files are named as *_rotQa  and *_rotUa.fits found in the rotated_QU folder.
'''
from pylab import *
from pyraf import iraf
import glob
import math

a=loadtxt('center_rotQU.txt',dtype=str) #load Xi,Yi values are str temporarily
x_Q=a[:,1] #x array contains Xi and so does x for Yi
y_Q=a[:,2]
x_U=a[:,1] #x array contains Xi and so does x for Yi
y_U=a[:,2]

x_new_Q=range(len(x_Q))
y_new_Q=range(len(y_Q))
x_new_U=range(len(x_U))
y_new_U=range(len(y_U))

for i in range(len(x_Q)):
  x_new_Q[i]=271-float(x_Q[i]) #get the difference in x=271 (relative to the X[0] which is x of 120-123 (reference))
  y_new_Q[i]=318-float(y_Q[i]) #do the same for y=318
#  print x_new[i], y_new[i]
  x_new_U[i]=271-float(x_U[i]) #get the difference in x=271 (relative to the X[0] which is x of 120-123 (reference))
  y_new_U[i]=318-float(y_U[i]) #do the same for y=318

file_list_Q=glob.glob('*_rotQ.fits')
file_list_Q=list(file_list_Q)
file_list_Q.sort()

file_list_U=glob.glob('*_rotU.fits')
file_list_U=list(file_list_U)
file_list_U.sort()
i=0
for filename_tmp_Q in file_list_Q:
  filename_org_Q=filename_tmp_Q[:-10] #get only the file no.: e.g. 120-123
  filename_align_Q=filename_org_Q+'_rotQa.fits' #rename as 120-123_rotIa.fits
#shifting
  iraf.imshift(filename_tmp_Q,filename_align_Q,x_new_Q[i],y_new_Q[i]) #load e.g. 120-123_rotI.fits and shift it by x_new[0] and y_new[0] pixels and save as above
  print filename_tmp_Q, filename_align_Q #double-check
  print x_new_Q[i], y_new_Q[i]
  print '\n'
  i=i+1
  raw_input() #do this one at a time
j=0
for filename_tmp_U in file_list_U:
  filename_org_U=filename_tmp_U[:-10] #get only the file no.: e.g. 120-123
  filename_align_U=filename_org_U+'_rotUa.fits' #rename as 120-123_rotIa.fits
#shifting
  iraf.imshift(filename_tmp_U,filename_align_U,x_new_U[j],y_new_U[j]) #load e.g. 120-123_rotI.fits and shift it by x_new[0] and y_new[0] pixels and save as above
  print filename_tmp_U, filename_align_U #double-check
  print x_new_U[j], y_new_U[j]
  print '\n'
  j=j+1
  raw_input() #do this one at a time

***********************************************************************************
#>>>>Take the median to increase S/N
#FILENAME: 9median_QUa_set.py
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/I_corrected/rotated_QU/aligned_QU
'''
This file stacks the images in each set (science/ND10, ND1 and ref) to increase SNR. 
It requires the rotated images and simply calculates and then applies the median pixel-
wise to make a "stacked image." There are 2 outputs for each set: obj_medQa, obj_medUa, 
ref_medQa, ref_medUa, ND1_medQa, ND1_medUa. 
'''
from pylab import*
import pyfits
#the last 2 are 215-218 & 219-222 actually
file_no_list_obj=['132-135','136-139','140-143','144-147','148-151','152-155','156-159','160-163',
'164-167','168-171','172-175','176-179'] 
# the last image comes from another ap pol set
file_no_list_ND1=['120-123','124-127','128-131','180-183'] 
file_no_list_ref=['184-187','188-191','192-195','196-199','200-203','204-207','208-211','212-215']

##science Q
Q_obj_array=[]
Q_ND1_array=[]
Q_ref_array=[]

for file_no_Q in file_no_list_obj:
  a1=pyfits.open(file_no_Q+'_rotQa.fits')
  Q_obj_array.append(a1[0].data)
  a1.close()
Q_obj_array=array(Q_obj_array)
Q_obj=median(Q_obj_array,axis=0)
#save 
pyfits.writeto('obj_medQa.fits',Q_obj)  
##ND1
for file_no_ND1 in file_no_list_ND1:
  a2=pyfits.open(file_no_ND1+'_rotQa.fits')
  Q_ND1_array.append(a2[0].data)
  a2.close()
Q_ND1_array=array(Q_ND1_array)
Q_ND1=median(Q_ND1_array,axis=0)
#save 
pyfits.writeto('ND1_medQa.fits',Q_ND1)
##ref
for file_no_ref in file_no_list_ref:
  a3=pyfits.open(file_no_ref+'_rotQa.fits')
  Q_ref_array.append(a3[0].data)
  a3.close()
Q_ref_array=array(Q_ref_array)
Q_ref=median(Q_ref_array,axis=0)
#save 
pyfits.writeto('ref_medQa.fits',Q_ref)

figure(1)
clf()
subplot(131)
imshow(Q_obj[250:350,200:300],vmin=-200,vmax=200,interpolation='nearest',cmap=cm.gray)
title('Q_obj')
xlabel("Dec")
ylabel("R.A.")
subplot(132)
imshow(Q_ND1[250:350,200:300],vmin=-200,vmax=200,interpolation='nearest',cmap=cm.gray)
title('Q_ND1')
subplot(133)
imshow(Q_ref[250:350,200:300],vmin=-200,vmax=200,interpolation='nearest',cmap=cm.gray)
title('Q_ref')
### Science U
U_obj_array=[]
U_ND1_array=[]
U_ref_array=[]

for file_no_U in file_no_list_obj:
  b1=pyfits.open(file_no_U+'_rotUa.fits')
  U_obj_array.append(b1[0].data)
  b1.close()
U_obj_array=array(U_obj_array)
U_obj=median(U_obj_array,axis=0)
#save 
pyfits.writeto('obj_medUa.fits',U_obj)  

##ND1
for file_no_ND1 in file_no_list_ND1:
  b2=pyfits.open(file_no_ND1+'_rotUa.fits')
  U_ND1_array.append(b2[0].data)
  b2.close()
U_ND1_array=array(U_ND1_array)
U_ND1=median(U_ND1_array,axis=0)
#save 
pyfits.writeto('ND1_medUa.fits',U_ND1)

##ref
for file_no_ref in file_no_list_ref:
  b3=pyfits.open(file_no_ref+'_rotUa.fits')
  U_ref_array.append(b3[0].data)
  b3.close()
U_ref_array=array(U_ref_array)
U_ref=median(U_ref_array,axis=0)
#save 
pyfits.writeto('ref_medUa.fits',U_ref)

figure(2)
clf()
subplot(131)
imshow(U_obj[250:350,200:300],vmin=-200,vmax=200,interpolation='nearest',cmap=cm.gray)
title('U_obj')
xlabel("Dec")
ylabel("R.A.")

subplot(132)
imshow(U_ND1[250:350,200:300],vmin=-200,vmax=200,interpolation='nearest',cmap=cm.gray)
title('U_ND1')

subplot(133)
imshow(U_ref[250:350,200:300],vmin=-200,vmax=200,interpolation='nearest',cmap=cm.gray)
title('U_ref')
show()

***********************************************************************************
###Polarized Intensity (PI) images
#FILENAME: 10PI_set.py
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/I_corrected/rotated_QU/aligned_QU
'''
last edit: aug16
This file makes the polarized intensity image (PI) of SU Aur
and its convolved counter part of a given sigma.
It does this by first importing medQa and medUa (aligned 2nd time) and then 
computing PI=sqrt(obj_medQ**2+obj_medU**2).
Different sigma and v scales are used to increase the contrast and reveal 
the tail in the final image. There are two output images (PI and PI_conv) per set (obj_?, ref_?, ND1_?).
The optimum sigma=2, vmin=-7.4, vmax=-5 for log was determined.
The output obj_PI_a_fs_conv_sig02.fits will be used for drawing polvec in 
12PI_fs_conv_polvec.py. Copy the outputs in the flux_scaling folder.
'''
from pylab import*
import pyfits
from scipy.ndimage.filters import gaussian_filter

a1=pyfits.open('obj_medQa.fits')
Q_obj=a1[0].data
a1.close()

a2=pyfits.open('obj_medUa.fits')
U_obj=a2[0].data
a2.close()

obj_PI=sqrt(U_obj**2+Q_obj**2)

#flux scaling
ND1_flux=1711181 #measured flux using iraf's phot (in the ND1_medI_a.fits.mag.1)
stellar_flux=ND1_flux*20 

obj_PI_fs=obj_PI/stellar_flux

#convolution smoothens the image
obj_PI_fs_conv=gaussian_filter(obj_PI_fs,sigma=2)

#rough estimate of object's center; but after rotation and alignment, it is defined as such
xcenter_obj=271
ycenter_obj=318

#convert pix to arcsec to AU; distance of object is 140 pc
scale=9.53e-3*140 #HiCIAO pixel scale (arcsec/pix)

#place plot origin to center of object
a=0-xcenter_obj
b=640-xcenter_obj
c=0-ycenter_obj
d=640-ycenter_obj
#convert pix to arcsec
extent_PI=array([a,b,c,d])*scale

#vmin=-10 #use this if objPI is not log10
#vmax=80
#vmin=0.4 #use this for obj_PI_fs
#vmax=2
#vmin=-7 #use this for obj_PI_fs_conv
#vmax=-5

xzoommin=-200
xzoommax=200
yzoommin=-200
yzoommax=200

figure(1)
clf()
subplot(221)
#interpolation prevents default smoothing
imshow(Q_obj,interpolation='nearest',origin='lower',cmap=cm.gray,vmin=-200,vmax=200,extent=extent_PI)
title('obj_Qa')
colorbar()
axis([xzoommin,xzoommax,yzoommin,yzoommax])

subplot(222)
imshow(U_obj,interpolation='nearest',origin='lower',cmap=cm.gray,vmin=-200,vmax=200,extent=extent_PI)
title('obj_Ua')
colorbar()
axis([xzoommin,xzoommax,yzoommin,yzoommax])

subplot(223)
imshow(log10(obj_PI_fs),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=-7.4,vmax=-5,extent=extent_PI)
colorbar()
title('obj_PI_fs_log')
xlabel("AU")
ylabel("AU")
axis([xzoommin,xzoommax,yzoommin,yzoommax])

subplot(224)
#log scale
imshow(log10(obj_PI_fs_conv),interpolation='nearest',origin='lower',vmin=-7.4,vmax=-5,cmap=cm.jet,extent=extent_PI)
colorbar()
title('obj_PI_fs_conv_log')
xlabel("AU")
ylabel("AU")
axis([xzoommin,xzoommax,yzoommin,yzoommax])
#figure(2)
#clf()
#imshow(obj_medI_a,interpolation='nearest',origin='lower',cmap=cm.gray,vmin=0,vmax=80,extent=extent_PI)
show()
#save
#pyfits.writeto('obj_PI_a_fs.fits',obj_PI_fs)
#pyfits.writeto('obj_PI_a_fs_conv_sig02.fits',obj_PI_fs_conv)

***********************************************************************************
###>>>>>>>Flux scaling
#FILENAME:11PI_flux_scaling.py
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/I_corrected/rotated_QU/aligned_QU
#!/usr/bin/env python
'''
This file do flux scaling (i.e. PI_flux/stellar_flux) of the object.
This is done by first measuring the flux of ND1 using iraf's photometry utility (phot).
The output is objPI_conva_fs and obj_PI_a_fs.fits.
Always view output in log10 so (vmin,vmax) range is compressed.
The obj_PI_a_fs are used to make obj_PI_conv_fs_sig?.fits.
optimum vmin,vmax is acquired from test_PI_fs.py
Optimizing sigma is done next in test_PI_opt_sigma.py

You can save obj_PI_a_fs.fits here or do it in 10PI_set.py
The output of 10PI_set.py which is obj_PI_fs_conv_sig02 will
be used as input in 12PI_fs_conv_polvec.
'''
from pylab import *
import pyfits

ND1_flux=1711181 #measured flux using iraf's phot (in the ND1_medI_a.fits.mag.1)
#measured from iraf's phot and computed based on filter transmission (10%) and 
#time exposure relative to object (30s- twice of ND1)
stellar_flux=ND1_flux*20 

z1=pyfits.open('obj_PI_conva_sig005.fits')
obj_PI_conv_sig05=z1[0].data
objPIconv_fs_sig05=obj_PI_conv_sig05/stellar_flux
z1.close()

#obj_PI_a
z2=pyfits.open('obj_PI_a.fits')
obj_PI_a=z2[0].data			#uncalibrated
objPIa_fs=obj_PI_a/stellar_flux		#calibrated
z2.close()
'''
z3=pyfits.open('obj_PI_conv_sig2.fits')
obj_PI_conv_sig2=z3[0].data
objPIconv_fs_sig2=obj_PI_conv_sig2/stellar_flux
z3.close()
'''
xcenter_obj=271
ycenter_obj=318
scale=9.53e-3*140

pix_scale=0.00948 #HiCIAO pixel scale (arcsec/pix)
#place plot origin to center of object
a=0-xcenter_obj
b=640-xcenter_obj
c=0-ycenter_obj
d=640-ycenter_obj
#convert pix to arcsec convert arcsec to AU; distance of object is 140 pc
extent_PI=array([a,b,c,d])*scale

xzoommin=-200
xzoommax=200
yzoommin=-200
yzoommax=200

figure(1)
clf()
imshow(log10(obj_PI_a),interpolation='nearest',origin='lower',vmin=0.5,vmax=2.5,extent=extent_PI)
title('obj_PI_a (uncalibrated flux)')
xlabel('AU')
ylabel('AU')
colorbar()
axis([xzoommin,xzoommax,yzoommin,yzoommax])

figure(2)
clf()
imshow(log10(objPIa_fs),interpolation='nearest',origin='lower',vmin=-7,vmax=-5,extent=extent_PI)
title('obj_PI_fs (calibrated flux)')
xlabel('AU')
ylabel('AU')
colorbar()
axis([xzoommin,xzoommax,yzoommin,yzoommax])
show()
'''
figure(3)
clf()
imshow(log10(objPIa_fs),interpolation='nearest',origin='lower',extent=extent_PI)
colorbar()
'''
#save
#pyfits.writeto('obj_PI_a.fits',obj_PI_a)
#pyfits.writeto('obj_PI_a_fs.fits',objPIa_fs)

***********************************************************************************
#>>>POLARIZATION VECTORS
#FILENAME:12PI_fs_conv_polvec
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU/flux_scaling
'''
last edited: aug16
This file maps polarization vectors given the
convolved PI image (e.g. sigma=0.8).
The file came from output of 10PI_set.
This files works for those are flux calibrated images ONLY.
obj_PI_conva_sigma05.fits
The input PI conva image can be changed with different sigma.
Change parameters such as threshold of polarization.

optimized parameters determined from test_PI_opt_v_fs.py
obj_PI_a_fs: vmin=0.4, vmax=2, sigma=0.8
obj_PI_a_fs_conv: vmin=-7.4, vmax=-5
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
      self.pl,=ax.plot([self.x-dx,self.x+dx],[self.y-dy,self.y+dy], linestyle='-',color=color,linewidth=2)
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
#I checked that objPIa does does not appear different from objPIa_fs
#except that objPIa_fs' flux is significantly smaller now; they have
#different v scales also
a=pyfits.open('obj_PI_a.fits') 	
obj_PI_a=a[0].data
a.close()

#fscaled PI
b=pyfits.open('obj_PI_a_fs.fits')
obj_PI_fs=b[0].data
b.close()

#fscaled convolved PI
c=pyfits.open('obj_PI_a_fs_conv_sig02.fits') 
obj_PI_fs_conv=c[0].data
c.close()

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

#place plot origin to center of object
a=0-xcenter_obj
b=640-xcenter_obj
c=0-ycenter_obj
d=640-ycenter_obj

scale=9.53e-3*140
#convert pix to arcsec to AU
extent_PI=array([a,b,c,d])*scale
'''
figure(0)
imshow(log10(obj_PI_a),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=0.4,vmax=2,extent=extent_PI)
colorbar()
title('obj_PI_fs')
xlabel('AU')
ylabel('AU')
'''
figure(1)
imshow(log10(obj_PI_fs),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=-7.4,vmax=-5,extent=extent_PI)
colorbar()
title('obj_PI_fs_conv')
xlabel('AU')
ylabel('AU')

figure(2)
clf()
ax=subplot(111)
imshow(log10(obj_PI_fs_conv),interpolation='nearest',origin='lower',cmap=cm.jet,vmin=-7.4,vmax=-5,extent=extent_PI)
colorbar()
title('obj_PI_fs_conv_sig02')
xlabel('AU')
ylabel('AU')

varray=[]
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
#savefig('obj_PI_conva_sigma05_pol.fits',v???)
draw()
show()

***********************************************************************************
###>>>radial PI
#FILENAME:15radial_PI_dist.py
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU/flux_scaling/PA_diskmajoraxis
'''
This file generates the radial PI distribution along PA=15 and 195 (major axis)
The radial PI distribution is generated by plotting the normalized flux as
a function of radius (from boundary of mask to r~80 AU).
The goal is to acquire the power index of the radial distribution.
This is done by fitting a power function (resembling a straight line)
in a log log plot. 
There is some problem regarding what conv sigma of image to use because 
it yields different power indices. For consistency, use sigma=2.
Export new_rscale and image_ave.txt and use them for plotting and
getting the power index in excel.
'''
from pylab import *
import pyfits
from scipy.ndimage.interpolation import rotate
import numpy as np
from matplotlib.patches import Ellipse
cmap=cm.jet
cmap.set_bad('black',1)

#z=pyfits.open('obj_PI_fs_conv_sigma008.fits')
#z=pyfits.open('obj_PI_fs_conv_sig01.fits')
z=pyfits.open('obj_PI_a_fs_conv_sig02.fits')
obj_PI_fs_conv=z[0].data-1.1e-7
z.close()

#define image center
scale=9.53e-3*140
xcenter=271
ycenter=318

#crop image; 401x401
#obj_PI_fs_conv_cropped=obj_PI_fs_conv[ycenter-200:ycenter+201,xcenter-200:xcenter+201]
obj_PI_fs_conv_cropped=obj_PI_fs_conv[ycenter-270:ycenter+271,xcenter-270:xcenter+271]

figure(0)
clf()
extent=array([-200,200,-200,200])*scale 
imshow(log10(obj_PI_fs_conv_cropped),interpolation='nearest',origin='lower',cmap=cm.jet,extent=extent,vmin=-7.4,vmax=-5)
plot([0,0], [0, 200*scale], color='w', linestyle='--', linewidth=1)
xlabel('AU')
ylabel('AU')
title('original image (PA=0)')

##scale the axes in AU; make array with 400 elements and subtract 200: [-200,-199,..199,200]*AU conversion factor
rscale=(arange(401)-200)*scale

#angle of image rotation along the major axis
angle=15
rotated_image=rotate(obj_PI_fs_conv_cropped,angle)
dim=rotated_image.shape[0]
midpoint   =dim/2

extent_PI=array([-midpoint,midpoint,-midpoint,midpoint])*scale
figure(1)
clf()
imshow(log10(rotated_image),extent=extent_PI,vmin=-7.4,vmax=-5,cmap=cmap)
plot([0,0], [0, midpoint*scale], color='w', linestyle='--', linewidth=1)
xlabel('AU')
ylabel('AU')
axis([-150,150,-150,150])
colorbar()
title('P.A.= %d deg.' % angle)

figure(2)
clf()
#get the average of of flux along the vertical (PA=15) +-2 pixels (5 columns) to increase SNR
image1=rotated_image[midpoint:,midpoint+1]*scale
image2=rotated_image[midpoint:,midpoint-1]*scale
image3=rotated_image[midpoint:,midpoint+2]*scale
image4=rotated_image[midpoint:,midpoint-2]*scale
image5=rotated_image[midpoint:,midpoint]*scale
image_ave=(image1+image2+image3+image4+image5)/5

#new_rscale=log((arange(rotated_image.shape[0])-midpoint)*scale)
new_rscale=(arange(rotated_image.shape[0])-midpoint)*scale
#get only the positive values of flux; midpoint>=0
new_rscale=new_rscale[midpoint:]

p1, p2 = -1, -2.8
constant= 0.0498
#fit a power law with exponent p=-1
power_law_m1= 1e-4 * new_rscale ** p1
power_law_m2= constant * new_rscale ** p2
loglog(new_rscale,image_ave,'k-')

#log log plot of power law 
label1, label2 = 'p= %.1f' %p1, str(constant)+'r ** %.1f' % p2
#loglog(new_rscale,power_law_m1,'g--',label=label1)
loglog(new_rscale,power_law_m2,'b--',label=label2)
#plot([0,0], [5e-8, 3e-5], color='r', linestyle='--', linewidth=1) #this is a vertical line along the origin

#input the last pixel = boundary of disk
end_pix_disk= 60
label3= 'mask boundary (r=20 AU); disk boundary r=%.1f AU' % ((end_pix_disk+1)*scale)

#mark the point marking the boundary of the mask at r=15, before of which the 
#flux is unreliable, and also the last pixel used in fitting (flux>0)
loglog(15*scale,image_ave[15], 'ro',label=label3)
loglog(end_pix_disk*scale,image_ave[end_pix_disk], 'ro') #for PA=15
axis([0,1000,5e-8,3e-5]) #AU scale
ylabel('log (n_PI / n*)')
xlabel('log(r) (AU)')
title('Power law index: %.1f for PA=%d' % (p2,angle))
legend(loc='upper right', shadow=True)

#Takami+13 used 0."3 arcsec in diameter mask
#0."3 arcsec/*0.00948arcsec/pix = 31.65 pixels
hmask,wmask= 30*scale,30*scale #radius = 15 pix = 20 AU
m=Ellipse(xy=(0,0),height=hmask,width=wmask)
figure(0).add_subplot(111).add_artist(m)
n=Ellipse(xy=(0,0),height=hmask,width=wmask)
figure(1).add_subplot(111).add_artist(n)
m.set_color('k')
n.set_color('k')
show()

***********************************************************************************
###Radial PI compared with other flux profiles
#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU/flux_scaling/PA_diskmajoraxis
'''
This file measures the 1D flux (vertical profile at the image center) at a given 
position angle (0-180) and plots the flux on a log scale compared with the all the other fluxes.
The image is rotated at various position angles (PA's) to see at 
which PA has the widest flux broadening profile which corresponds to the major axis
of the disk.
'''
from pylab import *
import pyfits
from scipy.ndimage.interpolation import rotate
import numpy as np
#z=pyfits.open('obj_PI_fs_conv_sig1.fits') 
z=pyfits.open('obj_PI_fs_conv_sigma08.fits')
obj_PI_fs_conv=z[0].data-1.1e-7
z.close()
#define image center
xcenter=271
ycenter=318

#crop image; 401x401
obj_PI_fs_conv_cropped=obj_PI_fs_conv[ycenter-200:ycenter+201,xcenter-200:xcenter+201]

figure(0)
clf()
extent=array([-200,200,-200,200])
imshow(log10(obj_PI_fs_conv_cropped),interpolation='nearest',origin='lower',cmap=cm.jet,extent=extent,vmin=-7.4,vmax=-5)
plot([0,0], [-200, 200], color='r', linestyle='--', linewidth=1)
title('PA=0')

##scale the axes in AU; make array with 400 elements and subtract 200: [-200,-199,..199,200]*AU conversion factor
rscale=arange(401)-200*9.53e-3*140
'''
figure(1)
clf()
semilogy(rscale,obj_PI_fs_conv_cropped[200,:],label='horizontal')
semilogy(rscale,obj_PI_fs_conv_cropped[:,200],label='vertical')
title('PA=0')
ylabel('Flux (normalized)')
xlabel('pixel position')
legend(loc='upper right', shadow=True)
'''
profile ={}
midpoint={}
image   ={}
profile[0]  =obj_PI_fs_conv_cropped[:,200]
midpoint[0] =200
image[0]    =obj_PI_fs_conv_cropped

angles=arange(0,181,10)
for i in angles:
  rotated_image=rotate(obj_PI_fs_conv_cropped,i)
  dim=rotated_image.shape[0]
  midpoint[i]   =dim/2
  profile[i]    =rotated_image[:,midpoint[i]]
  image[i]      =rotated_image

ion()
for i in range(0,181,10):
  extent_PI=array([-midpoint[i],midpoint[i],-midpoint[i],midpoint[i]])
  figure(0)
  clf()
  imshow(log10(image[i]),extent=extent_PI,vmin=-7.4,vmax=-5)
  plot([0,0], [-midpoint[i], midpoint[i]], color='r', linestyle='--', linewidth=1)
  axis([-150,150,-150,150])
  title('P.A.= %d deg.' % i)
  figure(1)
  clf()
  for ii in range(0,181,10):
    new_rscale=(arange(profile[ii].shape[0])-midpoint[ii])*9.53e-3*140
    semilogy(new_rscale,profile[ii],'c-')
  new_rscale=(arange(profile[i].shape[0])-midpoint[i])*9.53e-3*140
  semilogy(new_rscale,profile[i],'k-')
  axis([-100,100,5e-8,3e-5])
  title('P.A.= %d deg.' % i)
  show()
  raw_input()

***********************************************************************************
#>>>>dispay results
#FILENAME: 16final_ellipse_center_contour_scale_PA0.py
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU/flux_scaling/PA_diskmajoraxis/final_figs
'''
This file generates the final PI image.
The features that can be superposed with the image include:
1) polarization vectors
	-polarization fraction calibrator
2) Ellipse (disk) fitting
	-AU scale calibrator
3) geometric center of disk
4) contour plot
If viewing with polarization vector map only,
comment out the AU scale calibrator and leave pol. fraction calibrator as is.
You can also remove the contour plot and disk 'x' center and ellipse fitting.
If viewing with geometrical features, comment out polarization vector
mapping and leave all else as is. Comment out AU scale calibration.
'''
from pylab import*
import pyfits
from scipy.ndimage.filters import gaussian_filter
from matplotlib.patches import Ellipse
cmap=cm.jet
cmap.set_bad('black',1)
#Polarization fraction is greater farther from the star. Near the star, polarization vectors represent only the lower limit as polarized light reflected from the disk becomes more contaminated with unpolarized starlight
max_length=300       # Pol=100 %
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
      self.pl,=ax.plot([self.x,self.x],[self.y,self.y],linestyle='-',color=color,linewidth=2)
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
a=pyfits.open('obj_PI_a_fs_conv_sig02.fits')
obj_PI_a_fs_conv=a[0].data-1.1e-7
a.close()

#flux scaled convolved PI
c=pyfits.open('obj_PI_fs_conv_sig01.fits') 
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
#define stellar position (image center)
xcenter=271
ycenter=318
scale=9.53e-3*140
#extent=array([-200,200,-200,200])*scale 

#place plot origin to center of object
a=0-xcenter
b=640-xcenter
c=0-ycenter
d=640-ycenter

#convert pix to arcsec
extent_PI=array([a,b,c,d])*scale

figure(1)
clf()
ax=subplot(111)
imshow(log10(obj_PI_a_fs_conv),interpolation='nearest',origin='lower',cmap=cmap,vmin=-7.4,vmax=-5,extent=extent_PI)
colorbar()

#AU calibrator, length = 50 AU
plot([-100,-50],[-100,-100], color='w', linestyle='-', linewidth=3)
#cross-hair inside mask
plot([-15*scale,15*scale],[0,0], color='w', linestyle='-', linewidth=1)
plot([0,0],[-15*scale,15*scale], color='w', linestyle='-', linewidth=1)
#locate geometric center of disk in AU
plot(3, -3, 'ro', lw=6)

#polarization fraction calibrator: 60AU/300AU (max length) = 20%
#plot([-100,-40],[-100,-100], color='w', linestyle='-', linewidth=3)
contour(log10(obj_PI_a_fs_conv),extent=extent_PI,colors='k',levels=[-6.75,-6.5,-6.25,-6.0],linestyles='solid')
title('Normalized PI:  log(PI / I*)')
xlabel('Offset (AU)')
ylabel('Offset (AU)')
axis([-150,400,-150,150])

##superpose an ellipse centered at xy; geometric center offset = 2sqrt(2)AU
h,w=130*scale,100*scale
e=Ellipse(xy=(3,-3),height=h,width=w,linewidth=2,angle=15)
figure(1).add_subplot(111).add_artist(e)
e.set_ec('r')
e.set_fc('none')
e.set_ls('dashed')

varray=[]
#dx=dy=4
dx=dy=9
area=(2*dx+1)*(2*dy+1)

inc=20
xmin=xcenter-100	#extent of the region where pol vectors will be drawn
xmax=xcenter+310
ymin=ycenter-100
ymax=ycenter+110

x_in_AU=(arange(640)-xcenter)*scale
y_in_AU=(arange(640)-ycenter)*scale
'''
for x in range(xmin,xmax,inc):
  for y in range(ymin,ymax,inc):
    r_in_AU=sqrt(x_in_AU[x]**2+y_in_AU[y]**2)
    if r_in_AU < 15: continue			#put pol vectors outside r=15
    if log10(obj_PI_a_fs_conv[y,x]) > -7.4: 	#threshold of polarization (smaller- wider)
      I=sum(obj_medI_a[y-dy:y+dy+1,x-dx:x+dx+1])/area
      Q=sum(obj_medQa[y-dy:y+dy+1,x-dx:x+dx+1])/area
      U=sum(obj_medUa[y-dy:y+dy+1,x-dx:x+dx+1])/area
      v=Linear_pol_vector(x_in_AU[x],y_in_AU[y],I,-Q,-U,ax,max_length=max_length,color='w')
draw()
'''
#Takami+13 used 0."3 arcsec in diameter mask
#0."3 arcsec/*0.00948arcsec/pix = 31.65 pixels
hmask,wmask= 30*scale,30*scale #radius = 15 pix = 20 AU
m=Ellipse(xy=(0,0),height=hmask,width=wmask)
figure(1).add_subplot(111).add_artist(m)
m.set_color('k')
show()

***********************************************************************************
###>>>>>>>>> 
#FILENAME: 17disk_compare.py
#cd ~/Desktop/disk_images
'''
This file shows the 5 stars+disks observed 
during SEEDS survey. The images will be used
to compare the results of SU Aur.
'''
from pylab import *
import pyfits
cmap=cm.gray
cmap.set_bad('black',1)
from matplotlib.patches import Ellipse

a=pyfits.open('SAO206462_frac.fits')
sao=a[0].data
a.close()

b=pyfits.open('MWC758_frac.fits')
mwc758=b[0].data
b.close()

c=pyfits.open('UScoJ1604_frac.fits')
J1604=c[0].data
c.close()

d=pyfits.open('PDS70_frac.fits')
pds70=d[0].data
d.close()

e=pyfits.open('MWC480_frac_Kusakabe.fits')
mwc480=e[0].data
e.close()

xcenter=256
ycenter=256
scale1=9.53e-3*140
scale2=9.53e-3*200
scale3=9.53e-3*145
scale4=9.53e-3*140
scale5=9.53e-3*140

#place plot origin to center of object
a=0-xcenter
b=512-xcenter
c=0-ycenter
d=512-ycenter
extent_PI1=array([a,b,c,d])*scale1
extent_PI2=array([a,b,c,d])*scale2
extent_PI3=array([a,b,c,d])*scale3
extent_PI4=array([a,b,c,d])*scale4
extent_PI5=array([a,b,c,d])*scale5

#sao
figure(1)
clf()
imshow(log10(sao),interpolation='nearest',origin='lower',cmap=cmap,vmin=-7, vmax=-6,extent=extent_PI1)
plot([-120,-70],[-120,-120], color='w', linestyle='-', linewidth=3)
colorbar()
xlabel('Offset (AU)')
ylabel('Offset (AU)')
title('SAO 206642: Muto et. al. 2012')
axis([-150,150,-150,150])

#mwc758
figure(2)
clf()
imshow(log10(mwc758),interpolation='nearest',origin='lower',cmap=cmap,vmin=-7, vmax=-6,extent=extent_PI2)
plot([-120,-70],[-120,-120], color='w', linestyle='-', linewidth=3)
colorbar()
xlabel('Offset (AU)')
ylabel('Offset (AU)')
title('MWC 758: Grady et. al. 2013')
#axis([-120*scale2,120*scale2,-120*scale2,120*scale2])
axis([-150,150,-150,150])

#J1604
figure(3)
clf()
imshow(log10(J1604),interpolation='nearest',origin='lower',cmap=cmap,vmin=-7, vmax=-6,extent=extent_PI3)
plot([-100,-50],[-80,-80], color='w', linestyle='-', linewidth=3)
colorbar()
xlabel('Offset (AU)')
ylabel('Offset (AU)')
title('USco J1604: Mayama et. al. 2012')
#axis([-120*scale3,120*scale3,-120*scale3,120*scale3])
axis([-120,120,-120,120])

#pds70
figure(4)
clf()
imshow(log10(pds70),interpolation='nearest',origin='lower',cmap=cmap,vmin=-7, vmax=-6,extent=extent_PI4)
plot([-120,-70],[-120,-120], color='w', linestyle='-', linewidth=3)
colorbar()
xlabel('Offset (AU)')
ylabel('Offset (AU)')
title('PDS 70: Hashimoto et. al. 2012')
#axis([-120*scale4,120*scale4,-120*scale4,120*scale4])
axis([-150,150,-150,150])

#mwc480
figure(5)
clf()
imshow(log10(mwc480),interpolation='nearest',origin='lower',cmap=cmap,vmin=-7, vmax=-6,extent=extent_PI5)
plot([-120,-70],[-120,-120], color='w', linestyle='-', linewidth=3)
colorbar()
xlabel('Offset (AU)')
ylabel('Offset (AU)')
title('MWC 480: Kusakabe et. al. 2012')
#axis([-120*scale5,120*scale5,-120*scale5,120*scale5])
axis([-150,150,-150,150])

#SU AUR: mask radius = 0."15 => r=15 pixels = 21 AU
hmask1,wmask1= 30*scale1,30*scale1 #mask radius = 0."15 => r=15 pixels = 21 AU
hmask2,wmask2= 30*scale2,30*scale2 #mask radius = 0."15 => r=15 pixels = 30 AU
#problem: r=0."2 = 21 pixels is so big! tried r=0"10 and it looks like in paper
hmask3,wmask3= 21*scale3,21*scale3 #mask radius = 0."2 => r=21 pixels = 29 AU
hmask4,wmask4= 42*scale4,42*scale4 #mask radius = 0."2 => r=21 pixels = 28 AU
hmask5,wmask5= 30*scale5,30*scale5 #mask radius = 0."15 => r=15 pixels = 21 AU

m=Ellipse(xy=(0,0),height=hmask1,width=wmask1)
n=Ellipse(xy=(0,0),height=hmask2,width=wmask2)
o=Ellipse(xy=(0,0),height=hmask3,width=wmask3)
p=Ellipse(xy=(0,0),height=hmask4,width=wmask4)
q=Ellipse(xy=(0,0),height=hmask5,width=wmask5)

figure(1).add_subplot(111).add_artist(m)
figure(2).add_subplot(111).add_artist(n)
figure(3).add_subplot(111).add_artist(o)
figure(4).add_subplot(111).add_artist(p)
figure(5).add_subplot(111).add_artist(q)

m.set_color('k')
n.set_color('k')
o.set_color('k')
p.set_color('k')
q.set_color('k')
show()