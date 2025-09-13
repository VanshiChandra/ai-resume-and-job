import { Link } from "react-router-dom";

function NotFound() {
  return (
    <div className="flex flex-col justify-center items-center h-screen text-center">
      <h1 className="text-5xl font-bold text-indigo-600">404</h1>
      <p className="text-gray-600 mt-4">Oops! Page not found.</p>
      <Link
        to="/"
        className="mt-6 bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700"
      >
        Go Home
      </Link>
    </div>
  );
}

export default NotFound;
