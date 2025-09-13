import React from "react";

function Badges({ badges }) {
  if (!badges || badges.length === 0) return <p>No badges earned yet.</p>;

  return (
    <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
      {badges.map((badge, idx) => (
        <div
          key={idx}
          className="card"
          style={{
            padding: "0.75rem 1.25rem",
            backgroundColor: "#f0f9ff",
            border: "1px solid #bae6fd",
            fontWeight: "bold",
          }}
        >
          {badge}
        </div>
      ))}
    </div>
  );
}

export default Badges;
