import React, { useState } from "react";

export default function PdfExtractPanel({ apiUrl }) {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const extractPdf = async () => {
    if (!apiUrl) return alert("Set backend URL first!");
    if (!file) return alert("Select a PDF file!");

    setLoading(true);

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch(apiUrl + "/extract/pdf", {
        method: "POST",
        body: form,
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
      <h2 className="text-2xl font-bold mb-4">🔍 PDF Extractor</h2>

      <div className="bg-white rounded-lg shadow p-6 space-y-4 max-w-2xl">

        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="w-full border p-2 rounded-md"
        />

        <button
          onClick={extractPdf}
          className="bg-slate-800 text-white px-4 py-2 rounded-md hover:bg-slate-900"
        >
          Extract Text
        </button>

        {loading && (
          <div className="text-blue-600 font-medium">
            Extracting PDF text...
          </div>
        )}

        {result && (
          <pre className="bg-black text-green-400 p-4 rounded text-sm overflow-auto max-h-[28rem]">
            {JSON.stringify(result, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}
