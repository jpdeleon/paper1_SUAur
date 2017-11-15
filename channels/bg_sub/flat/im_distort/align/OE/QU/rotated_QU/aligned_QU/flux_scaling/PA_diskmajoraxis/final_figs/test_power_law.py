#!/usr/bin/env python
#cd ~/Desktop/SU_Aur_backup/channels/bg_sub/flat/im_distort/align/OE/QU/rotated_QU/aligned_QU/flux_scaling/PA_diskmajoraxis
from pylab import *
import pyfits
import numpy as np

figure(0)
clf()
p0, p1, p2, p3, p4, p5 = -1.,-1.5,-2., -2.5, -3., -3.5,
rscale=arange(50,200,1)
#fit a power law with exponent p=-1
m0= rscale ** p0
m1= rscale ** p1
m2= rscale ** p2
m3= rscale ** p3
m4= rscale ** p4
m5= rscale ** p5
label1,label2,label3,label4,label5,label6=p0,p1,p2,p3,p4,p5

loglog(rscale,m0,'k-',lw=2,label=label1)
loglog(rscale,m1,'r-',lw=2,label=label2)
loglog(rscale,m2,'c-',lw=2,label=label3)
loglog(rscale,m3,'y-',lw=2,label=label4)
loglog(rscale,m4,'b-',lw=2,label=label5)
loglog(rscale,m5,'g-',lw=2,label=label6)
legend(loc='lower left', shadow=True)

ylabel('log (n_PI / n*)')
xlabel('log(r) (AU)')
show()
