import React, { useState } from "react";
import axios from "axios";

function ResumeUpload() {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    if (!file) return alert("Please select a file");
    const formData = new FormData();
    formData.append("resume", file);

    try {
      await axios.post(`${import.meta.env.VITE_API_BASE_URL}/resume/upload`, formData);
      alert("Resume uploaded successfully!");
    } catch (err) {
      alert("Upload failed.");
    }
  };

  return (
    <div className="card" style={{ maxWidth: "500px", margin: "2rem auto" }}>
      <h2>Upload Resume</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button className="btn" onClick={handleUpload}>Upload</button>
    </div>
  );
}

export default ResumeUpload;
