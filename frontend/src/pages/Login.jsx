import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      setError("");
      const res = await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}/auth/login`,
        { email, password },
        { headers: { "Content-Type": "application/json" } }
      );

      // Extract values safely
      const session = res.data.session;
      const user = res.data.user;

      if (!session || !user) {
        throw new Error("Invalid login response");
      }

      // Save access token + role
      localStorage.setItem("token", session.access_token);
      localStorage.setItem("isAdmin", user.role === "admin");

      navigate("/home");
    } catch (err) {
      console.error("Login failed:", err.response?.data || err.message);
      setError(err.response?.data?.detail || "Login failed. Check credentials.");
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="card w-full max-w-sm p-6">
        <h2 className="text-2xl font-bold text-center mb-4">Login</h2>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="input w-full mb-3"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="input w-full mb-3"
        />

        <button className="btn w-full" onClick={handleLogin}>
          Login
        </button>

        {error && <p className="text-red-600 mt-3 text-center">{error}</p>}
      </div>
    </div>
  );
}

export default Login;
