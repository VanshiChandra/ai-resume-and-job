import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="bg-blue-600 text-white p-4 flex justify-between items-center">
      <Link to="/" className="font-bold text-lg">
        RESUME SCANNER
      </Link>
      <div className="space-x-4">
        <Link to="/home">Home</Link>
        <Link to="/leaderboard">Leaderboard</Link>
        <Link to="/resume-upload">Resume</Link>
        <Link to="/role-suggestions">Roles</Link>
        <Link to="/job-list">Jobs</Link>
        <Link to="/login">Login</Link>
      </div>
    </nav>
  );
};

export default Navbar;
