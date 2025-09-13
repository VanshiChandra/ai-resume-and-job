import { useEffect, useState } from "react";
import axios from "axios";

const Leaderboard = () => {
  const [scores, setScores] = useState([]);

  useEffect(() => {
    axios.get("/api/scores/leaderboard")
      .then(res => setScores(res.data || []))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Leaderboard</h2>
      <table className="w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th className="border px-4 py-2">Rank</th>
            <th className="border px-4 py-2">User</th>
            <th className="border px-4 py-2">Score</th>
          </tr>
        </thead>
        <tbody>
          {scores.map((s, i) => (
            <tr key={i}>
              <td className="border px-4 py-2">{i + 1}</td>
              <td className="border px-4 py-2">{s.user_name || s.user_email}</td>
              <td className="border px-4 py-2">{s.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Leaderboard;
