import cv2
import numpy as np


def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def negative(img):
    return 255 - img


def brightness(img, value=50):
    img = np.int16(img)
    img = img + value
    img = np.clip(img, 0, 255)
    return np.uint8(img)


def contrast(img, alpha=1.5):
    img = np.float32(img)
    img = img * alpha
    img = np.clip(img, 0, 255)
    return np.uint8(img)


def gamma_correction(img, gamma=1.5):
    gamma = max(gamma, 0.01)
    invGamma = 1.0 / gamma
    table = np.array([
        ((i / 255.0) ** invGamma) * 255
        for i in range(256)
    ]).astype("uint8")

    return cv2.LUT(img, table)