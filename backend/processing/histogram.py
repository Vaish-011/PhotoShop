import cv2
import numpy as np


def calculate_histogram(img):

    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    hist = cv2.calcHist([img], [0], None, [256], [0,256])

    hist = hist.flatten().tolist()

    return hist

def histogram_equalization(img):

    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    equalized = cv2.equalizeHist(img)

    return equalized