'use client';
import { classNames } from "@/lib/utils";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { LayoutDashboard, Network, FileSearch, Activity, LineChart, Server } from "lucide-react";

export function Sidebar() {
  const pathname = usePathname();
  const [rzpStatus, setRzpStatus] = useState<any>(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/integrations/razorpay/status')
      .then(res => res.json())
      .then(setRzpStatus)
      .catch(() => {});
  }, []);

  const navItems = [
    { name: "Dashboard", href: "/", icon: LayoutDashboard, section: "Overview" },
    { name: "Patterns", href: "/patterns", icon: Network, section: "Risk Intelligence" },
    { name: "Investigations", href: "/investigations", icon: FileSearch, section: "Risk Intelligence" },
    { name: "Simulations", href: "/simulations", icon: Activity, section: "Decisioning" },
    { name: "Evaluation", href: "/evaluation", icon: LineChart, section: "Evaluation" },
  ];

  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 flex flex-col border-r border-border bg-card">
      <div className="flex h-16 items-center px-6 border-b border-border">
        <div className="flex flex-col">
          <h1 className="text-lg font-bold tracking-wider text-foreground">FINANCIAL CSI</h1>
          <p className="text-[10px] text-muted-foreground uppercase tracking-widest font-semibold">AI Risk Manager</p>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto py-4">
        {["Overview", "Risk Intelligence", "Decisioning", "Evaluation"].map((section) => (
          <div key={section} className="mb-6 px-4">
            <h2 className="mb-2 px-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              {section}
            </h2>
            <nav className="space-y-1">
              {navItems
                .filter((item) => item.section === section)
                .map((item) => {
                  const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
                  return (
                    <Link
                      key={item.name}
                      href={item.href}
                      className={classNames(
                        "group flex items-center rounded-md px-2 py-2 text-sm font-medium",
                        isActive
                          ? "bg-secondary text-secondary-foreground"
                          : "text-muted-foreground hover:bg-muted hover:text-foreground"
                      )}
                    >
                      <item.icon
                        className={classNames(
                          "mr-3 h-5 w-5 flex-shrink-0",
                          isActive ? "text-foreground" : "text-muted-foreground group-hover:text-foreground"
                        )}
                        aria-hidden="true"
                      />
                      {item.name}
                    </Link>
                  );
                })}
            </nav>
          </div>
        ))}

        <div className="px-4 mt-8">
           <h2 className="mb-2 px-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Integrations
           </h2>
           <Link 
              href="/integrations/razorpay"
              className={classNames(
                "group flex items-center rounded-md px-2 py-2 text-sm font-medium",
                pathname === "/integrations/razorpay"
                  ? "bg-secondary text-secondary-foreground"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )}
            >
              <Server 
                className={classNames(
                  "mr-3 h-5 w-5 flex-shrink-0",
                  pathname === "/integrations/razorpay" ? "text-foreground" : "text-muted-foreground group-hover:text-foreground"
                )}
                aria-hidden="true" 
              />
              <div className="flex flex-col">
                <span>Razorpay Test Mode</span>
                <span className={classNames("text-[10px] mt-0.5 font-mono", rzpStatus?.enabled ? "text-emerald-500" : "text-muted-foreground")}>
                  {rzpStatus?.credentials_configured ? '● Configured' : '○ Not configured'}
                </span>
              </div>
           </Link>
        </div>
      </div>

      <div className="border-t border-border p-4">
        <div className="flex items-center text-sm font-medium text-emerald-500">
          <span className="relative flex h-2 w-2 mr-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          System Operational
        </div>
      </div>
    </aside>
  );
}
