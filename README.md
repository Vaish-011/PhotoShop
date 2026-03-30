# VisionLab Studio

**A professional Digital Image Processing educational toolkit for teaching and learning**

## Overview

VisionLab Studio is a comprehensive platform designed specifically for educators teaching Digital Image Processing to students. It combines a powerful backend processing engine with an intuitive, modern frontend that makes complex image processing concepts visual and interactive.

### Why VisionLab Studio?

✅ **Educational Excellence**
- Structured teaching notes for every operation
- Live metrics that quantify changes
- Before/after comparison for visual learning
- Processing timeline showing cumulative effects

✅ **Modern User Experience**
- Clean, professional interface
- Real-time parameter adjustment
- Smooth, responsive interactions
- Mobile-friendly responsive design

✅ **Comprehensive Functionality**
- 30+ image processing operations
- 6 multi-step preset workflows
- Tunable parameters for every operation
- Live histogram analysis
- Quality metrics (MSE, PSNR, entropy, contrast)

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Installation

```bash
# Clone or extract the project
cd PhotoShop

# Backend setup
cd backend
pip install flask flask-cors opencv-python pillow numpy
python app.py

# Frontend setup (in a new terminal)
cd frontend
npm install
npm run dev
```

Backend will run on `http://localhost:5000`  
Frontend will run on `http://localhost:5173`

## Features

### 1. Operation Categories

#### Intensity Transforms
- Grayscale conversion
- Negative (invert)
- Brightness adjustment
- Contrast scaling
- Gamma correction

#### Histogram Processing
- Histogram equalization
- CLAHE (Contrast Limited Adaptive Histogram Equalization)

#### Spatial Filtering
- Mean filter (box blur)
- Gaussian blur (tunable sigma)
- Median filter
- Sharpen
- Laplacian (edge emphasis)
- Bilateral (edge-preserving denoising)

#### Edge Detection
- Sobel (gradient-based)
- Prewitt (directional)
- Roberts (compact operators)
- Canny (multi-stage optimal)

#### Noise Modeling
- Gaussian noise (tunable sigma)
- Salt & pepper noise (tunable probability)
- Speckle noise (tunable intensity)

#### Morphological Operations
- Erosion (shrinking)
- Dilation (expanding)
- Opening (denoise)
- Closing (fill holes)
- Morphological gradient (boundary detection)

#### Frequency Domain
- Fourier spectrum visualization
- Low-pass filtering (tunable radius)
- High-pass filtering (tunable radius)

### 2. Teaching-Focused Features

**Classroom Visualization Guide**
- Concept explanation for each operation
- Teaching objective clarity
- Student observation points
- Demo tips

**Live Metrics Dashboard**
- Mean intensity
- Standard deviation (contrast)
- Entropy (information content)
- Min/Max pixel values
- Before/after comparison

**Before/After Slider**
- Interactive comparison scrubber
- Helps students see subtle differences
- Perfect for projection in lecture

**Processing Timeline**
- Shows sequence of applied operations
- Demonstrates cumulative effects
- Educational narrative building

**Quick-Start Presets**
- Enhance Contrast (CLAHE)
- Denoise (Bilateral filtering)
- Edge Emphasize (Grayscale + Canny)
- Sharpen Details (Gaussian + Sharpen)
- Noise Analysis (Gaussian noise addition)
- Morphology Analyze (Erosion + Dilation)

### 3. Parameter Tuning

Every operation with parameters includes real-time sliders:
- **Kernel sizes**: 1-51 pixels
- **Filter radii**: 1-512 pixels
- **Thresholds**: 0-255
- **Sigmas**: 0.1-50 with precision control
- **Intensities**: Domain-specific ranges

### 4. Image Analysis

**Histogram Visualization**
- Real-time histogram after each operation
- Visual representation of intensity distribution
- Tool for understanding histogram-based techniques

**Quality Metrics**
- MSE (Mean Squared Error)
- PSNR (Peak Signal-to-Noise Ratio)
- Entropy changes
- Contrast analysis

## API Documentation

### Processing Endpoint
```
POST /process
- image (file): Input image
- operation (string): Operation key
- [param_name] (float/int): Parameter values
Returns: Processed image (PNG)
```

### Metrics Endpoint
```
POST /metrics
- image (file): Input image
Returns: {mean, std, contrast, entropy, min, max}
```

### Comparison Endpoint
```
POST /compare
- before (file): Original image
- after (file): Processed image
Returns: {mse, psnr, before_metrics, after_metrics}
```

### Operations List
```
GET /operations
Returns: {sections: [{title, operations: [{key, label, description, params}]}]}
```

### Presets
```
GET /presets
Returns: {presets: [{id, name, steps}]}
```

## Project Structure

```
PhotoShop/
├── backend/
│   ├── app.py                 # Flask server
│   ├── utils.py               # Metrics & presets
│   ├── processing/
│   │   ├── intensity.py       # Intensity transforms
│   │   ├── spatial_filters.py # Blurring & sharpening
│   │   ├── edge_detection.py  # Edge operators
│   │   ├── frequency.py       # Fourier & filtering
│   │   ├── noise.py           # Noise generation
│   │   ├── morphology.py      # Erosion & dilation
│   │   └── histogram.py       # Histogram processing
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                  # Main app
│   │   ├── App.css                  # Modern styles
│   │   ├── main.jsx
│   │   ├── components/
│   │   │   ├── ImageUpload.jsx      # Main workflow
│   │   │   ├── Sidebar.jsx          # Operation browser
│   │   │   ├── Histogram.jsx        # Histogram chart
│   │   │   ├── BeforeAfterSlider.jsx# Comparison tool
│   │   │   ├── PresetsPanel.jsx     # Quick templates
│   │   │   └── MetricsPanel.jsx     # Analysis display
│   │   └── index.css
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── TEACHERS_GUIDE.md         # Teaching instructions
└── README.md                 # This file
```

## For Educators

See [TEACHERS_GUIDE.md](TEACHERS_GUIDE.md) for:
- Teaching strategies
- Sample classroom scenarios
- Assessment ideas
- Feature usage tips
- Preset explanations

## Teaching Scenarios

### Scenario 1: Intensity Transforms (30 min)
1. Load a portrait image
2. Show grayscale conversion with color mapping explanation
3. Apply brightness/contrast with metric tracking
4. Use before/after slider to compare
5. Discuss histogram changes

### Scenario 2: Noise & Denoising (45 min)
1. Load a clean image
2. Add Gaussian noise (escalating sigma)
3. Show metrics deterioration
4. Apply bilateral filter
5. Compare before/after/denoised
6. Discuss trade-offs using metrics

### Scenario 3: Edge Detection (40 min)
1. Load test image
2. Apply grayscale
3. Try different edge detectors (Sobel, Canny)
4. Adjust Canny thresholds in real-time
5. Use timeline to show workflow
6. Compare metric changes

### Scenario 4: Frequency Domain (50 min)
1. Show Fourier spectrum visualization
2. Apply low-pass filter with tunable radius
3. Show frequency removal effect
4. Apply high-pass filter
5. Discuss complementary filtering
6. Use histogram to show frequency content changes

## Performance Notes

- **Image Size**: Works best with images up to 2048x2048
- **Processing Speed**: Most operations complete in <500ms
- **Memory**: Efficient numpy operations
- **Scalability**: Can handle batch processing mode (future feature)

## Troubleshooting

### Backend won't start
```bash
pip install -r requirements.txt  # Ensure dependencies
python app.py  # Check for port 5000 conflicts
```

### Frontend shows "Cannot connect to backend"
```bash
# Verify backend is running
curl http://localhost:5000/health
# Should return: {"status": "ok"}
```

### Images not processing
- Check file format (PNG, JPG supported)
- Ensure image is under 10MB
- Try with a different image
- Check browser console for errors

## Browser Support

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Future Roadmap

- [ ] Batch processing mode
- [ ] Region of Interest (ROI) tools
- [ ] Custom filter kernel design
- [ ] Export analysis reports
- [ ] Student collaboration features
- [ ] Dark mode toggle
- [ ] Keyboard shortcuts
- [ ] Undo/Redo stack visualization
- [ ] Video processing support
- [ ] Real-time webcam input

## Contributing

This project is designed for educational use. Suggestions for improvement are welcome!

## License

Educational use. See institution policies for distribution.

## Support

For issues or questions:
1. Check TEACHERS_GUIDE.md
2. Review sample workflows
3. Test with different images
4. Check browser console for errors

---

**Built for educators, by educators.**  
Making Digital Image Processing concepts visual, interactive, and truly understandable.
