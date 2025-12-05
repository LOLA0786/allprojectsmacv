import { useState } from "react";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  async function doSearch() {
    const res = await fetch("http://localhost:8000/search/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, top_k: 5 }),
    });

    const data = await res.json();
    setResults(data);
  }

  return (
    <div>
      <h1 className="text-3xl font-bold">Search</h1>

      <div className="mt-6 flex gap-4">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="px-3 py-2 text-black rounded w-80"
          placeholder="Search events…"
        />
        <button
          onClick={doSearch}
          className="px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded"
        >
          Search
        </button>
      </div>

      <pre className="mt-6 bg-black/40 p-4 rounded text-sm">
        {JSON.stringify(results, null, 2)}
      </pre>
    </div>
  );
}
