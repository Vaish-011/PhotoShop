import numpy as np
import cv2


def calculate_image_metrics(img):
    """Calculate metrics about an image for educational display."""
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img

    mean_val = np.mean(gray)
    std_val = np.std(gray)
    min_val = np.min(gray)
    max_val = np.max(gray)
    
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    entropy = -np.sum((hist / hist.sum()) * np.log2(hist / hist.sum() + 1e-8))

    return {
        "mean": float(mean_val),
        "std": float(std_val),
        "min": float(min_val),
        "max": float(max_val),
        "entropy": float(entropy),
        "contrast": float(std_val),
    }


def compare_images(before_img, after_img):
    """Compute quality metrics comparing two images."""
    if len(before_img.shape) == 3:
        before_gray = cv2.cvtColor(before_img, cv2.COLOR_RGB2GRAY)
    else:
        before_gray = before_img

    if len(after_img.shape) == 3:
        after_gray = cv2.cvtColor(after_img, cv2.COLOR_RGB2GRAY)
    else:
        after_gray = after_img

    mse = np.mean((before_gray.astype(float) - after_gray.astype(float)) ** 2)

    if mse == 0:
        psnr = 100.0
    else:
        max_pixel = 255.0
        psnr = 20 * np.log10(max_pixel / np.sqrt(mse))

    return {
        "mse": float(mse),
        "psnr": float(psnr),
        "before_metrics": calculate_image_metrics(before_img),
        "after_metrics": calculate_image_metrics(after_img),
    }


OPERATION_PRESETS = {
    "enhance_contrast": [
        {"op": "clahe", "params": {"clip_limit": 3.0, "tile_grid_size": 8}},
    ],
    "denoise": [
        {"op": "bilateral", "params": {"d": 9, "sigma_color": 75, "sigma_space": 75}},
    ],
    "edge_emphasize": [
        {"op": "grayscale", "params": {}},
        {"op": "canny", "params": {"low_threshold": 50, "high_threshold": 150}},
    ],
    "sharpen_details": [
        {"op": "gaussian", "params": {"ksize": 3, "sigma": 0}},
        {"op": "sharpen", "params": {}},
    ],
    "noise_analysis": [
        {"op": "gaussian_noise", "params": {"sigma": 15}},
    ],
    "morphology_analyze": [
        {"op": "grayscale", "params": {}},
        {"op": "erosion", "params": {"kernel_size": 5, "iterations": 1}},
        {"op": "dilation", "params": {"kernel_size": 5, "iterations": 1}},
    ],
}
