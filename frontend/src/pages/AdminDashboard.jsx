function AdminDashboard() {
  const stats = {
    users: 120,
    resumes: 80,
    jobs: 35,
  };

  return (
    <div className="p-10">
      <h2 className="text-2xl font-bold text-indigo-600 mb-6 text-center">
        Admin Dashboard
      </h2>

      <div className="grid md:grid-cols-3 gap-6">
        {/* Users */}
        <div className="bg-white p-6 rounded-lg shadow hover:shadow-md transition text-center">
          <div className="text-4xl mb-2">👥</div>
          <h3 className="font-bold text-lg">Total Users</h3>
          <p className="text-3xl text-indigo-600">{stats.users}</p>
        </div>

        {/* Resumes */}
        <div className="bg-white p-6 rounded-lg shadow hover:shadow-md transition text-center">
          <div className="text-4xl mb-2">📄</div>
          <h3 className="font-bold text-lg">Resumes Uploaded</h3>
          <p className="text-3xl text-green-600">{stats.resumes}</p>
        </div>

        {/* Jobs */}
        <div className="bg-white p-6 rounded-lg shadow hover:shadow-md transition text-center">
          <div className="text-4xl mb-2">💼</div>
          <h3 className="font-bold text-lg">Jobs Posted</h3>
          <p className="text-3xl text-blue-600">{stats.jobs}</p>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;
