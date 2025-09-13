import React, { useState } from "react";
import axios from "axios";
import Badges from "../components/Badges";

function Dashboard() {
  const [skills, setSkills] = useState("");
  const [recommendations, setRecommendations] = useState(null);

  const handleRecommend = async () => {
    try {
      const res = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/recommend`, { skills });
      setRecommendations(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-3xl font-bold mb-4">Dashboard</h2>
      <textarea
        className="w-full border p-2 rounded mb-4"
        placeholder="Enter your skills..."
        value={skills}
        onChange={(e) => setSkills(e.target.value)}
      />
      <button
        onClick={handleRecommend}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Get Recommendations
      </button>

      {recommendations && (
        <div className="mt-6">
          <h3 className="text-xl font-bold mb-2">Career Recommendations</h3>
          <ul className="list-disc pl-6">
            {recommendations.careers.map((career, idx) => <li key={idx}>{career}</li>)}
          </ul>

          <h3 className="text-xl font-bold mt-4 mb-2">Suggested Courses</h3>
          <ul className="list-disc pl-6">
            {recommendations.courses.map((course, idx) => <li key={idx}>{course}</li>)}
          </ul>

          <h3 className="text-xl font-bold mt-4 mb-2">Badges Earned</h3>
          <Badges badges={recommendations.badges} />
        </div>
      )}
    </div>
  );
}

export default Dashboard;
