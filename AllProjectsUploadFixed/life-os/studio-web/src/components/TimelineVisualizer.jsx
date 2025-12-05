import React from "react";

function formatTS(ts){
  try {
    if (typeof ts === 'number') return new Date(ts*1000).toISOString().split('T')[0];
    return ts;
  } catch { return ts; }
}

export function Timeline({ events = [] }){
  return (
    <div style={{overflowX:'auto'}} className="py-2">
      <div style={{display:'flex', gap:12, padding:8}}>
        {events.map((e, i) => (
          <div key={i} className="p-3 bg-black/20 rounded min-w-[220px]">
            <div className="text-xs text-gray-400">{formatTS(e.timestamp)}</div>
            <div className="mt-2 font-semibold">{(e.document||'').slice(0,120)}</div>
            <div className="mt-2 text-xs text-gray-400">{JSON.stringify(e.metadata)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export function Heatmap({ events = [] }){
  // count per day
  const counts = {};
  events.forEach(e => {
    let d = formatTS(e.timestamp);
    counts[d] = (counts[d]||0) + 1;
  });
  const days = Object.keys(counts).sort();
  return (
    <div className="mt-4">
      <div className="text-sm text-gray-300 mb-2">Activity heatmap (per day)</div>
      <div style={{display:'flex', gap:6, flexWrap:'wrap'}}>
        {days.map(d => {
          const c = counts[d];
          const shade = Math.min(0.9, 0.15 + Math.log(c+1)/3);
          const bg = `rgba(56,189,248,${shade})`;
          return <div key={d} style={{background:bg, padding:'8px 10px', borderRadius:6}} className="text-xs text-white">{d} ({c})</div>
        })}
      </div>
    </div>
  );
}
