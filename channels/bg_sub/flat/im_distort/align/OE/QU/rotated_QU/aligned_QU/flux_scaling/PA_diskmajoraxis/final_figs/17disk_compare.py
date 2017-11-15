#!usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU/flux_scaling/PA_diskmajoraxis/final_figs
from pylab import*
import pyfits
cmap=cm.jet
cmap.set_bad('black',1)

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

#vmin=-7.4,vmax=-5
#sao
figure(1)
clf()
imshow(log10(sao),interpolation='nearest',origin='lower',cmap=cmap)

#mwc758
figure(2)
clf()
imshow(log10(mwc758),interpolation='nearest',origin='lower',cmap=cmap)

#J1604
figure(3)
clf()
imshow(log10(J1604),interpolation='nearest',origin='lower',cmap=cmap)

#pds70
figure(4)
clf()
imshow(log10(pds70),interpolation='nearest',origin='lower',cmap=cmap)

#mwc480
figure(5)
clf()
imshow(log10(mwc480),interpolation='nearest',origin='lower',cmap=cmap)
show()
