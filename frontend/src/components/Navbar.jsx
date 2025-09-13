import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="bg-indigo-600 text-white px-6 py-4 shadow-md">
      <div className="flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold tracking-wide">
          ResumeMatcher
        </Link>
        <div className="space-x-6">
          <Link to="/home" className="hover:text-gray-200">Home</Link>
          <Link to="/leaderboard" className="hover:text-gray-200">Leaderboard</Link>
          <Link to="/job-list" className="hover:text-gray-200">Jobs</Link>
          <Link to="/login" className="bg-white text-indigo-600 px-3 py-1 rounded-md hover:bg-gray-100">
            Login
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
