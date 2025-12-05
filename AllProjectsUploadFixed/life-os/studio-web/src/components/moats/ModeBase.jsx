import React, {useState} from "react";

export default function ModeBase({ mode, description }){
  const [input, setInput] = useState('');
  const [resp, setResp] = useState(null);
  const [loading, setLoading] = useState(false);

  async function run(){
    setLoading(true);
    try {
      const r = await fetch(`http://0.0.0.0:8000/moats/${mode}/run`, {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ input })
      });
      const j = await r.json();
      setResp(j);
    } catch(e){
      setResp({ error: String(e) });
    } finally { setLoading(false); }
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-2">{mode.replace(/_/g,' ')}</h2>
      <div className="text-sm text-gray-400 mb-4">{description}</div>

      <textarea value={input} onChange={e=>setInput(e.target.value)} placeholder="Input for mode (optional)" className="w-full p-2 text-black rounded mb-2" rows={4} />
      <div className="flex gap-2">
        <button onClick={run} className="px-4 py-2 bg-cyan-500 rounded">{loading ? 'Running...' : 'Run'}</button>
      </div>

      <pre className="mt-4 p-2 bg-black/30 rounded text-sm">{resp ? JSON.stringify(resp, null, 2) : 'No result yet.'}</pre>
    </div>
  );
}
