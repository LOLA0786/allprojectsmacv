import React, { useState, useEffect } from "react";
import { loadKeys } from "../localKeys.js";

export default function RegQaPanel({ apiUrl }) {
  const [question, setQuestion] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [provider, setProvider] = useState("openai");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const keys = loadKeys();
    if (provider === "openai" && keys.openai) setApiKey(keys.openai);
    if (provider === "grok" && keys.grok) setApiKey(keys.grok);
    if (provider === "gemini" && keys.gemini) setApiKey(keys.gemini);
  }, [provider]);

  const askQuestion = async () => {
    if (!apiUrl) return alert("Set backend URL first!");
    if (!apiKey) return alert("API key missing!");

    setLoading(true);

    const payload = {
      question: "[" + provider.toUpperCase() + "] " + question,
      api_key: apiKey
    };

    try {
      const res = await fetch(apiUrl + "/reg/qa", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
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
      <h2 className="text-2xl font-bold mb-4">🤖 Regulatory Q&A (GPT / Grok / Gemini)</h2>

      <div className="bg-white shadow rounded-lg p-6 space-y-4 max-w-2xl">

        <div>
          <label className="font-semibold">Choose Model</label>
          <select
            value={provider}
            className="w-full border p-2 rounded-md mt-1"
            onChange={(e) => setProvider(e.target.value)}
          >
            <option value="openai">OpenAI</option>
            <option value="grok">Grok</option>
            <option value="gemini">Gemini</option>
          </select>
        </div>

        <div>
          <label className="font-semibold">API Key</label>
          <input
            type="password"
            className="w-full border p-2 rounded-md mt-1"
            placeholder="API Key (auto-filled from Base64 if present)"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
          />
        </div>

        <div>
          <label className="font-semibold">Your Question</label>
          <textarea
            className="w-full border p-2 rounded-md mt-1 h-28"
            placeholder="Ask any AU/NZ compliance question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          ></textarea>
        </div>

        <button
          onClick={askQuestion}
          className="bg-slate-800 text-white px-4 py-2 rounded-md hover:bg-slate-900"
        >
          Ask AI
        </button>

        {loading && (
          <div className="text-blue-600 font-medium">Thinking...</div>
        )}

        {result && (
          <pre className="bg-black text-green-400 p-4 rounded text-sm overflow-auto max-h-[28rem] whitespace-pre-wrap">
            {JSON.stringify(result, null, 2)}
          </pre>
        )}

      </div>
    </div>
  );
}
