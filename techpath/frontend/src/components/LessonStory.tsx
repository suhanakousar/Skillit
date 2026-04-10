import { motion } from 'framer-motion';
import type { Lesson } from '../types';

interface Props {
  lesson: Lesson;
  onComplete: () => void;
  completing?: boolean;
}

export default function LessonStory({ lesson, onComplete, completing }: Props) {
  const content = lesson.content_json;
  return (
    <motion.article
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="mx-auto max-w-3xl space-y-6 rounded-2xl border border-white/5 bg-ink-800 p-8"
    >
      <header>
        <div className="text-xs uppercase tracking-wider text-brand-200">Story lesson</div>
        <h1 className="mt-2 text-3xl font-bold text-white">{lesson.title}</h1>
      </header>

      {content.hook_story && (
        <section>
          <h2 className="mb-2 text-xs font-medium uppercase tracking-wider text-white/50">
            The story
          </h2>
          <p className="text-lg leading-relaxed text-white/90">{content.hook_story}</p>
        </section>
      )}

      {content.aha_moment && (
        <section className="rounded-xl border border-brand-500/30 bg-brand-600/10 p-4">
          <div className="text-[10px] uppercase tracking-wider text-brand-200">Aha moment</div>
          <p className="mt-1 text-base font-medium text-white">{content.aha_moment}</p>
        </section>
      )}

      {content.concept_explained && (
        <section>
          <h2 className="mb-2 text-xs font-medium uppercase tracking-wider text-white/50">
            What's going on
          </h2>
          <p className="text-base leading-relaxed text-white/80">{content.concept_explained}</p>
        </section>
      )}

      {content.code_walkthrough && content.code_walkthrough.length > 0 && (
        <section>
          <h2 className="mb-3 text-xs font-medium uppercase tracking-wider text-white/50">
            Code walkthrough
          </h2>
          <div className="space-y-3">
            {content.code_walkthrough.map((step) => (
              <div key={step.step} className="rounded-lg border border-white/10 bg-ink-900 p-3">
                <div className="mb-1 text-xs text-white/50">Step {step.step}: {step.comment}</div>
                <pre className="overflow-x-auto text-sm text-brand-100">
                  <code>{step.code}</code>
                </pre>
              </div>
            ))}
          </div>
        </section>
      )}

      {content.quiz && content.quiz.length > 0 && (
        <section className="space-y-3">
          <h2 className="text-xs font-medium uppercase tracking-wider text-white/50">Quick check</h2>
          {content.quiz.map((q, i) => (
            <div key={i} className="rounded-lg border border-white/10 bg-ink-900/60 p-4">
              <p className="mb-2 text-sm font-medium text-white">{q.question}</p>
              <div className="flex flex-wrap gap-2">
                {q.options.map((opt) => (
                  <button
                    key={opt}
                    className="rounded-full border border-white/10 bg-ink-800 px-3 py-1 text-xs text-white/70 hover:bg-brand-600/20"
                  >
                    {opt}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </section>
      )}

      <button
        onClick={onComplete}
        disabled={completing}
        className="w-full rounded-xl bg-brand-600 py-3 text-sm font-medium text-white transition hover:bg-brand-500 disabled:opacity-60"
      >
        {completing ? 'Saving…' : `Mark complete · +${lesson.xp_reward} XP`}
      </button>
    </motion.article>
  );
}
