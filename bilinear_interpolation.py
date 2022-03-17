"""
https://eng.aurelienpierre.com/2020/03/bilinear-interpolation-on-images-stored-as-python-numpy-ndarray/
"""
import numpy as np
from numba import jit, prange
from PIL import Image
import matplotlib.pyplot as plt
import time


def interpolate_bilinear(array_in, width_in, height_in, array_out, width_out, height_out):
    for i in range(height_out):
        for j in range(width_out):
            # Relative coordinates of the pixel in output space
            x_out = j / width_out
            y_out = i / height_out

            # Corresponding absolute coordinates of the pixel in input space
            x_in = (x_out * width_in)
            y_in = (y_out * height_in)

            # Nearest neighbours coordinates in input space
            x_prev = int(np.floor(x_in))
            x_next = x_prev + 1
            y_prev = int(np.floor(y_in))
            y_next = y_prev + 1

            # Sanitize bounds - no need to check for < 0
            x_prev = min(x_prev, width_in - 1)
            x_next = min(x_next, width_in - 1)
            y_prev = min(y_prev, height_in - 1)
            y_next = min(y_next, height_in - 1)

            # Distances between neighbour nodes in input space
            Dy_next = y_next - y_in
            Dy_prev = 1. - Dy_next  # because next - prev = 1
            Dx_next = x_next - x_in
            Dx_prev = 1. - Dx_next  # because next - prev = 1

            # Interpolate over 3 RGB layers
            for c in range(3):
                array_out[i][j][c] = Dy_prev * (
                            array_in[y_next][x_prev][c] * Dx_next + array_in[y_next][x_next][c] * Dx_prev) \
                                     + Dy_next * (array_in[y_prev][x_prev][c] * Dx_next + array_in[y_prev][x_next][
                    c] * Dx_prev)

    return array_out


@jit(nopython=True, fastmath=True, nogil=True, cache=True, parallel=True)
def interpolate_bilinear_num(array_in, width_in, height_in, array_out, width_out, height_out):
    for i in prange(height_out):
        for j in prange(width_out):
            # Relative coordinates of the pixel in output space
            x_out = j / width_out
            y_out = i / height_out

            # Corresponding absolute coordinates of the pixel in input space
            x_in = (x_out * width_in)
            y_in = (y_out * height_in)

            # Nearest neighbours coordinates in input space
            x_prev = int(np.floor(x_in))
            x_next = x_prev + 1
            y_prev = int(np.floor(y_in))
            y_next = y_prev + 1

            # Sanitize bounds - no need to check for < 0
            x_prev = min(x_prev, width_in - 1)
            x_next = min(x_next, width_in - 1)
            y_prev = min(y_prev, height_in - 1)
            y_next = min(y_next, height_in - 1)

            # Distances between neighbour nodes in input space
            Dy_next = y_next - y_in
            Dy_prev = 1. - Dy_next  # because next - prev = 1
            Dx_next = x_next - x_in
            Dx_prev = 1. - Dx_next  # because next - prev = 1

            # Interpolate over 3 RGB layers

            array_out[i][j] = Dy_prev * (
                        array_in[y_next][x_prev][c] * Dx_next + array_in[y_next][x_next][c] * Dx_prev) \
                                 + Dy_next * (array_in[y_prev][x_prev][c] * Dx_next + array_in[y_prev][x_next][c] * Dx_prev)

    return array_out



if __name__ == "__main__":
    # load image
    im = Image.open("./images/dino0.png")
    width_2 = im.width * 4
    height_2 = im.height * 4


    # Go to normalized float and undo gamma
    # Note : sRGB gamma is not a pure power TF, but that will do
    im2 = (np.array(im) / 255.) ** 2.4

    # Interpolate in float64
    out = np.zeros((height_2, width_2, 3))
    s = time.time()
    out = interpolate_bilinear_num(im2, im.width, im.height, out, width_2, height_2)
    e = time.time()
    print("it takes {}s to interpolate".format(e - s))
    # Redo gamma and save back in uint8
    out = (out ** (1 / 2.4) * 255.).astype(np.uint8)
    Image.fromarray(out)
    plt.figure("dog")
    plt.subplot(1, 2, 1)
    plt.imshow(im)
    plt.subplot(1, 2, 2)
    plt.imshow(out)
    plt.show()

