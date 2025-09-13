import React, { useState } from "react";
import { supabase } from "../services/supabaseClient";
import { useNavigate } from "react-router-dom";

function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    const { error } = await supabase.auth.signUp({ email, password });
    if (error) setError(error.message);
    else navigate("/dashboard");
  };

  return (
    <div className="max-w-md mx-auto bg-white p-6 shadow rounded mt-10">
      <h2 className="text-2xl font-bold mb-4">Register</h2>
      {error && <p className="text-red-500">{error}</p>}
      <form onSubmit={handleRegister} className="space-y-4">
        <input type="email" placeholder="Email" className="w-full border p-2 rounded"
          value={email} onChange={(e) => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" className="w-full border p-2 rounded"
          value={password} onChange={(e) => setPassword(e.target.value)} />
        <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded w-full">Register</button>
      </form>
    </div>
  );
}

export default Register;
