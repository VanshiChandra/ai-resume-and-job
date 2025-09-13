import { useEffect, useState } from "react";
import axios from "axios";

const JobList = () => {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    axios.get("/api/recommendations/jobs")
      .then(res => setJobs(res.data || []))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Job Recommendations</h2>
      <div className="space-y-4">
        {jobs.map((job, i) => (
          <div key={i} className="border p-4 rounded shadow">
            <h3 className="font-bold">{job.title}</h3>
            <p>{job.company}</p>
            <a href={job.link} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">
              Apply Now
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default JobList;
