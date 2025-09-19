import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import Badges from "../components/Badges";
import AiSuggestions from "../pages/AiSuggestions";

function Dashboard({ user }) {
  const [skills, setSkills] = useState("");
  const [recommendations, setRecommendations] = useState(null);
  const [aiRoles, setAiRoles] = useState([]);

  // Fetch AI suggestions as fallback on mount
  useEffect(() => {
    if (!user?.id) return;

    const fetchAiRoles = async () => {
      try {
        const res = await axios.get(
          `${import.meta.env.VITE_API_BASE_URL}/ai-suggestions?user_id=${user.id}`
        );
        if (res.data && res.data.length > 0) {
          setAiRoles(res.data[0].suggested_roles || []);
        }
      } catch (err) {
        console.error("Failed to fetch AI suggestions:", err);
      }
    };

    fetchAiRoles();
  }, [user?.id]);

  const handleRecommend = async () => {
    if (!skills.trim()) return;

    try {
      const res = await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}/recommend`,
        { skills }
      );
      setRecommendations(res.data);
    } catch (err) {
      console.warn("/recommend API failed, falling back to AI suggestions:", err);

      // fallback: show AI suggestions if available
      if (aiRoles.length > 0) {
        setRecommendations({
          careers: aiRoles,
          courses: [],
          badges: []
        });
      } else {
        setRecommendations({
          careers: ["Software Engineer", "Data Engineer", "DevOps Engineer"],
          courses: [],
          badges: []
        });
      }
    }
  };

  return (
    <div className="dashboard-container" style={{ padding: "2rem" }}>
      <h2 className="dashboard-title">Welcome, {user?.name || "User"}</h2>

      <div style={{ marginBottom: "1.5rem" }}>
        <Link to="/home" style={{ textDecoration: "none" }}>
          <button style={{ padding: "0.5rem 1rem" }}>Back to Home</button>
        </Link>
      </div>

      <textarea
        placeholder="Enter your skills..."
        value={skills}
        onChange={(e) => setSkills(e.target.value)}
        style={{ width: "100%", height: "100px", marginBottom: "1rem" }}
      />
      <button onClick={handleRecommend} className="btn">
        Get Recommendations
      </button>

      {/* Resume Upload */}
      <div style={{ marginTop: "1.5rem" }}>
        <Link to="/resume-upload" style={{ textDecoration: "none" }}>
          <button className="btn">Upload Resume</button>
        </Link>
      </div>

      {/* Recommendations */}
      {recommendations && (
        <div style={{ marginTop: "2rem" }}>
          <h3 className="section-title">Career Recommendations</h3>
          <ul className="section-list">
            {recommendations.careers?.map((career, idx) => (
              <li key={idx}>{career}</li>
            ))}
          </ul>

          <h3 className="section-title">Suggested Courses</h3>
          <ul className="section-list">
            {recommendations.courses?.map((course, idx) => (
              <li key={idx}>{course}</li>
            ))}
          </ul>

          <h3 className="section-title">Badges Earned</h3>
          <Badges badges={recommendations.badges} />
        </div>
      )}

      {/* AI-based Role Suggestions */}
      {user?.id && (
        <div style={{ marginTop: "2rem" }}>
          <h3 className="section-title">AI Role Suggestions</h3>
          <AiSuggestions userId={user.id} />
        </div>
      )}
    </div>
  );
}

export default Dashboard;
