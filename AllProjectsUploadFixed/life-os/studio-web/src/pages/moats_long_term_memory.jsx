import React, { useState } from "react";
import ModeBase from "../components/moats/ModeBase";

export default function LongTermMemoryPage(){
  const [granular, setGranular] = useState(false);
  const [topk, setTopk] = useState(200);

  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Long-Term Memory</h1>
      <div className="mb-4">
        <label className="mr-3">Top K documents:</label>
        <input type="number" value={topk} onChange={e=>setTopk(Number(e.target.value))} className="px-2 py-1 text-black rounded" />
        <label className="ml-4"><input type="checkbox" checked={granular} onChange={e=>setGranular(e.target.checked)} /> By month</label>
      </div>

      <ModeBase mode="long_term_memory" description="Summarize your life memory. Use granular mode to get monthly summaries." />

      <div className="mt-4">
        <button onClick={async ()=>{
          // call run with granular param
          const res = await fetch('http://0.0.0.0:8000/moats/long_term_memory/run', {
            method:'POST', headers:{'Content-Type':'application/json'},
            body: JSON.stringify({ input: null, top_k: topk, granular })
          });
          const j = await res.json();
          alert(JSON.stringify(j.result.overall?.slice?.(0,500) || j.result.overall, null, 2));
        }} className="px-4 py-2 bg-cyan-500 rounded">Run Full Summary</button>
      </div>
    </div>
  );
}
