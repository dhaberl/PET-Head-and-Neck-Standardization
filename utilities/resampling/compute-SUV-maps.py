"""
This script computes the SUV maps of the raw PET images (activity). Missing data in the dcm-files is replaced by
approximations (e.g., patients weight, injected dose decay).
"""


import os
import numpy as np
import pydicom
import math
import datetime

# Format for datetime
format = '%H%M%S'

# Path to source files: 3D Numpy arrays of PET
path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/3D-PET-npy'

# Path to destination directory
dst_path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/Dev-SUV-PET'

# Path to PET folder containing associated Dicom Files
path_dcm = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/PET-dcm'

store_flags = []

for cohort in sorted(os.listdir(path)):
    print(cohort)

    # Make directory for each cohort
    os.makedirs(os.path.join(dst_path, cohort), exist_ok=True)

    for patient in sorted(os.listdir(os.path.join(path, cohort))):
        print(patient)

        # Make directory for each patient
        os.makedirs(os.path.join(dst_path, cohort, patient), exist_ok=True)

        # Get DICOM Data
        dcm = pydicom.dcmread(os.path.join(path_dcm, cohort + '_PET', patient,
                                           os.listdir(os.path.join(path_dcm, cohort + '_PET', patient))[0]))

        # Get Patient Weight in grams
        weight = dcm.PatientWeight
        sex = dcm.PatientSex

        if weight is None:
            if sex == 'M':
                weight = 80.3 * 1000
            if sex == 'F':
                weight = 75 * 1000
            else:
                weight = 80.3 * 1000
        else:
            weight = weight * 1000

        try:
            # Get Scan Time
            scan_time = dcm.AcquisitionTime
            if scan_time.endswith('.00'):  
                scan_time = scan_time[:-3]
            # print(scan_time)

            # Get Start Time for the Radiopharmaceutical Injection
            injection_time = dcm.RadiopharmaceuticalInformationSequence[0].RadiopharmaceuticalStartTime
            if injection_time.endswith('.00'):  
                injection_time = injection_time[:-3]
            # print(injection_time)

            # Get Half Life for Radionuclide
            half_life = dcm.RadiopharmaceuticalInformationSequence[0].RadionuclideHalfLife
            half_life = 6588  
            # print(half_life)

            # Get Total dose injected for Radionuclide
            injected_dose = dcm.RadiopharmaceuticalInformationSequence[0].RadionuclideTotalDose
            # print(injected_dose)

            # Calculate decay
            scan_time = datetime.datetime.strptime(scan_time, format)
            injection_time = datetime.datetime.strptime(injection_time, format)
            diff = scan_time - injection_time
            diff = diff.seconds
            decay = math.exp(-math.log(2) * diff / half_life)
            # print(decay)

            # Calculate the dose decayed during procedure in [Bq]
            injected_dose_decay = injected_dose * decay
            # print(injected_dose_decay)

        except:
            # Estimation: 90 min waiting time, 15 min preparation, 420 MBq
            decay = math.exp(-math.log(2) * (1.75*3600)/6588)
            injected_dose_decay = 420000000 * decay

            # See which patients are affected
            store_flags.append(patient)

        for files in sorted(os.listdir(os.path.join(path, cohort, patient))):
            pet = np.load(os.path.join(path, cohort, patient, files))

            # Calculate SUV
            SUV_map = pet*weight/injected_dose_decay

            # Save
            np.save(os.path.join(dst_path, cohort, patient, files), SUV_map)
