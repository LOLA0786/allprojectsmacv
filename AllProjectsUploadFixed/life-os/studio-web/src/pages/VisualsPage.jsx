import React, { useEffect, useState } from "react";
import MemoryGraph from "../components/MemoryGraph";
import { Timeline, Heatmap } from "../components/TimelineVisualizer";
import PredictivePanel from "../components/PredictivePanel";

export default function VisualsPage(){
  const [graph, setGraph] = useState(null);
  const [events, setEvents] = useState([]);

  async function loadGraph(){
    try {
      const r = await fetch('http://0.0.0.0:8000/moats/behavior_graph/run', {
        method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ top_k: 500 })
      });
      const j = await r.json();
      setGraph(j.result);
    } catch(e){ setGraph(null); }
  }

  async function loadEvents(){
    try {
      const r = await fetch('http://0.0.0.0:8000/search/', {
        method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ query:'', top_k:200 })
      });
      const j = await r.json();
      setEvents(j || []);
    } catch(e){ setEvents([]) }
  }

  useEffect(()=>{ loadGraph(); loadEvents(); }, []);

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-3xl font-bold">Memory Visuals</h1>
        <div className="text-sm text-gray-400">Graph • Timeline • Activity • Predictions</div>
      </div>

      <div className="mb-6">
        <h3 className="text-xl font-semibold mb-2">Behavior Graph</h3>
        {graph ? <MemoryGraph graph={graph} /> : <div className="text-gray-400">Loading graph…</div>}
      </div>

      <div className="mb-6">
        <h3 className="text-xl font-semibold mb-2">Timeline</h3>
        <Timeline events={events} />
        <Heatmap events={events} />
      </div>

      <div className="mb-6">
        <PredictivePanel />
      </div>
    </div>
  );
}
