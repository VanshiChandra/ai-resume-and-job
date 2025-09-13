import React from "react";
import { Link } from "react-router-dom";

function NotFound() {
  return (
    <div className="text-center py-20">
      <h1 className="text-4xl font-bold mb-4">404 - Page Not Found</h1>
      <Link to="/" className="text-blue-600">Go back Home</Link>
    </div>
  );
}

export default NotFound;
