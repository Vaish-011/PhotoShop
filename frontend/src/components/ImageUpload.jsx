import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import Histogram from "./Histogram";
import BeforeAfterSlider from "./BeforeAfterSlider";
import PresetsPanel from "./PresetsPanel";
import MetricsPanel from "./MetricsPanel";
import Sidebar from "./Sidebar";
import "../App.css";

const API_BASE = "http://localhost:5000";

const TEACHING_NOTES = {
  grayscale: {
    concept: "Color to intensity mapping",
    objective: "Show how RGB information is projected to one luminance channel.",
    observe: "Texture stays, chromatic information disappears.",
  },
  negative: {
    concept: "Point-wise intensity transform",
    objective: "Demonstrate invert transform: s = 255 - r.",
    observe: "Bright regions become dark and vice versa.",
  },
  brightness: {
    concept: "Additive intensity shift",
    objective: "Explain histogram translation along x-axis.",
    observe: "Overall exposure changes while shapes remain.",
  },
  contrast: {
    concept: "Multiplicative scaling",
    objective: "Relate slope changes in intensity mapping.",
    observe: "Highlights and shadows separate more strongly.",
  },
  gamma: {
    concept: "Non-linear mapping",
    objective: "Teach power-law correction and display compensation.",
    observe: "Midtones shift without linear clipping behavior.",
  },
  histogram_equalization: {
    concept: "Global histogram remapping",
    objective: "Show CDF-based contrast enhancement.",
    observe: "Low-contrast images gain global spread.",
  },
  clahe: {
    concept: "Adaptive local enhancement",
    objective: "Compare local vs global contrast enhancement.",
    observe: "Local details improve with limited noise boosting.",
  },
  mean: {
    concept: "Linear low-pass smoothing",
    objective: "Explain neighborhood averaging.",
    observe: "Noise reduces and edges soften.",
  },
  gaussian: {
    concept: "Weighted low-pass smoothing",
    objective: "Teach Gaussian kernel and sigma impact.",
    observe: "Natural blur with reduced ringing.",
  },
  median: {
    concept: "Order-statistic filter",
    objective: "Show robustness against impulse noise.",
    observe: "Salt-and-pepper noise drops with edge retention.",
  },
  sharpen: {
    concept: "High-frequency emphasis",
    objective: "Introduce kernel-based detail enhancement.",
    observe: "Edges and textures become more prominent.",
  },
  laplacian: {
    concept: "Second derivative response",
    objective: "Highlight rapid intensity changes.",
    observe: "Edge-like outlines with noise sensitivity.",
  },
  bilateral: {
    concept: "Edge-preserving denoise",
    objective: "Teach joint spatial-range filtering.",
    observe: "Smooth flat regions while preserving boundaries.",
  },
  sobel: {
    concept: "Gradient magnitude",
    objective: "Connect derivatives and edge orientation.",
    observe: "Stronger response on directional edges.",
  },
  prewitt: {
    concept: "Directional derivative kernels",
    objective: "Compare classic edge masks.",
    observe: "Similar to Sobel with different weighting.",
  },
  roberts: {
    concept: "Diagonal edge gradients",
    objective: "Demonstrate compact edge operators.",
    observe: "Fast but more sensitive to noise.",
  },
  canny: {
    concept: "Multi-stage optimal edge detection",
    objective: "Explain thresholds and hysteresis.",
    observe: "Cleaner edges with reduced false positives.",
  },
  fourier: {
    concept: "Frequency-domain representation",
    objective: "Show image energy distribution by frequency.",
    observe: "Center holds low frequencies, outer region high frequencies.",
  },
  lowpass: {
    concept: "Frequency-domain smoothing",
    objective: "Relate mask radius to blur strength.",
    observe: "Fine details attenuate as radius shrinks.",
  },
  highpass: {
    concept: "Frequency-domain edge enhancement",
    objective: "Teach removal of low-frequency background.",
    observe: "Contours and texture become dominant.",
  },
  gaussian_noise: {
    concept: "Additive stochastic noise",
    objective: "Model sensor noise assumptions.",
    observe: "Grain increases with sigma.",
  },
  salt_pepper: {
    concept: "Impulse corruption model",
    objective: "Use as a denoising benchmark.",
    observe: "Random bright/dark pixels appear sparsely.",
  },
  speckle: {
    concept: "Multiplicative noise",
    objective: "Discuss coherent imaging noise models.",
    observe: "Noise depends on local intensity.",
  },
  erosion: {
    concept: "Morphological shrink",
    objective: "Teach structuring element effects.",
    observe: "Foreground regions contract.",
  },
  dilation: {
    concept: "Morphological grow",
    objective: "Demonstrate region expansion.",
    observe: "Foreground regions expand.",
  },
  opening: {
    concept: "Erosion then dilation",
    objective: "Explain small-noise removal.",
    observe: "Small bright artifacts are removed.",
  },
  closing: {
    concept: "Dilation then erosion",
    objective: "Teach small-hole filling.",
    observe: "Small dark gaps are reduced.",
  },
  morph_gradient: {
    concept: "Boundary extraction",
    objective: "Show contour emphasis via morphology.",
    observe: "Object boundaries are highlighted.",
  },
};

function defaultsFromParams(params = []) {
  return params.reduce((acc, param) => {
    acc[param.name] = param.default;
    return acc;
  }, {});
}

function ImageUpload() {
  const [sections, setSections] = useState([]);
  const [selectedOperation, setSelectedOperation] = useState(null);
  const [params, setParams] = useState({});
  const [loadingOps, setLoadingOps] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState("");
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [histogram, setHistogram] = useState(null);
  const [history, setHistory] = useState([]);
  const [original, setOriginal] = useState(null);
  const [originalFile, setOriginalFile] = useState(null);
  const [mode, setMode] = useState("current");

  useEffect(() => {
    const fetchOperations = async () => {
      try {
        const response = await axios.get(`${API_BASE}/operations`);
        const loadedSections = response.data.sections || [];
        setSections(loadedSections);

        const firstOperation = loadedSections[0]?.operations?.[0] || null;
        setSelectedOperation(firstOperation);
        setParams(defaultsFromParams(firstOperation?.params));
      } catch {
        setError("Could not load operation list. Ensure backend is running on port 5000.");
      } finally {
        setLoadingOps(false);
      }
    };

    fetchOperations();
  }, []);

  const canProcess = useMemo(
    () => image && selectedOperation && !processing,
    [image, selectedOperation, processing]
  );

  const teachingNote = useMemo(() => {
    if (!selectedOperation) {
      return null;
    }

    return (
      TEACHING_NOTES[selectedOperation.key] || {
        concept: "Image transformation",
        objective: "Discuss algorithm behavior in spatial or frequency domain.",
        observe: "Observe visual changes and correlate with histogram trends.",
      }
    );
  }, [selectedOperation]);

  const getHistogram = async (fileForHistogram = image) => {
    if (!fileForHistogram) {
      return;
    }

    try {
      const formData = new FormData();
      formData.append("image", fileForHistogram);

      const response = await axios.post(`${API_BASE}/histogram`, formData);
      setHistogram(response.data);
    } catch {
      setHistogram(null);
    }
  };

  const handleImageChange = async (event) => {
    const file = event.target.files[0];
    if (!file) {
      return;
    }

    const url = URL.createObjectURL(file);
    setImage(file);
    setOriginalFile(file);
    setPreview(url);
    setOriginal(url);
    setHistory([]);
    setError("");
    setMode("current");

    await getHistogram(file);
  };

  const applyOperation = async () => {
    if (!canProcess) {
      return;
    }

    setProcessing(true);
    setError("");

    try {
      const formData = new FormData();
      const sourceImage = mode === "original" ? originalFile : image;

      formData.append("image", sourceImage);
      formData.append("operation", selectedOperation.key);

      Object.entries(params).forEach(([name, value]) => {
        formData.append(name, String(value));
      });

      const response = await axios.post(`${API_BASE}/process`, formData, {
        responseType: "blob",
      });

      const blob = response.data;
      const url = URL.createObjectURL(blob);

      setHistory((prev) => [
        ...prev,
        { image, preview, operationLabel: selectedOperation.label },
      ]);
      setPreview(url);

      const nextFile = new File([blob], `processed-${selectedOperation.key}.png`, {
        type: "image/png",
      });
      setImage(nextFile);

      await getHistogram(nextFile);
    } catch {
      setError("Processing failed. Retry with different parameters.");
    } finally {
      setProcessing(false);
    }
  };

  const resetImage = async () => {
    if (!original || !originalFile) {
      return;
    }

    setPreview(original);
    setImage(originalFile);
    setHistory([]);
    setMode("current");
    setError("");
    await getHistogram(originalFile);
  };

  const undoLast = async () => {
    if (!history.length) {
      return;
    }

    const last = history[history.length - 1];
    setHistory((prev) => prev.slice(0, -1));
    setImage(last.image);
    setPreview(last.preview);
    await getHistogram(last.image);
  };

  const selectOperation = (operation) => {
    setSelectedOperation(operation);
    setParams(defaultsFromParams(operation?.params));
  };

  const updateParam = (name, value, step) => {
    const nextValue = step >= 1 ? Number(value) : Number.parseFloat(value);
    setParams((prev) => ({ ...prev, [name]: nextValue }));
  };

  const downloadImage = () => {
    if (!preview) {
      return;
    }

    const link = document.createElement("a");
    link.href = preview;
    link.download = "visionlab-output.png";
    link.click();
  };

  return (
    <div className="container">
      <Sidebar
        sections={sections}
        selectedOperation={selectedOperation}
        onSelectOperation={selectOperation}
        resetImage={resetImage}
        undoLast={undoLast}
        downloadImage={downloadImage}
        canUndo={history.length > 0}
        disabled={!image || processing}
      />

      <div className="workspace">
        <div className="workspace-top">
          <div>
            <h2>Load an Image</h2>
            <p>Supports JPG and PNG. Tune parameters and compare iterative outputs.</p>
          </div>
          <input type="file" accept="image/*" onChange={handleImageChange} />
        </div>

        <div className="mode-switch">
          <span>Processing Source:</span>
          <button
            className={mode === "original" ? "selected" : ""}
            onClick={() => setMode("original")}
          >
            Original Image
          </button>
          <button
            className={mode === "current" ? "selected" : ""}
            onClick={() => setMode("current")}
          >
            Current Result
          </button>
        </div>

        {loadingOps && <p>Loading toolkit operations...</p>}

        {selectedOperation && (
          <div className="parameter-panel">
            <h3>{selectedOperation.label}</h3>
            <p>{selectedOperation.description}</p>

            {selectedOperation.params?.length ? (
              selectedOperation.params.map((param) => (
                <label key={param.name}>
                  <div className="param-header">
                    <span>{param.label}</span>
                    <strong>{params[param.name]}</strong>
                  </div>
                  <input
                    type="range"
                    min={param.min}
                    max={param.max}
                    step={param.step}
                    value={params[param.name] ?? param.default}
                    onChange={(event) =>
                      updateParam(param.name, event.target.value, param.step)
                    }
                  />
                </label>
              ))
            ) : (
              <p className="param-empty">This operation has no tunable parameters.</p>
            )}

            <div className="teaching-panel">
              <h4>Classroom Visualization Guide</h4>
              <p>
                <strong>Concept:</strong> {teachingNote?.concept}
              </p>
              <p>
                <strong>Teaching Objective:</strong> {teachingNote?.objective}
              </p>
              <p>
                <strong>What Students Should Observe:</strong> {teachingNote?.observe}
              </p>
              <p>
                <strong>Demo Tip:</strong> Run once in Original mode and once in Current mode,
                then compare histogram shifts.
              </p>
            </div>
          </div>
        )}

        {error && <p className="error-text">{error}</p>}
        {processing && <p className="processing-text">Processing image...</p>}

        {preview && (
          <div className="preview-wrap">
            <img src={preview} alt="Processed preview" />
            <div className="preview-actions">
              <button className="apply-btn" onClick={applyOperation} disabled={!canProcess}>
                {processing ? "Applying..." : `Apply ${selectedOperation?.label || "Operation"}`}
              </button>
              <span>
                Steps in pipeline: <strong>{history.length}</strong>
              </span>
            </div>
          </div>
        )}

        {!!history.length && (
          <div className="timeline-panel">
            <h3>Processing Timeline</h3>
            <p>Use this sequence while teaching to discuss cumulative effects.</p>
            <ol>
              {history.map((step, index) => (
                <li key={index}>
                  Step {index + 1}: {step.operationLabel}
                </li>
              ))}
              <li>Current: {selectedOperation?.label || "Operation"}</li>
            </ol>
          </div>
        )}

        {preview && original && (
          <BeforeAfterSlider before={original} after={preview} />
        )}

        <PresetsPanel onApplyPreset={(preset) => {}} />

        <MetricsPanel image={image} beforeImage={originalFile} />

        {histogram && <Histogram data={histogram} />}
      </div>
    </div>
  );
}

export default ImageUpload;