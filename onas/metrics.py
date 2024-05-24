import numpy as np

def psnr(original, coded):
    mse = np.mean((original - coded) ** 2)
    if mse == 0:
        return float('inf')
    return round(10 * np.log10(255**2 / mse), 2)