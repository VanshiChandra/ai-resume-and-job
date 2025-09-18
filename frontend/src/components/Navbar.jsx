import { Link, useNavigate } from "react-router-dom";
import { getCurrentUser, logout } from "../utils/auth"; // your auth utils

function Navbar() {
  const navigate = useNavigate();
  const user = getCurrentUser(); // returns null if not logged in

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          ResumeMatcher
        </Link>

        <div className="navbar-links">
          {!user && (
            <>
              <Link to="/login" className="btn navbar-login">Login</Link>
              <Link to="/register" className="navbar-link">Register</Link>
            </>
          )}

          {user && (
            <>
              <Link to="/home" className="navbar-link">Home</Link>
              <Link to="/dashboard" className="navbar-link">Dashboard</Link>
              <Link to="/leaderboard" className="navbar-link">Leaderboard</Link>
              <Link to="/resume-upload" className="navbar-link">Upload Resume</Link>
              <Link to="/role-suggestions" className="navbar-link">Role Suggestions</Link>
              <Link to="/job-list" className="navbar-link">Jobs</Link>

              {user.role === "admin" && (
                <Link to="/admin" className="navbar-link">Admin</Link>
              )}

              <button onClick={handleLogout} className="btn navbar-logout">
                Logout
              </button>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
