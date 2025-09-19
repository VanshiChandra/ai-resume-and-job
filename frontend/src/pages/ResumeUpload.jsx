import React, { useState, useEffect } from "react";
import axios from "axios";
import AiSuggestions from "./AiSuggestions";

function ResumeUpload({ userId }) {
  const [file, setFile] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [uploading, setUploading] = useState(false);
  const [resumes, setResumes] = useState([]);
  const [refreshAI, setRefreshAI] = useState(false); // 🔄 trigger AI refresh

  // Fetch resumes on mount or after upload/delete
  useEffect(() => {
    const fetchResumes = async () => {
      try {
        const res = await axios.get(
          `${import.meta.env.VITE_API_BASE_URL}/resumes?user_id=${userId}`
        );
        setResumes(res.data);
      } catch (err) {
        console.error("Error fetching resumes:", err);
      }
    };
    fetchResumes();
  }, [userId, refreshAI]);

  // Upload handler
  const handleUpload = async () => {
    if (!file) return alert("Please select a resume file to upload.");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_id", userId);
    formData.append("job_desc", jobDesc);

    try {
      setUploading(true);
      await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}/resume/upload`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      alert("Resume uploaded successfully!");
      setFile(null);
      setJobDesc("");

      // Refresh resume list
      setRefreshAI((prev) => !prev);
    } catch (err) {
      console.error(err);
      alert("Failed to upload resume.");
    } finally {
      setUploading(false);
    }
  };

  // Delete handler
  const handleDelete = async (id) => {
    try {
      await axios.delete(`${import.meta.env.VITE_API_BASE_URL}/resumes/${id}`);
      setResumes(resumes.filter((r) => r.id !== id));
      setRefreshAI((prev) => !prev); // refresh AI suggestions
    } catch {
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
      <button
        onClick={handleUpload}
        disabled={uploading}
        className="btn"
        style={{ marginBottom: "1rem" }}
      >
        {uploading ? "Uploading..." : "Upload"}
      </button>

      {/* List of uploaded resumes with delete option */}
      <ul className="section-list" style={{ marginBottom: "1.5rem" }}>
        {resumes.length > 0 ? (
          resumes.map((resume) => (
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
          ))
        ) : (
          <p>No resumes uploaded yet.</p>
        )}
      </ul>

      {/* AI Suggestions based on latest resume */}
      <AiSuggestions key={refreshAI} userId={userId} />
    </div>
  );
}

export default ResumeUpload;
