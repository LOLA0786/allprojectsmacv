import React from "react";
import { Link } from "react-router-dom";

const modes = [
  "long_term_memory","behavior_graph","passive_recorder","autopilot",
  "predictive_timeline","agent_marketplace","semantic_file_explorer",
  "relationship_memory","ai_therapist","hardware_ready"
];

export default function MoatsHub(){
  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">Moats Hub — Killer Features</h1>
      <p className="mb-4 text-gray-400">These are scaffolded moat features. Click any to open the demo UI.</p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {modes.map(m => (
          <div key={m} className="p-4 bg-black/20 rounded">
            <div className="flex justify-between items-start gap-4">
              <div>
                <div className="font-semibold">{m.replace(/_/g,' ')}</div>
                <div className="text-sm text-gray-400 mt-1">Demo UI & API stub for {m}.</div>
              </div>
              <Link to={'/moats/'+m} className="px-3 py-1 bg-cyan-500 rounded">Open</Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
