import type { CatalogTopic, Difficulty, Grade, Section, SubjectId } from '../types';

/**
 * Bölmələr: Fənn → Bölmə → Mövzu. Bölmə və mövzular hər sinif (9, 10, 11) üçün eynidir, suallar isə
 * sinfə görə fərqlənir (src/data/questions). Hər mövzuda 3 quiz × 20 sual var; Reading bölməsi
 * mövzulara bölünmür — orada 3 quiz × 10 sual (hər quiz bir mətn).
 */
export const SECTIONS: Section[] = [
  {
    id: 'math-num',
    subjectId: 'math',
    name: 'Ədədlər və hesablama',
    description: 'Həqiqi ədədlər, kəsrlər, qüvvət, modul və faizlər.',
  },
  {
    id: 'math-alg',
    subjectId: 'math',
    name: 'Cəbr',
    description: 'Tənliklər, tənliklər sistemi, kvadrat tənliklər, proqresiyalar və funksiyalar.',
  },
  {
    id: 'math-geo',
    subjectId: 'math',
    name: 'Həndəsə',
    description: 'Üçbucaqlar, çoxbucaqlılar, çevrə və triqonometriya.',
  },
  {
    id: 'math-stat',
    subjectId: 'math',
    name: 'Statistika və ehtimal',
    description: 'Orta qiymət, moda və ehtimal nəzəriyyəsinin əsasları.',
  },
  {
    id: 'aze-phon',
    subjectId: 'aze',
    name: 'Fonetika və orfoqrafiya',
    description: 'Səs və hərf sistemi, düzgün yazı qaydaları.',
  },
  {
    id: 'aze-lex',
    subjectId: 'aze',
    name: 'Leksika',
    description: 'Söz ehtiyatı, sinonim, antonim və frazeoloji birləşmələr.',
  },
  {
    id: 'aze-morph',
    subjectId: 'aze',
    name: 'Morfologiya',
    description: 'Nitq hissələri və onların qrammatik xüsusiyyətləri.',
  },
  {
    id: 'aze-synt',
    subjectId: 'aze',
    name: 'Sintaksis',
    description: 'Cümlə quruluşu, cümlə üzvləri və mürəkkəb cümlələr.',
  },
  {
    id: 'eng-gram',
    subjectId: 'eng',
    name: 'Grammar',
    description: 'Zamanlar, şərt cümlələri və məchul növ.',
  },
  {
    id: 'eng-vocab',
    subjectId: 'eng',
    name: 'Vocabulary',
    description: 'Söz yaradıcılığı və frazal feillər.',
  },
  {
    id: 'eng-read',
    subjectId: 'eng',
    name: 'Reading',
    description:
      'Hər quiz bir orijinal mətn və ona aid 10 sual: əsas fikir, detallar, söz mənası, nəticə çıxarma.',
    directQuizzes: true,
  },
];

const t = (
  id: string,
  subjectId: SubjectId,
  sectionId: string,
  name: string,
  difficulty: Difficulty,
  questionCount: number,
  mastery: number,
): CatalogTopic => ({ id, subjectId, sectionId, name, difficulty, questionCount, mastery });

export const CATALOG_TOPICS: CatalogTopic[] = [
  // Riyaziyyat · Ədədlər
  t('num-real', 'math', 'math-num', 'Həqiqi ədədlər', 'medium', 60, 88),
  t('num-frac', 'math', 'math-num', 'Kəsrlər', 'medium', 60, 81),
  t('num-pow', 'math', 'math-num', 'Dərəcə və qüvvət', 'medium', 60, 72),
  t('num-abs', 'math', 'math-num', 'Mütləq qiymət (Modul)', 'medium', 60, 66),
  t('num-pct', 'math', 'math-num', 'Faizlər', 'medium', 60, 62),
  // Riyaziyyat · Cəbr
  t('alg-eq', 'math', 'math-alg', 'Tənliklər', 'medium', 60, 84),
  t('alg-sys', 'math', 'math-alg', 'Tənliklər sistemi', 'medium', 60, 54),
  t('alg-quad', 'math', 'math-alg', 'Kvadrat tənliklər', 'medium', 60, 70),
  t('alg-prog', 'math', 'math-alg', 'Proqresiyalar', 'hard', 60, 47),
  t('alg-func', 'math', 'math-alg', 'Funksiyalar', 'medium', 60, 76),
  // Riyaziyyat · Həndəsə
  t('geo-basic', 'math', 'math-geo', 'Üçbucaqlar və bucaqlar', 'medium', 60, 68),
  t('geo-poly', 'math', 'math-geo', 'Çoxbucaqlılar', 'medium', 60, 73),
  t('geo-circle', 'math', 'math-geo', 'Çevrə və dairə', 'hard', 60, 58),
  t('geo-trig', 'math', 'math-geo', 'Trigonometriya', 'hard', 60, 51),
  // Riyaziyyat · Statistika
  t('stat-avg', 'math', 'math-stat', 'Orta qiymət və moda', 'medium', 60, 90),
  t('stat-prob', 'math', 'math-stat', 'Ehtimal nəzəriyyəsi', 'medium', 60, 64),
  // Azərbaycan dili
  t('aze-sound', 'aze', 'aze-phon', 'Səs və hərf', 'medium', 60, 86),
  t('aze-orth', 'aze', 'aze-phon', 'Orfoqrafiya qaydaları', 'medium', 60, 71),
  t('aze-syn', 'aze', 'aze-lex', 'Sinonim və antonim', 'medium', 60, 84),
  t('aze-idiom', 'aze', 'aze-lex', 'Frazeoloji birləşmələr', 'hard', 60, 55),
  t('aze-noun', 'aze', 'aze-morph', 'İsim və sifət', 'medium', 60, 80),
  t('aze-verb', 'aze', 'aze-morph', 'Feil və təsriflənməyən formalar', 'hard', 60, 52),
  t('aze-member', 'aze', 'aze-synt', 'Cümlənin üzvləri', 'medium', 60, 69),
  t('aze-complex', 'aze', 'aze-synt', 'Mürəkkəb cümlələr', 'hard', 60, 49),
  // English
  t('eng-tense', 'eng', 'eng-gram', 'Tenses', 'medium', 60, 66),
  t('eng-cond', 'eng', 'eng-gram', 'Conditionals', 'hard', 60, 48),
  t('eng-passive', 'eng', 'eng-gram', 'Passive voice', 'medium', 60, 61),
  t('eng-word', 'eng', 'eng-vocab', 'Word formation', 'medium', 60, 70),
  t('eng-phrasal', 'eng', 'eng-vocab', 'Phrasal verbs', 'hard', 60, 53),
  t('eng-reading', 'eng', 'eng-read', 'Reading', 'hard', 30, 60),
];

export const getSection = (id?: string) => SECTIONS.find((s) => s.id === id);
export const getTopic = (id: string) => CATALOG_TOPICS.find((x) => x.id === id);
/** Bölmələr bütün siniflər üçün eynidir (grade parametri gələcək üçün saxlanılıb) */
export const sectionsOf = (subjectId: SubjectId, _grade?: Grade) =>
  SECTIONS.filter((s) => s.subjectId === subjectId);
export const topicsOfSubject = (subjectId: SubjectId, _grade?: Grade) =>
  CATALOG_TOPICS.filter((t) => t.subjectId === subjectId);
export const topicsOf = (sectionId: string) =>
  CATALOG_TOPICS.filter((x) => x.sectionId === sectionId);

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
