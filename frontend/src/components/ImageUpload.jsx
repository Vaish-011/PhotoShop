import { useState } from "react";
import axios from "axios";
import Histogram from "./Histogram";
import Sidebar from "./Sidebar";
import "../App.css";

function ImageUpload() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [histogram, setHistogram] = useState(null);
  const [original, setOriginal] = useState(null);
  const [mode, setMode] = useState("current");
// Add this line after the existing useState declarations
const [originalImage, setOriginalImage] = useState(null);

// Update handleImageChange
const handleImageChange = (e) => {
  const file = e.target.files[0];
  setImage(file);
  setOriginalImage(file);  // Now this will work
  const url = URL.createObjectURL(file);
  setPreview(url);
  setOriginal(url);
};
  

const resetImage = () => {
  setPreview(original);
  setImage(originalImage);
  setHistogram(null);
  setMode("current");
};

const getHistogram = async () => {

  const formData = new FormData();
  formData.append("image", image);

  const res = await axios.post(
    "http://localhost:5000/histogram",
    formData
  );

  setHistogram(res.data);
};

const downloadImage = () => {
  const link = document.createElement("a");
  link.href = preview;
  link.download = "processed_image.png";
  link.click();
};

const processImage = async (operation) => {

  const formData = new FormData();

  if (mode === "original") {
    formData.append("image", originalImage);
  } else {
    formData.append("image", image);
  }

  formData.append("operation", operation);

  const res = await axios.post(
    "http://localhost:5000/process",
    formData,
    { responseType: "blob" }
  );

  const url = URL.createObjectURL(res.data);
  setPreview(url);

  const newFile = new File([res.data], "processed.png");
  setImage(newFile);

  getHistogram();
};
return (
  <div className="container">

    <Sidebar
      processImage={processImage}
      resetImage={resetImage}
      downloadImage={downloadImage}
    />

    <div className="workspace">

      

      <h2>Upload Image</h2>

      <input type="file" onChange={handleImageChange} />

      <br/><br/>

      <div style={{marginTop:"15px"}}>

  <b>Processing Mode:</b>

  <button
    onClick={() => setMode("original")}
    style={{
      marginLeft:"10px",
      background: mode==="original" ? "#2563eb" : "#1e3a8a"
    }}
  >
    Apply on Original
  </button>

  <button
    onClick={() => setMode("current")}
    style={{
      marginLeft:"10px",
      background: mode==="current" ? "#2563eb" : "#1e3a8a"
    }}
  >
    Apply on Current
  </button>

</div>

<br/>

      {preview && (
        <img
          src={preview}
          alt="preview"
          width="500"
        />
      )}

      <br/><br/>

      {histogram && <Histogram data={histogram} />}

    </div>

  </div>
);
}

export default ImageUpload;