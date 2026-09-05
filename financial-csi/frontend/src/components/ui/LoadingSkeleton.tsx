import { classNames } from "@/lib/utils";

export function LoadingSkeleton({ className }: { className?: string }) {
  return (
    <div className={classNames("animate-pulse rounded-md bg-muted", className)} />
  );
}

export function SkeletonRow({ className }: { className?: string }) {
  return (
    <div className={classNames("flex items-center space-x-4", className)}>
      <LoadingSkeleton className="h-12 w-12 rounded-full" />
      <div className="space-y-2">
        <LoadingSkeleton className="h-4 w-[250px]" />
        <LoadingSkeleton className="h-4 w-[200px]" />
      </div>
    </div>
  );
}
