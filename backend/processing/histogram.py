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


def clahe_equalization(img, clip_limit=2.0, tile_grid_size=8):

    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    tile = max(1, int(tile_grid_size))
    clahe = cv2.createCLAHE(clipLimit=float(clip_limit), tileGridSize=(tile, tile))

    return clahe.apply(img)