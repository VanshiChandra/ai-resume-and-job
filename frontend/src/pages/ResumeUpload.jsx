import React, { useState, useEffect } from "react";
import axios from "axios";

function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [resumes, setResumes] = useState([]);

  // Fetch resumes on mount
  useEffect(() => {
    const fetchResumes = async () => {
      try {
        const res = await axios.get(
          `${import.meta.env.VITE_API_BASE_URL}/resumes`
        );
        setResumes(res.data);
      } catch (err) {
        console.error("Error fetching resumes:", err);
      }
    };
    fetchResumes();
  }, []);

  // Upload handler
  const handleUpload = async () => {
    if (!file) return alert("Please select a file");

    const formData = new FormData();
    formData.append("resume", file);

    try {
      await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}/resumes/upload`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      alert("Resume uploaded successfully!");
      setFile(null);

      // Refresh list
      const res = await axios.get(
        `${import.meta.env.VITE_API_BASE_URL}/resumes`
      );
      setResumes(res.data);
    } catch {
      alert("Upload failed.");
    }
  };

  // Delete handler
  const handleDelete = async (id) => {
    try {
      await axios.delete(
        `${import.meta.env.VITE_API_BASE_URL}/resumes/${id}`
      );
      setResumes(resumes.filter((r) => r.id !== id));
    } catch {
      alert("Failed to delete resume.");
    }
  };

  return (
    <div className="card" style={{ maxWidth: "500px", margin: "2rem auto" }}>
      <h2 style={{ marginBottom: "1rem" }}>Upload Resume</h2>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        style={{ marginBottom: "1rem" }}
      />
      <button className="btn" onClick={handleUpload}>
        Upload
      </button>

      <ul className="section-list" style={{ marginTop: "1rem" }}>
        {resumes.length > 0 ? (
          resumes.map((resume) => (
            <li key={resume.id} style={{ marginBottom: "0.5rem" }}>
              <a
                href={resume.file_url}
                target="_blank"
                rel="noopener noreferrer"
              >
                {resume.file_name}
              </a>
              <button
                onClick={() => handleDelete(resume.id)}
                className="btn btn-danger"
                style={{ marginLeft: "1rem" }}
              >
                Delete
              </button>
            </li>
          ))
        ) : (
          <p>No resumes uploaded yet.</p>
        )}
      </ul>
    </div>
  );
}

export default ResumeUpload;
