from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
import io

from processing.intensity import (
    grayscale,
    negative,
    brightness,
    contrast,
    gamma_correction
)


from processing.morphology import (
    erosion,
    dilation,
    opening,
    closing,
    morphological_gradient
)

from processing.frequency import (
    fourier_spectrum,
    low_pass_filter,
    high_pass_filter
)

from processing.edge_detection import (
    sobel_edge,
    prewitt_edge,
    roberts_edge,
    canny_edge
)

from processing.histogram import (
    calculate_histogram,
    histogram_equalization,
    clahe_equalization
)

from processing.spatial_filters import (
    mean_filter,
    gaussian_filter,
    median_filter,
    sharpen_filter,
    laplacian_filter,
    bilateral_filter
)


from processing.noise import (
    gaussian_noise,
    salt_pepper_noise,
    speckle_noise
)

from utils import calculate_image_metrics, compare_images, OPERATION_PRESETS

app = Flask(__name__)
CORS(app)


def _get_int(name, default, minimum=None, maximum=None):
    value = request.form.get(name, default)
    try:
        value = int(value)
    except (TypeError, ValueError):
        value = default

    if minimum is not None:
        value = max(minimum, value)
    if maximum is not None:
        value = min(maximum, value)

    return value


def _get_float(name, default, minimum=None, maximum=None):
    value = request.form.get(name, default)
    try:
        value = float(value)
    except (TypeError, ValueError):
        value = default

    if minimum is not None:
        value = max(minimum, value)
    if maximum is not None:
        value = min(maximum, value)

    return value


OPERATION_HANDLERS = {
    "grayscale": lambda img: grayscale(img),
    "negative": lambda img: negative(img),
    "brightness": lambda img: brightness(img, value=_get_int("value", 50, -255, 255)),
    "contrast": lambda img: contrast(img, alpha=_get_float("alpha", 1.5, 0.1, 5.0)),
    "gamma": lambda img: gamma_correction(img, gamma=_get_float("gamma", 1.5, 0.1, 5.0)),
    "histogram_equalization": lambda img: histogram_equalization(img),
    "clahe": lambda img: clahe_equalization(
        img,
        clip_limit=_get_float("clip_limit", 2.0, 0.1, 10.0),
        tile_grid_size=_get_int("tile_grid_size", 8, 1, 32),
    ),
    "mean": lambda img: mean_filter(img, ksize=_get_int("ksize", 15, 1, 51)),
    "gaussian": lambda img: gaussian_filter(
        img,
        ksize=_get_int("ksize", 15, 1, 51),
        sigma=_get_float("sigma", 0, 0, 50),
    ),
    "median": lambda img: median_filter(img, ksize=_get_int("ksize", 9, 1, 51)),
    "sharpen": lambda img: sharpen_filter(img),
    "laplacian": lambda img: laplacian_filter(img),
    "bilateral": lambda img: bilateral_filter(
        img,
        d=_get_int("d", 9, 1, 25),
        sigma_color=_get_float("sigma_color", 75, 1, 200),
        sigma_space=_get_float("sigma_space", 75, 1, 200),
    ),
    "sobel": lambda img: sobel_edge(img, ksize=_get_int("ksize", 3, 1, 7)),
    "prewitt": lambda img: prewitt_edge(img),
    "roberts": lambda img: roberts_edge(img),
    "canny": lambda img: canny_edge(
        img,
        low_threshold=_get_int("low_threshold", 100, 0, 255),
        high_threshold=_get_int("high_threshold", 200, 0, 255),
    ),
    "fourier": lambda img: fourier_spectrum(img),
    "lowpass": lambda img: low_pass_filter(img, radius=_get_int("radius", 50, 1, 512)),
    "highpass": lambda img: high_pass_filter(img, radius=_get_int("radius", 30, 1, 512)),
    "gaussian_noise": lambda img: gaussian_noise(img, sigma=_get_float("sigma", 25, 1, 100)),
    "salt_pepper": lambda img: salt_pepper_noise(img, prob=_get_float("prob", 0.03, 0.001, 0.2)),
    "speckle": lambda img: speckle_noise(img, intensity=_get_float("intensity", 0.2, 0.01, 1.0)),
    "erosion": lambda img: erosion(
        img,
        kernel_size=_get_int("kernel_size", 5, 1, 31),
        iterations=_get_int("iterations", 1, 1, 10),
    ),
    "dilation": lambda img: dilation(
        img,
        kernel_size=_get_int("kernel_size", 5, 1, 31),
        iterations=_get_int("iterations", 1, 1, 10),
    ),
    "opening": lambda img: opening(img, kernel_size=_get_int("kernel_size", 5, 1, 31)),
    "closing": lambda img: closing(img, kernel_size=_get_int("kernel_size", 5, 1, 31)),
    "morph_gradient": lambda img: morphological_gradient(
        img,
        kernel_size=_get_int("kernel_size", 5, 1, 31),
    ),
}


OPERATION_SECTIONS = [
    {
        "title": "Intensity",
        "operations": [
            {"key": "grayscale", "label": "Grayscale", "description": "Convert image to luminance."},
            {"key": "negative", "label": "Negative", "description": "Invert all pixel values."},
            {
                "key": "brightness",
                "label": "Brightness",
                "description": "Shift pixel intensities by a constant value.",
                "params": [{"name": "value", "label": "Value", "type": "range", "min": -255, "max": 255, "step": 1, "default": 50}],
            },
            {
                "key": "contrast",
                "label": "Contrast",
                "description": "Scale pixel intensities.",
                "params": [{"name": "alpha", "label": "Alpha", "type": "range", "min": 0.1, "max": 5, "step": 0.1, "default": 1.5}],
            },
            {
                "key": "gamma",
                "label": "Gamma",
                "description": "Apply non-linear gamma correction.",
                "params": [{"name": "gamma", "label": "Gamma", "type": "range", "min": 0.1, "max": 5, "step": 0.1, "default": 1.5}],
            },
        ],
    },
    {
        "title": "Histogram",
        "operations": [
            {
                "key": "histogram_equalization",
                "label": "Histogram Equalization",
                "description": "Improve global contrast in grayscale space.",
            },
            {
                "key": "clahe",
                "label": "CLAHE",
                "description": "Adaptive local contrast enhancement.",
                "params": [
                    {"name": "clip_limit", "label": "Clip Limit", "type": "range", "min": 0.1, "max": 10, "step": 0.1, "default": 2.0},
                    {"name": "tile_grid_size", "label": "Tile Grid", "type": "range", "min": 1, "max": 32, "step": 1, "default": 8},
                ],
            },
        ],
    },
    {
        "title": "Spatial Filters",
        "operations": [
            {
                "key": "mean",
                "label": "Mean Blur",
                "description": "Average blur for low-pass smoothing.",
                "params": [{"name": "ksize", "label": "Kernel Size", "type": "range", "min": 1, "max": 51, "step": 2, "default": 15}],
            },
            {
                "key": "gaussian",
                "label": "Gaussian Blur",
                "description": "Gaussian smoothing controlled by sigma.",
                "params": [
                    {"name": "ksize", "label": "Kernel Size", "type": "range", "min": 1, "max": 51, "step": 2, "default": 15},
                    {"name": "sigma", "label": "Sigma", "type": "range", "min": 0, "max": 50, "step": 0.5, "default": 0},
                ],
            },
            {
                "key": "median",
                "label": "Median Filter",
                "description": "Excellent for impulse-noise removal.",
                "params": [{"name": "ksize", "label": "Kernel Size", "type": "range", "min": 1, "max": 51, "step": 2, "default": 9}],
            },
            {"key": "sharpen", "label": "Sharpen", "description": "Enhance local detail."},
            {"key": "laplacian", "label": "Laplacian", "description": "Second-order derivative response."},
            {
                "key": "bilateral",
                "label": "Bilateral",
                "description": "Edge-preserving smoothing.",
                "params": [
                    {"name": "d", "label": "Neighborhood", "type": "range", "min": 1, "max": 25, "step": 1, "default": 9},
                    {"name": "sigma_color", "label": "Sigma Color", "type": "range", "min": 1, "max": 200, "step": 1, "default": 75},
                    {"name": "sigma_space", "label": "Sigma Space", "type": "range", "min": 1, "max": 200, "step": 1, "default": 75},
                ],
            },
        ],
    },
    {
        "title": "Edge Detection",
        "operations": [
            {
                "key": "sobel",
                "label": "Sobel",
                "description": "Gradient-based edge detector.",
                "params": [{"name": "ksize", "label": "Kernel Size", "type": "range", "min": 1, "max": 7, "step": 2, "default": 3}],
            },
            {"key": "prewitt", "label": "Prewitt", "description": "Classic directional edge kernels."},
            {"key": "roberts", "label": "Roberts", "description": "Fast edge detector with 2x2 kernels."},
            {
                "key": "canny",
                "label": "Canny",
                "description": "Multi-stage detector with dual thresholds.",
                "params": [
                    {"name": "low_threshold", "label": "Low Threshold", "type": "range", "min": 0, "max": 255, "step": 1, "default": 100},
                    {"name": "high_threshold", "label": "High Threshold", "type": "range", "min": 0, "max": 255, "step": 1, "default": 200},
                ],
            },
        ],
    },
    {
        "title": "Noise",
        "operations": [
            {
                "key": "gaussian_noise",
                "label": "Gaussian Noise",
                "description": "Additive white Gaussian noise.",
                "params": [{"name": "sigma", "label": "Sigma", "type": "range", "min": 1, "max": 100, "step": 1, "default": 25}],
            },
            {
                "key": "salt_pepper",
                "label": "Salt & Pepper",
                "description": "Random impulse noise.",
                "params": [{"name": "prob", "label": "Probability", "type": "range", "min": 0.001, "max": 0.2, "step": 0.001, "default": 0.03}],
            },
            {
                "key": "speckle",
                "label": "Speckle",
                "description": "Multiplicative granular noise.",
                "params": [{"name": "intensity", "label": "Intensity", "type": "range", "min": 0.01, "max": 1, "step": 0.01, "default": 0.2}],
            },
        ],
    },
    {
        "title": "Morphology",
        "operations": [
            {
                "key": "erosion",
                "label": "Erosion",
                "description": "Shrink bright regions.",
                "params": [
                    {"name": "kernel_size", "label": "Kernel Size", "type": "range", "min": 1, "max": 31, "step": 1, "default": 5},
                    {"name": "iterations", "label": "Iterations", "type": "range", "min": 1, "max": 10, "step": 1, "default": 1},
                ],
            },
            {
                "key": "dilation",
                "label": "Dilation",
                "description": "Expand bright regions.",
                "params": [
                    {"name": "kernel_size", "label": "Kernel Size", "type": "range", "min": 1, "max": 31, "step": 1, "default": 5},
                    {"name": "iterations", "label": "Iterations", "type": "range", "min": 1, "max": 10, "step": 1, "default": 1},
                ],
            },
            {
                "key": "opening",
                "label": "Opening",
                "description": "Erosion followed by dilation.",
                "params": [{"name": "kernel_size", "label": "Kernel Size", "type": "range", "min": 1, "max": 31, "step": 1, "default": 5}],
            },
            {
                "key": "closing",
                "label": "Closing",
                "description": "Dilation followed by erosion.",
                "params": [{"name": "kernel_size", "label": "Kernel Size", "type": "range", "min": 1, "max": 31, "step": 1, "default": 5}],
            },
            {
                "key": "morph_gradient",
                "label": "Morph Gradient",
                "description": "Difference between dilation and erosion.",
                "params": [{"name": "kernel_size", "label": "Kernel Size", "type": "range", "min": 1, "max": 31, "step": 1, "default": 5}],
            },
        ],
    },
    {
        "title": "Frequency",
        "operations": [
            {"key": "fourier", "label": "Fourier Spectrum", "description": "Visualize magnitude spectrum."},
            {
                "key": "lowpass",
                "label": "Low Pass",
                "description": "Retain low frequencies in spectrum center.",
                "params": [{"name": "radius", "label": "Radius", "type": "range", "min": 1, "max": 512, "step": 1, "default": 50}],
            },
            {
                "key": "highpass",
                "label": "High Pass",
                "description": "Suppress low frequencies.",
                "params": [{"name": "radius", "label": "Radius", "type": "range", "min": 1, "max": 512, "step": 1, "default": 30}],
            },
        ],
    },
]


@app.route("/process", methods=["POST"])
def process_image():
    if "image" not in request.files:
        return jsonify({"error": "Image file is required."}), 400

    file = request.files["image"]
    operation = request.form.get("operation")

    if not operation:
        return jsonify({"error": "Operation is required."}), 400

    if operation not in OPERATION_HANDLERS:
        return jsonify({"error": f"Unsupported operation: {operation}"}), 400

    try:
        img = Image.open(file).convert("RGB")
    except Exception:
        return jsonify({"error": "Unable to read image."}), 400

    img_np = np.array(img)

    try:
        result = OPERATION_HANDLERS[operation](img_np)
    except Exception as exc:
        return jsonify({"error": f"Processing failed: {str(exc)}"}), 500

    # ensure correct datatype
    result = np.uint8(result)

    output = Image.fromarray(result)

    img_io = io.BytesIO()
    output.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")


@app.route("/operations", methods=["GET"])
def operations():
    return jsonify({"sections": OPERATION_SECTIONS})


@app.route("/histogram", methods=["POST"])
def histogram():

    file = request.files["image"]
    img = Image.open(file).convert("L")

    img_np = np.array(img)

    hist = calculate_histogram(img_np)

    return jsonify(hist)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/metrics", methods=["POST"])
def metrics():
    if "image" not in request.files:
        return jsonify({"error": "Image file is required."}), 400

    file = request.files["image"]

    try:
        img = Image.open(file).convert("RGB")
    except Exception:
        return jsonify({"error": "Unable to read image."}), 400

    img_np = np.array(img)
    metrics_data = calculate_image_metrics(img_np)

    return jsonify(metrics_data)


@app.route("/compare", methods=["POST"])
def compare():
    if "before" not in request.files or "after" not in request.files:
        return jsonify({"error": "Both before and after images required."}), 400

    try:
        before = np.array(Image.open(request.files["before"]).convert("RGB"))
        after = np.array(Image.open(request.files["after"]).convert("RGB"))
    except Exception:
        return jsonify({"error": "Unable to read images."}), 400

    comparison = compare_images(before, after)

    return jsonify(comparison)


@app.route("/presets", methods=["GET"])
def presets():
    preset_list = []
    for key, steps in OPERATION_PRESETS.items():
        preset_list.append({
            "id": key,
            "name": key.replace("_", " ").title(),
            "steps": steps,
        })

    return jsonify({"presets": preset_list})


if __name__ == "__main__":
    app.run(debug=True, port=5000)