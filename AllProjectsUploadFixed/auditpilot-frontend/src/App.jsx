import React, { useState } from "react";
import Sidebar from "./components/Sidebar.jsx";
import BackendStatus from "./components/BackendStatus.jsx";
import Dashboard from "./components/Dashboard.jsx";
import UploadPanel from "./components/UploadPanel.jsx";
import BreachPanel from "./components/BreachPanel.jsx";
import AutofillPanel from "./components/AutofillPanel.jsx";
import PdfExtractPanel from "./components/PdfExtractPanel.jsx";
import RegQaPanel from "./components/RegQaPanel.jsx";
import PaymentPanel from "./components/PaymentPanel.jsx";

export default function App() {
  const [active, setActive] = useState("dashboard");
  const [apiUrl, setApiUrl] = useState("");

  return (
    <div className="min-h-screen flex bg-slate-100">
      
      <Sidebar active={active} setActive={setActive} />

      <main className="flex-1 p-6">
        <BackendStatus apiUrl={apiUrl} setApiUrl={setApiUrl} />

        {active === "dashboard" && <Dashboard />}
        {active === "upload" && <UploadPanel apiUrl={apiUrl} />}
        {active === "breach" && <BreachPanel apiUrl={apiUrl} />}
        {active === "autofill" && <AutofillPanel apiUrl={apiUrl} />}
        {active === "pdf" && <PdfExtractPanel apiUrl={apiUrl} />}
        {active === "regqa" && <RegQaPanel apiUrl={apiUrl} />}
        {active === "payment" && <PaymentPanel />}
      </main>
    </div>
  );
}
