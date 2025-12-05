import React, { useEffect, useState } from "react";

export default function BackendStatus({ apiUrl, setApiUrl }) {
  const [status, setStatus] = useState("unknown");

  const checkStatus = async () => {
    if (!apiUrl) return setStatus("unknown");

    try {
      const res = await fetch(apiUrl + "/");
      if (!res.ok) throw new Error();
      const data = await res.json();
      if (data.status === "running") setStatus("online");
      else setStatus("offline");
    } catch {
      setStatus("offline");
    }
  };

  useEffect(() => {
    if (apiUrl) checkStatus();
  }, [apiUrl]);

  return (
    <div className="mb-6">
      <label className="block font-semibold mb-2">Backend URL</label>
      <input
        value={apiUrl}
        onChange={(e) => setApiUrl(e.target.value)}
        placeholder="https://xxxx.ngrok-free.app"
        className="w-full px-4 py-2 border rounded-md bg-white mb-2"
      />

      <button
        onClick={checkStatus}
        className="px-4 py-2 bg-slate-800 text-white rounded-md hover:bg-slate-900"
      >
        Check Status
      </button>

      <span className="ml-4 font-semibold text-sm">
        {status === "online" && <span className="text-green-600">● Online</span>}
        {status === "offline" && <span className="text-red-600">● Offline</span>}
        {status === "unknown" && <span className="text-slate-400">● Unknown</span>}
      </span>
    </div>
  );
}
