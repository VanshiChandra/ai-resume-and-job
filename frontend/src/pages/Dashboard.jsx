import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import Badges from "../components/Badges";
import AiSuggestions from "../pages/AiSuggestions";

function Dashboard({ user: propUser }) {
  const navigate = useNavigate();
  const [user, setUser] = useState(propUser || null);
  const [skills, setSkills] = useState("");
  const [recommendations, setRecommendations] = useState(null);
  const [matches, setMatches] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshAI, setRefreshAI] = useState(false);

  const API_BASE = import.meta.env.VITE_API_BASE_URL;

  // Fetch user from backend if propUser is not provided
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          navigate("/login");
          return;
        }

        const headers = { Authorization: `Bearer ${token}` };

        const userRes = await axios.get(`${API_BASE}/auth/me`, { headers });
        setUser(userRes.data);

      } catch (err) {
        console.error("Failed to fetch user:", err);
        navigate("/login");
      }
    };

    if (!user) fetchUser();
  }, [user, API_BASE, navigate]);

  // Fetch ATS matches and leaderboard
  useEffect(() => {
    if (!user?.id) return;

    const fetchData = async () => {
      try {
        setLoading(true);
        const token = localStorage.getItem("token");
        if (!token) return navigate("/login");

        const headers = { Authorization: `Bearer ${token}` };

        const matchRes = await axios.get(`${API_BASE}/matching/user/${user.id}`, { headers });
        setMatches(matchRes.data || []);

        const lbRes = await axios.get(`${API_BASE}/leaderboard/global`, { headers });
        setLeaderboard(lbRes.data || []);

      } catch (err) {
        console.error("Dashboard data fetch error:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user, API_BASE]);

  // Handle manual skill-based recommendations
  const handleRecommend = async () => {
    if (!skills.trim()) return;
    try {
      const token = localStorage.getItem("token");
      const headers = { Authorization: `Bearer ${token}` };
      const res = await axios.post(`${API_BASE}/recommend`, { skills }, { headers });
      setRecommendations(res.data);
      setRefreshAI((prev) => !prev);
    } catch (err) {
      console.error("Error fetching recommendations:", err);
    }
  };

  if (!user) return <p>Loading user info...</p>;
  if (loading) return <p>Loading dashboard...</p>;

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

      <div style={{ marginTop: "1.5rem" }}>
        <Link to="/resume-upload" style={{ textDecoration: "none" }}>
          <button className="btn">Upload Resume</button>
        </Link>
      </div>

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

      {matches.length > 0 && (
        <div style={{ marginTop: "2rem" }}>
          <h3 className="section-title">ATS Matches</h3>
          <ul className="section-list">
            {matches.map((m, idx) => (
              <li key={idx}>
                <strong>{m.job_title}</strong> – Score: {m.score}%
              </li>
            ))}
          </ul>
        </div>
      )}

      {leaderboard.length > 0 && (
        <div style={{ marginTop: "2rem" }}>
          <h3 className="section-title">Leaderboard</h3>
          <ol>
            {leaderboard.map((lb, idx) => (
              <li key={idx}>
                {idx + 1}. {lb.profiles?.name || "Anonymous"} – {lb.score}
              </li>
            ))}
          </ol>
        </div>
      )}

      {user?.id && (
        <div style={{ marginTop: "2rem" }}>
          <h3 className="section-title">AI Role Suggestions</h3>
          <AiSuggestions userId={user.id} refreshKey={refreshAI} />
        </div>
      )}
    </div>
  );
}

export default Dashboard;
