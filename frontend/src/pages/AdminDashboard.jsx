import { Users, FileText, Briefcase } from "lucide-react";

function AdminDashboard() {
  const stats = {
    users: 120,
    resumes: 80,
    jobs: 35,
  };

  const cards = [
    {
      title: "Total Users",
      value: stats.users,
      icon: <Users className="w-8 h-8 text-indigo-600" />,
      color: "from-indigo-50 to-indigo-100",
    },
    {
      title: "Resumes Uploaded",
      value: stats.resumes,
      icon: <FileText className="w-8 h-8 text-green-600" />,
      color: "from-green-50 to-green-100",
    },
    {
      title: "Jobs Posted",
      value: stats.jobs,
      icon: <Briefcase className="w-8 h-8 text-blue-600" />,
      color: "from-blue-50 to-blue-100",
    },
  ];

  return (
    <div className="p-10">
      <h2 className="text-3xl font-bold text-gray-800 mb-8">
        Admin Dashboard
      </h2>
      <div className="grid md:grid-cols-3 gap-6">
        {cards.map((card, idx) => (
          <div
            key={idx}
            className={`bg-gradient-to-br ${card.color} p-6 rounded-xl shadow hover:shadow-lg transition transform hover:-translate-y-1`}
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-lg text-gray-700">
                  {card.title}
                </h3>
                <p className="text-4xl font-bold text-gray-900 mt-2">
                  {card.value}
                </p>
              </div>
              {card.icon}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default AdminDashboard;
