import React from "react";
import { Link } from "react-router-dom";

function NotFound() {
  return (
    <div className="notfound-container text-center">
      <h1 className="notfound-title">404</h1>
      <p className="notfound-text">Page not found.</p>
      <Link to="/" className="btn">
        Go Home
      </Link>
    </div>
  );
}

export default NotFound;
