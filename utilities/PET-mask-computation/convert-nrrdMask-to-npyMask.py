"""
This script converts Mask-nrrd-files to Mask-npy-files. Only the masks of the label given in the
Excel-file (INFO_GTVcontours_HN_edit.xlsx) are going to be converted and saved.

Here: only the masks of the primary tumors (GTV Primary).
"""


import os
import numpy as np
import nrrd
import pandas as pd


# Path to nrrd masks
path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/Plastimatch_Output'

# Path to Excel list
path_names = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/INFO_GTVcontours_HN_edit.xlsx'

# Destination path
dst_path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/FOLDER'

for cohorts in sorted(os.listdir(path)):
    print(cohorts)
    print('\n')

    # Make directory in dst_path for saving files
    os.makedirs(os.path.join(dst_path, cohorts), exist_ok=True)

    # Read associated sheet name to cohort from Excel-file
    sheet_name = cohorts.split('_')[1]
    table = pd.read_excel(path_names, sheet_name=sheet_name)
    df = table.to_dict('list')
    roi = dict(zip(df['Patient'], df['Name GTV Primary']))

    for patients in sorted(os.listdir(os.path.join(path, cohorts))):
        print(patients)

        # Make directory in dst_path/cohorts for each patient for saving files
        os.makedirs(os.path.join(dst_path, cohorts, patients), exist_ok=True)

        # Find matching indices to labels from df
        label = roi[patients].split(',')

        for labels in label:
            # Read nrrd file
            mask, header = nrrd.read(os.path.join(path, cohorts, patients, labels + '.nrrd'))

            # Save masks as npy files
            np.save(os.path.join(dst_path, cohorts, patients, labels + '.npy'), mask)
