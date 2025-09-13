import React from "react";

function Badges({ badges }) {
  return (
    <div className="flex flex-wrap gap-2">
      {badges.map((badge, idx) => (
        <span key={idx} className="bg-green-200 text-green-800 px-3 py-1 rounded-full text-sm">
          {badge}
        </span>
      ))}
    </div>
  );
}

export default Badges;
