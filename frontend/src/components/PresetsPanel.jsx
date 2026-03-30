import { useEffect, useState } from "react";
import axios from "axios";

const API_BASE = "http://localhost:5000";

export default function PresetsPanel({ onApplyPreset }) {
  const [presets, setPresets] = useState([]);
  const [loadingPresets, setLoadingPresets] = useState(true);

  useEffect(() => {
    const fetchPresets = async () => {
      try {
        const response = await axios.get(`${API_BASE}/presets`);
        setPresets(response.data.presets || []);
      } catch {
        // Silently fail if presets unavailable
      } finally {
        setLoadingPresets(false);
      }
    };
    fetchPresets();
  }, []);

  if (loadingPresets || !presets.length) {
    return null;
  }

  return (
    <div className="presets-panel">
      <h3>Quick Start Workflows</h3>
      <p>Apply multi-step preset workflows for teaching demonstrations</p>
      <div className="presets-grid">
        {presets.map((preset) => (
          <button
            key={preset.id}
            className="preset-card"
            onClick={() => onApplyPreset(preset)}
          >
            <h4>{preset.name}</h4>
            <p>{preset.steps.length} step{preset.steps.length !== 1 ? "s" : ""}</p>
          </button>
        ))}
      </div>
    </div>
  );
}
