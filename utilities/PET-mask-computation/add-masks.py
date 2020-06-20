"""
This script adds several masks to a single one. The mask will then be saved with the associated PET in the destination
folder.

For example: A primary tumor has three masks GTV1, GTV2 and GTV3 => mask = GTV1 + GTV2 + GTV3

"""


import os
import numpy as np
from shutil import copy

path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/Dev-masks-npy'
dst_path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/3D-suv-pet-and-masks-prim-npy'

for cohort in sorted(os.listdir(path)):
    print(cohort)

    # Make directory in destination path for each cohort
    os.makedirs(os.path.join(dst_path, cohort), exist_ok=True)

    for patient in sorted(os.listdir(os.path.join(path, cohort))):
        print(patient)

        # Make directory in destination path for each patient
        os.makedirs(os.path.join(dst_path, cohort, patient), exist_ok=True)

        # Store loaded masks for adding in a list
        # Use  this line if pet and masks are in the same folder
        # masks = [np.load(os.path.join(path, cohort, patient, mask))for mask in os.listdir(os.path.join(path, cohort, patient)) if mask.startswith('mask')]

        # Use this line if masks are separated from the PET
        masks = [np.load(os.path.join(path, cohort, patient, mask))for mask in os.listdir(os.path.join(path, cohort, patient))]

        # If more than one mask add and save with name: 'mask'
        if len(masks) > 1:
            s = masks[0].shape
            temp = np.zeros(s)
            for mask in masks:
                result = np.add(temp, mask)
                temp = result
            np.save(os.path.join(dst_path, cohort, patient, 'mask.npy'), temp)

        # If only one mask in list of masks => save it as it is with name: 'mask'
        else:
            for mask in masks:
                np.save(os.path.join(dst_path, cohort, patient, 'mask.npy'), mask)

        # # Use  this line if pet and masks are in the same folder
        # # Copy pet to destination folder
        # for file in sorted(os.listdir(os.path.join(path, cohort, patient))):
        #     if file.startswith('pet'):
        #         src = os.path.join(path, cohort, patient, file)
        #         dst = os.path.join(dst_path, cohort, patient)
        #         copy(src, dst)

# Use this code if pet and masks are stored in separated folders
# Copy pet from given path to destination folder
path_pet = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/Dev-SUV-PET'

for cohort in sorted(os.listdir(path_pet)):
    for patient in sorted(os.listdir(os.path.join(path_pet, cohort))):
        for file in sorted(os.listdir(os.path.join(path_pet, cohort, patient))):
            src = os.path.join(path_pet, cohort, patient, file)
            dst = os.path.join(dst_path, cohort, patient)
            copy(src, dst)
