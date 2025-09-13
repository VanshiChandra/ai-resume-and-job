import { useState } from "react";
import axios from "axios";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [msg, setMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("/api/auth/forgot-password", { email });
      setMsg("Password reset instructions sent to your email.");
    } catch (err) {
      console.error(err);
      setMsg("Error sending reset email.");
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-md w-80">
        <h2 className="text-2xl font-bold mb-4">Forgot Password</h2>
        <input
          type="email"
          placeholder="Enter your email"
          className="w-full p-2 border rounded mb-4"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded">
          Reset Password
        </button>
        {msg && <p className="mt-4 text-sm text-gray-600">{msg}</p>}
      </form>
    </div>
  );
};

export default ForgotPassword;
