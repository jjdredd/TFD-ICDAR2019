#! /usr/bin/env python3

import os
import sys
import numpy
from numpy import genfromtxt

if len(sys.argv) < 3:
    print ("usage:")
    print ("convert_csv.py output_dir/ input_file.csv")

output_dir = sys.argv[1]
input_csv = sys.argv[2]
file_basename = os.path.splitext(os.path.basename(input_csv))[0]

data = genfromtxt(input_csv, delimiter=',', dtype=int)

i = 0
while i < data.shape[0]:
    j = data[i][0]
    fname = file_basename + '-' +  str(j) + '.pmath'
    fd_out = open(os.path.join(output_dir, fname), 'a')
    while j == data[i][0]:
        fd_out.write("{}, {}, {}, {}\n"
                 .format(data[i][1], data[i][2], data[i][3], data[i][4]))
        i += 1
        if i == data.shape[0]:
            fd_out.close()
            break
