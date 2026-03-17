import cv2
import numpy as np


def erosion(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    kernel = np.ones((5,5), np.uint8)

    result = cv2.erode(gray, kernel, iterations=1)

    return result


def dilation(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    kernel = np.ones((5,5), np.uint8)

    result = cv2.dilate(gray, kernel, iterations=1)

    return result


def opening(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    kernel = np.ones((5,5), np.uint8)

    result = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)

    return result


def closing(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    kernel = np.ones((5,5), np.uint8)

    result = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)

    return result


def morphological_gradient(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    kernel = np.ones((5,5), np.uint8)

    result = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)

    return result