import { useEffect, useState } from "react";
import axios from "axios";

const API_BASE = "http://localhost:5000";

export default function MetricsPanel({ image, beforeImage }) {
  const [metrics, setMetrics] = useState(null);
  const [beforeMetrics, setBeforeMetrics] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!image) {
      setMetrics(null);
      return;
    }

    const fetchMetrics = async () => {
      setLoading(true);
      try {
        const formData = new FormData();
        formData.append("image", image);
        const response = await axios.post(`${API_BASE}/metrics`, formData);
        setMetrics(response.data);
      } catch {
        setMetrics(null);
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
  }, [image]);

  useEffect(() => {
    if (!beforeImage) {
      setBeforeMetrics(null);
      return;
    }

    const fetchBeforeMetrics = async () => {
      try {
        const formData = new FormData();
        formData.append("image", beforeImage);
        const response = await axios.post(`${API_BASE}/metrics`, formData);
        setBeforeMetrics(response.data);
      } catch {
        setBeforeMetrics(null);
      }
    };

    fetchBeforeMetrics();
  }, [beforeImage]);

  if (!metrics) {
    return null;
  }

  const renderMetric = (label, value, unit = "") => (
    <div className="metric-row">
      <span className="metric-label">{label}</span>
      <span className="metric-value">
        {typeof value === "number" ? value.toFixed(2) : value}
        {unit && <span className="metric-unit">{unit}</span>}
      </span>
    </div>
  );

  return (
    <div className="metrics-panel">
      <h3>Image Analysis</h3>

      <div className="metrics-columns">
        <div className="metric-column">
          <h4>Current Image</h4>
          {renderMetric("Mean Intensity", metrics.mean)}
          {renderMetric("Std Deviation", metrics.std)}
          {renderMetric("Contrast", metrics.contrast)}
          {renderMetric("Entropy", metrics.entropy, " bits")}
          {renderMetric("Min Value", metrics.min)}
          {renderMetric("Max Value", metrics.max)}
        </div>

        {beforeMetrics && (
          <div className="metric-column">
            <h4>Before Processing</h4>
            {renderMetric("Mean Intensity", beforeMetrics.mean)}
            {renderMetric("Std Deviation", beforeMetrics.std)}
            {renderMetric("Contrast", beforeMetrics.contrast)}
            {renderMetric("Entropy", beforeMetrics.entropy, " bits")}
            {renderMetric("Min Value", beforeMetrics.min)}
            {renderMetric("Max Value", beforeMetrics.max)}
          </div>
        )}
      </div>

      {beforeMetrics && (
        <div className="metrics-changes">
          <h4>Changes</h4>
          <div className="change-row">
            <span>Mean Change:</span>
            <span
              className={`change-value ${
                metrics.mean > beforeMetrics.mean ? "increase" : "decrease"
              }`}
            >
              {(metrics.mean - beforeMetrics.mean).toFixed(2)}
            </span>
          </div>
          <div className="change-row">
            <span>Contrast Change:</span>
            <span
              className={`change-value ${
                metrics.contrast > beforeMetrics.contrast ? "increase" : "decrease"
              }`}
            >
              {(metrics.contrast - beforeMetrics.contrast).toFixed(2)}
            </span>
          </div>
          <div className="change-row">
            <span>Entropy Change:</span>
            <span
              className={`change-value ${
                metrics.entropy > beforeMetrics.entropy ? "increase" : "decrease"
              }`}
            >
              {(metrics.entropy - beforeMetrics.entropy).toFixed(2)}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
