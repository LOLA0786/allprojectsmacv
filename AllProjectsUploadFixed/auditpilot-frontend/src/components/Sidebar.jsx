import React from "react";

const items = [
  { id: "dashboard", label: "Dashboard" },
  { id: "upload", label: "Upload Documents" },
  { id: "breach", label: "Breach Detection" },
  { id: "autofill", label: "ATO / ASIC Autofill" },
  { id: "pdf", label: "PDF Extractor" },
  { id: "regqa", label: "Regulatory Q&A" },
  { id: "payment", label: "Payments" }
];

export default function Sidebar({ active, setActive }) {
  return (
    <aside className="w-64 bg-white border-r min-h-screen p-4">
      <div className="mb-6">
        <div className="text-2xl font-bold">AuditPilot</div>
        <div className="text-sm text-slate-500">AI Compliance Auditor</div>
      </div>

      <nav className="space-y-1">
        {items.map((it) => {
          const isActive = it.id === active;
          return (
            <button
              key={it.id}
              onClick={() => setActive(it.id)}
              className={
                "w-full text-left px-3 py-2 rounded-md flex items-center gap-3 " +
                (isActive
                  ? "bg-slate-100 text-slate-900 font-semibold"
                  : "text-slate-600 hover:bg-slate-50")
              }
            >
              <span className="inline-block w-2 h-2 rounded-full" style={{ background: isActive ? "#0f172a" : "#cbd5e1" }} />
              <span>{it.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="mt-8">
        <a
          href="https://razorpay.me/@pentaprimesolutionsllp"
          target="_blank"
          rel="noreferrer"
          className="inline-block w-full text-center bg-emerald-600 text-white py-2 rounded-md hover:opacity-95"
        >
          Donate / Pay
        </a>
      </div>

      <div className="mt-6 text-xs text-slate-400">
        <div>Version: 0.1.0</div>
        <div className="mt-2">© AuditPilot</div>
      </div>
    </aside>
  );
}
