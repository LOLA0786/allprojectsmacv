import { useEffect, useState } from "react";
import axios from "axios";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 
"recharts";

function App() {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/reports/leaderboard")
      .then((res) => setReports(res.data))
      .catch(() => setReports([]));
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-10">
      <header className="flex items-center space-x-3 mb-10">
        <img src="/logo.svg" alt="TechDebtZero Logo" className="w-12 h-12" 
/>
        <h1 className="text-3xl font-bold">TechDebtZero Dashboard</h1>
      </header>

      <section className="bg-gray-800 p-6 rounded-xl shadow-lg">
        <h2 className="text-xl font-semibold mb-4">🏗️ Leaderboard</h2>
        {reports.length === 0 ? (
          <p>No data yet — connect GitHub Action Phase 3 to start tracking 
results.</p>
        ) : (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={reports}>
              <XAxis dataKey="author" stroke="#ccc" />
              <YAxis stroke="#ccc" />
              <Tooltip />
              <Bar dataKey="score" fill="#4ade80" />
            </BarChart>
          </ResponsiveContainer>
        )}
      </section>

      <footer className="text-gray-400 mt-10 text-sm">
        © 2025 TechDebtZero • AI-Powered Code Quality Analytics
      </footer>
    </div>
  );
}

export default App;

