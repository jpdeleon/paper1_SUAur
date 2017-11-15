#!usr/bin/env python

from pylab import *
import numpy as np

a=loadtxt('center.txt',dtype=str)
x=a[:,1]
y=a[:,2]

x_new=range(len(x))
y_new=range(len(y))
for i in range(len(x)):
  x_new[i]=float(x[i])-float(x[0])
#print 'column 1', a[:,1]
