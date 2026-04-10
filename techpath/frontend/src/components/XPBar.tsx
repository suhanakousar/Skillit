import { motion } from 'framer-motion';

interface Props {
  current: number;
  target: number;
  label?: string;
}

export default function XPBar({ current, target, label }: Props) {
  const pct = Math.min(100, Math.round((current / Math.max(1, target)) * 100));
  return (
    <div className="w-full">
      {label && (
        <div className="mb-1 flex items-center justify-between text-xs text-white/60">
          <span>{label}</span>
          <span>
            {current} / {target} XP
          </span>
        </div>
      )}
      <div className="h-2 w-full overflow-hidden rounded-full bg-ink-700">
        <motion.div
          className="h-full rounded-full bg-gradient-to-r from-brand-500 to-brand-200"
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
        />
      </div>
    </div>
  );
}
