import React, { useRef, useState } from "react";

export default function NotionEditor(){
  const editorRef = useRef(null);
  const [status, setStatus] = useState('');

  async function save(){
    const content = editorRef.current.innerText || '';
    if(!content.trim()) return alert('Write something first');
    setStatus('Saving...');
    try {
      await fetch('http://0.0.0.0:8000/ingest', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({source:'studio-notes', type:'note', timestamp: Math.floor(Date.now()/1000), content, metadata:{from:'notion'}})
      });
      setStatus('Saved');
      setTimeout(()=>setStatus(''), 1500);
      editorRef.current.innerText = '';
    } catch(e){
      setStatus('Failed');
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-3">Notebook / Notion-like Editor</h2>
      <div ref={editorRef} contentEditable className="min-h-[200px] p-4 rounded bg-black/10" style={{outline:'none'}}>Write notes here...</div>
      <div className="mt-3 flex items-center gap-3">
        <button onClick={save} className="px-4 py-2 bg-cyan-500 rounded">Save to Life OS</button>
        <div className="text-sm text-gray-400">{status}</div>
      </div>
    </div>
  );
}
