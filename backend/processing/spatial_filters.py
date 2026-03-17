import cv2
import numpy as np


def mean_filter(img):
    return cv2.blur(img, (15,15))


def gaussian_filter(img):
    return cv2.GaussianBlur(img, (15,15), 0)


def median_filter(img):
    return cv2.medianBlur(img, 9)


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