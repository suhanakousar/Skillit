import Editor from '@monaco-editor/react';
import { useState } from 'react';

interface Props {
  language: string;
  value: string;
  onChange: (val: string) => void;
  onRun?: () => void;
  onSubmit?: () => void;
  running?: boolean;
  submitting?: boolean;
  availableLanguages?: string[];
  onLanguageChange?: (lang: string) => void;
}

const LANG_LABELS: Record<string, string> = {
  python: 'Python',
  cpp: 'C++',
  java: 'Java',
  javascript: 'JavaScript',
  c: 'C',
  go: 'Go',
};

const MONACO_LANG: Record<string, string> = {
  python: 'python',
  cpp: 'cpp',
  java: 'java',
  javascript: 'javascript',
  c: 'c',
  go: 'go',
};

export default function CodeEditor({
  language,
  value,
  onChange,
  onRun,
  onSubmit,
  running,
  submitting,
  availableLanguages = ['python', 'cpp', 'java', 'javascript'],
  onLanguageChange,
}: Props) {
  const [theme, setTheme] = useState<'vs-dark' | 'light'>('vs-dark');

  return (
    <div className="flex h-full flex-col overflow-hidden rounded-xl border border-white/10 bg-ink-800">
      <div className="flex items-center justify-between border-b border-white/10 bg-ink-700 px-3 py-2">
        <div className="flex items-center gap-2">
          <select
            value={language}
            onChange={(e) => onLanguageChange?.(e.target.value)}
            className="rounded bg-ink-800 px-2 py-1 text-xs text-white/80 outline-none"
          >
            {availableLanguages.map((l) => (
              <option key={l} value={l}>
                {LANG_LABELS[l] ?? l}
              </option>
            ))}
          </select>
          <button
            onClick={() => setTheme((t) => (t === 'vs-dark' ? 'light' : 'vs-dark'))}
            className="rounded bg-ink-800 px-2 py-1 text-xs text-white/60 hover:text-white"
          >
            {theme === 'vs-dark' ? '🌙' : '☀️'}
          </button>
        </div>
        <div className="flex gap-2">
          {onRun && (
            <button
              onClick={onRun}
              disabled={running}
              className="rounded bg-white/10 px-3 py-1 text-xs font-medium text-white hover:bg-white/20 disabled:opacity-50"
            >
              {running ? 'Running…' : 'Run'}
            </button>
          )}
          {onSubmit && (
            <button
              onClick={onSubmit}
              disabled={submitting}
              className="rounded bg-brand-600 px-3 py-1 text-xs font-medium text-white hover:bg-brand-500 disabled:opacity-50"
            >
              {submitting ? 'Submitting…' : 'Submit'}
            </button>
          )}
        </div>
      </div>
      <div className="flex-1 min-h-[300px]">
        <Editor
          height="100%"
          language={MONACO_LANG[language] ?? 'plaintext'}
          value={value}
          onChange={(v) => onChange(v ?? '')}
          theme={theme}
          options={{
            fontSize: 14,
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 4,
          }}
        />
      </div>
    </div>
  );
}
