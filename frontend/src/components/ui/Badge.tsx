import { classNames } from "@/lib/utils";

export function Badge({ children, variant = "default", className }: { children: React.ReactNode; variant?: "default" | "success" | "warning" | "danger" | "info" | "emergent", className?: string }) {
  const variants = {
    default: "bg-secondary text-secondary-foreground border-transparent",
    success: "bg-emerald-500/15 text-emerald-500 border-emerald-500/20",
    warning: "bg-amber-500/15 text-amber-500 border-amber-500/20",
    danger: "bg-red-500/15 text-red-500 border-red-500/20",
    info: "bg-blue-500/15 text-blue-400 border-blue-500/20",
    emergent: "bg-purple-500/15 text-purple-400 border-purple-500/20",
  };

  return (
    <span className={classNames("inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2", variants[variant], className)}>
      {children}
    </span>
  );
}
