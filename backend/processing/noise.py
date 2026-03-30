import numpy as np
import cv2


def gaussian_noise(img, sigma=25):

    row, col, ch = img.shape

    gauss = np.random.normal(0, sigma, (row, col, ch))
    noisy = img.astype(np.float32) + gauss

    noisy = np.clip(noisy, 0, 255)

    return noisy.astype(np.uint8)


def salt_pepper_noise(img, prob=0.03):

    noisy = np.copy(img)

    # salt
    salt = np.random.rand(*img.shape[:2]) < prob
    noisy[salt] = 255

    # pepper
    pepper = np.random.rand(*img.shape[:2]) < prob
    noisy[pepper] = 0

    return noisy


def speckle_noise(img, intensity=0.2):

    row, col, ch = img.shape

    gauss = np.random.randn(row, col, ch) * intensity

    noisy = img.astype(np.float32) + img.astype(np.float32) * gauss

    noisy = np.clip(noisy, 0, 255)

    return noisy.astype(np.uint8)