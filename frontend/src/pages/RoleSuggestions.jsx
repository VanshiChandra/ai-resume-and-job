import React, { useState } from "react";
import axios from "axios";

function RoleSuggestions() {
  const [skills, setSkills] = useState("");
  const [roles, setRoles] = useState([]);

  const handleSuggest = async () => {
    try {
      const res = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/match/suggest`, { skills });
      setRoles(res.data.roles || []);
    } catch (err) {
      alert("Error fetching role suggestions.");
    }
  };

  return (
    <div className="card" style={{ maxWidth: "600px", margin: "2rem auto" }}>
      <h2>Role Suggestions</h2>
      <textarea
        className="input"
        placeholder="Enter your skills..."
        value={skills}
        onChange={(e) => setSkills(e.target.value)}
      />
      <button className="btn" onClick={handleSuggest}>Get Suggestions</button>
      {roles.length > 0 && (
        <ul style={{ marginTop: "1rem", textAlign: "left" }}>
          {roles.map((role, idx) => <li key={idx}>{role}</li>)}
        </ul>
      )}
    </div>
  );
}

export default RoleSuggestions;
