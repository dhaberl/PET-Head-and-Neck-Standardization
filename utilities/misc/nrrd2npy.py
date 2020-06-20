"""
This script converts a single nrrd-file to a npy-file.
"""


import nrrd
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=str, default="", help="Path of directory containing image as nrrd-file")
parser.add_argument("-o", "--output_path", type=str, default="", help="Output path where the npy-file will be saved")
args = parser.parse_args()
path = args.path
output_path = args.output_path

read_data, header = nrrd.read(path)

head, file = os.path.split(path)
file = file.split('.')
file_name = file[0]
np.save('{}.npy'.format(os.path.join(output_path, file_name)), read_data)
