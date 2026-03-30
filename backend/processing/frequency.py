import cv2
import numpy as np


def fourier_spectrum(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)

    magnitude = 20 * np.log(np.abs(fshift) + 1)

    max_value = np.max(magnitude)
    if max_value == 0:
        return np.zeros_like(gray, dtype=np.uint8)

    magnitude = np.uint8(255 * magnitude / max_value)

    return magnitude


def low_pass_filter(img, radius=50):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    rows, cols = gray.shape
    crow, ccol = rows // 2, cols // 2

    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)

    mask = np.zeros((rows, cols), np.uint8)

    r = max(1, min(int(radius), min(crow, ccol) - 1))
    mask[crow-r:crow+r, ccol-r:ccol+r] = 1

    fshift = fshift * mask

    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)

    img_back = np.abs(img_back)

    return np.uint8(img_back)



def high_pass_filter(img, radius=30):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    rows, cols = gray.shape
    crow, ccol = rows // 2, cols // 2

    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)

    mask = np.ones((rows, cols), np.uint8)

    r = max(1, min(int(radius), min(crow, ccol) - 1))
    mask[crow-r:crow+r, ccol-r:ccol+r] = 0

    fshift = fshift * mask

    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)

    img_back = np.abs(img_back)

    return np.uint8(img_back)