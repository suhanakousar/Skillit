import { useEffect, useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
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

const DIFFICULTY_META: Record<number, { label: string; className: string }> = {
  1: { label: 'Easy', className: 'text-emerald-300 bg-emerald-500/10 ring-emerald-500/20' },
  2: { label: 'Easy+', className: 'text-emerald-200 bg-emerald-500/10 ring-emerald-500/20' },
  3: { label: 'Medium', className: 'text-yellow-300 bg-yellow-500/10 ring-yellow-500/20' },
  4: { label: 'Hard-', className: 'text-orange-300 bg-orange-500/10 ring-orange-500/20' },
  5: { label: 'Hard', className: 'text-red-300 bg-red-500/10 ring-red-500/20' },
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

function verdictBg(status: string): string {
  if (status === 'accepted') return 'bg-emerald-500/10 ring-emerald-500/30';
  if (status === 'wrong_answer') return 'bg-red-500/10 ring-red-500/30';
  if (status === 'compile_error') return 'bg-amber-500/10 ring-amber-500/30';
  return 'bg-orange-500/10 ring-orange-500/30';
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

  const resetCode = () => {
    if (!problem) return;
    setCode(problem.starter_code_json[language] ?? STARTER_BY_LANG[language] ?? '');
    toast.info('Code reset', 'Back to the starter template');
  };

  const run = async () => {
    if (!problem) return;
    setRunning(true);
    setResult(null);
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
    setRunResult(null);
    setConsoleTab('result');
    try {
      const r = await submissionsApi.submit(problem.id, language, code);
      setResult(r);
      if (r.status === 'accepted') {
        toast.success('Accepted', `+${r.xp_awarded} XP · ${r.runtime_ms} ms · ${r.passed}/${r.total} tests`);
        loadUser();
      } else {
        toast.error(verdictLabel(r.status), `${r.passed}/${r.total} tests passed`);
      }
    } catch (err: any) {
      toast.error('Submission failed', err?.response?.data?.detail ?? 'Try again');
    } finally {
      setSubmitting(false);
    }
  };

  if (!problem) {
    return (
      <div className="grid h-[calc(100vh-3rem)] grid-cols-1 gap-4 p-4 lg:grid-cols-2">
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

  const difficulty = DIFFICULTY_META[problem.difficulty] ?? DIFFICULTY_META[3];

  return (
    <div className="flex h-[calc(100vh-3rem)] flex-col gap-3 p-3 lg:p-4">
      {/* Top bar */}
      <div className="flex flex-shrink-0 items-center justify-between gap-3 rounded-xl border border-white/5 bg-ink-800/80 px-4 py-2.5 backdrop-blur">
        <div className="flex min-w-0 items-center gap-3">
          <Link
            to="/problems"
            className="flex items-center gap-1 rounded-md px-2 py-1 text-xs text-white/60 transition hover:bg-white/5 hover:text-white"
          >
            <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
            Problems
          </Link>
          <div className="h-4 w-px bg-white/10" />
          <h1 className="truncate text-sm font-semibold text-white">{problem.title}</h1>
          <span className={`flex-shrink-0 rounded-full px-2 py-0.5 text-[10px] font-medium ring-1 ring-inset ${difficulty.className}`}>
            {difficulty.label}
          </span>
        </div>
        <div className="flex items-center gap-1.5 text-[10px] text-brand-200">
          <svg className="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 0 0 .95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 0 0-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.539 1.118l-2.8-2.034a1 1 0 0 0-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 0 0-.363-1.118L2.98 8.719c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 0 0 .951-.69l1.07-3.292Z" />
          </svg>
          <span className="font-semibold">{problem.xp_reward} XP</span>
        </div>
      </div>

      {/* Split workspace */}
      <div className="grid min-h-0 flex-1 grid-cols-1 gap-3 lg:grid-cols-2">
        {/* LEFT: description / hints / submissions */}
        <div className="flex min-h-0 flex-col overflow-hidden rounded-2xl border border-white/5 bg-ink-800">
          <div className="flex flex-shrink-0 gap-1 border-b border-white/5 bg-ink-900/40 px-4 pt-3">
            {(['description', 'hints', 'submissions'] as Tab[]).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`rounded-t-lg px-3 py-2 text-xs font-medium capitalize transition ${
                  tab === t
                    ? 'bg-ink-800 text-white shadow-sm'
                    : 'text-white/50 hover:text-white/80'
                }`}
              >
                {t}
              </button>
            ))}
          </div>

          <div className="flex-1 overflow-y-auto p-5 scrollbar-thin">
            {tab === 'description' && (
              <div className="space-y-5 text-sm text-white/80">
                <div className="flex flex-wrap gap-1.5">
                  {problem.tags.map((t) => (
                    <span
                      key={t}
                      className="rounded-md bg-white/5 px-2 py-0.5 text-[10px] font-medium text-white/60 ring-1 ring-inset ring-white/10"
                    >
                      {t}
                    </span>
                  ))}
                </div>

                <p className="whitespace-pre-line leading-relaxed text-white/80">{problem.description}</p>

                {examples.length > 0 && (
                  <div className="space-y-3">
                    <h3 className="text-[11px] font-semibold uppercase tracking-wider text-white/50">
                      Examples
                    </h3>
                    {examples.map((ex, i) => (
                      <div
                        key={i}
                        className="overflow-hidden rounded-lg border border-white/10 bg-ink-900"
                      >
                        <div className="border-b border-white/5 bg-white/5 px-3 py-1.5 text-[10px] font-medium uppercase tracking-wider text-white/50">
                          Example {i + 1}
                        </div>
                        <div className="space-y-2 p-3">
                          <div>
                            <div className="text-[10px] font-medium uppercase text-white/40">Input</div>
                            <pre className="mt-1 whitespace-pre-wrap font-mono text-[11px] text-brand-100">{ex.input}</pre>
                          </div>
                          <div>
                            <div className="text-[10px] font-medium uppercase text-white/40">Output</div>
                            <pre className="mt-1 whitespace-pre-wrap font-mono text-[11px] text-emerald-200">{ex.output}</pre>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {problem.constraints_text && (
                  <div className="space-y-1.5">
                    <h3 className="text-[11px] font-semibold uppercase tracking-wider text-white/50">
                      Constraints
                    </h3>
                    <p className="rounded-md border border-white/10 bg-ink-900 p-3 font-mono text-[11px] text-white/60">
                      {problem.constraints_text}
                    </p>
                  </div>
                )}
              </div>
            )}

            {tab === 'hints' && (
              <div className="space-y-3 text-sm text-white/70">
                <div className="rounded-lg border border-brand-500/20 bg-brand-600/10 p-3 text-xs text-brand-100">
                  💡 Use the floating button at the bottom-right to chat with the AI hint coach — it gives
                  progressive nudges without spoiling the answer.
                </div>
                <div className="space-y-2">
                  {problem.hints_json.map((h) => (
                    <details
                      key={h.level}
                      className="group rounded-lg border border-white/10 bg-ink-900 p-3 open:bg-ink-900/80"
                    >
                      <summary className="flex cursor-pointer items-center justify-between text-xs font-medium text-white/80">
                        <span>Built-in hint {h.level}</span>
                        <span className="text-white/30 transition group-open:rotate-180">▼</span>
                      </summary>
                      <p className="mt-2 text-xs leading-relaxed text-white/60">{h.text}</p>
                    </details>
                  ))}
                </div>
              </div>
            )}

            {tab === 'submissions' && (
              <div className="space-y-2 text-xs">
                {!result ? (
                  <p className="text-white/50">No submissions yet. Hit Submit on the right to grade your code.</p>
                ) : (
                  <div className={`rounded-lg p-4 ring-1 ring-inset ${verdictBg(result.status)}`}>
                    <div className={`text-sm font-semibold ${verdictColor(result.status)}`}>
                      {verdictLabel(result.status)}
                    </div>
                    <div className="mt-2 grid grid-cols-2 gap-3 text-[11px] text-white/70">
                      <div>
                        <div className="text-white/40">Tests</div>
                        <div className="font-mono text-white">{result.passed}/{result.total}</div>
                      </div>
                      <div>
                        <div className="text-white/40">Runtime</div>
                        <div className="font-mono text-white">{result.runtime_ms} ms</div>
                      </div>
                      <div>
                        <div className="text-white/40">XP earned</div>
                        <div className="font-mono text-brand-200">+{result.xp_awarded}</div>
                      </div>
                      <div>
                        <div className="text-white/40">Language</div>
                        <div className="font-mono text-white">{language}</div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* RIGHT: editor + console */}
        <div className="flex min-h-0 flex-col gap-3">
          <div className="min-h-0 flex-1">
            <CodeEditor
              language={language}
              value={code}
              onChange={setCode}
              onLanguageChange={setLanguage}
              onRun={run}
              onSubmit={submit}
              onReset={resetCode}
              running={running}
              submitting={submitting}
            />
          </div>

          {/* Console */}
          <div className="flex h-[40%] min-h-[220px] flex-shrink-0 flex-col overflow-hidden rounded-xl border border-white/10 bg-ink-800">
            <div className="flex flex-shrink-0 items-center gap-1 border-b border-white/10 bg-ink-900/50 px-3 pt-2">
              {(['testcases', 'result'] as ConsoleTab[]).map((t) => (
                <button
                  key={t}
                  onClick={() => setConsoleTab(t)}
                  className={`rounded-t-md px-3 py-1.5 text-xs font-medium capitalize transition ${
                    consoleTab === t
                      ? 'bg-ink-800 text-white shadow-sm'
                      : 'text-white/50 hover:text-white/80'
                  }`}
                >
                  {t === 'testcases' ? 'Testcase' : 'Result'}
                </button>
              ))}
              <div className="ml-auto flex items-center gap-2 pb-1 pr-1 text-[10px] text-white/40">
                {running && (
                  <span className="flex items-center gap-1 text-yellow-300">
                    <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-yellow-300" />
                    Running
                  </span>
                )}
                {submitting && (
                  <span className="flex items-center gap-1 text-brand-200">
                    <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-brand-300" />
                    Submitting
                  </span>
                )}
                {!running && !submitting && <span>Idle</span>}
              </div>
            </div>

            <div className="flex-1 overflow-y-auto p-4 text-xs scrollbar-thin">
              {consoleTab === 'testcases' && (
                <div className="space-y-3">
                  <label className="flex items-center gap-2 text-white/70">
                    <input
                      type="checkbox"
                      checked={useCustomStdin}
                      onChange={(e) => setUseCustomStdin(e.target.checked)}
                      className="h-3.5 w-3.5 rounded border-white/20 bg-ink-900 accent-brand-500"
                    />
                    Use custom input
                  </label>

                  {useCustomStdin ? (
                    <textarea
                      value={customStdin}
                      onChange={(e) => setCustomStdin(e.target.value)}
                      placeholder="Type stdin exactly as the program will receive it"
                      className="h-28 w-full resize-none rounded-md border border-white/10 bg-ink-900 p-3 font-mono text-[11px] text-brand-100 outline-none transition focus:border-brand-500"
                    />
                  ) : examples.length === 0 ? (
                    <p className="text-white/50">No sample cases for this problem.</p>
                  ) : (
                    <>
                      <div className="flex flex-wrap gap-1.5">
                        {examples.map((_, i) => (
                          <button
                            key={i}
                            onClick={() => setActiveCaseIdx(i)}
                            className={`rounded-md px-2.5 py-1 text-[11px] font-medium transition ${
                              i === activeCaseIdx
                                ? 'bg-brand-600 text-white shadow-sm'
                                : 'bg-ink-900 text-white/50 hover:bg-ink-700 hover:text-white/80'
                            }`}
                          >
                            Case {i + 1}
                          </button>
                        ))}
                      </div>
                      <div>
                        <div className="mb-1 text-[10px] font-medium uppercase tracking-wider text-white/40">Input</div>
                        <pre className="rounded-md border border-white/10 bg-ink-900 p-3 font-mono text-[11px] text-brand-100">
                          {examples[activeCaseIdx]?.input}
                        </pre>
                      </div>
                      <div>
                        <div className="mb-1 text-[10px] font-medium uppercase tracking-wider text-white/40">Expected</div>
                        <pre className="rounded-md border border-white/10 bg-ink-900 p-3 font-mono text-[11px] text-emerald-200/80">
                          {examples[activeCaseIdx]?.output}
                        </pre>
                      </div>
                    </>
                  )}
                </div>
              )}

              {consoleTab === 'result' && !runResult && !result && (
                <div className="flex h-full flex-col items-center justify-center gap-2 text-center">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-white/5">
                    <svg className="h-5 w-5 text-white/30" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M8 5.25a.75.75 0 0 1 1.2-.6l8 6a.75.75 0 0 1 0 1.2l-8 6A.75.75 0 0 1 8 17.25v-12Z" />
                    </svg>
                  </div>
                  <p className="text-xs text-white/50">
                    Hit <kbd className="rounded border border-white/20 bg-white/5 px-1.5 py-0.5 font-mono text-[10px] text-white/80">Run</kbd> to test samples,
                    or <kbd className="rounded border border-white/20 bg-white/5 px-1.5 py-0.5 font-mono text-[10px] text-white/80">Submit</kbd> to grade all tests.
                  </p>
                </div>
              )}

              {consoleTab === 'result' && runResult && (
                <div className="space-y-3">
                  <div className={`flex items-center justify-between rounded-md p-3 ring-1 ring-inset ${verdictBg(runResult.status)}`}>
                    <div className={`text-sm font-semibold ${verdictColor(runResult.status)}`}>
                      {verdictLabel(runResult.status)}
                    </div>
                    <div className="flex gap-1">
                      {runResult.results.map((r) => (
                        <span
                          key={r.index}
                          title={`Case ${r.index + 1}: ${verdictLabel(r.status)}`}
                          className={`h-2 w-6 rounded-full ${
                            r.status === 'accepted' ? 'bg-emerald-400' : 'bg-red-400'
                          }`}
                        />
                      ))}
                    </div>
                  </div>
                  {runResult.compile_error && (
                    <pre className="overflow-x-auto rounded-md border border-amber-500/30 bg-amber-500/5 p-3 font-mono text-[11px] text-amber-200">
                      {runResult.compile_error}
                    </pre>
                  )}
                  {runResult.results.map((r) => (
                    <TestResultCard key={r.index} r={r} />
                  ))}
                </div>
              )}

              {consoleTab === 'result' && !runResult && result && (
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-3"
                >
                  {/* Headline */}
                  <div className={`rounded-lg p-4 ring-1 ring-inset ${verdictBg(result.status)}`}>
                    <div className="flex items-baseline justify-between gap-3">
                      <div className={`text-base font-semibold ${verdictColor(result.status)}`}>
                        {verdictLabel(result.status)}
                      </div>
                      <div className="text-[11px] text-white/60">
                        {result.runtime_ms} ms
                        {result.status === 'accepted' && ` · +${result.xp_awarded} XP`}
                      </div>
                    </div>

                    {/* Pass/fail progress bar */}
                    <div className="mt-3">
                      <div className="mb-1 flex items-center justify-between text-[10px] text-white/60">
                        <span>
                          {result.passed} / {result.total} tests passed
                        </span>
                        <span>{result.total ? Math.round((result.passed / result.total) * 100) : 0}%</span>
                      </div>
                      <div className="h-1.5 overflow-hidden rounded-full bg-white/10">
                        <div
                          className={`h-full transition-all ${
                            result.status === 'accepted' ? 'bg-emerald-400' : 'bg-red-400'
                          }`}
                          style={{ width: `${result.total ? (result.passed / result.total) * 100 : 0}%` }}
                        />
                      </div>
                    </div>
                  </div>

                  {result.compile_error && (
                    <pre className="overflow-x-auto rounded-md border border-amber-500/30 bg-amber-500/5 p-3 font-mono text-[11px] text-amber-200">
                      {result.compile_error}
                    </pre>
                  )}

                  {result.failing_test && (
                    <div className="overflow-hidden rounded-md border border-red-500/30 bg-red-500/5">
                      <div className="border-b border-red-500/20 bg-red-500/10 px-3 py-1.5 text-[10px] font-semibold uppercase tracking-wider text-red-300">
                        Failed on test {result.failing_test.index + 1}
                      </div>
                      <div className="space-y-2 p-3">
                        {result.failing_test.stdin && (
                          <div>
                            <div className="text-[10px] font-medium uppercase text-white/40">Input</div>
                            <pre className="mt-1 whitespace-pre-wrap font-mono text-[11px] text-white/70">
                              {result.failing_test.stdin}
                            </pre>
                          </div>
                        )}
                        {result.failing_test.expected != null && (
                          <div>
                            <div className="text-[10px] font-medium uppercase text-emerald-300/60">Expected</div>
                            <pre className="mt-1 whitespace-pre-wrap font-mono text-[11px] text-emerald-200/80">
                              {result.failing_test.expected}
                            </pre>
                          </div>
                        )}
                        <div>
                          <div className="text-[10px] font-medium uppercase text-red-300/60">Your Output</div>
                          <pre className="mt-1 whitespace-pre-wrap font-mono text-[11px] text-red-200">
                            {result.failing_test.stdout || <span className="text-white/30">(no output)</span>}
                          </pre>
                        </div>
                        {result.failing_test.stderr && (
                          <div>
                            <div className="text-[10px] font-medium uppercase text-red-300/60">Stderr</div>
                            <pre className="mt-1 whitespace-pre-wrap font-mono text-[11px] text-red-300/80">
                              {result.failing_test.stderr}
                            </pre>
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {result.status === 'accepted' && (
                    <div className="rounded-md border border-emerald-500/30 bg-emerald-500/10 p-4 text-center text-emerald-200">
                      <div className="text-lg">🎉</div>
                      <div className="mt-1 text-sm font-medium">All {result.total} tests passed</div>
                      <div className="mt-0.5 text-[11px] text-emerald-200/70">Nice work — on to the next problem.</div>
                    </div>
                  )}
                </motion.div>
              )}
            </div>
          </div>
        </div>
      </div>

      <HintChat problemId={problem.id} userCode={code} />
    </div>
  );
}

function TestResultCard({ r }: { r: { index: number; status: string; stdin?: string; expected?: string | null; stdout?: string; stderr?: string; runtime_ms?: number | null } }) {
  const pass = r.status === 'accepted';
  return (
    <div className={`overflow-hidden rounded-md border ${pass ? 'border-emerald-500/20' : 'border-red-500/20'} bg-ink-900`}>
      <div className={`flex items-center justify-between px-3 py-1.5 text-[11px] ${pass ? 'bg-emerald-500/5' : 'bg-red-500/5'}`}>
        <span className={`font-medium ${pass ? 'text-emerald-300' : 'text-red-300'}`}>
          {pass ? '✓' : '✗'} Case {r.index + 1} · {verdictLabel(r.status)}
        </span>
        {r.runtime_ms != null && <span className="text-white/40">{r.runtime_ms} ms</span>}
      </div>
      <div className="space-y-1.5 p-3">
        {r.stdin && (
          <div>
            <div className="text-[10px] font-medium uppercase text-white/40">Input</div>
            <pre className="mt-0.5 whitespace-pre-wrap font-mono text-[11px] text-white/70">{r.stdin}</pre>
          </div>
        )}
        {r.expected != null && (
          <div>
            <div className="text-[10px] font-medium uppercase text-emerald-300/60">Expected</div>
            <pre className="mt-0.5 whitespace-pre-wrap font-mono text-[11px] text-emerald-200/80">{r.expected}</pre>
          </div>
        )}
        <div>
          <div className={`text-[10px] font-medium uppercase ${pass ? 'text-emerald-300/60' : 'text-red-300/60'}`}>Your Output</div>
          <pre className={`mt-0.5 whitespace-pre-wrap font-mono text-[11px] ${pass ? 'text-emerald-200/80' : 'text-red-200'}`}>
            {r.stdout || <span className="text-white/30">(no output)</span>}
          </pre>
        </div>
        {r.stderr && (
          <div>
            <div className="text-[10px] font-medium uppercase text-red-300/60">Stderr</div>
            <pre className="mt-0.5 whitespace-pre-wrap font-mono text-[11px] text-red-300/80">{r.stderr}</pre>
          </div>
        )}
      </div>
    </div>
  );
}
