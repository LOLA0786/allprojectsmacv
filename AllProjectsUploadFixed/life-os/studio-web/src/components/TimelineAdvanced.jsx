import React, { useEffect, useState, useRef } from "react";

export default function TimelineAdvanced(){
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const perPage = 12;
  const pageRef = useRef(0);

  async function loadMore(reset=false){
    setLoading(true);
    const page = reset ? 0 : pageRef.current;
    // use search with empty query to get latest events
    const r = await fetch('http://0.0.0.0:8000/search/', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({query:'', top_k: perPage * (page+1)})
    });
    const res = await r.json();
    setEvents(res || []);
    pageRef.current = page + 1;
    setLoading(false);
  }

  useEffect(()=>{ loadMore(true) }, []);

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Timeline</h2>
        <div>
          <button onClick={()=>loadMore(true)} className="px-3 py-1 bg-white/5 rounded mr-2">Refresh</button>
          <button onClick={()=>loadMore()} className="px-3 py-1 bg-white/5 rounded">{loading ? 'Loading...':'Load more'}</button>
        </div>
      </div>

      <div className="space-y-4">
        {events.map((e, i) => (
          <div key={i} className="p-4 rounded bg-black/20 border border-white/5">
            <div className="text-sm text-gray-400">{e.metadata?.from || 'unknown'} • {e.id}</div>
            <div className="mt-2 font-semibold">{e.document}</div>
            <div className="mt-2 text-xs text-gray-400">{JSON.stringify(e.metadata)}</div>
          </div>
        ))}
        {events.length===0 && <div className="text-gray-400">No events yet — ingest something from your apps.</div>}
      </div>
    </div>
  );
}
