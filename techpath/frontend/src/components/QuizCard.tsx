import { useState } from 'react';
import { motion } from 'framer-motion';

interface Props {
  question: string;
  options: string[];
  correct: string;
  explanation?: string;
  onAnswer?: (correct: boolean) => void;
}

export default function QuizCard({ question, options, correct, explanation, onAnswer }: Props) {
  const [selected, setSelected] = useState<string | null>(null);
  const answered = selected !== null;
  const isCorrect = selected === correct;

  const handle = (opt: string) => {
    if (answered) return;
    setSelected(opt);
    onAnswer?.(opt === correct);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl border border-white/10 bg-ink-800 p-5"
    >
      <p className="mb-4 text-sm font-medium text-white">{question}</p>
      <div className="grid gap-2">
        {options.map((opt) => {
          let cls = 'bg-ink-900 text-white/80 hover:bg-brand-600/20';
          if (answered) {
            if (opt === correct) cls = 'bg-emerald-500/20 text-emerald-200 border-emerald-400/50';
            else if (opt === selected) cls = 'bg-red-500/20 text-red-200 border-red-400/50';
            else cls = 'bg-ink-900 text-white/40';
          }
          return (
            <button
              key={opt}
              onClick={() => handle(opt)}
              className={`rounded-lg border border-white/10 px-4 py-2 text-left text-sm transition ${cls}`}
            >
              {opt}
            </button>
          );
        })}
      </div>
      {answered && explanation && (
        <p className={`mt-3 text-xs ${isCorrect ? 'text-emerald-300' : 'text-red-300'}`}>
          {isCorrect ? '✓ ' : '✗ '}
          {explanation}
        </p>
      )}
    </motion.div>
  );
}
