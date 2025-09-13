import React from "react";
import { Link } from "react-router-dom";

function Landing() {
  return (
    <div className="text-center" style={{ padding: "4rem" }}>
      <h1 style={{ fontSize: "2.5rem", fontWeight: "bold" }}>
        AI Powered Resume & Job Matcher
      </h1>
      <p style={{ margin: "1rem 0" }}>
        Upload your resume, get job matches, role suggestions, and climb the leaderboard!
      </p>
      <Link to="/register" className="btn">Get Started</Link>
    </div>
  );
}

export default Landing;
