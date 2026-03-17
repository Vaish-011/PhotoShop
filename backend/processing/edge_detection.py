import cv2
import numpy as np


def sobel_edge(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    sobel = cv2.magnitude(sobelx, sobely)

    return np.uint8(sobel)


def prewitt_edge(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    kernelx = np.array([[1,0,-1],[1,0,-1],[1,0,-1]])
    kernely = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])

    x = cv2.filter2D(gray, -1, kernelx)
    y = cv2.filter2D(gray, -1, kernely)

    prewitt = cv2.magnitude(x.astype(float), y.astype(float))

    return np.uint8(prewitt)


def roberts_edge(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    kernelx = np.array([[1,0],[0,-1]])
    kernely = np.array([[0,1],[-1,0]])

    x = cv2.filter2D(gray, -1, kernelx)
    y = cv2.filter2D(gray, -1, kernely)

    roberts = cv2.magnitude(x.astype(float), y.astype(float))

    return np.uint8(roberts)


def canny_edge(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    edges = cv2.Canny(gray, 100, 200)

    return edges