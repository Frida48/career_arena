import type { CatalogTopic, Difficulty, Grade, Section, SubjectId } from '../types';

/**
 * Bölmələr: Fənn → Bölmə → Mövzu. Bölmə və mövzular hər sinif (9, 10, 11) üçün eynidir, suallar isə
 * sinfə görə fərqlənir (src/data/questions). Riyaziyyat və İngilis dilində hər mövzuda 3 quiz × 20 sual,
 * Azərbaycan dilində 3 quiz × 30 sual var; Reading bölməsi
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
    description: 'Tənliklər, tənliklər sistemi, kvadrat tənliklər, ardıcıllıqlar və funksiyalar.',
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
    description: 'Orta qiymət, moda, dispersiya və ehtimal nəzəriyyəsi (11-ci sinifdə yalnız ehtimal).',
  },
  {
    id: 'aze-phon',
    subjectId: 'aze',
    name: 'Fonetika və orfoqrafiya',
    description: 'Fonetik təhlil, səs və hərf; tələffüzə görə sözlərin düzgün yazılışı.',
  },
  {
    id: 'aze-lex',
    subjectId: 'aze',
    name: 'Leksika',
    description: 'Sinonim, antonim, omonim və frazeoloji birləşmələr — cümlə daxilində.',
  },
  {
    id: 'aze-main',
    subjectId: 'aze',
    name: 'Əsas nitq hissələri',
    description: 'İsim, sifət, say, əvəzlik, feil və zərf.',
  },
  {
    id: 'aze-aux',
    subjectId: 'aze',
    name: 'Köməkçi nitq hissələri',
    description: 'Qoşma, bağlayıcı, ədat, modal sözlər və nida.',
  },
  {
    id: 'aze-synt',
    subjectId: 'aze',
    name: 'Sintaksis',
    description: 'Cümlə üzvləri, sadə və mürəkkəb cümlələrin təhlili.',
  },
  {
    id: 'aze-punc',
    subjectId: 'aze',
    name: 'Durğu işarələri',
    description: 'Sadə və mürəkkəb cümlədə vergül, nöqtə, sual və nida işarələri.',
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
  grades?: Grade[],
): CatalogTopic => ({ id, subjectId, sectionId, name, difficulty, questionCount, mastery, grades });

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
  t('alg-prog', 'math', 'math-alg', 'Ardıcıllıqlar', 'hard', 60, 47),
  t('alg-func', 'math', 'math-alg', 'Funksiyalar', 'medium', 60, 76),
  // Riyaziyyat · Həndəsə
  t('geo-basic', 'math', 'math-geo', 'Üçbucaqlar və bucaqlar', 'medium', 60, 68),
  t('geo-poly', 'math', 'math-geo', 'Çoxbucaqlılar', 'medium', 60, 73),
  t('geo-circle', 'math', 'math-geo', 'Çevrə və dairə', 'hard', 60, 58),
  t('geo-trig', 'math', 'math-geo', 'Trigonometriya', 'hard', 60, 51),
  // Riyaziyyat · Statistika
  t('stat-avg', 'math', 'math-stat', 'Orta qiymət və moda', 'medium', 60, 90, [9, 10]),
  t('stat-prob', 'math', 'math-stat', 'Ehtimal nəzəriyyəsi', 'hard', 60, 64),
  // Azərbaycan dili
  t('aze-sound', 'aze', 'aze-phon', 'Səs və hərf (fonetik təhlil)', 'hard', 90, 86),
  t('aze-orth', 'aze', 'aze-phon', 'Orfoqrafiya qaydaları', 'hard', 90, 71),
  t('aze-syn', 'aze', 'aze-lex', 'Sinonim, antonim və omonim', 'hard', 90, 84),
  t('aze-idiom', 'aze', 'aze-lex', 'Frazeoloji birləşmələr', 'hard', 90, 55),
  // Azərbaycan dili · Əsas nitq hissələri
  t('aze-isim', 'aze', 'aze-main', 'İsim', 'hard', 90, 80),
  t('aze-sifet', 'aze', 'aze-main', 'Sifət', 'hard', 90, 74),
  t('aze-say', 'aze', 'aze-main', 'Say', 'hard', 90, 70),
  t('aze-evez', 'aze', 'aze-main', 'Əvəzlik', 'hard', 90, 66),
  t('aze-feil', 'aze', 'aze-main', 'Feil', 'hard', 90, 52),
  t('aze-zerf', 'aze', 'aze-main', 'Zərf', 'hard', 90, 61),
  // Azərbaycan dili · Köməkçi nitq hissələri
  t('aze-qosma', 'aze', 'aze-aux', 'Qoşma', 'hard', 90, 64),
  t('aze-bag', 'aze', 'aze-aux', 'Bağlayıcı', 'hard', 90, 67),
  t('aze-edat', 'aze', 'aze-aux', 'Ədat', 'hard', 90, 58),
  t('aze-modal', 'aze', 'aze-aux', 'Modal sözlər', 'hard', 90, 63),
  t('aze-nida', 'aze', 'aze-aux', 'Nida', 'hard', 90, 72),
  // Azərbaycan dili · Sintaksis və durğu işarələri
  t('aze-member', 'aze', 'aze-synt', 'Cümlənin üzvləri', 'hard', 90, 69),
  t('aze-complex', 'aze', 'aze-synt', 'Mürəkkəb cümlələr', 'hard', 90, 49),
  t('aze-punct', 'aze', 'aze-punc', 'Durğu işarələri', 'hard', 90, 57),
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
/** Mövzu bu sinifdə varmı (grades verilməyibsə — bütün siniflərdə) */
export const topicInGrade = (t: CatalogTopic, grade?: Grade) =>
  grade === undefined || !t.grades || t.grades.includes(grade);
/** Bölmələr bütün siniflər üçün eynidir (grade parametri gələcək üçün saxlanılıb) */
export const sectionsOf = (subjectId: SubjectId, _grade?: Grade) =>
  SECTIONS.filter((s) => s.subjectId === subjectId);
export const topicsOfSubject = (subjectId: SubjectId, grade?: Grade) =>
  CATALOG_TOPICS.filter((t) => t.subjectId === subjectId && topicInGrade(t, grade));
export const topicsOf = (sectionId: string, grade?: Grade) =>
  CATALOG_TOPICS.filter((x) => x.sectionId === sectionId && topicInGrade(x, grade));

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
