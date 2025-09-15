import React from "react";
import { Link } from "react-router-dom";

function NotFound() {
  return (
    <div style={{ textAlign: "center", padding: "4rem" }}>
      <h1 style={{ fontSize: "3rem", fontWeight: "bold", color: "#2563eb" }}>
        404
      </h1>
      <p style={{ margin: "1rem 0", color: "#555" }}>Oops! Page not found.</p>
      <Link to="/" className="btn">
        Go Home
      </Link>
    </div>
  );
}

export default NotFound;
