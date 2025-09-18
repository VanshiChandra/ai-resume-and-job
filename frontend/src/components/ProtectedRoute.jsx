import React from "react";
import { Navigate } from "react-router-dom";
import { getCurrentUser } from "../utils/auth"; // centralized auth util

function ProtectedRoute({ children, adminOnly = false }) {
  const user = getCurrentUser(); // returns null if not logged in

  if (!user) {
    // Not logged in
    return <Navigate to="/login" replace />;
  }

  if (adminOnly && user.role !== "admin") {
    // Not authorized for admin route
    return <Navigate to="/home" replace />;
  }

  return children;
}

export default ProtectedRoute;
