import React, { useState } from "react";
import axios from "axios";
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
    <div className="dashboard-container">
      <h2 className="dashboard-title">Dashboard</h2>

      <textarea
        className="dashboard-textarea"
        placeholder="Enter your skills..."
        value={skills}
        onChange={(e) => setSkills(e.target.value)}
      />

      <button onClick={handleRecommend} className="btn">
        Get Recommendations
      </button>

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
