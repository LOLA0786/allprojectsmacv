import React, { useState } from "react";

export default function AutofillPanel({ apiUrl }) {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [formType, setFormType] = useState("ATO_BAS");

  const runAutofill = async () => {
    if (!apiUrl) return alert("Set backend URL first!");

    setLoading(true);

    const payload = {
      company: {
        name: "AuditPilot Pty Ltd",
        acn: "123456789",
        registered_office: "123 George St, Sydney",
        gst_collected: 12000,
        gst_paid: 8000,
        sales: 35000,
        expenses: 15000,
      },
      form_type: formType,
    };

    try {
      const res = await fetch(apiUrl + "/form/autofill", {
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
      <h2 className="text-2xl font-bold mb-4">🧾 ATO / ASIC Autofill</h2>

      <div className="bg-white rounded-lg shadow p-6 space-y-4 max-w-2xl">

        <div>
          <label className="font-semibold">Select Form Type</label>
          <select
            value={formType}
            onChange={(e) => setFormType(e.target.value)}
            className="w-full border p-2 rounded-md mt-1"
          >
            <option value="ATO_BAS">ATO BAS</option>
            <option value="ASIC_AnnualReview">ASIC Annual Review</option>
          </select>
        </div>

        <button
          onClick={runAutofill}
          className="bg-slate-800 text-white px-4 py-2 rounded-md hover:bg-slate-900"
        >
          Autofill Form
        </button>

        {loading && (
          <div className="text-blue-600 font-medium">
            Generating autofill data...
          </div>
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
