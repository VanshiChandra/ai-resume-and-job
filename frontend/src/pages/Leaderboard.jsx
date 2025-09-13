import React, { useEffect, useState } from "react";
import axios from "axios";

function Leaderboard() {
  const [leaders, setLeaders] = useState([]);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/leaderboard`);
        setLeaders(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchLeaderboard();
  }, []);

  return (
    <div className="card">
      <h2 className="text-center" style={{ fontSize: "1.75rem", marginBottom: "1rem" }}>
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
                {user.name}
              </td>
              <td style={{ padding: "0.5rem", borderBottom: "1px solid #ddd" }}>
                {user.points}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Leaderboard;
