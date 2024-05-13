import numpy as np

def snr(original, coded):
    return 10 * np.log10(np.sum(original**2) / np.sum((original - coded)**2))