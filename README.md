# Career Arena · Exam Arena

9–11-ci sinif şagirdləri üçün buraxılış imtahanlarına hazırlıq platforması: frontend, backend API və 900 suallıq sual bankı.

**Stack:** React 19 · TypeScript · Vite · Tailwind CSS 4 · lucide-react · motion · Node.js API (node:http + node:sqlite)

## İşə salmaq

Node.js **22.22+** lazımdır (https://nodejs.org). Başqa heç nə (verilənlər bazası serveri və s.) quraşdırmaq lazım deyil.

```bash
npm install
npm run dev      # sayt: http://localhost:3000, API: http://localhost:4000/api
```

| Əmr | Nə edir |
| --- | --- |
| `npm run dev` | API serveri və Vite-i birlikdə işə salır (lokal inkişaf üçün) |
| `npm run build` | tip yoxlaması + production build (`dist/`) |
| `npm start` | build edir və hər şeyi bir portda açır: http://localhost:4000 |
| `npm run server` | yalnız API serveri |
| `npm run validate:questions` | sual bankını yoxlayır (Python 3 lazımdır) |

Verilənlər bazası ilk işə salınanda avtomatik yaranır: `server/data/career-arena.db` (git-ə düşmür). Sıfırlamaq üçün bu faylı silin.

**E-poçt təsdiqi:** real e-poçt hələ qoşulmayıb. Qeydiyyatdan sonra 6 rəqəmli kod server konsoluna yazılır və `npm run dev` rejimində təsdiq səhifəsində də göstərilir.

## Quruluş

```
src/
  App.tsx                  # marşrutlar (react-router), ümumi çərçivə (Navbar, Geri, Footer), sessiya
  routes.ts                # ekran adı ↔ URL xəritəsi
  types.ts                 # bütün data modelləri (backend DTO-ları üçün əsas)
  context/ExamContext.tsx  # imtahan seçimləri və gedişi (sessionStorage-də saxlanır)
  hooks/useTheme.ts        # light/dark rejimi
  services/authService.ts  # auth API (qeydiyyat, giriş, e-poçt kodu, profil, şifrə)
  services/resultsService.ts # imtahan nəticələrinin serverdə saxlanması
  utils/exam.ts            # müddət (sual sayı × 1,5), sual seçimi, nəticənin hesablanması
  data/
    catalog.ts             # sinif → fənn → bölmə → mövzu (sual bankından avtomatik qurulur)
    questionBank.ts        # sual bankına giriş (getQuestion)
    community.ts           # reytinq, rəylər, paketlər (MOCK)
    examData.ts            # fənlər və ilkin sual datası (MOCK)
    questions/             # 9–11-ci siniflər üçün sual bankı (JSON + index.ts)
  components/              # Navbar, Footer, BackBar, Modal, Accordion, StarRating, FiveStepCycle, ...
  screens/                 # hər səhifə üçün bir fayl
  assets/                  # logo.png buraya qoyulur
server/
  index.js                 # API serveri (auth, profil, nəticələr, reytinq) + production-da dist/ statik faylları
  db.js                    # SQLite cədvəlləri
scripts/dev.mjs            # npm run dev: API + Vite birlikdə
tools/question-gen/        # sual bankının generatorları və validator (bax: oradakı README)
```

## Sual bankı

**11430 sual**, hamısı orijinal suallardır. Bütün fənlərdə 9 və 11-ci sinif — yalnız çətin, 10-cu sinif — orta və çətin. Kataloqdakı bölmə və mövzular bütün siniflər üçün eynidir, suallar isə sinfə (9, 10, 11) görə fərqlənir.

| Fənn | Mövzular | Hər sinifdə |
| --- | --- | --- |
| Riyaziyyat | 16 mövzu (ədədlər, cəbr, həndəsə, statistika və ehtimal) | 16 × 3 × 20 = 960 (11-ci sinif: 15 mövzu, 900) |
| Azərbaycan dili | 18 mövzu: fonetika, leksika, əsas nitq hissələri (6), köməkçi nitq hissələri (5), sintaksis, durğu işarələri | 18 × 3 quiz × 30 sual = 1620 |
| İngilis dili | Grammar (10 mövzu: tenses, conditionals, passive, articles, quantifiers, nouns, adjectives, pronouns, numerals, adverbs), Vocabulary (3 mövzu: word formation, phrasal verbs, prepositions and prepositional phrases) + Reading | 13 × 3 quiz × 30 sual + Reading 10 × 8 = 1250 |

- **Quizlər:** mövzu səhifəsində hər mövzunun altında «Quiz 1 / 2 / 3» düymələri var. Bir neçə mövzu seçib qarışıq sınaq da qurmaq olar.
- **Reading** mövzulara bölünmür: hər sinif üçün 10 quiz, hər quizdə bir orijinal mətn və ona aid 8 sual.
- İngilis dili qrammatika və lüğət sualları çoxtələblidir (bir neçə boşluq birlikdə, düzgün cümlə, 11-ci sinifdə «hər iki cümləsi düzgün olan variant»); səhv variantların əksəriyyətində yalnız bir hissə səhvdir.
- Variantlı suallarda 5 variant (A–E) var, riyaziyyatda bəzi suallar açıqdır (cavab yazılır).
- Riyaziyyatda «Orta qiymət və moda» mövzusu 11-ci sinifdə yoxdur; həndəsə suallarının bir hissəsində çertyoj (SVG, JSON-da `image` sahəsi) var.
- Azərbaycan dili sualları cümlə daxilindədir və çoxşərtlidir; cavablar işarələnmiş cümlə korpusundan (hər söz: nitq hissəsi, növ, hal, cümlə üzvü) və fonetika/orfoqrafiya qaydalarından hesablanır, şərt hər variantda yenidən yoxlanır.
- Riyaziyyat cavabları kodla iki dəfə hesablanır: düsturla və müstəqil üsulla (sadalama, koordinatlar, ədədi yoxlama); uyğun gəlməsə generator dayanır. Azərbaycan dilinin fonetik və morfoloji sualları qaydalarla (ahəng qanunu, şəkilçilər) qurulur, qalan dil sualları yoxlanılmış banklardandır. Yayımdan əvvəl fənn müəllimi baxsa yaxşı olar.
- Sualları dəyişmək üçün JSON-u yox, `tools/question-gen/` skriptlərini dəyişib yenidən işə salın.

## Backend

API `server/index.js`-dədir, xarici paket istifadə etmir. Şifrələr `scrypt` ilə hash olunur, sessiya tokenləri və təsdiq kodları bazada hash kimi saxlanır.

| Endpoint | Təsvir |
| --- | --- |
| `POST /api/auth/register` | `{ fullName, email, password }` → `{ user, token }` |
| `POST /api/auth/login` | `{ email, password }` → `{ user, token }` |
| `POST /api/auth/logout` | sessiyanı bitirir |
| `POST /api/auth/verify-email` | `{ code }` → `{ user }` (15 dəq etibarlı, 5 cəhd) |
| `POST /api/auth/resend-code` | yeni kod |
| `GET /api/me`, `PATCH /api/me` | profil (`fullName`, `avatarUrl`) |
| `POST /api/me/password` | `{ currentPassword, newPassword }` |
| `POST /api/results`, `GET /api/results` | imtahan nəticəsini saxlamaq / öz nəticələri |
| `GET /api/ranking?subject=&grade=` | düzgün cavablara görə reytinq |

Autentifikasiya: `Authorization: Bearer <token>`.

## Qeydlər

- **İmtahan müddəti** = sual sayı × 1,5 dəqiqə (30 sual → 45 dəq). Hesablama `src/utils/exam.ts`-dədir.
- **Tab dəyişmə:** imtahan pəncərəsindən 3 dəfə çıxılsa, imtahan dayandırılır (`MAX_VIOLATIONS`). Pozuntu sayı nəticə ilə serverə göndərilir.
- **Hələ nümunə (mock) olan hissələr:** inkişaf paneli və fərdi məşq qrafikləri, reytinqdəki digər şagirdlər (sənin sətrin real nəticələrdən hesablanır), rəylər (brauzerdə saxlanır), plagiat hesabatı, mövzu üzrə «bilik səviyyəsi» faizləri, paketlər/ödəniş.
- **E-poçt:** yayımdan əvvəl `issueCode()` funksiyasına (server/index.js) real e-poçt göndərmə əlavə edilməlidir.
- **Profil şəkli** data URL kimi bazada saxlanır; çox istifadəçi olanda fayl yükləmə xidmətinə keçmək məsləhətdir.
- **Əlaqə məlumatları** (`info@careerarena.az`, telefon, ünvan) və **hüquqi mətnlər** (məxfilik, şərtlər) nümunədir. Yayımlamazdan əvvəl real məlumatla əvəz edin və hüquqşünas yoxlasın.
- **Hostinq:** `npm start` frontend və API-ni bir serverdə açır (VPS, Render, Railway və s.). Vercel/Netlify yalnız statik saytı saxlayır, API üçün ayrıca server lazımdır.
