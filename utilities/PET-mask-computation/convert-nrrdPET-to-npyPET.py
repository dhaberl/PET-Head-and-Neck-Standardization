"""
This script converts the PET-nrrd-files to PET-npy-files.
"""


import os
import numpy as np
import nrrd


# Path to nrrd-PET
path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/PET-Plastimatch-NoSpacing'

# Destination path
dst_path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/3D-PET-NPY'

for cohorts in sorted(os.listdir(path)):
    print(cohorts)

    # Make directory in dst_path for saving files
    os.makedirs(os.path.join(dst_path, cohorts), exist_ok=True)

    for patients in sorted(os.listdir(os.path.join(path, cohorts))):
        print(patients)

        # Make directory in dst_path/cohorts for each patient for saving files
        os.makedirs(os.path.join(dst_path, cohorts, patients), exist_ok=True)

        for files in sorted(os.listdir(os.path.join(path, cohorts, patients))):
            # print(files)

            # Read PET nrrd files
            pet, header = nrrd.read(os.path.join(path, cohorts, patients, files))

            # Save PET as npy files
            head, file = os.path.split(os.path.join(dst_path, cohorts, patients, files))
            file = file.split('.')
            file_name = file[0]
            np.save(os.path.join(dst_path, cohorts, patients, file_name), pet)
