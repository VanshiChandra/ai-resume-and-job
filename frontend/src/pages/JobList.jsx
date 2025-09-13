import React, { useEffect, useState } from "react";
import axios from "axios";

function JobList() {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    axios.get(`${import.meta.env.VITE_API_BASE_URL}/job/list`)
      .then(res => setJobs(res.data))
      .catch(() => alert("Error loading jobs"));
  }, []);

  return (
    <div className="card">
      <h2>Job Listings</h2>
      {jobs.length === 0 ? (
        <p>No jobs found</p>
      ) : (
        <ul style={{ textAlign: "left" }}>
          {jobs.map((job, idx) => (
            <li key={idx} style={{ marginBottom: "0.5rem" }}>
              <strong>{job.title}</strong> - {job.company}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default JobList;
