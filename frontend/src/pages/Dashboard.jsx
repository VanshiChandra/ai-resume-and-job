import React, { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import Badges from "../components/Badges";

function Dashboard() {
  const [skills, setSkills] = useState("");
  const [recommendations, setRecommendations] = useState(null);

  const handleRecommend = async () => {
    try {
      const res = await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}/recommend`,
        { skills }
      );
      setRecommendations(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="dashboard-container" style={{ padding: "2rem" }}>
      <h2 className="dashboard-title">Dashboard</h2>

      {/* Back to Home */}
      <div style={{ marginBottom: "1.5rem" }}>
        <Link to="/home" style={{ textDecoration: "none" }}>
          <button style={{ padding: "0.5rem 1rem" }}>Back to Home</button>
        </Link>
      </div>

      <textarea
        className="dashboard-textarea"
        placeholder="Enter your skills..."
        value={skills}
        onChange={(e) => setSkills(e.target.value)}
        style={{ width: "100%", height: "100px", marginBottom: "1rem" }}
      />

      <button onClick={handleRecommend} className="btn">
        Get Recommendations
      </button>

      {/* Resume Upload button */}
      <div style={{ marginTop: "1.5rem" }}>
        <Link to="/resume-upload" style={{ textDecoration: "none" }}>
          <button className="btn">Upload Resume</button>
        </Link>
      </div>

      {recommendations && (
        <div style={{ marginTop: "2rem" }}>
          <h3 className="section-title">Career Recommendations</h3>
          <ul className="section-list">
            {recommendations.careers.map((career, idx) => (
              <li key={idx}>{career}</li>
            ))}
          </ul>

          <h3 className="section-title">Suggested Courses</h3>
          <ul className="section-list">
            {recommendations.courses.map((course, idx) => (
              <li key={idx}>{course}</li>
            ))}
          </ul>

          <h3 className="section-title">Badges Earned</h3>
          <Badges badges={recommendations.badges} />
        </div>
      )}
    </div>
  );
}

export default Dashboard;
