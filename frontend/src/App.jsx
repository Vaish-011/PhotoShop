import ImageUpload from "./components/ImageUpload";
import "./App.css";

function App() {
  return (
    <div className="app-shell">
      <header className="hero">
        <div className="hero-badge">🎓 Educational Toolkit for DIP Teaching</div>
        <h1>VisionLab Studio</h1>
        <p className="hero-subtitle">
          A professional digital image processing platform designed for educators and students.
          Master intensity transforms, filtering, morphology, edge detection, and frequency-domain
          analysis through interactive visualization and real-time metrics.
        </p>
        <div className="hero-features">
          <span>📊 Live Metrics</span>
          <span>🔄 Before/After Comparison</span>
          <span>⚡ Preset Templates</span>
          <span>📈 Histogram Analysis</span>
        </div>
      </header>
      <ImageUpload />
    </div>
  );
}

export default App;