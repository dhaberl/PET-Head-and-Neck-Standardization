"""
This script resizes the images to a given size.
"""


import numpy as np
import os
import cv2


path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/PET_NUMPY/Head-Neck-PET-CT_HMR_PET_NUMPY'
dst_path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/PET_NUMPY_256x256/' \
           'Head-Neck-PET-CT_HMR_PET_NUMPY_256x256'

new_size = (256, 256)

for patients in os.listdir(path):
    os.makedirs(os.path.join(dst_path, patients), exist_ok=True)

    for files in os.listdir(os.path.join(path, patients)):
        arr = np.load(os.path.join(path, patients, files))
        arr = cv2.resize(arr, dsize=new_size, interpolation=cv2.INTER_CUBIC)
        np.save(os.path.join(dst_path, patients, os.path.splitext(files)[0]), arr)
