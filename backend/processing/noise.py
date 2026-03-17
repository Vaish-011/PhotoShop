import numpy as np
import cv2


def gaussian_noise(img):

    row, col, ch = img.shape

    mean = 0
    sigma = 25

    gauss = np.random.normal(mean, sigma, (row, col, ch))
    noisy = img + gauss

    noisy = np.clip(noisy, 0, 255)

    return noisy.astype(np.uint8)


def salt_pepper_noise(img):

    noisy = np.copy(img)

    prob = 0.05

    # salt
    salt = np.random.rand(*img.shape[:2]) < prob
    noisy[salt] = 255

    # pepper
    pepper = np.random.rand(*img.shape[:2]) < prob
    noisy[pepper] = 0

    return noisy


def speckle_noise(img):

    row, col, ch = img.shape

    gauss = np.random.randn(row, col, ch)

    noisy = img + img * gauss

    noisy = np.clip(noisy, 0, 255)

    return noisy.astype(np.uint8)