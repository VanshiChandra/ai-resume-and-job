import React from "react";
import { Navigate } from "react-router-dom";

function ProtectedRoute({ children, adminOnly = false }) {
  const token = localStorage.getItem("token");
  const isAdmin = localStorage.getItem("isAdmin") === "true";

  // Not logged in → redirect to login
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // Admin-only route check
  if (adminOnly && !isAdmin) {
    return <Navigate to="/home" replace />;
  }

  // Authorized → render children
  return children;
}

export default ProtectedRoute;
