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

3 sinif × 3 fənn × 3–4 bölmə × 30 sual = **900 sual**, hamısı DİM buraxılış formatında yazılmış orijinal suallardır.

| Sinif | Riyaziyyat (4 bölmə) | Azərbaycan dili (3 bölmə) | İngilis dili (3 bölmə) |
| --- | --- | --- | --- |
| 9 | Ədədlər · Cəbr · Funksiyalar və silsilələr · Həndəsə, statistika | Fonetika və leksika · Morfologiya · Sintaksis | Grammar · Vocabulary · Reading |
| 10 | Tənliklər · Funksiyalar · Triqonometriya · Həndəsə və kombinatorika | Leksika və üslubiyyat · Morfologiya · Sadə cümlə | Grammar · Vocabulary · Reading |
| 11 | Üstlü və loqarifmik · Törəmə · İnteqral · Fəza həndəsəsi | Orfoqrafiya və nitq · Mürəkkəb cümlə · Mətn və durğu | Grammar · Vocabulary · Reading |

- Variantlı suallarda 5 variant (A–E) var, riyaziyyatda bəzi suallar açıqdır (cavab yazılır).
- Reading suallarında oxu mətni (`passage`) var; eyni mətnin sualları imtahanda ardıcıl gəlir.
- Riyaziyyat sualları şablonlardan kodla yaradılır, cavablar hesablanır. Dil sualları əl ilə yazılıb, yayımdan əvvəl fənn müəllimi yoxlasa yaxşı olar.
- Sualları dəyişmək üçün JSON-u yox, `tools/question-gen/` skriptlərini dəyişib yenidən işə salın.

## Səhifələr (URL-lər)

| URL | Səhifə |
| --- | --- |
| `/` | Ana səhifə (dairəvi 5 addımlıq animasiya daxil) |
| `/subjects` → `/sections` → `/topics` | Fənn → bölmə → mövzu və çətinlik seçimi |
| `/exam-info` → `/exam` → `/result` | İmtahan məlumat səhifəsi → imtahan (taymer, 30 sual) → nəticə və plagiat hesabatı |
| `/dashboard`, `/practice` | İnkişaf paneli, fərdi məşq |
| `/login`, `/register`, `/verify-email` | Giriş, qeydiyyat, e-poçt təsdiq kodu |
| `/profile` | Profil məlumatları, şəkil yükləmə, şifrə dəyişmə |
| `/ranking` | Ümumi reytinq və imtahan üzrə reytinq (ulduz və şərh) |
| `/packages` | Free, Premium və məktəb/kurs paketləri |
| `/about`, `/contact`, `/privacy`, `/terms` | Haqqımızda, əlaqə, məxfilik, şərtlər |

Hostinqdə (Vercel, Netlify) bütün yolların `index.html`-ə yönləndirilməsi lazımdır. `vercel.json` və `public/_redirects` bunun üçün hazırdır.

## Kod qaydaları

- **Palitra:** "Meşə yaşılı" (forest green + qızılı vurğu + isti krem fon). Rənglər `src/index.css`-də `@theme` tokenləri kimi saxlanır (`bg-brand`, `bg-ink`, `btn-gold`, `dark:bg-surface-dark` və s.). Rəngi dəyişmək üçün yalnız orada düzəliş edin, komponentlərdə `#hex` yazmayın.
- **Data** komponentlərin içində yox, `src/data/`-da saxlanır, tiplər `src/types.ts`-dədir.
- `npm run format`: Prettier ilə kodu formatlayır. `npm run lint`: TypeScript yoxlaması (`strict` rejim).

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
