import { useEffect, useState } from "react";

export default function EventsPage() {
  const [events, setEvents] = useState([]);

  async function load() {
    try {
      const r = await fetch("http://0.0.0.0:8000/search/", {
        method:'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ query:'', top_k: 50 })
      });
      const data = await r.json();
      setEvents(data || []);
    } catch(e){
      console.warn(e);
      setEvents([]);
    }
  }

  useEffect(() => { load() }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold">Events</h1>

      <div className="mt-6 space-y-4">
        {events.map((e,i)=>(
          <div key={i} className="bg-black/30 p-4 rounded">
            <div className="text-sm text-gray-400">{e.metadata?.from || e.id}</div>
            <div className="mt-2 font-semibold">{e.document}</div>
            <div className="mt-2 text-xs text-gray-400">{JSON.stringify(e.metadata)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
