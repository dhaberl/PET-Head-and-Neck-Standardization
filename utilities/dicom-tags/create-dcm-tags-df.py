"""
This script creates a Pandas DataFrame of specific Dicom labels of a given cohort.
"""


import os
import pydicom
import pandas as pd
pd.options.display.max_rows = 999
pd.options.display.max_columns = 999


path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/PET/Head-Neck-PET-CT_CHUS_PET'

table = {'Patient': [], 'Manufacturer': [], 'Manufacturer Model Name': [], 'Slice Thickness': [],
         'Software Versions': [], 'Protocol Name': [], 'Reconstruction Diameter': [],
         'Collimator Type': [], 'Rows': [], 'Columns': [], 'Pixel Spacing 0': [],
         'Pixel Spacing 1': [], 'Corrected Image': []}

for folders in sorted(os.listdir(path)):
    table['Patient'].append(folders)
    for files in os.listdir(os.path.join(path, folders)):
        if files == '000000.dcm':
            img = pydicom.dcmread(os.path.join(path, folders, files))
            table['Manufacturer'].append(img.Manufacturer)
            table['Manufacturer Model Name'].append(img.ManufacturerModelName)
            # table['Manufacturer Model Name'].append('') #ONLY HMR
            table['Slice Thickness'].append(img.SliceThickness)
            table['Software Versions'].append(img.SoftwareVersions)
            # table['Software Versions'].append('') #ONLY HMR
            table['Protocol Name'].append(img.ProtocolName)
            # table['Protocol Name'].append('') #ONLY HGJ
            table['Reconstruction Diameter'].append(img.ReconstructionDiameter)
            # table['Collimator Type'].append(img.CollimatorType)
            table['Collimator Type'].append('')
            table['Rows'].append(img.Rows)
            table['Columns'].append(img.Columns)
            table['Pixel Spacing 0'].append(img.PixelSpacing[0])
            table['Pixel Spacing 1'].append(img.PixelSpacing[1])
            table['Corrected Image'].append(img.CorrectedImage)
            # table['Corrected Image'].append('')  # ONLY HMR

df = pd.DataFrame(table)
print(df)
