interface Props {
  className?: string;
  lines?: number;
}

export default function Skeleton({ className = '', lines = 1 }: Props) {
  if (lines > 1) {
    return (
      <div className={`space-y-2 ${className}`}>
        {Array.from({ length: lines }).map((_, i) => (
          <div
            key={i}
            className="h-3 animate-pulse rounded bg-white/5"
            style={{ width: `${60 + ((i * 17) % 40)}%` }}
          />
        ))}
      </div>
    );
  }
  return <div className={`animate-pulse rounded bg-white/5 ${className}`} />;
}

export function CardSkeleton() {
  return (
    <div className="rounded-2xl border border-white/5 bg-ink-800 p-5">
      <Skeleton className="mb-3 h-4 w-1/3" />
      <Skeleton lines={3} />
    </div>
  );
}
