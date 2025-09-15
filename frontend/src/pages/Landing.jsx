import React from "react";
import { Link } from "react-router-dom";

function Landing() {
  return (
    <div style={{ padding: "4rem", textAlign: "center" }}>
      <h1 style={{ fontSize: "2.5rem", fontWeight: "bold", marginBottom: "1rem" }}>
        AI Powered Resume & Job Matcher
      </h1>
      <p style={{ marginBottom: "1.5rem" }}>
        Upload your resume, get job matches, role suggestions, and climb the leaderboard!
      </p>
      <Link to="/register" className="btn">
        Get Started
      </Link>
    </div>
  );
}

export default Landing;
