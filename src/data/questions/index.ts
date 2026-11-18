// Sual bankı: 9–11-ci siniflər, riyaziyyat / Azərbaycan dili / ingilis dili.
// JSON faylları tools/question-gen/ skriptləri ilə yaradılır — əl ilə redaktə etməyin,
// skripti dəyişib yenidən işə salın.
import grade9Math from './grade9-math.json';
import grade9Az from './grade9-az.json';
import grade9En from './grade9-en.json';

export type Grade = 9 | 10 | 11;
export type BankSubject = 'math' | 'az' | 'en';
export type Difficulty = 'easy' | 'medium' | 'hard';

interface BaseQuestion {
  id: string;
  grade: Grade;
  subject: BankSubject;
  sectionId: string;
  sectionTitle: string;
  topic: string;
  difficulty: Difficulty;
  /** Oxu mətni (yalnız Reading suallarında) */
  passage?: string;
  text: string;
  explanation: string;
}

/** 5 variantlı qapalı sual */
export interface SingleChoiceQuestion extends BaseQuestion {
  type: 'single';
  options: string[];
  correctIndex: number;
}

/** Açıq (kodlaşdırıla bilən) sual — cavab mətn kimi müqayisə olunur */
export interface OpenQuestion extends BaseQuestion {
  type: 'open';
  answer: string;
}

export type BankQuestion = SingleChoiceQuestion | OpenQuestion;

export interface BankSection {
  id: string;
  title: string;
  questions: BankQuestion[];
}

export interface SubjectBank {
  grade: Grade;
  subject: BankSubject;
  sections: BankSection[];
}

export const questionBanks = [grade9Math, grade9Az, grade9En] as SubjectBank[];

export function getBank(grade: Grade, subject: BankSubject): SubjectBank | undefined {
  return questionBanks.find((b) => b.grade === grade && b.subject === subject);
}

export function getSectionQuestions(
  grade: Grade,
  subject: BankSubject,
  sectionId: string,
): BankQuestion[] {
  return getBank(grade, subject)?.sections.find((s) => s.id === sectionId)?.questions ?? [];
}

/** Açıq sualın cavabını yoxlayır (boşluq və vergül/nöqtə fərqi nəzərə alınmır). */
export function checkOpenAnswer(q: OpenQuestion, input: string): boolean {
  const norm = (s: string) => s.replace(/\s+/g, '').replace(',', '.').toLowerCase();
  return norm(q.answer) === norm(input);
}
