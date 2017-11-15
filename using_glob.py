#!/usr/bin/env python

from pylab import *
from pyraf import iraf
import glob

file_list=glob.glob('HICA*.fits')
file_list=list(file_list)
file_list.sort()

for filename in file_list:
  print filename
  iraf.display(filename,1)
  raw_input()


