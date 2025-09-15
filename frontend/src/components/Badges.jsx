import React from "react";

function Badges({ badges }) {
  if (!badges || badges.length === 0) return <p>No badges earned yet.</p>;

  return (
    <div className="badges-container">
      {badges.map((badge, idx) => (
        <div key={idx} className="badge-card">
          {badge}
        </div>
      ))}
    </div>
  );
}

export default Badges;
