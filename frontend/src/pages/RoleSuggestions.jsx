import { useEffect, useState } from "react";
import axios from "axios";

const RoleSuggestions = () => {
  const [roles, setRoles] = useState([]);

  useEffect(() => {
    axios.get("/api/recommendations/roles")
      .then(res => setRoles(res.data || []))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Recommended Roles</h2>
      <ul className="list-disc pl-5 space-y-2">
        {roles.map((role, i) => (
          <li key={i}>{role}</li>
        ))}
      </ul>
    </div>
  );
};

export default RoleSuggestions;
