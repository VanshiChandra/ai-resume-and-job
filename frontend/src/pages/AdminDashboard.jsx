function AdminDashboard() {
  const stats = {
    users: 120,
    resumes: 80,
    jobs: 35,
  };

  return (
    <div className="admin-container">
      <h2 className="admin-title">Admin Dashboard</h2>

      <div className="admin-grid">
        {/* Users */}
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <h3 className="stat-label">Total Users</h3>
          <p className="stat-value">{stats.users}</p>
        </div>

        {/* Resumes */}
        <div className="stat-card">
          <div className="stat-icon">📄</div>
          <h3 className="stat-label">Resumes Uploaded</h3>
          <p className="stat-value green">{stats.resumes}</p>
        </div>

        {/* Jobs */}
        <div className="stat-card">
          <div className="stat-icon">💼</div>
          <h3 className="stat-label">Jobs Posted</h3>
          <p className="stat-value blue">{stats.jobs}</p>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;
