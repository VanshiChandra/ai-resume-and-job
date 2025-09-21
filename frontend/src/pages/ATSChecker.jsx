import React, { useState } from "react";
import axios from "axios";

function ATSChecker() {
  const [file, setFile] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCheck = async () => {
    if (!file || !jobDesc) return alert("Please upload a resume and job description");
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_desc", jobDesc);

    try {
      const res = await axios.post(
        `${import.meta.env.VITE_API_URL}/ats/check`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      setResult(res.data.ats_result);
    } catch (err) {
      console.error("ATS check failed", err);
      alert("Error performing ATS check");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ats-checker">
      <h2>ATS Resume Checker</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <textarea
        placeholder="Paste Job Description here..."
        value={jobDesc}
        onChange={(e) => setJobDesc(e.target.value)}
      />
      <button onClick={handleCheck} disabled={loading}>
        {loading ? "Checking..." : "Run ATS Check"}
      </button>

      {result && (
        <div className="ats-results">
          <h3>Match Score: {result.score}%</h3>
          <p><strong>Matched Skills:</strong> {result.matched_skills.join(", ")}</p>
          <p><strong>Missing Skills:</strong> {result.missing_skills.join(", ")}</p>
        </div>
      )}
    </div>
  );
}

export default ATSChecker;
