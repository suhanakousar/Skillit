import { useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { problemsApi, submissionsApi } from '../api/endpoints';
import type { ProblemDetail, RunResult, SubmissionResult } from '../types';
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
type ConsoleTab = 'testcases' | 'result';

function verdictLabel(status: string): string {
  switch (status) {
    case 'accepted':
      return 'Accepted';
    case 'wrong_answer':
      return 'Wrong Answer';
    case 'tle':
      return 'Time Limit Exceeded';
    case 'runtime_error':
      return 'Runtime Error';
    case 'compile_error':
      return 'Compile Error';
    default:
      return status.replace(/_/g, ' ');
  }
}

function verdictColor(status: string): string {
  if (status === 'accepted') return 'text-emerald-300';
  if (status === 'wrong_answer') return 'text-red-300';
  if (status === 'compile_error') return 'text-amber-300';
  return 'text-orange-300';
}

export default function ProblemDetailPage() {
  const { problemId } = useParams<{ problemId: string }>();
  const [problem, setProblem] = useState<ProblemDetail | null>(null);
  const [language, setLanguage] = useState('python');
  const [code, setCode] = useState('');
  const [result, setResult] = useState<SubmissionResult | null>(null);
  const [runResult, setRunResult] = useState<RunResult | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [running, setRunning] = useState(false);
  const [tab, setTab] = useState<Tab>('description');
  const [consoleTab, setConsoleTab] = useState<ConsoleTab>('testcases');
  const [activeCaseIdx, setActiveCaseIdx] = useState(0);
  const [useCustomStdin, setUseCustomStdin] = useState(false);
  const [customStdin, setCustomStdin] = useState('');
  const loadUser = useAuthStore((s) => s.loadUser);

  useEffect(() => {
    if (!problemId) return;
    problemsApi.get(problemId).then((p) => {
      setProblem(p);
      setCode(p.starter_code_json[language] ?? STARTER_BY_LANG[language] ?? '');
      setActiveCaseIdx(0);
    });
  }, [problemId]);

  useEffect(() => {
    if (!problem) return;
    setCode(problem.starter_code_json[language] ?? STARTER_BY_LANG[language] ?? '');
  }, [language, problem]);

  const examples = useMemo(() => problem?.examples_json ?? [], [problem]);

  const run = async () => {
    if (!problem) return;
    setRunning(true);
    setConsoleTab('result');
    try {
      const r = await submissionsApi.run(
        problem.id,
        language,
        code,
        useCustomStdin ? customStdin : undefined,
      );
      setRunResult(r);
      if (r.compile_error) {
        toast.error('Compile error', 'Check the console for details');
      } else if (r.status === 'accepted') {
        toast.success('Sample tests passed', 'Hit Submit to run the hidden tests');
      } else {
        toast.error(verdictLabel(r.status), 'See the console for actual vs expected');
      }
    } catch (err: any) {
      toast.error('Run failed', err?.response?.data?.detail ?? 'Try again');
    } finally {
      setRunning(false);
    }
  };

  const submit = async () => {
    if (!problem) return;
    setSubmitting(true);
    setConsoleTab('result');
    try {
      const r = await submissionsApi.submit(problem.id, language, code);
      setResult(r);
      setRunResult(null);
      if (r.status === 'accepted') {
        toast.success('Accepted', `+${r.xp_awarded} XP · ${r.runtime_ms} ms · ${r.passed}/${r.total} tests`);
        loadUser();
      } else {
        toast.error(
          verdictLabel(r.status),
          `${r.passed}/${r.total} tests passed`,
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
            {examples.length > 0 && (
              <div>
                <h3 className="mb-2 text-xs uppercase text-white/50">Examples</h3>
                {examples.map((ex, i) => (
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
            <div>
              Status: <strong className={verdictColor(result.status)}>{verdictLabel(result.status)}</strong>
            </div>
            <div>
              Tests passed: {result.passed}/{result.total}
            </div>
            <div>Runtime: {result.runtime_ms} ms</div>
            <div>XP: +{result.xp_awarded}</div>
          </div>
        )}
      </div>

      <div className="flex min-h-0 flex-col gap-3">
        <div className="min-h-[280px] flex-1">
          <CodeEditor
            language={language}
            value={code}
            onChange={setCode}
            onLanguageChange={setLanguage}
            onRun={run}
            onSubmit={submit}
            running={running}
            submitting={submitting}
          />
        </div>

        {/* LeetCode-style console panel */}
        <div className="flex max-h-[45%] min-h-[180px] flex-col overflow-hidden rounded-xl border border-white/10 bg-ink-800">
          <div className="flex items-center gap-4 border-b border-white/10 bg-ink-700 px-3 py-2 text-xs">
            {(['testcases', 'result'] as ConsoleTab[]).map((t) => (
              <button
                key={t}
                onClick={() => setConsoleTab(t)}
                className={`capitalize ${
                  consoleTab === t ? 'font-medium text-white' : 'text-white/50 hover:text-white/80'
                }`}
              >
                {t === 'testcases' ? 'Testcase' : 'Result'}
              </button>
            ))}
            <div className="ml-auto text-[10px] text-white/40">
              {running ? 'Running…' : submitting ? 'Submitting…' : 'Idle'}
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-3 text-xs scrollbar-thin">
            {consoleTab === 'testcases' && (
              <div className="space-y-3">
                <label className="flex items-center gap-2 text-white/70">
                  <input
                    type="checkbox"
                    checked={useCustomStdin}
                    onChange={(e) => setUseCustomStdin(e.target.checked)}
                  />
                  Use custom input
                </label>

                {useCustomStdin ? (
                  <textarea
                    value={customStdin}
                    onChange={(e) => setCustomStdin(e.target.value)}
                    placeholder="Type stdin exactly as the program will receive it"
                    className="h-24 w-full resize-none rounded-md border border-white/10 bg-ink-900 p-2 font-mono text-[11px] text-brand-100 outline-none focus:border-brand-500"
                  />
                ) : examples.length === 0 ? (
                  <p className="text-white/50">No sample cases for this problem.</p>
                ) : (
                  <>
                    <div className="flex flex-wrap gap-1">
                      {examples.map((_, i) => (
                        <button
                          key={i}
                          onClick={() => setActiveCaseIdx(i)}
                          className={`rounded-full px-2 py-0.5 text-[10px] ${
                            i === activeCaseIdx
                              ? 'bg-brand-600 text-white'
                              : 'bg-ink-700 text-white/60 hover:bg-ink-600'
                          }`}
                        >
                          Case {i + 1}
                        </button>
                      ))}
                    </div>
                    <pre className="rounded-md border border-white/10 bg-ink-900 p-2 font-mono text-[11px] text-brand-100">
                      {examples[activeCaseIdx]?.input}
                    </pre>
                    <div className="text-[10px] text-white/40">Expected</div>
                    <pre className="rounded-md border border-white/10 bg-ink-900 p-2 font-mono text-[11px] text-white/70">
                      {examples[activeCaseIdx]?.output}
                    </pre>
                  </>
                )}
              </div>
            )}

            {consoleTab === 'result' && !runResult && !result && (
              <p className="text-white/50">
                Hit <span className="text-white">Run</span> to test against the sample cases, or{' '}
                <span className="text-white">Submit</span> to grade against all hidden tests.
              </p>
            )}

            {consoleTab === 'result' && runResult && (
              <div className="space-y-3">
                <div className={`text-sm font-medium ${verdictColor(runResult.status)}`}>
                  {verdictLabel(runResult.status)}
                </div>
                {runResult.compile_error && (
                  <pre className="overflow-x-auto rounded-md border border-amber-500/30 bg-amber-500/10 p-2 font-mono text-[11px] text-amber-200">
                    {runResult.compile_error}
                  </pre>
                )}
                {runResult.results.map((r) => (
                  <div
                    key={r.index}
                    className="rounded-md border border-white/10 bg-ink-900 p-2"
                  >
                    <div className="mb-1 flex items-center justify-between text-[10px]">
                      <span className={verdictColor(r.status)}>
                        Case {r.index + 1} · {verdictLabel(r.status)}
                      </span>
                      {r.runtime_ms != null && (
                        <span className="text-white/40">{r.runtime_ms} ms</span>
                      )}
                    </div>
                    {r.stdin && (
                      <>
                        <div className="text-[10px] text-white/40">Input</div>
                        <pre className="mb-1 whitespace-pre-wrap font-mono text-[11px] text-white/70">
                          {r.stdin}
                        </pre>
                      </>
                    )}
                    {r.expected != null && (
                      <>
                        <div className="text-[10px] text-white/40">Expected</div>
                        <pre className="mb-1 whitespace-pre-wrap font-mono text-[11px] text-white/70">
                          {r.expected}
                        </pre>
                      </>
                    )}
                    <div className="text-[10px] text-white/40">Your output</div>
                    <pre className="whitespace-pre-wrap font-mono text-[11px] text-brand-100">
                      {r.stdout || <span className="text-white/30">(no output)</span>}
                    </pre>
                    {r.stderr && (
                      <>
                        <div className="mt-1 text-[10px] text-red-300/60">Stderr</div>
                        <pre className="whitespace-pre-wrap font-mono text-[11px] text-red-300/80">
                          {r.stderr}
                        </pre>
                      </>
                    )}
                  </div>
                ))}
              </div>
            )}

            {consoleTab === 'result' && !runResult && result && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-3"
              >
                <div className="flex items-baseline gap-3">
                  <div className={`text-base font-semibold ${verdictColor(result.status)}`}>
                    {verdictLabel(result.status)}
                  </div>
                  <div className="text-[11px] text-white/50">
                    {result.passed}/{result.total} tests passed · {result.runtime_ms} ms
                    {result.status === 'accepted' && ` · +${result.xp_awarded} XP`}
                  </div>
                </div>

                {result.compile_error && (
                  <pre className="overflow-x-auto rounded-md border border-amber-500/30 bg-amber-500/10 p-2 font-mono text-[11px] text-amber-200">
                    {result.compile_error}
                  </pre>
                )}

                {result.failing_test && (
                  <div className="rounded-md border border-red-500/30 bg-red-500/5 p-2">
                    <div className="mb-1 text-[10px] uppercase tracking-wider text-red-300/80">
                      Failed on test {result.failing_test.index + 1}
                    </div>
                    {result.failing_test.stdin && (
                      <>
                        <div className="text-[10px] text-white/40">Input</div>
                        <pre className="mb-1 whitespace-pre-wrap font-mono text-[11px] text-white/70">
                          {result.failing_test.stdin}
                        </pre>
                      </>
                    )}
                    {result.failing_test.expected != null && (
                      <>
                        <div className="text-[10px] text-white/40">Expected</div>
                        <pre className="mb-1 whitespace-pre-wrap font-mono text-[11px] text-white/70">
                          {result.failing_test.expected}
                        </pre>
                      </>
                    )}
                    <div className="text-[10px] text-white/40">Your output</div>
                    <pre className="whitespace-pre-wrap font-mono text-[11px] text-brand-100">
                      {result.failing_test.stdout || <span className="text-white/30">(no output)</span>}
                    </pre>
                    {result.failing_test.stderr && (
                      <>
                        <div className="mt-1 text-[10px] text-red-300/60">Stderr</div>
                        <pre className="whitespace-pre-wrap font-mono text-[11px] text-red-300/80">
                          {result.failing_test.stderr}
                        </pre>
                      </>
                    )}
                  </div>
                )}

                {result.status === 'accepted' && (
                  <div className="rounded-md border border-emerald-500/30 bg-emerald-500/10 p-3 text-emerald-200">
                    All {result.total} test cases passed. Nice work — hit the next problem.
                  </div>
                )}
              </motion.div>
            )}
          </div>
        </div>
      </div>

      <HintChat problemId={problem.id} userCode={code} />
    </div>
  );
}
