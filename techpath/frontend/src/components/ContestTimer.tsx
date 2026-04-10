import { useEffect, useState } from 'react';

interface Props {
  endTime: string;
}

export default function ContestTimer({ endTime }: Props) {
  const [remaining, setRemaining] = useState(() => Math.max(0, new Date(endTime).getTime() - Date.now()));

  useEffect(() => {
    const id = setInterval(() => {
      setRemaining(Math.max(0, new Date(endTime).getTime() - Date.now()));
    }, 1000);
    return () => clearInterval(id);
  }, [endTime]);

  const minutes = Math.floor(remaining / 60000);
  const seconds = Math.floor((remaining % 60000) / 1000);
  const criticalClass = minutes < 5 ? 'text-red-400' : minutes < 15 ? 'text-yellow-300' : 'text-brand-200';

  return (
    <div className={`font-mono text-3xl font-bold tabular-nums ${criticalClass}`}>
      {minutes.toString().padStart(2, '0')}:{seconds.toString().padStart(2, '0')}
    </div>
  );
}
