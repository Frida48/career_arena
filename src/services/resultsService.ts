/**
 * İmtahan nəticələri — backend API ilə.
 *   POST /api/results   imtahan nəticəsini saxlayır (eyni sessiya ikinci dəfə yazılmır)
 *   GET  /api/results   istifadəçinin son nəticələri
 */
import type { ExamSession, SubjectId } from '../types';
import type { Evaluation } from '../utils/exam';
import { api, getToken } from './authService';

export interface SavedResult {
  id: string;
  grade: number;
  subjectId: SubjectId;
  sectionId: string | null;
  total: number;
  correct: number;
  wrong: number;
  blank: number;
  percent: number;
  usedSec: number;
  endReason: string;
  violations: number;
  createdAt: string;
}

/** Daxil olmuş istifadəçinin nəticəsini serverə göndərir. Daxil olmayıbsa heç nə etmir. */
export async function saveResult(session: ExamSession, ev: Evaluation): Promise<void> {
  if (!getToken() || session.isDemo) return;
  await api('/results', {
    method: 'POST',
    body: {
      sessionId: session.id,
      grade: session.setup.grade,
      subjectId: session.setup.subjectId,
      sectionId: session.setup.sectionId,
      total: ev.total,
      correct: ev.correct,
      wrong: ev.wrong,
      usedSec: ev.usedSec,
      endReason: session.endReason,
      violations: session.violations.length,
    },
  });
}

export async function getMyResults(): Promise<SavedResult[]> {
  if (!getToken()) return [];
  const data = await api<{ results: SavedResult[] }>('/results');
  return data.results;
}
