"""
This script converts image and mask npy-files to nrrd-files.
"""


import os
import nrrd
import numpy as np


path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/resampled-3D-suv-pet-and-masks-prim-npy'

dst_path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/resampled-3D-suv-pet-and-masks-prim-nrrd'

for cohort in sorted(os.listdir(path)):
    # print(cohort)

    # Create directory for each cohort
    os.makedirs(os.path.join(dst_path, cohort), exist_ok=True)

    for patient in sorted(os.listdir(os.path.join(path, cohort))):
        # print(patient)

        # Create directory for each patient
        os.makedirs(os.path.join(dst_path, cohort, patient), exist_ok=True)

        for file in sorted(os.listdir(os.path.join(path, cohort, patient))):

            item = np.load(os.path.join(path, cohort, patient, file))

            # Write to nrrd files
            print('Saving as nrrd file...')
            file_name = file.split('.')
            file_name = file_name[0] + '.nrrd'
            nrrd.write(os.path.join(dst_path, cohort, patient, file_name), item)
