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
    <div style={{ padding: "2rem" }}>
      <h2 style={{ fontSize: "2rem", fontWeight: "bold", marginBottom: "1rem" }}>
        Dashboard
      </h2>

      <textarea
        style={{
          width: "100%",
          border: "1px solid #ccc",
          padding: "0.75rem",
          borderRadius: "6px",
          marginBottom: "1rem",
          minHeight: "100px",
        }}
        placeholder="Enter your skills..."
        value={skills}
        onChange={(e) => setSkills(e.target.value)}
      />

      <button onClick={handleRecommend} className="btn">
        Get Recommendations
      </button>

      {recommendations && (
        <div style={{ marginTop: "2rem" }}>
          <h3 style={{ fontSize: "1.25rem", fontWeight: "bold", marginBottom: "0.5rem" }}>
            Career Recommendations
          </h3>
          <ul style={{ paddingLeft: "1.25rem", listStyle: "disc" }}>
            {recommendations.careers.map((career, idx) => (
              <li key={idx}>{career}</li>
            ))}
          </ul>

          <h3 style={{ fontSize: "1.25rem", fontWeight: "bold", margin: "1.5rem 0 0.5rem" }}>
            Suggested Courses
          </h3>
          <ul style={{ paddingLeft: "1.25rem", listStyle: "disc" }}>
            {recommendations.courses.map((course, idx) => (
              <li key={idx}>{course}</li>
            ))}
          </ul>

          <h3 style={{ fontSize: "1.25rem", fontWeight: "bold", margin: "1.5rem 0 0.5rem" }}>
            Badges Earned
          </h3>
          <Badges badges={recommendations.badges} />
        </div>
      )}
    </div>
  );
}

export default Dashboard;
