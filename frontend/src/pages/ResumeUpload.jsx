import React, { useState, useEffect } from "react";
import axios from "axios";
import AiSuggestions from "./AiSuggestions";

function ResumeUpload({ userId }) {
  const [file, setFile] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [uploading, setUploading] = useState(false);
  const [resumes, setResumes] = useState([]);
  const [refreshAI, setRefreshAI] = useState(false);

  const API_BASE = import.meta.env.VITE_API_BASE_URL;
  const token = localStorage.getItem("token");

  // Fetch resumes on mount or refresh
  useEffect(() => {
    if (!userId || !token) return;

    const fetchResumes = async () => {
      try {
        const headers = { Authorization: `Bearer ${token}` };
        const res = await axios.get(`${API_BASE}/resumes?user_id=${userId}`, { headers });
        setResumes(res.data || []);
      } catch (err) {
        console.error("Error fetching resumes:", err);
      }
    };

    fetchResumes();
  }, [userId, refreshAI, token]);

  // Upload resume
  const handleUpload = async () => {
    if (!file) return alert("Please select a resume to upload.");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_id", userId);
    formData.append("job_desc", jobDesc);

    try {
      setUploading(true);
      const headers = { 
        "Content-Type": "multipart/form-data",
        Authorization: `Bearer ${token}`
      };
      await axios.post(`${API_BASE}/resume/upload`, formData, { headers });
      alert("Resume uploaded successfully!");
      setFile(null);
      setJobDesc("");
      setRefreshAI((prev) => !prev); // Refresh resumes and AI
    } catch (err) {
      console.error("Upload error:", err);
      alert("Failed to upload resume.");
    } finally {
      setUploading(false);
    }
  };

  // Delete resume
  const handleDelete = async (id) => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      await axios.delete(`${API_BASE}/resumes/${id}`, { headers });
      setResumes(resumes.filter((r) => r.id !== id));
      setRefreshAI((prev) => !prev); // Refresh AI suggestions
    } catch (err) {
      console.error("Delete error:", err);
      alert("Failed to delete resume.");
    }
  };

  return (
    <div className="card" style={{ maxWidth: "600px", margin: "2rem auto", padding: "1rem" }}>
      <h2>Upload Resume</h2>

      <input
        type="file"
        accept=".pdf,.docx"
        onChange={(e) => setFile(e.target.files[0])}
        style={{ marginBottom: "1rem" }}
      />
      <textarea
        placeholder="Optional: Add job description"
        value={jobDesc}
        onChange={(e) => setJobDesc(e.target.value)}
        style={{ width: "100%", marginBottom: "1rem", padding: "0.5rem" }}
      />
      <button onClick={handleUpload} disabled={uploading} className="btn" style={{ marginBottom: "1rem" }}>
        {uploading ? "Uploading..." : "Upload"}
      </button>

      {/* List uploaded resumes */}
      {resumes.length > 0 ? (
        <ul className="section-list" style={{ marginBottom: "1.5rem" }}>
          {resumes.map((resume) => (
            <li key={resume.id} style={{ marginBottom: "0.5rem" }}>
              <a href={resume.file_url} target="_blank" rel="noopener noreferrer">
                {resume.file_name || "Resume"}
              </a>
              <button
                onClick={() => handleDelete(resume.id)}
                className="btn btn-danger"
                style={{ marginLeft: "1rem" }}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p>No resumes uploaded yet.</p>
      )}

      {/* AI Suggestions */}
      <AiSuggestions key={refreshAI} userId={userId} refreshKey={refreshAI} />
    </div>
  );
}

export default ResumeUpload;
