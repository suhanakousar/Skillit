import { create } from 'zustand';
import type { Branch, Goal, Language } from '../types';

interface SignupDraft {
  name: string;
  email: string;
  password: string;
  year: 1 | 2 | 3 | 4 | null;
  branch: Branch | null;
  goal: Goal | null;
  preferred_language: Language;
  college: string;
  step: number;
  setField: <K extends keyof Omit<SignupDraft, 'setField' | 'reset' | 'next' | 'prev' | 'step'>>(
    key: K,
    value: SignupDraft[K],
  ) => void;
  next: () => void;
  prev: () => void;
  reset: () => void;
}

export const useSignupDraft = create<SignupDraft>((set) => ({
  name: '',
  email: '',
  password: '',
  year: null,
  branch: null,
  goal: null,
  preferred_language: 'python',
  college: '',
  step: 1,
  setField: (key, value) => set((state) => ({ ...state, [key]: value })),
  next: () => set((state) => ({ step: Math.min(4, state.step + 1) })),
  prev: () => set((state) => ({ step: Math.max(1, state.step - 1) })),
  reset: () =>
    set({
      name: '',
      email: '',
      password: '',
      year: null,
      branch: null,
      goal: null,
      preferred_language: 'python',
      college: '',
      step: 1,
    }),
}));
