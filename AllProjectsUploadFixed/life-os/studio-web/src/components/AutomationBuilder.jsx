import React, { useState } from "react";

export default function AutomationBuilder(){
  const [name, setName] = useState('');
  const [trigger, setTrigger] = useState('');
  const [action, setAction] = useState('{"type":"tag","tag":"auto"}');

  async function saveRule(){
    try {
      await fetch('http://0.0.0.0:8000/ingest', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({
          source:'studio-automation', type:'automation-config',
          timestamp: Math.floor(Date.now()/1000),
          content: `automation:${name}`, metadata: { trigger, action: JSON.parse(action) }
        })
      });
      alert('Saved as automation (demo). The automation runner must pick this up.');
      setName(''); setTrigger(''); setAction('{"type":"tag","tag":"auto"}');
    } catch(e){
      alert('Save failed');
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-3">Automation Builder (demo)</h2>
      <div className="space-y-3">
        <input value={name} onChange={e=>setName(e.target.value)} placeholder="Rule name" className="w-full px-3 py-2 rounded text-black"/>
        <input value={trigger} onChange={e=>setTrigger(e.target.value)} placeholder="Trigger keyword" className="w-full px-3 py-2 rounded text-black"/>
        <textarea value={action} onChange={e=>setAction(e.target.value)} className="w-full px-3 py-2 rounded text-black" rows={5}/>
        <div><button onClick={saveRule} className="px-4 py-2 bg-cyan-500 rounded">Save Automation</button></div>
      </div>
    </div>
  );
}
