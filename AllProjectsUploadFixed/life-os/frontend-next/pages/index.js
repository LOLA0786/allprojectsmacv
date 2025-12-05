import { useState } from 'react'

export default function Home() {
  const [content, setContent] = useState("hello from nextjs")
  const [q, setQ] = useState("hello")
  const [searchRes, setSearchRes] = useState(null)

  async function sendIngest() {
    const res = await fetch('/api/ingest', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({
        source: 'nextjs',
        type: 'message',
        timestamp: Math.floor(Date.now()/1000),
        content,
        metadata: {from: 'nextjs'}
      })
    })
    const j = await res.json()
    alert(JSON.stringify(j))
  }

  async function doSearch() {
    const res = await fetch('/api/search', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({query: q, top_k: 5})
    })
    const j = await res.json()
    setSearchRes(j)
  }

  return (
    <div style={{padding:24, maxWidth:900, margin:'auto', fontFamily:'system-ui'}}>
      <h1>Life OS — Next.js Demo</h1>

      <h3>Ingest Event</h3>
      <textarea rows={4} value={content} onChange={(e)=>setContent(e.target.value)} style={{width:'100%'}}/>
      <button onClick={sendIngest} style={{marginTop:8}}>Send Ingest</button>

      <h3 style={{marginTop:40}}>Search</h3>
      <input value={q} onChange={(e)=>setQ(e.target.value)} style={{width:'100%'}}/>
      <button onClick={doSearch} style={{marginTop:8}}>Search</button>

      <pre style={{marginTop:20}}>{searchRes ? JSON.stringify(searchRes, null, 2) : ""}</pre>
    </div>
  )
}
