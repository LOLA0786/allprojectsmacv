export default function LeftSidebar() {
  return (
    <aside className="border-r border-white/10 p-4 text-sm text-gray-400">
      <div className="mb-6 text-xs uppercase tracking-widest text-gray-500">
        Live Topics
      </div>

      <div className="space-y-2">
        <div className="hover:text-white cursor-pointer">
          MacBook battery
        </div>
        <div className="hover:text-white cursor-pointer">
          Startup funding
        </div>
        <div className="hover:text-white cursor-pointer">
          AI agents
        </div>
      </div>
    </aside>
  );
}
