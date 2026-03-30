import cv2
import numpy as np


def _build_kernel(kernel_size):
    kernel_size = max(1, int(kernel_size))
    return np.ones((kernel_size, kernel_size), np.uint8)


def erosion(img, kernel_size=5, iterations=1):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    kernel = _build_kernel(kernel_size)

    result = cv2.erode(gray, kernel, iterations=max(1, int(iterations)))

    return result


def dilation(img, kernel_size=5, iterations=1):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    kernel = _build_kernel(kernel_size)

    result = cv2.dilate(gray, kernel, iterations=max(1, int(iterations)))

    return result


def opening(img, kernel_size=5):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    kernel = _build_kernel(kernel_size)

    result = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)

    return result


def closing(img, kernel_size=5):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    kernel = _build_kernel(kernel_size)

    result = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)

    return result


def morphological_gradient(img, kernel_size=5):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    kernel = _build_kernel(kernel_size)

    result = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)

    return result