import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

function Navbar() {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    const checkLoginStatus = () => {
      const token = localStorage.getItem("token");
      const role = localStorage.getItem("role");
      setIsLoggedIn(!!token);
      setIsAdmin(role === "admin");
    };

    checkLoginStatus();

    // Listen for storage changes (multi-tab sync)
    window.addEventListener("storage", checkLoginStatus);
    return () => window.removeEventListener("storage", checkLoginStatus);
  }, []);

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
        <Link to="/" className="navbar-logo">
          ResumeMatcher
        </Link>

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
