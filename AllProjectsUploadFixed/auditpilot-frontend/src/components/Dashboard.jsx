import React from "react";

export default function Dashboard() {
  return (
    <div className="p-2">
      <h1 className="text-3xl font-bold mb-6">Welcome to AuditPilot</h1>

      <p className="text-slate-600 mb-6">
        Your AI-powered compliance and audit automation dashboard.  
        Select a tool from the sidebar to begin.
      </p>

      <div className="grid grid-cols-3 gap-6">
        
        <div className="bg-white shadow rounded-lg p-6 hover:shadow-md transition">
          <h3 className="font-semibold text-lg mb-2">📄 Upload Documents</h3>
          <p className="text-sm text-slate-500">
            Import PDFs, invoices, payroll, compliance files.
          </p>
        </div>

        <div className="bg-white shadow rounded-lg p-6 hover:shadow-md transition">
          <h3 className="font-semibold text-lg mb-2">⚖️ Breach Detection</h3>
          <p className="text-sm text-slate-500">
            Detect Fair Work and payroll compliance risks instantly.
          </p>
        </div>

        <div className="bg-white shadow rounded-lg p-6 hover:shadow-md transition">
          <h3 className="font-semibold text-lg mb-2">🧾 ATO / ASIC Autofill</h3>
          <p className="text-sm text-slate-500">
            Auto-complete government forms using your data.
          </p>
        </div>

        <div className="bg-white shadow rounded-lg p-6 hover:shadow-md transition">
          <h3 className="font-semibold text-lg mb-2">🔍 PDF Extractor</h3>
          <p className="text-sm text-slate-500">
            Extract text and data from PDF documents.
          </p>
        </div>

        <div className="bg-white shadow rounded-lg p-6 hover:shadow-md transition">
          <h3 className="font-semibold text-lg mb-2">🤖 Regulatory Q&A</h3>
          <p className="text-sm text-slate-500">
            Ask any question about AU/NZ compliance laws.
          </p>
        </div>

        <div className="bg-white shadow rounded-lg p-6 hover:shadow-md transition">
          <h3 className="font-semibold text-lg mb-2">💳 Payments</h3>
          <p className="text-sm text-slate-500">
            Support development or activate premium features.
          </p>
        </div>

      </div>
    </div>
  );
}
