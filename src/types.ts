export type ScreenType =
  | 'landing'
  | 'subjects'
  | 'sections'
  | 'topics'
  | 'exam-info'
  | 'test'
  | 'result'
  | 'practice'
  | 'dashboard'
  | 'login'
  | 'register'
  | 'verify-email'
  | 'profile'
  | 'ranking'
  | 'packages'
  | 'about'
  | 'contact'
  | 'privacy'
  | 'terms';

export type PlanId = 'free' | 'premium' | 'school';

export interface AuthUser {
  id: string;
  fullName: string;
  email: string;
  /** ISO tarix: qeydiyyat vaxtı */
  createdAt: string;
  emailVerified: boolean;
  /** Profil şəkli (data URL). Backend hazır olanda şəkil URL-i olacaq. */
  avatarUrl?: string;
  plan: PlanId;
}

export type SubjectId = 'math' | 'aze' | 'eng';

export interface SubjectInfo {
  id: SubjectId;
  name: string;
  shortDesc: string;
  iconName: string;
  totalQuestions: number;
  completedQuestions: number;
  readinessScore: number;
  lastScore: string;
  lastDate: string;
  topicCount: number;
}

export interface TopicItem {
  id: string;
  subjectId: SubjectId;
  name: string;
  questionCount: number;
  masteryPercentage: number;
  status: 'mastered' | 'learning' | 'weak';
}

export interface TestQuestion {
  id: number;
  subject: string;
  topic: string;
  /** Oxu mətni (Reading sualları) */
  passage?: string;
  text: string;
  /** Çertyoj (SVG mətni, həndəsə sualları) */
  image?: string;
  /** 'single' — variantlı sual (default), 'open' — cavab yazılır */
  kind?: 'single' | 'open';
  options: {
    key: OptionKey;
    text: string;
  }[];
  /** Variantlı sualda düzgün variant */
  correctAnswer?: OptionKey;
  /** Açıq sualda düzgün cavab */
  openAnswer?: string;
  explanation: {
    summary: string;
    steps: string[];
    rule: string;
  };
}

export interface WeakTopic {
  id: string;
  subject: string;
  name: string;
  accuracy: number;
  mistakeCount: number;
  urgency: 'high' | 'medium';
  estimatedTime: string;
  questionCount: number;
  difficulty: 'Asan' | 'Orta' | 'Çətin';
}

export interface SavedMistake {
  id: string;
  subject: string;
  topic: string;
  questionPreview: string;
  userAnswer: string;
  correctAnswer: string;
  date: string;
  status: 'Yeni' | 'Təkrar et' | 'Düzəldildi';
}

export interface PracticeCard {
  id: string;
  topic: string;
  subject: string;
  questionsCount: number;
  estimatedTime: string;
  difficulty: 'Orta' | 'Çətin' | 'Baza';
  description: string;
}

export interface ResultMistake {
  id: number;
  questionNumber: number;
  topic: string;
  questionText: string;
  studentAnswer: string;
  correctAnswer: string;
  aiExplanation: {
    summary: string;
    steps: string[];
    tip: string;
  };
}

export type OptionKey = 'A' | 'B' | 'C' | 'D' | 'E';
export type Grade = 9 | 10 | 11;
export type Difficulty = 'easy' | 'medium' | 'hard';
export type DifficultyChoice = Difficulty | 'mixed';

export interface Section {
  id: string;
  subjectId: SubjectId;
  grade?: Grade;
  name: string;
  description: string;
  /** true — bölmə mövzulara bölünmür, quizlər birbaşa göstərilir (Reading) */
  directQuizzes?: boolean;
}

export interface CatalogTopic {
  id: string;
  subjectId: SubjectId;
  sectionId: string;
  name: string;
  difficulty: Difficulty;
  questionCount: number;
  /** 0–100: istifadəçinin mövzu üzrə bilik səviyyəsi (mock) */
  mastery: number;
  /** Mövzu yalnız bu siniflərdə var (verilməyibsə — bütün siniflərdə) */
  grades?: Grade[];
}

export interface BankQuestion extends TestQuestion {
  /** Sual bankındakı mətn id-si, məs. g9-math-algebra-004 */
  code?: string;
  grade?: Grade;
  /** Quiz nömrəsi (1–3) */
  quiz?: number;
  sectionId?: string;
  topicId: string;
  difficulty: Difficulty;
}

export interface ExamSetup {
  grade: Grade;
  /** Seçilmiş quiz (1–3). Təyin olunubsa, imtahan həmin quizin sabit suallarından ibarətdir */
  quiz?: number;
  subjectId: SubjectId;
  sectionId?: string;
  topicIds: string[];
  difficulty: DifficultyChoice;
  questionCount: number;
}

export type ExamEndReason = 'manual' | 'time' | 'tab-switch';

export interface ExamSession {
  id: string;
  setup: ExamSetup;
  questionIds: number[];
  startedAt: number;
  durationSec: number;
  /** Variantlı sualda variant hərfi, açıq sualda yazılmış cavab */
  answers: Record<number, string>;
  flagged: number[];
  /** Pəncərədən çıxma anları (ms timestamp) */
  violations: number[];
  status: 'running' | 'finished';
  endReason?: ExamEndReason;
  finishedAt?: number;
  isDemo?: boolean;
}
