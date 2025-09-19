import React, { useState, useEffect } from "react";
import axios from "axios";

function Dashboard({ user }) {
  const [recommendations, setRecommendations] = useState(null);
  const [aiRoles, setAiRoles] = useState(null);
  const [resumes, setResumes] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [selectedResume, setSelectedResume] = useState("");
  const [selectedJob, setSelectedJob] = useState("");
  const [loading, setLoading] = useState(false);

  // Load resumes and jobs for dropdowns
  useEffect(() => {
    if (!user?.id) return;

    axios
      .get(`${import.meta.env.VITE_API_BASE_URL}/resume/list/${user.id}`)
      .then((res) => setResumes(res.data))
      .catch(() => console.warn("No resumes found"));

    axios
      .get(`${import.meta.env.VITE_API_BASE_URL}/job/list`)
      .then((res) => setJobs(res.data))
      .catch(() => console.warn("No jobs found"));
  }, [user]);

  // ✅ ATS style recommendation
  const handleMatch = async () => {
    if (!selectedResume || !selectedJob) {
      alert("Please select both resume and job");
      return;
    }
    setLoading(true);
    try {
      const res = await axios.get(
        `${import.meta.env.VITE_API_BASE_URL}/recommend/${selectedResume}/${selectedJob}`
      );
      setRecommendations(res.data);
    } catch (err) {
      console.error(err);
      alert("Error matching resume with job");
    } finally {
      setLoading(false);
    }
  };

  // ✅ AI role recommendations
  const handleAiRecommendations = async () => {
    if (!user?.id) {
      alert("Please log in first");
      return;
    }
    setLoading(true);
    try {
      const res = await axios.get(
        `${import.meta.env.VITE_API_BASE_URL}/recommend/${user.id}`
      );
      setAiRoles(res.data);
    } catch (err) {
      console.error(err);
      alert("Error fetching AI recommendations");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "900px", margin: "2rem auto" }}>
      <h1>Welcome, {user?.name || "User"} 👋</h1>

      {/* ============================= */}
      {/* ATS STYLE MATCHING SECTION */}
      {/* ============================= */}
      <div
        style={{
          marginTop: "2rem",
          padding: "1rem",
          border: "1px solid #ddd",
          borderRadius: "8px",
        }}
      >
        <h2>ATS Resume → Job Match</h2>

        {/* Resume Selector */}
        <select
          value={selectedResume}
          onChange={(e) => setSelectedResume(e.target.value)}
          style={{ marginRight: "1rem", padding: "0.5rem" }}
        >
          <option value="">Select Resume</option>
          {resumes.map((r) => (
            <option key={r.id} value={r.id}>
              {r.file_url.split("/").pop()}
            </option>
          ))}
        </select>

        {/* Job Selector */}
        <select
          value={selectedJob}
          onChange={(e) => setSelectedJob(e.target.value)}
          style={{ marginRight: "1rem", padding: "0.5rem" }}
        >
          <option value="">Select Job</option>
          {jobs.map((j) => (
            <option key={j.id} value={j.id}>
              {j.title}
            </option>
          ))}
        </select>

        <button
          onClick={handleMatch}
          disabled={loading}
          style={{
            padding: "0.5rem 1rem",
            background: "#16a34a",
            color: "white",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
          }}
        >
          {loading ? "Matching..." : "Match Resume"}
        </button>

        {/* ATS Results */}
        {recommendations && (
          <div style={{ marginTop: "1rem" }}>
            <h3>Match Score: {recommendations.score}%</h3>
            <h4>Missing Skills:</h4>
            <ul>
              {recommendations.missing_skills?.map((s, idx) => (
                <li key={idx}>{s}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* ============================= */}
      {/* AI ROLE RECOMMENDATION SECTION */}
      {/* ============================= */}
      <div
        style={{
          marginTop: "2rem",
          padding: "1rem",
          border: "1px solid #ddd",
          borderRadius: "8px",
        }}
      >
        <h2>AI Role Recommendations</h2>
        <button
          onClick={handleAiRecommendations}
          disabled={loading}
          style={{
            padding: "0.5rem 1rem",
            background: "#2563eb",
            color: "white",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
          }}
        >
          {loading ? "Loading..." : "Get AI Suggestions"}
        </button>

        {/* AI Results */}
        {aiRoles && (
          <ul style={{ marginTop: "1rem" }}>
            {aiRoles.suggested_roles?.map((role, idx) => (
              <li key={idx}>{role}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
