import cv2
import numpy as np


def _normalize_uint8(data):
    return cv2.normalize(data, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def sobel_edge(img, ksize=3):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ksize = max(1, int(ksize))
    if ksize % 2 == 0:
        ksize += 1

    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)

    sobel = cv2.magnitude(sobelx, sobely)

    return _normalize_uint8(sobel)


def prewitt_edge(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    kernelx = np.array([[1,0,-1],[1,0,-1],[1,0,-1]])
    kernely = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])

    x = cv2.filter2D(gray, -1, kernelx)
    y = cv2.filter2D(gray, -1, kernely)

    prewitt = cv2.magnitude(x.astype(float), y.astype(float))

    return _normalize_uint8(prewitt)


def roberts_edge(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    kernelx = np.array([[1,0],[0,-1]])
    kernely = np.array([[0,1],[-1,0]])

    x = cv2.filter2D(gray, -1, kernelx)
    y = cv2.filter2D(gray, -1, kernely)

    roberts = cv2.magnitude(x.astype(float), y.astype(float))

    return _normalize_uint8(roberts)


def canny_edge(img, low_threshold=100, high_threshold=200):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    low = int(low_threshold)
    high = int(high_threshold)
    if high < low:
        low, high = high, low

    edges = cv2.Canny(gray, low, high)

    return edges