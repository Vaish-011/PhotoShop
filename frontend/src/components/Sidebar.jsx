function Sidebar({
  sections,
  selectedOperation,
  onSelectOperation,
  resetImage,
  undoLast,
  downloadImage,
  canUndo,
  disabled,
}) {
  return (
    <div className="sidebar">
      <h2>Toolbox</h2>
      <p className="sidebar-subtitle">Choose an operation, tune parameters, then apply.</p>

      {sections.map((section) => (
        <div key={section.title} className="section-block">
          <h3>{section.title}</h3>
          {section.operations.map((operation) => (
            <button
              key={operation.key}
              className={selectedOperation?.key === operation.key ? "is-active" : ""}
              onClick={() => onSelectOperation(operation)}
            >
              <span>{operation.label}</span>
              <small>{operation.description}</small>
            </button>
          ))}
        </div>
      ))}

      <div className="actions">
        <button onClick={undoLast} disabled={!canUndo}>
          Undo Last
        </button>
        <button onClick={resetImage} disabled={disabled}>
          Reset to Original
        </button>
        <button onClick={downloadImage} disabled={disabled}>
          Download PNG
        </button>
      </div>
    </div>
  );
}

export default Sidebar;