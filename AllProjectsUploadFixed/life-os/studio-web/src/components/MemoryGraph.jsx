import React, { useEffect, useRef } from "react";

export default function MemoryGraph({ graph }) {
  const svgRef = useRef();

  useEffect(() => {
    const svg = svgRef.current;
    if (!svg || !graph) return;
    const width = svg.clientWidth || 600;
    const height = svg.clientHeight || 400;
    const ctx = svg.getContext("2d");
    ctx.clearRect(0,0,width,height);

    const nodes = graph.nodes || [];
    const edges = graph.edges || [];

    const N = Math.max(1, nodes.length);
    const cx = width/2, cy = height/2, R = Math.min(width, height)/2 - 40;

    // position nodes on circle
    const positions = {};
    nodes.slice(0, Math.min(60, nodes.length)).forEach((n, i) => {
      const ang = (i / N) * Math.PI * 2;
      positions[n.id] = {
        x: cx + R * Math.cos(ang),
        y: cy + R * Math.sin(ang),
        size: Math.min(24, 6 + Math.log(n.count+1)*6)
      };
    });

    // draw edges
    ctx.strokeStyle = 'rgba(255,255,255,0.12)';
    ctx.lineWidth = 1;
    edges.slice(0, 400).forEach(e => {
      const s = positions[e.source];
      const t = positions[e.target];
      if (s && t) {
        ctx.beginPath();
        ctx.moveTo(s.x, s.y);
        ctx.lineTo(t.x, t.y);
        ctx.stroke();
      }
    });

    // draw nodes
    nodes.slice(0, Math.min(60, nodes.length)).forEach(n => {
      const p = positions[n.id];
      if (!p) return;
      // circle
      ctx.fillStyle = 'rgba(56,189,248,0.9)';
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI*2);
      ctx.fill();
      // label
      ctx.fillStyle = 'white';
      ctx.font = '12px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(n.id.split(' ').slice(0,3).join(' '), p.x, p.y + p.size + 12);
    });

  }, [graph]);

  return (
    <div style={{width: '100%', height: 400, background: 'transparent', borderRadius:8}}>
      <canvas ref={svgRef} width={900} height={400} style={{width:'100%', height:400}} />
    </div>
  );
}
