# Sual bankının generatoru

`src/data/questions/grade{9,10,11}-{math,az,en}.json` faylları bu qovluqdakı skriptlərlə yaradılır. Bütün suallar orijinaldır. Riyaziyyatda 9 və 11-ci sinif yalnız çətin, 10-cu sinif orta və çətin suallardan ibarətdir; 11-ci sinif sualları çoxaddımlıdır.

Quruluş: **sinif → mövzu → 3 quiz × 20 sual** (Azərbaycan dili: **3 quiz × 30 sual**). İstisna Reading-dir: **3 quiz × 10 sual**, hər quiz bir mətn.

| Fayl | Nə edir |
| --- | --- |
| `q_math.py` | Riyaziyyat: `m_num.py` (ədədlər), `m_alg.py` (cəbr, ardıcıllıqlar), `m_geo.py` (həndəsə + çertyojlar), `m_stat.py` (statistika, ehtimal) şablonlarını yığır |
| `mbuild.py`, `mx.py` | Riyaziyyat qurucusu: hər cavab müstəqil üsulla (`chk`) yoxlanır, oxşar variantlar, siniflər arasında unikal mətn |
| `svg.py` | Həndəsə çertyojları (real koordinatlardan, `currentColor`) |
| `q_az.py` | Azərbaycan dili, 18 mövzu × 90 sual (3 × 30): `az_phon.py` (fonetik təhlil, transkripsiyadan yazılış), `az_lex.py` (sinonim/antonim/omonim, frazeologizm), `az_pos.py` (11 nitq hissəsi), `az_synt.py` (cümlə üzvləri, mürəkkəb cümlə, durğu işarələri) |
| `az_corpus.py` | İşarələnmiş cümlə korpusu (hər sinif ayrı): nitq hissəsi, növ, hal, cümlə üzvü |
| `az_forms.py`, `az_morph.py` | İsim (mənsubiyyət + hal) və feil (zaman, şəxs, inkar) formaları — qaydalarla |
| `azbuild.py` | Azərbaycan dili qurucusu: şərt 5 variantda yenidən yoxlanır, düz bir variant doğru olmalıdır |
| `q_en.py` | İngilis dili, 5 mövzu. Feil cədvəli ilə zaman/şərt/məchul növ, söz yaradıcılığı və frazal feil bankları |
| `en_passages.py` | Reading mətnləri (hər sinif üçün 3 mətn × 10 sual) |
| `quiz.py` | Ümumi çərçivə: 60 unikal sual → 3 quiz (çətinlik qarışıq paylanır) |
| `common.py` | Formatlama, variantların qarışdırılması, Azərbaycan şəkilçiləri (3-cü, 6-cı, 2-yə…) |
| `validate.py` | Say, unikal id, 5 fərqli variant, cavab indeksi, çətinlik və təkrarların yoxlanması |

```bash
cd tools/question-gen
python3 q_math.py && python3 q_az.py && python3 q_en.py
python3 validate.py
```

Python 3.10+ lazımdır, əlavə paket tələb olunmur. Generatorlar sabit `seed` ilə işləyir, ona görə hər dəfə eyni suallar çıxır.

## Sual formatı

```json
{ "grade": 10, "subject": "math", "topics": [ { "topicId": "alg-quad", "quizzes": [[ { "id": "...", "difficulty": "hard", "text": "...", "type": "single", "options": ["…5 variant…"], "correctIndex": 2, "explanation": "..." } ]] } ] }
```

- `type: "single"` — `options` (5 variant) və `correctIndex` (0–4)
- `type: "open"` — `answer` (rəqəm və ya ifadə, mətn kimi)
- Reading suallarında `passage` sahəsi var.
- Həndəsə suallarında `image` (SVG mətni) ola bilər.

Mövzu id-ləri `src/data/catalog.ts`-dəki ilə eynidir. Loader: `src/data/questions/index.ts`.
