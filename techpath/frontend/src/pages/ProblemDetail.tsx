import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { problemsApi, submissionsApi } from '../api/endpoints';
import type { ProblemDetail, SubmissionResult } from '../types';
import CodeEditor from '../components/CodeEditor';
import HintChat from '../components/HintChat';
import Skeleton from '../components/Skeleton';
import { toast } from '../store/toast';
import { useAuthStore } from '../store/auth';

const STARTER_BY_LANG: Record<string, string> = {
  python: '# write your solution\n',
  cpp: '#include <bits/stdc++.h>\nusing namespace std;\nint main() {\n    return 0;\n}\n',
  java: 'public class Main {\n    public static void main(String[] args) {\n    }\n}\n',
  javascript: '// write your solution\n',
};

type Tab = 'description' | 'hints' | 'submissions';

export default function ProblemDetailPage() {
  const { problemId } = useParams<{ problemId: string }>();
  const [problem, setProblem] = useState<ProblemDetail | null>(null);
  const [language, setLanguage] = useState('python');
  const [code, setCode] = useState('');
  const [result, setResult] = useState<SubmissionResult | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [tab, setTab] = useState<Tab>('description');
  const loadUser = useAuthStore((s) => s.loadUser);

  useEffect(() => {
    if (!problemId) return;
    problemsApi.get(problemId).then((p) => {
      setProblem(p);
      setCode(p.starter_code_json[language] ?? STARTER_BY_LANG[language] ?? '');
    });
  }, [problemId]);

  useEffect(() => {
    if (!problem) return;
    setCode(problem.starter_code_json[language] ?? STARTER_BY_LANG[language] ?? '');
  }, [language, problem]);

  const submit = async () => {
    if (!problem) return;
    setSubmitting(true);
    try {
      const r = await submissionsApi.submit(problem.id, language, code);
      setResult(r);
      if (r.status === 'accepted') {
        toast.success('Accepted', `+${r.xp_awarded} XP · ${r.runtime_ms} ms`);
        loadUser();
      } else {
        toast.error(
          `Submission ${r.status.replace('_', ' ')}`,
          `${r.test_results.length} test(s) run`,
        );
      }
    } catch (err: any) {
      toast.error('Submission failed', err?.response?.data?.detail ?? 'Try again');
    } finally {
      setSubmitting(false);
    }
  };

  if (!problem) {
    return (
      <div className="grid h-[calc(100vh-3rem)] grid-cols-1 gap-4 lg:grid-cols-2">
        <div className="rounded-2xl border border-white/5 bg-ink-800 p-6">
          <Skeleton className="mb-3 h-6 w-2/3" />
          <Skeleton lines={6} />
        </div>
        <div className="rounded-2xl border border-white/5 bg-ink-800 p-6">
          <Skeleton lines={10} />
        </div>
      </div>
    );
  }

  return (
    <div className="grid h-[calc(100vh-3rem)] grid-cols-1 gap-4 lg:grid-cols-2">
      <div className="overflow-y-auto rounded-2xl border border-white/5 bg-ink-800 p-6 scrollbar-thin">
        <div className="mb-3 flex items-center gap-2">
          <h1 className="text-xl font-bold text-white">{problem.title}</h1>
          <span className="rounded-full bg-brand-600/20 px-2 py-0.5 text-[10px] text-brand-200">
            Difficulty {problem.difficulty}
          </span>
        </div>
        <div className="mb-4 flex flex-wrap gap-1">
          {problem.tags.map((t) => (
            <span key={t} className="rounded-full bg-ink-700 px-2 py-0.5 text-[10px] text-white/60">
              {t}
            </span>
          ))}
        </div>

        <div className="mb-4 flex gap-4 border-b border-white/10 text-xs">
          {(['description', 'hints', 'submissions'] as Tab[]).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`pb-2 capitalize ${tab === t ? 'border-b-2 border-brand-500 text-white' : 'text-white/50'}`}
            >
              {t}
            </button>
          ))}
        </div>

        {tab === 'description' && (
          <div className="space-y-4 text-sm text-white/80">
            <p className="leading-relaxed whitespace-pre-line">{problem.description}</p>
            {problem.examples_json.length > 0 && (
              <div>
                <h3 className="mb-2 text-xs uppercase text-white/50">Examples</h3>
                {problem.examples_json.map((ex, i) => (
                  <pre key={i} className="mt-2 rounded bg-ink-900 p-3 text-xs text-brand-100">
                    Input:  {ex.input}
                    {'\n'}Output: {ex.output}
                  </pre>
                ))}
              </div>
            )}
            {problem.constraints_text && (
              <div>
                <h3 className="mb-1 text-xs uppercase text-white/50">Constraints</h3>
                <p className="text-xs text-white/60">{problem.constraints_text}</p>
              </div>
            )}
          </div>
        )}

        {tab === 'hints' && (
          <div className="space-y-3 text-sm text-white/70">
            <p className="rounded-lg border border-brand-500/20 bg-brand-600/10 p-3 text-xs">
              Use the floating 💡 button in the bottom-right to chat with the AI hint coach —
              it gives progressive hints without spoiling the answer.
            </p>
            <div className="space-y-2">
              {problem.hints_json.map((h) => (
                <details
                  key={h.level}
                  className="rounded-lg border border-white/10 bg-ink-900 p-3"
                >
                  <summary className="cursor-pointer text-xs text-white/80">
                    Reveal built-in hint {h.level}
                  </summary>
                  <p className="mt-2 text-xs text-white/60">{h.text}</p>
                </details>
              ))}
            </div>
          </div>
        )}

        {tab === 'submissions' && result && (
          <div className="space-y-2 text-xs text-white/70">
            <div>Status: <strong>{result.status}</strong></div>
            <div>Runtime: {result.runtime_ms} ms</div>
            <div>XP: +{result.xp_awarded}</div>
          </div>
        )}
      </div>

      <div className="flex flex-col gap-3">
        <div className="flex-1 min-h-0">
          <CodeEditor
            language={language}
            value={code}
            onChange={setCode}
            onLanguageChange={setLanguage}
            onSubmit={submit}
            submitting={submitting}
          />
        </div>
        {result && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`rounded-xl border p-4 text-sm ${
              result.status === 'accepted'
                ? 'border-emerald-500/50 bg-emerald-500/10 text-emerald-200'
                : 'border-red-500/50 bg-red-500/10 text-red-200'
            }`}
          >
            <div className="font-medium">
              {result.status === 'accepted' ? '✓ Accepted' : `✗ ${result.status}`}
            </div>
            <div className="mt-1 text-xs opacity-80">
              {result.runtime_ms} ms · +{result.xp_awarded} XP
            </div>
          </motion.div>
        )}
      </div>

      <HintChat problemId={problem.id} userCode={code} />
    </div>
  );
}
