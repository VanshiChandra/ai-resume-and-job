import React, { useEffect, useState } from "react";
import axios from "axios";

function AiSuggestions({ userId, refreshKey }) {
  const [latest, setLatest] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!userId) return;

    const fetchSuggestions = async () => {
      setLoading(true);
      setError(null);
      try {
        // Latest AI suggestion
        const latestRes = await axios.get(
          `${import.meta.env.VITE_API_BASE_URL}/ai/suggest-for-user/${userId}`
        );
        setLatest(latestRes.data.suggested_roles || []);

        // Past suggestions history
        const historyRes = await axios.get(
          `${import.meta.env.VITE_API_BASE_URL}/ai/suggestions/${userId}`
        );
        setHistory(historyRes.data || []);
      } catch (err) {
        console.error(err);
        setError("Failed to fetch AI suggestions.");
      } finally {
        setLoading(false);
      }
    };

    fetchSuggestions();
  }, [userId, refreshKey]); // auto-refresh when userId or refreshKey changes

  if (loading) return <p style={{ textAlign: "center" }}>Loading suggestions...</p>;
  if (error) return <p style={{ textAlign: "center", color: "red" }}>{error}</p>;

  return (
    <div className="card" style={{ maxWidth: "600px", margin: "2rem auto", padding: "1rem" }}>
      <h2 style={{ fontSize: "1.5rem", marginBottom: "1rem", textAlign: "center" }}>
        AI Job Role Suggestions
      </h2>

      {/* Latest Suggestions */}
      <h3 style={{ fontSize: "1.2rem", marginBottom: "0.5rem" }}>Latest Suggestions</h3>
      {latest.length > 0 ? (
        <ul style={{ marginLeft: "1rem" }}>
          {latest.map((role, idx) => (
            <li key={idx}>{role}</li>
          ))}
        </ul>
      ) : (
        <p>No suggestions yet.</p>
      )}

      {/* Suggestion History */}
      <h3 style={{ fontSize: "1.2rem", margin: "1.5rem 0 0.5rem" }}>Suggestion History</h3>
      {history.length > 0 ? (
        <ul style={{ marginLeft: "1rem" }}>
          {history.map((entry, idx) => (
            <li key={entry.id || idx}>
              <strong>{new Date(entry.created_at).toLocaleString()}:</strong>{" "}
              {Array.isArray(entry.suggested_roles)
                ? entry.suggested_roles.join(", ")
                : JSON.stringify(entry.suggested_roles)}
            </li>
          ))}
        </ul>
      ) : (
        <p>No history found.</p>
      )}
    </div>
  );
}

export default AiSuggestions;
