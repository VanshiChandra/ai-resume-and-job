import React, { useEffect, useState } from "react";
import axios from "axios";

function JobList() {
  const [jobs, setJobs] = useState([]);
  const API_BASE = import.meta.env.VITE_API_BASE_URL;
  const token = localStorage.getItem("token"); // optional if auth required

  useEffect(() => {
    axios
      .get(`${API_BASE}/job/list`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      })
      .then((res) => setJobs(res.data))
      .catch(() => alert("Error loading jobs"));
  }, [API_BASE, token]);

  return (
    <div className="card" style={{ maxWidth: "600px", margin: "2rem auto", padding: "1rem" }}>
      <h2 style={{ marginBottom: "1rem", textAlign: "center" }}>Job Listings</h2>

      {jobs.length === 0 ? (
        <p style={{ textAlign: "center" }}>No jobs found</p>
      ) : (
        <ul style={{ textAlign: "left", paddingLeft: "1.25rem" }}>
          {jobs.map((job) => (
            <li key={job.id} style={{ marginBottom: "0.5rem" }}>
              <strong>{job.title}</strong> – {job.company || "N/A"}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default JobList;
