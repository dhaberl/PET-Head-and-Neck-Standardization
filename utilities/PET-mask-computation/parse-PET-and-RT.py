"""
This script parses the Head & Neck data into a new folder given by dst_path.

source: path/cohort/patients/folder/subfolder/files where files = CT, PET, RT-Structure files, dose files, ...
destination: dst_path/cohort/patients/files where files = PET files and associated RT-Structure file

This script copies the selected files from the source to destination path.
After that, the files are renamed to their SOPInstanceUID.

Note: Renaming is optional and not necessary.
"""


import os
import pydicom
from shutil import copy


path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/Separated_Centers/'
dst_path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/Separated_Centers_PET_RTStruct'


for cohort in sorted(os.listdir(path)):
    print(cohort)

    # Make folder for each cohort
    os.makedirs(os.path.join(dst_path, cohort), exist_ok=True)

    for patients in sorted(os.listdir(os.path.join(path, cohort))):
        print(patients)

        # Make folder for each patient
        os.makedirs(os.path.join(dst_path, cohort, patients), exist_ok=True)

        for folders in sorted(os.listdir(os.path.join(path, cohort, patients))):

            for subfolders in sorted(os.listdir(os.path.join(path, cohort, patients, folders))):

                for i, files in enumerate(sorted(os.listdir(os.path.join(
                        path, cohort, patients, folders, subfolders)))):

                    ds = pydicom.dcmread(os.path.join(path, cohort, patients, folders, subfolders, files))
                    new_name = ds.SOPInstanceUID

                    if ds.Modality == 'PT':
                        length = [item for item in
                                  os.listdir(os.path.join(path, cohort, patients, folders, subfolders))]

                        destination_path = os.path.join(dst_path, cohort, patients)
                        source_path = os.path.join(path, cohort, patients, folders, subfolders, files)

                        # print('Copy {} from {} to  {}'.format(files, source_path, destination_path))
                        copy(source_path, destination_path)

                        print('File {} from {} copied.'.format(i + 1, len(length)))

                        # Rename files in destination path
                        os.rename(os.path.join(destination_path, files),
                                  os.path.join(destination_path, new_name + '.dcm'))

                        # print('File {} renamed to {}'.format(os.path.join(dst_path, cohort, patients, files),
                        #                                      os.path.join(dst_path, cohort,
                        #                                                   patients, new_name + '.dcm')))

                    try:  # attribute does not exists for all files in source path => try / except

                        if ds.SeriesDescription == 'RTstruct_CTsim->PET(PET-CT)':

                            destination_path = os.path.join(dst_path, cohort, patients)
                            source_path = os.path.join(path, cohort, patients, folders, subfolders, files)

                            # print('Copy {} from {} to  {}'.format(files, source_path, destination_path))
                            copy(source_path, destination_path)

                            print('RT-Structure-File copied.')

                            # Rename files in destination path
                            os.rename(os.path.join(destination_path, files),
                                      os.path.join(destination_path, new_name + '.dcm'))
                    except:

                        print('An exception occurred')
