import { create } from 'zustand';
import { authApi } from '../api/endpoints';
import type { User } from '../types';

interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  user: User | null;
  setTokens: (access: string, refresh: string) => void;
  loadUser: () => Promise<void>;
  logout: () => void;
  hydrate: () => void;
}

const STORAGE_KEY = 'techpath.auth';

export const useAuthStore = create<AuthState>((set, get) => ({
  accessToken: null,
  refreshToken: null,
  user: null,

  setTokens: (access, refresh) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ access, refresh }));
    set({ accessToken: access, refreshToken: refresh });
    get().loadUser();
  },

  loadUser: async () => {
    try {
      const user = await authApi.me();
      set({ user });
    } catch {
      get().logout();
    }
  },

  logout: () => {
    localStorage.removeItem(STORAGE_KEY);
    set({ accessToken: null, refreshToken: null, user: null });
  },

  hydrate: () => {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    try {
      const { access, refresh } = JSON.parse(raw);
      set({ accessToken: access, refreshToken: refresh });
      get().loadUser();
    } catch {
      localStorage.removeItem(STORAGE_KEY);
    }
  },
}));
