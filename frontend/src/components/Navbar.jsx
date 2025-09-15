import { Link } from "react-router-dom";

function Navbar() {
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
          <Link to="/login" className="btn navbar-login">Login</Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
