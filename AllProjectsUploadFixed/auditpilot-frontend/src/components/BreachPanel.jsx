import React, { useState } from "react";

export default function BreachPanel({ apiUrl }) {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const runBreachCheck = async () => {
    if (!apiUrl) return alert("Set backend URL first!");

    setLoading(true);

    const payload = {
      payroll: [
        { employee: "John", hourly_rate: 15, hours_worked: 45 },
        { employee: "Sarah", hourly_rate: 28, hours_worked: 36 },
        { employee: "Liam", hourly_rate: 17, hours_worked: 55 }
      ]
    };

    try {
      const res = await fetch(apiUrl + "/breach-detect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ error: err.message });
    }

    setLoading(false);
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">⚖️ Breach Detection</h2>

      <div className="bg-white rounded-lg shadow p-6 space-y-4 max-w-2xl">

        <p className="text-slate-600">
          Click below to run sample Fair Work payroll breach detection.
        </p>

        <button
          onClick={runBreachCheck}
          className="bg-slate-800 text-white px-4 py-2 rounded-md hover:bg-slate-900"
        >
          Run Breach Detection
        </button>

        {loading && (
          <div className="text-blue-600 font-medium">Checking breaches...</div>
        )}

        {result && (
          <pre className="bg-black text-green-400 p-4 rounded text-sm overflow-auto max-h-96">
            {JSON.stringify(result, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}
