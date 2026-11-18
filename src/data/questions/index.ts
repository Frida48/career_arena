// Sual bankı: 9–11-ci siniflər, riyaziyyat / Azərbaycan dili / ingilis dili.
// JSON faylları tools/question-gen/ skriptləri ilə yaradılır. Onları əl ilə redaktə etməyin,
// skripti dəyişib yenidən işə salın. Yeni grade*-*.json faylı avtomatik qoşulur.
import type {
  BankQuestion,
  CatalogTopic,
  Difficulty,
  Grade,
  OptionKey,
  Section,
  SubjectId,
} from '../../types';

/** JSON faylındakı sualın forması */
interface RawQuestion {
  id: string;
  grade: Grade;
  subject: RawSubject;
  sectionId: string;
  sectionTitle: string;
  topic: string;
  difficulty: Difficulty;
  passage?: string;
  text: string;
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
  sections: { id: string; title: string; description?: string; questions: RawQuestion[] }[];
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

/** Mövzu üzrə bilik səviyyəsi hələ hesablanmır — sabit nümunə dəyər (40–92) */
function mockMastery(seed: string): number {
  let h = 0;
  for (const ch of seed) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  return 40 + (h % 53);
}

function majority(list: Difficulty[]): Difficulty {
  const count = { easy: 0, medium: 0, hard: 0 };
  list.forEach((d) => (count[d] += 1));
  return (Object.keys(count) as Difficulty[]).sort((a, b) => count[b] - count[a])[0];
}

const sections: Section[] = [];
const topics: CatalogTopic[] = [];
const questions: BankQuestion[] = [];

let nextId = 1;
for (const bank of banks) {
  const subjectId = SUBJECT_ID[bank.subject];
  for (const sec of bank.sections) {
    const sectionId = `g${bank.grade}-${bank.subject}-${sec.id}`;
    sections.push({
      id: sectionId,
      subjectId,
      grade: bank.grade,
      name: sec.title,
      description: sec.description ?? '',
    });

    const topicIds = new Map<string, string>();
    const topicDiffs = new Map<string, Difficulty[]>();
    for (const q of sec.questions) {
      if (!topicIds.has(q.topic)) topicIds.set(q.topic, `${sectionId}-t${topicIds.size + 1}`);
      topicDiffs.set(q.topic, [...(topicDiffs.get(q.topic) ?? []), q.difficulty]);
      const isOpen = q.type === 'open';
      questions.push({
        id: nextId++,
        code: q.id,
        grade: bank.grade,
        sectionId,
        topicId: topicIds.get(q.topic)!,
        subject: SUBJECT_NAME[subjectId],
        topic: q.topic,
        difficulty: q.difficulty,
        passage: q.passage,
        text: q.text,
        kind: isOpen ? 'open' : 'single',
        options: isOpen ? [] : (q.options ?? []).map((text, i) => ({ key: KEYS[i], text })),
        correctAnswer: isOpen ? undefined : KEYS[q.correctIndex ?? 0],
        openAnswer: isOpen ? q.answer : undefined,
        explanation: { summary: q.explanation, steps: [], rule: '' },
      });
    }

    for (const [name, id] of topicIds) {
      const diffs = topicDiffs.get(name)!;
      topics.push({
        id,
        subjectId,
        sectionId,
        name,
        difficulty: majority(diffs),
        questionCount: diffs.length,
        mastery: mockMastery(id),
      });
    }
  }
}

export const BANK_SECTIONS = sections;
export const BANK_TOPICS = topics;
export const BANK_QUESTIONS = questions;

const byId = new Map(questions.map((q) => [q.id, q]));
export const getBankQuestion = (id: number) => byId.get(id);

export const questionsOf = (grade: Grade, subjectId: SubjectId) =>
  questions.filter((q) => q.grade === grade && sectionSubject(q.sectionId) === subjectId);

const sectionSubjectMap = new Map(sections.map((s) => [s.id, s.subjectId]));
function sectionSubject(sectionId?: string) {
  return sectionId ? sectionSubjectMap.get(sectionId) : undefined;
}

export const hasBank = (grade: Grade, subjectId: SubjectId) =>
  sections.some((s) => s.grade === grade && s.subjectId === subjectId);

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
