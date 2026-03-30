import cv2
import numpy as np


def _odd_kernel(size):
    size = int(size)
    return size + 1 if size % 2 == 0 else max(size, 1)


def mean_filter(img, ksize=15):
    k = _odd_kernel(ksize)
    return cv2.blur(img, (k, k))


def gaussian_filter(img, ksize=15, sigma=0):
    k = _odd_kernel(ksize)
    return cv2.GaussianBlur(img, (k, k), sigma)


def median_filter(img, ksize=9):
    k = _odd_kernel(ksize)
    return cv2.medianBlur(img, k)


def sharpen_filter(img):

    kernel = np.array([
        [0,-1,0],
        [-1,9,-1],
        [0,-1,0]
    ])

    return cv2.filter2D(img, -1, kernel)


def laplacian_filter(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    lap = cv2.Laplacian(gray, cv2.CV_64F)

    return np.uint8(np.absolute(lap))


def bilateral_filter(img, d=9, sigma_color=75, sigma_space=75):
    return cv2.bilateralFilter(img, int(d), float(sigma_color), float(sigma_space))