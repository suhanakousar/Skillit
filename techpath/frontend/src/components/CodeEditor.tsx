import Editor from '@monaco-editor/react';
import { useEffect, useState } from 'react';
import type { ReactNode } from 'react';

interface Props {
  language: string;
  value: string;
  onChange: (val: string) => void;
  onRun?: () => void;
  onSubmit?: () => void;
  onReset?: () => void;
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
  onReset,
  running,
  submitting,
  availableLanguages = ['python', 'cpp', 'java', 'javascript'],
  onLanguageChange,
}: Props) {
  const [theme, setTheme] = useState<'vs-dark' | 'light'>('vs-dark');
  const [fontSize, setFontSize] = useState(14);

  // Keyboard shortcuts: Ctrl/Cmd+Enter = Run, Ctrl/Cmd+Shift+Enter = Submit
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        if (e.shiftKey) {
          onSubmit?.();
        } else {
          onRun?.();
        }
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [onRun, onSubmit]);

  return (
    <div className="flex h-full min-h-0 flex-col overflow-hidden rounded-xl border border-white/10 bg-ink-800 shadow-lg shadow-black/20">
      {/* Toolbar */}
      <div className="flex flex-shrink-0 items-center justify-between gap-2 border-b border-white/10 bg-ink-900/60 px-3 py-2">
        <div className="flex items-center gap-1.5">
          <select
            value={language}
            onChange={(e) => onLanguageChange?.(e.target.value)}
            className="rounded-md border border-white/10 bg-ink-800 px-2.5 py-1.5 text-xs font-medium text-white/90 outline-none transition hover:border-white/20 focus:border-brand-500"
          >
            {availableLanguages.map((l) => (
              <option key={l} value={l}>
                {LANG_LABELS[l] ?? l}
              </option>
            ))}
          </select>

          <div className="hidden items-center gap-1 sm:flex">
            <IconButton
              title={theme === 'vs-dark' ? 'Switch to light theme' : 'Switch to dark theme'}
              onClick={() => setTheme((t) => (t === 'vs-dark' ? 'light' : 'vs-dark'))}
            >
              {theme === 'vs-dark' ? '🌙' : '☀️'}
            </IconButton>
            <IconButton
              title="Decrease font size"
              onClick={() => setFontSize((s) => Math.max(10, s - 1))}
            >
              A−
            </IconButton>
            <IconButton
              title="Increase font size"
              onClick={() => setFontSize((s) => Math.min(24, s + 1))}
            >
              A+
            </IconButton>
            {onReset && (
              <IconButton title="Reset to starter code" onClick={onReset}>
                ↺
              </IconButton>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2">
          {onRun && (
            <button
              onClick={onRun}
              disabled={running || submitting}
              title="Run sample tests (Ctrl+Enter)"
              className="flex items-center gap-1.5 rounded-md border border-white/10 bg-white/5 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {running ? (
                <>
                  <span className="h-3 w-3 animate-spin rounded-full border-2 border-white/20 border-t-white" />
                  Running
                </>
              ) : (
                <>
                  <svg className="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M6 4.75c0-.55.6-.89 1.06-.6l8.25 5.25a.7.7 0 0 1 0 1.2l-8.25 5.25A.7.7 0 0 1 6 15.25V4.75Z" />
                  </svg>
                  Run
                </>
              )}
            </button>
          )}
          {onSubmit && (
            <button
              onClick={onSubmit}
              disabled={submitting || running}
              title="Submit all tests (Ctrl+Shift+Enter)"
              className="flex items-center gap-1.5 rounded-md bg-brand-600 px-4 py-1.5 text-xs font-semibold text-white shadow-md shadow-brand-900/40 transition hover:bg-brand-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {submitting ? (
                <>
                  <span className="h-3 w-3 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                  Submitting
                </>
              ) : (
                <>
                  <svg className="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm3.86-9.14a.75.75 0 0 0-1.22-.87l-3.24 4.53L7.53 10.4a.75.75 0 1 0-1.06 1.06l3 3a.75.75 0 0 0 1.14-.09l4.25-6Z" clipRule="evenodd" />
                  </svg>
                  Submit
                </>
              )}
            </button>
          )}
        </div>
      </div>

      <div className="min-h-0 flex-1">
        <Editor
          height="100%"
          language={MONACO_LANG[language] ?? 'plaintext'}
          value={value}
          onChange={(v) => onChange(v ?? '')}
          theme={theme}
          options={{
            fontSize,
            fontFamily: 'JetBrains Mono, ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
            fontLigatures: true,
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 4,
            lineNumbersMinChars: 3,
            padding: { top: 12, bottom: 12 },
            smoothScrolling: true,
            cursorBlinking: 'smooth',
            renderLineHighlight: 'all',
            bracketPairColorization: { enabled: true },
          }}
        />
      </div>
    </div>
  );
}

function IconButton({ children, onClick, title }: { children: ReactNode; onClick: () => void; title: string }) {
  return (
    <button
      onClick={onClick}
      title={title}
      className="flex h-7 w-7 items-center justify-center rounded-md text-xs text-white/60 transition hover:bg-white/10 hover:text-white"
    >
      {children}
    </button>
  );
}
