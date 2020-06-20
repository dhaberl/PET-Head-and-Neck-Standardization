"""
This script computes the bounding box of the images based on the masks.
"""


import os
import numpy as np


def bounding_box(arr):

    r = np.any(arr, axis=(1, 2))
    c = np.any(arr, axis=(0, 2))
    z = np.any(arr, axis=(0, 1))

    rmin, rmax = np.where(r)[0][[0, -1]]
    cmin, cmax = np.where(c)[0][[0, -1]]
    zmin, zmax = np.where(z)[0][[0, -1]]

    return rmin, rmax, cmin, cmax, zmin, zmax


def main():

    path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/resampled-3D-suv-pet-and-masks-prim-npy'

    dst_path = '/home/davidhaberl/PycharmProjects/MasterThesis/Data/Head-Neck-PET-CT/resampled-bb-3d-suv-pet-and-masks-prim-npy'

    dilated = 10

    for cohort in sorted(os.listdir(path)):
        os.makedirs(os.path.join(dst_path, cohort), exist_ok=True)

        for patient in sorted(os.listdir(os.path.join(path, cohort))):
            os.makedirs(os.path.join(dst_path, cohort, patient), exist_ok=True)

            for file in sorted(os.listdir(os.path.join(path, cohort, patient))):
                if file.startswith('mask'):
                    mask = np.load(os.path.join(path, cohort, patient, file))

                    # Get coordinates of bounding box
                    rmin, rmax, cmin, cmax, zmin, zmax = bounding_box(mask)

                    # TODO: Clemens fragen -> ich glaube hier ist ein Denkfehler bzgl Bounding-Box u. Dilatieren und zwar: Masken werden dilatiert und dann die Bounding-Box gezogen oder?
                    rmin = rmin - dilated
                    rmax = rmax + dilated
                    cmin = cmin - dilated
                    cmax = cmax + dilated
                    zmin = zmin - dilated
                    zmax = zmax + dilated

                    # Create new array
                    # print(mask.shape)
                    mask = mask[rmin:rmax, cmin:cmax, zmin:zmax]
                    # print(mask.shape)

                    # Save bounding-boxed masks
                    print('Saving mask...')
                    np.save(os.path.join(dst_path, cohort, patient, file), mask)

                if file.startswith('pet'):
                    pet = np.load(os.path.join(path, cohort, patient, file))

                    # Create new array
                    # print(pet.shape)
                    print('Saving pet...')
                    pet = pet[rmin:rmax, cmin:cmax, zmin:zmax]
                    # print(pet.shape)

                    # Save bounding-boxed pet
                    np.save(os.path.join(dst_path, cohort, patient, file), pet)


if __name__ == "__main__":
    main()
