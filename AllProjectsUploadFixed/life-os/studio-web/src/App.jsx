import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import SearchPage from "./pages/SearchPage";
import EventsPage from "./pages/EventsPage";
import VisualsPage from "./pages/VisualsPage";
import MoatsHub from "./pages/MoatsHub";

export default function App(){
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-[#0b1220] text-white">
        <div className="w-64 bg-[#111827] border-r border-gray-700 p-4">
          <h2 className="text-xl font-bold mb-4">Life OS Studio</h2>
          <nav className="flex flex-col gap-2">
            <Link to="/" className="hover:text-blue-400">🏠 Dashboard</Link>
            <Link to="/visuals" className="hover:text-blue-400">📊 Visuals</Link>
            <Link to="/moats" className="hover:text-blue-400">🛡️ Moats</Link>
            <Link to="/search" className="hover:text-blue-400">🔍 Search</Link>
            <Link to="/events" className="hover:text-blue-400">🗂 Events</Link>
          </nav>
        </div>

        <div className="flex-1 p-8 overflow-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/visuals" element={<VisualsPage />} />
            <Route path="/moats" element={<MoatsHub />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/events" element={<EventsPage />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}
