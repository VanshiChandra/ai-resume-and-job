import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="text-center py-20">
      <h1 className="text-5xl font-bold mb-6">Welcome to AI Powered Resume Scanner And Job Matcher</h1>
      <p className="mb-6 text-lg">Get AI-powered resume scanner and job recommendations to tailor your skills.</p>
      <Link to="/register" className="bg-blue-600 text-white px-6 py-3 rounded-lg">Get Started</Link>
    </div>
  );
}

export default Home;
