import React, { useState } from "react";

function ForgotPassword() {
  const [email, setEmail] = useState("");

  const handleSubmit = () => {
    alert(`Password reset link sent to ${email}`);
  };

  return (
    <div className="card" style={{ maxWidth: "400px", margin: "2rem auto" }}>
      <h2>Forgot Password</h2>
      <input
        type="email"
        placeholder="Enter your email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="input"
      />
      <button className="btn" onClick={handleSubmit}>Send Reset Link</button>
    </div>
  );
}

export default ForgotPassword;
