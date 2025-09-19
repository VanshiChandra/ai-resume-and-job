import React, { useEffect, useState } from "react";
import axios from "axios";

function Leaderboard() {
  const [leaders, setLeaders] = useState([]);

  useEffect(() => {
    axios
      .get(`${import.meta.env.VITE_API_BASE_URL}/leaderboard`)
      .then((res) => setLeaders(res.data))
      .catch(() => alert("Error loading leaderboard"));
  }, []);

  return (
    <div className="card" style={{ maxWidth: "600px", margin: "2rem auto" }}>
      <h2 style={{ fontSize: "1.75rem", marginBottom: "1rem", textAlign: "center" }}>
        Leaderboard
      </h2>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#f3f4f6" }}>
            <th style={{ textAlign: "left", padding: "0.5rem" }}>Name</th>
            <th style={{ textAlign: "left", padding: "0.5rem" }}>Points</th>
          </tr>
        </thead>
        <tbody>
          {leaders.map((user, idx) => (
           <tr key={idx}>
           <td style={{ padding: "0.5rem", borderBottom: "1px solid #ddd" }}>
            {user.profiles?.name || "Unknown"}
           </td>
           <td style={{ padding: "0.5rem", borderBottom: "1px solid #ddd" }}>
           {user.score}
           </td>
           <td style={{ padding: "0.5rem", borderBottom: "1px solid #ddd" }}>
           {user.badges?.join(", ") || "—"}
           </td>
          </tr>
           ))}
        </tbody>

      </table>
    </div>
  );
}

export default Leaderboard;
