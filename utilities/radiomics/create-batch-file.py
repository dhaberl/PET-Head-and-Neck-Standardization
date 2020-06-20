"""
This script creates a csv-file with the paths to the images and masks.
"""


import os
import pandas as pd


path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/resampled-3D-suv-pet-and-masks-prim-nrrd'

name_of_cohort = 'Head-Neck-PET-CT_HMR'

table = {'Image': [], 'Mask': []}

for cohort in sorted(os.listdir(path)):
    # print(cohort)

    if cohort == name_of_cohort:
        for patient in sorted(os.listdir(os.path.join(path, cohort))):
            # print(patient)

            for file in sorted(os.listdir(os.path.join(path, cohort, patient))):
                # print(file)

                if file.startswith('pet'):
                    path2pet = os.path.join(path, cohort, patient, file)
                    table['Image'].append(path2pet)
                if file.startswith('mask'):
                    path2mask = os.path.join(path, cohort, patient, file)
                    table['Mask'].append(path2mask)
    else:
        pass

df = pd.DataFrame(table)
df.to_csv(name_of_cohort + '.csv', index=False)
