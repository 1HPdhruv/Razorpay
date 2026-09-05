import { classNames } from "@/lib/utils";

export function Card({ children, className }: { children?: React.ReactNode; className?: string }) {
  return (
    <div className={classNames("bg-card text-card-foreground border border-border rounded-lg shadow-sm", className)}>
      {children}
    </div>
  );
}
