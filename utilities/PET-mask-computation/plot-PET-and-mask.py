"""
This script plots a slice of a PET scan with the corresponding mask.
"""


import os
import numpy as np
import matplotlib.pyplot as plt

path = '/home/davidhaberl/PycharmProjects/MasterThesis'

number = 33

pet = np.load(os.path.join(path, 'outfile.npy'))[:, :, number]
mask = np.load(os.path.join(path, 'GTV.npy'))[:, :, number]


plt.imshow(pet)
plt.imshow(mask, alpha=.5)
plt.show()
