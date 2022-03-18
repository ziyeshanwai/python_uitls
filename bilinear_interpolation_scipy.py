"""
https://stackoverflow.com/questions/55086971/scipy-interpolate-on-structured-2d-data-but-evaluate-at-unstructured-points
"""

import numpy as np
from scipy import interpolate


def f(x, y):
    return np.sin(x**2+y**2)


if __name__ == '__main__':
    x = np.arange(-5.01, 5.01, 0.25)
    y = np.arange(-5.01, 5.01, 0.2)
    z = f(*np.meshgrid(x, y, indexing='ij', sparse=True))
    func = interpolate.RegularGridInterpolator((x, y), z, method='linear', bounds_error=False, fill_value=np.nan)
    x_new = np.random.random(256*256)
    y_new = np.random.random(256*256)
    xy_new = list(zip(x_new,y_new))
    z_new = func(xy_new)  # func(xy_new)
    print(z_new.shape)