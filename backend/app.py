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
    histogram_equalization
)

from processing.spatial_filters import (
    mean_filter,
    gaussian_filter,
    median_filter,
    sharpen_filter,
    laplacian_filter
)


from processing.noise import (
    gaussian_noise,
    salt_pepper_noise,
    speckle_noise
)

app = Flask(__name__)
CORS(app)


@app.route("/process", methods=["POST"])
def process_image():

    file = request.files["image"]
    operation = request.form.get("operation")

    img = Image.open(file).convert("RGB")
    img_np = np.array(img)

    # default result
    result = img_np

    # ---- operations ----

    if operation == "grayscale":
        result = grayscale(img_np)

    elif operation == "negative":
        result = negative(img_np)

    elif operation == "brightness":
        result = brightness(img_np)

    elif operation == "contrast":
        result = contrast(img_np)

    elif operation == "gamma":
        result = gamma_correction(img_np)

    elif operation == "histogram_equalization":
        result = histogram_equalization(img_np)

    elif operation == "mean":
        result = mean_filter(img_np)

    elif operation == "gaussian":
        result = gaussian_filter(img_np)

    elif operation == "median":
        result = median_filter(img_np)

    elif operation == "sharpen":
        result = sharpen_filter(img_np)

    elif operation == "laplacian":
        result = laplacian_filter(img_np)


    elif operation == "sobel":
        result = sobel_edge(img_np)

    elif operation == "prewitt":
        result = prewitt_edge(img_np)

    elif operation == "roberts":
        result = roberts_edge(img_np)

    elif operation == "canny":
        result = canny_edge(img_np)


    elif operation == "fourier":
        result = fourier_spectrum(img_np)

    elif operation == "lowpass":
        result = low_pass_filter(img_np)

    elif operation == "highpass":
        result = high_pass_filter(img_np)


    elif operation == "gaussian_noise":
        result = gaussian_noise(img_np)

    elif operation == "salt_pepper":
        result = salt_pepper_noise(img_np)

    elif operation == "speckle":
        result = speckle_noise(img_np)


    elif operation == "erosion":
        result = erosion(img_np)

    elif operation == "dilation":
        result = dilation(img_np)

    elif operation == "opening":
        result = opening(img_np)

    elif operation == "closing":
        result = closing(img_np)

    elif operation == "morph_gradient":
        result = morphological_gradient(img_np)

    # ensure correct datatype
    result = np.uint8(result)

    output = Image.fromarray(result)

    img_io = io.BytesIO()
    output.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")


@app.route("/histogram", methods=["POST"])
def histogram():

    file = request.files["image"]
    img = Image.open(file).convert("L")

    img_np = np.array(img)

    hist = cv2.calcHist([img_np], [0], None, [256], [0,256])
    hist = hist.flatten().tolist()

    return jsonify(hist)


if __name__ == "__main__":
    app.run(debug=True, port=5000)