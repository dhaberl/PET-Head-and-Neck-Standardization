"""
This script resamples the PET images to an isotropic voxel size.
"""


import os
import numpy as np
import pydicom
import scipy.ndimage
from shutil import copy

# Path to source files: 3D Numpy arrays of PET and masks
path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/3D-suv-pet-and-masks-prim-npy'

# Path to destination directory
dst_path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/resampled-3D-suv-pet-and-masks-prim-npy'

# Path to PET folder containing Dicom Files
path_dcm = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/PET-dcm'

# New Spacing
new_spacing = np.array([4, 4, 4], dtype=np.float32)


for cohort in sorted(os.listdir(path)):

    # Make directory for each cohort in destination path
    os.makedirs(os.path.join(dst_path, cohort), exist_ok=True)

    for patient in sorted(os.listdir(os.path.join(path, cohort))):
        print('Cohort: {}'.format(cohort))
        print('Patient: {}'.format(patient))

        # Make directory for each patient in destination path
        os.makedirs(os.path.join(dst_path, cohort, patient), exist_ok=True)

        # Read a random dcm slice from the same patient as a reference to extract spacing values from dcm
        ref_slice = pydicom.dcmread(os.path.join(path_dcm, cohort + '_PET', patient,
                                                 os.listdir(os.path.join(path_dcm, cohort + '_PET', patient))[0]))

        # Check if the dcm file is the corresponding one to the npy file by comparing the Patient's Name
        if ref_slice.PatientName != patient:
            print('Mismatch between Dicom and NumPy File')
            exit()

        else:

            # Get spacing from reference dcm file:
            # PixelSpacing = [row_spacing, column_spacing] in mm, SliceThickness = Nominal slice thickness, in mm.
            # ONLY valid, if SliceThickness = const. through all slices
            spacing = np.array(list(ref_slice.PixelSpacing) + [ref_slice.SliceThickness], dtype=np.float32)

            print('New Spacing: {}'.format(np.round(new_spacing)))
            print('Old Spacing: {}'.format(spacing))

            # Check if old spacing = new spacing. If True => no interpolation is needed, else: interpolate.
            if np.array_equal(np.round(new_spacing), spacing):
                print('No interpolation needed: New Spacing = Old Spacing')
                print('\n')

                list_of_files = [file for file in os.listdir(os.path.join(path, cohort, patient))]
                for file in list_of_files:
                    source = os.path.join(path, cohort, patient, file)
                    destination = os.path.join(dst_path, cohort, patient, file)
                    copy(source, destination)
            else:

                # Resize factor
                resize_factor = spacing/new_spacing

                for file in sorted(os.listdir(os.path.join(path, cohort, patient))):

                    img = np.load(os.path.join(path, cohort, patient, file))

                    # Calculate new shape: real and rounded
                    new_real_shape = img.shape * resize_factor
                    new_shape = np.round(new_real_shape)
                    real_resize_factor = new_shape / img.shape
                    new_spacing = spacing / real_resize_factor

                    # Interpolation # TODO: What kind of interpolation + order + pet and masks same?
                    print('Interpolating the {}-volume using Cubic Spline-Interpolation'.format(file.split('.')[0]))
                    print('Old shape: {}'.format(img.shape))

                    image = scipy.ndimage.zoom(img, real_resize_factor, mode='nearest', order=3)

                    print('New shape: {}'.format(image.shape))

                    # Save file
                    print('Save {}-file to destination folder...'.format(file.split('.')[0]))
                    np.save(os.path.join(dst_path, cohort, patient, file), image)
                print('\n')
