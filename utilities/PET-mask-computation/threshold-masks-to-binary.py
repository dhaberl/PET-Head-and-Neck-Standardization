"""
This script computes binary masks.
"""


import os
import numpy as np


path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/resampled-3D-suv-pet-and-masks-prim-npy'

for cohort in sorted(os.listdir(path)):
    print(cohort)
    for patient in sorted(os.listdir(os.path.join(path, cohort))):
        print(patient)
        for file in sorted(os.listdir(os.path.join(path, cohort, patient))):
            if file.startswith('mask'):
                mask = np.load(os.path.join(path, cohort, patient, file))
                print(np.where(mask > 1))
                mask[mask >= 1] = 1
                np.save(os.path.join(path, cohort, patient, file), mask)


# Checking
# for cohort in sorted(os.listdir(path)):
#     print(cohort)
#     for patient in sorted(os.listdir(os.path.join(path, cohort))):
#         print(patient)
#         for file in sorted(os.listdir(os.path.join(path, cohort, patient))):
#             if file.startswith('mask'):
#                 mask = np.load(os.path.join(path, cohort, patient, file))
#                 print(patient)
#                 arr = np.where(mask > 1)
#                 if arr[0].size and arr[1].size and arr[2].size != 0:
#                     print('Found')
