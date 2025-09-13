import { Link } from "react-router-dom";

const Landing = () => {
  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-r from-blue-500 to-purple-600 text-white">
      <h1 className="text-4xl font-bold mb-6">AI Powered Resume Scanner And Job Matcher </h1>
      <p className="mb-6 text-lg text-center max-w-xl">
        Discover careers, upload resumes, and get personalized job role recommendations powered by AI.
      </p>
      <div className="flex gap-4">
        <Link to="/login" className="bg-white text-blue-600 px-6 py-2 rounded-lg font-semibold shadow">
          Login
        </Link>
        <Link to="/register" className="bg-purple-700 px-6 py-2 rounded-lg font-semibold shadow">
          Register
        </Link>
      </div>
    </div>
  );
};

export default Landing;
