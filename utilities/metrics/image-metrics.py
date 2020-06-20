"""
This script will contain different image metrics.
"""


import os
import numpy as np
import pandas as pd


def signal_to_noise_ratio(arr):
    """Computes the signal to noise ratio (SNR) of a given Numpy array."""
    m = np.mean(arr, axis=None)
    s = np.std(arr, axis=None)
    snr = m / s

    return snr


def main():
    path = 'D:\\QIMP\\MA\\3D-PET-NPY'

    table = {'Patient': [], 'SNR': []}

    for cohort in sorted(os.listdir(path)):
        print(cohort)

        for patient in sorted(os.listdir(os.path.join(path, cohort))):
            print(patient)

            for file in sorted(os.listdir(os.path.join(path, cohort, patient))):
                print(file)

                pet = np.load(os.path.join(path, cohort, patient, file))

                snr = signal_to_noise_ratio(pet)
                table['Patient'].append(patient)
                table['SNR'].append(snr)

    df = pd.DataFrame(table)
    print(df)


if __name__ == "__main__":
    main()
