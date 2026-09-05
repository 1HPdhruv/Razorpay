import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Financial CSI | Risk Manager",
  description: "AI Risk Manager for discovering hidden payment-loss patterns",
};

import { Sidebar } from "@/components/layout/Sidebar";
import { TopHeader } from "@/components/layout/TopHeader";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-foreground antialiased selection:bg-primary selection:text-primary-foreground min-h-screen">
        <div className="flex h-screen overflow-hidden">
          <Sidebar />
          <div className="flex flex-1 flex-col overflow-hidden pl-64">
            <TopHeader />
            <main className="flex-1 overflow-y-auto p-8">
              <div className="mx-auto max-w-7xl">
                {children}
              </div>
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}
