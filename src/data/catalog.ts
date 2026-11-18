import type { CatalogTopic, Difficulty, Grade, Section, SubjectId } from '../types';
import { BANK_SECTIONS, BANK_TOPICS } from './questions';

/**
 * Kataloq: Sinif → Fənn → Bölmə → Mövzu. Bölmə və mövzular sual bankından (src/data/questions)
 * avtomatik qurulur. Backend hazır olanda GET /subjects/:id/sections ilə əvəz oluna bilər.
 */
export const SECTIONS: Section[] = BANK_SECTIONS;
export const CATALOG_TOPICS: CatalogTopic[] = BANK_TOPICS;

export const getSection = (id?: string) => SECTIONS.find((s) => s.id === id);
export const getTopic = (id: string) => CATALOG_TOPICS.find((x) => x.id === id);
export const sectionsOf = (subjectId: SubjectId, grade: Grade) =>
  SECTIONS.filter((s) => s.subjectId === subjectId && s.grade === grade);
export const topicsOf = (sectionId: string) =>
  CATALOG_TOPICS.filter((x) => x.sectionId === sectionId);
export const topicsOfSubject = (subjectId: SubjectId, grade: Grade) => {
  const ids = new Set(sectionsOf(subjectId, grade).map((s) => s.id));
  return CATALOG_TOPICS.filter((t) => ids.has(t.sectionId));
};

export const DIFFICULTY_META: Record<
  Difficulty,
  { label: string; level: 1 | 2 | 3; description: string }
> = {
  easy: { label: 'Asan', level: 1, description: 'Əsas anlayışlar və bir addımlı tapşırıqlar.' },
  medium: { label: 'Orta', level: 2, description: 'Buraxılış imtahanının tipik sualları.' },
  hard: { label: 'Çətin', level: 3, description: 'Çoxaddımlı və yüksək bal üçün tapşırıqlar.' },
};

export const masteryStatus = (mastery: number): 'weak' | 'learning' | 'mastered' =>
  mastery < 60 ? 'weak' : mastery < 80 ? 'learning' : 'mastered';
