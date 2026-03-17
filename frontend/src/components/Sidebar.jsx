function Sidebar({ processImage, resetImage, downloadImage }) {
  return (
    <div className="sidebar">

      <h3>Intensity</h3>
      <button onClick={() => processImage("grayscale")}>Grayscale</button>
      <button onClick={() => processImage("negative")}>Negative</button>
      <button onClick={() => processImage("brightness")}>Brightness</button>
      <button onClick={() => processImage("contrast")}>Contrast</button>
      <button onClick={() => processImage("gamma")}>Gamma</button>

      <h3>Histogram</h3>
      <button onClick={() => processImage("histogram_equalization")}>
        Histogram Equalization
      </button>

      <h3>Spatial Filters</h3>
      <button onClick={() => processImage("mean")}>Mean</button>
      <button onClick={() => processImage("gaussian")}>Gaussian</button>
      <button onClick={() => processImage("median")}>Median</button>
      <button onClick={() => processImage("sharpen")}>Sharpen</button>
      <button onClick={() => processImage("laplacian")}>Laplacian</button>

      <h3>Edge Detection</h3>
      <button onClick={() => processImage("sobel")}>Sobel</button>
      <button onClick={() => processImage("prewitt")}>Prewitt</button>
      <button onClick={() => processImage("roberts")}>Roberts</button>
      <button onClick={() => processImage("canny")}>Canny</button>

      <h3>Noise</h3>
      <button onClick={() => processImage("gaussian_noise")}>Gaussian Noise</button>
      <button onClick={() => processImage("salt_pepper")}>Salt & Pepper</button>
      <button onClick={() => processImage("speckle")}>Speckle</button>

      <h3>Morphology</h3>
      <button onClick={() => processImage("erosion")}>Erosion</button>
      <button onClick={() => processImage("dilation")}>Dilation</button>
      <button onClick={() => processImage("opening")}>Opening</button>
      <button onClick={() => processImage("closing")}>Closing</button>

      <h3>Frequency</h3>
      <button onClick={() => processImage("fourier")}>Fourier</button>
      <button onClick={() => processImage("lowpass")}>Low Pass</button>
      <button onClick={() => processImage("highpass")}>High Pass</button>

      <hr/>

      <button onClick={resetImage}>Reset</button>
      <button onClick={downloadImage}>Download</button>

    </div>
  );
}

export default Sidebar;