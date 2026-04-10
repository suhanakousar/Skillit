import { useEffect, useState } from 'react';

export interface ContestLeaderboardRow {
  rank: number;
  user_id: string;
  name: string;
  college: string | null;
  points: number;
}

/**
 * Subscribes to the contest live leaderboard WebSocket.
 * Falls back to silent polling via onPollFallback if the socket can't connect.
 */
export function useContestLeaderboard(
  contestId: string | undefined,
  onPollFallback?: () => Promise<ContestLeaderboardRow[]>,
): ContestLeaderboardRow[] {
  const [board, setBoard] = useState<ContestLeaderboardRow[]>([]);

  useEffect(() => {
    if (!contestId) return;

    const proto = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const url = `${proto}://${window.location.host}/api/contests/${contestId}/live`;

    let ws: WebSocket | null = null;
    let pollId: ReturnType<typeof setInterval> | null = null;
    let cancelled = false;

    const startPolling = () => {
      if (!onPollFallback) return;
      const fetchOnce = async () => {
        try {
          const rows = await onPollFallback();
          if (!cancelled) setBoard(rows);
        } catch {
          /* swallow */
        }
      };
      fetchOnce();
      pollId = setInterval(fetchOnce, 10000);
    };

    try {
      ws = new WebSocket(url);
      ws.onmessage = (evt) => {
        try {
          const data = JSON.parse(evt.data);
          if (Array.isArray(data.leaderboard)) setBoard(data.leaderboard);
        } catch {
          /* ignore non-json */
        }
      };
      ws.onerror = () => {
        ws?.close();
        if (!cancelled) startPolling();
      };
      ws.onclose = () => {
        if (!cancelled && !pollId) startPolling();
      };
    } catch {
      startPolling();
    }

    return () => {
      cancelled = true;
      ws?.close();
      if (pollId) clearInterval(pollId);
    };
  }, [contestId, onPollFallback]);

  return board;
}
