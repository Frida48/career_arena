import type { BankQuestion, ExamSession, ExamSetup } from '../types';
import { getQuestion } from '../data/questionBank';
import { correctValue, isCorrect, questionsOf } from '../data/questions';

/** İmtahan müddəti (dəqiqə) = sual sayı × 1,5. 30 sual → 45 dəqiqə. */
export const MINUTES_PER_QUESTION = 1.5;
export const MAX_VIOLATIONS = 3;
export const QUESTION_COUNT_OPTIONS = [10, 20, 30] as const;

export const examDurationMinutes = (questionCount: number) => questionCount * MINUTES_PER_QUESTION;
export const examDurationSec = (questionCount: number) =>
  Math.round(examDurationMinutes(questionCount) * 60);

export const formatMinutes = (minutes: number) =>
  Number.isInteger(minutes) ? `${minutes}` : minutes.toFixed(1).replace('.', ',');

export const formatClock = (totalSec: number) => {
  const safe = Math.max(0, Math.floor(totalSec));
  const m = Math.floor(safe / 60);
  const s = safe % 60;
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
};

export const DEFAULT_SETUP: ExamSetup = {
  grade: 9,
  subjectId: 'math',
  sectionId: undefined,
  topicIds: [],
  difficulty: 'mixed',
  questionCount: 30,
};

function shuffle<T>(list: T[]): T[] {
  const a = [...list];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/**
 * Sinif, fənn, bölmə, mövzu və çətinliyə görə sualları seçir (təsadüfi sıra ilə).
 * Seçim kifayət etməzsə, əvvəlcə həmin bölmədən, sonra fənnin digər bölmələrindən tamamlanır.
 */
export function pickQuestions(setup: ExamSetup): BankQuestion[] {
  const pool = questionsOf(setup.grade ?? 9, setup.subjectId);
  const inSection = (q: BankQuestion) => !setup.sectionId || q.sectionId === setup.sectionId;
  const matches = (q: BankQuestion) =>
    inSection(q) &&
    (setup.topicIds.length === 0 || setup.topicIds.includes(q.topicId)) &&
    (setup.difficulty === 'mixed' || q.difficulty === setup.difficulty);

  const primary = shuffle(pool.filter(matches));
  const sameSection = shuffle(pool.filter((q) => inSection(q) && !primary.includes(q)));
  const rest = shuffle(pool.filter((q) => !inSection(q)));
  const picked = [...primary, ...sameSection, ...rest].slice(0, setup.questionCount);
  return groupByPassage(picked);
}

/** Eyni oxu mətninə aid suallar ardıcıl gəlsin (mətn bir dəfə oxunub bir neçə suala cavab verilir) */
function groupByPassage(list: BankQuestion[]): BankQuestion[] {
  const order: (BankQuestion | BankQuestion[])[] = [];
  const groups = new Map<string, BankQuestion[]>();
  for (const q of list) {
    if (!q.passage) {
      order.push(q);
      continue;
    }
    const g = groups.get(q.passage);
    if (g) g.push(q);
    else {
      const ng = [q];
      groups.set(q.passage, ng);
      order.push(ng);
    }
  }
  return order.flat();
}

export type AnswerStatus = 'correct' | 'wrong' | 'blank';

export interface EvaluatedQuestion {
  index: number;
  question: BankQuestion;
  chosen?: string;
  status: AnswerStatus;
  flagged: boolean;
}

export interface Evaluation {
  items: EvaluatedQuestion[];
  total: number;
  correct: number;
  wrong: number;
  blank: number;
  percent: number;
  usedSec: number;
  weakTopics: { topicId: string; topic: string; wrong: number; total: number }[];
}

export function evaluate(session: ExamSession): Evaluation {
  const items: EvaluatedQuestion[] = [];
  session.questionIds.forEach((id, index) => {
    const question = getQuestion(id);
    if (!question) return;
    const chosen = session.answers[id];
    const status: AnswerStatus = !chosen
      ? 'blank'
      : isCorrect(question, chosen)
        ? 'correct'
        : 'wrong';
    items.push({ index, question, chosen, status, flagged: session.flagged.includes(id) });
  });

  const correct = items.filter((i) => i.status === 'correct').length;
  const wrong = items.filter((i) => i.status === 'wrong').length;
  const blank = items.filter((i) => i.status === 'blank').length;
  const total = items.length;

  const byTopic = new Map<string, { topic: string; wrong: number; total: number }>();
  items.forEach((i) => {
    const row = byTopic.get(i.question.topicId) ?? { topic: i.question.topic, wrong: 0, total: 0 };
    row.total += 1;
    if (i.status !== 'correct') row.wrong += 1;
    byTopic.set(i.question.topicId, row);
  });

  const end = session.finishedAt ?? Date.now();
  const usedSec = Math.min(
    session.durationSec,
    Math.max(0, Math.round((end - session.startedAt) / 1000)),
  );

  return {
    items,
    total,
    correct,
    wrong,
    blank,
    percent: total ? Math.round((correct / total) * 100) : 0,
    usedSec,
    weakTopics: [...byTopic.entries()]
      .map(([topicId, v]) => ({ topicId, ...v }))
      .filter((v) => v.wrong > 0)
      .sort((a, b) => b.wrong / b.total - a.wrong / a.total || b.wrong - a.wrong),
  };
}

/** Nəticə ekranını nümunə ilə göstərmək üçün (imtahan verilməyibsə) */
export function buildDemoSession(): ExamSession {
  const setup: ExamSetup = { ...DEFAULT_SETUP };
  const questions = pickQuestions(setup);
  const answers: Record<number, string> = {};
  questions.forEach((q, i) => {
    if (i % 7 === 6) return; // boş
    if (i % 4 === 3) {
      // yanlış
      answers[q.id] =
        q.kind === 'open' ? '0' : (q.options.find((o) => o.key !== q.correctAnswer)?.key ?? 'A');
      return;
    }
    answers[q.id] = correctValue(q); // doğru
  });
  const durationSec = examDurationSec(setup.questionCount);
  const startedAt = Date.now() - 38 * 60 * 1000;
  return {
    id: 'demo',
    setup,
    questionIds: questions.map((q) => q.id),
    startedAt,
    durationSec,
    answers,
    flagged: [],
    violations: [startedAt + 12 * 60 * 1000],
    status: 'finished',
    endReason: 'manual',
    finishedAt: startedAt + 38 * 60 * 1000,
    isDemo: true,
  };
}
