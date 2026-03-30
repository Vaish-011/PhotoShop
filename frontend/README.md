# VisionLab Studio Frontend

VisionLab Studio is an advanced Digital Image Processing toolkit UI built with React and Vite.

## What makes this bonus-ready

- Backend-driven operation catalog (`/operations`) so tools and parameter sliders stay in sync.
- Adjustable parameters for major operations (intensity, smoothing, morphology, noise, frequency, edges).
- Processing modes:
	- Apply on original input
	- Apply on current output
- Image iteration workflow:
	- Undo last operation
	- Reset to original image
	- Download result as PNG
- Histogram visualization after each transformation.
- Responsive layout suitable for desktop and mobile demos.

## Run frontend

```bash
npm install
npm run dev
```

The app expects the Flask backend at `http://localhost:5000`.
