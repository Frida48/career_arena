// Sual bankı: 9–11-ci siniflər; hər mövzuda 3 quiz (riyaziyyatda «Orta qiymət və moda» 11-ci sinifdə yoxdur). Reading: 10 quiz × 8 sual, hər quiz bir mətn.
// JSON faylları tools/question-gen/ skriptləri ilə yaradılır. Onları əl ilə redaktə etməyin,
// skripti dəyişib yenidən işə salın. Yeni grade*-*.json faylı avtomatik qoşulur.
import type { BankQuestion, Difficulty, Grade, OptionKey, SubjectId } from '../../types';
import { CATALOG_TOPICS } from '../catalog';

/** JSON faylındakı sualın forması */
interface RawQuestion {
  id: string;
  difficulty: Difficulty;
  passage?: string;
  text: string;
  /** SVG çertyoj */
  image?: string;
  type: 'single' | 'open';
  options?: string[];
  correctIndex?: number;
  answer?: string;
  explanation: string;
}

type RawSubject = 'math' | 'az' | 'en';

interface RawBank {
  grade: Grade;
  subject: RawSubject;
  topics: { topicId: string; quizzes: RawQuestion[][] }[];
}

const SUBJECT_ID: Record<RawSubject, SubjectId> = { math: 'math', az: 'aze', en: 'eng' };
const SUBJECT_NAME: Record<SubjectId, string> = {
  math: 'Riyaziyyat',
  aze: 'Azərbaycan dili',
  eng: 'İngilis dili',
};
const KEYS: OptionKey[] = ['A', 'B', 'C', 'D', 'E'];
export const GRADES: Grade[] = [9, 10, 11];
const GRADE_LABEL: Record<Grade, string> = { 9: '9-cu', 10: '10-cu', 11: '11-ci' };
/** «9-cu», «10-cu», «11-ci» */
export const gradeLabel = (g: Grade) => GRADE_LABEL[g];

const files = import.meta.glob<RawBank>('./grade*-*.json', { eager: true, import: 'default' });
const banks = Object.values(files).sort(
  (a, b) => a.grade - b.grade || a.subject.localeCompare(b.subject),
);
const topicById = new Map(CATALOG_TOPICS.map((t) => [t.id, t]));

const questions: BankQuestion[] = [];
let nextId = 1;
for (const bank of banks) {
  const subjectId = SUBJECT_ID[bank.subject];
  for (const t of bank.topics) {
    const topic = topicById.get(t.topicId);
    t.quizzes.forEach((quiz, qi) => {
      for (const q of quiz) {
        const isOpen = q.type === 'open';
        questions.push({
          id: nextId++,
          code: q.id,
          grade: bank.grade,
          quiz: qi + 1,
          sectionId: topic?.sectionId,
          topicId: t.topicId,
          subject: SUBJECT_NAME[subjectId],
          topic: topic?.name ?? t.topicId,
          difficulty: q.difficulty,
          passage: q.passage,
          text: q.text,
          image: q.image,
          kind: isOpen ? 'open' : 'single',
          options: isOpen ? [] : (q.options ?? []).map((text, i) => ({ key: KEYS[i], text })),
          correctAnswer: isOpen ? undefined : KEYS[q.correctIndex ?? 0],
          openAnswer: isOpen ? q.answer : undefined,
          explanation: { summary: q.explanation, steps: [], rule: '' },
        });
      }
    });
  }
}

export const BANK_QUESTIONS = questions;

const byId = new Map(questions.map((q) => [q.id, q]));
export const getBankQuestion = (id: number) => byId.get(id);

const subjectOfTopic = (topicId: string) => topicById.get(topicId)?.subjectId;

/** Sinif və fənn üzrə bütün suallar */
export const questionsOf = (grade: Grade, subjectId: SubjectId) =>
  questions.filter((q) => q.grade === grade && subjectOfTopic(q.topicId) === subjectId);

/** Mövzunun konkret quizi (sabit sıra ilə) */
export const quizQuestions = (grade: Grade, topicId: string, quiz: number) =>
  questions.filter((q) => q.grade === grade && q.topicId === topicId && q.quiz === quiz);

/** Mövzuda neçə quiz var və hər birində neçə sual */
export function quizzesOf(grade: Grade, topicId: string): { quiz: number; count: number }[] {
  const counts = new Map<number, number>();
  for (const q of questions) {
    if (q.grade === grade && q.topicId === topicId && q.quiz) {
      counts.set(q.quiz, (counts.get(q.quiz) ?? 0) + 1);
    }
  }
  return [...counts.entries()]
    .sort((a, b) => a[0] - b[0])
    .map(([quiz, count]) => ({ quiz, count }));
}

export const hasBank = (grade: Grade, subjectId: SubjectId) =>
  questions.some((q) => q.grade === grade && subjectOfTopic(q.topicId) === subjectId);

/** Sualın düzgün cavabı mətn kimi (variant hərfi və ya açıq cavab) */
export const correctValue = (q: BankQuestion) =>
  (q.kind === 'open' ? q.openAnswer : q.correctAnswer) ?? '';

const normalize = (s: string) =>
  s.replace(/\s+/g, '').replace(/,/g, '.').replace(/−/g, '-').toLowerCase();

/** Cavabı yoxlayır: açıq suallarda boşluq, vergül/nöqtə və mənfi işarəsi fərqi nəzərə alınmır */
export function isCorrect(q: BankQuestion, given: string | undefined): boolean {
  if (!given) return false;
  if (q.kind === 'open') return normalize(given) === normalize(q.openAnswer ?? '');
  return given === q.correctAnswer;
}
