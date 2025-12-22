import "./globals.css";
import LeftSidebar from "@/components/LeftSidebar";
import RightSidebar from "@/components/RightSidebar";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-[#0f0f0f] text-white">
        <div className="h-screen grid grid-cols-[240px_1fr_280px]">
          <LeftSidebar />
          <main className="flex justify-center overflow-y-auto">
            <div className="w-full max-w-3xl px-6 py-6">
              {children}
            </div>
          </main>
          <RightSidebar />
        </div>
      </body>
    </html>
  );
}
