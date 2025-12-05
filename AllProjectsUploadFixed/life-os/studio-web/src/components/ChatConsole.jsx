import React, { useState } from "react";

export default function ChatConsole(){
  const [messages, setMessages] = useState([
    {from:'system', text:'Welcome to Life OS Chat.'}
  ]);
  const [input, setInput] = useState('');

  async function send(){
    if(!input.trim()) return;
    const userMsg = {from:'user', text: input};
    setMessages(m=>[...m, userMsg]);
    setInput('');

    // POST to /ingest as a user message (and optionally ask backend to produce a reply)
    await fetch('http://0.0.0.0:8000/ingest', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({source:'chat', type:'message', timestamp: Math.floor(Date.now()/1000), content: input, metadata:{from:'chat'}})
    });

    // naive bot reply using search: find similar events and reply summarised
    try {
      const r = await fetch('http://0.0.0.0:8000/search/', {
        method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({query: input, top_k:3})
      });
      const res = await r.json();
      const doc = (res && res.length) ? res.map(x=>x.document).join('\\n---\\n') : 'No related memories found.';
      const bot = {from:'bot', text: 'Related memories:\\n' + doc};
      setMessages(m=>[...m, bot]);
    } catch(e){
      setMessages(m=>[...m, {from:'bot', text: 'Failed to fetch.'}])
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-3">Chat — Ask your Life</h1>
      <div className="border rounded p-3" style={{height: '60vh', overflow:'auto', background:'rgba(255,255,255,0.02)'}}>
        {messages.map((m,i)=>(
          <div key={i} className={"mb-3 "+ (m.from==='user' ? 'text-right' : 'text-left')}>
            <div className={"inline-block p-2 rounded " + (m.from==='user' ? 'bg-cyan-600/80' : 'bg-white/5')}>{m.text}</div>
          </div>
        ))}
      </div>

      <div className="mt-3 flex gap-2">
        <input value={input} onChange={e=>setInput(e.target.value)} className="flex-1 px-3 py-2 rounded text-black" placeholder="Ask something..."/>
        <button onClick={send} className="px-4 py-2 bg-cyan-500 rounded">Send</button>
      </div>
    </div>
  );
}
