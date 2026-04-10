import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { lessonsApi } from '../api/endpoints';
import type { Lesson as LessonType } from '../types';
import LessonStory from '../components/LessonStory';
import Skeleton from '../components/Skeleton';
import { toast } from '../store/toast';
import { useAuthStore } from '../store/auth';

export default function LessonPage() {
  const { lessonId } = useParams<{ lessonId: string }>();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState<LessonType | null>(null);
  const [completing, setCompleting] = useState(false);
  const loadUser = useAuthStore((s) => s.loadUser);

  useEffect(() => {
    if (!lessonId) return;
    lessonsApi.get(lessonId).then(setLesson);
  }, [lessonId]);

  if (!lesson) {
    return (
      <div className="mx-auto max-w-3xl space-y-4 rounded-2xl border border-white/5 bg-ink-800 p-8">
        <Skeleton className="h-8 w-2/3" />
        <Skeleton lines={5} />
      </div>
    );
  }

  const complete = async () => {
    setCompleting(true);
    try {
      const result = await lessonsApi.complete(lesson.id);
      toast.success(`+${result.xp_awarded} XP earned`, 'Lesson complete');
      result.new_badges.forEach((b) =>
        toast.info(`New badge: ${b.name}`, 'Check your profile'),
      );
      loadUser();
      navigate(`/track/${lesson.track_id}`);
    } catch (err: any) {
      toast.error('Could not save progress', err?.message ?? 'Try again');
    } finally {
      setCompleting(false);
    }
  };

  return <LessonStory lesson={lesson} onComplete={complete} completing={completing} />;
}
