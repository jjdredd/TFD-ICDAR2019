#! /usr/bin/env python3

import os
import sys
import numpy
from numpy import genfromtxt
import argparse
import glob


def create_pmath(input_csv, output_dir):
    """ create pmath csv annotations from original
    annotations """

    file_basename = os.path.splitext(os.path.basename(input_csv))[0]
    data = genfromtxt(input_csv, delimiter=',', dtype=int)
    file_dir = os.path.join(output_dir, file_basename)
    os.makedirs(file_dir, exist_ok=True)

    i = 0
    while i < data.shape[0]:
        j = data[i][0]
        fname = "{}.pmath".format(str(j))
        fd_out = open(os.path.join(file_dir, fname), 'a')
        while j == data[i][0]:
            fd_out.write("{}, {}, {}, {}\n"
                         .format(data[i][1], data[i][2],
                                 data[i][3], data[i][4]))
            i += 1
            if i == data.shape[0]:
                fd_out.close()
                break
    return (i > 0)

def create_images(input_pdf, output_dir):
    """ convert pdf pages to individual png with density 600
    should be correct"""

    file_basename = os.path.splitext(os.path.basename(input_pdf))[0]
    file_dir = os.path.join(output_dir, file_basename)
    os.makedirs(file_dir, exist_ok=True)
    filename = os.path.join(file_dir, "%d.png")

    ret = os.system("convert -limit memory 4GB -density 600 {} {}"
              .format(input_pdf, os.path.join(output_dir, filename)))

    if os.WIFEXITED(ret):
        return (os.WEXITSTATUS(ret) == 0)
    else:
        return False



parser = argparse.ArgumentParser(description='Create datasets.')
parser.add_argument('--dataset', dest='dataset_dir',
                    help='directory to create the dataset in')
parser.add_argument('--pdfs', dest='pdf_dir',
                    help='directory of pdf files for the dataset')
parser.add_argument('--annotations', dest='annotations_dir',
                    help='directory with csv annotations')
args = parser.parse_args()

dataset_images = os.path.join(args.dataset_dir, 'images')
dataset_annotations = os.path.join(args.dataset_dir, 'annotations')
os.makedirs(dataset_images, exist_ok=True)
os.makedirs(dataset_annotations, exist_ok=True)

ds_file = open(os.path.join(args.dataset_dir, 'data_file.txt'), 'w')
for annot_file in glob.glob(os.path.join(args.annotations_dir, '*.csv')):
    ca = create_pmath(annot_file, dataset_annotations)
    file_basename = os.path.splitext(os.path.basename(annot_file))[0]
    pdf_file = file_basename + '.pdf'
    ci = create_images(os.path.join(args.pdf_dir, pdf_file), dataset_images)
    if ci and ca:
        ds_file.write('{}\n'.format(file_basename))
        print(file_basename)


ds_file.close()
