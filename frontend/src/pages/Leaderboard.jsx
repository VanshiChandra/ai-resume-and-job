import React, { useEffect, useState } from "react";
import axios from "axios";

function Leaderboard() {
  const [leaders, setLeaders] = useState([]);

  useEffect(() => {
    axios
      .get(`${import.meta.env.VITE_API_BASE_URL}/leaderboard/global`) // ✅ fixed endpoint
      .then((res) => setLeaders(res.data))
      .catch(() => alert("Error loading leaderboard"));
  }, []);

  return (
    <div className="card" style={{ maxWidth: "600px", margin: "2rem auto", padding: "1rem" }}>
      <h2 style={{ fontSize: "1.75rem", marginBottom: "1rem", textAlign: "center" }}>
        Leaderboard
      </h2>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#f3f4f6" }}>
            <th style={{ textAlign: "left", padding: "0.5rem" }}>Name</th>
            <th style={{ textAlign: "left", padding: "0.5rem" }}>Points</th>
            <th style={{ textAlign: "left", padding: "0.5rem" }}>Badges</th>
          </tr>
        </thead>
        <tbody>
          {leaders.length > 0 ? (
            leaders.map((user, idx) => (
              <tr key={idx}>
                <td style={{ padding: "0.5rem", borderBottom: "1px solid #ddd" }}>
                  {user.name || "Unknown"} {/* ✅ flattened from FastAPI */}
                </td>
                <td style={{ padding: "0.5rem", borderBottom: "1px solid #ddd" }}>
                  {user.score}
                </td>
                <td style={{ padding: "0.5rem", borderBottom: "1px solid #ddd" }}>
                  {user.badges?.join(", ") || "—"}
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={3} style={{ textAlign: "center", padding: "1rem" }}>
                No leaderboard data found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Leaderboard;
