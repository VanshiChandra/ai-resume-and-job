import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";

function Navbar() {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);

  const API_BASE = import.meta.env.VITE_API_BASE_URL;

  // -------------------------------
  // Check login status
  // -------------------------------
  const checkLoginStatus = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      setIsLoggedIn(false);
      setIsAdmin(false);
      return;
    }

    try {
      const headers = { Authorization: `Bearer ${token}` };
      const res = await axios.get(`${API_BASE}/auth/me`, { headers });

      if (res.data) {
        setIsLoggedIn(true);
        setIsAdmin(res.data.role === "admin");
      } else {
        setIsLoggedIn(false);
        setIsAdmin(false);
      }
    } catch (err) {
      console.error("Token validation failed:", err);
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      setIsLoggedIn(false);
      setIsAdmin(false);
    }
  };

  // -------------------------------
  // Run on mount & listen for storage changes
  // -------------------------------
  useEffect(() => {
    checkLoginStatus();

    const handleStorageChange = () => checkLoginStatus();
    window.addEventListener("storage", handleStorageChange);

    return () => window.removeEventListener("storage", handleStorageChange);
  }, []);

  // -------------------------------
  // Logout handler
  // -------------------------------
  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    setIsLoggedIn(false);
    setIsAdmin(false);
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">ResumeMatcher</Link>

        <div className="navbar-links">
          <Link to="/home" className="navbar-link">Home</Link>
          <Link to="/leaderboard" className="navbar-link">Leaderboard</Link>
          <Link to="/job-list" className="navbar-link">Jobs</Link>

          {isLoggedIn ? (
            <>
              <Link to="/dashboard" className="navbar-link">Dashboard</Link>
              <Link to="/resume-upload" className="navbar-link">Upload Resume</Link>
              <Link to="/role-suggestions" className="navbar-link">Role Suggestions</Link>
              {isAdmin && <Link to="/admin" className="navbar-link">Admin</Link>}
              <button onClick={handleLogout} className="btn navbar-logout">Logout</button>
            </>
          ) : (
            <Link to="/login" className="btn navbar-login">Login</Link>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
