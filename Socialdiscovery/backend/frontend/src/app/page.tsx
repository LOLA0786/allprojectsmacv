"use client"

import { useEffect, useState } from "react"

export default function Home() {
  const [data, setData] = useState<any>(null)

  useEffect(() => {
    fetch("${process.env.NEXT_PUBLIC_API_URL}/intent")
      .then(res => res.json())
      .then(setData)
      .catch(() => {})
  }, [])

  if (!data) {
    return (
      <main style={{ padding: 40 }}>
        <h1>Loading live intent…</h1>
      </main>
    )
  }

  return (
    <main style={{ padding: 40, fontFamily: "system-ui" }}>
      <h1>🔥 Live Intent</h1>

      <h2>{data.topic}</h2>
      <p><b>Momentum:</b> {data.momentum}</p>
      <p><b>Confidence:</b> {Math.round(data.confidence * 100)}%</p>

      <hr />

      <h3>✅ Authenticity</h3>
      <p>{data.authenticity.label}</p>
      <p>
        Human {data.authenticity.human_source_pct}% ·
        AI {data.authenticity.ai_assist_pct}%
      </p>

      <hr />

      <h3>🧠 AI Ethics</h3>
      <p>Human input: {data.ethics.human_input * 100}%</p>
      <p>AI assist: {data.ethics.ai_input * 100}%</p>
      <p>Moderated: {data.ethics.moderated ? "Yes" : "No"}</p>

      <hr />

      <p style={{ opacity: 0.6 }}>
        ⏳ Expires at: {new Date(data.expires_at).toLocaleString()}
      </p>
    </main>
  )
}
