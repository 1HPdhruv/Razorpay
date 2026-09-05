'use client';
import { classNames } from "@/lib/utils";
import { RefreshCcw, Bell } from "lucide-react";
import { usePathname } from "next/navigation";

export function TopHeader() {
  const pathname = usePathname();
  
  const getPageInfo = () => {
    if (pathname === "/") return { title: "Risk Overview", subtitle: "Discover and investigate payment-loss patterns." };
    if (pathname.startsWith("/patterns")) return { title: "Emergent Patterns", subtitle: "Patterns discovered from payment-event interactions." };
    if (pathname.startsWith("/investigations")) return { title: "Pattern Investigation", subtitle: "Evidence-backed analysis of the payment lifecycle." };
    if (pathname.startsWith("/simulations")) return { title: "Counterfactual Simulation", subtitle: "What could happen if we intervene?" };
    if (pathname.startsWith("/evaluation")) return { title: "Evaluation", subtitle: "Does the discovered risk generalize to unseen transactions?" };
    return { title: "Financial CSI", subtitle: "AI Risk Manager" };
  };

  const { title, subtitle } = getPageInfo();

  return (
    <header className="sticky top-0 z-30 flex h-16 shrink-0 items-center gap-x-4 border-b border-border bg-card px-4 sm:gap-x-6 sm:px-6 lg:px-8">
      <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
        <div className="flex flex-1 flex-col justify-center">
          <h1 className="text-xl font-semibold leading-6 text-foreground">{title}</h1>
          <p className="text-sm text-muted-foreground">{subtitle}</p>
        </div>
        <div className="flex items-center gap-x-4 lg:gap-x-6">
          <button
            type="button"
            onClick={() => window.location.reload()}
            className="-m-2.5 p-2.5 text-muted-foreground hover:text-foreground"
          >
            <span className="sr-only">Refresh</span>
            <RefreshCcw className="h-5 w-5" aria-hidden="true" />
          </button>
        </div>
      </div>
    </header>
  );
}
