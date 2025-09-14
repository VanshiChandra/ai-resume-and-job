import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Register() {
  const [name, setName] = useState("");   // add name
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      setError("");
      await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}/auth/register`,
        { name, email, password },  // include name
        { headers: { "Content-Type": "application/json" } }
      );
      navigate("/login");
    } catch (err) {
      setError(
        err.response?.data?.detail || "Registration failed. Try again."
      );
    }
  };

  return (
    <div className="card max-w-sm mx-auto mt-10 p-6">
      <h2 className="text-2xl font-bold mb-4 text-center">Register</h2>
      
      <input
        type="text"
        placeholder="Full Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        className="input w-full mb-3"
      />
      
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
      
      <button className="btn w-full" onClick={handleRegister}>
        Register
      </button>
      
      {error && <p className="text-red-600 mt-3 text-center">{error}</p>}
    </div>
  );
}

export default Register;
