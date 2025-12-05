import React, { useState } from "react";

export default function PredictivePanel(){
  const [pred, setPred] = useState(null);
  const [loading, setLoading] = useState(false);

  async function run(){
    setLoading(true);
    try {
      const r = await fetch('http://0.0.0.0:8000/moats/predictive_timeline/run', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ top_k: 1000 })
      });
      const j = await r.json();
      setPred(j.result);
    } catch(e){
      setPred({ error: String(e) });
    } finally { setLoading(false); }
  }

  return (
    <div>
      <div className="flex items-center gap-3 mb-3">
        <h3 className="text-xl font-bold">Predictions</h3>
        <button onClick={run} className="px-3 py-1 bg-cyan-500 rounded">{loading?'Running...':'Run Predictor'}</button>
      </div>

      <div className="bg-black/20 p-3 rounded">
        {pred ? (
          <div>
            <div className="text-sm text-gray-400 mb-2">Predicted recurring events</div>
            {(pred.predictions || []).map((p, i) => (
              <div key={i} className="p-2 border-b border-white/5">
                <div className="font-semibold">{p.example_document.slice(0,80)}</div>
                <div className="text-xs text-gray-400">Next: {p.predicted_next} • confidence: {p.confidence}</div>
              </div>
            ))}
            {(!pred.predictions || pred.predictions.length===0) && <div className="text-gray-400">No strong recurring patterns found.</div>}
          </div>
        ) : (
          <div className="text-gray-400">Press Run Predictor to analyze recurring events and estimate next occurrences.</div>
        )}
      </div>
    </div>
  );
}
