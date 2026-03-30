import { useState } from "react";

export default function BeforeAfterSlider({ before, after }) {
  const [splitPosition, setSplitPosition] = useState(50);
  const [isDragging, setIsDragging] = useState(false);

  if (!before || !after) {
    return null;
  }

  const handleMouseDown = () => {
    setIsDragging(true);
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const position = ((e.clientX - rect.left) / rect.width) * 100;
    setSplitPosition(Math.min(Math.max(position, 0), 100));
  };

  return (
    <div className="before-after-container">
      <h3>Before & After Comparison</h3>
      <p>Drag the divider to compare</p>
      <div
        className="before-after-split"
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        <div className="split-half" style={{ flex: splitPosition }}>
          <div className="split-label">Original</div>
          <img src={before} alt="Before" className="split-image" />
        </div>
        <div
          className="split-divider"
          onMouseDown={handleMouseDown}
          style={{ cursor: isDragging ? "grabbing" : "ew-resize" }}
        />
        <div className="split-half" style={{ flex: 100 - splitPosition }}>
          <div className="split-label">Enhanced</div>
          <img src={after} alt="After" className="split-image" />
        </div>
      </div>
    </div>
  );
}
