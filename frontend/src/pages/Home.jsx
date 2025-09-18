import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div style={{ padding: "2rem", textAlign: "center" }}>
      <h2 style={{ marginBottom: "1rem" }}>Welcome to Your Dashboard</h2>
      <p>Upload resumes, get job matches, view leaderboard, and more.</p>

      {/* Navigate to Dashboard page */}
      <div style={{ marginTop: "2rem" }}>
        <Link to="/dashboard" style={{ textDecoration: "none" }}>
          <button style={{ padding: "0.5rem 1rem", fontSize: "1rem" }}>
            Go to Dashboard
          </button>
        </Link>
      </div>
    </div>
  );
}

export default Home;
