import React from "react";
import { Link } from "react-router-dom";

function NotFound() {
  return (
    <div className="text-center" style={{ padding: "4rem" }}>
      <h1 style={{ fontSize: "3rem", fontWeight: "bold" }}>404</h1>
      <p style={{ marginBottom: "1rem" }}>Page not found.</p>
      <Link to="/" className="btn">
        Go Home
      </Link>
    </div>
  );
}

export default NotFound;
