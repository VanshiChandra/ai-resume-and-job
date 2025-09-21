import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const API_BASE = import.meta.env.VITE_API_BASE_URL;

  const handleLogin = async () => {
    try {
      const res = await axios.post(`${API_BASE}/auth/login`, { email, password });

      // Save token and role
      localStorage.setItem("token", res.data.token);
      localStorage.setItem("role", res.data.role);

      // Redirect to dashboard
      navigate("/dashboard");
    } catch (err) {
      console.error("Login failed:", err);
      alert("Login failed. Check credentials.");
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "3rem auto" }}>
      <div className="card">
        <h2 className="text-center" style={{ marginBottom: "1rem" }}>
          Login
        </h2>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="input"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="input"
        />

        <button className="btn" style={{ width: "100%" }} onClick={handleLogin}>
          Login
        </button>
      </div>
    </div>
  );
}

export default Login;
